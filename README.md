# 🥘 Risotto - Static Documentation Site Generator

**Risotto** is a simple, lightweight static site generator that converts Markdown (`.md`) files into a styled HTML documentation website.  
It supports light/dark themes, configurable colors, logos, and navigation structure — all controlled through a `config.risotto` file.

---

## Project Structure

```
your-project/
├── docs/
│   ├── index.md
│   ├── category1/
│   │   ├── intro.md
│   │   └── usage.md
│   └── category2/
│       └── guide.md
├── example.config.risotto
└── risotto.py
```

---

## Getting Started

### 1. Install Requirements
Risotto uses only the Python standard library — **no external dependencies required**.  
You just need **Python 3.8+** installed.

### 2. Prepare Configuration

Copy the example configuration to your working config file:

```bash
cp example.config.risotto config.risotto
```

You can edit `config.risotto` to customize:
- Site name and title  
- Description and favicon  
- Logo for light/dark themes  
- Theme colors  
- Output directory  
- Home page name  

---

## Writing Documentation

Place your Markdown files under the `docs/` directory.  
Each subfolder becomes a category in the sidebar.

Example:
```
docs/
├── index.md
├── GettingStarted/
│   ├── install.md
│   └── config.md
└── Advanced/
    └── tips.md
```

---

## Building the Site

Run the generator:

```bash
python3 risotto.py
```

Optional flags:
```bash
python3 risotto.py --docs docs --config config.risotto
```

This will:
- Convert all Markdown files in `docs/` to HTML
- Create the output folder (default: `site/`)
- Generate:
  - `site/index.html` (home page)
  - `site/<category>/<page>.html` for each subpage

---

##  Theme Switching

The generated site includes a built-in theme toggle:
- Automatically detects system light/dark mode
- Saves user preference to `localStorage`
- Fully configurable through your `config.risotto`

---

## Markdown Features

Risotto supports:
- Headings (`#`, `##`, `###`, etc.)
- Bold and italic (`**bold**`, `_italic_`)
- Inline code and code blocks (`` `code` `` or ```python ... ```)
- Links (`[text](url)`)
- Ordered and unordered lists

---

## 📦 Output

After running the build, open:

```
site/index.html
```

in your browser to preview your generated documentation.

---

## Notes

- The home page (`index.md`) **is required**.
- All other Markdown files must be inside subdirectories.
- You can safely re-run the generator after editing files — it overwrites existing HTML.

Enjoy your hot, fresh docs!
