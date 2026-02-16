# PPT Translator GUI

**一键翻译 PPT，完美保留格式**

基于 [tristan-mcinnis/PPT-Translator-Formatting-Intact-with-LLMs](https://github.com/tristan-mcinnis/PPT-Translator-Formatting-Intact-with-LLMs) 开发，新增完整图形界面，让非技术用户也能轻松使用。

---

## 下载

| 版本 | 文件 | 大小 | 系统要求 |
|------|------|------|----------|
| v1.0.0 | [PPTTranslator.exe](https://github.com/DancingLi/PPT-Translator-GUI/releases/download/v1.0.0/PPTTranslator.exe) | ~64MB | Windows 10/11 |

> **注意**: 本程序为单文件可执行程序，无需安装 Python 环境，但首次运行时需要配置 API 密钥。

---

## 快速开始

### 1. 首次运行配置

双击 `PPTTranslator.exe`，点击 **"API 密钥管理"** 按钮：

| 提供商 | 环境变量名 | 获取地址 |
|--------|-----------|----------|
| OpenAI | `OPENAI_API_KEY` | https://platform.openai.com |
| Anthropic | `ANTHROPIC_API_KEY` | https://console.anthropic.com |
| Gemini | `GEMINI_API_KEY` | https://aistudio.google.com |
| DeepSeek | `DEEPSEEK_API_KEY` | https://platform.deepseek.com |
| Grok | `GROK_API_KEY` | https://console.x.ai |

> **提示**: 配置 API 密钥后，程序会自动保存，下次启动无需重复配置。

### 2. 翻译 PPT

1. **选择文件**: 点击 "选择 PPT 文件" 或拖拽文件到窗口
2. **选择提供商**: 从下拉菜单选择已配置 API 的 LLM 提供商
3. **选择模型**: 选择具体的模型（如 gpt-4o, claude-3-sonnet 等）
4. **设置语言**: 选择源语言和目标语言
5. **开始翻译**: 点击 "开始翻译" 按钮

### 3. 查看结果

翻译完成后，程序会在原文件同目录下生成 `{原文件名}_translated.pptx`。

---

## 常见问题

### Q: 提示 "API Key 未配置"
A: 请点击 "API 密钥管理" 按钮，至少配置一个 LLM 提供商的 API 密钥。

### Q: 翻译过程中报错
A: 请检查：
- API 密钥是否有效
- 网络连接是否正常
- 所选模型是否对您可用（部分模型需要特定权限）

### Q: 翻译后的 PPT 格式错乱
A: 本程序使用 XML 中间格式保留所有格式属性，如遇格式问题：
- 确保原 PPT 使用标准字体
- 检查特殊图形对象（如 SmartArt）可能需要手动调整

### Q: 支持哪些 PPT 格式？
A: 支持 `.pptx` 格式（Office 2007+）。不支持旧的 `.ppt` 格式。

---

## 系统要求

- **操作系统**: Windows 10 或 Windows 11
- **内存**: 4GB RAM（推荐 8GB+）
- **磁盘空间**: 100MB 可用空间
- **网络**: 需要连接互联网以调用 LLM API

---

## 致谢

本项目基于 [tristan-mcinnis/PPT-Translator-Formatting-Intact-with-LLMs](https://github.com/tristan-mcinnis/PPT-Translator-Formatting-Intact-with-LLMs) 开发，感谢原作者提供的优秀核心翻译引擎。

GUI 界面使用 [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) 构建。

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

---

## 反馈与支持

如有问题或建议，欢迎提交 [Issue](https://github.com/DancingLi/PPT-Translator-GUI/issues)。

**项目主页**: https://github.com/DancingLi/PPT-Translator-GUI
