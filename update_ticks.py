import json

with open('BeamAnalysisTool.ipynb', 'r') as f:
    nb = json.load(f)

# Helper to generate the tick marks
# We want 10 increments (11 tick marks) plus the special location 'a'
def get_tick_code(is_fbd=False):
    if is_fbd:
        return [
            "    # Set 10 regular increments + the special location 'a'\n",
            "    standard_ticks = np.linspace(0, l, 11)\n",
            "    all_ticks = np.unique(np.sort(np.append(standard_ticks, a)))\n",
            "    ax.set_xticks(all_ticks)\n"
        ]
    else:
        return [
            "    standard_ticks = np.linspace(0, l, 11)\n",
            "    ax.set_xticks(standard_ticks)\n"
        ]

# --- CASE (A) UPDATES ---
# The code is in nb['cells'][2]['source']
source_a = nb['cells'][2]['source']
new_source_a = []
for line in source_a:
    if "ax.set_xticks([0, a, l])" in line:
        new_source_a.append("    standard_ticks = np.linspace(0, l, 11)\n")
        new_source_a.append("    all_ticks = np.unique(np.sort(np.append(standard_ticks, a)))\n")
        new_source_a.append("    ax.set_xticks(all_ticks)\n")
    elif "axs[4].grid(True, alpha=0.3); axs[4].axhline(0, color='k', lw=1); axs[4].set_xlabel('Position x (m)')" in line:
        # Before the last plot shows up, we need to set ticks for all lower plots
        new_source_a.append(line)
        new_source_a.append("\n    # Set regular 10 increments for all physical diagrams\n")
        new_source_a.append("    for ax in axs[1:]: ax.set_xticks(np.linspace(0, l, 11))\n")
    else:
        new_source_a.append(line)
nb['cells'][2]['source'] = new_source_a

# --- CASE (B) UPDATES ---
# The code is in nb['cells'][4]['source']
source_b = nb['cells'][4]['source']
new_source_b = []
for line in source_b:
    if "ax.set_xticks([0, a, l])" in line:
        new_source_b.append("    standard_ticks = np.linspace(0, l, 11)\n")
        new_source_b.append("    all_ticks = np.unique(np.sort(np.append(standard_ticks, a)))\n")
        new_source_b.append("    ax.set_xticks(all_ticks)\n")
    elif "axs[4].grid(True, alpha=0.3); axs[4].axhline(0, color='k', lw=1); axs[4].set_xlabel('Position x (m)')" in line:
        new_source_b.append(line)
        new_source_b.append("\n    # Set regular 10 increments for all physical diagrams\n")
        new_source_b.append("    for ax in axs[1:]: ax.set_xticks(np.linspace(0, l, 11))\n")
    else:
        new_source_b.append(line)
nb['cells'][4]['source'] = new_source_b

with open('BeamAnalysisTool.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
