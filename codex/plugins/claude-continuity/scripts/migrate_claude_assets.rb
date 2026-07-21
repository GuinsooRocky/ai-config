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
SKILLS_DIR = File.join(PLUGIN_DIR, "skills")

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

FileUtils.mkdir_p(SKILLS_DIR)

copied_skills = 0
Dir.glob(File.join(CLAUDE_DIR, "skills", "*")).sort.each do |source|
  name = File.basename(source)
  next unless File.directory?(source) || File.symlink?(source)

  destination = File.join(SKILLS_DIR, name)
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
  metadata = frontmatter(source)
  original_name = metadata["name"].to_s.strip
  original_name = File.basename(source, ".md") if original_name.empty?
  name = "agent-#{original_name.downcase.gsub(/[^a-z0-9]+/, "-").gsub(/^-|-$/, "")}"
  destination = File.join(SKILLS_DIR, name)
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
  text = File.read(source, encoding: "UTF-8")
  original_name = text[/\bname:\s*['\"]([^'\"]+)['\"]/, 1] || File.basename(source, ".js")
  original_description = text[/\bdescription:\s*['\"]([^'\"]+)['\"]/, 1] || "Migrated Claude workflow #{original_name}."
  name = "workflow-#{original_name.downcase.gsub(/[^a-z0-9]+/, "-").gsub(/^-|-$/, "")}"
  destination = File.join(SKILLS_DIR, name)
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

  metadata = frontmatter(source)
  original_name = File.basename(source, File.extname(source))
  name = "command-#{original_name.downcase.gsub(/[^a-z0-9]+/, "-").gsub(/^-|-$/, "")}"
  destination = File.join(SKILLS_DIR, name)
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
  "claude-compat" => File.join(BRIDGE_DIR, "claude-compat"),
  "recall-claude-history" => File.join(BRIDGE_DIR, "recall-claude-history")
}.each do |name, source|
  next unless File.directory?(source)

  destination = File.join(SKILLS_DIR, name)
  ensure_new(destination)
  FileUtils.cp_r(source, destination)
end

legacy_hooks = File.join(PLUGIN_DIR, "hooks", "legacy-claude")
FileUtils.mkdir_p(legacy_hooks)
Dir.glob(File.join(CLAUDE_DIR, "hooks", "*")).sort.each do |source|
  FileUtils.cp(source, legacy_hooks) if File.file?(source)
end

design_spec = File.join(CLAUDE_DIR, "design-spec")
FileUtils.mkdir_p(File.join(PLUGIN_DIR, "assets"))
FileUtils.cp_r(design_spec, File.join(PLUGIN_DIR, "assets", "design-spec")) if File.directory?(design_spec)
FileUtils.cp(File.join(CLAUDE_DIR, "RTK.md"), File.join(PLUGIN_DIR, "assets", "RTK.md")) if File.file?(File.join(CLAUDE_DIR, "RTK.md"))

puts JSON.pretty_generate(
  copied_skills: copied_skills,
  converted_agents: converted_agents,
  converted_workflows: converted_workflows,
  converted_commands: converted_commands,
  total_plugin_skills: Dir.glob(File.join(SKILLS_DIR, "*", "SKILL.md")).length
)
