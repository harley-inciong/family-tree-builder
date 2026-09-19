# 🌳 Kinship - Interactive Streamlit Family Tree Builder

A modern, interactive web application built with **Streamlit** and **D3.js** for building, exploring, and sharing genealogical family trees with universal ancestral notation, collapsible branches, and responsive full-screen visualization.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

- **Stemming Tree Layout & Lineage Arrangement**:
  - **Maternal on Left, Paternal on Right**: Strictly arranges maternal ancestors/mothers to the left and paternal ancestors/fathers to the right.
  - **Biological Stemming Branches**: Central trunk drop from parental unions with glowing junction nodes and horizontal descent conduits leading to each child.
  - **Bidirectional Generational Propagation**: Automatically calculates accurate generation tiers so parents are never misplaced into older or younger generations.
- **Side Floating Toolbar (Undo, Redo, Save Progress)**:
  - **↩️ Undo (Ctrl+Z)** and **↪️ Redo (Ctrl+Y)** with complete in-memory history stack.
  - **💾 Save Progress (Ctrl+S)**: Persists snapshots directly to permanent browser local storage with instant toast alerts.
  - **⛶ Fit Canvas**: Instant center-fit zoom.
- **Crop-to-Fit Export Pipeline (PNG & PDF)**:
  - Crops exactly to the dimensions of the family tree without generating long empty rows. Perfect for compact and large trees alike.
- **Clean 2-Column Edit & Add Relative Interface**:
  - Structured 2-column layout in exact hierarchy: First & Middle Name, Surname & Nickname, Gender & Relationship Type, Birth Date & Passing Date.
  - **Vertically Expandable Bio Notes**: Locked horizontal width with smooth vertical expansion.
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
