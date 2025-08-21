# -*- coding: utf-8 -*-

import sympy as sp
from colorama import init, Fore, Style

init(autoreset=True)

class s2ExcitationSolver:
    def __init__(self, k_abss0s1=None, k_fls1s0=None, k_ics1s0=None, time_pulse=None, num_photon=None):
        self.t = sp.symbols('t')
        self.k_abss0s1 = sp.Symbol('k_abss0s1', positive=True)
        self.k_fls1s0 = sp.Symbol('k_fls1s0', positive=True)
        self.k_ics1s0 = sp.Symbol('k_ics1s0', positive=True)
        
        # assign values
        self.k_abss0s1 = k_abss0s1
        self.k_fls1s0 = k_fls1s0
        self.k_ics1s0 = k_ics1s0
        self.time_pulse = time_pulse
        self.num_photon = num_photon
        
        # define functions
        self.S0 = sp.Function('S0')(self.t)
        self.S1 = sp.Function('S1')(self.t)
        
        self.S0_sol = None
        self.S1_sol = None
        self.S0_limit = None
        self.S1_limit = None

    def _build_ode_equations(self):
        eq1 = sp.Eq(
            self.S0.diff(self.t), -self.k_abss0s1 * self.S0 + (self.k_fls1s0 + self.k_ics1s0) * self.S1
        )
        eq2 = sp.Eq(
            self.S1.diff(self.t), self.k_abss0s1 * self.S0 - (self.k_fls1s0 + self.k_ics1s0) * self.S1
        )
        return [eq1, eq2]

    def solve_odes(self):
        odes = self._build_ode_equations()
        # initial conditions
        ics = {
            self.S0.subs(self.t, 0): self.num_photon, self.S1.subs(self.t, 0): 0
        }
        solution = sp.dsolve(odes, ics=ics)
        
        self.S0_sol = solution[0].rhs
        self.S1_sol = solution[1].rhs
        
        self._substitute_values()

    def _substitute_values(self):
        if self.S0_sol is None or self.S1_sol is None:
            self.solve_odes()
        
        if self.k_abss0s1 is not None:
            self.S0_sol = self.S0_sol.subs(self.k_abss0s1, self.k_abss0s1)
            self.S1_sol = self.S1_sol.subs(self.k_abss0s1, self.k_abss0s1)
        
        if self.k_fls1s0 is not None:
            self.S0_sol = self.S0_sol.subs(self.k_fls1s0, self.k_fls1s0)
            self.S1_sol = self.S1_sol.subs(self.k_fls1s0, self.k_fls1s0)
        
        if self.k_ics1s0 is not None:
            self.S0_sol = self.S0_sol.subs(self.k_ics1s0, self.k_ics1s0)
            self.S1_sol = self.S1_sol.subs(self.k_ics1s0, self.k_ics1s0)
        
        self.S0_sol = sp.simplify(self.S0_sol).evalf()
        self.S1_sol = sp.simplify(self.S1_sol).evalf()

    def calculate_limits(self):
        # calculate population limits as time goes to infinity
        self.S0_limit = sp.limit(self.S0_sol, self.t, sp.oo).evalf()
        self.S1_limit = sp.limit(self.S1_sol, self.t, sp.oo).evalf()

    def display_c_code(self):
        self.solve_odes()
        self.calculate_limits()
        
        expressions = {
                'S0(t)': self.S0_sol,
                'S1(t)': self.S1_sol,
        }

        print(Fore.YELLOW + "\n >>>  Analytic expression of population evolution: \n")
        for label, expr in expressions.items():
                print(f" {label}:")
                print(f" {sp.ccode(expr)} \n")

        limits = {
                'S0(infinity)': self.S0_limit,
                'S1(infinity)': self.S1_limit,
        }

        print(Fore.YELLOW + "\n >>> Analytic expression of population at infinity: \n")

        for label, expr in limits.items():
                print(f" {label}:")
                print(f" {sp.ccode(expr)} \n")

    def get_solution_at_time(self):
        if self.time_pulse is None:
            raise ValueError("Please set a valid pulse time.")
        
        if self.S0_sol is None or self.S1_sol is None:
            self.solve_odes()
        
        S0_at_time = self.S0_sol.subs(self.t, self.time_pulse).evalf()
        S1_at_time = self.S1_sol.subs(self.t, self.time_pulse).evalf()
        
        return S0_at_time, S1_at_time

