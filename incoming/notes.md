MouseBridge v0.2.6

- Add an interactive mouse schematic with selectable middle/side buttons and
  a horizontal thumb-wheel editor, referencing OpenLogi's control-selection UI.
- Add paired horizontal-wheel presets (tabs, browser history, undo/redo,
  desktops and zoom), per-direction custom shortcuts and a swap action.
- Map mouse X-axis scroll events with independent 200 ms direction cooldowns;
  preserve unbound native scrolling, vertical deltas and existing trackpad filtering.
- Migrate to config schema 4 with native horizontal scrolling as the default;
  add `horizontal-left` and `horizontal-right` CLI configuration keys.

- Group settings into Mouse, Trackpad and General pages with native cards,
  scrollable content and a resizable window.
- Offer readable action presets while preserving custom shortcut strings.
- Simplify the menu to device status, Settings, Pause, Check for Updates and Quit;
  move automatic update preferences, permission details and About into General.
- Open General on first settings access when Accessibility permission is missing.

- Validation: 35 macOS XCTest cases and 13 publication tests pass. Physical
  MX Master thumb-wheel behavior still needs validation on real hardware.

预发布版本：使用 ad-hoc 签名，未经过 Apple 公证。首次安装可能需要在 macOS 中手动允许打开。

安装包与更新清单使用独立 Ed25519 签名。首次安装本版后，可在菜单栏选择“检查更新…”。

GPL-3.0-or-later：完整对应源码见 `MouseBridge-v0.2.6-source.zip`，请勿使用 GitHub 自动生成的下载仓库源码归档。各 ZIP 附带 SHA-256 校验文件。
