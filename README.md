<div align="center">

```
   ██████╗███╗   ███╗██████╗ ██████╗ ███████╗███████╗
  ██╔════╝████╗ ████║██╔══██╗██╔══██╗██╔════╝██╔════╝
  ██║     ██╔████╔██║██║  ██║██████╔╝█████╗  █████╗
  ██║     ██║╚██╔╝██║██║  ██║██╔══██╗██╔══╝  ██╔══╝
  ╚██████╗██║ ╚═╝ ██║██████╔╝██║  ██║███████╗██║
   ╚═════╝╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝
  ──────────────────────────────────────────────────────
  Command Referencer                    [ 51LV3RC4T ]
  ──────────────────────────────────────────────────────
```

**A terminal tool that keeps every command you need — one search away.**

</div>

---

## What is cmdref?

`cmdref` is a command-line tool built for anyone who works with a lot of terminal commands — penetration testers, sysadmins, CTF players, or developers — and wants a faster way to find, build, and use them.

You store your commands in plain markdown files using a simple template. `cmdref` parses them, lets you search by keyword or description, fills in `{{variables}}` interactively, and copies the final command straight to your clipboard.

**No browser. No context-switch. No retyping the same IP for the tenth time.**

```
cmdref nmap -d aggressive -c -b
```

```
  Possible Commands :  (2 found)

  0.  nmap -A {{cmd_ref_target}} -oN {{cmd_ref_param_file}}
       ↳  Aggressive Nmap scan — OS, version, scripts, traceroute

  1.  nmap -A {{cmd_ref_target}} -oN {{cmd_ref_param_file}} -T4
       ↳  Aggressive Nmap with T4 timing (faster, noisier)

  Select command to build : 0

  Specify parameter values :

  Target's IP  [10.10.10.10] : 192.168.1.50
  Input file                 : initial-scan

  → nmap -A 192.168.1.50 -oN initial-scan
  Command copied to clipboard ! :)
```

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Flag Reference](#flag-reference)
- [Usage Guide](#usage-guide)
  - [Basic Search](#basic-search)
  - [Refining Results](#refining-results)
  - [Builder Mode](#builder-mode)
  - [Clipboard Copy](#clipboard-copy)
  - [Verbose Modes](#verbose-modes)
  - [Windows Commands](#windows-commands)
  - [Searching Custom Files](#searching-custom-files)
- [Workflows](#workflows)
  - [What is a Workflow?](#what-is-a-workflow)
  - [Writing Your Own Commands](#writing-your-own-commands)
  - [The Command Template](#the-command-template)
  - [Variables Reference](#variables-reference)
  - [Sourcing a Workflow](#sourcing-a-workflow)
- [Updating the Database](#updating-the-database)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Features

| | Feature | Description |
|---|---|---|
| 🔍 | **Keyword Search** | Search across command text, descriptions, and tags at once |
| 📝 | **Description Filter** | Narrow results by matching words in the description (`-d`) |
| 🔧 | **Parameter Filter** | Filter by which variables a command uses (`-p`) |
| 🛠️ | **Builder Mode** | Fill in `{{variables}}` interactively before running (`-b`) |
| 📋 | **Clipboard Copy** | Copy the finished command in one step — paste-ready (`-c`) |
| 🪟 | **OS Switching** | Toggle between Linux (default) and Windows command sets |
| 📂 | **Custom Sources** | Search any `.md` file or folder, anywhere (`-f`) |
| 📦 | **Workflow Import** | Add your personal command files to the local store (`-s`, `-sf`) |
| 🔄 | **Live DB Update** | Pull the latest community database from GitHub (`-udb`) |
| 🟢 | **Zero Dependencies** | Pure Python 3 standard library — nothing to `pip install` |

---

## Requirements

- **Python 3.7+** — pre-installed on most Linux distributions
- **git** — only required for `cmdref -udb` (database update)
- **A clipboard tool** — for the `-c` (copy) feature:

| Platform | Install |
|---|---|
| Linux (X11) | `sudo apt install xclip` |
| Linux (X11) | `sudo apt install xsel` |
| Linux (Wayland) | `sudo apt install wl-clipboard` |
| macOS | `pbcopy` is built-in — nothing to install |
| WSL / Windows | `clip.exe` is built-in — nothing to install |

---

## Installation

**Clone and install in three commands:**

```bash
git clone https://github.com/51LV3RC4T/cmdref.git
cd cmdref
sudo python3 install.py
```

The installer:
1. Creates `/etc/cmdref/db` and `/etc/cmdref/workflow`
2. Copies any bundled DB files into `/etc/cmdref/db`
3. Installs `cmdref` to `/usr/local/bin/cmdref` and makes it executable

**Then pull the full command database:**

```bash
cmdref -udb
```

**To uninstall completely:**

```bash
sudo python3 install.py --uninstall
```

> **No root?** You can still use cmdref without installing — just run `python3 cmdref.py` directly and point at your own files with `-f`.

---

## Quick Start

```bash
# Show the help menu
cmdref -h

# Search for nmap commands
cmdref nmap

# Search with a description keyword
cmdref nmap -d aggressive

# Build a command interactively, then copy it
cmdref nmap -c -b

# Search a specific file instead of the default database
cmdref nmap -f ~/my-notes/nmap.md
```

---

## Flag Reference

```
cmdref <search terms> [flags]
```

| Flag | Argument | Description |
|:---|:---|:---|
| `-h` | — | Show the help menu |
| `-V` | — | Print the version number and exit |
| `-s` | `<file>` | Import a workflow `.md` file into `/etc/cmdref/workflow` |
| `-sf` | `<folder>` | Import an entire workflow folder into `/etc/cmdref/workflow` |
| `-f` | `<path>` | Search only in the specified file or directory |
| `-w` | — | Search inside `/etc/cmdref/workflow` |
| `-ol` | — | Linux commands only — **default when `-ow` is not set** |
| `-ow` | — | Windows commands only |
| `-d` | `<terms…>` | Match words in the Description field |
| `-p` | `<terms…>` | Match words in the Parameters field |
| `-v` | — | Verbose — show description under each result |
| `-vv` | — | Super-verbose — show the complete raw command block |
| `-c` | — | Copy the selected/built command to clipboard |
| `-b` | — | Builder — replace `{{variables}}` with real values interactively |
| `-udb` | — | Update the local DB from the GitHub repository |

> All filters are **AND**ed together. Stack as many as you need:
> ```bash
> cmdref nmap -d full -p cmd_ref_target -v -c -b
> ```

---

## Usage Guide

### Basic Search

Pass any keyword as a search term. cmdref checks command text, descriptions, and tags simultaneously.

```bash
cmdref nmap
cmdref smb
cmdref brute
```

Multiple terms narrow the results further:

```bash
cmdref nmap scan udp
```

---

### Refining Results

**`-d` — search the description field:**

```bash
# Only show nmap entries whose description mentions "aggressive"
cmdref nmap -d aggressive
```

**`-p` — search by parameter variable name:**

```bash
# Only show commands that use a password-file variable
cmdref -p cmd_ref_param_file_pass

# Combine with a keyword
cmdref hydra -p cmd_ref_param_file_users
```

---

### Builder Mode

Add `-b` to fill in each `{{variable}}` interactively after selecting a command.

```bash
cmdref hydra -b
```

```
  Possible Commands :  (2 found)

  0.  hydra -L {{cmd_ref_param_file_users}} -P {{cmd_ref_param_file_pass}} ssh://{{cmd_ref_target}}
  1.  hydra -L {{cmd_ref_param_file_users}} -P {{cmd_ref_param_file_pass}} {{cmd_ref_url}} http-post-form ...

  Select command to build : 0

  Specify parameter values :

  Input users file             : users.txt
  Input Passwords file         : rockyou.txt
  Target's IP  [10.10.10.10]  : 10.0.0.5

  → hydra -L users.txt -P rockyou.txt ssh://10.0.0.5
```

**How variable prompts work:**

- Variables with a **default value** show it in brackets — press `Enter` to accept it.
- Variables with **no default** require input. Leaving them blank shows the example command instead.

---

### Clipboard Copy

Add `-c` to copy the final command to your clipboard automatically.

```bash
# Search, select, build, and copy in one command
cmdref nmap -d aggressive -c -b
```

```
  → nmap -A 192.168.1.50 -oN initial-scan
  Command copied to clipboard ! :)
```

If only one result matches, it is selected automatically — no prompt needed.

---

### Verbose Modes

```bash
# -v  — show the description under each result
cmdref nmap -v
```

```
  0.  nmap -A {{cmd_ref_target}} -oN {{cmd_ref_param_file}}
       ↳  Aggressive Nmap scan — OS, version, scripts, traceroute

  1.  nmap -p- {{cmd_ref_target}} -oN {{cmd_ref_param_file}}
       ↳  Full TCP port scan — all 65535 ports
```

```bash
# -vv — show the full raw command block (useful for debugging your DB files)
cmdref nmap -d full -vv
```

```
  0.  nmap -p- {{cmd_ref_target}} -oN {{cmd_ref_param_file}}
       ↳  Full TCP port scan — all 65535 ports

     ┌─── Full Entry ──────────────────────────────────────
     │ Description :
     │     Full TCP port scan — all 65535 ports
     │
     │ Parameters : #cmd_ref_target #cmd_ref_param_file
     │
     │ ```cmd
     │ nmap -p- {{cmd_ref_target}} -oN {{cmd_ref_param_file}}
     │ ```
     │
     │ Tags : #nmap #scan #full #linux
     └─────────────────────────────────────────────────────
```

---

### Windows Commands

Tag any command with `#windows` instead of `#linux` to put it in the Windows set. Use `-ow` to display Windows commands.

```bash
cmdref -ow
cmdref mimikatz -ow -v
cmdref -ow -d dump -c -b
```

> Commands tagged with **both** `#linux` and `#windows` appear in either view.

---

### Searching Custom Files

You don't need to import a file to search it. Point cmdref at any `.md` file or folder with `-f`:

```bash
# Search a single file
cmdref nmap -f ~/notes/nmap-commands.md

# Search all .md files inside a folder (recursive)
cmdref smb -f ~/notes/

# Combine with any other flags
cmdref nmap -f ~/notes/ -d aggressive -c -b
```

---

## Workflows

### What is a Workflow?

A **workflow** is any `.md` file that follows the cmdref command template. It lives in `/etc/cmdref/workflow/` (your personal store) or anywhere on disk (searched with `-f`).

The idea is simple: keep every tool you use regularly documented in a workflow file — with variables, examples, and tags — so you never have to look it up again.

---

### Writing Your Own Commands

Create a `.md` file anywhere:

```bash
nano ~/my-workflows/web-testing.md
```

Each command entry lives between two `---` separator lines. A minimal entry looks like this:

```markdown
---

Description :
    Run a directory brute-force against a target web server.

Parameters : #cmd_ref_url #cmd_ref_param_file_users #cmd_ref_param_file

```cmd
gobuster dir -u {{cmd_ref_url}} -w {{cmd_ref_param_file_users}} -o {{cmd_ref_param_file}}
```

```example
gobuster dir -u http://10.10.10.10 -w common.txt -o dirs.txt
```

Tags : #gobuster #web #directory #linux

---
```

---

### The Command Template

```markdown
---

Description :
    What does this command do? One clear sentence.

Parameters : #variable_name  #another_variable_name

```cmd
tool-name {{variable_name}} -flag {{another_variable_name}}
```

```example
tool-name default-value -flag default-value
```

Tags : #tool #category #linux

---
```

**Field breakdown:**

| Field | Required | Purpose |
|:---|:---:|:---|
| `Description :` | Recommended | Summary text; searched with `-d` |
| `Parameters :` | Optional | Lists which `#variable_name`s the command uses; searched with `-p` |
| ` ```cmd ` | **Yes** | The command template — this is what cmdref shows and builds |
| ` ```example ` | Recommended | A pre-filled example shown when Builder has no value to give |
| `Tags :` | Recommended | `#keyword` labels for search; include `#linux` or `#windows` |

> A block **must** contain a ` ```cmd ` section or it is silently ignored.
> Blocks with neither `#linux` nor `#windows` default to Linux.

---

### Variables Reference

These are the built-in variables recognised by the Builder. Use `{{variable_name}}` in your `cmd` blocks.

<details>
<summary><strong>Click to expand the full variable table</strong></summary>

| Variable | Prompt Shown | Default |
|:---|:---|:---|
| `{{cmd_ref_target}}` | Target's IP | `10.10.10.10` |
| `{{cmd_ref_attacker}}` | Attacker's IP | `127.0.0.1` |
| `{{cmd_ref_target_port}}` | Target PORT | `51` |
| `{{cmd_ref_attacker_port}}` | Attacker PORT | `9999` |
| `{{cmd_ref_domain}}` | Domain | `silver.cat` |
| `{{cmd_ref_url}}` | URL | `http://silver.cat` |
| `{{cmd_ref_protocol}}` | Protocol | *(none)* |
| `{{cmd_ref_param_file}}` | Input file | *(none)* |
| `{{cmd_ref_param_file_users}}` | Input users file | *(none)* |
| `{{cmd_ref_param_file_pass}}` | Input Passwords file | *(none)* |
| `{{cmd_Ref_target_hash}}` | NTLM Hash | *(none)* |

</details>

You can also use **any custom placeholder** — just write `{{my_custom_var}}` in your command. The Builder will prompt for it by name, with no default.

---

### Sourcing a Workflow

Once you have a workflow file, you have two options:

**Option A — Search it directly (no import needed):**

```bash
cmdref gobuster -f ~/my-workflows/web-testing.md
```

**Option B — Import it into your local store:**

```bash
# Import a single file
cmdref -s ~/my-workflows/web-testing.md

# Import an entire folder at once
cmdref -sf ~/my-workflows/

# Now search your imported workflows with -w
cmdref gobuster -w

# Combine -w with any other flag
cmdref gobuster -w -v -c -b
```

> If the destination already exists, cmdref will ask before overwriting anything.

**Full walkthrough — from file to clipboard:**

```bash
# Step 1 — write your workflow
nano ~/my-workflows/web-testing.md

# Step 2 — test it without importing (fast feedback loop)
cmdref gobuster -f ~/my-workflows/web-testing.md -v

# Step 3 — import it once you're happy
cmdref -s ~/my-workflows/web-testing.md

# Step 4 — use it anywhere
cmdref gobuster -w -c -b
```

---

## Updating the Database

```bash
cmdref -udb
```

This shallow-clones the GitHub repository, replaces `/etc/cmdref/db` with the latest `/db` folder from the repo, and removes the temporary clone.

If you get a permission error:

```bash
sudo cmdref -udb
```

---

## Directory Structure

```
/etc/cmdref/
├── db/                     ← Community database (managed by -udb)
│   └── *.md
└── workflow/               ← Your personal imported workflows (managed by -s / -sf)
    └── *.md

Repository:
cmdref/
├── cmdref.py               ← The tool (installed to /usr/local/bin/cmdref)
├── install.py              ← Installer and uninstaller
├── requirements.txt        ← Zero dependencies; optional clipboard backend notes
├── db/
│   └── network_recon.md    ← Bundled starter database (nmap, hydra, gobuster, CME…)
└── README.md
```

---

## Contributing

Contributions are welcome — whether that's new command entries, bug fixes, or feature ideas.

**To add commands to the database:**

1. Fork the repository
2. Add or edit a file in `db/` following the [Command Template](#the-command-template)
3. Test locally: `cmdref -f db/your-file.md`
4. Open a pull request with a short description

**Quick checklist before submitting:**

- [ ] Each entry is between `---` separators
- [ ] Each `cmd` block uses `{{variable_name}}` for anything a user would change
- [ ] Each entry has an `example` block showing the command with real values
- [ ] Tags include `#linux` and/or `#windows`
- [ ] Tested locally and results look correct

---

## License

MIT © [51LV3RC4T](https://github.com/51LV3RC4T)

```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

<div align="center">

Built with purpose by **[51LV3RC4T](https://github.com/51LV3RC4T)**

*Find it. Build it. Execute.*

</div>
