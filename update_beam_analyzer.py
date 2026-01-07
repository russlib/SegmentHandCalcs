import json

# Define the content for the notebook
nb = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Beam Analyzer\n",
    "This tool analyzes simply supported beams under different loading conditions using Norton Machine Design 6e formulas."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Case (a): Concentrated Loading\n",
    "A single force $F$ applied at distance $a$ from the left support."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "# ==========================================\n",
    "# 1. INPUT VALUES - Case (a)\n",
    "# ==========================================\n",
    "F = 1000      # Force (N)\n",
    "l = 1.0       # Total length of beam (m)\n",
    "a = 0.4       # Distance from left support to load (m)\n",
    "E = 200e9     # Modulus of Elasticity (Pa)\n",
    "I = 1e-6      # Moment of Inertia (m^4)\n",
    "\n",
    "def macaulay(x, a, n):\n",
    "    return np.where(x > a, (x - a)**n, 0.0)\n",
    "\n",
    "x = np.linspace(0, l, 1000)\n",
    "R1 = F * (1 - a/l)\n",
    "R2 = F * (a/l)\n",
    "V = R1 - F * macaulay(x, a, 0)\n",
    "M = R1 * x - F * macaulay(x, a, 1)\n",
    "const_theta = (a / (3 * l)) * (-a**2 + 3 * a * l - 2 * l**2)\n",
    "theta = (F / (2 * E * I)) * ((1 - a/l) * x**2 - macaulay(x, a, 2) + const_theta)\n",
    "y = (F / (6 * E * I)) * ((1 - a/l) * x**3 - macaulay(x, a, 3) + 3 * const_theta * x)\n",
    "\n",
    "fig, axs = plt.subplots(4, 1, figsize=(10, 10), sharex=True)\n",
    "axs[0].plot(x, V, 'r'); axs[0].set_ylabel('Shear (N)')\n",
    "axs[1].plot(x, M, 'b'); axs[1].set_ylabel('Moment (Nm)')\n",
    "axs[2].plot(x, theta, 'g'); axs[2].set_ylabel('Slope (rad)')\n",
    "axs[3].plot(x, y*1000, 'purple'); axs[3].set_ylabel('Deflection (mm)')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Case (b): Uniformly Distributed Loading\n",
    "A distributed load $w$ starting at distance $a$ and continuing to the end of the beam."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "# ==========================================\n",
    "# 1. INPUT VALUES - Case (b)\n",
    "# ==========================================\n",
    "w_load = 5000  # Load intensity (N/m)\n",
    "l = 1.0        # Total length of beam (m)\n",
    "a = 0.3        # Start of distributed load (m)\n",
    "E = 200e9      # Modulus of Elasticity (Pa)\n",
    "I = 1e-6       # Moment of Inertia (m^4)\n",
    "\n",
    "def macaulay(x, a, n):\n",
    "    return np.where(x > a, (x - a)**n, 0.0)\n",
    "\n",
    "x = np.linspace(0, l, 1000)\n",
    "\n",
    "# Reactions\n",
    "R1 = (w_load / (2 * l)) * (l - a)**2\n",
    "R2 = (w_load / (2 * l)) * (l**2 - a**2)\n",
    "\n",
    "# Shear, Moment, Slope, Deflection\n",
    "V = w_load * ( (1/(2*l))*(l-a)**2 - macaulay(x, a, 1) )\n",
    "M = (w_load / 2) * ( (x/l)*(l-a)**2 - macaulay(x, a, 2) )\n",
    "\n",
    "term_const = (1/l) * ( (l-a)**4 - 2*(l**2)*((l-a)**2) )\n",
    "theta = (w_load / (24 * E * I)) * ( (6*(x**2)/l)*(l-a)**2 - 4*macaulay(x, a, 3) + term_const )\n",
    "y = (w_load / (24 * E * I)) * ( (2*(x**3)/l)*(l-a)**2 - macaulay(x, a, 4) + (x/l)*term_const )\n",
    "\n",
    "# Plotting\n",
    "fig, axs = plt.subplots(4, 1, figsize=(10, 10), sharex=True)\n",
    "plt.subplots_adjust(hspace=0.4)\n",
    "\n",
    "axs[0].plot(x, V, 'r'); axs[0].fill_between(x, V, color='r', alpha=0.1); axs[0].set_ylabel('Shear (N)')\n",
    "axs[1].plot(x, M, 'b'); axs[1].fill_between(x, M, color='b', alpha=0.1); axs[1].set_ylabel('Moment (Nm)')\n",
    "axs[2].plot(x, theta, 'g'); axs[2].fill_between(x, theta, color='g', alpha=0.1); axs[2].set_ylabel('Slope (rad)')\n",
    "axs[3].plot(x, y*1000, 'purple'); axs[3].fill_between(x, y*1000, color='purple', alpha=0.1); axs[3].set_ylabel('Deflection (mm)')\n",
    "\n",
    "for ax in axs: ax.grid(True, linestyle='--', alpha=0.6); ax.axhline(0, color='black', lw=1)\n",
    "plt.xlabel('Position x (m)')\n",
    "plt.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

with open('BeamAnalysisTool.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
