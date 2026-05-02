# -*- coding: utf-8 -*-

import sympy as sp
from colorama import init, Fore, Style

init(autoreset=True)

class s3ExcitationSolver:
    def __init__(self, k_abss0s1=None, k_fls1s0=None, k_ics1s0=None, k_iscs1t1=None, k_risct1s1=None, k_isct1s0=None, k_pht1s0=None, time_pulse=None, num_photon=None):
        self.t = sp.symbols('t')

        # assign values
        self.k_abss0s1 = k_abss0s1
        self.k_fls1s0 = k_fls1s0
        self.k_ics1s0 = k_ics1s0
        self.k_iscs1t1 = k_iscs1t1
        self.k_risct1s1 = k_risct1s1
        self.k_isct1s0 = k_isct1s0
        self.k_pht1s0 = k_pht1s0
        self.time_pulse = time_pulse
        self.num_photon = num_photon

        # define functions
        self.S0 = sp.Function('S0')(self.t)
        self.S1 = sp.Function('S1')(self.t)
        self.T1 = sp.Function('T1')(self.t)

        self.S0_sol = None
        self.S1_sol = None
        self.T1_sol = None
        self.S0_limit = None
        self.S1_limit = None
        self.T1_limit = None

    def _define_ode_equations(self):
        eq1 = sp.Eq(
            self.S0.diff(self.t),
            self.T1 * (self.k_isct1s0 + self.k_pht1s0) - self.S0 * self.k_abss0s1 + self.S1 * (self.k_fls1s0 + self.k_ics1s0)
        )
        eq2 = sp.Eq(
            self.S1.diff(self.t),
            self.S0 * self.k_abss0s1 - self.S1 * (self.k_fls1s0 + self.k_ics1s0 + self.k_iscs1t1) + self.T1 * self.k_risct1s1
        )
        eq3 = sp.Eq(
            self.T1.diff(self.t),
            self.S1 * self.k_iscs1t1 - self.T1 * (self.k_risct1s1 + self.k_isct1s0 + self.k_pht1s0)
        )
        return [eq1, eq2, eq3]

    def solve_odes(self):
        odes = self._define_ode_equations()
        # initial conditions 
        ics = {
            self.S0.subs(self.t, 0): self.num_photon,  
            self.S1.subs(self.t, 0): 0,  
            self.T1.subs(self.t, 0): 0  
        }

        solution = sp.dsolve(odes, ics=ics)

        self.S0_sol = solution[0].rhs  
        self.S1_sol = solution[1].rhs  
        self.T1_sol = solution[2].rhs  

        self.simplify_solutions()

    def simplify_solutions(self):
        self.S0_sol = sp.simplify(self.S0_sol).evalf()
        self.S1_sol = sp.simplify(self.S1_sol).evalf()
        self.T1_sol = sp.simplify(self.T1_sol).evalf()

    def calculate_limits(self):
        self.S0_limit = sp.limit(self.S0_sol, self.t, sp.oo).evalf()
        self.S1_limit = sp.limit(self.S1_sol, self.t, sp.oo).evalf()
        self.T1_limit = sp.limit(self.T1_sol, self.t, sp.oo).evalf()

    def display_c_code(self):
        self.solve_odes()  
        self.calculate_limits()  

        expressions = {
                'S0(t)': self.S0_sol,
                'S1(t)': self.S1_sol,
                'T1(t)': self.T1_sol,
        }

        print(Fore.YELLOW + "\n >>>  Analytic expression of population evolution: \n")
        for label, expr in expressions.items():
                print(f" {label}:")
                print(f" {sp.ccode(expr)} \n")

        limits = {
                'S0(infinity)': self.S0_limit,
                'S1(infinity)': self.S1_limit,
                'T1(infinity)': self.T1_limit,
        }

        print(Fore.YELLOW + "\n >>> Analytic expression of population at infinity: \n")

        for label, expr in limits.items():
                print(f" {label}:")
                print(f" {sp.ccode(expr)} \n")

    def get_excitation_limits(self):
        self.solve_odes()  
        self.calculate_limits()  
        return self.S0_limit, self.S1_limit, self.T1_limit  

    def get_solution_at_time(self):
        if self.time_pulse is None:
            raise ValueError("Please set a valid pulse time.")

        if self.S0_sol is None or self.S1_sol is None or self.T1_sol is None:
            self.solve_odes()

        S0_at_time = self.S0_sol.subs(self.t, self.time_pulse).evalf()
        S1_at_time = self.S1_sol.subs(self.t, self.time_pulse).evalf()
        T1_at_time = self.T1_sol.subs(self.t, self.time_pulse).evalf()

        return S0_at_time, S1_at_time, T1_at_time


