#!/usr/bin/env python3
"""
cmdref — Command Referencer
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Automate variable switching in your workflows and find the right
command in seconds.

  Usage:  cmdref <search terms> [options]
  Help:   cmdref -h

Author  : 51LV3RC4T
Repo    : https://github.com/51LV3RC4T/cmdref
License : MIT
"""

# ──────────────────────────────────────────────────────────────────────────────
#  Standard-library only — zero external dependencies.
# ──────────────────────────────────────────────────────────────────────────────
import os
import re
import sys
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

# ──────────────────────────────────────────────────────────────────────────────
#  Version & paths
# ──────────────────────────────────────────────────────────────────────────────

VERSION         = "1.0.0"
DEFAULT_DB_PATH = "/etc/cmdref/db"
WORKFLOW_PATH   = "/etc/cmdref/workflow"
GIT_REPO_URL    = "https://github.com/51LV3RC4T/cmdref"

# Guard: skip files larger than this to prevent accidental DoS.
MAX_FILE_BYTES = 5 * 1024 * 1024   # 5 MB

# Allowlist for git URLs passed to subprocess.
_SAFE_URL_RE = re.compile(r"^https?://[A-Za-z0-9.\-_/]+$")

# ──────────────────────────────────────────────────────────────────────────────
#  ANSI colour layer
#
#  Colours are disabled automatically when:
#    • stdout is not a TTY  (e.g. piped to grep / a file)
#    • the environment variable NO_COLOR is set  (https://no-color.org)
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


def _c(text: str, *codes: str) -> str:
    """Wrap *text* in one or more ANSI codes and append a reset."""
    return "".join(codes) + str(text) + C_RST


def _strip_ansi(text: str) -> str:
    """Remove every ANSI escape sequence from *text*."""
    return re.sub(r"\033\[[0-9;]*m", "", text)


# ──────────────────────────────────────────────────────────────────────────────
#  Variable registry   (mirrors variable_defined.md)
# ──────────────────────────────────────────────────────────────────────────────

VARIABLES: dict = {
    "cmd_ref_target":           {"display": "Target's IP",           "default": "10.10.10.10"},
    "cmd_ref_attacker":         {"display": "Attacker's IP",         "default": "127.0.0.1"},
    "cmd_ref_target_port":      {"display": "Target PORT",           "default": "51"},
    "cmd_ref_attacker_port":    {"display": "Attacker PORT",         "default": "9999"},
    "cmd_ref_domain":           {"display": "Domain",                "default": "silver.cat"},
    "cmd_ref_url":              {"display": "URL",                   "default": "http://silver.cat"},
    "cmd_ref_protocol":         {"display": "Protocol",              "default": ""},
    "cmd_ref_param_file":       {"display": "Input file",            "default": ""},
    "cmd_ref_param_file_users": {"display": "Input users file",      "default": ""},
    "cmd_ref_param_file_pass":  {"display": "Input Passwords file",  "default": ""},
    "cmd_Ref_target_hash":      {"display": "NTLM Hash",             "default": ""},
}

# ──────────────────────────────────────────────────────────────────────────────
#  Banner
# ──────────────────────────────────────────────────────────────────────────────

# Silver-cat art — the mascot of the tool.  
_CAT = r"""
         /\_/\
        ( -.- )
         > ^ <
"""

# "cmdref" in Unicode block-drawing font.
_LOGO = (
    "   ██████╗███╗   ███╗██████╗ ██████╗ ███████╗███████╗\n"
    "  ██╔════╝████╗ ████║██╔══██╗██╔══██╗██╔════╝██╔════╝\n"
    "  ██║     ██╔████╔██║██║  ██║██████╔╝█████╗  █████╗  \n"
    "  ██║     ██║╚██╔╝██║██║  ██║██╔══██╗██╔══╝  ██╔══╝  \n"
    "  ╚██████╗██║ ╚═╝ ██║██████╔╝██║  ██║███████╗██║     \n"
    "   ╚═════╝╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     "
)


def _print_banner() -> None:
    """Render the full splash: silver-cat art → logo → attribution line."""
    # Cat art in dim cyan — visible but not overpowering
    for line in _CAT.splitlines():
        print(_c(line, C_CYN + C_DIM))

    print()

    # "cmdref" block logo in bright cyan
    for line in _LOGO.splitlines():
        print(_c(line, C_CYN + C_BLD))

    # Attribution bar — separator, tag-line, handle
    bar   = "  " + "─" * 54
    left  = "  Command Referencer"
    right = f"[ 51LV3RC4T ]  v{VERSION}"
    gap   = 54 - len(left) - len(right) + 2

    print(_c(bar, C_DIM))
    print(_c(left, C_DIM) + " " * gap + _c(right, C_YLW + C_BLD))
    print(_c(bar, C_DIM))
    print()


# ──────────────────────────────────────────────────────────────────────────────
#  Data model
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class CommandEntry:
    """One command block parsed from a cmdref markdown DB file."""

    description: str       = ""
    parameters:  List[str] = field(default_factory=list)
    command:     str       = ""
    example:     str       = ""
    tags:        List[str] = field(default_factory=list)
    os_type:     str       = "linux"   # "linux" | "windows" | "both"
    raw_block:   str       = ""
    source_file: str       = ""


# ──────────────────────────────────────────────────────────────────────────────
#  Parser
# ──────────────────────────────────────────────────────────────────────────────

def _parse_block(block: str, source: str) -> Optional[CommandEntry]:
    """
    Turn one text block (content between two --- lines) into a CommandEntry.

    A block is considered valid only when it contains a ```cmd section.
    Comment blocks, headings, and template blocks are silently ignored.
    """
    if "```cmd" not in block and "```command" not in block:
        return None

    entry = CommandEntry(raw_block=block.strip(), source_file=source)

    # Description ──────────────────────────────────────────────────────────────
    m = re.search(
        r"Description\s*:\s*(.*?)(?=\n\s*Parameters\s*:|```|\n\s*Tags\s*:|$)",
        block, re.DOTALL | re.IGNORECASE,
    )
    if m:
        entry.description = m.group(1).strip()

    # Parameters ───────────────────────────────────────────────────────────────
    m = re.search(
        r"Parameters\s*:\s*(.*?)(?=```|\n\s*Tags\s*:|$)",
        block, re.DOTALL | re.IGNORECASE,
    )
    if m:
        entry.parameters = re.findall(r"#(\w+)", m.group(1))

    # Command block  ```cmd … ``` ──────────────────────────────────────────────
    m = re.search(r"```(?:cmd|command)\s*\n(.*?)```", block, re.DOTALL)
    if not m:
        return None
    entry.command = m.group(1).strip()

    # Example block  ```example … ``` ─────────────────────────────────────────
    m = re.search(r"```(?:exp|example)\s*\n(.*?)```", block, re.DOTALL)
    if m:
        entry.example = m.group(1).strip()

    # Tags ─────────────────────────────────────────────────────────────────────
    m = re.search(r"Tags\s*:\s*(.*?)$", block, re.MULTILINE | re.IGNORECASE)
    if m:
        entry.tags = [t.lower() for t in re.findall(r"#(\w+)", m.group(1))]

    # OS type  (linux / windows / both) ───────────────────────────────────────
    has_linux   = "linux"   in entry.tags
    has_windows = "windows" in entry.tags
    if has_linux and has_windows:
        entry.os_type = "both"
    elif has_windows:
        entry.os_type = "windows"
    else:
        entry.os_type = "linux"

    return entry


def _read_file(filepath: str) -> Optional[str]:
    """
    Read a file safely with:
      • A hard size cap  (MAX_FILE_BYTES) to prevent DoS.
      • Multi-encoding fallback: UTF-8 → UTF-8-BOM → Latin-1.

    Returns the file content as a string, or None on any failure.
    """
    p = Path(filepath)

    try:
        size = p.stat().st_size
    except OSError:
        return None

    if size > MAX_FILE_BYTES:
        print(
            _c(f"  [!] Skipping {filepath} — exceeds {MAX_FILE_BYTES // 1_048_576} MB limit.",
               C_RED),
            file=sys.stderr,
        )
        return None

    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return p.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
        except OSError as exc:
            print(_c(f"  [!] Cannot read {filepath}: {exc}", C_RED), file=sys.stderr)
            return None

    print(_c(f"  [!] Cannot decode {filepath} — skipping.", C_RED), file=sys.stderr)
    return None


def parse_file(filepath: str) -> List[CommandEntry]:
    """Parse one markdown DB file and return all valid CommandEntry objects."""
    text = _read_file(filepath)
    if text is None:
        return []

    entries: List[CommandEntry] = []
    for block in re.split(r"\n---+\n", text):
        entry = _parse_block(block, filepath)
        if entry:
            entries.append(entry)
    return entries


def collect_md_files(path: str) -> List[str]:
    """
    Return a sorted list of .md files reachable from *path*.

    Symbolic links are intentionally skipped to prevent traversal
    outside of the expected DB / workflow directories.
    """
    p = Path(path)
    if not p.exists():
        return []

    if p.is_symlink():
        print(_c(f"  [!] Skipping symlink: {path}", C_DIM), file=sys.stderr)
        return []

    if p.is_file():
        return [str(p)] if p.suffix == ".md" else []

    result: List[str] = []
    for f in sorted(p.rglob("*.md")):
        if f.is_symlink():
            continue
        result.append(str(f))
    return result


def load_entries(paths: List[str]) -> List[CommandEntry]:
    """Load and parse every markdown DB file reachable from *paths*."""
    entries: List[CommandEntry] = []
    for path in paths:
        for fp in collect_md_files(path):
            entries.extend(parse_file(fp))
    return entries


# ──────────────────────────────────────────────────────────────────────────────
#  Search / filter
# ──────────────────────────────────────────────────────────────────────────────

def _matches(
    entry:       CommandEntry,
    query_terms: List[str],
    desc_terms:  List[str],
    param_terms: List[str],
    os_filter:   str,
) -> bool:
    """
    Return True when *entry* satisfies every active filter.

    Filters are ANDed:  all must pass for the entry to be included.

    os_filter   — "linux" | "windows"
    query_terms — matched against command text + description + tags
    desc_terms  — matched only against the description field   (-d)
    param_terms — matched only against parameter names          (-p)
    """
    # OS filter ────────────────────────────────────────────────────────────────
    if os_filter == "linux"   and entry.os_type == "windows":
        return False
    if os_filter == "windows" and entry.os_type == "linux":
        return False

    # General terms ────────────────────────────────────────────────────────────
    hay = " ".join([entry.command, entry.description] + entry.tags).lower()
    if any(t.lower() not in hay for t in query_terms):
        return False

    # Description terms  (-d) ──────────────────────────────────────────────────
    if any(t.lower() not in entry.description.lower() for t in desc_terms):
        return False

    # Parameter terms  (-p) ────────────────────────────────────────────────────
    param_hay = " ".join(entry.parameters).lower()
    if any(t.lower() not in param_hay for t in param_terms):
        return False

    return True


# ──────────────────────────────────────────────────────────────────────────────
#  Display
# ──────────────────────────────────────────────────────────────────────────────

_VAR_RE = re.compile(r"(\{\{[\w]+\}\})")


def _highlight(command: str) -> str:
    """Colour {{variable}} placeholders yellow inside a command string."""
    return _VAR_RE.sub(lambda m: _c(m.group(1), C_YLW), command)


def display_results(
    results:       List[CommandEntry],
    verbose:       bool,
    super_verbose: bool,
) -> None:
    print()
    print(
        _c("  Possible Commands :", C_BLD + C_CYN),
        _c(f"({len(results)} found)", C_DIM),
    )
    print()

    for i, entry in enumerate(results):
        print(f"  {_c(str(i) + '.', C_BLD + C_CYN)}  {_c(_highlight(entry.command), C_GRN)}")

        if verbose or super_verbose:
            if entry.description:
                print(f"       {_c('↳  ' + entry.description, C_DIM)}")

        if super_verbose:
            print()
            print(_c("     ┌─── Full Entry " + "─" * 38, C_MAG + C_DIM))
            for line in entry.raw_block.splitlines():
                print(_c("     │ ", C_MAG + C_DIM) + line)
            print(_c("     └" + "─" * 53, C_MAG + C_DIM))

        print()


# ──────────────────────────────────────────────────────────────────────────────
#  Builder  (-b)
# ──────────────────────────────────────────────────────────────────────────────

def _placeholders(command: str) -> List[str]:
    """Return unique, in-order list of variable names from {{…}} tokens."""
    seen: set  = set()
    out:  list = []
    for var in _VAR_RE.findall(command):
        name = var[2:-2]   # strip {{ }}
        if name not in seen:
            seen.add(name)
            out.append(name)
    return out


def build_command(command: str, example: str) -> Optional[str]:
    """
    Interactively substitute every {{variable}} in *command*.

    For each placeholder:
      • The user sees the human-readable display name and the default value.
      • Pressing Enter with no input accepts the default.
      • If a variable has no default the user MUST supply a value;
        leaving it blank triggers the "Silver kitty is confused" message.

    Returns the substituted command string, or None if the user aborts.
    """
    vars_needed = _placeholders(command)
    if not vars_needed:
        return command

    print()
    print(_c("  Specify parameter values :", C_BLD + C_CYN))
    print()

    subs: dict = {}

    for var in vars_needed:
        info    = VARIABLES.get(var, {})
        name    = info.get("display", var.replace("_", " ").title())
        default = str(info.get("default", ""))

        prompt = f"  {_c(name, C_YLW)}"
        if default:
            prompt += f" {_c('[' + default + ']', C_DIM)}"
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
                print()
                print(_c("  MEOW MEOW ! Silver kitty is confused !", C_RED + C_BLD))
                if example:
                    print(_c(f"  Example → {example}", C_DIM))
                print()
                return None

        subs[var] = value

    result = command
    for var, val in subs.items():
        result = result.replace(f"{{{{{var}}}}}", val)

    return result


# ──────────────────────────────────────────────────────────────────────────────
#  Clipboard  (-c)
# ──────────────────────────────────────────────────────────────────────────────

def copy_to_clipboard(text: str) -> bool:
    """
    Copy *text* to the system clipboard.

    ANSI escape codes are stripped before copying so the clipboard
    never contains raw terminal control sequences.

    Backends tried in order (first available wins):
        Linux X11   → xclip
        Linux X11   → xsel
        Linux Wayland → wl-copy
        macOS       → pbcopy
        WSL/Windows → clip
    """
    clean = _strip_ansi(text)
    for cmd in (
        ["xclip", "-selection", "clipboard"],
        ["xsel",  "--clipboard", "--input"],
        ["wl-copy"],
        ["pbcopy"],
        ["clip"],
    ):
        if shutil.which(cmd[0]):
            try:
                subprocess.run(
                    cmd,
                    input=clean.encode("utf-8"),
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return True
            except subprocess.CalledProcessError:
                continue
    return False


# ──────────────────────────────────────────────────────────────────────────────
#  DB update  (-udb)
# ──────────────────────────────────────────────────────────────────────────────

def update_db() -> None:
    """
    Shallow-clone the configured git repository and replace the local
    /etc/cmdref/db directory with the /db folder from the repo.

    Security notes:
      • The URL is validated against a strict allowlist regex before being
        handed to subprocess — guards against argument-injection.
      • tempfile.mkdtemp() creates an unpredictable temp directory, closing
        the TOCTOU / symlink-race window that a fixed /tmp path would expose.
      • The temp directory is always removed in the finally block.
    """
    if not _SAFE_URL_RE.match(GIT_REPO_URL):
        _die(f"GIT_REPO_URL appears malformed: {GIT_REPO_URL}")

    print(_c(f"\n  [*] Fetching DB from: {GIT_REPO_URL}", C_CYN))

    if not shutil.which("git"):
        print(_c("  [!] git is not installed or not in PATH.\n", C_RED))
        return

    tmp: Optional[str] = None
    try:
        tmp = tempfile.mkdtemp(prefix="cmdref_db_")

        proc = subprocess.run(
            ["git", "clone", "--depth=1", GIT_REPO_URL, tmp],
            capture_output=True,
        )
        if proc.returncode != 0:
            print(_c(f"  [!] git clone failed:\n      {proc.stderr.decode().strip()}", C_RED))
            return

        db_src = os.path.join(tmp, "db")
        if not os.path.isdir(db_src):
            print(_c("  [!] The repository has no /db directory.", C_RED))
            return

        if os.path.exists(DEFAULT_DB_PATH):
            shutil.rmtree(DEFAULT_DB_PATH)

        shutil.copytree(db_src, DEFAULT_DB_PATH)
        print(_c("  [✓] DB updated successfully!\n", C_GRN))

    except PermissionError:
        print(_c(f"  [!] Permission denied — try:  sudo cmdref -udb\n", C_RED))
    except OSError as exc:
        print(_c(f"  [!] Filesystem error: {exc}\n", C_RED))
    finally:
        if tmp and os.path.exists(tmp):
            shutil.rmtree(tmp, ignore_errors=True)


# ──────────────────────────────────────────────────────────────────────────────
#  Workflow sourcing  (-s / -sf)
# ──────────────────────────────────────────────────────────────────────────────

def source_workflow(source: str, folder: bool = False) -> None:
    """
    Copy a workflow file (or folder) into /etc/cmdref/workflow.

    If the destination already exists the user is asked to confirm
    before any data is overwritten.
    """
    src = Path(source).resolve()

    if not src.exists():
        print(_c(f"  [!] Source not found: {source}", C_RED))
        return

    try:
        os.makedirs(WORKFLOW_PATH, exist_ok=True)
    except PermissionError:
        print(_c(f"  [!] Permission denied creating {WORKFLOW_PATH} — try sudo.", C_RED))
        return

    dst = Path(WORKFLOW_PATH) / src.name

    if dst.exists():
        try:
            ans = input(_c(f"  [?] {dst} already exists — overwrite? [y/N] : ", C_YLW)).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if ans.lower() != "y":
            print(_c("  [-] Skipped.\n", C_DIM))
            return

    try:
        if folder:
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        print(_c(f"  [✓] Copied to {dst}\n", C_GRN))
    except PermissionError:
        print(_c(f"  [!] Permission denied — try sudo.", C_RED))
    except OSError as exc:
        print(_c(f"  [!] Copy failed: {exc}", C_RED))


# ──────────────────────────────────────────────────────────────────────────────
#  Help text
# ──────────────────────────────────────────────────────────────────────────────

def print_help() -> None:
    _print_banner()

    print(_c("  Usage:", C_BLD + C_CYN))
    print("    cmdref <search terms> [options]\n")

    flags = [
        ("-h",    "",           "Help — display this menu"),
        ("-V",    "",           f"Version — print version and exit  (v{VERSION})"),
        ("-s",    "<file>",     "Source a workflow file  →  copies it to /etc/cmdref/workflow"),
        ("-sf",   "<folder>",   "Source a workflow folder  →  copies it to /etc/cmdref/workflow"),
        ("-f",    "<path>",     "Search only in the specified file or folder"),
        ("-w",    "",           "Search inside /etc/cmdref/workflow"),
        ("-ol",   "",           "Linux commands only  [default unless -ow is set]"),
        ("-ow",   "",           "Windows commands only"),
        ("-d",    "<terms…>",   "Match terms inside the Description field"),
        ("-p",    "<terms…>",   "Match terms inside the Parameters field"),
        ("-v",    "",           "Verbose — show description under each result"),
        ("-vv",   "",           "Super-verbose — show the full raw command block"),
        ("-c",    "",           "Copy the selected command to clipboard"),
        ("-b",    "",           "Builder — interactively replace {{variables}} with real values"),
        ("-udb",  "",           "Update DB — pull the latest /db from the git repo"),
    ]

    print(_c("  Flags:", C_BLD + C_CYN))
    for flag, arg, desc in flags:
        print(f"    {_c(f'{flag:<7}', C_YLW + C_BLD)}{_c(f'{arg:<12}', C_DIM)}  {desc}")

    print()
    print(_c("  Examples:", C_BLD + C_CYN))
    examples = [
        ("cmdref nmap",                             "list every nmap entry"),
        ("cmdref nmap -d aggressive -v",            "search description, show verbose"),
        ("cmdref hydra -p cmd_ref_param_file_pass", "filter by parameter name"),
        ("cmdref nmap -c -b",                       "build a command and copy it"),
        ("cmdref -ow",                              "show Windows-only commands"),
        ("cmdref smb -f ~/my_notes/smb.md",         "search a custom file"),
        ("cmdref -s ~/my_workflow.md",              "add a workflow file"),
        ("cmdref -udb",                             "pull latest DB from GitHub"),
    ]
    for cmd, note in examples:
        print(f"    {_c(cmd, C_GRN)}  {_c('# ' + note, C_DIM)}")
    print()


# ──────────────────────────────────────────────────────────────────────────────
#  Argument parser
#
#  Written by hand instead of using argparse because:
#    1.  argparse treats -vv as -v with value "v".
#    2.  -udb cannot coexist cleanly with short-form flags in argparse.
#    3.  We want free-form positional search terms mixed with flags.
# ──────────────────────────────────────────────────────────────────────────────

class Args:
    """Typed namespace populated by parse_args()."""

    __slots__ = (
        "query", "help", "version",
        "s", "sf", "f",
        "w", "ol", "ow",
        "d", "p",
        "v", "vv",
        "c", "b", "udb",
    )

    def __init__(self) -> None:
        self.query:   List[str]     = []
        self.help:    bool          = False
        self.version: bool          = False
        self.s:       Optional[str] = None
        self.sf:      Optional[str] = None
        self.f:       Optional[str] = None
        self.w:       bool          = False
        self.ol:      bool          = False
        self.ow:      bool          = False
        self.d:       List[str]     = []
        self.p:       List[str]     = []
        self.v:       bool          = False
        self.vv:      bool          = False
        self.c:       bool          = False
        self.b:       bool          = False
        self.udb:     bool          = False


# flag token  →  Args attribute name
_FLAG_MAP: dict = {
    "-h":   "help",
    "-V":   "version",
    "-w":   "w",
    "-ol":  "ol",
    "-ow":  "ow",
    "-v":   "v",
    "-vv":  "vv",
    "-c":   "c",
    "-b":   "b",
    "-udb": "udb",
}
_BOOL_FLAGS  = set(_FLAG_MAP)
_VALUE_FLAGS = {"-s", "-sf", "-f"}
_LIST_FLAGS  = {"-d", "-p"}


def parse_args(argv: List[str]) -> Args:
    args = Args()
    i    = 0

    while i < len(argv):
        tok = argv[i]

        if tok in _BOOL_FLAGS:
            setattr(args, _FLAG_MAP[tok], True)

        elif tok in _VALUE_FLAGS:
            i += 1
            if i >= len(argv):
                _die(f"Flag {tok} requires an argument.")
            setattr(args, tok.lstrip("-"), argv[i])

        elif tok in _LIST_FLAGS:
            collected: List[str] = []
            i += 1
            while i < len(argv) and not argv[i].startswith("-"):
                collected.append(argv[i])
                i += 1
            setattr(args, tok.lstrip("-"), collected)
            continue   # i is already past the collected items

        elif tok.startswith("-"):
            _die(f"Unknown flag '{tok}'  —  run  cmdref -h  for help.")

        else:
            args.query.append(tok)

        i += 1

    return args


# ──────────────────────────────────────────────────────────────────────────────
#  Utilities
# ──────────────────────────────────────────────────────────────────────────────

def _die(msg: str) -> None:
    """Print a formatted error to stderr and exit with code 1."""
    print(_c(f"\n  [!] {msg}\n", C_RED), file=sys.stderr)
    sys.exit(1)


# ──────────────────────────────────────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    argv = sys.argv[1:]

    # Bare call → show banner + help and exit cleanly
    if not argv:
        print_help()
        return

    args = parse_args(argv)

    # ── Informational flags ───────────────────────────────────────────────────
    if args.help:
        print_help()
        return

    if args.version:
        print(f"cmdref v{VERSION}")
        return

    # ── DB update ─────────────────────────────────────────────────────────────
    if args.udb:
        update_db()
        return

    # ── Workflow sourcing ─────────────────────────────────────────────────────
    if args.sf:
        source_workflow(args.sf, folder=True)
        return
    if args.s:
        source_workflow(args.s, folder=False)
        return

    # ── Determine search paths ────────────────────────────────────────────────
    if args.f:
        search_paths = [args.f]
    elif args.w:
        search_paths = [WORKFLOW_PATH]
    else:
        search_paths = [DEFAULT_DB_PATH]

    # ── Load command database ─────────────────────────────────────────────────
    entries = load_entries(search_paths)

    if not entries:
        print(_c(f"\n  [!] No command entries found in: {', '.join(search_paths)}", C_RED))
        print(_c("      • Run  cmdref -udb  to download the database from GitHub.", C_DIM))
        print(_c("      • Use  -f <path>  to point at a custom file or folder.\n",  C_DIM))
        sys.exit(1)

    # ── Filter ────────────────────────────────────────────────────────────────
    os_filter = "windows" if args.ow else "linux"

    results = [
        e for e in entries
        if _matches(e, args.query, args.d, args.p, os_filter)
    ]

    if not results:
        print(_c("\n  MEOW MEOW ! Silver kitty is confused !", C_RED + C_BLD))
        print(_c("  No commands matched your search.\n", C_DIM))
        sys.exit(1)

    # ── Display ───────────────────────────────────────────────────────────────
    display_results(results, verbose=args.v, super_verbose=args.vv)

    # ── Interactive selection  (only needed when -c or -b is active) ──────────
    if not (args.c or args.b):
        return

    if len(results) == 1:
        selected = results[0]
    else:
        prompt = _c(f"  Select command{'  to build' if args.b else ''} : ", C_CYN + C_BLD)
        try:
            raw = input(prompt).strip()
            idx = int(raw)
            if not (0 <= idx < len(results)):
                raise ValueError
            selected = results[idx]
        except (ValueError, TypeError):
            print(_c("\n  [!] Invalid selection.\n", C_RED))
            return
        except (EOFError, KeyboardInterrupt):
            print()
            return

    final_cmd = selected.command

    # ── Builder ───────────────────────────────────────────────────────────────
    if args.b:
        built = build_command(final_cmd, selected.example)
        if built is None:
            return
        final_cmd = built

    # ── Result output ─────────────────────────────────────────────────────────
    print()
    print(_c(f"  → {final_cmd}", C_GRN + C_BLD))

    # ── Clipboard ─────────────────────────────────────────────────────────────
    if args.c:
        if copy_to_clipboard(final_cmd):
            print(_c("  Command copied to clipboard ! :)", C_CYN))
        else:
            print(_c(
                "  [!] Clipboard unavailable — install xclip, xsel, or wl-copy.",
                C_RED,
            ))

    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Clean Ctrl-C — no traceback, exit code 0
        print()
        sys.exit(0)
