# -*- coding: utf-8 -*-

from colorama import Fore, Style, init
import sympy as sp

init(autoreset=True)

class s3QuantumYieldCalculator:
    def __init__(self, k_abss0s1=None, k_fls1s0=None, k_ics1s0=None, k_iscs1t1=None,
                 k_risct1s1=None, k_pht1s0=None, k_isct1s0=None):
        self.k_abss0s1 = k_abss0s1  
        self.k_fls1s0 = k_fls1s0  
        self.k_ics1s0 = k_ics1s0  
        self.k_iscs1t1 = k_iscs1t1  
        self.k_risct1s1 = k_risct1s1  
        self.k_pht1s0 = k_pht1s0  
        self.k_isct1s0 = k_isct1s0 

    def _calculate_quantum_yield(self):
        if all(val is not None for val in [self.k_fls1s0, self.k_ics1s0, self.k_iscs1t1,
                                           self.k_risct1s1, self.k_pht1s0, self.k_isct1s0]):

            total_S1 = (self.k_fls1s0 + self.k_ics1s0 + self.k_iscs1t1) - \
                       self.k_risct1s1 * self.k_iscs1t1 / (self.k_risct1s1 + self.k_isct1s0 + self.k_pht1s0)
            total_T1 = -self.k_risct1s1 + (self.k_risct1s1 + self.k_isct1s0 + self.k_pht1s0) / \
                       self.k_iscs1t1 * (self.k_fls1s0 + self.k_ics1s0 + self.k_iscs1t1)

            # quantum yields for FL, IC and ISC
            QY_fl = (self.k_fls1s0 / total_S1) * 100   
            QY_ic = (self.k_ics1s0 / total_S1) * 100   
            QY_isc = ((self.k_iscs1t1) / total_S1) * 100  

            return QY_fl, QY_ic, QY_isc
        else:
            return None

    def display_quantum_yield(self):
        QY = self._calculate_quantum_yield()
        print(Fore.YELLOW + "\n Quantum Yield of Fluorescence (%): ")
        print(" {:.2f}% \n".format(QY[0]))

