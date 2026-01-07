import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

tensile_area_latex = [
    "### Tensile Stress Area\n",
    "\n",
    "If a threaded rod is subjected to pure tensile loading, its strength is defined by the average of the minor and pitch diameters. The **tensile-stress area**, $A_t$, is defined as:\n",
    "\n",
    "$$ A_t = \\frac{\\pi}{4} \\left( \\frac{d_p + d_r}{2} \\right)^2 $$\n",
    "\n",
    "Where, for ISO metric threads:\n",
    "- $d_p = d - 0.649519p$ (Pitch diameter)\n",
    "- $d_r = d - 1.226869p$ (Minor/Root diameter)\n",
    "- $d$ = major diameter (mm)\n",
    "- $p$ = thread pitch (mm)\n",
    "\n",
    "The axial tensile stress $\\sigma_t$ due to load $F$ is:\n",
    "$$ \\sigma_t = \\frac{F}{A_t} $$\n",
    "\n",
    "> *Ref: Norton, R. L. (2020). Machine Design: An Integrated Approach. 6th ed., p. 907.*"
]

# Find the Fasteners section header
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown' and '## 3. Fasteners' in "".join(cell['source']):
        # Insert the LaTeX explanation after the header
        nb['cells'].insert(i + 1, {
            "cell_type": "markdown",
            "metadata": {},
            "source": tensile_area_latex
        })
        break

with open('FSAESegmentHandCalcs.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
