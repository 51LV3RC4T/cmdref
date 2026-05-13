<div align="center">

```
 ██████╗███╗   ███╗██████╗ ██████╗ ███████╗███████╗
 ██╔════╝████╗ ████║██╔══██╗██╔══██╗██╔════╝██╔════╝
 ██║     ██╔████╔██║██║  ██║██████╔╝█████╗  █████╗
 ██║     ██║╚██╔╝██║██║  ██║██╔══██╗██╔══╝  ██╔══╝
 ╚██████╗██║ ╚═╝ ██║██████╔╝██║  ██║███████╗██║
  ╚═════╝╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝
```

**Command Referencer** — A terminal-first command reference tool for offensive security workflows.

[![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=flat-square)]()
[![Zero Extra Setup](https://img.shields.io/badge/Core-No%20Root%20Needed-brightgreen?style=flat-square)]()

**v5.5.0**

</div>

---

## Table of Contents

- [What is cmdref?](#what-is-cmdref)
- [Demo](#demo)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Flag Reference](#flag-reference)
- [Writing Your Own Cheatsheet](#writing-your-own-cheatsheet)
  - [The Command Template](#the-command-template)
  - [Variable Reference](#variable-reference)
  - [A Complete Entry Example](#a-complete-entry-example)
  - [Tips for Good Entries](#tips-for-good-entries)
- [Working with Profiles](#working-with-profiles)
  - [What is a Profile?](#what-is-a-profile)
  - [Creating a Profile](#creating-a-profile)
  - [Adding Workflows to a Profile](#adding-workflows-to-a-profile)
  - [Searching Within a Profile](#searching-within-a-profile)
  - [Managing Profiles](#managing-profiles)
- [The Pane View](#the-pane-view)
- [Builder Mode & Copy (`-b` / `-c`)](#builder-mode--copy--b---c)
- [Shell Environment Shortcuts](#shell-environment-shortcuts)
- [Session Memory](#session-memory)
- [Updating the Database](#updating-the-database)
- [Team Database Sync](#team-database-sync)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)
- [Security Notes](#security-notes)
- [Legal & Ethical Use](#legal--ethical-use)
- [License](#license)

---

## What is cmdref?

During an engagement you spend a surprising amount of time looking up flags, retyping IPs, and hunting through old notes. `cmdref` solves all three.

Store your commands as plain Markdown files. `cmdref` indexes them, fuzzy‑searches tags and text, and turns `{{variables}}` into real values using your **session file**, **`CMDREF_*`** environment exports, familiar pentest **`RHOST` / `LHOST`**-style shell variables, and **`variables.md`**. Use **`-b`** to step through every placeholder interactively, or **`-c`** when the shell already knows the target and you only need prompts for gaps.

```bash
cmdref nmap -b -c
```

```
 Results · 4 match(es)

 1. nmap -sC -sV -oN {{file}} {{target-ip}}
 2. nmap -p- --min-rate 5000 -oN {{file}} {{target-ip}}
 ...

 Select [1-4] › 2

 › nmap -p- --min-rate 5000 -oN recon/full-ports 10.10.10.50
 ✓ Copied to clipboard.
```

---

## Demo

> Full walkthrough of search, pane view, builder, and profiles.

https://github.com/51LV3RC4T/cmdref/assets/demo.mp4

---

## Features

| | Feature | Description |
|:---|:---|:---|
| 🔍 | **Fuzzy search** | Typo-tolerant ranking powered by `rapidfuzz` |
| 🗂️ | **Tag & description filters** | Narrow by `-d` words or `-a` variable names |
| 👁️ | **Variable preview** | See `{{placeholders}}` filled with defaults before you commit |
| 🛠️ | **Builder (`-b`)** | Walk every placeholder; answers persist as sticky defaults |
| 🖥️ | **Pane view** | `-vp` full-screen split TUI: result list left, full detail right |
| 📁 | **Profiles** | Separate search roots per project or engagement |
| 📋 | **Smart copy (`-c`)** | Session + `CMDREF_*` + `RHOST`/`LHOST`-style env + `variables.md`; prompt only if unknown |
| ⚡ | **JSON cache** | Parses once; re-uses cached index until source files change |
| 🐚 | **Integrated shell** | `-e` drops into a persistent `ref ›` REPL |
| 🔄 | **DB update** | `-udb` pulls the latest community database from GitHub |
| 👥 | **Team-db sync** | `-ts <url>` mirrors a repo's markdown tree into `/etc/cmdref/db/team-db` |
| 🟢 | **Portable core** | Runs on Python 3.7+ with no external deps (`rapidfuzz` optional) |

---

## Requirements

| Requirement | Notes |
|:---|:---|
| **Python 3.7+** | Pre-installed on Kali, Parrot, and most Linux distros |
| **rapidfuzz** | Optional but strongly recommended for fuzzy search — `pip install rapidfuzz` |
| **curses** | Built into Python on Linux/macOS. On Windows: `pip install windows-curses` |
| **git** | Needed for `cmdref -udb` and team-db sync (`-ts`) |
| **Clipboard tool** | See table below |

**Clipboard backends** (install one):

| Platform | Package |
|:---|:---|
| Linux X11 | `sudo apt install xclip` |
| Linux X11 | `sudo apt install xsel` |
| Linux Wayland | `sudo apt install wl-clipboard` |
| macOS | `pbcopy` — built-in |
| WSL / Windows | `clip.exe` — built-in |

---

## Installation

### Option A — System-wide (recommended on Kali / Parrot)

```bash
git clone https://github.com/51LV3RC4T/cmdref.git
cd cmdref
pip install -r requirements.txt
sudo python3 install.py
```

The installer creates `/usr/local/bin/cmdref`, populates `/etc/cmdref/db` from the bundled `db/` tree, and creates `/etc/cmdref/workflow`.

**Uninstall:**

```bash
sudo python3 install.py --uninstall
```

### Option B — Run from clone (no root required)

```bash
git clone https://github.com/51LV3RC4T/cmdref.git
cd cmdref
pip install -r requirements.txt
python3 cmdref.py -h
```

In this mode, point a profile at your clone's `db/` folder:

```bash
python3 cmdref.py -pc mydb
python3 cmdref.py -ws ./db -p mydb
python3 cmdref.py -p mydb nmap
```

### Option C — Windows

```bash
pip install -r requirements.txt
pip install windows-curses  # enables -vp pane view
python cmdref.py -h
```

---

## Quick Start

```bash
# Show full help and flag reference
cmdref -h

# Check version
cmdref -V

# Basic keyword search (Linux commands, default profile)
cmdref nmap
cmdref smb enum
cmdref reverse shell

# Verbose — show descriptions
cmdref nmap -v

# Smart copy — fill from session / RHOST / CMDREF_* / variables.md; prompt only if unknown
cmdref nmap -c

# Builder — confirm every {{variable}} interactively, optionally copy
cmdref nmap -b -c

# Interactive pane view
cmdref nmap -vp

# Windows-tagged commands only
cmdref mimikatz -ow

# Search a specific file or folder (no profile needed)
cmdref nmap -s ~/notes/nmap.md

# Open the persistent interactive shell
cmdref -e
```

---

## Flag Reference

```
cmdref <query> [flags]
```

### Basic

| Flag | Long form | Argument | Description |
|:---|:---|:---|:---|
| `-h` | `--help` | — | Display this help menu |
| `-V` | `--version` | — | Print version and exit |
| `-v` | `--verbose` | — | Show description under each result |
| `-vp` | `--pane-view` | — | Interactive split-pane TUI |
| `-d` | `--description` | `<words>` | Match words in the description field |
| `-a` | `--argument` | `<names>` | Filter entries by variable name (e.g. `target-ip`) |
| `-s` | `--source` | `<path>` | Search a specific file or folder, bypassing the active profile |
| `-ow` | `--os-windows` | — | Windows-tagged commands only (default: Linux) |
| `-O` | `--outfile` | `<path>` | Write results to a plain-text file |
| `-udb` | `--update-db` | — | Pull latest `/db` from GitHub and rebuild cache |
| `-uw` | `--update-workflow` | — | Rebuild cache for the active profile's workflows |

### Team database

| Flag | Long form | Argument | Description |
|:---|:---|:---|:---|
| `-ts` | `--team-sync` | `<url>` | Shallow-clone the repo and replace `/etc/cmdref/db/team-db` with its markdown tree |
| `-td` | `--team-dry-run` | — | With `-ts`: print paths that would sync; do not write |
| `-tb` | `--team-branch` | `<branch>` | Optional branch for the clone |
| `-tp` | `--team-path` | `<path>` | Folder inside the repo to copy [default: `team-db`]; also tries `db/` |

### Profiles & Workflows

| Flag | Long form | Argument | Description |
|:---|:---|:---|:---|
| `-p` | `--profile` | `<name>` | Use a named profile for this search |
| `-pc` | `--profile-create` | `<name>` | Create a new empty profile |
| `-pd` | `--profile-delete` | `<name>` | Delete a profile and its managed workflows |
| `-pr` | `--profile-rename` | `<old> <new>` | Rename a profile |
| `-ps` | `--profile-selected` | — | Show the currently active profile and its sources |
| `-ws` | `--workflow-source` | `<path> -p <name>` | Copy a workflow file/folder into a profile |
| `-wd` | `--workflow-delete` | `[-p <name>]` | Remove a workflow from a profile (interactive list if no name given) |

### Power

| Flag | Long form | Description |
|:---|:---|:---|
| `-b` | `--builder` | Interactively prompt for each `{{variable}}`; store answers as new defaults |
| `-c` | `--copy` | Copy the resolved command: auto-fill from env/session, prompt only when a value is unknown |
| `-e` | `--exec` | Open the interactive `ref ›` shell (REPL) |

> Flags can be combined freely: `cmdref nmap -d aggressive -b -c -vp`

---

## Writing Your Own Cheatsheet

The database is just Markdown. Any `.md` file following the format below is picked up automatically when added to a profile or searched with `-s`.

### The Command Template

Each entry lives between two `---` separator lines.

```markdown
---

Description :
  A clear, one-line description of what this command does.

Parameters :
  #variable-name #another-variable

```cmd
tool-name {{variable-name}} -flag {{another-variable}}
```

```example
tool-name 10.10.10.10 -flag output.txt
```

Tags : #toolname #category #linux

---
```

**Field reference:**

| Field | Required | Purpose |
|:---|:---:|:---|
| `Description :` | Recommended | Summary text; matched by `-d` |
| `Parameters :` | Optional | Space-separated `#variable-name` tags; matched by `-a`. Also accepts `Argument :` for backward compatibility. |
| ` ```cmd` | **Yes** | The command template with `{{variable}}` placeholders. Also accepts ` ```command`. |
| ` ```example` | Recommended | A pre-filled example; shown when builder has no default. Also accepts ` ```exp`. |
| `Tags :` | Recommended | `#keyword` labels for search; must include `#linux` or `#windows` |

> A block with no `` ```cmd `` section is silently ignored.
> Blocks with neither `#linux` nor `#windows` in their tags default to Linux.

---

### Variable Reference

These variable names are built into the tool. Use `{{variable-name}}` inside your `cmd` blocks.

| Variable | Default | Notes |
|:---|:---|:---|
| `{{target-ip}}` | *(user sets)* | |
| `{{attacker-ip}}` | tun0 IPv4 | Auto-detected at startup; falls back to `127.0.0.1` |
| `{{target-port}}` | *(user sets)* | |
| `{{attacker-port}}` | *(user sets)* | |
| `{{domain}}` | *(user sets)* | |
| `{{url}}` | *(user sets)* | |
| `{{protocol}}` | *(user sets)* | e.g. `smb`, `rdp`, `ftp` |
| `{{file}}` | *(user sets)* | Input or output file path |
| `{{user-file}}` | *(user sets)* | Usernames wordlist |
| `{{pass-file}}` | *(user sets)* | Passwords wordlist |
| `{{hash}}` | *(user sets)* | NTLM or other hash |
| `{{password}}` | `Meow!Meow!` | |
| `{{directory}}` | *(user sets)* | |
| `{{binary}}` | *(user sets)* | |
| `{{username}}` | `51lv3rc4t` | |
| `{{executable}}` | *(user sets)* | |
| `{{pid}}` | *(user sets)* | Process ID |
| `{{groupname}}` | *(user sets)* | |
| `{{servicename}}` | *(user sets)* | |

### Environment-driven defaults

Set **`CMDREF_*`** or **`CMDREF_DEFAULT_*`**, where **`*`** is the placeholder in **UPPERCASE** with hyphens as underscores (`target-ip` → **`CMDREF_TARGET_IP`**).

The same resolution order applies to previews, **`-b`**, **`-c`**, and pane **smart-copy**. **`RHOST`**, **`LHOST`**, and related exports are documented under **[Shell environment shortcuts](#shell-environment-shortcuts)** — you do not need the **`CMDREF_`** prefix for those.

```bash
export CMDREF_TARGET_IP=10.10.15.20
export CMDREF_ATTACKER_IP=10.10.14.5
export CMDREF_URL="http://10.10.10.5/"
cmdref nmap -vp
```

**Precedence:** `~/.cmdref/session.json` **>** `CMDREF_*` **>** `RHOST` / `LHOST` / … **>** `db/Template/variables.md`.

Use any custom placeholder name in your cheatsheets (`{{my-engagement-tag}}`) — cmdref prompts when nothing in that stack resolves it.

---

### A Complete Entry Example

Here is a real, production-ready entry you can drop straight into a `.md` file:

```markdown
---

Description :
  Aggressive Nmap scan saving output to a file.

Parameters : #target-ip #file

```cmd
nmap -sC -sV -oN {{file}} {{target-ip}}
```

```example
nmap -sC -sV -oN recon/initial 10.10.10.10
```

Tags : #nmap #recon #scan #linux

---

Description :
  Hydra SSH brute-force with a username and password list.

Parameters : #target-ip #user-file #pass-file

```cmd
hydra -L {{user-file}} -P {{pass-file}} ssh://{{target-ip}} -t 4
```

```example
hydra -L users.txt -P rockyou.txt ssh://10.10.10.10 -t 4
```

Tags : #hydra #bruteforce #ssh #linux

---
```

### Tips for Good Entries

- Keep `Description :` to one clear sentence — it shows up under `-v` and in the pane view detail panel.
- Every substitutable value should be a `{{variable}}`. Hard-coded IPs in `cmd` blocks defeat the builder.
- Use the `#linux` / `#windows` tag accurately — it controls which OS filter shows the entry.
- Group related commands in the same file (e.g., `nmap.md`, `smb.md`, `web.md`) so folder-level profile paths stay tidy.
- Always include an `example` block — it is displayed when the builder cannot find a default, and it shows up in the pane view.

---

## Working with Profiles

### What is a Profile?

A profile is a named collection of file and folder paths that cmdref searches together. Each profile is stored as a small JSON file in `~/.cmdref/profiles/`. The active profile is remembered between sessions.

Profiles let you keep completely separate search scopes:

| Profile | Use case |
|:---|:---|
| `default` | System DB at `/etc/cmdref/db` |
| `htb` | Your HTB notes + community toolkit |
| `client-xyz` | Notes scoped to a specific engagement |
| `web` | Only web-application attack commands |

---

### Creating a Profile

```bash
# Create a new empty profile
cmdref -pc web

# Create one for a specific engagement
cmdref -pc client-xyz
```

---

### Adding Workflows to a Profile

A workflow is any `.md` file or folder full of `.md` files that follows the command template format.

```bash
# Add a single file
cmdref -ws ~/notes/web-attacks.md -p web

# Add an entire folder of notes
cmdref -ws ~/notes/web/ -p web

# Add multiple sources to the same profile
cmdref -ws ~/notes/sqli.md -p web
cmdref -ws ~/notes/xss.md -p web
cmdref -ws ~/notes/ssti.md -p web
```

cmdref copies the files into `/etc/cmdref/workflow/web/` and registers the paths in the profile. The cache is invalidated automatically.

**Full walkthrough — from notes to searchable profile:**

```bash
# 1. Write your cheatsheet
nano ~/notes/my-toolkit.md   # follow the template above

# 2. Create a profile for it
cmdref -pc toolkit

# 3. Add the workflow
cmdref -ws ~/notes/my-toolkit.md -p toolkit

# 4. Search it
cmdref -p toolkit nmap

# 5. Switch it to be your default for this session
cmdref -p toolkit
cmdref nmap   # now searches toolkit automatically
```

---

### Searching Within a Profile

```bash
# Search using a named profile (also sets it as active for this session)
cmdref -p web nmap

# Check which profile is currently active
cmdref -ps

# Search only a specific file, bypassing profiles entirely
cmdref nmap -s ~/notes/nmap.md
```

---

### Managing Profiles

```bash
# List active profile and its source paths
cmdref -ps

# Rename a profile
cmdref -pr web web-attacks

# Delete a profile (also removes its managed workflow copies)
cmdref -pd old-engagement

# Remove one workflow from a profile (shows interactive list)
cmdref -wd -p web

# Rebuild the cache for a profile after manually editing files
cmdref -uw -p web
```

---

## The Pane View

Launch the interactive split-screen view with `-vp`:

```bash
cmdref nmap -vp
cmdref smb -vp -ow   # Windows commands in pane view
```

```
┌── Results (5) ──────────────────┬── Detail ───────────────────────────────────┐
│                                 │                                             │
│ 1. nmap -sC -sV -oN...        │ COMMAND                                     │
│▶ 2. nmap -p- --min-rate 5000..│ nmap -p- --min-rate 5000 -oN {{file}}       │
│ 3. nmap -sU --top-ports 200.. │ {{target-ip}}                               │
│ 4. nmap -A -T4 -oN ...        │                                             │
│ 5. nmap -sn {{target-ip}}      │ PREVIEW                                     │
│                                 │ nmap -p- --min-rate 5000 -oN file.txt       │
│                                 │ 10.10.10.10                                 │
│                                 │                                             │
│                                 │ DESCRIPTION                                 │
│                                 │ Full TCP port scan with rate limiting       │
│                                 │                                             │
│                                 │ ARGUMENTS                                   │
│                                 │ file → file.txt                             │
│                                 │ target-ip → 10.10.10.10                     │
│                                 │                                             │
│                                 │ TAGS                                        │
│                                 │ #nmap #recon #full #linux                   │
└─────────────────────────────────┴─────────────────────────────────────────────┘
 Navigate · Home/End · PgUp/PgDn · `b`/`Enter` build · `c` smart-copy · `e` exec · `q` quit
```

**Controls:**

| Key | Action |
|:---|:---|
| `↑` / `k` | Move selection up |
| `↓` / `j` | Move selection down |
| `Page Up` / `Page Dn` | Jump one page |
| `Home` / `End` | First / last result |
| `b` / `Enter` | Run the builder for the selected line, then copy the result |
| `c` | **Smart copy** — same autofill as **`cmdref -c`** (session → `CMDREF_*` → `RHOST`/`LHOST`/… → prompts only if still blank) |
| `e` | Run the builder, then optionally execute the result in `$SHELL` (`y` to confirm) |
| `q` / `Esc` | Quit pane view |

The **Preview** column shows the command with the full resolution chain applied (so it should match what **`c`** produces when every placeholder is known). If something is still unresolved, **`c`** drops into the same short prompts as CLI **`-c`**.

**Terminal compatibility:** The pane draws on the **root curses screen** (rather than nested subwindows) for broad terminal compatibility, including xfce **QTerminal** and similar VTE builds. If sizing is wrong, try `export CMDREF_PANE_CLEAR_LINES=1` so stale `LINES`/`COLUMNS` values are dropped before `curses` starts.

---

## Builder Mode & Copy (`-b` / `-c`)

### `-b` — interactive builder

Use **`-b`** when you want to **review and confirm every** `{{variable}}`, even if the environment already has a guess.

```bash
cmdref hydra -b -c
```

```
 Select [1-3] › 1

 ──────────────────────────────────────────────────────────
 Builder — confirm or edit each {{variable}}

 user-file [cat-users.txt] : users.txt
 pass-file [silver-pass.txt]: rockyou.txt
 target-ip [10.10.10.10]   :

 ──────────────────────────────────────────────────────────
 › hydra -L users.txt -P rockyou.txt ssh://10.10.10.10

 ✓ Copied to clipboard.
```

**Behaviour**

- Bracketed defaults follow the stack in [Shell environment shortcuts](#shell-environment-shortcuts): session → **`CMDREF_*`** → **`RHOST` / `LHOST`**-style exports → **`variables.md`**.
- **Enter** accepts; typing overrides. Each value is saved to **`~/.cmdref/session.json`** as you go.

### `-c` — smart copy

**`-c`** resolves placeholders from that same stack and **only prompts for variables that are still empty**. Ideal when you already **`export RHOST=…`** or keep **`CMDREF_*`** in your shell.

```bash
export RHOST=10.10.10.42
export LHOST=10.11.0.5
cmdref nmap -c
```

**`-b` then `-c`** means: run the full builder once, then copy the finished line (**`-c`** does not second-guess the builder output).

> **Note:** "Suggested next" command hints (e.g. for ligolo-ng workflows) are shown after a successful **`-c`** copy in CLI mode. They are not displayed inside the pane view.

---

## Shell Environment Shortcuts

Pentesters often export a small set of variables in **`msfconsole` resource scripts**, **`~/.bashrc`**, or wrappers. cmdref maps them onto `{{placeholders}}` using the same precedence as previews:

| Export | Example | Commonly fills |
|:---|:---|:---|
| **`RHOST`** | `export RHOST=10.10.10.42` | `{{target-ip}}` and other host-style placeholders |
| **`LHOST`** | `export LHOST=10.11.0.5` | `{{attacker-ip}}`, listener bind address |
| **`RPORT`** | `export RPORT=445` | `{{target-port}}` (via env alias) |
| **`LPORT`** | `export LPORT=4444` | `{{attacker-port}}` (via env alias) |
| **`CMDREF_TARGET_IP`** | `export CMDREF_TARGET_IP=10.10.10.42` | Explicit override for **`{{target-ip}}`** (wins over **`RHOST`**) |

Hyphenated names use **`CMDREF_*`** (for example **`CMDREF_TARGET_IP`** for **`{{target-ip}}`**). See **`db/Template/variables.md`** for the bundled registry.

Pane key **`c`** uses the exact same resolution path as **`cmdref -c`**.

---

## Session Memory

Anything you type during **`-b`**, **`-c`** (missing fields), or pane **smart-copy** is mirrored into **`~/.cmdref/session.json`**, so you stop retyping the same target and listener after the first run.

```bash
# First run — you confirm or type target-ip
cmdref nmap -b
# target-ip : 10.10.10.50

# Later — bracket already shows the sticky value
cmdref hydra -b
# target-ip [10.10.10.50] :
```

Session data persists across terminals. Change box? Type the new **`RHOST`** export (or override once in the builder) and every command follows.

---

## Updating the Database

```bash
# Pull the latest /db from GitHub and rebuild the cache
cmdref -udb

# If you get a permission error (system-wide install)
sudo cmdref -udb

# Rebuild the cache for a profile after manually editing .md files
cmdref -uw
cmdref -uw -p web   # for a specific profile
```

`-udb` does a `git clone --depth=1` of the repository, replaces `/etc/cmdref/db`, and invalidates the relevant cache entry. The clone is always made to a uniquely-named temp directory — no fixed `/tmp/` paths.

---

## Team Database Sync

Share a private or team cheatsheet tree in git: keep Markdown under a folder named `team-db` (or another path), then sync it into the system database.

```bash
# Replace /etc/cmdref/db/team-db with /team-db (or /db/team-db)
sudo cmdref -ts https://github.com/your-org/your-repo.git

# Preview what would be copied
sudo cmdref -ts https://github.com/your-org/your-repo.git -td

# Use a specific branch or a non-default folder inside the repo
sudo cmdref -ts https://github.com/your-org/your-repo.git -tb develop -tp notes/team-db
```

Synced files live under **`/etc/cmdref/db/team-db`**. The default profile searches all of `/etc/cmdref/db`, so new `.md` files are picked up automatically after sync (cache is invalidated for you). Use `cmdref -uw` if you ever need to force a full reparse.

---

## Troubleshooting

| Problem | Fix |
|:---|:---|
| **Pane view (`-vp`) is blank or crashes** | Use a real TTY (xfce **QTerminal**, Terminator, xterm). The pane uses a **single full-screen stdscr** layout for broad terminal compatibility. On **Windows**, `pip install windows-curses`. Try `export CMDREF_NCURSES_NO_UTF8_ACS=1` (tmux / line-drawing issues) or `export CMDREF_PANE_CLEAR_LINES=1` if the window size is wrong due to inherited `LINES`/`COLUMNS`. |
| **Arrows / Esc behave wrong inside tmux** | Set `set -g escape-time 10` in `~/.tmux.conf`. Override ncurses delay with **`CMDREF_ESC_DELAY`** (milliseconds). Confirm `TERM` is `tmux-256color` inside the session (`CMDREF_TMUX_TERM` overrides cmdref's fix). |
| **No results for anything** | Run `cmdref -ps` to confirm which profile and paths are active. Check that the paths exist and contain `.md` files with `` ```cmd `` blocks. |
| **"No entries found"** | Run `cmdref -udb` to populate `/etc/cmdref/db`, or point at your own files with `-s <path>`. |
| **Clipboard copy fails** | Install `xclip`, `xsel`, or `wl-clipboard` on Linux. `pbcopy` on macOS is built-in. `clip.exe` on WSL is built-in. |
| **`rapidfuzz` missing** | Search works without it (proportional scoring). Install with `pip install rapidfuzz` for full fuzzy/typo-tolerant matching. |
| **Cache returning stale results** | Run `cmdref -uw` to force a full reparse. The cache auto-invalidates when source file mtimes change, but manual edits via an editor that preserves mtime may need a manual rebuild. |
| **Profile paths not searched** | Run `cmdref -ps` and confirm the paths listed actually exist. Recreate with `-ws` if not. |

---

## Project Structure

```
cmdref/
├── cmdref.py              # CLI entry point
├── install.py             # Optional system-wide installer / uninstaller
├── requirements.txt         # rapidfuzz + clipboard tool notes
├── LICENSE                # MIT
│
├── db/                    # Bundled command database
│   ├── Template/
│   │   ├── Command Template.md   # Blank starter template
│   │   └── variables.md        # Default variable values
│   ├── Linux Fundamentals/     # Core Linux commands
│   ├── Offensive/              # Red-team style enumeration, shells, AD, web, polyglots
│   └── Toolkit/                # Reverse shells, NetExec, Impacket,
│                               # BloodHound Cypher, SQLi, ligolo-ng, …
│
└── tests/
    └── test_cmdref.py     # unittest coverage for parse, search, cache, profiles

~/.cmdref/                 # User data (created on first run)
├── config.json            # Active profile name
├── session.json           # Sticky variable defaults from builder
├── cache/                 # JSON index cache (one file per source path)
│   └── <hash>.json
└── profiles/              # Profile definitions
    ├── default.json
    └── <name>.json
```

---

## Security Notes

cmdref is primarily a **lookup and string templating tool**. It does not run commands unless you explicitly confirm **pane `e`** (execute) or run them yourself in the shell.

| Area | Behaviour |
|:---|:---|
| **File reads** | Individual `.md` files capped at **5 MB** |
| **Symlinks** | Skipped when collecting `.md` files under a directory |
| **`-udb` git clone** | URL validated against a strict allowlist regex; uses `mkdtemp`; no `shell=True` |
| **`-ts` team sync** | Git URL validated (no whitespace); shallow clone with list-form `git` args; only regular `.md` files are copied |
| **Subprocesses** | `ip addr`, `git`, and clipboard helpers use list-form args where possible |
| **Pane execute (`e`)** | Runs the built command with `shell=True` in `$SHELL` only after an explicit `y` confirmation |
| **Session file** | Size-capped on load; stores variable defaults in plain JSON |
| **Profile names** | Validated to reject path-traversal characters (`/`, `\`, `..`, null bytes) |
| **Cache** | Structure validated before trusting; oversized entry arrays rejected |
| **Builder output** | Resulting command string capped at 2 MB |
| **Clipboard** | ANSI escape codes stripped before data is passed to clipboard helpers |

**Shared machines:** run `chmod 700 ~/.cmdref` and avoid storing live credentials in `session.json` or `variables.md`.

---

## Legal & Ethical Use

This software is intended for **authorised security testing**, **education**, and **system administration** on systems you own or have explicit written permission to assess. Misuse is solely your responsibility.

---

## License

MIT © [51LV3RC4T](https://github.com/51LV3RC4T)

---

Built with purpose by **[51LV3RC4T](https://github.com/51LV3RC4T)**

*Know your commands before you run them.*
