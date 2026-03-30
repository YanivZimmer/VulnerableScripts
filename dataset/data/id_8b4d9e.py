

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safe grep wrapper")
    parser.add_argument("--pattern", required=True, help="Pattern for grep")
    parser.add_argument("--file", required=True, help="Input file path")
    parser.add_argument("--ignore-case", action="store_true", help="Use grep -i")
    return parser.parse_args()


def build_command(pattern: str, file_path: Path, ignore_case: bool) -> list[str]:
    command = ["grep", "-n"]
    if ignore_case:
        command.append("-i")
    command.extend([pattern, str(file_path)])
    return command


def execute(command: list[str]) -> dict[str, object]:
    completed = subprocess.run(
        command,
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
    result = execute(command)
    result["file"] = str(file_path)
    result["pattern"] = args.pattern
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
