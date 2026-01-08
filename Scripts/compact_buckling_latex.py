import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

compact_buckling_latex = [
    "### Euler-Johnson Buckling ($SR = L/k$)\n",
    "$$ C_c = \\pi \\sqrt{\\frac{2E}{\\sigma_y}}, \\quad k = \\sqrt{\\frac{I_{xx}}{A}} $$\n",
    "\n",
    "**Johnson ($SR < C_c$):** $P_{cr} = A \\left[ \\sigma_y - \\frac{1}{E} \\left( \\frac{\\sigma_y SR}{2\\pi} \\right)^2 \\right]$  \n",
    "**Euler ($SR \\ge C_c$):** $P_{cr} = \\frac{\\pi^2 E I_{xx}}{L^2}$  \n",
    "**Safety Factor:** $SF = P_{cr} / F_{applied}$\n",
    "\n",
    "> *(Ref: Norton, Machine Design, 6th Ed., p. 231)*"
]

# Find the cell starting with ### Euler-Johnson Buckling Criteria or similar
for cell in nb['cells']:
    if cell['cell_type'] == 'markdown' and 'Euler-Johnson Buckling' in "".join(cell['source']):
        # If it's the criteria header we just added, replace it
        if 'determine the critical' in "".join(cell['source']) or 'Criteria' in "".join(cell['source']):
            cell['source'] = compact_buckling_latex
            break

with open('FSAESegmentHandCalcs.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
