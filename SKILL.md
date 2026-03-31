---
name: swap-macos-displays
description: Use when Codex needs to swap the positions of exactly two macOS displays on the current machine, especially when the user wants to exchange left/right monitor arrangement without manually dragging displays in System Settings.
---

# Swap macOS Displays

## Overview

Use this skill to swap the current arrangement of two macOS displays with a deterministic local script instead of dragging monitor tiles in System Settings.

This public version is safe to share: it stores no machine-specific display IDs or absolute local paths.

## Quick Start

1. Confirm the machine is macOS and currently has exactly two active displays.
2. Run the repo launcher in dry-run mode first:
   ```bash
   ./swap-displays --dry-run
   ```
3. If the swapped command looks correct, run it for real:
   ```bash
   ./swap-displays
   ```
4. Verify the layout changed by rerunning:
   ```bash
   ./swap-displays --dry-run
   ```
   On scaled displays, macOS may normalize the final logical coordinates after applying the change. Treat the swap as successful when the display that used to own `origin:(0,0)` no longer does.

## Workflow

1. Prefer the repository-local `bin/displayplacer` if present.
2. Otherwise use `displayplacer` from `PATH`.
3. If neither exists, build the vendored source using `scripts/bootstrap_displayplacer.sh`.
4. Read the current arrangement from `displayplacer list`.
5. Extract the last line that starts with `displayplacer `.
6. Require exactly two display specs.
7. Swap only the two `origin:(x,y)` values. Keep the rest unchanged.

## Failure Handling

- If the machine is not macOS, stop immediately.
- If there are not exactly two active displays, stop and explain the limitation.
- If the upstream helper cannot be built, surface the compiler or `make` output directly.
- If `displayplacer list` does not contain a runnable command, stop and show the parsing error instead of guessing.

## Scripts

- `./swap-displays`: best entry point for end users
- `./scripts/bootstrap_displayplacer.sh`: build vendored `displayplacer` into `./bin/displayplacer`
- `./scripts/swap_macos_displays.py`: Python implementation
- `./scripts/test_swap_macos_displays.py`: unit tests
