MouseBridge v0.2.8

- Prevent external mouse clicks from triggering trackpad multi-finger shortcuts
  while fingers rest on the trackpad. Resolve click origin using the HID sender
  and device identity, following OpenLogi's implementation. Unknown sources pass
  through without consuming the armed trackpad gesture.
- Preserve successfully loaded settings when the startup configuration rewrite
  fails. Distinguish write/read errors from malformed JSON; only malformed JSON
  is moved to a corrupt-config backup.
- Include the OpenLogi MIT license in the application bundle.

- Validation: 47 macOS XCTest cases and 13 publication tests pass. Built-in and
  external trackpad click attribution still needs hardware regression testing.

预发布版本：使用 ad-hoc 签名，未经过 Apple 公证。首次安装可能需要在 macOS 中手动允许打开。

安装包与更新清单使用独立 Ed25519 签名。首次安装本版后，可在菜单栏选择“检查更新…”。

GPL-3.0-or-later：完整对应源码见 `MouseBridge-v0.2.8-source.zip`，请勿使用 GitHub 自动生成的下载仓库源码归档。各 ZIP 附带 SHA-256 校验文件。
