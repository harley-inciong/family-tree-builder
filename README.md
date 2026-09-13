# 🌳 Kinship - Interactive Streamlit Family Tree Builder

A modern, interactive web application built with **Streamlit** and **D3.js** for building, exploring, and sharing genealogical family trees with universal ancestral notation, collapsible branches, and responsive full-screen visualization.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

- **Universal Genealogical Diagram Symbols & Extended Notation**:
  - **■ ♂ (Square / Male)** with cerulean header
  - **● ♀ (Circle / Female)** with rose header
  - **◆ ◇ (Diamond / Other or Unknown)** with amethyst header
  - **† (Latin Cross & Diagonal Strikethrough)** for deceased relatives
  - **══ 💍 ══ (Marriage)**, **══ ≠ ══ (Divorced / Separated)**, and **🤝 (Partners)**
  - **Descent Traces**: Solid (Biological), Dashed (`- - -` for Adopted with `[Name]`), Dotted (`···` for Foster/Ward), and Step relations
  - Dedicated **🧭 Universal Symbols Modal** detailing all symbols
- **🇵🇭 Philippine Naming System & Parent Auto-Allocation**:
  - Dedicated data entry for **Middle Name** (Maternal maiden surname) and **Surname** (Paternal surname).
  - Automatically detects when middle and last names are provided and offers 1-click **Auto-Allocation of Father and Mother branches** linked in marriage!
- **Zero-Cropping Export Pipeline**:
  - **📸 Download PNG**: Captures the entire tree canvas at 2x resolution with untruncated bounds and all connection lines preserved.
  - **📄 Download PDF**: Vector landscape PDF generation tailored to the exact dimensions of your tree.
- **100% Responsive UI/UX**:
  - Full-viewport responsive layout (`96vh`) that automatically refits whenever the browser window is resized.
  - **Hover Tooltips**: Instant preview of lifespan, nickname, bio notes, and family summary on hover.
  - **Click to Edit**: Clicking any member opens an elegant slide-out **Edit & Relationship Drawer**.
- **Family Relationship Hub**:
  - Quick navigation chips to jump between parents, spouses, and children, with instant `+ Add` shortcuts.
- **Retractable Lineage Pills**:
  - Collapse complex descendant branches into sleek indicator badges (*"▶ Expand Lineage of [Surname]"*).
- **Ephemeral Session Privacy**:
  - In-browser session persistence (`sessionStorage`): automatically saves your work across page refreshes and cleans up when the browser tab is closed.

---

## 🚀 Quickstart

### Prerequisites
- Python 3.9+
- `pip` or Python Launcher (`py`)

### Local Installation
```bash
# 1. Clone or navigate to the directory
cd family-tree-builder

# 2. Install dependencies
py -m pip install -r requirements.txt

# 3. Run the app
py -m streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📤 Push to GitHub & Deploy Live

Instructions for **[harley-inciong](https://github.com/harley-inciong)**:

### 1. Create Repository on GitHub
1. Go to [https://github.com/new](https://github.com/new).
2. Set repository name to: **`family-tree-builder`**.
3. Choose **Public**.
4. Leave **"Add a README file"** unchecked (we already have one).
5. Click **Create repository**.

### 2. Push Local Code
Run these commands in PowerShell or Terminal:
```bash
cd C:\Users\acer\.gemini\antigravity\scratch\family-tree-builder
git init
git add .
git commit -m "feat: complete interactive family tree builder"
git branch -M main
git remote add origin https://github.com/harley-inciong/family-tree-builder.git
git push -u origin main
```

### 3. Deploy Live for Free on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
2. Click **New app**.
3. Select your repository: `harley-inciong/family-tree-builder`.
4. Branch: `main`.
5. Main file path: `app.py`.
6. Click **Deploy!**
