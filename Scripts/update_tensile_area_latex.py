import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

tensile_area_latex = [
    "### Tensile Stress Area\n",
    "\n",
    "If a threaded rod is subjected to pure tensile loading, its strength is defined by the average of the minor and pitch diameters. The **tensile-stress area**, $A_t$, is defined as:\n",
    "\n",
    "$$ A_t = \\frac{\\pi}{4} \\left( \\frac{d_p + d_r}{2} \\right)^2 \\tag{15.1a} $$\n",
    "\n",
    "**For UNS threads:**\n",
    "$$ d_p = d - \\frac{0.649519}{N} \\quad d_r = d - \\frac{1.299038}{N} \\tag{15.1b} $$\n",
    "\n",
    "**For ISO metric threads:**\n",
    "$$ d_p = d - 0.649519p \\quad d_r = d - 1.226869p \\tag{15.1c} $$\n",
    "\n",
    "Where:\n",
    "- $d$ = major/outside diameter\n",
    "- $N$ = number of threads per inch\n",
    "- $p$ = thread pitch (mm)\n",
    "\n",
    "The axial tensile stress $\\sigma_t$ due to load $F$ is:\n",
    "$$ \\sigma_t = \\frac{F}{A_t} \\tag{15.2} $$\n",
    "\n",
    "> *Ref: Norton, R. L. (2020). Machine Design: An Integrated Approach. 6th ed., p. 907.*"
]

# Find the cell I just added (it starts with ### Tensile Stress Area)
for cell in nb['cells']:
    if cell['cell_type'] == 'markdown' and '### Tensile Stress Area' in "".join(cell['source']):
        cell['source'] = tensile_area_latex
        break

with open('FSAESegmentHandCalcs.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
