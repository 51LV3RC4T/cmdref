#!/usr/bin/env python3
"""
install.py — Installer for cmdref

Run as root:
    sudo python3 install.py

What it does:
  1. Creates /etc/cmdref/db  and  /etc/cmdref/workflow
  2. Copies any local db/*.md files to /etc/cmdref/db
  3. Installs cmdref.py as  /usr/local/bin/cmdref  (executable)
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
INSTALL_DIR   = Path(__file__).parent.resolve()
DB_DST        = Path("/etc/cmdref/db")
WORKFLOW_DST  = Path("/etc/cmdref/workflow")
BIN_DST       = Path("/usr/local/bin/cmdref")

# ── ANSI helpers ──────────────────────────────────────────────────────────────
def ok(msg):  print(f"\033[92m  [✓] {msg}\033[0m")
def err(msg): print(f"\033[91m  [!] {msg}\033[0m")
def inf(msg): print(f"\033[96m  [*] {msg}\033[0m")


def install():
    inf("Installing cmdref …\n")

    # ── 1. Check we are running as root ───────────────────────────────────────
    if os.geteuid() != 0:
        err("Please run as root:  sudo python3 install.py")
        sys.exit(1)

    # ── 2. Create system directories ──────────────────────────────────────────
    for directory in (DB_DST, WORKFLOW_DST):
        directory.mkdir(parents=True, exist_ok=True)
        ok(f"Directory ready : {directory}")

    # ── 3. Copy bundled DB files ───────────────────────────────────────────────
    local_db = INSTALL_DIR / "db"
    if local_db.is_dir():
        copied = 0
        for md_file in local_db.rglob("*.md"):
            dst = DB_DST / md_file.relative_to(local_db)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(md_file, dst)
            copied += 1
        ok(f"Copied {copied} DB file(s) to {DB_DST}")
    else:
        print(f"  [-] No local db/ folder found — skipping DB copy")
        print(f"      Run  cmdref -udb  after install to download the database.")

    # ── 4. Install cmdref.py → /usr/local/bin/cmdref ──────────────────────────
    src = INSTALL_DIR / "cmdref.py"
    if not src.exists():
        err(f"cmdref.py not found in {INSTALL_DIR}")
        sys.exit(1)

    shutil.copy2(src, BIN_DST)
    BIN_DST.chmod(0o755)
    ok(f"Installed cmdref command to {BIN_DST}")

    # ── 5. Verify Python 3 shebang is reachable ───────────────────────────────
    py3 = shutil.which("python3")
    if py3:
        ok(f"python3 found at {py3}")
    else:
        err("python3 not found in PATH — the shebang line may fail.")

    print()
    ok("Installation complete!")
    print("\n  Try it:  cmdref -h\n")


def uninstall():
    """Remove all installed files (pass --uninstall)."""
    inf("Uninstalling cmdref …\n")

    if os.geteuid() != 0:
        err("Please run as root:  sudo python3 install.py --uninstall")
        sys.exit(1)

    removed = []
    for target in (BIN_DST, Path("/etc/cmdref")):
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
            removed.append(str(target))
            ok(f"Removed {target}")

    if removed:
        ok("Uninstall complete.")
    else:
        print("  Nothing to remove.")
    print()


if __name__ == "__main__":
    if "--uninstall" in sys.argv:
        uninstall()
    else:
        install()
