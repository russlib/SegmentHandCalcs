import json

with open('FSAESegmentHandCalcs.ipynb', 'r') as f:
    nb = json.load(f)

# Current cells:
# 7: ## 2. Load Cases & Bending Stress
# 8: ## 3. Tab Bending Analysis
# 9: # 3.1 Geometry for Tab Analysis (uses top_force)
# 10: # 2.1 Vertical Force (20g) (defines top_force)

# We want to move Cell 10 to be Cell 8, so the order is:
# 7: Header 2
# 8: Code 2 (defines top_force)
# 9: Header 3
# 10: Code 3 (uses top_force)

cell_10 = nb['cells'].pop(10)
nb['cells'].insert(8, cell_10)

with open('FSAESegmentHandCalcs.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
