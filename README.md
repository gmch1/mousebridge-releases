# MouseBridge 下载与更新

[下载最新安装包](https://github.com/gmch1/mousebridge-releases/releases)

MouseBridge 是原生 macOS 鼠标按键映射、触控板多指快捷键、滚轮与 Logitech DPI 工具。

- macOS 13 及以上；当前发布的应用针对 Apple Silicon。
- 将滚轮中键设为 `cmd+left click`，即可模拟 Command + 左键点击链接。
- 从 0.2.5 开始，菜单栏提供“检查更新…”及“自动检查更新”。旧版需要先手动安装一次。
- 更新包与更新清单使用 Ed25519 签名。没有 Apple 公证的版本标为预发布版，首次运行
  可能需要在系统设置中允许打开。

本仓库只存放公开分发所需文件和发布工具，不包含开发仓库的 Git 历史、个人配置、令牌
或私钥。每个版本的完整对应源码以 `MouseBridge-v<版本>-source.zip` 附件提供，包含构建
脚本和许可证。请使用该附件，而非 GitHub 自动生成的本下载仓库源码归档。

应用采用 GPL-3.0-or-later；具体许可证与第三方声明随安装包及对应源码提供。

`appcast` 是客户端使用的滚动签名更新清单；用户请下载带版本号 Release 中的安装 ZIP。
