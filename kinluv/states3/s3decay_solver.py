# -*- coding: utf-8 -*-

import sympy as sp
from colorama import init, Fore, Style
from .s3excitation_solver import s3ExcitationSolver

init(autoreset=True)  

class s3DecaySolver:
    def __init__(self, k_abss0s1=None, k_fls1s0=None, k_ics1s0=None, k_iscs1t1=None,
                 k_risct1s1=None, k_isct1s0=None, k_pht1s0=None, time_pulse=None, num_photon=None):

        self.t = sp.symbols('t', positive=True)

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
        eq1 = sp.Eq(self.S0.diff(self.t),
                     self.T1 * (self.k_isct1s0 + self.k_pht1s0)
                     + self.S1 * (self.k_fls1s0 + self.k_ics1s0))

        eq2 = sp.Eq(self.S1.diff(self.t),
                     - self.S1 * (self.k_fls1s0 + self.k_ics1s0 + self.k_iscs1t1)
                     + self.T1 * self.k_risct1s1)

        eq3 = sp.Eq(self.T1.diff(self.t),
                     self.S1 * self.k_iscs1t1
                     - self.T1 * (self.k_isct1s0 + self.k_pht1s0 + self.k_risct1s1))
        return [eq1, eq2, eq3]

    def solve_odes(self):
        exsolver = s3ExcitationSolver(k_abss0s1=self.k_abss0s1,
                                    k_fls1s0=self.k_fls1s0,
                                    k_ics1s0=self.k_ics1s0,
                                    k_iscs1t1=self.k_iscs1t1,
                                    k_risct1s1=self.k_risct1s1,
                                    k_isct1s0=self.k_isct1s0,
                                    k_pht1s0=self.k_pht1s0,
                                    time_pulse=self.time_pulse,
                                    num_photon=self.num_photon
        )

        S0_initial, S1_initial, T1_initial = exsolver.get_solution_at_time()

        odes = self._define_ode_equations()

        # initial conditions
        ics = {
            self.S0.subs(self.t, 0): S0_initial,
            self.S1.subs(self.t, 0): S1_initial,
            self.T1.subs(self.t, 0): T1_initial
        }

        print("\n" + Fore.YELLOW + "Initial Population for decay:")
        print(Fore.YELLOW + f" S0_initial: {S0_initial:>10.3e}")
        print(Fore.YELLOW + f" S1_initial: {S1_initial:>10.3e}") 
        print(Fore.YELLOW + f" T1_initial: {T1_initial:>10.3e}\n")

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
        # calculate population limits as time goes to infinity
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


