<h1 align="left">
  <a href="https://github.com/stevenuoa/KinLuv.git"><img src="https://github.com/stevenuoa/KinLuv/blob/main/logo_transparent.png" alt="Markdownify" width="600"></a>
</h1>

<h2 align="justify">A Python Toolkit for Modeling Multistate Kinetics in Thermally Activated Delayed Fluorescence (TADF) Systems.</h2>

<div align="left">
 
[![GitHub](https://img.shields.io/github/stars/stevenuoa/KinLuv?style=social)](https://github.com/stevenuoa/KinLuv)
[![GitHub Issues](https://img.shields.io/github/issues/stevenuoa/KinLuv?color=4aa8d8&style=flat-square)](https://github.com/stevenuoa/KinLuv/issues)
[![Latest Release](https://img.shields.io/github/v/release/stevenuoa/KinLuv?include_prereleases&color=6a5acd&style=flat-square)](https://github.com/stevenuoa/KinLuv/releases/latest)
[![License](https://img.shields.io/github/license/stevenuoa/KinLuv?color=2db27d&style=flat-square)](https://github.com/stevenuoa/KinLuv/blob/main/LICENSE)

</div>

<div align="justify">

**KinLuv** is a Python-based simulation toolkit for multistate kinetic modeling. It can predict prompt and delayed fluorescence lifetimes, as well as photoluminescence quantum yield (PLQY) directly from user-defined rate constants.

Going beyond conventional approaches, **KinLuv** solves systems of ordinary differential equations (ODEs) to capture the complex photophysical processes, including:

- **Fluorescence (FL)** (Kasha and anti-Kasha)
- **Phosphorescence (PH)**
- **Internal Conversion (IC)**
- **Reverse Internal Conversion (rIC)**
- **Intersystem Crossing (ISC)**
- **Reverse Intersystem Crossing (rISC)**

Whether you’re exploring novel TADF materials or discovering new TADF mechanisms, **KinLuv** offers a versatile and practical platform for universal multistate kinetic simulations.

</div>

---

## ✨ Key Features

* Supports:
  * Multistate photophysical models from two states (S<sub>0</sub>, S<sub>1</sub>) to five states (S<sub>0</sub>, S<sub>1</sub>, S<sub>2</sub>, T<sub>1</sub>, T<sub>2</sub>)
  
* Computes:
  * Prompt fluorescence lifetime
  * Delayed fluorescence lifetime
  * PLQY
    
* Handles:
  * Analytical solutions for two- and three-state models
  * Numerical solutions for four- and five-state models to minimize computational cost
    
* Allows:
  * Distinguishable timescales are observed for the excitation period corresponding to the pulse duration, and the subsequent decay stage
  * Enables direct comparison with experimental data (e.g., photoluminescence transient decay curve and PLQY)
  * Clear and modular Python API

---

## 🛠 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/stevenuoa/KinLuv.git
cd KinLuv
pip install .
```
---

## 🚀 Quick Start

1. Prepare an input example as below for using **KinLuv**:

```python
        _           __
  /\ /\(_) _ __    / /   _   _ __   __
 / //_/| || '_ \  / /   | | | |\ \ / /
/ __ \ | || | | |/ /___ | |_| | \ V /
\/  \/ |_||_| |_|\____/  \__,_|  \_/


# Define the rate constants (units: s⁻¹):
# e.g.,
# k_iscs1t1 denotes the intersystem crossing (ISC) rate constant from the first singlet excited state (S1) to the first triplet state (T1).

# by default
k_abss0s1=1.00E+13,
k_abss0s2=1.00E+13,

# by provided
k_iscs1t1=1.00E+07,
k_iscs1t2=1.00E+07,
k_iscs2t1=1.00E+07,
k_iscs2t2=1.00E+07,
k_isct1s0=1.00E+04,
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
2. Enter the following commands and options:
   
e.g., running the (b). three-state model and input the parameters with a file "inp"

```bash
kinluv
b
f
*.inp
```
---

## 📈 Output Summary

**KinLuv** output the following results:
  * Prompt fluorescence lifetime 
  * Delayed fluorescence lifetime 
  * PLQY 
  * Time-resolved population curves
    
Detailed examples please see the document.

---

## 📝 Citation

If you use **KinLuv** in your research, please cite:

```
@software{KinLuv2025,
  author = {Yue He, Daniel Escudero},
  title = {KinLuv: A Python Toolkit for Modeling Multistate Kinetics in Thermally Activated Delayed Fluorescence (TADF) Systems},
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

