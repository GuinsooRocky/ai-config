#!/usr/bin/env ruby
# frozen_string_literal: true

require "fileutils"
require "json"
require "yaml"

HOME_DIR = File.expand_path("~")
CLAUDE_DIR = File.expand_path(ENV.fetch("CLAUDE_SOURCE_DIR", File.join(HOME_DIR, ".claude")))
PLUGIN_DIR = File.expand_path(ENV.fetch("CODEX_PLUGIN_OUTPUT", File.expand_path("..", __dir__)))
BRIDGE_DIR = File.expand_path(
  ENV.fetch("CLAUDE_BRIDGE_DIR", File.join(HOME_DIR, "Desktop/cc-memory/codex-ready/skills"))
)
CAPABILITY_CONFIG_PATH = File.expand_path(
  ENV.fetch("CONTINUITY_CAPABILITY_CONFIG", File.expand_path("../../../capabilities.json", __dir__))
)
CAPABILITY_CONFIG = JSON.parse(File.read(CAPABILITY_CONFIG_PATH, encoding: "UTF-8"))
PROFILE_NAME = ENV.fetch("CONTINUITY_PROFILE", CAPABILITY_CONFIG.fetch("defaultProfile"))
PROFILE = CAPABILITY_CONFIG.fetch("profiles").fetch(PROFILE_NAME)
BLOCKED_TERMS = CAPABILITY_CONFIG.fetch("blockedTerms", []).map { |term| term.to_s.downcase }.freeze
DESCRIPTION_OVERRIDES = CAPABILITY_CONFIG.fetch("descriptionOverrides", {}).freeze
GENERATED_SKILLS_DIR = File.join(PLUGIN_DIR, ".generated-skills")
EXPOSED_SKILLS_DIR = File.join(PLUGIN_DIR, "skills")
CATALOG_DIR = File.join(PLUGIN_DIR, "assets", "capabilities")

def frontmatter(path)
  text = File.read(path, encoding: "UTF-8")
  match = text.match(/\A---\n(.*?)\n---\n/m)
  return {} unless match

  YAML.safe_load(match[1], permitted_classes: [], aliases: false) || {}
rescue Psych::SyntaxError
  {}
end

def yaml_string(value)
  JSON.generate(value.to_s)
end

def write_skill(destination, name:, description:, heading:, body:, reference_name:, reference_source:)
  FileUtils.mkdir_p(File.join(destination, "references"))
  File.write(
    File.join(destination, "SKILL.md"),
    <<~MARKDOWN,
      ---
      name: #{name}
      description: #{yaml_string(description)}
      ---

      # #{heading}

      #{body}
    MARKDOWN
    encoding: "UTF-8"
  )
  FileUtils.cp(reference_source, File.join(destination, "references", reference_name))
end

def ensure_new(destination)
  abort("Refusing to overwrite existing path: #{destination}") if File.exist?(destination) || File.symlink?(destination)
end

def blocked_source?(source)
  real_source = File.realpath(source)
  candidates = if File.directory?(real_source)
                 Dir.glob(File.join(real_source, "**", "*"), File::FNM_DOTMATCH)
               else
                 [real_source]
               end

  candidates.unshift(real_source)
  candidates.any? do |candidate|
    folded_path = candidate.downcase
    next true if BLOCKED_TERMS.any? { |term| folded_path.include?(term) }
    next false unless File.file?(candidate)

    raw_bytes = File.binread(candidate)
    next false if raw_bytes.include?("\0".b)

    bytes = raw_bytes.downcase
    BLOCKED_TERMS.any? { |term| bytes.include?(term.b) }
  end
end

def replace_description(skill_md, description)
  text = File.read(skill_md, encoding: "UTF-8")
  match = text.match(/\A---\n(.*?)\n---\n/m)
  abort("Missing YAML frontmatter: #{skill_md}") unless match

  metadata = YAML.safe_load(match[1], permitted_classes: [], aliases: false) || {}
  metadata["description"] = description
  serialized = YAML.dump(metadata).sub(/\A---\s*\n/, "")
  body = text[match.end(0)..]
  File.write(skill_md, "---\n#{serialized}---\n#{body}", encoding: "UTF-8")
end

FileUtils.mkdir_p(GENERATED_SKILLS_DIR)
skipped_capabilities = 0

copied_skills = 0
Dir.glob(File.join(CLAUDE_DIR, "skills", "*")).sort.each do |source|
  name = File.basename(source)
  next unless File.directory?(source) || File.symlink?(source)
  unless File.exist?(source)
    warn("Skipping unavailable skill source: #{source}")
    skipped_capabilities += 1
    next
  end

  unless File.file?(File.join(File.realpath(source), "SKILL.md"))
    warn("Skipping skill directory without SKILL.md: #{source}")
    skipped_capabilities += 1
    next
  end

  if blocked_source?(source)
    skipped_capabilities += 1
    next
  end

  destination = File.join(GENERATED_SKILLS_DIR, name)
  ensure_new(destination)
  real_source = File.realpath(source)
  FileUtils.mkdir_p(destination)
  FileUtils.cp_r(Dir.glob(File.join(real_source, "{*,.*}"), File::FNM_DOTMATCH).reject { |path| [".", ".."].include?(File.basename(path)) }, destination)

  skill_md = File.join(destination, "SKILL.md")
  if File.file?(skill_md)
    text = File.read(skill_md, encoding: "UTF-8")
    text = text.gsub(/^disable[-_]model[-_]invocation:\s*true\s*$/, "disable-model-invocation: false")
    text << <<~NOTE unless text.include?("## Codex compatibility")

      ## Codex compatibility

      Preserve this workflow's intent and evidence rules. Translate Claude-specific tool names to the available Codex tools.
    NOTE
    File.write(skill_md, text, encoding: "UTF-8")
  end
  copied_skills += 1
end

converted_agents = 0
Dir.glob(File.join(CLAUDE_DIR, "agents", "*.md")).sort.each do |source|
  if blocked_source?(source)
    skipped_capabilities += 1
    next
  end

  metadata = frontmatter(source)
  original_name = metadata["name"].to_s.strip
  original_name = File.basename(source, ".md") if original_name.empty?
  name = "agent-#{original_name.downcase.gsub(/[^a-z0-9]+/, "-").gsub(/^-|-$/, "")}"
  destination = File.join(GENERATED_SKILLS_DIR, name)
  ensure_new(destination)
  description = metadata["description"].to_s.strip
  description = "Use the migrated Claude #{original_name} agent role in Codex." if description.empty?
  description = "Migrated Claude agent role. #{description} Use when the user names #{original_name}, requests this specialist, or invokes a workflow that requires it."
  body = <<~BODY
    Read `references/role.md` completely and preserve its role, scope, evidence requirements and output contract.

    When the user requests agent, delegated, parallel, panel or adversarial work, give the role to an independent Codex sub-agent if the current runtime permits it. Otherwise perform the role locally and state that it was not an independent agent. Do not hard-code a Claude model name; respect current concurrency and safety rules.
  BODY
  write_skill(destination, name: name, description: description, heading: "#{original_name} Agent", body: body, reference_name: "role.md", reference_source: source)
  converted_agents += 1
end

converted_workflows = 0
Dir.glob(File.join(CLAUDE_DIR, "workflows", "*.js")).sort.each do |source|
  if blocked_source?(source)
    skipped_capabilities += 1
    next
  end

  text = File.read(source, encoding: "UTF-8")
  original_name = text[/\bname:\s*['\"]([^'\"]+)['\"]/, 1] || File.basename(source, ".js")
  original_description = text[/\bdescription:\s*['\"]([^'\"]+)['\"]/, 1] || "Migrated Claude workflow #{original_name}."
  name = "workflow-#{original_name.downcase.gsub(/[^a-z0-9]+/, "-").gsub(/^-|-$/, "")}"
  destination = File.join(GENERATED_SKILLS_DIR, name)
  ensure_new(destination)
  description = "Run the migrated Claude #{original_name} workflow in Codex. #{original_description} Use when the user names #{original_name} or asks for its described end-to-end flow."
  body = <<~BODY
    Read `references/workflow.js` completely. Treat it as the authoritative orchestration specification, not as JavaScript to execute blindly.

    Reproduce its phases, role isolation, inputs, intermediate artifacts, verification gates and final output with current Codex tools. Resolve referenced Claude agents through the migrated `agent-*` skills. Use independent sub-agents only when requested and available. Preserve the workflow's stopping conditions.
  BODY
  write_skill(destination, name: name, description: description, heading: "#{original_name} Workflow", body: body, reference_name: "workflow.js", reference_source: source)
  converted_workflows += 1
end

converted_commands = 0
Dir.glob(File.join(CLAUDE_DIR, "commands", "*")).sort.each do |source|
  next unless File.file?(source)
  if blocked_source?(source)
    skipped_capabilities += 1
    next
  end

  metadata = frontmatter(source)
  original_name = File.basename(source, File.extname(source))
  name = "command-#{original_name.downcase.gsub(/[^a-z0-9]+/, "-").gsub(/^-|-$/, "")}"
  destination = File.join(GENERATED_SKILLS_DIR, name)
  ensure_new(destination)
  description = metadata["description"].to_s.strip
  description = "Run the migrated Claude /#{original_name} command behavior in Codex. #{description} Use when the user types /#{original_name} or asks for this command's behavior."
  body = <<~BODY
    Read `references/command.md` completely and carry out the command's user-facing workflow using current Codex tools. Preserve its interaction and output contract without assuming Claude-only UI controls exist.
  BODY
  write_skill(destination, name: name, description: description, heading: "/#{original_name} Command", body: body, reference_name: "command.md", reference_source: source)
  converted_commands += 1
end

{
  "ai-capability-router" => File.join(BRIDGE_DIR, "ai-capability-router"),
  "claude-compat" => File.join(BRIDGE_DIR, "claude-compat"),
  "recall-claude-history" => File.join(BRIDGE_DIR, "recall-claude-history")
}.each do |name, source|
  next unless File.directory?(source)
  if blocked_source?(source)
    skipped_capabilities += 1
    next
  end

  destination = File.join(GENERATED_SKILLS_DIR, name)
  ensure_new(destination)
  FileUtils.cp_r(source, destination)
end

generated = Dir.glob(File.join(GENERATED_SKILLS_DIR, "*", "SKILL.md")).to_h do |skill_md|
  [File.basename(File.dirname(skill_md)), File.dirname(skill_md)]
end
exposed_names = if PROFILE["exposeAll"]
                  generated.keys.sort
                else
                  PROFILE.fetch("exposedSkills")
                end
missing = exposed_names.reject { |name| generated.key?(name) }
abort("Profile #{PROFILE_NAME} references missing capabilities: #{missing.join(', ')}") unless missing.empty?

FileUtils.mkdir_p(EXPOSED_SKILLS_DIR)
FileUtils.mkdir_p(CATALOG_DIR)
generated.each do |name, source|
  destination_root = exposed_names.include?(name) ? EXPOSED_SKILLS_DIR : CATALOG_DIR
  FileUtils.mv(source, File.join(destination_root, name))
end
Dir.rmdir(GENERATED_SKILLS_DIR)

exposed_names.each do |name|
  description = DESCRIPTION_OVERRIDES[name]
  next unless description

  replace_description(File.join(EXPOSED_SKILLS_DIR, name, "SKILL.md"), description)
end

FileUtils.mkdir_p(File.join(PLUGIN_DIR, "assets"))
FileUtils.cp(CAPABILITY_CONFIG_PATH, File.join(PLUGIN_DIR, "assets", "capabilities.json"))

legacy_hooks = File.join(PLUGIN_DIR, "hooks", "legacy-claude")
FileUtils.mkdir_p(legacy_hooks)
Dir.glob(File.join(CLAUDE_DIR, "hooks", "*")).sort.each do |source|
  FileUtils.cp(source, legacy_hooks) if File.file?(source)
end

design_spec = File.join(CLAUDE_DIR, "design-spec")
FileUtils.mkdir_p(File.join(PLUGIN_DIR, "assets"))
FileUtils.cp_r(design_spec, File.join(PLUGIN_DIR, "assets", "design-spec")) if File.directory?(design_spec)
FileUtils.cp(File.join(CLAUDE_DIR, "RTK.md"), File.join(PLUGIN_DIR, "assets", "RTK.md")) if File.file?(File.join(CLAUDE_DIR, "RTK.md"))

build_summary = {
  profile: PROFILE_NAME,
  copied_skills: copied_skills,
  converted_agents: converted_agents,
  converted_workflows: converted_workflows,
  converted_commands: converted_commands,
  skipped_capabilities: skipped_capabilities,
  exposed_skills: Dir.glob(File.join(EXPOSED_SKILLS_DIR, "*", "SKILL.md")).length,
  catalog_capabilities: Dir.glob(File.join(CATALOG_DIR, "*", "SKILL.md")).length,
  total_capabilities: Dir.glob(File.join(PLUGIN_DIR, "{skills,assets/capabilities}", "*", "SKILL.md")).length
}
File.write(
  File.join(PLUGIN_DIR, "assets", "profile.json"),
  JSON.pretty_generate(build_summary) + "\n",
  encoding: "UTF-8"
)
puts JSON.pretty_generate(build_summary)
