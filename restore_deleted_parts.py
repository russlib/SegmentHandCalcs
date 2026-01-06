import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

# 1. Restore ASCII Art
ascii_art_1 = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "             ____________________________________________________________\n",
        "            /                                                           /|\n",
        "           /                     POLYCARBONATE LID                     / |\n",
        "          /___________________________________________________________/  |\n",
        "         |                                                           |   | <--- EneSegHeight\n",
        "         |                                                           |   |      (105.6mm)\n",
        "         |___________________________________________________________|   |\n",
        "         |                                                           |  /\n",
        "         |                                                           | / <--- EneSegmentWidth\n",
        "         |___________________________________________________________|/        (81.2mm)\n",
        "           <------------------- EneSegmentDepth -------------------> \n",
        "                                 (417.0mm)"
    ]
}

ascii_art_2 = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "         _________________________________________________________   \n",
        "      | | [ o o ]   [ o o ]   [ o o ]   [ o o ]   [ o o ]   [ o o ] | \n",
        "      | | [ o o ]   [ o o ]   [ o o ]   [ o o ]   [ o o ]   [ o o ] | \n",
        "      | | [ o o ]   [ o o ]   [ o o ]   [ o o ]   [ o o ]   [ o o ] |  (81.2mm)WIDTH\n",
        "      | | [ o o ]   [ o o ]   [ o o ]   [ o o ]   [ o o ]           | \n",
        "      | |_________________________________________________________| |\n",
        "      |                                                             |\n",
        "        <---------------------- DEPTH (417.0mm) ------------------->"
    ]
}

# Insert after Cell 0 (Header)
nb['cells'].insert(1, ascii_art_1)
nb['cells'].insert(2, ascii_art_2)

# 2. Add missing Fastener calculations to Cell 8 (previously Cell 6)
# After insertion, Cell 6 becomes Cell 8
cell_6_index = 8 
cell_6_source = nb['cells'][cell_6_index]['source']

# Add bolt shear and tear-out
extra_fastener_code = [
    "\n",
    "# 3.4 Bolt Shear SF (Assumes 2 bolts per side)\n",
    "sf_bolt_shear = (max_tensile_fastener * 2) / (6 * segment_modules_weight * 40 * G)\n",
    "\n",
    "# 3.5 Tear-out Strength\n",
    "bolt_dist_edge = 8 / 1000\n",
    "max_tearout_force = bolt_dist_edge * garolite_thickness * (38000 * PSI_TO_PA)\n",
    "sf_tearout = max_tearout_force / (width_force / 6)\n",
    "\n",
    "print(f\"Bolt Shear SF: {sf_bolt_shear:.4f}\")\n",
    "print(f\"Bolt Tear-out SF: {sf_tearout:.4f}\")"
]
nb['cells'][cell_6_index]['source'].extend(extra_fastener_code)

# 3. Add Bond Strength Section before Buckling (Cell 7 becomes Cell 9)
bond_strength_md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 4. Bond Strength Analysis\n",
        "Checking the structural epoxy bond between Garolite panels."
    ]
}

bond_strength_code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# 4.1 Bond Strength\n",
        "fr4_bond_strength = 2200 * PSI_TO_PA\n",
        "depth_force = segment_modules_weight * 40 * G\n",
        "\n",
        "# 4.2 Bond Areas\n",
        "depth_restricting_bond_area = garolite_thickness * (80 / 1000)\n",
        "side_bond_area = 0.02 * garolite_thickness * 2\n",
        "bond_max_force = fr4_bond_strength * (depth_restricting_bond_area + side_bond_area)\n",
        "sf_bond = bond_max_force / depth_force\n",
        "\n",
        "print(f\"Bond Safety Factor: {sf_bond:.4f}\")"
    ]
}

# Buckling header is currently Cell 7, after 2 inserts it's Cell 9.
# We want to insert Bond Strength before Buckling.
nb['cells'].insert(9, bond_strength_md)
nb['cells'].insert(10, bond_strength_code)

# 4. Update Summary Table (now Cell 13, was 10)
summary_cell_index = 13
nb['cells'][summary_cell_index]['source'] = [
    "summary_data = {\n",
    "    \"Load Case\": [\n",
    "        \"Vertical Bending\", \"Bolt Tension\", \"Bolt Bearing\", \n",
    "        \"Bolt Shear\", \"Bolt Tear-out\", \"Bond Strength\", \"Casing Buckling\"\n",
    "    ],\n",
    "    \"Safety Factor\": [\n",
    "        sf_lid, sf_bolt_tension, sf_bearing, \n",
    "        sf_bolt_shear, sf_tearout, sf_bond, sf_buckling\n",
    "    ],\n",
    "    \"Minimum Required\": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]\n",
    "}\n",
    "\n",
    "df = pd.DataFrame(summary_data)\n",
    "df[\"Status\"] = df[\"Safety Factor\"].apply(lambda x: \"PASS\" if x >= 1.0 else \"FAIL\")\n",
    "display(df.round(4))"
]

# Rename 4. Euler-Johnson Buckling Analysis to 5. Euler-Johnson Buckling Analysis
# It should be Cell 11 now.
nb['cells'][11]['source'] = ["## 5. Euler-Johnson Buckling Analysis"]
# And 5. Summary Results Table to 6. Summary Results Table
# It should be Cell 13 now (but the header is Cell 12)
nb['cells'][12]['source'] = ["## 6. Summary Results Table"]

with open('FSAESegmentHandCalcs.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
