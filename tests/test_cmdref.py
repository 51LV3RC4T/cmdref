"""
Edge-case and regression tests for cmdref.
Run from repository root:  python -m unittest tests.test_cmdref -v
"""

from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent


def _load_module():
    spec = importlib.util.spec_from_file_location("cmdref", _ROOT / "cmdref.py")
    mod = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("cannot load cmdref")
    spec.loader.exec_module(mod)
    return mod


cmdref = _load_module()


class TestProfilePaths(unittest.TestCase):
    def test_normalize_empty_list_stays_empty(self) -> None:
        self.assertEqual(cmdref._normalize_profile_paths([]), [])

    def test_normalize_non_list_defaults_system_db(self) -> None:
        self.assertEqual(cmdref._normalize_profile_paths(None), [cmdref.SYSTEM_DB])
        self.assertEqual(cmdref._normalize_profile_paths("nope"), [cmdref.SYSTEM_DB])

    def test_normalize_filters_null_and_coerces(self) -> None:
        raw = ["/tmp/ok", "\x00bad", "", "  /home/x  ", 123, "valid/path"]
        out = cmdref._normalize_profile_paths(raw)
        self.assertTrue(any(p.endswith("ok") and "tmp" in p.replace("\\", "/") for p in out))
        self.assertTrue(any("valid" in p and "path" in p for p in out))
        self.assertTrue(all(isinstance(p, str) for p in out))

    def test_profile_name_rejects_traversal(self) -> None:
        self.assertFalse(cmdref._is_valid_profile_name("../etc"))
        self.assertFalse(cmdref._is_valid_profile_name(""))
        self.assertTrue(cmdref._is_valid_profile_name("web-1"))


class TestParser(unittest.TestCase):
    def test_team_sync_flags(self) -> None:
        a = cmdref.parse_args(
            [
                "-ts",
                "https://github.com/org/repo.git",
                "-td",
                "-tb",
                "main",
                "-tp",
                "db/team-db",
            ]
        )
        self.assertEqual(a.team_sync, "https://github.com/org/repo.git")
        self.assertTrue(a.team_dry_run)
        self.assertEqual(a.team_branch, "main")
        self.assertEqual(a.team_subpath, "db/team-db")

    def test_parse_minimal_block(self) -> None:
        block = """
Description :
     Test desc

Parameters : #target-ip

```cmd
ping {{target-ip}}
```

```example
ping 1.1.1.1
```

Tags :  #linux #test

"""
        e = cmdref._parse_block(block, "x.md")
        self.assertIsNotNone(e)
        assert e is not None
        self.assertIn("target-ip", e.arguments)
        self.assertIn("{{target-ip}}", e.command)
        self.assertEqual(e.os_type, "linux")

    def test_parse_skips_without_cmd_fence(self) -> None:
        self.assertIsNone(cmdref._parse_block("Description:\nfoo\n", "x.md"))

    def test_parse_file_splits_on_separator(self) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(
                """
Description :
     A

Parameters :

```cmd
echo a
```

```example
echo a
```

Tags :  #linux

---

Description :
     B

Parameters :

```cmd
echo b
```

```example
echo b
```

Tags :  #linux

"""
            )
            path = f.name
        try:
            entries = cmdref.parse_file(path)
            self.assertEqual(len(entries), 2)
            self.assertEqual(entries[0].command.strip(), "echo a")
            self.assertEqual(entries[1].command.strip(), "echo b")
        finally:
            Path(path).unlink(missing_ok=True)


class TestSearch(unittest.TestCase):
    def test_empty_query_returns_matches(self) -> None:
        e = cmdref.Entry(
            command="nmap {{target-ip}}",
            description="scan",
            tags=["linux"],
        )
        r = cmdref.search([e], [], [], [], "linux")
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].score, 100.0)

    def test_windows_filter(self) -> None:
        e = cmdref.Entry(command="cmd", tags=["windows"], os_type="windows")
        r = cmdref.search([e], ["cmd"], [], [], "linux")
        self.assertEqual(len(r), 0)
        r2 = cmdref.search([e], ["cmd"], [], [], "windows")
        self.assertEqual(len(r2), 1)


class TestEntryFromDict(unittest.TestCase):
    def test_coerces_bad_types(self) -> None:
        d = {
            "command": "x",
            "description": 123,
            "arguments": ["a", 2],
            "tags": "notalist",
            "os_type": "linux",
        }
        e = cmdref.Entry.from_dict(d)
        self.assertEqual(e.description, "123")
        self.assertEqual(e.arguments, ["a", "2"])
        self.assertEqual(e.tags, [])


class TestEnvDefaults(unittest.TestCase):
    def test_env_overrides_registry(self) -> None:
        cmdref._SESSION.clear()
        old = os.environ.pop("CMDREF_TARGET_IP", None)
        try:
            os.environ["CMDREF_TARGET_IP"] = "192.0.2.1"
            self.assertEqual(cmdref._effective_default("target-ip"), "192.0.2.1")
        finally:
            if old is not None:
                os.environ["CMDREF_TARGET_IP"] = old
            else:
                os.environ.pop("CMDREF_TARGET_IP", None)

    def test_session_beats_env(self) -> None:
        cmdref._SESSION.clear()
        old = os.environ.pop("CMDREF_TARGET_IP", None)
        try:
            os.environ["CMDREF_TARGET_IP"] = "192.0.2.1"
            cmdref._SESSION["target-ip"] = "10.0.0.1"
            self.assertEqual(cmdref._effective_default("target-ip"), "10.0.0.1")
        finally:
            cmdref._SESSION.pop("target-ip", None)
            if old is not None:
                os.environ["CMDREF_TARGET_IP"] = old
            else:
                os.environ.pop("CMDREF_TARGET_IP", None)


class TestPentestEnvAliases(unittest.TestCase):
    def tearDown(self) -> None:
        cmdref._SESSION.clear()
        for k in (
            "RHOST",
            "LHOST",
            "RPORT",
            "CMDREF_TARGET_IP",
            "CMDREF_ATTACKER_IP",
        ):
            os.environ.pop(k, None)

    def test_rhost_maps_to_target_ip(self) -> None:
        os.environ["RHOST"] = "192.0.2.99"
        val, src = cmdref._resolve_var_components("target-ip")
        self.assertEqual(val, "192.0.2.99")
        self.assertEqual(src, "RHOST")

    def test_cmdref_beats_rhost(self) -> None:
        os.environ["RHOST"] = "192.0.2.99"
        os.environ["CMDREF_TARGET_IP"] = "10.10.10.10"
        val, src = cmdref._resolve_var_components("target-ip")
        self.assertEqual(val, "10.10.10.10")
        self.assertEqual(src, "CMDREF_TARGET_IP")

    def test_lhost_maps_to_attacker_ip(self) -> None:
        cmdref._SESSION.pop("attacker-ip", None)
        os.environ["LHOST"] = "10.11.12.13"
        val, src = cmdref._resolve_var_components("attacker-ip")
        self.assertEqual(val, "10.11.12.13")
        self.assertEqual(src, "LHOST")


if __name__ == "__main__":
    unittest.main()
