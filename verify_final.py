import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

print(f"Total cells: {len(nb['cells'])}")
for i, cell in enumerate(nb['cells']):
    source = "".join(cell['source']) if isinstance(cell['source'], list) else cell['source']
    first_line = source.split('\n')[0] if source else "EMPTY"
    if cell['cell_type'] == 'markdown' and first_line.startswith('##'):
        print(f"Cell {i} ({cell['cell_type']}): {first_line}")
    elif i == 1: # ToC
         print(f"Cell {i} (ToC): {first_line}")

# Check summary table code
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'summary_data =' in "".join(cell['source']):
        print("\nSummary Table Code:")
        print("".join(cell['source']))
