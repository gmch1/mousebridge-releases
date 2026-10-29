MouseBridge v0.2.5

- Integrate Sparkle 2.9.4 with menu-bar update checks and a daily automatic-check
  toggle. Installation uses Sparkle's download, signature verification and restart UI.
- Bundle and sign the updater framework and helpers, and verify signed update
  archives and feeds in CI.
- Publish verified update archives and a signed rolling feed through the public
  download repository, without exposing credentials or private repository history.
- Use version-derived build numbers so update ordering is stable across workflow reruns.

预发布版本：使用 ad-hoc 签名，未经过 Apple 公证。首次安装可能需要在 macOS 中手动允许打开。

安装包与更新清单使用独立 Ed25519 签名。首次安装本版后，可在菜单栏选择“检查更新…”。

GPL-3.0-or-later：完整对应源码见 `MouseBridge-v0.2.5-source.zip`，请勿使用 GitHub 自动生成的下载仓库源码归档。各 ZIP 附带 SHA-256 校验文件。
