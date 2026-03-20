
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Insecure find wrapper")
    parser.add_argument("--base-dir", required=True, help="Directory to search")
    parser.add_argument("--extension", required=True, help="Extension like py or txt")
    parser.add_argument("--max-depth", type=int, default=3, help="Find maxdepth")
    return parser.parse_args()


def build_find_command(base_dir: str, extension: str, max_depth: int) -> str:
    quoted_glob = f"*.{extension}"
    return f"find {base_dir} -maxdepth {max_depth} -type f -name {quoted_glob}"


def run_find(command: str) -> dict[str, object]:
    # Vulnerable: command is executed by shell with unsanitized user segments.
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
    command = build_find_command(args.base_dir, args.extension, args.max_depth)
    result = run_find(command)
    result["timestamp"] = datetime.utcnow().isoformat() + "Z"
    result["shell_command"] = command
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
