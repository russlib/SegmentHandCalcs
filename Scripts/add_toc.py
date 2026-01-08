import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

toc_content = [
    "## Table of Contents\n",
    "1. [1. Constants and Geometry](#1.-Constants-and-Geometry)\n",
    "2. [2. Load Cases & Bending Stress](#2.-Load-Cases-&-Bending-Stress)\n",
    "3. [3. Fasteners: Tension, Shear, and Bearing](#3.-Fasteners:-Tension,-Shear,-and-Bearing)\n",
    "4. [4. Bond Strength Analysis](#4.-Bond-Strength-Analysis)\n",
    "5. [5. Euler-Johnson Buckling Analysis](#5.-Euler-Johnson-Buckling-Analysis)\n",
    "6. [6. Summary Results Table](#6.-Summary-Results-Table)"
]

toc_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": toc_content
}

# Insert TOC after the title cell (Cell 0)
nb['cells'].insert(1, toc_cell)

with open('FSAESegmentHandCalcs.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
