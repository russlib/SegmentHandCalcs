import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

# Fix double "Table" in header
for cell in nb['cells']:
    if cell['cell_type'] == 'markdown' and '## 8. Summary Results Table Table' in "".join(cell['source']):
        cell['source'] = ["## 8. Summary Results Table"]

# Fix numbering in code comments
numbering_fixes = {
    "# 3.1 Bolt Geometry": "# 4.1 Bolt Geometry",
    "# 3.2 SF Calculations": "# 4.2 SF Calculations",
    "# 3.3 Bearing Stress": "# 4.3 Bearing Stress",
    "# 3.4 Bolt Shear SF": "# 4.4 Bolt Shear SF",
    "# 3.5 Tear-out Strength": "# 4.5 Tear-out Strength",
    "# 4.1 Bond Strength": "# 5.1 Bond Strength",
    "# 4.2 Bond Areas": "# 5.2 Bond Areas"
}

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        new_source = []
        for line in cell['source']:
            updated_line = line
            for old, new in numbering_fixes.items():
                if old in line:
                    updated_line = line.replace(old, new)
                    break
            new_source.append(updated_line)
        cell['source'] = new_source

with open('FSAESegmentHandCalcs.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
