#!/usr/bin/env python3
"""
cmdref — Command Referencer  v4.0.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Find, build, and copy security commands without leaving the terminal.

  Usage : cmdref <search terms> [flags]
          ref    <search terms> [flags]
  Help  : cmdref -h

Author  : 51LV3RC4T
Repo    : https://github.com/51LV3RC4T/cmdref
License : MIT
"""

# ──────────────────────────────────────────────────────────────────────────────
#  Imports
# ──────────────────────────────────────────────────────────────────────────────
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import curses
except ImportError:  # e.g. Windows CPython without windows-curses
    curses = None  # type: ignore

try:
    from rapidfuzz import fuzz as _rfuzz
    _HAS_FUZZ = True
except ImportError:
    _HAS_FUZZ = False

# ──────────────────────────────────────────────────────────────────────────────
#  Constants
# ──────────────────────────────────────────────────────────────────────────────

VERSION        = "4.0.0"
SYSTEM_DB      = "/etc/cmdref/db"
SYSTEM_WF      = "/etc/cmdref/workflow"
GIT_REPO_URL   = "https://github.com/51LV3RC4T/cmdref"
USER_DIR       = Path.home() / ".cmdref"
CACHE_DIR      = USER_DIR / "cache"
PROFILE_DIR    = USER_DIR / "profiles"
SESSION_FILE   = USER_DIR / "session.json"
CONFIG_FILE    = USER_DIR / "config.json"
MAX_FILE_BYTES   = 5 * 1024 * 1024
MAX_SESSION_BYTES = 1 * 1024 * 1024
MAX_CACHE_ENTRIES = 100_000
MAX_PROFILE_PATHS = 256
MAX_JSON_CONFIG_BYTES = 256_000

_SAFE_URL_RE   = re.compile(r"^https?://[A-Za-z0-9.\-_/]+$")
_VAR_RE        = re.compile(r"\{\{([\w-]+)\}\}")   # {{var-name}} placeholders
_ARG_RE        = re.compile(r"#([\w-]+)")           # #var-name in Argument / Tags

# ──────────────────────────────────────────────────────────────────────────────
#  ANSI colours  (auto-disabled for non-TTY / NO_COLOR)
# ──────────────────────────────────────────────────────────────────────────────

_COLOR = sys.stdout.isatty() and "NO_COLOR" not in os.environ

C_RST = "\033[0m"  if _COLOR else ""
C_BLD = "\033[1m"  if _COLOR else ""
C_DIM = "\033[2m"  if _COLOR else ""
C_CYN = "\033[96m" if _COLOR else ""
C_GRN = "\033[92m" if _COLOR else ""
C_YLW = "\033[93m" if _COLOR else ""
C_RED = "\033[91m" if _COLOR else ""
C_MAG = "\033[95m" if _COLOR else ""


def _c(*args) -> str:
    """_c(C_CYN, C_BLD, "text") → coloured text + reset."""
    *codes, text = args
    return "".join(codes) + str(text) + C_RST


def _strip_ansi(s: str) -> str:
    return re.sub(r"\033\[[0-9;]*m", "", s)


# ──────────────────────────────────────────────────────────────────────────────
#  tun0 detection  — default for attacker-ip
# ──────────────────────────────────────────────────────────────────────────────

def _tun0_ip() -> str:
    """Return the IPv4 address of tun0, falling back to 127.0.0.1."""
    try:
        out = subprocess.run(
            ["ip", "addr", "show", "tun0"],
            capture_output=True, text=True, timeout=2,
        )
        m = re.search(r"inet (\d+\.\d+\.\d+\.\d+)", out.stdout)
        if m:
            return m.group(1)
    except Exception:
        pass
    return "127.0.0.1"


# ──────────────────────────────────────────────────────────────────────────────
#  Variable registry
# ──────────────────────────────────────────────────────────────────────────────

def _parse_variables_markdown(text: str) -> Dict[str, str]:
    """
    Parse | #variable-name | default value | rows from db/Template/variables.md.
    Keys are normalized without the leading '#'.
    """
    out: Dict[str, str] = {}
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        if "---" in s:
            continue
        parts = [c.strip() for c in s.strip("|").split("|")]
        if len(parts) < 2:
            continue
        key_cell, val_cell = parts[0], parts[1]
        if key_cell.lower() in ("variables", "# variables"):
            continue
        m = re.match(r"#?([\w-]+)", key_cell)
        if not m:
            continue
        out[m.group(1)] = val_cell
    return out


def _variables_template_paths() -> Tuple[Path, ...]:
    root = Path(__file__).resolve().parent
    return (
        root / "db" / "Template" / "variables.md",
        root / "db" / "template" / "variables.md",
        root / "db" / "template" / "varaibles.md",
    )


def _default_variables_registry(attacker_ip: str) -> Dict[str, str]:
    """Fallback when no variables.md is found (matches shipped template)."""
    return {
        "target-ip":     "default",
        "attacker-ip":   attacker_ip,
        "target-port":   "default",
        "attacker-port": "default",
        "domain":        "default",
        "url":           "default",
        "protocol":      "default",
        "file":          "default",
        "user-file":     "default",
        "pass-file":     "default",
        "hash":          "default",
        "password":      "Meow!Meow!",
        "directory":     "default",
        "binary":        "default",
        "username":      "51lv3rc4t",
        "executable":    "default",
        "pid":           "default",
        "groupname":     "default",
        "servicename":   "default",
    }


def _load_variables_registry(attacker_ip: str) -> Dict[str, str]:
    """
    Load VARIABLES from the first existing template path, else built-in defaults.
    Placeholder attacker-ip values ([tun0 ip], tun0, etc.) are replaced with
    the detected tun0 address (or 127.0.0.1 fallback).
    """
    loaded: Dict[str, str] = {}
    for path in _variables_template_paths():
        if not path.is_file():
            continue
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError):
            continue
        loaded = _parse_variables_markdown(text)
        if loaded:
            break

    if not loaded:
        return _default_variables_registry(attacker_ip)

    raw = (loaded.get("attacker-ip") or "").strip()
    if not raw:
        loaded["attacker-ip"] = attacker_ip
    elif re.search(r"tun0", raw, re.I) or raw.casefold() == "[tun0 ip]".casefold():
        loaded["attacker-ip"] = attacker_ip
    return loaded


_ATTACKER_IP = _tun0_ip()
VARIABLES: Dict[str, str] = _load_variables_registry(_ATTACKER_IP)

# ──────────────────────────────────────────────────────────────────────────────
#  Session storage  — sticky defaults that persist across invocations
# ──────────────────────────────────────────────────────────────────────────────

_SESSION: Dict[str, str] = {}


def _load_session() -> None:
    global _SESSION
    try:
        if SESSION_FILE.exists():
            if SESSION_FILE.stat().st_size > MAX_SESSION_BYTES:
                return
            data = json.loads(SESSION_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                _SESSION = {str(k): str(v) for k, v in list(data.items())[:10_000]}
    except Exception:
        _SESSION = {}


def _save_session() -> None:
    try:
        USER_DIR.mkdir(parents=True, exist_ok=True)
        SESSION_FILE.write_text(json.dumps(_SESSION, indent=2), encoding="utf-8")
    except Exception:
        pass


def _effective_default(var: str) -> str:
    """Session override > VARIABLES registry > empty string."""
    return _SESSION.get(var, VARIABLES.get(var, ""))


# ──────────────────────────────────────────────────────────────────────────────
#  JSON cache
# ──────────────────────────────────────────────────────────────────────────────

def _cache_key(path: str) -> str:
    return hashlib.sha256(path.encode()).hexdigest()[:16]


def _max_mtime(path: str) -> float:
    p = Path(path)
    if not p.exists():
        return 0.0
    if p.is_file():
        return p.stat().st_mtime
    mtimes = [f.stat().st_mtime for f in p.rglob("*.md") if not f.is_symlink()]
    return max(mtimes, default=0.0)


def _load_cache(path: str) -> Optional[List[dict]]:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cf = CACHE_DIR / f"{_cache_key(path)}.json"
        if not cf.exists():
            return None
        data = json.loads(cf.read_text(encoding="utf-8"))
        # Validate structure before trusting it
        if not isinstance(data, dict) or "entries" not in data:
            return None
        if data.get("mtime", 0) < _max_mtime(path):
            return None   # stale
        ent = data["entries"]
        if not isinstance(ent, list) or len(ent) > MAX_CACHE_ENTRIES:
            return None
        return ent
    except Exception:
        return None


def _save_cache(path: str, entries: List[dict]) -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cf = CACHE_DIR / f"{_cache_key(path)}.json"
        cf.write_text(
            json.dumps({"mtime": _max_mtime(path), "path": path, "entries": entries}, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass


def invalidate_cache(path: str) -> None:
    try:
        cf = CACHE_DIR / f"{_cache_key(path)}.json"
        if cf.exists():
            cf.unlink()
    except Exception:
        pass


# ──────────────────────────────────────────────────────────────────────────────
#  Data model
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class Entry:
    """One parsed command block from a cmdref markdown file."""

    description: str       = ""
    arguments:   List[str] = field(default_factory=list)
    command:     str       = ""
    example:     str       = ""
    tags:        List[str] = field(default_factory=list)
    os_type:     str       = "linux"
    raw:         str       = ""
    source:      str       = ""
    score:       float     = field(default=100.0, compare=False)

    def preview(self) -> str:
        """Command with every {{variable}} substituted by its effective default."""
        out = self.command
        for var in _VAR_RE.findall(self.command):
            out = out.replace(f"{{{{{var}}}}}", _effective_default(var) or f"<{var}>")
        return out

    def to_dict(self) -> dict:
        d = asdict(self)
        d.pop("score", None)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Entry":
        d = dict(d)
        d.pop("score", None)
        known = {k for k in cls.__dataclass_fields__}
        for k in ("arguments", "tags"):
            v = d.get(k)
            if isinstance(v, list):
                d[k] = [str(x) for x in v[:500]]
            else:
                d[k] = []
        for k in ("description", "command", "example", "raw", "source", "os_type"):
            if k in d and not isinstance(d[k], str):
                d[k] = "" if d[k] is None else str(d[k])[:500_000]
        return cls(**{k: v for k, v in d.items() if k in known})


# ──────────────────────────────────────────────────────────────────────────────
#  Parser
# ──────────────────────────────────────────────────────────────────────────────

def _parse_block(block: str, source: str) -> Optional[Entry]:
    """
    Parse a single text block (content between two --- separators).
    Returns None if the block has no ```cmd section.
    Accepts both 'Argument :' and 'Parameters :' for backward compatibility.
    """
    if "```cmd" not in block and "```command" not in block:
        return None

    e = Entry(raw=block.strip(), source=source)

    # Description
    m = re.search(
        r"Description\s*:\s*(.*?)(?=\n\s*(?:Argument|Parameters)\s*:|```|\n\s*Tags\s*:|$)",
        block, re.DOTALL | re.IGNORECASE,
    )
    if m:
        e.description = m.group(1).strip()

    # Arguments / Parameters
    m = re.search(
        r"(?:Argument|Parameters)\s*:\s*(.*?)(?=```|\n\s*Tags\s*:|$)",
        block, re.DOTALL | re.IGNORECASE,
    )
    if m:
        e.arguments = _ARG_RE.findall(m.group(1))

    # Command block
    m = re.search(r"```(?:cmd|command)\s*\n(.*?)```", block, re.DOTALL)
    if not m:
        return None
    e.command = m.group(1).strip()

    # Example block
    m = re.search(r"```(?:exp|example)\s*\n(.*?)```", block, re.DOTALL)
    if m:
        e.example = m.group(1).strip()

    # Tags
    m = re.search(r"Tags\s*:\s*(.*?)$", block, re.MULTILINE | re.IGNORECASE)
    if m:
        e.tags = [t.lower() for t in _ARG_RE.findall(m.group(1))]

    # OS type
    has_linux   = "linux"   in e.tags
    has_windows = "windows" in e.tags
    if has_linux and has_windows:
        e.os_type = "both"
    elif has_windows:
        e.os_type = "windows"
    else:
        e.os_type = "linux"

    return e


def _read_safe(filepath: str) -> Optional[str]:
    """
    Read a file with size guard and encoding fallback.
    Security: caps at MAX_FILE_BYTES to prevent DoS from large/adversarial files.
    """
    p = Path(filepath)
    try:
        if p.stat().st_size > MAX_FILE_BYTES:
            print(_c(C_RED, f"  [!] Skipping {filepath} — exceeds 5 MB."), file=sys.stderr)
            return None
    except OSError:
        return None

    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return p.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
        except OSError as exc:
            print(_c(C_RED, f"  [!] Cannot read {filepath}: {exc}"), file=sys.stderr)
            return None

    print(_c(C_RED, f"  [!] Cannot decode {filepath}."), file=sys.stderr)
    return None


def parse_file(filepath: str) -> List[Entry]:
    text = _read_safe(filepath)
    if text is None:
        return []
    entries = []
    for block in re.split(r"\n---+\n", text):
        e = _parse_block(block, filepath)
        if e:
            entries.append(e)
    return entries


def _collect_md(path: str) -> List[str]:
    """
    Sorted .md file paths under *path*.
    Security: symbolic links are skipped to prevent directory traversal.
    """
    p = Path(path)
    if not p.exists():
        return []
    if p.is_symlink():
        return []
    if p.is_file():
        return [str(p)] if p.suffix == ".md" else []
    return sorted(str(f) for f in p.rglob("*.md") if not f.is_symlink())


def load_entries(paths: List[str], use_cache: bool = True) -> List[Entry]:
    """Load entries from *paths*, using JSON cache when fresh."""
    all_entries: List[Entry] = []
    for path in paths:
        if use_cache:
            cached = _load_cache(path)
            if cached is not None:
                for d in cached:
                    if isinstance(d, dict):
                        try:
                            all_entries.append(Entry.from_dict(d))
                        except Exception:
                            pass
                continue

        # Cache miss — parse live
        entries: List[Entry] = []
        for fp in _collect_md(path):
            entries.extend(parse_file(fp))
        _save_cache(path, [e.to_dict() for e in entries])
        all_entries.extend(entries)

    return all_entries


# ──────────────────────────────────────────────────────────────────────────────
#  Profile management
# ──────────────────────────────────────────────────────────────────────────────

_DEFAULT_PROFILE = "default"
_PROFILE_NAME_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,63}$")


def _is_valid_profile_name(name: str) -> bool:
    """Reject path separators and traversal (profile JSON lives under ~/.cmdref/profiles/)."""
    if not name or name in (".", ".."):
        return False
    return bool(_PROFILE_NAME_RE.match(name))


def _validate_profile_name(name: str) -> None:
    if not _is_valid_profile_name(name):
        _err(
            "Invalid profile name. Use 1–64 characters: start with a letter or digit, "
            "then letters, digits, . _ - only."
        )


def _profiles_dir() -> Path:
    d = PROFILE_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def _profile_path(name: str) -> Path:
    return _profiles_dir() / f"{name}.json"


def _load_config() -> dict:
    try:
        if CONFIG_FILE.exists():
            if CONFIG_FILE.stat().st_size > MAX_JSON_CONFIG_BYTES:
                return {"active_profile": _DEFAULT_PROFILE}
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {"active_profile": _DEFAULT_PROFILE}


def _save_config(cfg: dict) -> None:
    try:
        USER_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    except Exception:
        pass


def _active_profile() -> str:
    name = _load_config().get("active_profile", _DEFAULT_PROFILE)
    if not _is_valid_profile_name(str(name)):
        return _DEFAULT_PROFILE
    return str(name)


def _load_profile(name: str) -> dict:
    if not _is_valid_profile_name(name):
        name = _DEFAULT_PROFILE
    pp = _profile_path(name)
    if pp.exists():
        try:
            if pp.stat().st_size > MAX_JSON_CONFIG_BYTES:
                return {"name": name, "paths": [SYSTEM_DB]}
            data = json.loads(pp.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data = dict(data)
                raw_paths = data.get("paths", [SYSTEM_DB])
                if raw_paths is None:
                    raw_paths = [SYSTEM_DB]
                data["paths"] = _normalize_profile_paths(raw_paths)
                return data
        except Exception:
            pass
    return {"name": name, "paths": [SYSTEM_DB]}


def _save_profile(data: dict) -> None:
    _validate_profile_name(str(data.get("name", "")))
    _profiles_dir()
    _profile_path(data["name"]).write_text(json.dumps(data, indent=2), encoding="utf-8")


def _normalize_profile_paths(raw: object) -> List[str]:
    """
    Coerce profile paths from JSON; cap count; drop malformed entries.
    An explicit empty list (new profile) stays empty; corrupt lists fall back to SYSTEM_DB.
    """
    if not isinstance(raw, list):
        return [SYSTEM_DB]
    if len(raw) == 0:
        return []
    out: List[str] = []
    for p in raw[:MAX_PROFILE_PATHS]:
        if not isinstance(p, str):
            continue
        s = p.strip()
        if not s or "\x00" in s:
            continue
        out.append(os.path.normpath(os.path.expanduser(s)))
    return out if out else [SYSTEM_DB]


def _profile_search_paths(name: str) -> List[str]:
    return _load_profile(name).get("paths", [SYSTEM_DB])


def cmd_profile_create(name: str) -> None:
    _validate_profile_name(name)
    if _profile_path(name).exists():
        print(_c(C_YLW, f"  [!] Profile '{name}' already exists."))
        return
    _save_profile({"name": name, "paths": []})
    print(_c(C_GRN, f"  [✓] Profile '{name}' created.\n"))


def cmd_profile_delete(name: str) -> None:
    _validate_profile_name(name)
    if name == _DEFAULT_PROFILE:
        _err("Cannot delete the default profile.")
    pp = _profile_path(name)
    if not pp.exists():
        _err(f"Profile '{name}' not found.")
    pp.unlink()
    wf_dir = Path(SYSTEM_WF) / name
    if wf_dir.exists():
        shutil.rmtree(wf_dir, ignore_errors=True)
    cfg = _load_config()
    if cfg.get("active_profile") == name:
        cfg["active_profile"] = _DEFAULT_PROFILE
        _save_config(cfg)
    print(_c(C_GRN, f"  [✓] Profile '{name}' deleted.\n"))


def cmd_profile_rename(old: str, new: str) -> None:
    _validate_profile_name(old)
    _validate_profile_name(new)
    pp = _profile_path(old)
    if not pp.exists():
        _err(f"Profile '{old}' not found.")
    data = _load_profile(old)
    data["name"] = new
    _save_profile(data)
    pp.unlink()
    cfg = _load_config()
    if cfg.get("active_profile") == old:
        cfg["active_profile"] = new
        _save_config(cfg)
    print(_c(C_GRN, f"  [✓] Profile renamed: '{old}' → '{new}'.\n"))


def cmd_profile_selected() -> None:
    name    = _active_profile()
    profile = _load_profile(name)
    paths   = profile.get("paths", [SYSTEM_DB])
    print()
    print(_c(C_BLD, C_CYN, f"  Active profile : {name}"))
    print(_c(C_DIM, "  Sources:"))
    for p in paths:
        print(_c(C_DIM, f"    • {p}"))
    print()


def cmd_workflow_source(source: str, profile_name: str) -> None:
    _validate_profile_name(profile_name)
    if "\x00" in source:
        _err("Invalid source path.")
    src = Path(source).resolve()
    if not src.exists():
        _err(f"Source not found: {source}")

    profile = _load_profile(profile_name)
    paths   = profile.setdefault("paths", [])
    str_src = str(src)

    if str_src in paths:
        print(_c(C_YLW, f"  [!] Already in profile '{profile_name}'."))
        return

    dst_dir = Path(SYSTEM_WF) / profile_name
    try:
        dst_dir.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            dst = dst_dir / src.name
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            added = str(dst)
        else:
            shutil.copy2(src, dst_dir / src.name)
            added = str(dst_dir / src.name)
    except PermissionError:
        _err(f"Permission denied writing to {dst_dir}. Try sudo.")
    except OSError as exc:
        _err(f"Copy failed: {exc}")

    paths.append(added)
    _save_profile(profile)
    invalidate_cache(added)
    print(_c(C_GRN, f"  [✓] Workflow added to profile '{profile_name}'.\n"))


def cmd_workflow_delete(profile_name: str, wf_name: Optional[str] = None) -> None:
    _validate_profile_name(profile_name)
    profile = _load_profile(profile_name)
    paths   = profile.get("paths", [])

    if not paths:
        print(_c(C_YLW, f"  No workflows in profile '{profile_name}'."))
        return

    if wf_name is None:
        print()
        print(_c(C_BLD, C_CYN, f"  Workflows in '{profile_name}' :"))
        for i, p in enumerate(paths, 1):
            print(f"  {_c(C_YLW, str(i))}.  {p}")
        print()
        try:
            raw = input(_c(C_CYN, "  Select workflow to delete : ")).strip()
            idx = int(raw) - 1
            if not (0 <= idx < len(paths)):
                raise ValueError
        except (ValueError, EOFError, KeyboardInterrupt):
            print(_c(C_RED, "\n  Cancelled."))
            return
        wf_path = paths.pop(idx)
    else:
        matches = [p for p in paths if wf_name in Path(p).name]
        if not matches:
            _err(f"Workflow '{wf_name}' not found in profile '{profile_name}'.")
        wf_path = matches[0]
        paths.remove(wf_path)

    managed = (Path(SYSTEM_WF) / profile_name).resolve()
    pp = Path(wf_path)
    if pp.exists():
        try:
            resolved = pp.resolve()
            resolved.relative_to(managed)
        except ValueError:
            pass
        else:
            if pp.is_dir():
                shutil.rmtree(pp, ignore_errors=True)
            else:
                pp.unlink(missing_ok=True)

    profile["paths"] = paths
    _save_profile(profile)
    invalidate_cache(wf_path)
    print(_c(C_GRN, f"  [✓] Removed '{wf_path}' from '{profile_name}'.\n"))


# ──────────────────────────────────────────────────────────────────────────────
#  Fuzzy ranking
# ──────────────────────────────────────────────────────────────────────────────

_MIN_SCORE = 45.0


def _score(entry: Entry, query_terms: List[str]) -> float:
    """
    Fuzzy relevance score in [0, 100].
    Uses rapidfuzz.fuzz.token_set_ratio when available for typo-tolerance.
    Falls back to a proportional hit-rate without rapidfuzz.
    Exact substring matches receive a +25 boost to stay at the top.
    """
    if not query_terms:
        return 100.0

    hay = " ".join([entry.command, entry.description] + entry.tags + entry.arguments).lower()
    q   = " ".join(query_terms).lower()

    if _HAS_FUZZ:
        base = float(_rfuzz.token_set_ratio(q, hay))
        if all(t in hay for t in query_terms):
            base = min(100.0, base + 25.0)
        return base

    hits = sum(1 for t in query_terms if t in hay)
    return (hits / len(query_terms)) * 100.0


# ──────────────────────────────────────────────────────────────────────────────
#  Search
# ──────────────────────────────────────────────────────────────────────────────

def search(
    entries:    List[Entry],
    query:      List[str],
    desc_terms: List[str],
    arg_terms:  List[str],
    os_filter:  str,
) -> List[Entry]:
    """
    Filter and rank entries.
    • OS type is a hard filter.
    • desc_terms (-d) are matched against the description field.
    • arg_terms  (-a) are matched against the arguments list.
    • query terms drive the fuzzy score; results below _MIN_SCORE are excluded.
    Returns entries sorted by score descending.
    """
    out: List[Entry] = []

    for e in entries:
        # OS hard filter
        if os_filter == "linux"   and e.os_type == "windows":
            continue
        if os_filter == "windows" and e.os_type == "linux":
            continue

        # Description filter
        if any(t.lower() not in e.description.lower() for t in desc_terms):
            continue

        # Argument filter (-a)
        if arg_terms:
            hay = " ".join(e.arguments).lower()
            if any(t.lower() not in hay for t in arg_terms):
                continue

        # Fuzzy score
        s = _score(e, query)
        if query and s < _MIN_SCORE:
            continue

        e.score = s
        out.append(e)

    out.sort(key=lambda x: x.score, reverse=True)
    return out


# ──────────────────────────────────────────────────────────────────────────────
#  Normal display
# ──────────────────────────────────────────────────────────────────────────────

def _hi(cmd: str) -> str:
    """Colour {{variable}} placeholders yellow."""
    return _VAR_RE.sub(lambda m: _c(C_YLW, f"{{{{{m.group(1)}}}}}"), cmd)


def display_results(results: List[Entry], verbose: bool) -> None:
    print()
    print(_c(C_BLD, C_CYN, "  Possible Commands :"), _c(C_DIM, f"({len(results)} found)"))
    print()

    for i, e in enumerate(results, 1):
        score_tag = _c(C_DIM, f" [{e.score:.0f}%]") if e.score < 99.9 else ""
        print(f"  {_c(C_BLD, C_CYN, str(i) + '.')}  {_c(C_GRN, _hi(e.command))}{score_tag}")

        if verbose:
            if e.description:
                print(f"       {_c(C_DIM, '↳  ' + e.description)}")
        print()


# ──────────────────────────────────────────────────────────────────────────────
#  Preview pane  (-vp)
#  Curses-based split-screen.
#  Left  : scrollable numbered result list (shows preview with defaults)
#  Right : full detail (command, preview, description, arguments, tags)
# ──────────────────────────────────────────────────────────────────────────────

_CP_HDR = 1   # cyan bold  — headers / border titles
_CP_NRM = 2   # default    — body text
_CP_SEL = 3   # black on cyan — selected row
_CP_DIM = 4   # white dim  — secondary text
_CP_GRN = 5   # green      — preview / command output
_CP_YLW = 6   # yellow     — variable names
_CP_MAG = 7   # magenta    — tags

# Env snapshot for -vp (restored after curses.endwin)
_PANE_ENV_SNAPSHOT: List[Tuple[str, Optional[str]]] = []


def _pane_env_set(key: str, value: str) -> None:
    """Remember previous value so we can restore after the pane exits."""
    global _PANE_ENV_SNAPSHOT
    if not any(k == key for k, _ in _PANE_ENV_SNAPSHOT):
        _PANE_ENV_SNAPSHOT.append((key, os.environ.get(key)))
    os.environ[key] = value


def _prepare_pane_terminal_env() -> None:
    """
    Tune TERM / ncurses for tmux, QTerminal, Terminator, and other common setups.

    • tmux: TERM must be tmux* or screen* — xterm* inside tmux breaks ncurses.
    • VTE / xfce QTerminal: NCURSES_NO_UTF8_ACS avoids blank ACS line-drawing.
    • ESCDELAY: helps Esc vs arrow-key disambiguation under tmux.
    """
    global _PANE_ENV_SNAPSHOT
    _PANE_ENV_SNAPSHOT = []

    term = os.environ.get("TERM", "") or ""
    in_tmux = bool(os.environ.get("TMUX"))

    # tmux: never use xterm* / linux / dumb as inner TERM (see tmux wiki FAQ).
    if in_tmux:
        override = os.environ.get("CMDREF_TMUX_TERM", "").strip()
        if override:
            _pane_env_set("TERM", override)
        elif term in ("", "dumb", "unknown") or term.startswith("xterm") or term == "linux":
            chosen = "screen-256color"
            if sys.platform == "linux":
                terminfo_dir = "/usr/share/terminfo"
                for candidate in ("tmux-256color", "tmux", "screen-256color", "screen"):
                    ti = os.path.join(terminfo_dir, candidate[0], candidate)
                    if os.path.isfile(ti):
                        chosen = candidate
                        break
            else:
                chosen = "tmux-256color"
            _pane_env_set("TERM", chosen)

    if sys.platform != "win32":
        # Prefer classic ACS / VT100 drawing — fixes empty borders in several terminals.
        if "NCURSES_NO_UTF8_ACS" not in os.environ:
            _pane_env_set("NCURSES_NO_UTF8_ACS", "1")

    if in_tmux and "ESCDELAY" not in os.environ:
        _pane_env_set("ESCDELAY", os.environ.get("CMDREF_ESC_DELAY", "100"))


def _restore_pane_terminal_env() -> None:
    global _PANE_ENV_SNAPSHOT
    for key, prev in reversed(_PANE_ENV_SNAPSHOT):
        if prev is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = prev
    _PANE_ENV_SNAPSHOT = []


def _init_pairs() -> None:
    if curses is None:
        return
    if not curses.has_colors():
        return
    try:
        curses.start_color()
    except curses.error:
        return
    try:
        curses.use_default_colors()
    except curses.error:
        pass

    def _pair(pid: int, fg: int, bg: int) -> None:
        try:
            curses.init_pair(pid, fg, bg)
        except curses.error:
            try:
                curses.init_pair(pid, curses.COLOR_WHITE, curses.COLOR_BLACK)
            except curses.error:
                pass

    _pair(_CP_HDR, curses.COLOR_CYAN,    -1)
    _pair(_CP_NRM, -1,                   -1)
    _pair(_CP_SEL, curses.COLOR_BLACK,   curses.COLOR_CYAN)
    _pair(_CP_DIM, curses.COLOR_WHITE,   -1)
    _pair(_CP_GRN, curses.COLOR_GREEN,   -1)
    _pair(_CP_YLW, curses.COLOR_YELLOW,  -1)
    _pair(_CP_MAG, curses.COLOR_MAGENTA, -1)


def _draw_box_ascii(win) -> None:
    """+---+ border when win.box() ACS would render as blank (QTerminal / some VTE)."""
    try:
        rows, cols = win.getmaxyx()
        if rows < 2 or cols < 2:
            return
        for x in range(cols):
            win.addch(0, x, ord("-"))
            win.addch(rows - 1, x, ord("-"))
        for y in range(1, rows - 1):
            win.addch(y, 0, ord("|"))
            win.addch(y, cols - 1, ord("|"))
        win.addch(0, 0, ord("+"))
        win.addch(0, cols - 1, ord("+"))
        win.addch(rows - 1, 0, ord("+"))
        win.addch(rows - 1, cols - 1, ord("+"))
    except curses.error:
        pass


def _curses_safe_slice(text: str, max_chars: int) -> str:
    """Truncate for curses.addstr; strip ANSI so width matches visible cells."""
    if max_chars <= 0:
        return ""
    plain = _strip_ansi(text)
    if len(plain) <= max_chars:
        return plain
    return plain[: max_chars - 1] + ">" if max_chars > 1 else plain[:max_chars]


def _wrap(text: str, width: int) -> List[str]:
    lines = []
    for para in (text or "").splitlines():
        if not para.strip():
            lines.append("")
            continue
        words, cur = para.split(), ""
        for w in words:
            if len(cur) + len(w) + (1 if cur else 0) <= width:
                cur = (cur + " " if cur else "") + w
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines or [""]


def _draw_detail(win, entry: Entry) -> None:
    """Render the right-side detail panel (curses color pairs only — no ANSI escapes)."""
    win.erase()
    _draw_box_ascii(win)
    rows, cols = win.getmaxyx()
    inner_w = max(0, cols - 4)
    row = [2]

    def put(text: str, attr: int = 0, cp: int = _CP_NRM) -> None:
        if row[0] >= rows - 2 or inner_w <= 0:
            return
        try:
            win.addstr(row[0], 2, _curses_safe_slice(str(text), inner_w),
                       curses.color_pair(cp) | attr)
        except curses.error:
            pass
        row[0] += 1

    def section(label: str) -> None:
        if row[0] < rows - 2:
            put("")
        put(label, curses.A_BOLD, _CP_HDR)

    # Command (raw with placeholders)
    section("COMMAND")
    for line in _wrap(entry.command, inner_w):
        put(line, 0, _CP_YLW)

    # Preview (substituted defaults)
    section("PREVIEW")
    for line in _wrap(entry.preview(), inner_w):
        put(line, 0, _CP_GRN)

    # Description
    if entry.description:
        section("DESCRIPTION")
        for line in _wrap(entry.description, inner_w):
            put(line, 0, _CP_DIM)

    # Arguments — never mix terminal ANSI with curses
    if entry.arguments:
        section("ARGUMENTS")
        arg_w = max(8, min(18, inner_w // 3))
        for arg in entry.arguments:
            val = _effective_default(arg)
            arg_disp = _curses_safe_slice(str(arg), arg_w).ljust(arg_w)
            if val:
                val_w = max(0, inner_w - 4 - arg_w)
                put(f"  {arg_disp}  {_curses_safe_slice(val, val_w)}", 0, _CP_NRM)
            else:
                put(f"  {arg_disp}  (no default)", 0, _CP_DIM)

    # Tags
    if entry.tags:
        section("TAGS")
        put("  " + "  ".join(f"#{t}" for t in entry.tags), 0, _CP_MAG)

    win.noutrefresh()


def _pane_inner(stdscr, results: List[Entry]) -> Optional[Tuple[Entry, str]]:
    if curses is None:
        return None
    curses.curs_set(0)
    try:
        esc_ms = int(os.environ.get("ESCDELAY", "100"))
    except ValueError:
        esc_ms = 100
    curses.set_escdelay(max(25, min(esc_ms, 1000)))
    stdscr.keypad(True)
    stdscr.nodelay(False)
    _init_pairs()

    sel = 0
    top = 0
    n   = len(results)
    key_resize = getattr(curses, "KEY_RESIZE", None)

    while True:
        try:
            curses.update_lines_cols()
        except curses.error:
            pass
        rows, cols = stdscr.getmaxyx()
        if rows < 12 or cols < 60:
            return None

        left_w  = max(38, min(50, cols // 3))
        right_w = cols - left_w
        if right_w < 14:
            return None

        list_h = rows - 2

        stdscr.erase()

        # ── Header bar ────────────────────────────────────────────────────────
        hdr = f"  cmdref v{VERSION}  —  {n} result{'s' if n != 1 else ''}"
        try:
            stdscr.addstr(0, 0, _curses_safe_slice(hdr.ljust(cols), cols),
                          curses.color_pair(_CP_HDR) | curses.A_BOLD)
        except curses.error:
            pass

        # ── Left pane — result list ───────────────────────────────────────────
        lwin = curses.newwin(rows - 2, left_w, 1, 0)
        lwin.erase()
        _draw_box_ascii(lwin)
        title = " Results "
        try:
            lwin.addstr(0, 2, title, curses.color_pair(_CP_HDR) | curses.A_BOLD)
        except curses.error:
            pass

        visible_n = max(1, list_h - 2)
        visible   = results[top: top + visible_n]

        show_scroll = n > visible_n
        list_cols   = max(1, (left_w - 3) if show_scroll else (left_w - 2))
        for vi, e in enumerate(visible):
            gi    = top + vi
            plain = _strip_ansi(e.preview())
            label = _curses_safe_slice(f" {gi + 1:>2}. {plain}", list_cols)
            try:
                if gi == sel:
                    lwin.addstr(vi + 2, 1, label.ljust(list_cols)[:list_cols],
                                curses.color_pair(_CP_SEL) | curses.A_BOLD)
                else:
                    lwin.addstr(vi + 2, 1, label[:list_cols],
                                curses.color_pair(_CP_GRN))
            except curses.error:
                pass

        # Scroll indicator (ASCII — reliable on all Windows consoles)
        if show_scroll:
            bar_h = max(1, visible_n * visible_n // n)
            bar_y = int(sel / max(1, n - 1) * max(0, visible_n - bar_h)) if n > 1 else 0
            col_sc = left_w - 2
            for rr in range(visible_n):
                ch = "#" if bar_y <= rr < bar_y + bar_h else ":"
                try:
                    lwin.addch(rr + 2, col_sc, ch, curses.color_pair(_CP_DIM))
                except curses.error:
                    pass

        lwin.noutrefresh()

        # ── Right pane — detail ───────────────────────────────────────────────
        rwin = curses.newwin(rows - 2, right_w, 1, left_w)
        _draw_detail(rwin, results[sel])

        # ── Footer bar ────────────────────────────────────────────────────────
        footer = "  [Up/Down j k] Nav  [b/Enter] Build  [c] Copy  [q/Esc] Quit"
        try:
            stdscr.addstr(rows - 1, 0, _curses_safe_slice(footer.ljust(cols), cols),
                          curses.color_pair(_CP_DIM) | curses.A_BOLD)
        except curses.error:
            pass

        stdscr.noutrefresh()
        curses.doupdate()

        # ── Key handling ─────────────────────────────────────────────────────
        key = stdscr.getch()

        if key in (ord("q"), ord("Q"), 27):
            return None
        if key_resize is not None and key == key_resize:
            try:
                curses.update_lines_cols()
            except curses.error:
                pass
            continue
        if key in (curses.KEY_UP, ord("k")):
            sel = max(0, sel - 1)
        elif key in (curses.KEY_DOWN, ord("j")):
            sel = min(n - 1, sel + 1)
        elif key == curses.KEY_PPAGE:
            sel = max(0, sel - visible_n)
        elif key == curses.KEY_NPAGE:
            sel = min(n - 1, sel + visible_n)
        elif key in (ord("b"), ord("B"), ord("\n"), ord("\r"), 10):
            return results[sel], "build"
        elif key in (ord("c"), ord("C")):
            return results[sel], "copy"

        if sel < top:
            top = sel
        elif sel >= top + visible_n:
            top = sel - visible_n + 1


def show_pane(results: List[Entry]) -> Optional[Tuple[Entry, str]]:
    if not results:
        return None
    if curses is None:
        return None
    if not (sys.stdout.isatty() and sys.stdin.isatty()):
        return None

    _prepare_pane_terminal_env()
    stdscr = None
    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        return _pane_inner(stdscr, results)
    except curses.error:
        return None
    finally:
        if stdscr is not None:
            try:
                stdscr.keypad(False)
                curses.echo()
                curses.nocbreak()
                curses.endwin()
            except curses.error:
                pass
        _restore_pane_terminal_env()


# ──────────────────────────────────────────────────────────────────────────────
#  Builder  (-b)
# ──────────────────────────────────────────────────────────────────────────────

def build_command(command: str, example: str) -> Optional[str]:
    """
    Interactively fill in every {{variable}}.
    Session memory: each value entered is persisted and becomes the sticky
    default for that variable in all future prompts.
    Priority: session override > VARIABLES registry > (user must supply).
    """
    vars_needed = list(dict.fromkeys(_VAR_RE.findall(command)))
    if not vars_needed:
        return command

    print()
    print(_c(C_BLD, C_CYN, "  Specify parameter values :"))
    print()

    subs: Dict[str, str] = {}

    for var in vars_needed:
        default = _effective_default(var)

        prompt = f"  {_c(C_YLW, var)}"
        if default:
            prompt += f" {_c(C_DIM, '[' + default + ']')}"
        prompt += " : "

        try:
            value = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return None

        if not value:
            if default:
                value = default
            else:
                _meow(f"No value provided for '{var}' which has no default.")
                if example:
                    print(_c(C_DIM, f"  Example → {example}"))
                print()
                return None

        _SESSION[var] = value   # persist immediately
        subs[var]     = value

    _save_session()

    result = command
    for var, val in subs.items():
        result = result.replace(f"{{{{{var}}}}}", val)
    if len(result) > 2_000_000:
        _meow("Built command exceeds size limit.")
        return None

    return result


# ──────────────────────────────────────────────────────────────────────────────
#  Clipboard
# ──────────────────────────────────────────────────────────────────────────────

def copy_to_clipboard(text: str) -> bool:
    """
    Copy plain text to system clipboard. ANSI codes are stripped first.
    Security: all subprocess calls use list-form args (no shell=True).
    Windows clip.exe expects UTF-16LE; Unix tools use UTF-8.
    """
    clean = _strip_ansi(text)
    attempts: Tuple[Tuple[List[str], str], ...] = (
        (["xclip", "-selection", "clipboard"], "utf-8"),
        (["xsel", "--clipboard", "--input"], "utf-8"),
        (["wl-copy"], "utf-8"),
        (["pbcopy"], "utf-8"),
        (["clip"], "utf-16le" if sys.platform == "win32" else "utf-8"),
    )
    for cmd, enc in attempts:
        if not shutil.which(cmd[0]):
            continue
        try:
            data = clean.encode(enc, errors="replace")
            subprocess.run(
                cmd,
                input=data,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except (subprocess.CalledProcessError, OSError, ValueError):
            continue
    return False


# ──────────────────────────────────────────────────────────────────────────────
#  Outfile  (-O)
# ──────────────────────────────────────────────────────────────────────────────

def write_outfile(results: List[Entry], outfile: str) -> None:
    if "\x00" in outfile or not outfile.strip():
        print(_c(C_RED, "  [!] Invalid outfile path."))
        return
    lines = []
    for i, e in enumerate(results, 1):
        lines += [f"{i}. {e.command}", f"   {e.description}", f"   Preview: {e.preview()}", ""]
    try:
        Path(outfile).write_text("\n".join(lines), encoding="utf-8")
        print(_c(C_GRN, f"  [✓] Results written to {outfile}"))
    except OSError as exc:
        print(_c(C_RED, f"  [!] Could not write {outfile}: {exc}"))


# ──────────────────────────────────────────────────────────────────────────────
#  DB / workflow update
# ──────────────────────────────────────────────────────────────────────────────

def cmd_update_db() -> None:
    """
    Shallow-clone the repo and replace /etc/cmdref/db.
    Security:
      • URL validated with strict allowlist regex.
      • Temp dir created with mkdtemp() — prevents TOCTOU / symlink race.
      • No shell=True in subprocess.
    """
    if not _SAFE_URL_RE.match(GIT_REPO_URL):
        _err(f"GIT_REPO_URL is malformed: {GIT_REPO_URL}")

    print(_c(C_CYN, f"\n  [*] Fetching DB from: {GIT_REPO_URL}"))

    if not shutil.which("git"):
        print(_c(C_RED, "  [!] git not found in PATH.\n"))
        return

    tmp: Optional[str] = None
    try:
        tmp = tempfile.mkdtemp(prefix="cmdref_")
        proc = subprocess.run(
            ["git", "clone", "--depth=1", GIT_REPO_URL, tmp],
            capture_output=True,
        )
        if proc.returncode != 0:
            err = proc.stderr.decode("utf-8", errors="replace").strip()
            print(_c(C_RED, f"  [!] git clone failed: {err}"))
            return

        src = os.path.join(tmp, "db")
        if not os.path.isdir(src):
            print(_c(C_RED, "  [!] Repository has no /db directory."))
            return

        if os.path.exists(SYSTEM_DB):
            shutil.rmtree(SYSTEM_DB)
        shutil.copytree(src, SYSTEM_DB)
        invalidate_cache(SYSTEM_DB)
        print(_c(C_GRN, f"  [✓] DB updated at {SYSTEM_DB}\n"))

    except PermissionError:
        print(_c(C_RED, "  [!] Permission denied — try: sudo cmdref -udb\n"))
    except OSError as exc:
        print(_c(C_RED, f"  [!] Error: {exc}\n"))
    finally:
        if tmp and os.path.exists(tmp):
            shutil.rmtree(tmp, ignore_errors=True)


def cmd_update_workflow(profile_name: str) -> None:
    _validate_profile_name(profile_name)
    paths = _profile_search_paths(profile_name)
    print(_c(C_CYN, f"\n  [*] Rebuilding cache for profile '{profile_name}'..."))
    for path in paths:
        invalidate_cache(path)
        load_entries([path], use_cache=False)
        print(_c(C_GRN, f"  [✓] {path}"))
    print()


# ──────────────────────────────────────────────────────────────────────────────
#  Banner
# ──────────────────────────────────────────────────────────────────────────────

_LOGO = (
    "   ██████╗███╗   ███╗██████╗ ██████╗ ███████╗███████╗\n"
    "  ██╔════╝████╗ ████║██╔══██╗██╔══██╗██╔════╝██╔════╝\n"
    "  ██║     ██╔████╔██║██║  ██║██████╔╝█████╗  █████╗  \n"
    "  ██║     ██║╚██╔╝██║██║  ██║██╔══██╗██╔══╝  ██╔══╝  \n"
    "  ╚██████╗██║ ╚═╝ ██║██████╔╝██║  ██║███████╗██║     \n"
    "   ╚═════╝╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     "
)


def _print_banner() -> None:
    print()
    for line in _LOGO.splitlines():
        print(_c(C_CYN, C_BLD, line))
    bar   = "  " + "─" * 54
    left  = "  Command Referencer"
    right = f"[ 51LV3RC4T ]  v{VERSION}"
    gap   = 54 - len(left) - len(right) + 2
    print(_c(C_DIM, bar))
    print(_c(C_DIM, left) + " " * gap + _c(C_YLW, C_BLD, right))
    print(_c(C_DIM, bar))
    print()


# ──────────────────────────────────────────────────────────────────────────────
#  Help
# ──────────────────────────────────────────────────────────────────────────────

def print_help() -> None:
    _print_banner()

    print(_c(C_BLD, C_CYN, "  Usage:"))
    print("    cmdref <search terms> [flags]")
    print("    ref    <search terms> [flags]\n")

    sections = [
        ("Basic", [
            ("-h",   "--help",            "",                     "Display this help menu"),
            ("-V",   "--version",         "",                     f"Print version  (v{VERSION})"),
            ("-v",   "--verbose",         "",                     "Show description under each result"),
            ("-vp",  "--pane-view",       "",                     "Interactive split-pane view"),
            ("-d",   "--description",     "<words…>",             "Match words in description"),
            ("-a",   "--argument",        "<var-names…>",         "Filter by argument variable name"),
            ("-s",   "--source",          "<file | folder>",      "Search in a specific file or folder"),
            ("-ow",  "--os-windows",      "",                     "Windows commands only  [default: Linux]"),
            ("-O",   "--outfile",         "<filename>",           "Write results to a file"),
            ("-udb", "--update-db",       "",                     "Pull latest /db from GitHub + rebuild cache"),
            ("-uw",  "--update-workflow", "",                     "Rebuild workflow cache for active profile"),
        ]),
        ("Workflow & Profiles", [
            ("-ws",  "--workflow-source",  "<path> -p <profile>", "Add a workflow to a profile"),
            ("-p",   "--profile",          "<name>",              "Use a specific profile for search"),
            ("-pc",  "--profile-create",   "<name>",              "Create a new profile"),
            ("-pd",  "--profile-delete",   "<name>",              "Delete a profile"),
            ("-pr",  "--profile-rename",   "<old> <new>",         "Rename a profile"),
            ("-ps",  "--profile-selected", "",                    "Show currently active profile"),
            ("-wd",  "--workflow-delete",  "[-p <profile>]",      "Remove a workflow from a profile"),
        ]),
        ("Power", [
            ("-b",   "--builder",   "",   "Interactively fill in {{variables}} then run"),
            ("-c",   "--copy",      "",   "Copy selected command to clipboard"),
            ("-e",   "--exec",      "",   "Open the interactive cmdref shell  (REPL)"),
        ]),
    ]

    for sec, flags in sections:
        print(_c(C_BLD, C_CYN, f"  {sec}:"))
        for short, long_, arg, desc in flags:
            print(
                f"    {_c(C_YLW, C_BLD, f'{short:<6}')}"
                f" {_c(C_DIM, f'{long_:<22}')}"
                f" {_c(C_DIM, f'{arg:<24}')}"
                f" {desc}"
            )
        print()

    print(_c(C_BLD, C_CYN, "  Examples:"))
    examples = [
        ("cmdref nmap",                        "list all nmap entries"),
        ("cmdref namp",                        "typo-tolerant fuzzy search"),
        ("cmdref nmap -d aggressive -v",        "description filter, verbose"),
        ("cmdref -a target-ip pass-file",       "filter by argument variables"),
        ("cmdref nmap -b -c",                   "build a command and copy it"),
        ("cmdref nmap -vp",                     "open interactive pane view"),
        ("cmdref -ow mimikatz",                 "Windows-only results"),
        ("cmdref nmap -s ~/notes/nmap.md",      "search a custom file"),
        ("cmdref -ws ~/pentest.md -p web",      "add workflow to the 'web' profile"),
        ("cmdref -p web nmap",                  "search the 'web' profile"),
        ("cmdref -e",                           "open the interactive shell"),
        ("cmdref -udb",                         "pull latest DB from GitHub"),
    ]
    for cmd, note in examples:
        print(f"    {_c(C_GRN, cmd)}  {_c(C_DIM, '# ' + note)}")
    print()


# ──────────────────────────────────────────────────────────────────────────────
#  Error helpers
# ──────────────────────────────────────────────────────────────────────────────

def _meow(msg: str) -> None:
    """Non-fatal Silver Kitty error."""
    print(_c(C_RED, C_BLD, f"  MEOW MEOW ! Silver Kitty is confused :/ ! -> {msg}"))


def _err(msg: str) -> None:
    """Fatal error — print and exit."""
    _meow(msg)
    sys.exit(1)


# ──────────────────────────────────────────────────────────────────────────────
#  Integrated shell  (-e / --exec)
# ──────────────────────────────────────────────────────────────────────────────

def run_exec_shell() -> None:
    try:
        import readline   # noqa — enables line editing and history
    except ImportError:
        pass

    _print_banner()
    print(_c(C_DIM, "  Interactive Shell  ─  type 'exit' or Ctrl-C to quit"))
    print(_c(C_DIM, "  " + "─" * 54))
    print()

    while True:
        try:
            raw = input(_c(C_CYN, C_BLD, "  ref> ")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not raw:
            continue
        if raw.lower() in ("exit", "quit", "q", ":q"):
            break

        try:
            _run(raw.split())
        except SystemExit:
            pass    # search may sys.exit(1) on no results — absorb it

        print()


# ──────────────────────────────────────────────────────────────────────────────
#  Argument parser
# ──────────────────────────────────────────────────────────────────────────────

class Args:
    __slots__ = (
        "query", "help", "version",
        "verbose", "pane",
        "d", "a", "s",
        "ow", "outfile",
        "udb", "uw",
        "ws", "p", "pc", "pd", "pr", "ps", "wd",
        "b", "c", "exec_shell",
    )

    def __init__(self) -> None:
        self.query:      List[str]     = []
        self.help:       bool          = False
        self.version:    bool          = False
        self.verbose:    bool          = False
        self.pane:       bool          = False
        self.d:          List[str]     = []
        self.a:          List[str]     = []
        self.s:          Optional[str] = None
        self.ow:         bool          = False
        self.outfile:    Optional[str] = None
        self.udb:        bool          = False
        self.uw:         bool          = False
        self.ws:         Optional[str] = None
        self.p:          Optional[str] = None
        self.pc:         Optional[str] = None
        self.pd:         Optional[str] = None
        self.pr:         List[str]     = []
        self.ps:         bool          = False
        self.wd:         bool          = False
        self.b:          bool          = False
        self.c:          bool          = False
        self.exec_shell: bool          = False


_BOOLS: Dict[str, str] = {
    "-h":   "help",       "--help":             "help",
    "-V":   "version",    "--version":          "version",
    "-v":   "verbose",    "--verbose":          "verbose",
    "-vp":  "pane",       "--pane-view":        "pane",
    "-ow":  "ow",         "--os-windows":       "ow",
    "-udb": "udb",        "--update-db":        "udb",
    "-uw":  "uw",         "--update-workflow":  "uw",
    "-ps":  "ps",         "--profile-selected": "ps",
    "-wd":  "wd",         "--workflow-delete":  "wd",
    "-b":   "b",          "--builder":          "b",
    "-c":   "c",          "--copy":             "c",
    "-e":   "exec_shell", "--exec":             "exec_shell",
}

_VALS: Dict[str, str] = {
    "-s":  "s",       "--source":           "s",
    "-O":  "outfile", "--outfile":          "outfile",
    "-ws": "ws",      "--workflow-source":  "ws",
    "-p":  "p",       "--profile":          "p",
    "-pc": "pc",      "--profile-create":   "pc",
    "-pd": "pd",      "--profile-delete":   "pd",
}

_LISTS: Dict[str, str] = {
    "-d": "d", "--description": "d",
    "-a": "a", "--argument":    "a",
}


def parse_args(argv: List[str]) -> Args:
    args = Args()
    i    = 0
    while i < len(argv):
        tok = argv[i]

        if tok in _BOOLS:
            setattr(args, _BOOLS[tok], True)

        elif tok in ("-pr", "--profile-rename"):
            i += 1
            if i + 1 >= len(argv):
                _err(f"{tok} requires two arguments: <old-name> <new-name>")
            args.pr = [argv[i], argv[i + 1]]
            i += 1

        elif tok in _VALS:
            i += 1
            if i >= len(argv):
                _err(f"{tok} requires an argument.")
            setattr(args, _VALS[tok], argv[i])

        elif tok in _LISTS:
            attr = _LISTS[tok]
            collected: List[str] = []
            i += 1
            while i < len(argv) and not argv[i].startswith("-"):
                collected.append(argv[i])
                i += 1
            setattr(args, attr, collected)
            continue

        elif tok.startswith("-"):
            _err(f"Unknown flag '{tok}'.  Run  cmdref -h  for help.")

        else:
            args.query.append(tok)

        i += 1

    return args


# ──────────────────────────────────────────────────────────────────────────────
#  Core run  (shared by main() and the exec shell)
# ──────────────────────────────────────────────────────────────────────────────

def _run(argv: List[str]) -> None:
    args = parse_args(argv)

    # Informational
    if args.help:
        print_help()
        return
    if args.version:
        print(f"cmdref v{VERSION}")
        return
    if args.exec_shell:
        run_exec_shell()
        return

    # DB update
    if args.udb:
        cmd_update_db()
        return

    # Profile operations
    if args.pc:
        cmd_profile_create(args.pc)
        return
    if args.pd:
        cmd_profile_delete(args.pd)
        return
    if args.pr:
        cmd_profile_rename(args.pr[0], args.pr[1])
        return
    if args.ps:
        cmd_profile_selected()
        return
    if args.ws:
        profile = args.p or _active_profile()
        cmd_workflow_source(args.ws, profile)
        return
    if args.wd:
        profile = args.p or _active_profile()
        cmd_workflow_delete(profile)
        return
    if args.uw:
        profile = args.p or _active_profile()
        cmd_update_workflow(profile)
        return

    # Set active profile from -p if given without a sub-command
    if args.p:
        _validate_profile_name(args.p)
        cfg = _load_config()
        cfg["active_profile"] = args.p
        _save_config(cfg)

    profile_name = args.p or _active_profile()
    if args.s:
        if "\x00" in args.s:
            _err("Invalid source path.")
        search_paths = [args.s]
    else:
        search_paths = _profile_search_paths(profile_name)

    # Load
    entries = load_entries(search_paths)
    if not entries:
        _meow(f"No entries found in: {', '.join(search_paths)}")
        print(_c(C_DIM, "  • Run  cmdref -udb  to fetch the database."))
        print(_c(C_DIM, "  • Use  -s <path>  to search a custom file."))
        sys.exit(1)

    os_filter = "windows" if args.ow else "linux"
    results   = search(entries, args.query, args.d, args.a, os_filter)

    if not results:
        _meow("No commands matched your search.")
        sys.exit(1)

    if args.outfile and "\x00" in args.outfile:
        _err("Invalid outfile path.")

    # Pane view
    if args.pane:
        outcome = show_pane(results)
        if outcome is None:
            print(_c(C_YLW, "\n  [!] Pane unavailable — falling back to verbose display."))
            display_results(results, verbose=True)
        else:
            selected, action = outcome
            args.b = (action == "build")
            args.c = True
            final_cmd = selected.command
            if args.b:
                built = build_command(final_cmd, selected.example)
                if built is None:
                    return
                final_cmd = built
            print()
            print(_c(C_GRN, C_BLD, f"  → {final_cmd}"))
            if copy_to_clipboard(final_cmd):
                print(_c(C_CYN, "  Command copied to clipboard ! :)"))
            else:
                _meow("Clipboard unavailable — install xclip, xsel, or wl-copy.")
            print()
        return

    display_results(results, verbose=args.verbose)

    if args.outfile:
        write_outfile(results, args.outfile)

    if not (args.b or args.c):
        return

    # Selection
    if len(results) == 1:
        selected = results[0]
    else:
        prompt = _c(C_CYN, C_BLD, f"  Select command [1-{len(results)}] : ")
        try:
            raw = input(prompt).strip()
            idx = int(raw) - 1
            if not (0 <= idx < len(results)):
                raise ValueError
            selected = results[idx]
        except (ValueError, TypeError):
            _meow("Invalid selection.")
            return
        except (EOFError, KeyboardInterrupt):
            print()
            return

    final_cmd = selected.command

    if args.b:
        built = build_command(final_cmd, selected.example)
        if built is None:
            return
        final_cmd = built

    print()
    print(_c(C_GRN, C_BLD, f"  → {final_cmd}"))

    if args.c:
        if copy_to_clipboard(final_cmd):
            print(_c(C_CYN, "  Command copied to clipboard ! :)"))
        else:
            _meow("Clipboard unavailable — install xclip, xsel, or wl-copy.")

    print()


# ──────────────────────────────────────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    _load_session()
    argv = sys.argv[1:]
    if not argv:
        print_help()
        return
    _run(argv)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(0)
