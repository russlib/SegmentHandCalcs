import json

with open('BeamAnalysisTool.ipynb', 'r') as f:
    nb = json.load(f)

# Helper to fix indentation in a cell's source
def fix_indent(source):
    new_source = []
    for line in source:
        # Remove exactly 4 leading spaces from the lines I broke
        if line.startswith("    standard_ticks = np.linspace(0, l, 11)"):
            new_source.append(line.lstrip())
        elif line.startswith("    all_ticks = np.unique"):
            new_source.append(line.lstrip())
        elif line.startswith("    ax.set_xticks(all_ticks)"):
            new_source.append(line.lstrip())
        elif line.startswith("    # Set regular 10 increments"):
            new_source.append(line.lstrip())
        elif line.startswith("    for ax in axs[1:]"):
            new_source.append(line.lstrip())
        else:
            new_source.append(line)
    return new_source

# Fix Case (a) and Case (b) code cells
nb['cells'][2]['source'] = fix_indent(nb['cells'][2]['source'])
nb['cells'][4]['source'] = fix_indent(nb['cells'][4]['source'])

with open('BeamAnalysisTool.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
