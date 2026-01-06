import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

print(f"Total cells: {len(nb['cells'])}")
for i, cell in enumerate(nb['cells']):
    source = "".join(cell['source']) if isinstance(cell['source'], list) else cell['source']
    first_line = source.split('\n')[0] if source else "EMPTY"
    print(f"Cell {i} ({cell['cell_type']}): {first_line[:50]}")
