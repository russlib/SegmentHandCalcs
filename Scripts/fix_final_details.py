import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

# Fix summary table minimum required list length (7 instead of 8)
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'summary_data =' in "".join(cell['source']):
        source_str = "".join(cell['source'])
        source_str = source_str.replace('[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]', '[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]')
        cell['source'] = [line + '\n' for line in source_str.split('\n')]
        if cell['source'][-1] == '\n':
            cell['source'].pop()

# Update ToC with correct headers
new_toc = [
    "## Table of Contents\n",
    "1. [1. Constants and Geometry](#1.-Constants-and-Geometry)\n",
    "2. [2. Load Cases & Bending Stress](#2.-Load-Cases-&-Bending-Stress---Polycarbonate-Lid)\n",
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
