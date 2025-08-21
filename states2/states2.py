# -*- coding: utf-8 -*-

import os
import sys
import logging
import re
from .s2decay_solver import s2DecaySolver
from .s2excitation_solver import s2ExcitationSolver
from .s2qyd import s2QuantumYieldCalculator
from .s2plot_kinetics import s2plot_kinetics
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

# create results folder
results_folder = "results_2states"
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

def main(k_abss0s1, k_fls1s0, k_ics1s0, time_pulse, num_photon, time_excitation, time_decay):

    print_main_title("o WELCOME TO TWO STATES KINETICS CALCULATIONS o")

    # input parameters
    logger.info(Fore.RED + "\n >>> Running 2-states module with parameters:\n")
    logger.info(Fore.WHITE + f"k_abss0s1: {k_abss0s1:.2e}")
    logger.info(Fore.WHITE + f"k_fls1s0: {k_fls1s0:.2e}")
    logger.info(Fore.WHITE + f"k_ics1s0: {k_ics1s0:.2e}")

    # step 1: run excitation solver
    print_section_title("→ Step 1: Running the excitation solver")
    logger.info(Fore.CYAN + "\n >>> Solving the excitation kinetcis...\n")
    
    s2excitation_solver = s2ExcitationSolver(
        k_abss0s1=k_abss0s1,
        k_fls1s0=k_fls1s0,
        k_ics1s0=k_ics1s0,
        time_pulse=time_pulse,
        num_photon=num_photon
    ) 

    s2excitation_solver.display_c_code()
    S0_at_time, S1_at_time = s2excitation_solver.get_solution_at_time()
    logger.info(Fore.CYAN + f"\n Population after pulse duration {s2excitation_solver.time_pulse:.2e} s:")
    logger.info(Fore.CYAN + f"  S0 = {S0_at_time:.3e}")
    logger.info(Fore.CYAN + f"  S1 = {S1_at_time:.3e}")

    # step 2: run decay solver
    print_section_title("→ Step 2: Running the decay solver")
    logger.info(Fore.CYAN + "\n >>> Solving the decay kinetics...\n")

    s2decay_solver = s2DecaySolver(
        k_abss0s1=k_abss0s1,
        k_fls1s0=k_fls1s0,
        k_ics1s0=k_ics1s0,
        time_pulse=time_pulse,
        num_photon=num_photon
    )
    s2decay_solver.display_c_code()

    # step 3: run PLQY calculations
    print_section_title("→ Step 3: Running the quantum yield calculation")
    logger.info(Fore.CYAN + "\n >>> Calculating the quantum yield...\n")

    s2quantum_yield_calculator = s2QuantumYieldCalculator(
        k_abss0s1=k_abss0s1,
        k_fls1s0=k_fls1s0,
        k_ics1s0=k_ics1s0,
    )
    s2quantum_yield_calculator.display_quantum_yield()

    # step 4: plotting kinetic figures
    print_section_title("→ Step 4: Plotting kinetics")
    logger.info(Fore.CYAN + "\n >>> Generating plots for excitation and decay kinetics...\n")

    t_plot_excitation = np.logspace(-15, np.log10(time_excitation), 10000)
    t_plot_decay = np.logspace(-12, np.log10(time_decay), 10000)

    plot_file = os.path.join(results_folder, "kinetics_plot.pdf")
    data_file = os.path.join(results_folder, "kinetics_data.out")

    s2plot_kinetics(
        s2excitation_solver,
        s2decay_solver,
        t_plot_excitation,
        t_plot_decay,
        fig_path=plot_file,
        data_path=data_file,
    )

    print_main_title("o CALCULATIONS COMPLETE o")


