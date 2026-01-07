import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

# 1. Identify and Remove Tab Bending cells
# Based on previous verification:
# Cell 9 is Markdown: ## 3. Tab Bending Analysis
# Cell 10 is Code: # 3.1 Geometry for Tab Analysis
# We'll use more robust matching to be sure.

new_cells = []
skip_next = False
for i, cell in enumerate(nb['cells']):
    source_str = "".join(cell['source'])
    if '## 3. Tab Bending Analysis' in source_str:
        # Skip this cell and the next one (code cell)
        skip_next = True
        continue
    if skip_next:
        skip_next = False
        continue
    new_cells.append(cell)

nb['cells'] = new_cells

# 2. Renumber Markdown Headers
header_map = {
    "## 4. Fasteners": "## 3. Fasteners",
    "## 5. Bond Strength": "## 4. Bond Strength",
    "## 6. Euler-Johnson Buckling": "## 5. Euler-Johnson Buckling",
    "## 7. Passive Thermal Properties": "## 6. Passive Thermal Properties",
    "## 8. Summary Results Table": "## 7. Summary Results Table"
}

for cell in nb['cells']:
    if cell['cell_type'] == 'markdown':
        source = "".join(cell['source'])
        for old, new in header_map.items():
            if source.startswith(old):
                cell['source'] = [new + source[len(old):]]

# 3. Renumber Code Comments
numbering_fixes = {
    "# 4.1 Bolt Geometry": "# 3.1 Bolt Geometry",
    "# 4.2 SF Calculations": "# 3.2 SF Calculations",
    "# 4.3 Bearing Stress": "# 3.3 Bearing Stress",
    "# 4.4 Bolt Shear SF": "# 3.4 Bolt Shear SF",
    "# 4.5 Tear-out Strength": "# 3.5 Tear-out Strength",
    "# 5.1 Bond Strength": "# 4.1 Bond Strength",
    "# 5.2 Bond Areas": "# 4.2 Bond Areas",
    "# 6.1 Global Moment of Inertia": "# 5.1 Global Moment of Inertia",
    "# 6.2 Slenderness and Buckling": "# 5.2 Slenderness and Buckling",
    "# 7.1 Surface Area": "# 6.1 Surface Area"
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

# 4. Update Summary Table Code (remove sf_tab_bending)
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'summary_data = {' in "".join(cell['source']):
        source_str = "".join(cell['source'])
        # Remove "Tab Bending" from list and sf_tab_bending from list
        source_str = source_str.replace('"Tab Bending", ', '')
        source_str = source_str.replace('sf_tab_bending, ', '')
        # Convert back to list of lines (roughly)
        cell['source'] = [line + '\n' for line in source_str.split('\n')]
        # Ensure last line doesn't have double newline if it ended with one
        if cell['source'][-1] == '\n':
            cell['source'].pop()

# 5. Update Table of Contents
new_toc = [
    "## Table of Contents\n",
    "1. [1. Constants and Geometry](#1.-Constants-and-Geometry)\n",
    "2. [2. Load Cases & Bending Stress](#2.-Load-Cases-&-Bending-Stress)\n",
    "3. [3. Fasteners: Tension, Shear, and Bearing](#3.-Fasteners:-Tension,-Shear,-and-Bearing)\n",
    "4. [4. Bond Strength Analysis](#4.-Bond-Strength-Analysis)\n",
    "5. [5. Euler-Johnson Buckling Analysis](#5.-Euler-Johnson-Buckling-Analysis)\n",
    "6. [6. Summary Results Table](#6.-Summary-Results-Table)\n",
    "7. [7. Passive Thermal Properties](#7.-Passive-Thermal-Properties)\n",
    "8. [Sources Referenced](#Sources-Referenced)"
]
# Wait, let's check the renumbered order:
# 1. Constants
# 2. Load Cases
# 3. Fasteners
# 4. Bond Strength
# 5. Buckling
# 6. Thermal
# 7. Summary
# 8. Sources

new_toc = [
    "## Table of Contents\n",
    "1. [1. Constants and Geometry](#1.-Constants-and-Geometry)\n",
    "2. [2. Load Cases & Bending Stress](#2.-Load-Cases-&-Bending-Stress)\n",
    "3. [3. Fasteners: Tension, Shear, and Bearing](#3.-Fasteners:-Tension,-Shear,-and-Bearing)\n",
    "4. [4. Bond Strength Analysis](#4.-Bond-Strength-Analysis)\n",
    "5. [5. Euler-Johnson Buckling Analysis](#5.-Euler-Johnson-Buckling-Analysis)\n",
    "6. [6. Passive Thermal Properties](#6.-Passive-Thermal-Properties)\n",
    "7. [7. Summary Results Table](#7.-Summary-Results-Table)\n",
    "8. [Sources Referenced](#Sources-Referenced)"
]

for cell in nb['cells']:
    if cell['cell_type'] == 'markdown' and '## Table of Contents' in "".join(cell['source']):
        cell['source'] = new_toc

with open('FSAESegmentHandCalcs.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
