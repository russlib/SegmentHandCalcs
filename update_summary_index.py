import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

# The summary table code is in the 2nd to last cell (index -2 or -3 depending on if sources are last)
# Based on the grep, it's near the end.
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'summary_data =' in "".join(cell['source']):
        cell['source'] = [
            "summary_data = {\n",
            "    \"Calculation Ref\": [\n",
            "        \"Section 2.4\", \"Section 3.2\", \"Section 3.3\", \n",
            "        \"Section 3.4\", \"Section 3.5\", \"Section 4.1\", \"Section 5.2\"\n",
            "    ],\n",
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
            "df = pd.DataFrame(summary_data).set_index(\"Calculation Ref\")\n",
            "df[\"Status\"] = df[\"Safety Factor\"].apply(lambda x: \"PASS\" if x >= 1.0 else \"FAIL\")\n",
            "display(df.round(4))"
        ]
        break

with open('FSAESegmentHandCalcs.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
