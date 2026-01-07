import json

with open('BeamAnalysisTool.ipynb', 'r') as f:
    nb = json.load(f)

def update_tick_visibility(source):
    new_source = []
    found_sharex = False
    for line in source:
        # 1. Modify subplots to NOT share x labels (keep alignment but show numbers)
        if "plt.subplots(5, 1, figsize=(10, 15), sharex=True)" in line:
            new_source.append(line.replace("sharex=True", "sharex=True")) # Keep sharex for alignment
            found_sharex = True
        elif found_sharex and "plt.subplots_adjust" in line:
            new_source.append(line)
            # Add logic to re-enable labels for all subplots despite sharex
            new_source.append("\n    # Ensure tick labels are visible on ALL graphs\n")
            new_source.append("    for ax in axs:\n")
            new_source.append("        ax.tick_params(labelbottom=True)\n")
            found_sharex = False
        # 2. Ensure FBD still has top labels
        elif "ax.xaxis.tick_top()" in line:
            new_source.append("    ax.tick_params(labeltop=True) # Ensure FBD labels stay at top\n")
        else:
            new_source.append(line)
    return new_source

nb['cells'][2]['source'] = update_tick_visibility(nb['cells'][2]['source'])
nb['cells'][4]['source'] = update_tick_visibility(nb['cells'][4]['source'])

with open('BeamAnalysisTool.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
