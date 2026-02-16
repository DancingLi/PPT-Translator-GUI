# PPT Translator GUI

**One-click PPT translation with perfect formatting preservation**

Built on top of [tristan-mcinnis/PPT-Translator-Formatting-Intact-with-LLMs](https://github.com/tristan-mcinnis/PPT-Translator-Formatting-Intact-with-LLMs) core engine, featuring a complete graphical interface that makes PPT translation as simple as drag-and-drop.

---

## Download

| Version | File | Size | System Requirements |
|---------|------|------|---------------------|
| v1.0.0 | **[PPTTranslator.exe](https://github.com/DancingLi/PPT-Translator-GUI/releases/download/v1.0.0/PPTTranslator.exe)** | ~64MB | Windows 10/11 |

> **Note**: This is a single-file executable. No Python runtime installation required. API key configuration needed on first run.

---

## Quick Start

### 1. Configure API Key (First Time Only)

Run `PPTTranslator.exe`, click the **"API Key Management"** button:

| Provider | Environment Variable | Get API Key | Recommended Model |
|----------|---------------------|-------------|-------------------|
| **DeepSeek** | `DEEPSEEK_API_KEY` | [platform.deepseek.com](https://platform.deepseek.com) | `deepseek-chat` |
| **OpenAI** | `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com) | `gpt-4o` |
| **Anthropic** | `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) | `claude-3-sonnet` |
| **Gemini** | `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com) | `gemini-pro` |
| **Grok** | `GROK_API_KEY` | [console.x.ai](https://console.x.ai) | `grok-beta` |

> **Tip**: API keys are encrypted and stored in Windows Credential Manager. They'll be automatically loaded on next startup.

### 2. Translate PPT

1. **Select File**: Drag & drop or click to select `.pptx` file
2. **Configure Translation**:
   - Choose provider and model from dropdown
   - Set source and target language (e.g., zh → en)
3. **Start Translation**: Click the button and wait for completion
4. **Get Result**: Find `{filename}_translated.pptx` in the same directory

---

## Features

- **100% Format Preservation**: Fonts, colors, spacing, tables, alignment all intact
- **Multi-Provider Support**: Switch between LLM providers with one click
- **Batch Processing**: Translate multiple files at once
- **Smart Caching**: Same text translated once, saving API costs
- **Real-time Preview**: Live progress display with cancel support
- **Local Security**: API keys stored locally, never uploaded

---

## Troubleshooting

### "API Key Not Configured" Error
- Click "API Key Management" and configure at least one provider
- Verify the API key is valid and has available quota

### Translation Errors
- **Check network**: Ensure access to the LLM provider's API endpoint
- **Verify API key**: Confirm the key is valid in provider console
- **Model availability**: Some models require specific permissions

### Format Issues After Translation
- **Font missing**: Install original fonts or replace with common fonts
- **Complex graphics**: SmartArt and complex charts may need manual adjustment
- **Version compatibility**: Use Office 2016+ or WPS to open output files

### Performance Issues
- **Large files**: Split PPTs over 100 pages for batch translation
- **Memory**: Close other apps, ensure 4GB+ available RAM

---

## System Requirements

- **OS**: Windows 10 or Windows 11 (64-bit)
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 100MB free space
- **Network**: Internet connection for LLM API calls

---

## Acknowledgments

This project is built on [tristan-mcinnis/PPT-Translator-Formatting-Intact-with-LLMs](https://github.com/tristan-mcinnis/PPT-Translator-Formatting-Intact-with-LLMs). Special thanks to the original author for the excellent core translation engine.

GUI built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Support & Feedback

- **Report Issues**: [GitHub Issues](https://github.com/DancingLi/PPT-Translator-GUI/issues)
- **Feature Requests**: Welcome via Issues
- **Email**: lipeihangermany@163.com

**Star this project**: If you find it useful, please ⭐ [star it on GitHub](https://github.com/DancingLi/PPT-Translator-GUI)!

---

**Project Homepage**: https://github.com/DancingLi/PPT-Translator-GUI
