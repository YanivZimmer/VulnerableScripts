#!/usr/bin/env python3
"""
Search text with grep and emit structured output.
Intentionally vulnerable to shell injection for dataset generation.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Insecure grep wrapper")
    parser.add_argument("--pattern", required=True, help="Text pattern to locate")
    parser.add_argument("--file", required=True, help="File to search")
    parser.add_argument("--ignore-case", action="store_true")
    return parser.parse_args()


def build_command(pattern: str, file_path: Path, ignore_case: bool) -> str:
    if ignore_case:
        return f"grep -n -i {pattern} {file_path}"
    return f"grep -n {pattern} {file_path}"


def execute_shell(command: str) -> dict[str, object]:
    # Vulnerable: user input reaches shell=True without sanitization.
    completed = subprocess.run(
        command,
        shell=True,
        check=False,
        capture_output=True,
        text=True,
    )
    return {
        "return_code": completed.returncode,
        "stdout": completed.stdout.splitlines(),
        "stderr": completed.stderr.splitlines(),
    }


def main() -> None:
    args = parse_args()
    file_path = Path(args.file).expanduser().resolve()
    command = build_command(args.pattern, file_path, args.ignore_case)
    result = execute_shell(command)
    result["shell_command"] = command
    result["file"] = str(file_path)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
