import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

# Cell 11 is the Buckling Header - Correct
# Cell 12 should be the Buckling Code
nb['cells'][12]['cell_type'] = 'code'
# Ensure it doesn't have the wrong header
if nb['cells'][12]['source'] and nb['cells'][12]['source'][0].startswith('## 6.'):
    nb['cells'][12]['source'].pop(0)

# Cell 13 should be the Summary Header
nb['cells'][13]['cell_type'] = 'markdown'
nb['cells'][13]['source'] = ["## 6. Summary Results Table"]

# Cell 14 should be the Summary Code
nb['cells'][14]['cell_type'] = 'code'

with open('FSAESegmentHandCalcs.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
