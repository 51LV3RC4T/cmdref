#!/usr/bin/env python3
"""
cmdref — Command Referencer
Automates variable switching in workflows and speeds up finding the right commands.

Usage:
    cmdref <search terms> [options]
"""

import os
import re
import sys
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

# ──────────────────────────────────────────────────────────────────────────────
#  Constants
# ──────────────────────────────────────────────────────────────────────────────

DEFAULT_DB_PATH = "/etc/cmdref/db"
WORKFLOW_PATH   = "/etc/cmdref/workflow"
GIT_REPO_URL    = "https://github.com/51LV3RC4T/cmdref"  # Set your repo here

BANNER = r"""
  ██████╗███╗   ███╗██████╗ ██████╗ ███████╗███████╗
 ██╔════╝████╗ ████║██╔══██╗██╔══██╗██╔════╝██╔════╝
 ██║     ██╔████╔██║██║  ██║██████╔╝█████╗  █████╗
 ██║     ██║╚██╔╝██║██║  ██║██╔══██╗██╔══╝  ██╔══╝
 ╚██████╗██║ ╚═╝ ██║██████╔╝██║  ██║███████╗██║
  ╚═════╝╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝
  Command Referencer  |  ~ Silver Kitty's Tool ~
"""

# ──────────────────────────────────────────────────────────────────────────────
#  Variable Registry  (mirrors variable_defined.md)
# ──────────────────────────────────────────────────────────────────────────────

VARIABLES: dict = {
    "cmd_ref_target":           {"display": "Target's IP",            "default": "10.10.10.10"},
    "cmd_ref_attacker":         {"display": "Attacker's IP",          "default": "127.0.0.1"},
    "cmd_ref_target_port":      {"display": "Target PORT",            "default": "51"},
    "cmd_ref_attacker_port":    {"display": "Attacker PORT",          "default": "9999"},
    "cmd_ref_domain":           {"display": "Domain",                 "default": "silver.cat"},
    "cmd_ref_url":              {"display": "URL",                    "default": "http://silver.cat"},
    "cmd_ref_protocol":         {"display": "Protocol",               "default": ""},
    "cmd_ref_param_file":       {"display": "Input file",             "default": ""},
    "cmd_ref_param_file_users": {"display": "Input users file",       "default": ""},
    "cmd_ref_param_file_pass":  {"display": "Input Passwords file",   "default": ""},
    "cmd_Ref_target_hash":      {"display": "NTLM Hash",              "default": ""},
}

# ──────────────────────────────────────────────────────────────────────────────
#  ANSI Colors
# ──────────────────────────────────────────────────────────────────────────────

C_RESET   = "\033[0m"
C_BOLD    = "\033[1m"
C_DIM     = "\033[2m"
C_CYAN    = "\033[96m"
C_GREEN   = "\033[92m"
C_YELLOW  = "\033[93m"
C_RED     = "\033[91m"
C_MAGENTA = "\033[95m"
C_BLUE    = "\033[94m"

def c(text: str, *codes: str) -> str:
    """Wrap text with ANSI codes and reset at the end."""
    return "".join(codes) + str(text) + C_RESET


# ──────────────────────────────────────────────────────────────────────────────
#  Data Model
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class CommandEntry:
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
    Parse a single text block (between --- separators) into a CommandEntry.
    Returns None if the block contains no ```cmd section.
    """
    # Must have a command block to be valid
    if "```cmd" not in block and "```command" not in block:
        return None

    entry = CommandEntry(raw_block=block.strip(), source_file=source)

    # ── Description ──────────────────────────────────────────────────────────
    m = re.search(
        r"Description\s*:\s*(.*?)(?=\n\s*Parameters\s*:|```|\n\s*Tags\s*:|$)",
        block, re.DOTALL | re.IGNORECASE
    )
    if m:
        entry.description = m.group(1).strip()

    # ── Parameters ───────────────────────────────────────────────────────────
    m = re.search(
        r"Parameters\s*:\s*(.*?)(?=```|\n\s*Tags\s*:|$)",
        block, re.DOTALL | re.IGNORECASE
    )
    if m:
        entry.parameters = re.findall(r"#(\w+)", m.group(1))

    # ── Command block (```cmd ... ```) ───────────────────────────────────────
    m = re.search(r"```(?:cmd|command)\s*\n(.*?)```", block, re.DOTALL)
    if m:
        entry.command = m.group(1).strip()
    else:
        return None   # no command → skip

    # ── Example block (```exp / ```example) ──────────────────────────────────
    m = re.search(r"```(?:exp|example)\s*\n(.*?)```", block, re.DOTALL)
    if m:
        entry.example = m.group(1).strip()

    # ── Tags ─────────────────────────────────────────────────────────────────
    m = re.search(r"Tags\s*:\s*(.*?)$", block, re.MULTILINE | re.IGNORECASE)
    if m:
        entry.tags = [t.lower() for t in re.findall(r"#(\w+)", m.group(1))]

    # ── OS type ──────────────────────────────────────────────────────────────
    has_linux   = "linux"   in entry.tags
    has_windows = "windows" in entry.tags
    if has_linux and has_windows:
        entry.os_type = "both"
    elif has_windows:
        entry.os_type = "windows"
    else:
        entry.os_type = "linux"

    return entry


def parse_file(filepath: str) -> List[CommandEntry]:
    """Read a markdown DB file and return all valid CommandEntry objects."""
    try:
        text = Path(filepath).read_text(encoding="utf-8")
    except OSError as e:
        print(c(f"  [!] Cannot read {filepath}: {e}", C_RED), file=sys.stderr)
        return []

    entries: List[CommandEntry] = []
    for block in re.split(r"\n---+\n", text):
        entry = _parse_block(block, filepath)
        if entry:
            entries.append(entry)
    return entries


def collect_md_files(path: str) -> List[str]:
    """Return all .md files from a path (either a single file or a directory)."""
    p = Path(path)
    if not p.exists():
        return []
    if p.is_file():
        return [str(p)] if p.suffix == ".md" else []
    return sorted(str(f) for f in p.rglob("*.md"))


def load_entries(paths: List[str]) -> List[CommandEntry]:
    """Load and parse all markdown files from a list of paths."""
    entries: List[CommandEntry] = []
    for path in paths:
        for fp in collect_md_files(path):
            entries.extend(parse_file(fp))
    return entries


# ──────────────────────────────────────────────────────────────────────────────
#  Search / Filter
# ──────────────────────────────────────────────────────────────────────────────

def entry_matches(
    entry:       CommandEntry,
    query_terms: List[str],
    desc_terms:  List[str],
    param_terms: List[str],
    os_filter:   str,          # "linux" | "windows"
) -> bool:
    """Return True when the entry satisfies all active search criteria."""

    # ── OS filter ────────────────────────────────────────────────────────────
    if os_filter == "linux"   and entry.os_type == "windows":
        return False
    if os_filter == "windows" and entry.os_type == "linux":
        return False

    # ── General query (command + description + tags) ──────────────────────
    haystack = " ".join([entry.command, entry.description] + entry.tags).lower()
    for term in query_terms:
        if term.lower() not in haystack:
            return False

    # ── Description search (-d) ───────────────────────────────────────────
    for term in desc_terms:
        if term.lower() not in entry.description.lower():
            return False

    # ── Parameter search (-p) ─────────────────────────────────────────────
    param_haystack = " ".join(entry.parameters).lower()
    for term in param_terms:
        if term.lower() not in param_haystack:
            return False

    return True


# ──────────────────────────────────────────────────────────────────────────────
#  Display
# ──────────────────────────────────────────────────────────────────────────────

def display_results(
    results:       List[CommandEntry],
    verbose:       bool,
    super_verbose: bool,
) -> None:
    print()
    count_str = c(f"{len(results)} found", C_DIM)
    print(c(f"  Possible Commands : ", C_BOLD + C_CYAN) + c(f"({len(results)} found)", C_DIM))
    print()

    for i, entry in enumerate(results):
        # Highlight {{variables}} in the command string
        cmd_display = re.sub(
            r"(\{\{[\w]+\}\})",
            lambda m: c(m.group(1), C_YELLOW),
            entry.command,
        )
        print(f"  {c(str(i) + '.', C_BOLD + C_CYAN)}  {c(cmd_display, C_GREEN)}")

        if verbose or super_verbose:
            if entry.description:
                print(f"       {c('↳ ' + entry.description, C_DIM)}")

        if super_verbose:
            print()
            print(c("     ┌─── Full Entry " + "─" * 40, C_MAGENTA + C_DIM))
            for line in entry.raw_block.splitlines():
                print(c("     │ ", C_MAGENTA + C_DIM) + line)
            print(c("     └" + "─" * 55, C_MAGENTA + C_DIM))

        print()


# ──────────────────────────────────────────────────────────────────────────────
#  Builder  (-b flag)
# ──────────────────────────────────────────────────────────────────────────────

def extract_placeholders(command: str) -> List[str]:
    """Return unique ordered list of {{variable}} names in a command."""
    seen = set()
    result = []
    for var in re.findall(r"\{\{(\w+)\}\}", command):
        if var not in seen:
            seen.add(var)
            result.append(var)
    return result


def build_command(command: str, example: str) -> Optional[str]:
    """
    Interactively replace each {{variable}} placeholder.
    Returns the final command string, or None on failure/abort.
    """
    placeholders = extract_placeholders(command)

    if not placeholders:
        return command

    print()
    print(c("  Specify parameter values :", C_BOLD + C_CYAN))
    print()

    substitutions: dict = {}

    for var in placeholders:
        info         = VARIABLES.get(var, {})
        display_name = info.get("display", var.replace("_", " ").title())
        default_val  = info.get("default", "")

        prompt = f"  {c(display_name, C_YELLOW)}"
        if default_val:
            prompt += f" {c('[' + default_val + ']', C_DIM)}"
        prompt += " : "

        try:
            value = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return None

        if not value:
            if default_val:
                value = default_val
            else:
                print(c("\n  MEOW MEOW ! Silver kitty is confused !", C_RED + C_BOLD))
                if example:
                    print(c(f"  Example : {example}", C_DIM))
                print()
                return None

        substitutions[var] = value

    result = command
    for var, val in substitutions.items():
        result = result.replace(f"{{{{{var}}}}}", val)

    return result


# ──────────────────────────────────────────────────────────────────────────────
#  Clipboard  (-c flag)
# ──────────────────────────────────────────────────────────────────────────────

def copy_to_clipboard(text: str) -> bool:
    """Try multiple clipboard backends. Returns True on success."""
    candidates = [
        ["xclip", "-selection", "clipboard"],
        ["xsel",  "--clipboard", "--input"],
        ["wl-copy"],
        ["pbcopy"],            # macOS
        ["clip"],              # Windows (WSL)
    ]
    for cmd in candidates:
        if shutil.which(cmd[0]):
            try:
                subprocess.run(cmd, input=text.encode(), check=True,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
            except subprocess.CalledProcessError:
                continue
    return False


# ──────────────────────────────────────────────────────────────────────────────
#  DB Update  (-udb flag)
# ──────────────────────────────────────────────────────────────────────────────

def update_db() -> None:
    print(c(f"\n  [*] Updating DB from : {GIT_REPO_URL}", C_CYAN))

    if not shutil.which("git"):
        print(c("  [!] git is not installed or not in PATH.", C_RED))
        return

    tmp = "/tmp/cmdref_db_update"

    try:
        if os.path.exists(tmp):
            shutil.rmtree(tmp)

        result = subprocess.run(
            ["git", "clone", "--depth=1", GIT_REPO_URL, tmp],
            capture_output=True,
        )
        if result.returncode != 0:
            print(c(f"  [!] Git error: {result.stderr.decode().strip()}", C_RED))
            return

        db_src = os.path.join(tmp, "db")
        if not os.path.isdir(db_src):
            print(c("  [!] The repository has no /db directory.", C_RED))
            return

        if os.path.exists(DEFAULT_DB_PATH):
            shutil.rmtree(DEFAULT_DB_PATH)
        shutil.copytree(db_src, DEFAULT_DB_PATH)
        shutil.rmtree(tmp, ignore_errors=True)

        print(c("  [✓] DB updated successfully!\n", C_GREEN))

    except Exception as e:
        print(c(f"  [!] Update failed: {e}", C_RED))


# ──────────────────────────────────────────────────────────────────────────────
#  Workflow Sourcing  (-s / -sf flags)
# ──────────────────────────────────────────────────────────────────────────────

def source_workflow(source: str, folder: bool = False) -> None:
    os.makedirs(WORKFLOW_PATH, exist_ok=True)
    src = Path(source)

    if not src.exists():
        print(c(f"  [!] Source not found: {source}", C_RED))
        return

    dst = Path(WORKFLOW_PATH) / src.name

    if folder:
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(c(f"  [✓] Folder copied to {dst}", C_GREEN))
    else:
        shutil.copy2(src, dst)
        print(c(f"  [✓] File copied to {dst}", C_GREEN))


# ──────────────────────────────────────────────────────────────────────────────
#  Help Text
# ──────────────────────────────────────────────────────────────────────────────

def print_help() -> None:
    print(BANNER)
    print(c("  Usage:", C_BOLD + C_CYAN))
    print("    cmdref <search terms> [options]\n")

    flags = [
        ("-h",        "",         "Help — display this menu"),
        ("-s",        "<file>",   "Source workflow file  →  copy to /etc/cmdref/workflow"),
        ("-sf",       "<folder>", "Source workflow folder →  copy to /etc/cmdref/workflow"),
        ("-f",        "<path>",   "Search only in specified file or folder"),
        ("-w",        "",         "Search in /etc/cmdref/workflow directory"),
        ("-ol",       "",         "Linux commands  [default when -ow is not set]"),
        ("-ow",       "",         "Windows commands"),
        ("-d",        "<terms>",  "Match terms in description"),
        ("-p",        "<terms>",  "Match terms in parameters field"),
        ("-v",        "",         "Verbose — show description of each result"),
        ("-vv",       "",         "Super-verbose — show full command block"),
        ("-c",        "",         "Copy selected command to clipboard"),
        ("-b",        "",         "Builder — replace {{variables}} interactively"),
        ("-udb",      "",         "Update DB — fetch /db from git repo"),
    ]

    print(c("  Flags:", C_BOLD + C_CYAN))
    for flag, arg, desc in flags:
        flag_str = c(f"{flag:<6}", C_YELLOW + C_BOLD)
        arg_str  = c(f"{arg:<10}", C_DIM)
        print(f"    {flag_str} {arg_str}  {desc}")

    print()
    print(c("  Example:", C_BOLD + C_CYAN))
    print(c("    cmdref nmap -d aggressive scan -p outfile -c -b\n", C_GREEN))


# ──────────────────────────────────────────────────────────────────────────────
#  Argument Parser  (manual, to support -vv and -udb without argparse conflicts)
# ──────────────────────────────────────────────────────────────────────────────

class Args:
    """Simple namespace populated by our manual parser."""
    def __init__(self):
        self.query:   List[str]      = []
        self.help:    bool           = False
        self.s:       Optional[str]  = None
        self.sf:      Optional[str]  = None
        self.f:       Optional[str]  = None
        self.w:       bool           = False
        self.ol:      bool           = False
        self.ow:      bool           = False
        self.d:       List[str]      = []
        self.p:       List[str]      = []
        self.v:       bool           = False
        self.vv:      bool           = False
        self.c:       bool           = False
        self.b:       bool           = False
        self.udb:     bool           = False


def parse_args(argv: List[str]) -> Args:
    """
    Manual argument parser to handle flags like -vv and -udb that argparse
    struggles with alongside positional arguments.
    """
    args = Args()
    i = 0
    option_flags = {"-h", "-w", "-ol", "-ow", "-v", "-vv", "-c", "-b", "-udb"}
    value_flags  = {"-s", "-sf", "-f"}
    list_flags   = {"-d", "-p"}

    # Explicit flag → Args attribute name mapping
    flag_attr = {
        "-h":   "help",
        "-w":   "w",
        "-ol":  "ol",
        "-ow":  "ow",
        "-v":   "v",
        "-vv":  "vv",
        "-c":   "c",
        "-b":   "b",
        "-udb": "udb",
    }

    while i < len(argv):
        tok = argv[i]

        if tok in option_flags:
            setattr(args, flag_attr[tok], True)
        elif tok in value_flags:
            i += 1
            if i >= len(argv):
                print(c(f"  [!] {tok} requires an argument.", C_RED))
                sys.exit(1)
            setattr(args, tok.lstrip("-"), argv[i])
        elif tok in list_flags:
            collected: List[str] = []
            i += 1
            while i < len(argv) and not argv[i].startswith("-"):
                collected.append(argv[i])
                i += 1
            setattr(args, tok.lstrip("-"), collected)
            continue   # don't increment again
        elif tok.startswith("-"):
            print(c(f"  [!] Unknown flag: {tok}  (try -h for help)", C_RED))
            sys.exit(1)
        else:
            args.query.append(tok)

        i += 1

    return args


# ──────────────────────────────────────────────────────────────────────────────
#  Main
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:
    argv = sys.argv[1:]

    # Show help when called bare
    if not argv:
        print_help()
        return

    args = parse_args(argv)

    # ── Help ─────────────────────────────────────────────────────────────────
    if args.help:
        print_help()
        return

    # ── DB Update ────────────────────────────────────────────────────────────
    if args.udb:
        update_db()
        return

    # ── Source Workflow ──────────────────────────────────────────────────────
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

    # ── Load entries ──────────────────────────────────────────────────────────
    entries = load_entries(search_paths)

    if not entries:
        print(c(f"\n  [!] No command entries found in: {', '.join(search_paths)}", C_RED))
        print(c("      Run  cmdref -udb  to download the database.\n", C_DIM))
        return

    # ── OS filter (Linux by default) ──────────────────────────────────────────
    os_filter = "windows" if args.ow else "linux"

    # ── Filter results ────────────────────────────────────────────────────────
    results = [
        e for e in entries
        if entry_matches(e, args.query, args.d, args.p, os_filter)
    ]

    if not results:
        print(c("\n  MEOW MEOW ! Silver kitty is confused !", C_RED + C_BOLD))
        print(c("  No commands matched your search.\n", C_DIM))
        return

    # ── Display ───────────────────────────────────────────────────────────────
    display_results(results, verbose=args.v, super_verbose=args.vv)

    # ── Selection prompt (only when -c or -b requested) ───────────────────────
    if not (args.c or args.b):
        return

    if len(results) == 1:
        selected = results[0]
    else:
        label = "to build" if args.b else ""
        prompt = c(f"  Select command {label} : ", C_CYAN + C_BOLD)
        try:
            raw = input(prompt).strip()
            idx = int(raw)
            if not (0 <= idx < len(results)):
                raise ValueError
            selected = results[idx]
        except (ValueError, TypeError):
            print(c("\n  [!] Invalid selection.\n", C_RED))
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

    # ── Output ────────────────────────────────────────────────────────────────
    print()
    print(c(f"  → {final_cmd}", C_GREEN + C_BOLD))

    # ── Clipboard ─────────────────────────────────────────────────────────────
    if args.c:
        if copy_to_clipboard(final_cmd):
            print(c("  Command copied to clipboard ! :)", C_CYAN))
        else:
            print(c(
                "  [!] Clipboard copy failed.  "
                "Install xclip, xsel, or wl-copy and try again.",
                C_RED
            ))
    print()


if __name__ == "__main__":
    main()
