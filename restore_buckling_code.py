import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

buckling_code = [
    "i_walls = 2 * (((ene_segment_width/2 + garolite_thickness/2)**2 * garolite_thickness * (ene_seg_height + (2 * garolite_thickness))))\n",
    "radius_of_gyration = math.sqrt(i_walls / depth_cross_sec_area)\n",
    "slenderness_ratio = ene_segment_depth / radius_of_gyration\n",
    "critical_slenderness = math.pi * math.sqrt((2 * garolite_modulus) / garolite_strength)\n",
    "\n",
    "if slenderness_ratio < critical_slenderness:\n",
    "    max_force_buckle = depth_cross_sec_area * (garolite_strength - (garolite_strength**2 * slenderness_ratio**2) / (4 * math.pi**2 * garolite_modulus))\n",
    "    mode = \"Johnson\"\n",
    "else:\n",
    "    max_force_buckle = (math.pi**2 * garolite_modulus * i_walls) / (ene_segment_depth**2)\n",
    "    mode = \"Euler\"\n",
    "\n",
    "sf_buckling = max_force_buckle / (segment_modules_weight * 40 * G)\n",
    "print(f\"Buckling Mode: {mode}, SF: {sf_buckling:.4f}\")"
]

nb['cells'][12]['source'] = buckling_code

with open('FSAESegmentHandCalcs.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
