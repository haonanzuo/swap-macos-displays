# swap-macos-displays

Swap the positions of exactly two macOS displays with one command.

一个面向 macOS 的小工具，同时附带一个可复用的 Codex skill，用来把当前两块屏幕的位置直接对调，不需要手动去系统设置里拖来拖去。

This repository is intentionally sanitized for public sharing:

- No personal display IDs are committed
- No absolute local paths are committed
- No machine-specific prebuilt `displayplacer` binary is committed

## Why this exists / 为什么有这个工具

If you often switch between monitor layouts, manually dragging displays in System Settings is annoying and easy to get wrong.

如果你经常切换显示器摆放方式，系统设置里手动拖屏幕很麻烦，也容易拖错。这个仓库把这件事变成一个可重复执行的本地命令。

## Features / 功能亮点

- Swap exactly two active macOS displays with one command
- Build `displayplacer` locally from vendored source when needed
- Keep the repo safe to publish by avoiding machine-specific IDs and binaries
- Include both an end-user CLI entrypoint and a reusable Codex skill

## Quick Start / 快速开始

Clone or download the repository, then run:

```bash
./swap-displays --dry-run
./swap-displays
```

下载或 clone 仓库后，先跑一次 `--dry-run` 看它将要执行什么，再正式运行交换。

Behavior:

- If `displayplacer` already exists in `PATH`, the repo uses it
- Otherwise, the first run builds a local copy into `./bin/displayplacer`
- The tool prints the current command and the swapped command before applying changes

## Install / 安装前提

- macOS
- Exactly two active displays
- `python3`
- Xcode or Command Line Tools that provide `cc` and `make`

You do not need Homebrew for the default path in this repository.

这个仓库默认不依赖 Homebrew，因为它可以直接用 vendored source 本地编译 `displayplacer`。

## Usage / 使用方式

End-user entrypoint:

```bash
./swap-displays --dry-run
./swap-displays
```

Manual helper build:

```bash
./scripts/bootstrap_displayplacer.sh
```

Direct Python entrypoint:

```bash
python3 ./scripts/swap_macos_displays.py --dry-run
python3 ./scripts/swap_macos_displays.py
```

Tests:

```bash
python3 ./scripts/test_swap_macos_displays.py
```

## Example dry-run output / 示例输出

The real output on your machine will use your current display IDs. Public examples in this repository use placeholders only:

```text
Current command:
displayplacer "id:<display-a> res:1920x1080 hz:60 color_depth:8 enabled:true scaling:off origin:(0,0) degree:0" "id:<display-b> res:1470x956 hz:60 color_depth:8 enabled:true scaling:on origin:(1920,0) degree:0"

Swapped command:
displayplacer "id:<display-a> res:1920x1080 hz:60 color_depth:8 enabled:true scaling:off origin:(1470,0) degree:0" "id:<display-b> res:1470x956 hz:60 color_depth:8 enabled:true scaling:on origin:(0,0) degree:0"
```

## Privacy / 隐私与安全

This repository does not contain any machine-specific display arrangement captured from the original authoring machine.

这个仓库不会提交作者机器上的显示器 UUID、用户名路径或本地构建二进制。

The only time display IDs appear is when the script runs on the current machine and prints that machine's own live `displayplacer list` output.

## Limitations / 限制

- This tool only targets macOS
- It expects exactly two active displays
- It swaps positions, not arbitrary multi-monitor layouts
- On scaled displays, macOS may normalize the final logical coordinates after applying the change

Treat the swap as successful when the display that used to own `origin:(0,0)` no longer does.

## Repository layout / 仓库结构

- [`swap-displays`](./swap-displays): best entry point for normal users
- [`scripts/bootstrap_displayplacer.sh`](./scripts/bootstrap_displayplacer.sh): local build helper for vendored `displayplacer`
- [`scripts/swap_macos_displays.py`](./scripts/swap_macos_displays.py): implementation
- [`scripts/test_swap_macos_displays.py`](./scripts/test_swap_macos_displays.py): tests
- [`SKILL.md`](./SKILL.md): Codex skill definition
- [`agents/openai.yaml`](./agents/openai.yaml): skill metadata
- [`third_party/displayplacer`](./third_party/displayplacer): vendored upstream source and license

## Third-party code / 第三方依赖

This repository vendors the source of `displayplacer` by Jake Hilborn under the MIT License.

- Upstream project: [jakehilborn/displayplacer](https://github.com/jakehilborn/displayplacer)
- Vendored license: [`third_party/displayplacer/LICENSE`](./third_party/displayplacer/LICENSE)
- Notes: [`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md)

## Codex Skill usage / 作为 Codex Skill 使用

This repository is not only a CLI utility. It also includes a reusable Codex skill:

- Skill file: [`SKILL.md`](./SKILL.md)
- Metadata: [`agents/openai.yaml`](./agents/openai.yaml)

If you are using Codex locally, keep the skill concise and let this README carry the full human-facing product explanation.
