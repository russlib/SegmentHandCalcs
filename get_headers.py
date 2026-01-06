import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        source = "".join(cell['source'])
        lines = source.split('\n')
        for line in lines:
            if line.strip().startswith('#'):
                print(f"Cell {i}: {line.strip()}")
