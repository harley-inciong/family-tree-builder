# 🌳 Kinship - Interactive Streamlit Family Tree Builder

A modern, interactive web application built with **Streamlit** and **D3.js** for building, exploring, and sharing genealogical family trees with universal ancestral notation, collapsible branches, and spreadsheet import/export.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

- **Universal Genealogical Diagram Symbols & Traces**:
  - **■ ♂ (Square / Male)** with cerulean header
  - **● ♀ (Circle / Female)** with rose header
  - **◆ ◇ (Diamond / Other or Unknown)** with amethyst header
  - **† (Latin Cross & Diagonal Strikethrough)** for deceased relatives
  - **══ 💍 ══** Horizontal marriage/union connection
  - **Orthogonal descent forks** tracing parentage to children
  - Dedicated **🧭 Universal Symbols Modal** with visual breakdown
- **Minimal, High-Focus UI**:
  - Uncluttered full-screen family tree canvas without distracting sidebars or tabs.
  - **Hover Tooltips**: Instant preview of lifespan, nickname, bio notes, and family summary on hover.
  - **Click to Edit**: Clicking any member opens an elegant slide-out **Edit & Relationship Drawer**.
- **Family Relationship Hub**:
  - **Parents**: Quick navigation chips to jump to parents + `+ Add Parent` (automatically pairs co-parents as spouses).
  - **Spouses**: Quick navigation chips + `+ Add Spouse`.
  - **Children**: Quick navigation chips + `+ Add Child`.
- **Retractable Lineage Pills**:
  - Collapse any complex descendant branch into a sleek indicator badge (*"▶ Expand Lineage of [Surname]"*), reducing chart clutter.
- **Crisp Export**:
  - **📸 Download PNG**: High-res image with all connecting lines, union links, and symbols rendered.
  - **📄 Download PDF**: Vector landscape PDF generation.
- **Ephemeral Session Privacy**:
  - In-browser session persistence (`sessionStorage`): preserves changes across refreshes, automatically wipes all data when you exit the browser, plus a 1-click **🧹 Clear** button.

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
4. Leave **"Add a README"** unchecked (we already have one).
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
