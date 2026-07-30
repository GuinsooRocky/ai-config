#!/usr/bin/env ruby
# frozen_string_literal: true

require "json"
require "yaml"

repo_root = File.expand_path("..", __dir__)
plugin_root = File.expand_path(ARGV.fetch(0, File.join(repo_root, "plugins", "claude-continuity")))
config_path = File.join(repo_root, "capabilities.json")
config = JSON.parse(File.read(config_path, encoding: "UTF-8"))
profile_name = ENV.fetch("CONTINUITY_PROFILE", config.fetch("defaultProfile"))
profile = config.fetch("profiles").fetch(profile_name)
blocked_terms = config.fetch("blockedTerms", []).map { |term| term.to_s.downcase }

def skill_names(root)
  Dir.glob(File.join(root, "*", "SKILL.md")).map { |item| File.basename(File.dirname(item)) }.sort
end

def description_for(skill_md)
  text = File.read(skill_md, encoding: "UTF-8")
  match = text.match(/\A---\n(.*?)\n---\n/m)
  abort("Missing YAML frontmatter: #{skill_md}") unless match

  metadata = YAML.safe_load(match[1], permitted_classes: [], aliases: false) || {}
  metadata.fetch("description", "").to_s
end

exposed_root = File.join(plugin_root, "skills")
catalog_root = File.join(plugin_root, "assets", "capabilities")
manifest_path = File.join(plugin_root, ".codex-plugin", "plugin.json")
profile_path = File.join(plugin_root, "assets", "profile.json")
auto_mcp_path = File.join(plugin_root, ".mcp.json")

abort("Missing plugin manifest: #{manifest_path}") unless File.file?(manifest_path)
abort("Missing build profile: #{profile_path}") unless File.file?(profile_path)

manifest = JSON.parse(File.read(manifest_path, encoding: "UTF-8"))
abort("MCP must not auto-start from the portable core plugin") if manifest.key?("mcpServers")
abort("Plugin-root .mcp.json would be auto-discovered: #{auto_mcp_path}") if File.exist?(auto_mcp_path)

exposed = skill_names(exposed_root)
catalog = skill_names(catalog_root)
duplicates = exposed & catalog
abort("Capabilities appear in both exposed and catalog sets: #{duplicates.join(', ')}") unless duplicates.empty?

unless profile["exposeAll"]
  expected = profile.fetch("exposedSkills").sort
  missing = expected - exposed
  extra = exposed - expected
  abort("Profile mismatch. Missing: #{missing.join(', ')}; extra: #{extra.join(', ')}") unless missing.empty? && extra.empty?
end

blocked_hits = []
[exposed_root, catalog_root].each do |root|
  Dir.glob(File.join(root, "**", "*"), File::FNM_DOTMATCH).sort.each do |item|
    folded_path = item.downcase
    if blocked_terms.any? { |term| folded_path.include?(term) }
      blocked_hits << item
      next
    end
    next unless File.file?(item)

    raw_bytes = File.binread(item)
    next if raw_bytes.include?("\0".b)

    folded = raw_bytes.downcase
    blocked_hits << item if blocked_terms.any? { |term| folded.include?(term.b) }
  end
end
abort("Blocked capability content found: #{blocked_hits.first}") unless blocked_hits.empty?

description_chars = exposed.sum do |name|
  description_for(File.join(exposed_root, name, "SKILL.md")).length
end
max_chars = profile["maxDescriptionChars"]
if max_chars && description_chars > max_chars
  abort("Exposed descriptions use #{description_chars} chars; profile budget is #{max_chars}")
end

summary = JSON.parse(File.read(profile_path, encoding: "UTF-8"))
abort("Built profile is #{summary['profile']}, expected #{profile_name}") unless summary["profile"] == profile_name

puts JSON.pretty_generate(
  profile: profile_name,
  exposed_skills: exposed.length,
  catalog_capabilities: catalog.length,
  total_capabilities: exposed.length + catalog.length,
  exposed_description_chars: description_chars,
  description_budget_chars: max_chars
)
