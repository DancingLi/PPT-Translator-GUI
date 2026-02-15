# PPT Translator - Project Knowledge Base

## Project Overview

**PPT Translator** is a Python-based tool that translates PowerPoint presentations while preserving formatting. It supports multiple AI translation providers and maintains fonts, colors, spacing, tables, and alignment after translation.

---

## Project Metadata

- **Language**: Python 3.10+
- **Package Manager**: UV
- **License**: MIT
- **Test Framework**: Pytest
- **Code Style**: Black

---

## Directory Structure

```
ppt-translator/
├── ppt_translator/               # Core translation module
│   ├── cli.py                   # CLI parsing and orchestration
│   ├── pipeline.py              # PPT extraction, translation, regeneration
│   ├── translation.py           # Chunking + caching translation service
│   ├── utils.py                 # Filesystem helpers
│   ├── __init__.py
│   └── providers/               # AI provider adapters
│       ├── base.py              # Base provider interface
│       ├── openai_provider.py   # OpenAI provider
│       ├── anthropic_provider.py # Anthropic provider
│       ├── deepseek.py          # DeepSeek provider
│       ├── gemini_provider.py   # Google Gemini provider
│       ├── grok_provider.py     # Grok provider
│       ├── glm_provider.py      # GLM provider
│       └── __init__.py
├── tests/                        # Test suite
│   ├── conftest.py
│   ├── test_translation.py
│   └── test_utils.py
├── .claude/skills/ppt-translator/ # Self-contained Agent Skill
│   ├── SKILL.md
│   ├── LICENSE.txt
│   └── scripts/                   # Copy of all translation scripts
├── main.py                        # Entry point
├── requirements.txt               # Dependencies
├── example.env                    # Environment variable template
├── README.md                      # Project documentation
└── 使用手册.md                    # Chinese user manual
```

---

## Key Files

### Core Modules

| File | Purpose |
|------|---------|
| `main.py` | Entry point - loads .env and delegates to CLI |
| `ppt_translator/cli.py` | Command-line argument parsing and orchestration |
| `ppt_translator/pipeline.py` | Main pipeline: PPT → XML → Translate → PPTX |
| `ppt_translator/translation.py` | Translation service with chunking and caching |
| `ppt_translator/utils.py` | Filesystem utilities and helpers |

### Provider Adapters

| File | Provider | Default Model |
|------|----------|---------------|
| `openai_provider.py` | OpenAI | gpt-5.2-2025-12-11 |
| `anthropic_provider.py` | Anthropic | claude-sonnet-4-5-20250514 |
| `deepseek.py` | DeepSeek | deepseek-chat |
| `gemini_provider.py` | Google Gemini | gemini-3-flash-preview |
| `grok_provider.py` | Grok | grok-4.1-fast |
| `glm_provider.py` | GLM | (custom) |

---

## Supported Providers & Configuration

| Provider | Required Variable | Optional Variables | Default Model |
|----------|------------------|-------------------|---------------|
| DeepSeek | `DEEPSEEK_API_KEY` | `DEEPSEEK_API_BASE` | `deepseek-chat` |
| OpenAI | `OPENAI_API_KEY` | `OPENAI_ORG` | `gpt-5.2-2025-12-11` |
| Anthropic | `ANTHROPIC_API_KEY` | — | `claude-sonnet-4-5-20250514` |
| Grok | `GROK_API_KEY` | `GROK_API_BASE` | `grok-4.1-fast` |
| Gemini | `GEMINI_API_KEY` | — | `gemini-3-flash-preview` |

---

## Usage Examples

### Basic Translation

```bash
python main.py /path/to/decks \
  --provider openai \
  --source-lang zh \
  --target-lang en
```

### Advanced Options

```bash
python main.py /path/to/decks \
  --provider openai \
  --model gpt-5-mini \
  --source-lang zh \
  --target-lang en \
  --max-workers 4 \
  --max-chunk-size 1000 \
  --keep-intermediate
```

### Available CLI Options

| Option | Description |
|--------|-------------|
| `--provider` | Choose provider: deepseek, openai, anthropic, grok, gemini |
| `--model` | Override default model |
| `--source-lang` | Source language code (ISO) |
| `--target-lang` | Target language code (ISO) |
| `--max-chunk-size` | Character limit per translation request (default: 1000) |
| `--max-workers` | Thread count for scanning slides (default: 4) |
| `--keep-intermediate` | Keep intermediate XML files |

---

## Output Files

For each input file `{deck}.pptx`, the tool generates:

1. `{deck}_original.xml` - Extracted source content
2. `{deck}_translated.xml` - Translated content
3. `{deck}_translated.pptx` - Rebuilt presentation with translated text

---

## Testing

Run the test suite with Pytest:

```bash
pytest
```

Tests focus on:
- Translation chunking/caching
- CLI utilities
- Provider integration

---

## Dependencies

Core dependencies (from `requirements.txt`):

- `python-pptx` - PowerPoint file manipulation
- `openai` - OpenAI API client
- `anthropic` - Anthropic API client
- `google-generativeai` - Google Gemini client
- `python-dotenv` - Environment variable management
- `pytest` - Testing framework
- `tqdm` - Progress bars
- `openpyxl` - Excel file support
- `Pillow` - Image processing

---

## Architecture Notes

### Pipeline Flow

```
PPTX Input → Extract XML → Parse Text → Translate → Rebuild PPTX
                ↓              ↓            ↓
           Original.xml    Chunks    Translated.xml
```

### Key Design Decisions

1. **Provider Pattern** - All AI providers implement a common base interface for easy swapping
2. **Chunking** - Large texts are split into manageable chunks to respect API limits
3. **Caching** - Translated strings are cached to avoid duplicate API calls
4. **Threading** - Multiple workers scan slides in parallel for performance

### Extension Points

To add a new translation provider:

1. Create `ppt_translator/providers/{name}_provider.py`
2. Inherit from `BaseProvider`
3. Implement `translate()` method
4. Register in provider imports

---

## Agent Skill

This project includes a self-contained Agent Skill in `.claude/skills/ppt-translator/`:

- `SKILL.md` - Instructions for Claude on how to use the tool
- `scripts/` - Complete copy of all translation scripts and dependencies

To use in another project: Copy the `.claude/skills/ppt-translator/` directory into your project's `.claude/skills/` folder.

---

## Recent Updates

- **Gemini support**: Added Google Gemini as a translation provider
- **Updated model defaults**: Now using latest model versions
- **Security fix**: Replaced unsafe `eval()` with safe lookup functions

---

## License

MIT License - See `LICENSE` for details

---

*This knowledge base was automatically generated for the PPT Translator project.*
