#!/usr/bin/env python3
"""metro_map.py - Draw colored simplified Delhi Metro schematic using data/stations.csv and data/lines.csv"""
import os, csv
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
STATIONS_CSV = DATA_DIR / "stations.csv"
LINES_CSV = DATA_DIR / "lines.csv"
OUT_PNG = BASE_DIR / "delhi_metro_map_colored.png"

LINE_COLORS = {
    "Blue": "#0078C8",
    "Yellow": "#FFD700",
    "Violet": "#800080",
    "Magenta": "#FF0090",
    "Pink": "#FFC0CB",
    "Red": "#FF0000",
    "Green": "#008000",
    "Grey": "#808080"
}

# Load stations
stations = {}
with open(STATIONS_CSV, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    # find column names for id and name (tolerant)
    cols = reader.fieldnames
    id_col = 'station_id' if 'station_id' in cols else cols[0]
    name_col = 'station_name' if 'station_name' in cols else cols[1] if len(cols)>1 else cols[0]
    for r in reader:
        stations[r[id_col]] = r[name_col]

# Load lines
lines = []
with open(LINES_CSV, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    cols = reader.fieldnames
    id_col = 'line_id' if 'line_id' in cols else cols[0]
    name_col = 'line_name' if 'line_name' in cols else cols[1] if len(cols)>1 else cols[0]
    station_ids_col = 'station_ids' if 'station_ids' in cols else cols[-1]
    for r in reader:
        station_ids = [x.strip() for x in r.get(station_ids_col,'').split(',') if x.strip()]
        lines.append((r.get(name_col,''), station_ids))

G = nx.Graph()
for sid, name in stations.items():
    G.add_node(sid, label=name)

# compute layout
pos = nx.spring_layout(G, seed=42, k=0.6)
plt.figure(figsize=(12,10))

# draw each line
legend_entries = []
for line_name, station_ids in lines:
    color = LINE_COLORS.get(line_name, '#999999')
    edges = [(station_ids[i], station_ids[i+1]) for i in range(len(station_ids)-1)]
    # draw edges and nodes
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=3, edge_color=color)
    nx.draw_networkx_nodes(G, pos, nodelist=station_ids, node_size=300, node_color=color)
    if line_name:
        legend_entries.append((line_name, color))

# labels
labels = {sid: name for sid, name in stations.items()}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=7)

# legend
from matplotlib.lines import Line2D
handles = [Line2D([0],[0], color=c, lw=6) for _,c in legend_entries]
labels = [n for n,_ in legend_entries]
plt.legend(handles, labels, title='Lines', loc='upper right')
plt.axis('off')
plt.title('Delhi Metro - Simplified Colored Schematic')
plt.tight_layout()
plt.savefig(OUT_PNG, dpi=200)
print('Saved map to', OUT_PNG)
