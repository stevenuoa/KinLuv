[![GitHub Stars](https://img.shields.io/github/stars/stevenuoa/KinLuv.svg)](https://github.com/stevenuoa/KinLuv/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/stevenuoa/KinLuv.svg)](https://github.com/stevenuoa/KinLuv/issues)
[![github release version](https://img.shields.io/github/v/release/stevenuoa/KinLuv.svg?include_prereleases)](https://github.com/stevenuoa/KinLuv/releases/latest)
[![license](https://img.shields.io/github/license/stevenioa/KinLuv.svg)](https://github.com/stevenuoa/KinLuv/LICENSE)

# KinLuv

**KinLuv** is a Python-based kinetic simulation tool designed to predict both prompt and delayed fluorescence lifetimes, as well as photoluminescence quantum yield (PLQY), from user-defined rate constants. Unlike conventional methods, KinLuv solves systems of ordinary differential equations (ODEs) to model complex multi-state photophysical processes, including fluorescence (FL), internal conversion (IC), intersystem crossing (ISC), and reverse intersystem crossing (rISC).

---

## ✨ Key Features

* Supports **2- to 5-state** photophysical models
* Computes:

  * Prompt fluorescence lifetime
  * Delayed fluorescence lifetime
  * Photoluminescence quantum yield (PLQY)
* Handles both:

  * **Analytical solutions** for 2- and 3-state models
  * **Numerical integration** for 4- and 5-state systems
* Allows different timescales for excitation and decay (e.g., 1 ns excitation, 1 ms decay)
* Enables direct comparison with experimental data
* Clear, modular Python API

---

## 🛠 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/kinluv.git
cd kinluv
pip install -r requirements.txt
```

Or (if available on PyPI):

```bash
pip install kinluv
```

---

## 🚀 Quick Start

Here’s an example of how to simulate a 3-state photophysical system using KinLuv:

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

---

## 🗂 Project Structure

```
kinluv/
├── core/               # Core kinetic simulation modules
├── examples/           # Usage examples and demo scripts
├── tests/              # Unit tests
├── utils/              # Helper functions
├── README.md           # Project documentation
├── requirements.txt    # Dependency list
└── setup.py            # Packaging configuration
```

## 📈 Output Summary

Simulation results include:

* Prompt fluorescence lifetime (in seconds)
* Delayed fluorescence lifetime (in seconds)
* PLQY (0 to 1)
* Time-resolved population curves (optional)

Plots can be generated using built-in plotting tools or external libraries like `matplotlib`.

---

## 📝 Citation

If you use **KinLuv** in your research, please cite:

```
@software{KinLuv2025,
  author = {Your Name},
  title = {KinLuv: A Python-Based Tool for Kinetic Modeling of Photophysical Processes},
  year = {2025},
  url = {https://github.com/yourusername/kinluv}
}
```

---

## 🤝 Contributing

Contributions are welcome! You can help by:

* Reporting bugs via [Issues](https://github.com/yourusername/kinluv/issues)
* Submitting pull requests
* Improving documentation
* Adding test cases or models

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before submitting changes.

---

## 📬 Contact

For questions, bug reports, or feature requests:

* Open an issue: [GitHub Issues](https://github.com/yourusername/kinluv/issues)
* Contact the maintainer: **[your.email@example.com](mailto:your.email@example.com)**

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

