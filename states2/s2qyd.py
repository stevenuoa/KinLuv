# -*- coding: utf-8 -*-

from colorama import Fore, Style, init
import sympy as sp

init(autoreset=True)

class s2QuantumYieldCalculator:
    def __init__(self, k_abss0s1=None, k_fls1s0=None, k_ics1s0=None):
        self.k_abss0s1 = k_abss0s1
        self.k_fls1s0 = k_fls1s0
        self.k_ics1s0 = k_ics1s0

    def _calculate_quantum_yield(self):
        if self.k_fls1s0 is not None and self.k_ics1s0 is not None:
            total = self.k_fls1s0 + self.k_ics1s0
            # quantum yield for fluorescence in %
            QY_fl = (self.k_fls1s0 / total) * 100
            # quantum yield for internal conversion in %
            QY_ic = (self.k_ics1s0 / total) * 100   
            return QY_fl, QY_ic
        else:
            return None

    def display_quantum_yield(self):
        QY = self._calculate_quantum_yield()
        print(Fore.YELLOW + "\n Quantum Yield of Fluorescence (%): ")
        print(" {:.2f}% \n".format(QY[0]))


