<div align="center">

```
                          ...::...                      ..:::.
                      :++++++++++++++=:.         ..-++++++++++++++:
                      -+:          .:-=+=:     :=++-:.          :+:
                    .-++:              .-++:.:++-.              :++-..
                 :+++==+:                .=+++=.                :+==+++.
                 -+-  -+:            ..    -+-    ..            :+-  -+-
                 -+-  -+:            .*#=  :-:  -##:            :+-  -+:
                 -+-  -+:             +###%%%%####*.            :+-  -+:
                 -+-  -+:            .*############.            :+-  -+-
                 -+-  -+:            -#############+.           :+-  -+:
                 -+-  -+:            =#############+.           :+-  -+:
                 -+-  -+:            -#############=.           :+-  -+:
                 -+-  -+:             =###########*.            :+-  -+:
                 -+-  -+:            .*###########*.            :+-  -+:
                 -+-  -+:            =#############+.           :+-  -+:
                 -+-  -+:           :###############-           :+-  -+:
                 -+-  -+-:-======-:.*################ :-======-:-+-  -+:
                 -+-  .=++=-::::-=:*#################*:=-::::-=++=.  -+:
                 -+-           . :*###################*:..           -+:
                 -+-     :-=+++:*#######################+:+++=-:.    -+:
                 -+=:=++++=:. .*#########################*. .-=++++=:-+:
                 :++=-:.      -###########################=      .::=++.
                              =###########################=
                              -###########################-
                              .*########################%#.
                               :########################%-
                                .#######################-
                                 .+###################*:
                                   .=###############*:
                                 :-=+=-::--==+#####:
                               =####%#############.
                              :*##-  .=*#######+:
                                .         ...

   ██████╗███╗   ███╗██████╗ ██████╗ ███████╗███████╗
  ██╔════╝████╗ ████║██╔══██╗██╔══██╗██╔════╝██╔════╝
  ██║     ██╔████╔██║██║  ██║██████╔╝█████╗  █████╗
  ██║     ██║╚██╔╝██║██║  ██║██╔══██╗██╔══╝  ██╔══╝
  ╚██████╗██║ ╚═╝ ██║██████╔╝██║  ██║███████╗██║
   ╚═════╝╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝
  ────────────────────────────────────────────────────────
  Command Referencer                    [ 51LV3RC4T ]
  ────────────────────────────────────────────────────────
```

**Stop retyping commands. Stop forgetting flags. Start moving faster.**

`cmdref` is a terminal tool for security practitioners that stores your
favourite commands as markdown templates and lets you search, build, and
copy them with a single line — parameters filled in, clipboard ready.

[![Python](https://img.shields.io/badge/python-3.7%2B-blue?style=flat-square&logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20WSL-lightgrey?style=flat-square)]()
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)]()
[![Zero deps](https://img.shields.io/badge/dependencies-zero-brightgreen?style=flat-square)]()

</div>

---

## Table of Contents

- [Why cmdref?](#why-cmdref)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Flag Reference](#flag-reference)
- [Builder Mode](#builder-mode)
- [Database Format](#database-format)
  - [Workflow Template](#workflow-template)
  - [Variable Reference](#variable-reference)
- [Writing Your Own Commands](#writing-your-own-commands)
- [Verbose Modes](#verbose-modes)
- [Windows Commands](#windows-commands)
- [Searching Custom Files](#searching-custom-files)
- [Sourcing Workflows](#sourcing-workflows)
- [Updating the Database](#updating-the-database)
- [Directory Structure](#directory-structure)
- [Security Notes](#security-notes)
- [Contributing](#contributing)
- [License](#license)

---

## Why cmdref?

During a pentest or CTF you spend a surprising amount of time looking up
the exact flags for a tool you use every week, filling in an IP address you
already have open in another window, or hunting through your notes for that
one `hydra` invocation that actually worked.

`cmdref` solves all three:

- **Search** your personal command library by keyword, description, or parameter.
- **Build** — it asks you for each variable value and substitutes them into the command automatically.
- **Copy** the final command straight to your clipboard, ready to paste.

No browser, no context-switch, no retyping.

---

## Features

| Feature | Detail |
|---|---|
| **Fuzzy-style search** | Search by keyword across commands, descriptions, and tags simultaneously |
| **Description filter** | Narrow results by matching words in the description field (`-d`) |
| **Parameter filter** | Filter by the parameter variables a command uses (`-p`) |
| **Builder mode** | Interactively fill in `{{variables}}` with real values before copying |
| **Clipboard** | Copies the finished command with one flag; works on X11, Wayland, macOS, and WSL |
| **OS filter** | Switch between Linux (`-ol`, default) and Windows (`-ow`) command sets |
| **Verbose modes** | `-v` shows descriptions; `-vv` shows the entire raw command block |
| **Workflow import** | Add your own `.md` files with `-s` / `-sf` |
| **Live DB update** | Pull the latest community database from GitHub with `-udb` |
| **Zero dependencies** | Pure Python 3 standard library — nothing to `pip install` |
| **No-colour mode** | Respects `NO_COLOR` env var and non-TTY pipes automatically |

---

## Requirements

| Requirement | Version / Notes |
|---|---|
| Python | 3.7 or newer |
| git | Only needed for `cmdref -udb` (DB update) |
| Clipboard tool | `xclip` **or** `xsel` **or** `wl-copy` (Linux), `pbcopy` (macOS), built-in (WSL) |

Install a clipboard backend on Kali / Debian:

```bash
sudo apt install xclip
```

---

## Installation

### One-step install

```bash
git clone https://github.com/51LV3RC4T/cmdref.git
cd cmdref
sudo python3 install.py
```

The installer will:

1. Create `/etc/cmdref/db` and `/etc/cmdref/workflow`
2. Copy the bundled DB files into `/etc/cmdref/db`
3. Install `cmdref` to `/usr/local/bin/cmdref` (executable)

After installation, pull the full community database:

```bash
cmdref -udb
```

### Uninstall

```bash
sudo python3 install.py --uninstall
```

This removes `/usr/local/bin/cmdref` and the entire `/etc/cmdref/` directory.

---

## Quick Start

```bash
# Show help and the full flag list
cmdref -h

# Search for nmap commands
cmdref nmap

# Search with a description filter — "aggressive scan"
cmdref nmap -d aggressive scan

# Build a command: fill in variables interactively, then copy
cmdref nmap -c -b

# Filter by which parameter a command uses
cmdref hydra -p cmd_ref_param_file_pass

# List Windows-only commands
cmdref -ow

# Full workflow: search → select → build → copy
cmdref nmap -d aggressive -c -b
```

**Example session:**

```
kali@kali:~$ cmdref nmap -d aggressive -c -b

  Possible Commands : (2 found)

  0.  nmap -A {{cmd_ref_target}} -oN {{cmd_ref_param_file}}
       ↳  Aggressive Nmap scan — OS, version, scripts, traceroute

  1.  nmap -A {{cmd_ref_target}} -oN {{cmd_ref_param_file}} -T4
       ↳  Aggressive Nmap with T4 timing (faster, noisier)

  Select command to build : 0

  Specify parameter values :

  Target's IP [10.10.10.10] : 192.168.1.50
  Input file                : scan-output

  → nmap -A 192.168.1.50 -oN scan-output
  Command copied to clipboard ! :)

kali@kali:~$
```

---

## Flag Reference

| Flag | Argument | Description |
|---|---|---|
| `-h` | — | Display the help menu |
| `-V` | — | Print the version and exit |
| `-s` | `<file>` | Copy a workflow `.md` file into `/etc/cmdref/workflow` |
| `-sf` | `<folder>` | Copy an entire workflow folder into `/etc/cmdref/workflow` |
| `-f` | `<path>` | Search only in the specified file or directory |
| `-w` | — | Search inside `/etc/cmdref/workflow` |
| `-ol` | — | Show Linux commands only **[default]** |
| `-ow` | — | Show Windows commands only |
| `-d` | `<terms…>` | Match terms against the Description field |
| `-p` | `<terms…>` | Match terms against the Parameters field |
| `-v` | — | Verbose — show description under each result |
| `-vv` | — | Super-verbose — show the full raw command block |
| `-c` | — | Copy the selected/built command to clipboard |
| `-b` | — | Builder — interactively fill in `{{variables}}` |
| `-udb` | — | Update DB — pull the latest `/db` from GitHub |

**Combining flags** — all filters are ANDed together, so you can stack as many as you need:

```bash
cmdref nmap -d aggressive -p cmd_ref_target -v -c -b
```

---

## Builder Mode

When you add `-b`, cmdref enters Builder mode after you select a command.
It asks for a value for each `{{variable}}` in that command.

- If a variable has a **default value**, press **Enter** to accept it.
- If a variable has **no default**, you must provide one — leaving it blank
  shows the "Silver kitty is confused" message and the example command instead.

```bash
cmdref hydra -c -b
```

```
  Specify parameter values :

  Input users file  : users.txt
  Input Passwords file [rockyou.txt] :   ← pressed Enter, used default
  Target's IP [10.10.10.10] : 10.0.0.5

  → hydra -L users.txt -P rockyou.txt ssh://10.0.0.5
  Command copied to clipboard ! :)
```

---

## Database Format

cmdref parses markdown files. Each file can contain multiple command entries,
separated by `---` (three or more dashes on their own line).

### Workflow Template

```markdown
---

Description :
    One-line summary of what this command does.

Parameters : #cmd_ref_target #cmd_ref_param_file

```cmd
tool-name {{cmd_ref_target}} -o {{cmd_ref_param_file}}
```

```example
tool-name 10.10.10.10 -o output.txt
```

Tags : #tool-name #category #linux

---
```

**Block anatomy:**

| Field | Required | Purpose |
|---|---|---|
| `Description :` | Recommended | Human-readable summary; searched with `-d` |
| `Parameters :` | Optional | Space-separated `#variable_name` tags; searched with `-p` |
| ` ```cmd ` | **Required** | The command template with `{{variable}}` placeholders |
| ` ```example ` | Recommended | Concrete example shown when Builder has no value |
| `Tags :` | Recommended | `#tag` words for search; must include `#linux` or `#windows` |

> **Important:** Every block must contain a ` ```cmd ` section or it is silently
> skipped. Include either `#linux` or `#windows` in the Tags line — commands
> with neither default to Linux.

---

### Variable Reference

These are the built-in variables recognised by the Builder.
Use `{{variable_name}}` inside your `cmd` blocks.

| Variable | Display Name | Default Value | Accepted Format |
|---|---|---|---|
| `{{cmd_ref_target}}` | Target's IP | `10.10.10.10` | `1.1.1.1` or `1.1.1.1/24` |
| `{{cmd_ref_attacker}}` | Attacker's IP | `127.0.0.1` | `1.1.1.1` |
| `{{cmd_ref_target_port}}` | Target PORT | `51` | integer |
| `{{cmd_ref_attacker_port}}` | Attacker PORT | `9999` | integer |
| `{{cmd_ref_domain}}` | Domain | `silver.cat` | `domain.tld` |
| `{{cmd_ref_url}}` | URL | `http://silver.cat` | `http://…` or `https://…` |
| `{{cmd_ref_protocol}}` | Protocol | _(none)_ | `smb`, `rdp`, etc. |
| `{{cmd_ref_param_file}}` | Input file | _(none)_ | file path |
| `{{cmd_ref_param_file_users}}` | Input users file | _(none)_ | file path |
| `{{cmd_ref_param_file_pass}}` | Input Passwords file | _(none)_ | file path |
| `{{cmd_Ref_target_hash}}` | NTLM Hash | _(none)_ | NTLM hash string |

You can use any `{{custom_name}}` placeholder you like — the Builder will
prompt for it by its raw variable name if it is not in the registry above.

---

## Writing Your Own Commands

1. Create a new `.md` file anywhere on your system (e.g. `~/notes/web.md`).
2. Write your entries using the template above.
3. Either:
   - **Search it directly** with `-f`:
     ```bash
     cmdref burp -f ~/notes/web.md
     ```
   - **Import it** into the local store with `-s`:
     ```bash
     cmdref -s ~/notes/web.md
     # then search with -w
     cmdref burp -w
     ```

---

## Verbose Modes

```bash
# Show description under each command
cmdref nmap -v

# Show the full raw markdown block (useful for debugging your DB files)
cmdref nmap -vv
```

---

## Windows Commands

Tag your commands with `#windows` instead of `#linux` to add them to the
Windows set. Use `-ow` to display them:

```bash
cmdref -ow
cmdref mimikatz -ow -v
cmdref -ow -d dump credentials -c -b
```

Commands tagged with **both** `#linux` and `#windows` appear in either view.

---

## Searching Custom Files

You don't need to import a file to search it. Point cmdref at any `.md`
file or directory with `-f`:

```bash
# Single file
cmdref nmap -f ~/pentest-notes/nmap.md

# Entire folder (searches all .md files recursively)
cmdref smb -f ~/pentest-notes/

# Combine with other flags
cmdref nmap -f ~/pentest-notes/ -d aggressive -c -b
```

---

## Sourcing Workflows

Import a workflow file (or a whole folder) into `/etc/cmdref/workflow` so
it becomes part of the permanent workflow library (searched with `-w`).

```bash
# Import a single file
cmdref -s ~/my-workflow.md

# Import an entire folder
cmdref -sf ~/my-workflows/

# Then search your workflow library
cmdref nmap -w
```

If the destination already exists, cmdref will ask before overwriting.

---

## Updating the Database

```bash
cmdref -udb
```

This shallow-clones `https://github.com/51LV3RC4T/cmdref`, copies the `/db`
directory to `/etc/cmdref/db`, and removes the temporary clone.

If you don't have write permission to `/etc/cmdref/db`, run with `sudo`:

```bash
sudo cmdref -udb
```

---

## Directory Structure

```
/etc/cmdref/
├── db/                    ← community command database (managed by -udb)
│   └── *.md
└── workflow/              ← your personal imported workflows (managed by -s / -sf)
    └── *.md

Repository layout:
cmdref/
├── cmdref.py              ← main tool (installed to /usr/local/bin/cmdref)
├── install.py             ← installer / uninstaller
├── requirements.txt       ← no external dependencies
├── db/
│   └── network_recon.md   ← bundled starter database
└── README.md
```

---

## Security Notes

The following mitigations are implemented in the codebase:

| Vector | Mitigation |
|---|---|
| **Symlink traversal** | `rglob` skips all symbolic links when collecting `.md` files |
| **File-size DoS** | Files larger than 5 MB are skipped with a warning |
| **Temp-dir race (TOCTOU)** | `tempfile.mkdtemp()` is used for git clone temp dirs instead of a fixed `/tmp/` path |
| **Subprocess injection** | All subprocess calls use list arguments — no `shell=True` anywhere |
| **Git URL injection** | The repo URL is validated against a strict `https?://[safe-chars]` regex before being passed to git |
| **ANSI in clipboard** | Escape codes are stripped from text before clipboard copy |
| **Multi-encoding** | Files are tried as UTF-8 → UTF-8-BOM → Latin-1 so malformed encoding never crashes the parser |
| **No-colour pipe support** | Colours are disabled automatically when stdout is not a TTY or `NO_COLOR` is set |
| **Clean Ctrl-C** | `KeyboardInterrupt` is caught at the top level — no tracebacks, exit code 0 |

---

## Contributing

Contributions are welcome — new DB entries, bug fixes, and feature ideas alike.

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-commands`
3. Add or edit files in `db/` following the [Workflow Template](#workflow-template).
4. Open a pull request with a clear description of what you added.

**DB contribution checklist:**

- [ ] Every entry is between `---` separators
- [ ] Every `cmd` block uses `{{variable_name}}` for substitutable values
- [ ] Every entry has an `example` block showing the default values
- [ ] Tags include `#linux` and/or `#windows`
- [ ] Tested locally with `cmdref -f db/your-file.md`

---

## License

```
MIT License

Copyright (c) 2024 51LV3RC4T

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

Made with ❤️ by **51LV3RC4T**

*Automate. Reference. Execute.*

</div>
