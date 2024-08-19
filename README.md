# 快捷翻译工具

欢迎使用 **快捷翻译工具**，这是一个高效、易用的翻译辅助软件，旨在帮助用户通过快捷键快速翻译文本。

## 特性

- **快捷键激活**：一键激活翻译功能，无需离开当前工作环境。
- **多语言支持**：支持中文与多种语言的互译。
- **智能识别**：自动检测文本语言，无需手动设置源语言。
- **一键粘贴**：翻译结果直接粘贴到所选位置，方便粘贴使用。

## 使用方法

1. 选择文本并使用快捷键（默认为`Ctrl+i`）。
2. 翻译结果将自动显示，并复制到剪贴板。

## 配置（暂无）

你可以通过配置文件 `config.ini` 自定义快捷键和其他设置：

```ini
[Settings]
shortcut = Ctrl+i  ; 自定义快捷键
language = auto  ; 翻译目标语言
```

## 快捷键自定义（暂无）

如果你需要修改快捷键，可以编辑 `config.ini` 文件中的 `shortcut` 项。

## 依赖

- `pyperclip`：用于剪贴板交互。
- `keyboard`：用于监听快捷键事件。
- `pynput`: 用于模拟按键。
- `tencentcloud-sdk-python-tmt`：腾讯云SDK。

## 开发者

- **Name**: ywm
- **Email**: [ywmssh@gmail.com](mailto:ywmssh@gmail.com)

## 开发状态
- [x] 基本功能已经实现
- [ ] 用图形库封装，提高用户自定义程度
- [ ] 应用打包
- [ ] 构建action自动发布
