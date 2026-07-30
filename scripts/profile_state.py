#!/usr/bin/env python3
"""Install and compare runtime-specific ai-config profiles."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "ai-config.json"
SKIP_NAMES = {".DS_Store", "__pycache__"}
SKIP_SUFFIXES = {".pyc"}


@dataclass(frozen=True)
class ProfileFile:
    source: Path
    target: Path
    content: bytes
    mode: int
    merge: str | None = None


def load_manifest() -> dict:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("schemaVersion") != 1:
        raise RuntimeError("Unsupported ai-config schemaVersion")
    return manifest


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def is_binary(content: bytes) -> bool:
    return b"\0" in content[:4096]


def validate_relative(path: Path) -> Path:
    if path.is_absolute() or not path.parts or any(part in (".", "..") for part in path.parts):
        raise RuntimeError(f"Unsafe profile path: {path}")
    return path


def blocked_skill_names(manifest: dict) -> set[str]:
    terms = [term.casefold().encode() for term in manifest.get("blockedTerms", [])]
    skills_root = ROOT / "skills"
    blocked: set[str] = set()
    if not skills_root.is_dir() or not terms:
        return blocked

    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        if any(term.decode() in skill_dir.name.casefold() for term in terms):
            blocked.add(skill_dir.name)
            continue
        for path in skill_dir.rglob("*"):
            if not path.is_file() or path.is_symlink():
                continue
            try:
                content = path.read_bytes()
            except OSError:
                blocked.add(skill_dir.name)
                break
            if is_binary(content):
                continue
            lowered = content.lower()
            if any(term in lowered for term in terms):
                blocked.add(skill_dir.name)
                break
    return blocked


def should_skip(relative: Path, manifest: dict, blocked_skills: set[str]) -> bool:
    if relative.name in SKIP_NAMES or relative.suffix in SKIP_SUFFIXES:
        return True
    terms = [term.casefold() for term in manifest.get("blockedTerms", [])]
    if any(term in part.casefold() for part in relative.parts for term in terms):
        return True
    if len(relative.parts) >= 2 and relative.parts[0] == "skills":
        return relative.parts[1] in blocked_skills
    return False


def read_portable_file(source: Path) -> tuple[bytes, int]:
    if source.is_symlink():
        resolved = source.resolve(strict=True)
        try:
            resolved.relative_to(ROOT)
        except ValueError as error:
            raise RuntimeError(f"Non-portable external symlink: {source}") from error
        source = resolved
    content = source.read_bytes()
    mode = 0o755 if source.stat().st_mode & stat.S_IXUSR else 0o644
    return content, mode


def collect_profile(profile: str) -> tuple[dict, dict[Path, ProfileFile], int]:
    manifest = load_manifest()
    definition = manifest.get("profiles", {}).get(profile)
    if not definition:
        raise RuntimeError(f"Unknown profile: {profile}")

    blocked_skills = blocked_skill_names(manifest) if profile == "claude" else set()
    files: dict[Path, ProfileFile] = {}

    for configured in definition.get("paths", []):
        configured_path = validate_relative(Path(configured))
        source_root = ROOT / configured_path
        if not source_root.exists():
            raise RuntimeError(f"Profile source is missing: {configured}")
        candidates = [source_root] if source_root.is_file() else sorted(source_root.rglob("*"))
        for source in candidates:
            if not source.is_file():
                continue
            relative = source.relative_to(ROOT)
            if should_skip(relative, manifest, blocked_skills):
                continue
            content, mode = read_portable_file(source)
            files[relative] = ProfileFile(source, relative, content, mode)

    for generated in definition.get("generated", []):
        source = ROOT / validate_relative(Path(generated["source"]))
        target = validate_relative(Path(generated["target"]))
        content, mode = read_portable_file(source)
        if target in files:
            raise RuntimeError(f"Duplicate profile target: {target}")
        files[target] = ProfileFile(source, target, content, mode, generated.get("merge"))

    return manifest, files, len(blocked_skills)


def profile_digest(files: dict[Path, ProfileFile]) -> str:
    digest = hashlib.sha256()
    for target, item in sorted(files.items(), key=lambda pair: pair[0].as_posix()):
        digest.update(target.as_posix().encode())
        digest.update(b"\0")
        digest.update(f"{item.mode:o}".encode())
        digest.update(b"\0")
        digest.update(item.content)
        digest.update(b"\0")
    return digest.hexdigest()


def source_commit() -> str:
    try:
        commit = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "--short=12", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        return f"{commit}-dirty" if dirty else commit
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def state_root() -> Path:
    configured = os.environ.get("AI_CONFIG_STATE_HOME")
    return Path(configured).expanduser() if configured else Path.home() / ".config" / "ai-config"


def receipt_path(profile: str) -> Path:
    return state_root() / "receipts" / f"{profile}.json"


def load_receipt(profile: str) -> dict | None:
    path = receipt_path(profile)
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def atomic_write(path: Path, content: bytes, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
        os.chmod(temporary_name, mode)
        os.replace(temporary_name, path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def write_receipt(
    profile: str,
    install_root: str | None = None,
    managed_files: list[dict] | None = None,
    managed_settings_keys: list[str] | None = None,
) -> dict:
    manifest, files, _ = collect_profile(profile)
    receipt = {
        "schemaVersion": 1,
        "profile": profile,
        "releaseVersion": manifest["version"],
        "profileDigest": profile_digest(files),
        "sourceCommit": source_commit(),
        "installedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    if install_root:
        receipt["installRoot"] = install_root
    if managed_files is not None:
        receipt["managedFiles"] = managed_files
    if managed_settings_keys is not None:
        receipt["managedSettingsKeys"] = managed_settings_keys
    path = receipt_path(profile)
    atomic_write(path, (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode())
    return receipt


def backup_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_symlink():
        destination.symlink_to(os.readlink(source))
    elif source.is_file():
        shutil.copy2(source, destination)
    else:
        raise RuntimeError(f"Cannot safely replace directory: {source}")


def install_claude(target_root: Path, dry_run: bool) -> int:
    manifest, files, blocked_count = collect_profile("claude")
    definition = manifest["profiles"]["claude"]
    digest = profile_digest(files)
    regular = {path: item for path, item in files.items() if not item.merge}
    merged = {path: item for path, item in files.items() if item.merge}
    previous = load_receipt("claude") or {}
    previous_files = {entry["path"]: entry for entry in previous.get("managedFiles", [])}
    current_paths = {path.as_posix() for path in regular}
    stale_paths = sorted(set(previous_files) - current_paths)
    for relative in stale_paths:
        validate_relative(Path(relative))

    added = updated = unchanged = archived = 0
    for relative, item in sorted(regular.items(), key=lambda pair: pair[0].as_posix()):
        target = target_root / relative
        if target.is_file() and not target.is_symlink() and sha256(target.read_bytes()) == sha256(item.content):
            unchanged += 1
        else:
            updated += int(target.exists() or target.is_symlink())
            added += int(not target.exists() and not target.is_symlink())

    for relative in stale_paths:
        target = target_root / relative
        archived += int(target.exists() or target.is_symlink())

    for relative, item in merged.items():
        if item.merge != "json-top-level":
            raise RuntimeError(f"Unsupported merge strategy: {item.merge}")
        incoming = json.loads(item.content.decode())
        allowed = set(definition.get("allowedSettingsKeys", []))
        unexpected = set(incoming) - allowed
        if unexpected:
            raise RuntimeError(f"Portable settings contain unmanaged keys: {sorted(unexpected)}")
        target = target_root / relative
        existing = json.loads(target.read_text(encoding="utf-8")) if target.is_file() else {}
        result = dict(existing)
        for key in previous.get("managedSettingsKeys", []):
            if key not in incoming:
                result.pop(key, None)
        result.update(incoming)
        rendered = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
        if target.is_file() and target.read_bytes() == rendered:
            unchanged += 1
        else:
            updated += int(target.exists())
            added += int(not target.exists())

    print(
        f"Claude profile {manifest['version']} ({digest[:12]}): "
        f"新增 {added}，更新 {updated}，不变 {unchanged}，归档旧文件 {archived}，"
        f"按规则排除 skill {blocked_count} 个。"
    )
    if dry_run:
        print(f"Dry run：不会修改 {target_root}。")
        return 0

    if target_root.resolve() == ROOT.resolve():
        raise RuntimeError("Repository root cannot also be CLAUDE_HOME; clone ai-config to a neutral path")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup_base = Path(
        os.environ.get("AI_CONFIG_BACKUP_HOME", Path.home() / ".ai-config-backups")
    ).expanduser()
    backup_root = backup_base / "claude" / timestamp
    backup_used = False

    for relative in stale_paths:
        target = target_root / relative
        if not target.exists() and not target.is_symlink():
            continue
        destination = backup_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(target), str(destination))
        backup_used = True

    managed_files: list[dict] = []
    for relative, item in sorted(regular.items(), key=lambda pair: pair[0].as_posix()):
        target = target_root / relative
        if target.is_file() and not target.is_symlink() and sha256(target.read_bytes()) == sha256(item.content):
            os.chmod(target, item.mode)
        else:
            if target.exists() or target.is_symlink():
                backup_file(target, backup_root / relative)
                backup_used = True
            atomic_write(target, item.content, item.mode)
        managed_files.append({"path": relative.as_posix(), "sha256": sha256(item.content)})

    managed_settings_keys: list[str] = []
    for relative, item in merged.items():
        incoming = json.loads(item.content.decode())
        target = target_root / relative
        existing = json.loads(target.read_text(encoding="utf-8")) if target.is_file() else {}
        result = dict(existing)
        for key in previous.get("managedSettingsKeys", []):
            if key not in incoming:
                result.pop(key, None)
        result.update(incoming)
        rendered = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
        if not target.is_file() or target.read_bytes() != rendered:
            if target.exists():
                backup_file(target, backup_root / relative)
                backup_used = True
            atomic_write(target, rendered, item.mode)
        managed_settings_keys.extend(sorted(incoming))

    write_receipt(
        "claude",
        str(target_root),
        managed_files,
        sorted(set(managed_settings_keys)),
    )
    backup_message = str(backup_root) if backup_used else "未产生备份（目标内容相同）"
    print(f"Claude-only 安装完成：{target_root}")
    print(f"备份：{backup_message}")
    return 0


def print_status(as_json: bool, selected_profile: str) -> int:
    manifest = load_manifest()
    result = {
        "repository": {
            "version": manifest["version"],
            "commit": source_commit(),
        },
        "profiles": {},
    }
    profiles = ("claude", "codex") if selected_profile == "all" else (selected_profile,)
    for profile in profiles:
        _, files, blocked_count = collect_profile(profile)
        digest = profile_digest(files)
        receipt = load_receipt(profile)
        if not receipt:
            state = "not-installed"
        elif receipt.get("profileDigest") == digest:
            state = "current" if receipt.get("releaseVersion") == manifest["version"] else "content-current"
        else:
            state = "update-available"
        result["profiles"][profile] = {
            "state": state,
            "repositoryDigest": digest,
            "installedVersion": receipt.get("releaseVersion") if receipt else None,
            "installedDigest": receipt.get("profileDigest") if receipt else None,
            "installedAt": receipt.get("installedAt") if receipt else None,
            "blockedSkills": blocked_count,
        }

    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(f"ai-config 仓库：{manifest['version']} ({result['repository']['commit']})")
    labels = {
        "not-installed": "未安装",
        "current": "已是最新",
        "content-current": "内容已是最新，仅发布版本号不同",
        "update-available": "有内容更新",
    }
    for profile in profiles:
        item = result["profiles"][profile]
        installed = item["installedVersion"] or "-"
        print(
            f"{profile.capitalize():6}：{labels[item['state']]}；"
            f"已装 {installed}；仓库指纹 {item['repositoryDigest'][:12]}"
        )
    return 0


def bump_version(part: str) -> int:
    manifest = load_manifest()
    pieces = manifest["version"].split(".")
    if len(pieces) != 3 or not all(piece.isdigit() for piece in pieces):
        raise RuntimeError("ai-config version must be strict x.y.z semver")
    major, minor, patch = map(int, pieces)
    if part == "major":
        major, minor, patch = major + 1, 0, 0
    elif part == "minor":
        minor, patch = minor + 1, 0
    else:
        patch += 1
    old = manifest["version"]
    manifest["version"] = f"{major}.{minor}.{patch}"
    atomic_write(MANIFEST_PATH, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode())
    print(f"ai-config version: {old} -> {manifest['version']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_parser = subparsers.add_parser("install-claude")
    install_parser.add_argument("--target")
    install_parser.add_argument("--dry-run", action="store_true")

    status_parser = subparsers.add_parser("status")
    status_parser.add_argument(
        "profile", nargs="?", choices=("claude", "codex", "all"), default="all"
    )
    status_parser.add_argument("--json", action="store_true")

    record_parser = subparsers.add_parser("record")
    record_parser.add_argument("profile", choices=("claude", "codex"))
    record_parser.add_argument("--install-root")

    bump_parser = subparsers.add_parser("bump")
    bump_parser.add_argument("part", choices=("major", "minor", "patch"))

    args = parser.parse_args()
    if args.command == "install-claude":
        target = Path(args.target or os.environ.get("CLAUDE_HOME", Path.home() / ".claude")).expanduser()
        return install_claude(target, args.dry_run)
    if args.command == "status":
        return print_status(args.json, args.profile)
    if args.command == "record":
        receipt = write_receipt(args.profile, args.install_root)
        print(
            f"Recorded {args.profile} {receipt['releaseVersion']} "
            f"({receipt['profileDigest'][:12]})."
        )
        return 0
    if args.command == "bump":
        return bump_version(args.part)
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, json.JSONDecodeError) as error:
        print(f"ai-config error: {error}", file=sys.stderr)
        raise SystemExit(1)
