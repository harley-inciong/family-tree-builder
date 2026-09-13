"""
app.py - Interactive Streamlit Family Tree Builder
"""
import streamlit as st
import streamlit.components.v1 as components
from tree_model import FamilyTree, FamilyMember
from sample_data import get_sample_family_tree
from visualizer import generate_family_tree_html
from import_export import (
    export_tree_to_json,
    import_tree_from_json,
    generate_csv_template,
    import_tree_from_sheet,
    CSV_COLUMNS
)

# Page configuration
st.set_page_config(
    page_title="Kinship | Family Tree Builder",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    /* Clean headers and badges */
    .metric-card {
        background: #1E293B;
        padding: 12px 16px;
        border-radius: 8px;
        border: 1px solid #334155;
        text-align: center;
        color: #F8FAFC;
    }
    .metric-value {
        font-size: 22px;
        font-weight: 700;
        color: #38BDF8;
    }
    .metric-label {
        font-size: 11px;
        text-transform: uppercase;
        color: #94A3B8;
        letter-spacing: 0.5px;
    }
    .sidebar-section {
        background: #F1F5F9;
        padding: 10px;
        border-radius: 6px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "tree" not in st.session_state:
    st.session_state.tree = get_sample_family_tree()

if "selected_id" not in st.session_state:
    st.session_state.selected_id = st.session_state.tree.root_id

tree: FamilyTree = st.session_state.tree

# Ensure selected member exists
if st.session_state.selected_id not in tree.members and tree.members:
    st.session_state.selected_id = tree.root_id or next(iter(tree.members.keys()))
elif not tree.members:
    st.session_state.selected_id = None

# TOP HEADER & METRICS
col_title, col_m1, col_m2, col_m3, col_m4 = st.columns([4, 1.2, 1.2, 1.2, 1.2])

with col_title:
    st.title("🌳 Kinship")
    st.caption("Interactive Genealogical Tree Builder • Universal Notation • Ephemeral In-Browser Session")

with col_m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(tree.members)}</div>
        <div class="metric-label">Relatives</div>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{tree.get_generation_depth()}</div>
        <div class="metric-label">Generations</div>
    </div>
    """, unsafe_allow_html=True)

with col_m3:
    living_count = sum(1 for m in tree.members.values() if m.is_living)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:#10B981;">{living_count}</div>
        <div class="metric-label">Living</div>
    </div>
    """, unsafe_allow_html=True)

with col_m4:
    deceased_count = sum(1 for m in tree.members.values() if not m.is_living)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:#94A3B8;">{deceased_count}</div>
        <div class="metric-label">Deceased (†)</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ----------------- SIDEBAR CONTROLS -----------------
with st.sidebar:
    st.header("👤 Relative Inspector")

    # Member Search & Selection Box
    member_options = {}
    for m in sorted(tree.members.values(), key=lambda x: (x.last_name, x.first_name)):
        sym = m.symbol_glyph
        status = "†" if not m.is_living else ""
        label = f"{sym} {m.display_name} {status} ({m.lifespan_str})"
        member_options[m.id] = label

    if member_options:
        selected_key = st.selectbox(
            "Select Current Focal Relative:",
            options=list(member_options.keys()),
            format_func=lambda k: member_options[k],
            index=list(member_options.keys()).index(st.session_state.selected_id) if st.session_state.selected_id in member_options else 0,
            key="sidebar_selector"
        )
        st.session_state.selected_id = selected_key
    else:
        st.info("Tree is currently empty. Add a root member below!")
        st.session_state.selected_id = None

    selected_member = tree.get_member(st.session_state.selected_id)

    if selected_member:
        # Quick badges
        st.markdown(f"**Focused:** `{selected_member.display_name}`")
        if selected_member.notes:
            st.caption(f"📝 *{selected_member.notes}*")

        # Quick Actions Row
        c_act1, c_act2 = st.columns(2)
        with c_act1:
            collapse_label = "Expand Lineage" if selected_member.is_collapsed else "Collapse Lineage"
            if st.button(f"🗂️ {collapse_label}", use_container_width=True):
                selected_member.is_collapsed = not selected_member.is_collapsed
                st.rerun()
        with c_act2:
            if st.button("👑 Make Root", use_container_width=True, help="Set this relative as the ancestral root"):
                tree.root_id = selected_member.id
                st.success(f"{selected_member.first_name} is now the primary root.")
                st.rerun()

        st.divider()

        # TABS: Add Branch vs Edit Relative
        side_tab_add, side_tab_edit = st.tabs(["➕ Add Branch", "✏️ Edit Details"])

        with side_tab_add:
            st.subheader("Add Connected Branch")
            branch_type = st.radio(
                "Branch Type to Connect:",
                ["👶 Child", "👴 Parent", "💍 Spouse / Partner"],
                index=0
            )

            with st.form("add_branch_form", clear_on_submit=True):
                col_fn, col_ln = st.columns(2)
                with col_fn:
                    new_fn = st.text_input("First Name*", placeholder="e.g. Liam")
                with col_ln:
                    default_ln = selected_member.last_name if "Child" in branch_type else ""
                    new_ln = st.text_input("Surname / Last Name", value=default_ln, placeholder="e.g. Vance")

                new_nick = st.text_input("Nickname (Optional)", placeholder="e.g. Lee")
                
                col_g, col_b = st.columns(2)
                with col_g:
                    new_gender = st.selectbox("Gender / Symbol", ["Male (♂)", "Female (♀)", "Other / Unknown (◇)"])
                with col_b:
                    new_birth = st.text_input("Birth Year / Date", placeholder="e.g. 1995")

                new_is_living = st.checkbox("Currently Living", value=True)
                new_death = ""
                if not new_is_living:
                    new_death = st.text_input("Passing Year / Date (†)", placeholder="e.g. 2020")

                new_notes = st.text_area("Notes / Bio", placeholder="Profession, hometown, achievements...", height=68)

                # If adding child, optionally select other parent from existing spouses
                other_p_id = None
                if "Child" in branch_type and selected_member.spouses:
                    spouse_choices = {"None / Unspecified": None}
                    for sp_id in selected_member.spouses:
                        sp_m = tree.get_member(sp_id)
                        if sp_m:
                            spouse_choices[sp_m.display_name] = sp_m.id
                    chosen_sp_name = st.selectbox("Second Parent (Optional):", list(spouse_choices.keys()))
                    other_p_id = spouse_choices[chosen_sp_name]

                submit_add = st.form_submit_button("🌱 Add Branch to Tree", use_container_width=True)

                if submit_add:
                    if not new_fn.strip():
                        st.error("First name is required!")
                    else:
                        g_code = "M" if "Male" in new_gender else ("F" if "Female" in new_gender else "O")
                        new_mem = FamilyMember(
                            first_name=new_fn,
                            last_name=new_ln,
                            nickname=new_nick,
                            gender=g_code,
                            birth_date=new_birth,
                            death_date=new_death,
                            is_living=new_is_living and not new_death.strip(),
                            notes=new_notes
                        )

                        if "Child" in branch_type:
                            tree.add_child(selected_member.id, new_mem, other_parent_id=other_p_id)
                        elif "Parent" in branch_type:
                            tree.add_parent(selected_member.id, new_mem)
                        else:  # Spouse
                            tree.add_spouse(selected_member.id, new_mem)

                        st.session_state.selected_id = new_mem.id
                        st.success(f"Added {new_mem.display_name}!")
                        st.rerun()

        with side_tab_edit:
            st.subheader(f"Edit {selected_member.first_name}")
            with st.form("edit_member_form"):
                col_efn, col_eln = st.columns(2)
                with col_efn:
                    edit_fn = st.text_input("First Name", value=selected_member.first_name)
                with col_eln:
                    edit_ln = st.text_input("Surname / Last Name", value=selected_member.last_name)

                edit_nick = st.text_input("Nickname", value=selected_member.nickname)
                
                g_index = 0 if selected_member.gender == 'M' else (1 if selected_member.gender == 'F' else 2)
                edit_gender = st.selectbox("Gender", ["Male (♂)", "Female (♀)", "Other / Unknown (◇)"], index=g_index)
                
                col_eb, col_ed = st.columns(2)
                with col_eb:
                    edit_birth = st.text_input("Birth Date/Year", value=selected_member.birth_date)
                with col_ed:
                    edit_death = st.text_input("Death Date/Year", value=selected_member.death_date)

                edit_living = st.checkbox("Currently Living", value=selected_member.is_living and not edit_death.strip())
                edit_notes = st.text_area("Notes / Bio", value=selected_member.notes, height=75)

                col_sub1, col_sub2 = st.columns(2)
                with col_sub1:
                    save_edit = st.form_submit_button("💾 Save Changes", use_container_width=True)

                if save_edit:
                    g_code = "M" if "Male" in edit_gender else ("F" if "Female" in edit_gender else "O")
                    tree.update_member(
                        selected_member.id,
                        first_name=edit_fn,
                        last_name=edit_ln,
                        nickname=edit_nick,
                        gender=g_code,
                        birth_date=edit_birth,
                        death_date=edit_death,
                        is_living=edit_living and not edit_death.strip(),
                        notes=edit_notes
                    )
                    st.success("Changes saved!")
                    st.rerun()

            # Delete Member Section
            with st.expander("⚠️ Danger Zone: Delete Member"):
                st.warning(f"Delete `{selected_member.display_name}` from the tree?")
                if st.button("🗑️ Confirm Delete", type="primary", use_container_width=True):
                    tree.delete_member(selected_member.id)
                    st.session_state.selected_id = tree.root_id
                    st.success("Member removed.")
                    st.rerun()
    else:
        # If tree is empty, provide Root Member creator
        st.subheader("Create Base Root Member")
        with st.form("root_create_form"):
            root_fn = st.text_input("First Name*", "Alexander")
            root_ln = st.text_input("Surname", "Hamilton")
            root_gender = st.selectbox("Gender", ["Male (♂)", "Female (♀)", "Other / Unknown (◇)"])
            root_birth = st.text_input("Birth Year", "1755")
            root_submit = st.form_submit_button("🌱 Plant Root Member", use_container_width=True)
            if root_submit and root_fn.strip():
                g_code = "M" if "Male" in root_gender else ("F" if "Female" in root_gender else "O")
                root_mem = FamilyMember(
                    first_name=root_fn,
                    last_name=root_ln,
                    gender=g_code,
                    birth_date=root_birth
                )
                tree.add_member(root_mem)
                tree.root_id = root_mem.id
                st.session_state.selected_id = root_mem.id
                st.success("Root planted!")
                st.rerun()

# ----------------- MAIN CANVAS & CONTROLS -----------------
main_c1, main_c2, main_c3, main_c4 = st.columns([3, 1.2, 1.2, 1.2])

with main_c1:
    search_q = st.text_input("🔍 Quick Search Relative (highlights matches in real-time):", placeholder="Type name, nickname, or surname...").strip()

with main_c2:
    canvas_height = st.slider("Canvas Height", min_value=500, max_value=950, value=680, step=30)

with main_c3:
    if st.button("🔄 Reload Sample", use_container_width=True, help="Reset to the 3-generation demo tree"):
        st.session_state.tree = get_sample_family_tree()
        st.session_state.selected_id = st.session_state.tree.root_id
        st.rerun()

with main_c4:
    if st.button("🧹 Clear All", use_container_width=True, help="Wipe all data for a fresh private session"):
        st.session_state.tree = FamilyTree()
        st.session_state.selected_id = None
        st.rerun()

# Render Interactive SVG/D3 Diagram
html_diagram = generate_family_tree_html(
    tree=tree,
    selected_id=st.session_state.selected_id,
    search_query=search_q,
    height=canvas_height
)

components.html(html_diagram, height=canvas_height + 20, scrolling=False)

st.write("")

# ----------------- BOTTOM TABS: IMPORT / EXPORT / GUIDE -----------------
tab_sheet, tab_json, tab_symbols, tab_deploy = st.tabs([
    "📊 Import Spreadsheet (CSV / Excel)",
    "💾 JSON Save & Restore",
    "🧭 Universal Diagram Symbols Legend",
    "🚀 GitHub & Streamlit Cloud Deploy Guide"
])

with tab_sheet:
    st.subheader("Transform Spreadsheet to Family Tree")
    st.write(
        "Upload a spreadsheet (.csv or .xlsx) with relative relationships to instantly transform it into an interactive tree!"
    )
    
    col_s1, col_s2 = st.columns([1, 2])
    with col_s1:
        st.download_button(
            label="📄 Download Starter CSV Template",
            data=generate_csv_template(),
            file_name="family_tree_template.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.caption("Includes example columns: `id`, `first_name`, `last_name`, `gender`, `birth_date`, `parent_ids`, `spouse_ids`")

    with col_s2:
        uploaded_sheet = st.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx", "xls"])
        if uploaded_sheet is not None:
            if st.button("⚡ Transform to Family Tree", type="primary"):
                bytes_data = uploaded_sheet.read()
                imported_tree, msg = import_tree_from_sheet(bytes_data, uploaded_sheet.name)
                if imported_tree:
                    st.session_state.tree = imported_tree
                    st.session_state.selected_id = imported_tree.root_id
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

with tab_json:
    st.subheader("JSON Save & Restore (Full Tree Backup)")
    st.write("Save your work as an editable JSON backup file and restore it on any device.")
    
    c_j1, c_j2 = st.columns(2)
    with c_j1:
        json_data = export_tree_to_json(tree)
        st.download_button(
            label="💾 Download Tree (.json)",
            data=json_data,
            file_name="my_family_tree.json",
            mime="application/json",
            use_container_width=True
        )
    with c_j2:
        uploaded_json = st.file_uploader("Restore from .json file", type=["json"])
        if uploaded_json is not None:
            if st.button("📂 Load JSON Tree", use_container_width=True):
                try:
                    raw_str = uploaded_json.read().decode("utf-8")
                    restored_tree = import_tree_from_json(raw_str)
                    st.session_state.tree = restored_tree
                    st.session_state.selected_id = restored_tree.root_id
                    st.success("Family tree restored successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to load JSON: {str(e)}")

with tab_symbols:
    st.subheader("Universal Genealogical Notation & Visual Traces")
    st.markdown("""
    Standard genealogical conventions used across international ancestral charts and genograms:

    | Symbol / Trace | Meaning | Visual Representation in Chart |
    | :--- | :--- | :--- |
    | **■ ♂ (Square)** | **Male** | Blue card header with square marker and `♂` glyph |
    | **● ♀ (Circle)** | **Female** | Rose/pink card header with circle marker and `♀` glyph |
    | **◆ ◇ (Diamond)** | **Other / Unknown** | Purple card header with diamond marker and `◇` glyph |
    | **† (Latin Cross)** | **Deceased** | Cross before death year (`†2015`), diagonal strikethrough pattern |
    | **══ 💍 ══** | **Marriage / Union** | Horizontal double dashed link with gold wedding ring |
    | **│ └───┘ │** | **Descent / Offspring** | Orthogonal downward fork branching to all children |
    | **▶ Lineage Badge** | **Retractable Lineage** | Indigo pill summarizing descendants to reduce visual clutter |
    """)

with tab_deploy:
    st.subheader("Push to GitHub & Deploy Live")
    st.markdown("""
    ### 1. Create Repository on GitHub
    1. Visit [https://github.com/new](https://github.com/new).
    2. Name your repo: **`family-tree-builder`**.
    3. Keep it **Public**, leave *Add a README* **unchecked**.
    4. Click **Create repository**.

    ### 2. Push from your machine
    Open PowerShell in this project folder and run:
    ```powershell
    cd C:\\Users\\acer\\.gemini\\antigravity\\scratch\\family-tree-builder
    git init
    git add .
    git commit -m "feat: complete interactive family tree builder with universal symbols"
    git branch -M main
    git remote add origin https://github.com/harley-inciong/family-tree-builder.git
    git push -u origin main
    ```

    ### 3. Deploy for free on Streamlit Community Cloud
    1. Open [share.streamlit.io](https://share.streamlit.io).
    2. Click **New app** and select:
       - **Repository**: `harley-inciong/family-tree-builder`
       - **Branch**: `main`
       - **Main file path**: `app.py`
    3. Click **Deploy!** — your site is now live on the internet! 🌐
    """)
