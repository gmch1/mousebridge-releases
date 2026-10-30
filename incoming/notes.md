MouseBridge v0.2.7

- Add normal and reversed vertical-scrolling presets for the horizontal thumb
  wheel, with per-direction scroll actions in the custom editor and CLI.
- Preserve wheel distance and event units while moving X into Y, without the
  shortcut cooldown; apply the existing main-wheel reversal and line settings.

- Validation: 41 macOS XCTest cases and 13 publication tests pass. Physical
  MX Master wheel behavior still needs validation on real hardware.

预发布版本：使用 ad-hoc 签名，未经过 Apple 公证。首次安装可能需要在 macOS 中手动允许打开。

安装包与更新清单使用独立 Ed25519 签名。首次安装本版后，可在菜单栏选择“检查更新…”。

GPL-3.0-or-later：完整对应源码见 `MouseBridge-v0.2.7-source.zip`，请勿使用 GitHub 自动生成的下载仓库源码归档。各 ZIP 附带 SHA-256 校验文件。
