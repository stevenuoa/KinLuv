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

Here is an example input for using *KinLuv*:

```python
        _           __
  /\ /\(_) _ __    / /   _   _ __   __
 / //_/| || '_ \  / /   | | | |\ \ / /
/ __ \ | || | | |/ /___ | |_| | \ V /
\/  \/ |_||_| |_|\____/  \__,_|  \_/


# Define the rate constants (units: s⁻¹):
# e.g.,
# `k_iscs1t1` denotes the intersystem crossing (ISC) rate constant from the first singlet excited state (S1) to the first triplet state (T1).

# by default
k_abss0s1=1.00E+13,
k_abss0s2=1.00E+13,

# by provided
k_iscs1t1=1.00E+07,
k_iscs1t2=1.00E+07,
k_iscs2t1=1.00E+07,
k_iscs2t2=1.00E+07,
k_isct1s0=1.00E+07,
k_risct1s1=1.00E+05,
k_risct1s2=1.00E+05,
k_risct2s1=1.00E+05,
k_risct2s2=1.00E+05,
k_fls1s0=1.00E+07,
k_fls2s0=0.00E+00,
k_ics1s0=1.00E+07,
k_ics2s1=1.00E+12,
k_ics1s2=0.00E+00,
k_ict2t1=1.00E+12,
k_ict1t2=0.00E+00,
k_pht1s0=1.00E+02

# Specify the pulse width (s) of the excitation prior to decay:

time_pulse=1e-11
num_photon=1

# Define the excitation and decay timescale (s) for plotting and numerical solving (four- and five-state models):

time_excitation=1e-9
time_decay=1e-3

```
```bash
kinluv
b
f
*.inp
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

