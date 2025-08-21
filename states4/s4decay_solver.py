# -*- coding: utf-8 -*-

import sympy as sp 
import numpy as np
from colorama import Fore, Style, init
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, differential_evolution, least_squares
from .s4excitation_solver import s4ExcitationSolver

init(autoreset=True)

class s4DecaySolver:
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
            [0, k['k_fls1s0'] + k['k_ics1s0'], (k['k_pht1s0'] + k['k_isct1s0']), 0],
            [0, -(k['k_fls1s0'] + k['k_ics1s0'] + k['k_iscs1t1'] + k['k_iscs1t2']), k['k_risct1s1'], k['k_risct2s1']],
            [0, k['k_iscs1t1'], -(k['k_pht1s0'] + k['k_isct1s0'] + k['k_risct1s1'] + k['k_ict1t2']), k['k_ict2t1']],
            [0, k['k_iscs1t2'], k['k_ict1t2'], -(k['k_risct2s1'] + k['k_ict2t1'])]
        ])

        P = sp.Matrix(self.state_symbols)
        # define differential matrix equation
        dP_dt = A * P
        return A, dP_dt

    def solve_numerically(self, t_span=None, y0=None, t_eval=None, t_span_excitation=None, t_eval_excitation=None, rate_constants=None):

        icsolver = s4ExcitationSolver(time_pulse=self.time_pulse, num_photon=self.num_photon, **rate_constants)
        icsolution = icsolver.solve_numerically(t_span=t_span_excitation, t_eval=t_eval_excitation)
        S0_at_time, S1_at_time, T1_at_time, T2_at_time = icsolver.get_solution_at_time()
        y0 = [S0_at_time, S1_at_time, T1_at_time, T2_at_time] 
        
        # initial conditions
        print("\n" + Fore.YELLOW + "Initial Population for decay:")
        print(Fore.YELLOW + f"  S0 : {y0[0]:>10.3e}")
        print(Fore.YELLOW + f"  S1 : {y0[1]:>10.3e}")
        print(Fore.YELLOW + f"  T1 : {y0[2]:>10.3e}")
        print(Fore.YELLOW + f"  T2 : {y0[3]:>10.3e}\n")

        A, _ = self._define_matrix_equation()
        A_numeric = np.array(A).astype(np.float64)

        def odes(t, y):
            return A_numeric @ y

        def jac(t, y):
            return A_numeric

        # solve ODEs with Radau method
        solution = solve_ivp(
            odes,
            t_span,
            y0,
            t_eval=t_eval,
            method='Radau',
            jac=jac,
            rtol=1e-8,  
            atol=1e-13,  
            max_step=1e-8,
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

    def fit_s1_with_two_exponentials(self, t_data, s1_data, fit_path=None):

        def two_exp(t, A1, log10_tau1, A2, log10_tau2, C):
            tau1 = 10 ** log10_tau1
            tau2 = 10 ** log10_tau2
            return A1 * np.exp(-t / tau1) + A2 * np.exp(-t / tau2) + C

        def long_exp(t, A2, log10_tau2, C):
            tau2 = 10 ** log10_tau2
            return A2 * np.exp(-t / tau2) + C

        def short_exp(t, A1, log10_tau1):
            tau1 = 10 ** log10_tau1
            return A1 * np.exp(-t / tau1)

        threshold = 1e-7
        mask_long = t_data >= threshold
        mask_short = t_data <= threshold

        p2, _ = curve_fit(
            long_exp,
            t_data[mask_long], s1_data[mask_long],
            p0=[self.num_photon, np.log10(1e-6), 0],
            bounds=(
                [0, np.log10(1e-12), 0],
                [self.num_photon, np.log10(1), self.num_photon]
            )
        )
        A2_0, log10_tau2_0, C_0 = p2

        tail = long_exp(t_data, *p2)
        residual = s1_data - tail
        p1, _ = curve_fit(
            short_exp,
            t_data[mask_short], residual[mask_short],
            p0=[self.num_photon, np.log10(1e-9)],
            bounds=(
                [0, np.log10(1e-12)],
                [self.num_photon, np.log10(1)]
            )
        )
        A1_0, log10_tau1_0 = p1

        x0_init = [A1_0, log10_tau1_0, A2_0, log10_tau2_0, C_0]

        print(Fore.CYAN + "\n" + "—" * 40)
        print(Fore.CYAN + "\n Initial Two Exponential Fit:")
        print(Fore.CYAN + "\n" + "—" * 40)
        print(Fore.CYAN + "\n Model:")
        print(Fore.CYAN + "\n y = A1 * exp(-t/tau1) + A2 * exp(-t/tau2) + C")
        print(Fore.YELLOW + "\n >>> Initial fitted guess:\n", x0_init)

        bounds = [
            (0, self.num_photon),
            (np.log10(1e-12), np.log10(1)),
            (0, self.num_photon),
            (np.log10(1e-12), np.log10(1)),
            (0, self.num_photon),
        ]
        lower = np.array([b[0] for b in bounds])
        upper = np.array([b[1] for b in bounds])
        popsize = 100
        n_params = len(bounds)

        init_pop = np.random.rand(popsize, n_params)
        init_pop = lower + init_pop * (upper - lower)
        init_pop[0] = x0_init

        def loss_func(params):
            y = two_exp(t_data, *params)
            y = np.clip(y, 1e-12, None)
            s = np.clip(s1_data, 1e-12, None)
            return np.log(s) - np.log(y)

        result_global = differential_evolution(
            lambda p: np.sum(loss_func(p) ** 2),
            bounds=bounds,
            init=init_pop,
            maxiter=10000,
            popsize=popsize,
            tol=1e-8,
            seed=42,
            polish=False
        )

        result_local = least_squares(
            loss_func,
            x0=result_global.x,
            bounds=(lower, upper),
            method='trf',
            loss='soft_l1',
            ftol=1e-12,
            xtol=1e-12,
            gtol=1e-12
        )

        A1_fit, log10_tau1_fit, A2_fit, log10_tau2_fit, C_fit = result_local.x
        tau1 = 10 ** log10_tau1_fit
        tau2 = 10 ** log10_tau2_fit

        fitted_params = {
            "A1":  A1_fit,
            "tau1": tau1,
            "A2":  A2_fit,
            "tau2": tau2,
            "C":    C_fit
        }

        print(Fore.CYAN + "\n" + "—" * 40)
        print(Fore.CYAN + "\n Final Two Exponential Fit:")
        print(Fore.CYAN + "\n" + "—" * 40)
        print(Fore.CYAN + "\n Model:")
        print(Fore.CYAN + "\n y = A1 * exp(-t/tau1) + A2 * exp(-t/tau2) + C")
        print(Fore.YELLOW + "\n >>> Fitted decay parameters are:\n")

        max_len = max(len(k) for k in fitted_params)
        for key, val in fitted_params.items():
            print(f"{key.ljust(max_len)} = {val:.3e}")

        fitted_curve = two_exp(t_data, *result_local.x)
        resid = s1_data - fitted_curve
        mse = np.mean(resid ** 2)
        rmse = np.sqrt(mse)
        r_squared = 1 - np.sum(resid ** 2) / np.sum((s1_data - np.mean(s1_data)) ** 2)

        print(f"\n{'MSE:':<6}{mse:.3e}")
        print(f"{'RMSE:':<6}{rmse:.3e}")
        print(f"{'R^2:':<6}{r_squared:.3f}\n")

        plt.figure(figsize=(8, 5))
        plt.plot(t_data, s1_data, label='Actual data', color='blue')
        plt.plot(t_data, two_exp(t_data, *result_local.x),
                 label='Fitted curve', color='red', linestyle="--")
        plt.xlabel('Time (s)')
        plt.ylabel('Counts (au)')
        plt.yscale('log')
        plt.title('S1(t) Decay Fit')
        plt.legend()
        plt.grid(True)

        x_min_de, x_max_de= np.min(t_data), np.max(t_data)
        y_max_de = np.max(s1_data)
        plt.xlim(x_min_de - 0.05 * (x_max_de - x_min_de),x_max_de + 0.05 * (x_max_de - x_min_de))
        plt.ylim(1e-10, float(y_max_de * 1.05))

        if fit_path:
           plt.savefig(fit_path, dpi=300, format="pdf", bbox_inches='tight')
           print(Fore.CYAN + f"\n Fitted figure successfully saved to {fit_path} \n")
 
        return fitted_params


