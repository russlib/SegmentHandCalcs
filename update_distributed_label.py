import json

with open('BeamAnalysisTool.ipynb', 'r') as f:
    nb = json.load(f)

# Update Case (b) source code (nb['cells'][4])
source_b = nb['cells'][4]['source']
new_source_b = []
for line in source_b:
    if "ax.text((a+l)/2, -0.6, f'w={w_load}N/m', color='red', ha='center', fontweight='bold')" in line:
        new_source_b.append(line)
        new_source_b.append("total_w_load = w_load * (l - a)\n")
        new_source_b.append("ax.text((a+l)/2, -0.2, f'{total_w_load:.0f}', color='white', ha='center', va='center', fontweight='bold')\n")
    else:
        new_source_b.append(line)

nb['cells'][4]['source'] = new_source_b

with open('BeamAnalysisTool.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
