import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

# 1. Update Section 2 to include Longitudinal Force
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and '# 2.1 Vertical Force (20g)' in "".join(cell['source']):
        cell['source'].insert(3, "\n")
        cell['source'].insert(4, "# 2.2 Lateral/Longitudinal Forces (40g)\n")
        cell['source'].insert(5, "side_force = segment_modules_weight * 40 * G\n")
        cell['source'].insert(6, "long_force = segment_modules_weight * 40 * G\n")

# 2. Add Section 3: Tab Bending Analysis
tab_bending_md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 3. Tab Bending Analysis\n",
        "Analyzing the bending stress on the Garolite tabs where they interface with the segment structure."
    ]
}

tab_bending_code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# 3.1 Geometry for Tab Analysis\n",
        "insetlength = 26.75 * MM_TO_M\n",
        "bolttosegmentlength = 14 * MM_TO_M\n",
        "L1 = 14 * MM_TO_M\n",
        "L2 = 40.75 * MM_TO_M\n",
        "\n",
        "# 3.2 Reaction Forces and Moments\n",
        "P1 = -(top_force * L2) / (L2 - L1)\n",
        "P2 = (top_force * L1) / (L2 - L1)\n",
        "Mc = top_force * L2 - P1 * (L2 - L1)\n",
        "Medge = -top_force * L1 + Mc\n",
        "\n",
        "# 3.3 Tab Bending Stress\n",
        "i_tab = (4 * garolite_thickness * (garolite_thickness**3)) / 12\n",
        "stress_bending_tab = (Medge * (garolite_thickness / 2)) / i_tab\n",
        "sf_tab_bending = garolite_strength / stress_bending_tab\n",
        "\n",
        "print(f\"Tab Bending SF: {sf_tab_bending:.4f}\")"
    ]
}

# Insert Section 3 after Section 2's code cell (which is now Cell 7)
nb['cells'].insert(8, tab_bending_md)
nb['cells'].insert(9, tab_bending_code)

# 3. Update Buckling Analysis with Global Ixx
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'i_walls =' in "".join(cell['source']):
        cell['source'] = [
            "# 6.1 Global Moment of Inertia (Ixx) Assembly\n",
            "moment_inertia_walls = 2 * (((ene_segment_width/2 + garolite_thickness/2)**2 * garolite_thickness * ene_seg_height)) + (garolite_thickness**3 * ene_seg_height / 12)\n",
            "moment_inertia_bottom = (garolite_thickness/2 + ene_seg_height/2)**2 * garolite_thickness * ene_segment_width + (garolite_thickness**3 * ene_segment_width / 12)\n",
            "moment_inertia_lid = (garolite_thickness/2 + ene_seg_height/2 + 0.015)**2 * garolite_thickness * ene_segment_width + (garolite_thickness**3 * ene_segment_width / 12)\n",
            "ixx = moment_inertia_walls + moment_inertia_bottom + moment_inertia_lid\n",
            "\n",
            "# 6.2 Slenderness and Buckling Limits\n",
            "radius_of_gyration = math.sqrt(ixx / depth_cross_sec_area)\n",
            "slenderness_ratio = ene_segment_depth / radius_of_gyration\n",
            "critical_slenderness = math.pi * math.sqrt((2 * garolite_modulus) / garolite_strength)\n",
            "\n",
            "if slenderness_ratio < critical_slenderness:\n",
            "    # Johnson Inelastic Buckling\n",
            "    max_force_buckle = depth_cross_sec_area * (garolite_strength - (garolite_strength**2 * slenderness_ratio**2) / (4 * math.pi**2 * garolite_modulus))\n",
            "    mode = \"Johnson\"\n",
            "else:\n",
            "    # Euler Elastic Buckling\n",
            "    max_force_buckle = (math.pi**2 * garolite_modulus * ixx) / (ene_segment_depth**2)\n",
            "    mode = \"Euler\"\n",
            "\n",
            "sf_buckling = max_force_buckle / side_force\n",
            "print(f\"Buckling Mode: {mode}, SF: {sf_buckling:.4f}\")"
        ]

# 4. Add Section 7: Passive Thermal Properties
thermal_md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 7. Passive Thermal Properties\n",
        "Calculating the heat dissipation capacity of the segment casing."
    ]
}

thermal_code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# 7.1 Surface Area and Heat Transfer\n",
        "surface_area = (ene_segment_depth * ene_segment_width * 2) + (ene_seg_height * ene_segment_depth * 2)\n",
        "garolite_conductivity = 0.288 # W/m*K\n",
        "watts_per_kelvin = (1 / garolite_thickness) * garolite_conductivity * surface_area\n",
        "\n",
        "print(f\"Total Segment Surface Area: {surface_area:.4f} m^2\")\n",
        "print(f\"Heat Transfer Rate: {watts_per_kelvin:.4f} W/K\")"
    ]
}

# Summary table is currently near the end. Let's find its position.
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown' and '## 6. Summary Results Table' in "".join(cell['source']):
        summary_header_index = i
        break

nb['cells'].insert(summary_header_index, thermal_md)
nb['cells'].insert(summary_header_index + 1, thermal_code)

# 5. Sources Referenced block at the bottom
sources_md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "---\n",
        "## Sources Referenced\n",
        "1. [Enepaq VTC6 Module Datasheet](https://enepaq.com/wp-content/uploads/2023/09/VTC6-Sony-Murata-Li-ion-Battery-Module-With-Temperature-Sensor-Datasheet-Tesla-Battery-Sponsorship-Formula-SAE-Electric-Formula-Student-Battery-Pack.pdf) - Module dimensions and weight specifications.\n",
        "2. [Laminated Plastics G-10/FR4 Data](https://laminatedplastics.com/g-10.pdf) - Material strengths, bonding data, and tear-out limits.\n",
        "3. [MatWeb Polycarbonate Data](https://www.matweb.com/search/DataSheet.aspx?MatGUID=501acbb63cbc4f748faa7490884cdbca) - Mechanical properties for the module lid.\n",
        "4. **SES 2.10.3.4.b** - Formula SAE load case requirements for battery segments."
    ]
}
nb['cells'].append(sources_md)

# Update Summary Table to include Tab Bending
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'summary_data = {' in "".join(cell['source']):
        cell['source'] = [
            "summary_data = {\n",
            "    \"Load Case\": [\n",
            "        \"Vertical Bending\", \"Tab Bending\", \"Bolt Tension\", \"Bolt Bearing\", \n",
            "        \"Bolt Shear\", \"Bolt Tear-out\", \"Bond Strength\", \"Casing Buckling\"\n",
            "    ],\n",
            "    \"Safety Factor\": [\n",
            "        sf_lid, sf_tab_bending, sf_bolt_tension, sf_bearing, \n",
            "        sf_bolt_shear, sf_tearout, sf_bond, sf_buckling\n",
            "    ],\n",
            "    \"Minimum Required\": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]\n",
            "}\n",
            "\n",
            "df = pd.DataFrame(summary_data)\n",
            "df[\"Status\"] = df[\"Safety Factor\"].apply(lambda x: \"PASS\" if x >= 1.0 else \"FAIL\")\n",
            "display(df.round(4))"
        ]

# Final Cleanup: Rename headers and ToC
header_map = {
    "## 3. Fasteners": "## 4. Fasteners",
    "## 4. Bond Strength": "## 5. Bond Strength",
    "## 5. Euler-Johnson Buckling": "## 6. Euler-Johnson Buckling",
    "## 6. Summary Results": "## 8. Summary Results Table"
}

for cell in nb['cells']:
    if cell['cell_type'] == 'markdown':
        source = "".join(cell['source'])
        for old, new in header_map.items():
            if source.startswith(old):
                cell['source'] = [new + source[len(old):]]

# Update ToC
toc_content = [
    "## Table of Contents\n",
    "1. [1. Constants and Geometry](#1.-Constants-and-Geometry)\n",
    "2. [2. Load Cases & Bending Stress](#2.-Load-Cases-&-Bending-Stress)\n",
    "3. [3. Tab Bending Analysis](#3.-Tab-Bending-Analysis)\n",
    "4. [4. Fasteners: Tension, Shear, and Bearing](#4.-Fasteners:-Tension,-Shear,-and-Bearing)\n",
    "5. [5. Bond Strength Analysis](#5.-Bond-Strength-Analysis)\n",
    "6. [6. Euler-Johnson Buckling Analysis](#6.-Euler-Johnson-Buckling-Analysis)\n",
    "7. [7. Passive Thermal Properties](#7.-Passive-Thermal-Properties)\n",
    "8. [8. Summary Results Table](#8.-Summary-Results-Table)\n",
    "9. [Sources Referenced](#Sources-Referenced)"
]

for cell in nb['cells']:
    if cell['cell_type'] == 'markdown' and '## Table of Contents' in "".join(cell['source']):
        cell['source'] = toc_content

with open('FSAESegmentHandCalcs.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
