"""
visualizer.py - High-fidelity Interactive Family Tree Visualizer with Universal Symbols,
Zoom/Pan, Collapsible Lineage, and Vector/PNG Export.
"""
import json
from typing import Optional
from tree_model import FamilyTree

def generate_family_tree_html(
    tree: FamilyTree,
    selected_id: Optional[str] = None,
    search_query: str = "",
    height: int = 700
) -> str:
    """
    Generate an interactive SVG/HTML representation of the family tree
    with D3 zoom/pan, universal genealogical notation, and export capabilities.
    """
    tree_data = tree.to_dict()
    gen_map = tree.get_generations_map()

    # Calculate descendant counts for collapsible badges
    desc_counts = {}
    for mid in tree.members:
        desc_counts[mid] = tree.count_descendants(mid)

    tree_json_str = json.dumps(tree_data)
    gen_map_str = json.dumps(gen_map)
    desc_counts_str = json.dumps(desc_counts)
    selected_id_str = json.dumps(selected_id or "")
    search_query_str = json.dumps(search_query or "")

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Family Tree Diagram</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }}

  body {{
    background: #0F172A;
    color: #F8FAFC;
    overflow: hidden;
    user-select: none;
    height: {height}px;
    position: relative;
  }}

  #canvas-container {{
    width: 100%;
    height: 100%;
    cursor: grab;
  }}
  #canvas-container:active {{
    cursor: grabbing;
  }}

  /* Floating Toolbar */
  .toolbar {{
    position: absolute;
    top: 14px;
    right: 14px;
    display: flex;
    gap: 8px;
    background: rgba(30, 41, 59, 0.85);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 6px 10px;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    z-index: 50;
  }}

  .tool-btn {{
    background: #334155;
    border: 1px solid #475569;
    color: #F1F5F9;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    display: inline-flex;
    align-items: center;
    gap: 5px;
  }}
  .tool-btn:hover {{
    background: #2563EB;
    border-color: #3B82F6;
    transform: translateY(-1px);
    color: white;
  }}

  /* Legend Pill in top-left */
  .legend {{
    position: absolute;
    top: 14px;
    left: 14px;
    background: rgba(30, 41, 59, 0.85);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 11px;
    color: #CBD5E1;
    display: flex;
    align-items: center;
    gap: 12px;
    z-index: 50;
  }}
  .legend-item {{
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  .sym-male {{ color: #60A5FA; font-weight: bold; }}
  .sym-female {{ color: #F472B6; font-weight: bold; }}
  .sym-other {{ color: #C084FC; font-weight: bold; }}
  .sym-deceased {{ color: #94A3B8; font-weight: bold; }}

  /* SVG Links */
  .link-descent {{
    fill: none;
    stroke: #64748B;
    stroke-width: 2.5px;
    stroke-linecap: round;
    stroke-linejoin: round;
    transition: stroke 0.3s;
  }}
  .link-marriage {{
    fill: none;
    stroke: #F59E0B;
    stroke-width: 3px;
    stroke-dasharray: 6 3;
    transition: stroke 0.3s;
  }}

  /* Node Cards */
  .node-card {{
    cursor: pointer;
    transition: transform 0.15s ease;
  }}
  .node-card:hover rect.card-bg {{
    stroke: #60A5FA;
    stroke-width: 2.5px;
    filter: drop-shadow(0 0 10px rgba(96, 165, 250, 0.5));
  }}

  rect.card-bg {{
    rx: 10px;
    ry: 10px;
    transition: all 0.2s ease;
  }}

  .card-male rect.card-bg {{
    fill: #1E293B;
    stroke: #3B82F6;
    stroke-width: 1.5px;
  }}
  .card-female rect.card-bg {{
    fill: #1E293B;
    stroke: #EC4899;
    stroke-width: 1.5px;
  }}
  .card-other rect.card-bg {{
    fill: #1E293B;
    stroke: #A855F7;
    stroke-width: 1.5px;
  }}
  .card-deceased rect.card-bg {{
    fill: #18202F;
    stroke: #64748B;
    stroke-dasharray: 4 2;
  }}

  .node-selected rect.card-bg {{
    stroke: #FACC15 !important;
    stroke-width: 3.5px !important;
    filter: drop-shadow(0 0 14px rgba(250, 204, 21, 0.8)) !important;
  }}

  .node-searched rect.card-bg {{
    stroke: #10B981 !important;
    stroke-width: 3px !important;
    filter: drop-shadow(0 0 12px rgba(16, 185, 129, 0.8)) !important;
  }}

  /* Retracted Lineage Pill */
  .retracted-pill rect {{
    fill: #312E81;
    stroke: #818CF8;
    stroke-width: 1.5px;
    rx: 16px;
    ry: 16px;
    cursor: pointer;
  }}
  .retracted-pill:hover rect {{
    fill: #4338CA;
    stroke: #A5B4FC;
    filter: drop-shadow(0 0 8px rgba(129, 140, 248, 0.6));
  }}

  .info-tooltip {{
    position: absolute;
    bottom: 12px;
    left: 14px;
    font-size: 11px;
    color: #64748B;
    pointer-events: none;
    z-index: 50;
  }}
</style>
</head>
<body>

<div class="legend">
  <div class="legend-item"><span class="sym-male">■ ♂</span> Male</div>
  <div class="legend-item"><span class="sym-female">● ♀</span> Female</div>
  <div class="legend-item"><span class="sym-other">◆ ◇</span> Other</div>
  <div class="legend-item"><span class="sym-deceased">†</span> Deceased</div>
  <div class="legend-item"><span style="color:#F59E0B;">═💍═</span> Union</div>
</div>

<div class="toolbar">
  <button class="tool-btn" id="btn-fit" title="Fit to Screen">⛶ Fit Screen</button>
  <button class="tool-btn" id="btn-reset" title="Reset Zoom">↺ Reset</button>
  <button class="tool-btn" id="btn-svg" title="Download Vector SVG">📄 SVG</button>
  <button class="tool-btn" id="btn-png" title="Download High-Res Image">📸 PNG</button>
</div>

<div class="info-tooltip">
  💡 Click any card to select • Scroll to zoom • Drag to pan
</div>

<div id="canvas-container"></div>

<script>
  const treeData = {tree_json_str};
  const genMap = {gen_map_str};
  const descCounts = {desc_counts_str};
  const selectedId = {selected_id_str};
  const searchQuery = {search_query_str}.toLowerCase();

  const members = treeData.members || {{}};
  const rootId = treeData.root_id;

  const CARD_WIDTH = 210;
  const CARD_HEIGHT = 92;
  const X_GAP = 40;
  const Y_GAP = 90;

  // Build hierarchical layout starting from roots
  const svgWidth = window.innerWidth || 1000;
  const svgHeight = {height};

  const svg = d3.select("#canvas-container")
    .append("svg")
    .attr("width", "100%")
    .attr("height", "100%")
    .attr("id", "tree-svg");

  // Defs for gradients & patterns
  const defs = svg.append("defs");
  
  // Diagonal strike pattern for deceased
  const pattern = defs.append("pattern")
    .attr("id", "deceased-stripe")
    .attr("width", 8)
    .attr("height", 8)
    .attr("patternUnits", "userSpaceOnUse")
    .attr("patternTransform", "rotate(45)");
  pattern.append("line")
    .attr("x1", 0).attr("y1", 0).attr("x2", 0).attr("y2", 8)
    .attr("stroke", "#475569").attr("stroke-width", 1.5).attr("opacity", 0.4);

  const mainGroup = svg.append("g").attr("id", "main-group");

  // Zoom behavior
  const zoom = d3.zoom()
    .scaleExtent([0.15, 3])
    .on("zoom", (event) => {{
      mainGroup.attr("transform", event.transform);
    }});

  svg.call(zoom);

  // Position nodes by generations
  const nodes = [];
  const links = [];
  const spouseLinks = [];

  // Group by generation level
  const genGroups = {{}};
  for (const [mid, m] of Object.entries(members)) {{
    const gen = genMap[mid] || 1;
    if (!genGroups[gen]) genGroups[gen] = [];
    genGroups[gen].push(m);
  }}

  // Assign Coordinates:
  // Order generations vertically
  const maxGen = Math.max(...Object.keys(genGroups).map(Number), 1);
  const placed = new Set();
  const nodePositions = {{}};

  // Recursive or structured placement
  // Position by families starting from root
  function positionSubtree(memberId, startX, genLevel, visited = new Set()) {{
    if (!memberId || visited.has(memberId) || !members[memberId]) return startX;
    visited.add(memberId);

    const m = members[memberId];
    let curX = startX;

    // Place primary member
    nodePositions[memberId] = {{ x: curX, y: (genLevel - 1) * (CARD_HEIGHT + Y_GAP) + 60 }};
    placed.add(memberId);
    curX += CARD_WIDTH + X_GAP;

    // Place Spouses immediately next to them
    if (m.spouses && m.spouses.length > 0) {{
      m.spouses.forEach(spId => {{
        if (!placed.has(spId) && members[spId]) {{
          placed.add(spId);
          visited.add(spId);
          nodePositions[spId] = {{ x: curX, y: (genLevel - 1) * (CARD_HEIGHT + Y_GAP) + 60 }};
          spouseLinks.push({{ source: memberId, target: spId }});
          curX += CARD_WIDTH + X_GAP;
        }} else if (placed.has(spId)) {{
          spouseLinks.push({{ source: memberId, target: spId }});
        }}
      }});
    }}

    // Position children unless collapsed
    if (!m.is_collapsed && m.children && m.children.length > 0) {{
      let childStartX = nodePositions[memberId].x - ((m.children.length - 1) * (CARD_WIDTH + X_GAP)) / 4;
      m.children.forEach(chId => {{
        if (!placed.has(chId)) {{
          childStartX = positionSubtree(chId, childStartX, genLevel + 1, visited);
          links.push({{ source: memberId, target: chId }});
        }}
      }});
    }}

    return curX;
  }}

  // Find root members
  let initialX = 80;
  const roots = Object.values(members).filter(m => (!m.parents || m.parents.length === 0));
  const startingRoots = roots.length > 0 ? roots : Object.values(members);

  startingRoots.forEach(r => {{
    if (!placed.has(r.id)) {{
      initialX = positionSubtree(r.id, initialX, genMap[r.id] || 1) + X_GAP * 2;
    }}
  }});

  // Catch any orphan or unlinked members
  Object.values(members).forEach(m => {{
    if (!placed.has(m.id)) {{
      const gen = genMap[m.id] || 1;
      nodePositions[m.id] = {{ x: initialX, y: (gen - 1) * (CARD_HEIGHT + Y_GAP) + 60 }};
      placed.add(m.id);
      initialX += CARD_WIDTH + X_GAP;
    }}
  }});

  // RENDER SPOUSE LINKS (Horizontal marriage line)
  const linksGroup = mainGroup.append("g").attr("class", "links-layer");

  spouseLinks.forEach(sl => {{
    const sPos = nodePositions[sl.source];
    const tPos = nodePositions[sl.target];
    if (sPos && tPos) {{
      const x1 = sPos.x < tPos.x ? sPos.x + CARD_WIDTH : sPos.x;
      const x2 = sPos.x < tPos.x ? tPos.x : tPos.x + CARD_WIDTH;
      const y = sPos.y + CARD_HEIGHT / 2;

      linksGroup.append("line")
        .attr("class", "link-marriage")
        .attr("x1", x1)
        .attr("y1", y)
        .attr("x2", x2)
        .attr("y2", y);

      // Union ring badge icon
      const midX = (x1 + x2) / 2;
      linksGroup.append("text")
        .attr("x", midX)
        .attr("y", y - 6)
        .attr("text-anchor", "middle")
        .attr("font-size", "12px")
        .text("💍");
    }}
  }});

  // RENDER DESCENT LINKS (Orthogonal fork to children)
  links.forEach(l => {{
    const pPos = nodePositions[l.source];
    const cPos = nodePositions[l.target];
    if (pPos && cPos) {{
      const startX = pPos.x + CARD_WIDTH / 2;
      const startY = pPos.y + CARD_HEIGHT;
      const endX = cPos.x + CARD_WIDTH / 2;
      const endY = cPos.y;
      const midY = startY + (endY - startY) / 2;

      const pathData = `M ${{startX}} ${{startY}} V ${{midY}} H ${{endX}} V ${{endY}}`;
      linksGroup.append("path")
        .attr("class", "link-descent")
        .attr("d", pathData);
    }}
  }});

  // RENDER MEMBER CARDS
  const nodesGroup = mainGroup.append("g").attr("class", "nodes-layer");

  Object.values(members).forEach(m => {{
    const pos = nodePositions[m.id];
    if (!pos) return;

    const isSel = (m.id === selectedId);
    const matchesSearch = searchQuery && (
      (m.first_name || "").toLowerCase().includes(searchQuery) ||
      (m.last_name || "").toLowerCase().includes(searchQuery) ||
      (m.nickname || "").toLowerCase().includes(searchQuery)
    );

    const card = nodesGroup.append("g")
      .attr("class", `node-card card-${{m.gender === 'M' ? 'male' : (m.gender === 'F' ? 'female' : 'other')}} ${{!m.is_living ? 'card-deceased' : ''}} ${{isSel ? 'node-selected' : ''}} ${{matchesSearch ? 'node-searched' : ''}}`)
      .attr("transform", `translate(${{pos.x}}, ${{pos.y}})`)
      .on("click", () => {{
        // Notify parent or copy ID
        navigator.clipboard.writeText(m.id).catch(() => {{}});
      }});

    // Background Card
    card.append("rect")
      .attr("class", "card-bg")
      .attr("width", CARD_WIDTH)
      .attr("height", CARD_HEIGHT);

    // Deceased overlay pattern if deceased
    if (!m.is_living) {{
      card.append("rect")
        .attr("width", CARD_WIDTH)
        .attr("height", CARD_HEIGHT)
        .attr("rx", 10).attr("ry", 10)
        .attr("fill", "url(#deceased-stripe)");
    }}

    // Header strip
    const headerColor = m.gender === 'M' ? '#2563EB' : (m.gender === 'F' ? '#DB2777' : '#9333EA');
    card.append("path")
      .attr("d", `M 0 10 A 10 10 0 0 1 10 0 H ${{CARD_WIDTH - 10}} A 10 10 0 0 1 ${{CARD_WIDTH}} 10 V 26 H 0 Z`)
      .attr("fill", headerColor)
      .attr("opacity", m.is_living ? 0.95 : 0.6);

    // Universal Symbol Icon (Square / Circle / Diamond + Glyph)
    const symGlyph = m.gender === 'M' ? '■ ♂' : (m.gender === 'F' ? '● ♀' : '◆ ⚧');
    card.append("text")
      .attr("x", 10)
      .attr("y", 17)
      .attr("fill", "#FFFFFF")
      .attr("font-size", "11px")
      .attr("font-weight", "700")
      .text(symGlyph);

    // Surname / Lineage badge on top right
    if (m.last_name) {{
      card.append("text")
        .attr("x", CARD_WIDTH - 10)
        .attr("y", 17)
        .attr("text-anchor", "end")
        .attr("fill", "#E2E8F0")
        .attr("font-size", "10px")
        .attr("font-weight", "600")
        .text(m.last_name.toUpperCase());
    }}

    // Full Name
    const fullName = `${{m.first_name || ''}} ${{m.nickname ? '\"' + m.nickname + '\" ' : ''}}${{m.last_name || ''}}`.trim() || "Unknown";
    card.append("text")
      .attr("x", 12)
      .attr("y", 46)
      .attr("fill", "#F8FAFC")
      .attr("font-size", "13px")
      .attr("font-weight", "600")
      .text(fullName.length > 22 ? fullName.slice(0, 20) + "..." : fullName);

    // Lifespan & Status
    const b = m.birth_date || "?";
    let lifespanText = m.is_living ? `b. ${{b}} (Living)` : `${{b}} — †${{m.death_date || '?'}}`;
    card.append("text")
      .attr("x", 12)
      .attr("y", 65)
      .attr("fill", m.is_living ? "#38BDF8" : "#94A3B8")
      .attr("font-size", "11px")
      .text(lifespanText);

    // Generational badge
    const genNum = genMap[m.id] || 1;
    card.append("rect")
      .attr("x", 12)
      .attr("y", 72)
      .attr("width", 42)
      .attr("height", 14)
      .attr("rx", 3).attr("ry", 3)
      .attr("fill", "#334155");

    card.append("text")
      .attr("x", 33)
      .attr("y", 82)
      .attr("text-anchor", "middle")
      .attr("fill", "#94A3B8")
      .attr("font-size", "9px")
      .attr("font-weight", "600")
      .text(`GEN ${{genNum}}`);

    // Retractable / Collapsed badge indicator
    const dCount = descCounts[m.id] || 0;
    if (m.is_collapsed && dCount > 0) {{
      const pill = nodesGroup.append("g")
        .attr("class", "retracted-pill")
        .attr("transform", `translate(${{pos.x + 10}}, ${{pos.y + CARD_HEIGHT + 14}})`);

      pill.append("rect")
        .attr("width", CARD_WIDTH - 20)
        .attr("height", 26);

      pill.append("text")
        .attr("x", (CARD_WIDTH - 20) / 2)
        .attr("y", 17)
        .attr("text-anchor", "middle")
        .attr("fill", "#E0E7FF")
        .attr("font-size", "10px")
        .attr("font-weight", "600")
        .text(`▶ Lineage of ${{m.last_name || 'Branch'}} (${{dCount}})`);
    }}
  }});

  // Toolbar Actions
  function fitView() {{
    const bbox = mainGroup.node().getBBox();
    if (!bbox || bbox.width === 0 || bbox.height === 0) return;
    const padding = 60;
    const fullW = bbox.width + padding * 2;
    const fullH = bbox.height + padding * 2;
    const scale = Math.min(svgWidth / fullW, svgHeight / fullH, 1.2);
    const tx = (svgWidth - bbox.width * scale) / 2 - bbox.x * scale;
    const ty = (svgHeight - bbox.height * scale) / 2 - bbox.y * scale;

    svg.transition().duration(750).call(
      zoom.transform,
      d3.zoomIdentity.translate(tx, ty).scale(scale)
    );
  }}

  // Auto-fit on initial render
  setTimeout(fitView, 100);

  document.getElementById("btn-fit").addEventListener("click", fitView);
  document.getElementById("btn-reset").addEventListener("click", () => {{
    svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity.translate(40, 40).scale(0.9));
  }});

  // SVG Vector Download
  document.getElementById("btn-svg").addEventListener("click", () => {{
    const svgEl = document.getElementById("tree-svg");
    const serializer = new XMLSerializer();
    let source = serializer.serializeToString(svgEl);
    if (!source.match(/^<svg[^>]+xmlns="http:\\/\\/www\\.w3\\.org\\/2000\\/svg"/)) {{
      source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
    }}
    const blob = new Blob([source], {{ type: "image/svg+xml;charset=utf-8" }});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "family_tree.svg";
    a.click();
    URL.revokeObjectURL(url);
  }});

  // High-Res PNG Download via Canvas
  document.getElementById("btn-png").addEventListener("click", () => {{
    const svgEl = document.getElementById("tree-svg");
    const serializer = new XMLSerializer();
    const svgString = serializer.serializeToString(svgEl);
    const img = new Image();
    const svgBlob = new Blob([svgString], {{ type: "image/svg+xml;charset=utf-8" }});
    const url = URL.createObjectURL(svgBlob);

    img.onload = () => {{
      const canvas = document.createElement("canvas");
      canvas.width = svgWidth * 2;
      canvas.height = svgHeight * 2;
      const ctx = canvas.getContext("2d");
      ctx.scale(2, 2);
      ctx.fillStyle = "#0F172A";
      ctx.fillRect(0, 0, svgWidth, svgHeight);
      ctx.drawImage(img, 0, 0);
      URL.revokeObjectURL(url);

      const pngUrl = canvas.toDataURL("image/png");
      const a = document.createElement("a");
      a.href = pngUrl;
      a.download = "family_tree_chart.png";
      a.click();
    }};
    img.src = url;
  }});
</script>
</body>
</html>
"""
    return html_content
