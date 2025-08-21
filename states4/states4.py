# -*- coding: utf-8 -*-

import os
import sys
import logging
import re
from .s4decay_solver import s4DecaySolver
from .s4excitation_solver import s4ExcitationSolver
from .s4qyd import s4QuantumYieldCalculator  
from .s4plot_kinetics import s4plot_kinetics
from colorama import Fore, Style, init
import numpy as np

class Tee(object):
    ANSI_ESCAPE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]') 

    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            if hasattr(f, 'name') and 'log' in f.name:
                clean_obj = self.ANSI_ESCAPE.sub('', obj)
                f.write(clean_obj)
            else:
                f.write(obj)
            f.flush()

    def flush(self):
        for f in self.files:
            f.flush()

results_folder = "results_4states"
os.makedirs(results_folder, exist_ok=True)

log_file_path = os.path.join(results_folder, 'log')
log_file = open(log_file_path, 'w', encoding='utf-8')
sys.stdout = Tee(sys.stdout, log_file)

init(autoreset=True)
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

if logger.hasHandlers():
    logger.handlers.clear()

file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
file_handler.setLevel(logging.INFO)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def print_main_title(title: str, color_outer=Fore.RED, color_inner=Fore.RED):
    width = 80
    pad = 4
    inner_width = width - pad * 2

    top_border = color_outer + "┌" + "─" * (width - 2) + "┐"
    bottom_border = color_outer + "└" + "─" * (width - 2) + "┘"
    empty_line = color_outer + "│" + " " * (width - 2) + "│"
    title_line = color_inner + "│" + " " * pad + title.center(inner_width) + " " * pad + "│"

    logger.info("\n" + top_border)
    logger.info(empty_line)
    logger.info(empty_line)
    logger.info(title_line)
    logger.info(empty_line)
    logger.info(empty_line)
    logger.info(bottom_border + "\n")

def print_section_title(title: str, color=Fore.GREEN):
    width = 80
    line = color + "─" * width
    empty_line = color + "│" + " " * (width - 2) + "│"
    title_line = color + title.center(width)

    logger.info("\n" + line)
    logger.info(empty_line)
    logger.info(title_line)
    logger.info(empty_line)
    logger.info(line + "\n")

def main(
    k_abss0s1, k_iscs1t1, k_iscs1t2, k_isct1s0,
    k_risct1s1, k_risct2s1, k_fls1s0,
    k_ics1s0, k_ict2t1, k_ict1t2, k_pht1s0, time_pulse, num_photon, time_excitation, time_decay 
):
    rate_constants = {
        'k_abss0s1': k_abss0s1,
        'k_iscs1t1': k_iscs1t1,
        'k_iscs1t2': k_iscs1t2,
        'k_isct1s0': k_isct1s0,
        'k_risct1s1': k_risct1s1,
        'k_risct2s1': k_risct2s1,
        'k_fls1s0': k_fls1s0,
        'k_ics1s0': k_ics1s0,
        'k_ict2t1': k_ict2t1,
        'k_ict1t2': k_ict1t2,
        'k_pht1s0': k_pht1s0,
    }

    print_main_title("o WELCOME TO FOUR STATES KINETICS CALCULATIONS o")

    logger.info(Fore.RED + "\n >>> Running 4-states module with the following parameters: \n")
    for key, value in rate_constants.items():
        logger.info(Fore.WHITE + f"{key}: {value:.2e}")

    # step 1: run excitation solver
    print_section_title("→ Step 1: Running the excitation solver")
    logger.info(Fore.CYAN + "\n >>> Solving the excitation kinetics...\n")

    s4excitation_solver = s4ExcitationSolver(time_pulse, num_photon, **rate_constants)
    # define time span and initial conditions for excitation
    t_span_excitation = (0, time_excitation)  
    t_eval_excitation = np.logspace(-15, np.log10(time_excitation), 10000)  

    solution_excitation = s4excitation_solver.solve_numerically(t_span=t_span_excitation, t_eval=t_eval_excitation)
    s4excitation_solver.display_results()
    S0_at_time, S1_at_time, T1_at_time, T2_at_time = s4excitation_solver.get_solution_at_time()
    logger.info(Fore.CYAN + f"\n Population after pulse duration {s4excitation_solver.time_pulse:.2e} s:")
    logger.info(Fore.CYAN + f"  S0 = {S0_at_time:.3e}")
    logger.info(Fore.CYAN + f"  S1 = {S1_at_time:.3e}")
    logger.info(Fore.CYAN + f"  T1 = {T1_at_time:.3e}")
    logger.info(Fore.CYAN + f"  T2 = {T2_at_time:.3e}\n")

    # step 2: run decay solver
    print_section_title("→ Step 2: Running the decay solver")
    logger.info(Fore.CYAN + "\n >>> Solving the decay kinetics...\n")

    s4decay_solver = s4DecaySolver(time_pulse, num_photon, **rate_constants)

    # define time span and initial conditions for decay
    t_span_decay = (0, time_decay)
    t_fast = np.logspace(-12, -7, 10000)  
    t_low = np.logspace(-7, np.log10(time_decay), 10000)  
    t_eval_decay = np.unique(np.concatenate((t_fast, t_low)))

    solution_decay = s4decay_solver.solve_numerically(
        t_span=t_span_decay,
        t_eval=t_eval_decay,
        t_span_excitation=t_span_excitation,
        t_eval_excitation=t_eval_excitation,
        rate_constants=rate_constants
    )
    s4decay_solver.display_results()

    # fit S1 decay using exponentials
    fit_file = os.path.join(results_folder, "decay_fit.pdf")
    s4decay_solver.fit_s1_with_two_exponentials(solution_decay.t, solution_decay.y[1], fit_path=fit_file)  

    # step 3: run PLQY calculations
    print_section_title("→ Step 3: Running the quantum yield calculation")
    logger.info(Fore.CYAN + "\n >>> Calculating the quantum yield...")

    s4qyd_calculator = s4QuantumYieldCalculator(rate_constants)
    s4qyd_calculator.calculate_quantum_yield()  

    # step 4: plotting kinetic figures
    print_section_title("→ Step 4: Plotting kinetics")
    logger.info(Fore.CYAN + "\n >>> Generating plots for excitation and decay kinetics...\n")

    plot_file = os.path.join(results_folder, "kinetics_plot.pdf")
    data_file = os.path.join(results_folder, "kinetics_data.out")

    s4plot_kinetics(solution_excitation, solution_decay, fig_path=plot_file, data_path=data_file)

    print_main_title("o CALCULATIONS COMPLETE o")


