#!/usr/bin/env python3
"""
install.py — Installer for cmdref  (v5.5.0 bundle)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Run as root to install the tool system-wide:

    sudo python3 install.py

To uninstall:

    sudo python3 install.py --uninstall

What the installer does
-----------------------
  1.  Creates  /etc/cmdref/db        (command database directory)
  2.  Creates  /etc/cmdref/workflow  (user workflow directory)
  3.  Copies any bundled db/*.md files to /etc/cmdref/db
  4.  Installs cmdref.py as /usr/local/bin/cmdref  (chmod 755)
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────

_HERE        = Path(__file__).parent.resolve()
_DB_DST      = Path("/etc/cmdref/db")
_WF_DST      = Path("/etc/cmdref/workflow")
_BIN_DST     = Path("/usr/local/bin/cmdref")
_SCRIPT_SRC  = _HERE / "cmdref.py"

# ── ANSI helpers (kept minimal; no shared module dependency) ──────────────────

def _ok(msg:  str) -> None: print(f"\033[92m  [✓] {msg}\033[0m")
def _err(msg: str) -> None: print(f"\033[91m  [!] {msg}\033[0m")
def _inf(msg: str) -> None: print(f"\033[96m  [*] {msg}\033[0m")
def _dim(msg: str) -> None: print(f"\033[2m      {msg}\033[0m")

# ── Root check ────────────────────────────────────────────────────────────────

def _require_root() -> None:
    try:
        uid = os.geteuid()
    except AttributeError:
        # Windows — os.geteuid doesn't exist; skip the check.
        return
    if uid != 0:
        _err("Please run as root:  sudo python3 install.py")
        sys.exit(1)

# ── Install ───────────────────────────────────────────────────────────────────

def install() -> None:
    _require_root()

    print("\n\033[96m\033[1m  cmdref — installer\033[0m\n")

    # 1. System directories ────────────────────────────────────────────────────
    for d in (_DB_DST, _WF_DST):
        try:
            d.mkdir(parents=True, exist_ok=True)
            _ok(f"Directory ready : {d}")
        except PermissionError:
            _err(f"Cannot create {d}  —  are you root?")
            sys.exit(1)

    # 2. Bundled DB files ──────────────────────────────────────────────────────
    local_db = _HERE / "db"
    if local_db.is_dir():
        copied = 0
        for md in sorted(local_db.rglob("*.md")):
            rel = md.relative_to(local_db)
            dst = _DB_DST / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(md, dst)
            copied += 1
        _ok(f"Copied {copied} DB file(s) to {_DB_DST}")
    else:
        _inf("No bundled db/ folder found — skipping DB copy.")
        _dim("Run  cmdref -udb  after install to pull the database from GitHub.")

    # 3. Install cmdref command ────────────────────────────────────────────────
    if not _SCRIPT_SRC.exists():
        _err(f"cmdref.py not found at {_SCRIPT_SRC}")
        sys.exit(1)

    shutil.copy2(_SCRIPT_SRC, _BIN_DST)
    _BIN_DST.chmod(0o755)
    _ok(f"Installed:  {_BIN_DST}")

    # 4. Sanity-check the Python 3 interpreter ─────────────────────────────────
    py3 = shutil.which("python3")
    if py3:
        _ok(f"python3 found at {py3}")
    else:
        _err("python3 not found in PATH — the shebang line may not work.")

    print()
    _ok("Installation complete!  Run  cmdref -h  to get started.\n")


# ── Uninstall ─────────────────────────────────────────────────────────────────

def uninstall() -> None:
    _require_root()

    print("\n\033[96m\033[1m  cmdref — uninstaller\033[0m\n")

    removed = False
    for target in (_BIN_DST, Path("/etc/cmdref")):
        if not target.exists():
            continue
        try:
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
            _ok(f"Removed {target}")
            removed = True
        except PermissionError:
            _err(f"Cannot remove {target}  —  are you root?")

    if removed:
        print()
        _ok("Uninstall complete.\n")
    else:
        print("  Nothing to remove.\n")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--uninstall" in sys.argv:
        uninstall()
    else:
        install()
