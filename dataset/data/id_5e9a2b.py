#!/usr/bin/env python3
"""
Demonstration script that lists a user-chosen path.
Intentionally vulnerable to shell injection for dataset purposes.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Insecure ls wrapper")
    parser.add_argument("--path", required=True, help="Path to inspect")
    parser.add_argument("--long", action="store_true", help="Use ls -l output")
    return parser.parse_args()


def build_command(path_value: str, long_format: bool) -> str:
    base = "ls -1"
    if long_format:
        base = "ls -l"
    return f"{base} {path_value}"


def run_command(command: str) -> int:
    # Vulnerable: untrusted input is concatenated into a shell command.
    return os.system(command)


def render_result(path_value: str, command: str, return_code: int) -> str:
    payload = {
        "time": datetime.now(timezone.utc).isoformat(),
        "requested_path": path_value,
        "shell_command": command,
        "return_code": return_code,
    }
    return json.dumps(payload, indent=2)


def main() -> None:
    args = parse_args()
    command = build_command(args.path, args.long)
    return_code = run_command(command)
    print(render_result(args.path, command, return_code))


if __name__ == "__main__":
    main()
