<h1 align="center">
  <a href="https://github.com/stevenuoa/KinLuv.git"><img src="https://github.com/stevenuoa/KinLuv/blob/main/logo_transparent.png" alt="Markdownify" width="800"></a>
</h1>

<h2 align="justify">A Python toolkit for modeling kinetics in thermally activated delayed fluorescence (TADF) systems.</h2>

<div align="center">
 
[![GitHub](https://img.shields.io/github/stars/stevenuoa/KinLuv?style=social)](https://github.com/stevenuoa/KinLuv)
[![GitHub Issues](https://img.shields.io/github/issues/stevenuoa/KinLuv?color=4aa8d8&style=flat-square)](https://github.com/stevenuoa/KinLuv/issues)
[![Latest Release](https://img.shields.io/github/v/release/stevenuoa/KinLuv?include_prereleases&color=6a5acd&style=flat-square)](https://github.com/stevenuoa/KinLuv/releases/latest)
[![License](https://img.shields.io/github/license/stevenuoa/KinLuv?color=2db27d&style=flat-square)](https://github.com/stevenuoa/KinLuv/blob/main/LICENSE)

</div>

<div align="justify">

*KinLuv* is a Python-based kinetics simulation tool designed to predict both prompt and delayed fluorescence lifetimes, as well as photoluminescence quantum yield (PLQY), from user-input rate constants.

Going beyond conventional approaches, *KinLuv* solves systems of ordinary differential equations (ODEs) to model complex multi-state photophysical processes, including:

- **Fluorescence (FL)**
- **Phosphorescence (Ph)**
- **Internal Conversion (IC)**
- **Intersystem Crossing (ISC)**
- **Reverse Intersystem Crossing (rISC)**

Whether you’re exploring novel TADF materials or discovering new TADF mechanisms, *KinLuv* offers a robust and practical platform for kinetic modeling.

</div>

---

## ✨ Key Features

* Supports:
  * Multi-state photophysical models from two states to five states
  
* Computes:
  * Prompt fluorescence lifetime
  * Delayed fluorescence lifetime
  * Photoluminescence quantum yield (PLQYD)
    
* Handles:
  * Analytical solutions for two- and three-state models
  * Numerical solutions for four- and five-state models
    
* Allows:
  * Distinguishable timescales for excitation and decay (*e.g.*, 1 ns excitation, 1 ms decay)
  * Enables direct comparison with experimental data (*e.g.*, photoluminescence transient decay curve and QYD)
  * Clear and modular Python API

---

## 🛠 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/stevenuoa/KinLuv.git
cd KinLuv_v1.0.0
pip install .
```
---

## 🚀 Quick Start

Here’s an input example of how to simulate a 3-state photophysical system using KinLuv:

```python
from kinluv import KinModel

# Define rate constants (in s⁻¹)
params = {
    'k_r_S1': 1e8,      # Radiative decay from S1
    'k_nr_S1': 1e7,     # Non-radiative decay from S1
    'k_ISC': 1e6,       # Intersystem crossing (S1 → T1)
    'k_r_T1': 0.0,      # Radiative decay from T1
    'k_nr_T1': 1e4,     # Non-radiative decay from T1
    'k_rISC': 1e5       # Reverse intersystem crossing (T1 → S1)
}

# Initialize a 3-state model
model = KinModel(states=3, params=params)

# Run the simulation
results = model.run_simulation(
    excitation_pulse_width=10e-15,  # 10 fs
    absorbed_photons=1,
    excitation_time=1e-9,           # 1 ns
    decay_time=1e-3                 # 1 ms
)

# Output results
print("Prompt lifetime:", results['prompt_lifetime'], "s")
print("Delayed lifetime:", results['delayed_lifetime'], "s")
print("PLQY:", results['QY'])
```
```bash
git clone https://github.com/stevenuoa/KinLuv.git
cd KinLuv_v1.0.0
pip install .
```
---

## 📈 Output Summary

Simulation results include:

* Prompt fluorescence lifetime 
* Delayed fluorescence lifetime 
* PLQY 
* Time-resolved population curves 

More examples please see the documentation.

---

## 📝 Citation

If you use *KinLuv* in your research, please cite:

```
@software{KinLuv2025,
  author = {Your Name},
  title = {KinLuv: A Python-Based Tool for Kinetic Modeling of Photophysical Processes},
  year = {2025},
  url = {https://github.com/stevenuoa/KinLuv.git}
}
```

---

## 📬 Contact

For more questions or requests:

* Please Contact Prof. Daniel Escudero: **[daniel.escudero@kuleuven.be](mailto:daniel.escudero@kuleuven.be)**

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/stevenuoa/KinLuv/blob/main/LICENSE) file for details.

