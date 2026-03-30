
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safe directory lister")
    parser.add_argument("--target", default=".", help="Directory to list")
    parser.add_argument("--all", action="store_true", help="Include hidden files")
    return parser.parse_args()


def build_command(target: Path, include_hidden: bool) -> list[str]:
    command = ["ls", "-1"]
    if include_hidden:
        command.append("-a")
    command.append(str(target))
    return command


def run_listing(command: list[str]) -> tuple[int, list[str]]:
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    rows = [line for line in completed.stdout.splitlines() if line.strip()]
    return completed.returncode, rows


def main() -> None:
    args = parse_args()
    target = Path(args.target).expanduser().resolve()
    command = build_command(target, args.all)
    code, rows = run_listing(command)
    payload = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "target": str(target),
        "return_code": code,
        "entries": rows,
        "entry_count": len(rows),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
