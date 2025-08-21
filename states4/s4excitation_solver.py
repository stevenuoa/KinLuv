# -*- coding: utf-8 -*-

import sympy as sp
import numpy as np
from colorama import init, Fore, Style
from scipy.integrate import solve_ivp

init(autoreset=True) 

class s4ExcitationSolver:
    def __init__(self, time_pulse=None, num_photon=None, **params):
        self.params = params
        self.t = sp.symbols('t')
        for key, value in params.items():
            setattr(self, key, value)
        self.state_symbols = sp.symbols('S0 S1 T1 T2')
        self.S0, self.S1, self.T1, self.T2 = self.state_symbols
        self.solutions = None
        self.time_pulse = time_pulse
        self.num_photon = num_photon

    def _define_matrix_equation(self):
        k = self.params  
        
        A = sp.Matrix([
	    [-k['k_abss0s1'], k['k_fls1s0'] + k['k_ics1s0'], (k['k_pht1s0'] + k['k_isct1s0']), 0],
            [k['k_abss0s1'], -(k['k_fls1s0'] + k['k_ics1s0'] + k['k_iscs1t1'] + k['k_iscs1t2']), k['k_risct1s1'], k['k_risct2s1']],
            [0, k['k_iscs1t1'], -(k['k_pht1s0'] + k['k_isct1s0'] + k['k_risct1s1'] + k['k_ict1t2']), k['k_ict2t1']],
            [0, k['k_iscs1t2'], k['k_ict1t2'], -(k['k_risct2s1'] + k['k_ict2t1'])]
	])

        P = sp.Matrix(self.state_symbols)
        # define differential matrix equation
        dP_dt = A * P
        return A, dP_dt

    def solve_numerically(self, t_span=None, y0=None, t_eval=None):
        if y0 is None:
            y0 = [self.num_photon, 0, 0, 0]  # initial conditions: [S0, S1, T1, T2]

        A, _ = self._define_matrix_equation()
        A_numeric = np.array(A).astype(np.float64)

        def odes(t, y):
            return A_numeric @ y
        
        def jac(t, y):
            return A_numeric

        # Radau to solve ODEs
        solution = solve_ivp(
            odes, 
            t_span, 
            y0, 
            t_eval=t_eval, 
            method='Radau', 
            jac=jac,
            rtol=1e-8,  
            atol=1e-13,  
            max_step=1e-12,
            dense_output=True  
        )

        if not solution.success:
            raise RuntimeError(f"ODE solver failed: {solution.message}")

        self.solutions = solution
        return solution

    def display_results(self):
        if self.solutions:
            t = self.solutions.t
            print(Fore.YELLOW + "\n >>> Numerical solution : ")
            for idx, state in enumerate(['S0', 'S1', 'T1', 'T2']):
                values = self.solutions.y[idx]
                print(Fore.YELLOW + f"\n Population evolution of state: {state} ")
                for ti, vi in zip(t[:5], values[:5]):
                    print(f"  {state}({ti:.3e} s) = {vi:.3e}")
                print("  ...")
                for ti, vi in zip(t[-5:], values[-5:]):
                    print(f"  {state}({ti:.3e} s) = {vi:.3e}")

    def get_solution_at_time(self):
        if self.time_pulse is None:
            raise ValueError("Please set a valid pulse time.")

        if self.solutions is None:
            raise RuntimeError("No solution available.")

        S0_at_time, S1_at_time, T1_at_time, T2_at_time = self.solutions.sol(self.time_pulse)

        return S0_at_time, S1_at_time, T1_at_time, T2_at_time


