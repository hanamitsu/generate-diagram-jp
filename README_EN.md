# generate-diagram-jp

Claude Code skill for generating Japanese-language diagrams from text input, powered by Gemini Imagen.

Built on the [PaperBanana](https://github.com/llmsresearch/paperbanana) methodology — a multi-stage pipeline (Retriever → Planner → Stylist → Visualizer → Critic) where Claude handles all reasoning stages and Gemini Imagen generates the final image.

## Examples

| Input | Style | Output |
|-------|-------|--------|
| AI agent pipeline description | balanced | Hand-drawn graphic recording style with colorful soft-tone boxes |
| Healthcare AI strategy comparison | balanced | Side-by-side comparison with ribbon banners and marker highlights |
| 3D character generation pipeline | balanced | Left-to-right pipeline with phase groupings |

## Style Modes

Three modes on a spectrum from academic to graphic recording:

| Mode | Concept | Use Case |
|------|---------|----------|
| `academic` | Minimal Structure, Friendly Icons | Paper submissions, conferences |
| `balanced` (default) | Structured Graphic Note | Tech blogs, presentations, explainer articles |
| `graphic-note` | Visual Graphic Recording | Social media, internal docs, concept overviews |

All modes share the same spatial composition rules (grid alignment, flow direction, whitespace hierarchy). They differ in color usage, line treatment, decoration, and icon style.

## Setup

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
- Python 3.10+
- Gemini API key ([get one here](https://aistudio.google.com/apikey))

### Installation

1. Clone this repository:

```bash
git clone https://github.com/hanamitsu/generate-diagram-jp.git
cd generate-diagram-jp
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your API key:

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

4. Open the project in Claude Code:

```bash
claude
```

## Usage

```
/generate-diagram-jp input.txt "図のキャプション"
/generate-diagram-jp input.txt "図のキャプション" --style graphic-note
```

- First argument: path to a text file describing the content to visualize
- Second argument: caption for the diagram (optional — Claude will ask if omitted)
- `--style`: `academic` / `balanced` (default) / `graphic-note`

### Input Format

The input text file should describe a concept, system, or process in plain Japanese or English. For example:

```
このシステムは3層アーキテクチャを採用する。
第1層はユーザーインターフェース、第2層はビジネスロジック、
第3層はデータベースである。各層間はAPIで通信する。
```

Claude will analyze the text, determine the best diagram type (pipeline, comparison, architecture, etc.), and generate a detailed visual description before passing it to Gemini Imagen for image generation.

## How It Works

1. **Retriever** — Selects reference examples from `data/reference_sets/` based on diagram type and topic similarity
2. **Planner** — Generates a detailed visual description (layout, components, icons, colors) from the input text
3. **Stylist** — Refines the description against the style guide for the chosen mode
4. **Visualizer** — Sends the description to Gemini Imagen via `gemini_generate.py`
5. **Critic** — Evaluates the generated image for faithfulness and readability; may trigger one re-generation

## Project Structure

```
.claude/skills/generate-diagram-jp/
  SKILL.md              # Pipeline definition (the skill itself)
  style-guide.md        # Style rules for all three modes (Japanese)
  scripts/
    gemini_generate.py  # Gemini Imagen API wrapper
data/
  guidelines/
    methodology_style_guide.md  # Style rules (English)
  reference_sets/
    index.json          # Reference example metadata
    images/             # Reference diagram images (~1.2MB total)
```

## License

MIT License — see [LICENSE](LICENSE).

This project is built on [PaperBanana](https://github.com/llmsresearch/paperbanana) (MIT License, Copyright (c) 2025 PaperBanana Contributors).
