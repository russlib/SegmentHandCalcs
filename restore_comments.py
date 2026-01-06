import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

# Cell 2: Constants and Geometry Code
# Find the cell containing 'ene_segment_depth'
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and any('ene_segment_depth' in line for line in cell['source']):
        new_source = []
        for line in cell['source']:
            if 'ene_segment_depth = 6 * ene_mod_depth' in line:
                new_source.append('ene_segment_depth = 6 * ene_mod_depth #This represents the longest dimension of the segment\n')
            elif 'ene_segment_width = ene_mod_width * 4' in line:
                new_source.append('ene_segment_width = ene_mod_width * 4 #This repersents the width fromm 4 enepaq bricks side by side\n')
                new_source.append('#1x Enepaq bricks in height | 1 * ene_seg_height = Redundant\n')
            elif 'segment_modules_weight = module_weight * 23' in line:
                new_source.append('segment_modules_weight = module_weight * 23 #total enepaq mass\n')
            elif 'top_cross_sec_area =' in line:
                new_source.append('# Areas Garolite - Imagine Section Views\n')
                new_source.append('top_cross_sec_area = ene_segment_depth * garolite_thickness * 2 #airflow "endplates" arent considerd valid area   # View Axis: Depth X, Width Y\n')
            elif 'depth_cross_sec_area =' in line:
                # Need to check if width_cross_sec_area was restored, it seems it was missing in my previous restoration
                # Let's add it back if it's missing or update it if it exists
                new_source.append('width_cross_sec_area = ene_segment_depth * garolite_thickness * 1 #airflow "endplates" arent considerd valid area # View Axis: Depth X, Height Y\n')
                new_source.append('depth_cross_sec_area = (ene_segment_width * garolite_thickness * 2) + (ene_seg_height * garolite_thickness * 2)   # View Axis: Width X, Height Y\n')
            else:
                new_source.append(line)
        cell['source'] = new_source

# Cell 8: Fasteners Code
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and any('sf_bolt_tension' in line for line in cell['source']):
        new_source = []
        for line in cell['source']:
            if 'sf_bolt_tension =' in line:
                new_source.append('# Safety Factors (Assumes 2 bolts share load per side)\n')
                new_source.append(line)
            else:
                new_source.append(line)
        cell['source'] = new_source

# Cell 10: Bond Strength Code
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and any('fr4_bond_strength' in line for line in cell['source']):
        if not any('# FR4 / G10 Bond Strength' in line for line in cell['source']):
            cell['source'].insert(0, '# FR4 / G10 Bond Strength\n')

# Cell 12: Buckling Code
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and any('max_force_buckle' in line for line in cell['source']):
        new_source = []
        for line in cell['source']:
            if 'mode = "Johnson"' in line:
                new_source.append('    # Johnson Inelastic Buckling\n')
                new_source.append(line)
            elif 'mode = "Euler"' in line:
                new_source.append('    # Euler Elastic Buckling\n')
                new_source.append(line)
            else:
                new_source.append(line)
        cell['source'] = new_source

with open('FSAESegmentHandCalcs.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
