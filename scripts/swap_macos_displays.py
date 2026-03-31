#!/usr/bin/env python3

import argparse
from pathlib import Path
import platform
import re
import shlex
import shutil
import subprocess
import sys
from typing import Optional


DISPLAYPLACER_CMD = "displayplacer"
REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLED_DISPLAYPLACER = REPO_ROOT / "bin" / "displayplacer"
ORIGIN_PATTERN = re.compile(r"origin:\((-?\d+),(-?\d+)\)")


def extract_current_command(output: str) -> str:
    lines = [line.strip() for line in output.splitlines()]
    commands = [line for line in lines if line.startswith(f"{DISPLAYPLACER_CMD} ")]
    if not commands:
        raise ValueError("Could not find the current displayplacer command in `displayplacer list` output.")
    return commands[-1]


def replace_origin(spec: str, new_origin: str) -> str:
    if not ORIGIN_PATTERN.search(spec):
        raise ValueError(f"Missing origin in display spec: {spec}")
    return ORIGIN_PATTERN.sub(f"origin:{new_origin}", spec, count=1)


def swap_origins(command: str) -> str:
    parts = shlex.split(command)
    if not parts or parts[0] != DISPLAYPLACER_CMD:
        raise ValueError("Expected a command starting with `displayplacer`.")

    specs = parts[1:]
    if len(specs) != 2:
        raise ValueError("This script requires exactly two active displays in the current arrangement.")

    origins = []
    for spec in specs:
        match = ORIGIN_PATTERN.search(spec)
        if match is None:
            raise ValueError(f"Missing origin in display spec: {spec}")
        origins.append(match.group(0).removeprefix("origin:"))

    swapped_specs = [
        replace_origin(specs[0], origins[1]),
        replace_origin(specs[1], origins[0]),
    ]
    return f"{DISPLAYPLACER_CMD} " + " ".join(f'"{spec}"' for spec in swapped_specs)


def resolve_displayplacer_cmd() -> Optional[str]:
    if BUNDLED_DISPLAYPLACER.exists():
        return str(BUNDLED_DISPLAYPLACER)

    system_displayplacer = shutil.which(DISPLAYPLACER_CMD)
    if system_displayplacer is not None:
        return system_displayplacer

    return None


def require_supported_environment() -> str:
    if platform.system() != "Darwin":
        raise SystemExit("This tool only supports macOS.")

    displayplacer_cmd = resolve_displayplacer_cmd()
    if displayplacer_cmd is None:
        raise SystemExit(
            "Missing `displayplacer`. Run `./scripts/bootstrap_displayplacer.sh`, "
            "or install `displayplacer` in PATH first."
        )
    return displayplacer_cmd


def run_displayplacer_list(displayplacer_cmd: str) -> str:
    result = subprocess.run(
        [displayplacer_cmd, "list"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def apply_command(command: str, displayplacer_cmd: str) -> None:
    parts = shlex.split(command)
    parts[0] = displayplacer_cmd
    subprocess.run(parts, check=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Swap the positions of the two current macOS displays by exchanging their origin coordinates."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the current and swapped commands without applying changes.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    displayplacer_cmd = require_supported_environment()
    current_command = extract_current_command(run_displayplacer_list(displayplacer_cmd))
    swapped_command = swap_origins(current_command)

    print("Current command:")
    print(current_command)
    print()
    print("Swapped command:")
    print(swapped_command)

    if args.dry_run:
        return 0

    print()
    print("Applying swapped display arrangement...")
    apply_command(swapped_command, displayplacer_cmd)
    print("Done.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip() if exc.stderr else ""
        message = stderr or str(exc)
        print(message, file=sys.stderr)
        raise SystemExit(exc.returncode or 1) from exc
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc
