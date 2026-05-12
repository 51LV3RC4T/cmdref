# cmdref

**Command Referencer** — fast, offline-friendly lookup for penetration-testing and Linux operations. Search a curated Markdown command database, preview substitutions, build `{{variables}}` interactively, and copy results to the clipboard without leaving the terminal.

Designed to feel at home next to tools on **Kali Linux** and similar distros: plain Python 3, no database daemon, and a workflow that matches how operators actually work.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-3776ab.svg)](https://www.python.org/)
**Release:** 4.0.0 (see `cmdref.py` `VERSION`)

---

## Features

| Capability | Description |
|------------|-------------|
| **Fuzzy search** | Typo-tolerant matching when `rapidfuzz` is installed |
| **Tags & description filters** | Narrow by `#linux` / `#web` / `-d` description keywords |
| **Variable preview** | `{{placeholders}}` filled from `variables.md` and session memory |
| **Interactive builder** | `-b` prompts for each variable; values persist in `~/.cmdref/session.json` |
| **Pane view** | `-vp` full-screen TUI: list + detail split (requires curses) |
| **Profiles** | Multiple search roots under `~/.cmdref/profiles/` |
| **Clipboard** | `-c` copies via `xclip`, `xsel`, `wl-copy`, `pbcopy`, or Windows `clip` |
| **Cache** | JSON cache under `~/.cmdref/cache/` for fast repeat searches |
| **Portable core** | Runs without `curses` (search, builder, clipboard); `-vp` needs curses or `windows-curses` |

---

## Requirements

- **Python** 3.7 or newer  
- **`rapidfuzz`** (recommended): `pip install -r requirements.txt`  
- **Curses** (for `-vp`): included on Linux/macOS; on **Windows** install [`windows-curses`](https://pypi.org/project/windows-curses/)  
- **Optional**: `git` (for `cmdref -udb`), clipboard tools as listed in `requirements.txt`

---

## Installation

### Option A — System-wide (Kali / Debian-style)

From the repository root:

```bash
sudo python3 install.py
```

This installs:

- `/usr/local/bin/cmdref`
- `/etc/cmdref/db` — populated from the bundled `db/` tree when present
- `/etc/cmdref/workflow` — managed workflow copies

Remove with:

```bash
sudo python3 install.py --uninstall
```

### Option B — Run from a clone (no root)

```bash
git clone https://github.com/51LV3RC4T/cmdref.git
cd cmdref
pip install -r requirements.txt   # optional but recommended

python3 cmdref.py -h
# or: chmod +x cmdref.py && ./cmdref.py -h
```

With this mode, cmdref loads **`db/`** next to `cmdref.py` when the system path `/etc/cmdref/db` is not your active profile source—point a profile at your clone’s `db` with `-ws` or edit `~/.cmdref/profiles/*.json` if needed.

### Windows

```powershell
pip install -r requirements.txt
pip install windows-curses   # for -vp / --pane-view
python cmdref.py -h
```

---

## Quick start

```bash
# Help and version
cmdref -h
cmdref -V

# Search (default profile uses /etc/cmdref/db after install)
cmdref nmap
cmdref smb enum -v

# Interactive split pane (real TTY required)
cmdref nmap -vp

# Build placeholders then copy
cmdref reverse shell -b -c

# Search only your notes
cmdref -s ~/labs/target.md creds

# Windows-only tagged entries
cmdref mimikatz -ow
```

---

## Database format

Commands live in **`db/**/*.md`**. Each entry is a block separated by `---` and follows the structure in **`db/Template/Command Template.md`**:

- `Description :` — short summary  
- `Parameters :` — `#var` names matching `{{var}}` in the command  
- ` ```cmd` / ` ```command` — the command template  
- ` ```example` / ` ```exp` — concrete example  
- `Tags :` — e.g. `#linux #oscp #web`

Default substitution values come from **`db/Template/variables.md`** (and session overrides). Tun0-style attacker IP detection fills `attacker-ip` when the template says so.

---

## Profiles & workflows

- **Profiles** store lists of directories or files to search (`~/.cmdref/profiles/<name>.json`).  
- **Active profile** is stored in `~/.cmdref/config.json`.  
- **`-ws`** copies a workflow path into `/etc/cmdref/workflow/<profile>/` and adds it to the profile (typically requires write access to that tree).

Profile names are restricted to safe characters (no `/`, `\`, or `..`) to avoid path traversal.

---

## Security & trust model

cmdref is a **lookup and string templating** tool: it does **not** execute the commands it displays. You paste or run them in your own shell.

| Area | Behavior |
|------|----------|
| **Markdown sources** | Treat DB files like code: only add paths you trust. Single files are capped at **5 MB** per read. |
| **Directory index** | Symbolic links are **skipped** when collecting `*.md` under a directory. |
| **`cmdref -udb`** | Clones only the configured **`GIT_REPO_URL`**, validated by an internal allowlist regex; uses `mkdtemp` and `git` without `shell=True`. |
| **Subprocess** | `ip addr`, `git clone`, and clipboard helpers use argument lists, not shell strings. |
| **Session file** | `~/.cmdref/session.json` — size-capped on load; stores variable defaults (plain JSON). |
| **Profiles** | Names validated; workflow deletes only unlink paths under the managed workflow directory. |
| **Profile paths** | JSON lists normalized; null bytes rejected; capped count. |
| **CLI paths** | `-s`, `-O`, `-ws` reject embedded null bytes. |
| **Config / profile JSON** | Size capped when loading. |
| **Cache** | Rejects oversized `entries` arrays. |
| **Builder** | Built command capped at 2 MB. |
| **Clipboard** | Data to OS clipboard helpers; ANSI stripped first. |

`~/.cmdref` may contain **session defaults and cached parsed entries**. On shared machines use restrictive permissions (e.g. `chmod 700 ~/.cmdref`) and avoid storing live credentials in `variables.md` or session files.

If you need **maximum isolation**, run cmdref in a VM, use a dedicated profile pointing only at your own `db/`, and audit third-party Markdown before indexing.

---

## Legal & ethical use

This software is intended for **authorized security testing**, **education**, and **system administration** on systems you own or have explicit permission to assess. Misuse is solely your responsibility. See the [MIT License](LICENSE).

---

## Project layout

```text
cmdref.py          # CLI entry point
install.py         # Optional system installer
db/
  Template/        # Command template, variables, categories
  Linux Fundamentals/
  PEN-200/
  Toolkit/         # Reverse shells, NetExec, Impacket, BloodHound Cypher, SQLi, ligolo-ng, …
tests/
  test_cmdref.py   # unittest edge cases (run from repo root)
requirements.txt
```

---

## Testing

From the repository root:

```bash
python3 -m unittest tests.test_cmdref -v
```

This covers profile-path normalization, Markdown parsing, search edge cases, and cache-entry coercion. Full `-vp` behaviour requires a TTY and curses (install `windows-curses` on Windows to include curses in the same interpreter).

---

## Troubleshooting

| Issue | What to try |
|--------|----------------|
| **Pane (`-vp`) fails or is blank** | Use a real TTY (QTerminal, Terminator, xterm, etc.). **tmux:** `TERM` should be `tmux-256color` or `screen-256color` inside the session — cmdref fixes common mis-set `xterm*` values automatically. Override with `CMDREF_TMUX_TERM` if needed. On Windows, `import curses` fails until you `pip install windows-curses` (other features still work). |
| **Esc / arrows wrong in tmux** | cmdref sets `ESCDELAY` (override with `CMDREF_ESC_DELAY`, milliseconds). In `~/.tmux.conf`: `set -g escape-time 10` often helps other TUI apps too. |
| **No results** | Run `cmdref -ps` to see profile paths; confirm `db` exists and contains ` ```cmd` blocks. |
| **Clipboard copy fails** | Install `xclip`, `xsel`, or `wl-clipboard` on Linux; use `pbcopy` on macOS; `clip` on Windows. |
| **`rapidfuzz` missing** | Search still works with a simpler scorer; `pip install rapidfuzz` for fuzzy matching. |

---

## Credits

- **Author:** 51LV3RC4T  
- **Repository:** [github.com/51LV3RC4T/cmdref](https://github.com/51LV3RC4T/cmdref)  
- **License:** MIT

---

*“Know your commands before you run them.”*
