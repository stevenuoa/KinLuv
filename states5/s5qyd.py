# -*- coding: utf-8 -*-

from colorama import Fore, Style, init
import sympy as sp

init(autoreset=True)

class s5QuantumYieldCalculator:
    def __init__(self, rate_constants):
        self.S0, self.S1, self.S2, self.T1, self.T2 = sp.symbols('S0 S1 S2 T1 T2')
        self.rate_constants = rate_constants

        # define equations
        self.equations = [
            -self.S0 * self.rate_constants['k_abss0s2'] 
            + self.S1 * (self.rate_constants['k_fls1s0'] + self.rate_constants['k_ics1s0']) 
            + self.S2 * self.rate_constants['k_fls2s0'] 
            + self.T1 * (self.rate_constants['k_pht1s0'] + self.rate_constants['k_isct1s0']),
            
            -self.S1 * (self.rate_constants['k_iscs1t1'] + self.rate_constants['k_iscs1t2'] 
                        + self.rate_constants['k_fls1s0'] + self.rate_constants['k_ics1s0'] + self.rate_constants['k_ics1s2']) 
            + self.S2 * self.rate_constants['k_ics2s1'] 
            + self.T1 * self.rate_constants['k_risct1s1'] 
            + self.T2 * self.rate_constants['k_risct2s1'],

            self.S0 * self.rate_constants['k_abss0s2'] + self.S1 * self.rate_constants['k_ics1s2']
            - self.S2 * (self.rate_constants['k_fls2s0'] + self.rate_constants['k_ics2s1'] 
                         + self.rate_constants['k_iscs2t1'] + self.rate_constants['k_iscs2t2']) 
            + self.T1 * self.rate_constants['k_risct1s2'] 
            + self.T2 * self.rate_constants['k_risct2s2'],

            self.S1 * self.rate_constants['k_iscs1t1'] 
            + self.S2 * self.rate_constants['k_iscs2t1'] 
            - self.T1 * (self.rate_constants['k_pht1s0'] + self.rate_constants['k_isct1s0'] 
                         + self.rate_constants['k_risct1s1'] + self.rate_constants['k_risct1s2'] + self.rate_constants['k_ict1t2']) 
            + self.T2 * self.rate_constants['k_ict2t1'],

            self.S1 * self.rate_constants['k_iscs1t2'] 
            + self.S2 * self.rate_constants['k_iscs2t2'] + self.T1 * self.rate_constants['k_ict1t2']
            - self.T2 * (self.rate_constants['k_risct2s1'] + self.rate_constants['k_risct2s2'] 
                         + self.rate_constants['k_ict2t1'])
        ]

    def calculate_quantum_yield(self):
        equations_with_values = [eq.subs(self.rate_constants) for eq in self.equations]
        solution = sp.solve(equations_with_values, (self.S0, self.S2, self.T1, self.T2, self.S1))

        # output solutions with S1
        print(Fore.YELLOW + "\n Expressions of different state population with S1: ")
        print("S0 = ", solution[self.S0])
        print("S2 = ", solution[self.S2])
        print("T1 = ", solution[self.T1])
        print("T2 = ", solution[self.T2])

        QY_fl = ((self.S1 * self.rate_constants['k_fls1s0']
                  + solution[self.S2] * self.rate_constants['k_fls2s0']) /
                 (solution[self.S2] * self.rate_constants['k_fls2s0']
                  + solution[self.T1] * (self.rate_constants['k_pht1s0']
                                         + self.rate_constants['k_isct1s0'])
                  + self.S1 * (self.rate_constants['k_fls1s0']
                               + self.rate_constants['k_ics1s0']))) * 100


        QY_ic = (self.S1 * self.rate_constants['k_ics1s0'] /
                 (solution[self.S2] * self.rate_constants['k_fls2s0'] 
                  + solution[self.T1] * (self.rate_constants['k_pht1s0'] 
                                         + self.rate_constants['k_isct1s0']) 
                  + self.S1 * (self.rate_constants['k_fls1s0'] 
                               + self.rate_constants['k_ics1s0']))) * 100

        QY_isc_t1 = (self.S1 * self.rate_constants['k_iscs1t1'] /
                     (solution[self.S2] * self.rate_constants['k_fls2s0'] 
                      + solution[self.T1] * (self.rate_constants['k_pht1s0'] 
                                             + self.rate_constants['k_isct1s0']) 
                      + self.S1 * (self.rate_constants['k_fls1s0'] 
                                   + self.rate_constants['k_ics1s0']))) * 100

        QY_isc_t2 = (self.S1 * self.rate_constants['k_iscs1t2'] /
                     (solution[self.S2] * self.rate_constants['k_fls2s0'] 
                      + solution[self.T1] * (self.rate_constants['k_pht1s0'] 
                                             + self.rate_constants['k_isct1s0']) 
                      + self.S1 * (self.rate_constants['k_fls1s0'] 
                                   + self.rate_constants['k_ics1s0']))) * 100

        print(Fore.YELLOW + "\n Quantum Yield of Fluorescence (%): ")
        print(f" {QY_fl:.2f}%")


