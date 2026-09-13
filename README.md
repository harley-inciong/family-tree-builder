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
- **Dynamic Branch Builder**:
  - Add **Children**, **Parents**, and **Spouses/Partners** relative to any selected focal relative.
  - Automatic relationship linking across multiple generations.
- **Retractable Lineage Pills**:
  - Click to collapse any complex descendant branch into a sleek indicator badge (*"▶ Lineage of [Surname] (N members)"*), reducing chart clutter.
- **Interactive Visualizer**:
  - Smooth pan and zoom (drag canvas, mousewheel zoom).
  - **Fit Screen** and **Reset Zoom** one-click buttons.
  - **Export High-Res PNG** or **Vector SVG** directly from the chart canvas.
  - Real-time relative search with glow highlights.
- **Data Portability**:
  - **JSON Backup & Restore**: Save your entire editable tree to a `.json` file and restore it anytime.
  - **Spreadsheet / CSV Import**: Upload a `.csv` or `.xlsx` spreadsheet to instantly transform tabular data into a family tree. Starter CSV template included.
- **Ephemeral Session Privacy**:
  - Built-in session state holds changes in your browser and automatically cleans up upon exit or by clicking **🧹 Clear All**.

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

---

## 📊 CSV Import Schema

| Column | Description | Example |
| :--- | :--- | :--- |
| `id` | Unique ID | `1` or `art_1` |
| `first_name` | Given Name | `Arthur` |
| `last_name` | Surname / Lineage | `Pendleton` |
| `nickname` | Informal name | `Artie` |
| `gender` | `M` (Male), `F` (Female), `O` (Other) | `M` |
| `birth_date`| Birth Year / Date | `1932` |
| `death_date`| Passing Year / Date (leave empty if living) | `2015` |
| `is_living` | `TRUE` or `FALSE` | `FALSE` |
| `parent_ids`| Comma-separated parent IDs | `1,2` |
| `spouse_ids`| Comma-separated spouse IDs | `2` |
| `notes` | Biographical notes | `Clockmaker & botanist` |
