import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

buckling_latex = [
    "### Euler-Johnson Buckling Criteria\n",
    "\n",
    "We determine the critical buckling force $P_{cr}$ by comparing the slenderness ratio $SR = L/k$ to the critical slenderness constant $C_c$:\n",
    "\n",
    "$$ I_{xx} = \\sum I_{parts}, \\quad k = \\sqrt{\\frac{I_{xx}}{A}}, \\quad SR = \\frac{L}{k}, \\quad C_c = \\pi \\sqrt{\\frac{2E}{\\sigma_y}} $$\n",
    "\n",
    "**Johnson (Inelastic) if $SR < C_c$:**\n",
    "$$ P_{cr} = A \\left[ \\sigma_y - \\frac{1}{E} \\left( \\frac{\\sigma_y SR}{2\\pi} \\right)^2 \\right] $$\n",
    "\n",
    "**Euler (Elastic) if $SR \\ge C_c$:**\n",
    "$$ P_{cr} = \\frac{\\pi^2 E I_{xx}}{L^2} $$\n",
    "\n",
    "**Safety Factor:**\n",
    "$$ SF_{buckling} = \\frac{P_{cr}}{F_{applied}} $$"
]

# Find the buckling header to insert after
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown' and '## 5. Euler-Johnson Buckling' in "".join(cell['source']):
        nb['cells'].insert(i + 1, {
            "cell_type": "markdown",
            "metadata": {},
            "source": buckling_latex
        })
        break

with open('FSAESegmentHandCalcs.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
