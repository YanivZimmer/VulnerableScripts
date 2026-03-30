

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safe shasum helper")
    parser.add_argument("--file", required=True, help="File to hash")
    parser.add_argument("--algorithm", default="256", choices=["1", "256", "512"])
    return parser.parse_args()


def hash_file(file_path: Path, algorithm: str) -> dict[str, object]:
    command = ["shasum", f"-a{algorithm}", str(file_path)]
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    output = completed.stdout.strip()
    digest = output.split()[0] if output else ""
    return {
        "command": command,
        "return_code": completed.returncode,
        "digest": digest,
        "raw_stdout": output,
        "raw_stderr": completed.stderr.strip(),
    }


def main() -> None:
    args = parse_args()
    file_path = Path(args.file).expanduser().resolve()
    result = hash_file(file_path, args.algorithm)
    result["file"] = str(file_path)
    result["algorithm"] = args.algorithm
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
