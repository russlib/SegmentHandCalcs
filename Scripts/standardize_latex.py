import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

# Cell 7: Load Cases & Bending Stress
nb['cells'][7]['source'] = [
    "## 2. Load Cases & Bending Stress - Polycarbonate Lid\n",
    "Calculated for 20g vertical and 40g lateral loads.\n",
    "\n",
    "Assuming a uniformly distributed load where total force $F$ is related to the distributed load $w$ by $F = w \\cdot L$:\n",
    "\n",
    "**Maximum Bending Moment:**\n",
    "$$ M_{max} = \\frac{w L^2}{8} = \\frac{F \\cdot L}{8} $$\n",
    "\n",
    "**Bending Stress:**\n",
    "$$ \\sigma = \\frac{M \\cdot c}{I} $$\n",
    "\n",
    "**Maximum Deflection ($\\delta_{max}$):**\n",
    "$$ \\delta_{max} = \\frac{5 w L^4}{384 E I} = \\frac{5 F \\cdot L^3}{384 E I} $$"
]

# Cell 10: Tensile Stress Area
nb['cells'][10]['source'] = [
    "### Tensile Stress Area\n",
    "\n",
    "If a threaded rod is subjected to pure tensile loading, its strength is defined by the average of the minor and pitch diameters. The **tensile-stress area**, $A_t$, is defined as:\n",
    "\n",
    "$$ A_t = \\frac{\\pi}{4} \\left( \\frac{d_p + d_r}{2} \\right)^2 \\tag{15.1a} $$\n",
    "\n",
    "**For ISO metric threads:**\n",
    "$$ d_p = d - 0.649519p, \\quad d_r = d - 1.226869p \\tag{15.1c} $$\n",
    "\n",
    "**Where:**\n",
    "- $d$ = major/outside diameter (mm)\n",
    "- $p$ = thread pitch (mm)\n",
    "\n",
    "**Axial Tensile Stress:**\n",
    "$$ \\sigma_t = \\frac{F}{A_t} \\tag{15.2} $$\n",
    "\n",
    "> *Ref: Norton, R. L. (2020). Machine Design: An Integrated Approach. 6th ed., p. 907.*"
]

# Cell 15: Euler-Johnson Buckling
nb['cells'][15]['source'] = [
    "### Euler-Johnson Buckling Criteria ($SR = L/k$)\n",
    "\n",
    "**Critical Slenderness and Radius of Gyration:**\n",
    "$$ C_c = \\pi \\sqrt{\\frac{2E}{\\sigma_y}}, \\quad k = \\sqrt{\\frac{I_{xx}}{A}} $$\n",
    "\n",
    "**Johnson (Inelastic) Buckling if $SR < C_c$:**\n",
    "$$ P_{cr} = A \\left[ \\sigma_y - \\frac{1}{E} \\left( \\frac{\\sigma_y SR}{2\\pi} \\right)^2 \\right] $$\n",
    "\n",
    "**Euler (Elastic) Buckling if $SR \\ge C_c$:**\n",
    "$$ P_{cr} = \\frac{\\pi^2 E I_{xx}}{L^2} $$\n",
    "\n",
    "**Safety Factor:**\n",
    "$$ SF = \\frac{P_{cr}}{F_{applied}} $$\n",
    "\n",
    "> *(Ref: Norton, Machine Design, 6th Ed., p. 231)*"
]

with open('FSAESegmentHandCalcs.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
