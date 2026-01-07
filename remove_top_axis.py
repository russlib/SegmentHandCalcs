import json

with open('BeamAnalysisTool.ipynb', 'r') as f:
    nb = json.load(f)

def move_fbd_axis_to_bottom(source):
    new_source = []
    for line in source:
        # Remove top axis specific lines
        if "ax.tick_params(labeltop=True)" in line:
            continue
        if "ax.xaxis.set_label_position('top')" in line:
            continue
        if "ax.xaxis.tick_top()" in line:
            continue
        # Reduce title padding since axis is no longer at the top
        if "ax.set_title" in line and "pad=40" in line:
            new_source.append(line.replace("pad=40", "pad=20"))
        else:
            new_source.append(line)
    return new_source

nb['cells'][2]['source'] = move_fbd_axis_to_bottom(nb['cells'][2]['source'])
nb['cells'][4]['source'] = move_fbd_axis_to_bottom(nb['cells'][4]['source'])

with open('BeamAnalysisTool.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
