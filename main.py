# -*- coding: utf-8 -*-

import os
import importlib
import sys
import inspect
from colorama import Fore, Style, init
from art import text2art

init(autoreset=True)
author_info = """
{0}Author: {1}Yue(Steven) He{2} and {1}Daniel Escudero
{0}Affiliation: {3}Computational Photochemistry Lab, KU Leuven
""".format(Fore.CYAN, Fore.LIGHTYELLOW_EX, Fore.WHITE, Fore.GREEN)

# set the module paths for 2 states, 3 states, 4 states and 5 states
sys.path.append(os.path.join(os.getcwd(), 'states2'))
sys.path.append(os.path.join(os.getcwd(), 'states3'))
sys.path.append(os.path.join(os.getcwd(), 'states4'))
sys.path.append(os.path.join(os.getcwd(), 'states5'))


def print_kinluv_logo():
    ascii_art = text2art("KinLuv", font="ogre")
    colors = [Fore.RED, Fore.LIGHTYELLOW_EX, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.LIGHTCYAN_EX, Fore.MAGENTA]
    colored_art = ""
    color_index = 0
    for char in ascii_art:
        if char != '\n':  
            colored_art += f"{colors[color_index % len(colors)]}{char}{Style.RESET_ALL}"
            color_index += 1
        else:
            colored_art += char  
    print(colored_art)

def run_module(module_name, params=None):
    try:
        module = importlib.import_module(module_name)
        print(f"Module {module_name} imported successfully")

        if hasattr(module, 'main'):
            print(f"Found main function in {module_name}")
            main_func = module.main

            if params:
                sig = inspect.signature(main_func)
                valid_keys = sig.parameters.keys()
                filtered_params = {k: v for k, v in params.items() if k in valid_keys}
                main_func(**filtered_params)
            else:
                main_func()
        else:
            print(f"{module_name} does not have a 'main' function")
    except Exception as e:
        print(f"Error importing module {module_name}: {e}")

def get_2states_params():
    print("\nPlease enter the parameters for the 2-states module:")

    k_abss0s1 = float(input("k_abss0s1 (e.g., 1.00E+13): "))
    k_fls1s0 = float(input("k_fls1s0 (e.g., 1.00E+07): "))
    k_ics1s0 = float(input("k_ics1s0 (e.g., 1.00E+07): "))
    time_pulse = float(input("time_pulse (e.g., 1.00E-11): "))
    num_photon = float(input("num_photon (e.g., 1): "))
    time_excitation = float(input("time_excitation (e.g., 1.00E-09): "))
    time_decay = float(input("time_decay (e.g., 1.00E-03): "))

    return {
        'k_abss0s1': k_abss0s1,
        'k_fls1s0': k_fls1s0,
        'k_ics1s0': k_ics1s0,
        'time_pulse' : time_pulse,
        'num_photon' : num_photon,
        'time_excitation' : time_excitation,
        'time_decay' : time_decay
    }

def get_3states_params():
    print("\nPlease enter the parameters for the 3-states module:")

    k_abss0s1 = float(input("k_abss0s1 (e.g., 1.00E+13): "))
    k_fls1s0 = float(input("k_fls1s0 (e.g., 1.00E+07): "))
    k_ics1s0 = float(input("k_ics1s0 (e.g., 1.00E+07): "))
    k_iscs1t1 = float(input("k_iscs1t1 (e.g., 1.00E+07): "))
    k_risct1s1 = float(input("k_risct1s1 (e.g., 1.00E+05): "))
    k_isct1s0 = float(input("k_isct1s0 (e.g., 1.00E+04): "))
    k_pht1s0 = float(input("k_pht1s0 (e.g., 1.00E+02): "))
    time_pulse = float(input("time_pulse (e.g., 1.00E-11): "))
    num_photon = float(input("num_photon (e.g., 1): "))
    time_excitation = float(input("time_excitation (e.g., 1.00E-09): "))
    time_decay = float(input("time_decay (e.g., 1.00E-03): "))

    return {
        'k_abss0s1': k_abss0s1,
        'k_fls1s0': k_fls1s0,
        'k_ics1s0': k_ics1s0,
        'k_iscs1t1': k_iscs1t1,
        'k_risct1s1': k_risct1s1,
        'k_isct1s0': k_isct1s0,
        'k_pht1s0': k_pht1s0,
        'time_pulse' : time_pulse,
        'num_photon' : num_photon,
        'time_excitation' : time_excitation,
        'time_decay' : time_decay
    }

def get_4states_params():
    print("\nPlease enter the parameters for the 4-states module:")

    k_abss0s1 = float(input("k_abss0s1 (e.g., 1.00E+13): "))
    k_iscs1t1 = float(input("k_iscs1t1 (e.g., 1.00E+07): "))
    k_iscs1t2 = float(input("k_iscs1t2 (e.g., 1.00E+07): "))
    k_isct1s0 = float(input("k_isct1s0 (e.g., 1.00E+04): "))
    k_risct1s1 = float(input("k_risct1s1 (e.g., 1.00E+05): "))
    k_risct2s1 = float(input("k_risct2s1 (e.g., 1.00E+05): "))
    k_fls1s0 = float(input("k_fls1s0 (e.g., 1.00E+07): "))
    k_ics1s0 = float(input("k_ics1s0 (e.g., 1.00E+07): "))
    k_ict2t1 = float(input("k_ict2t1 (e.g., 1.00E+12): "))
    k_ict1t2 = float(input("k_ict1t2 (e.g., 0.00E+00): "))
    k_pht1s0 = float(input("k_pht1s0 (e.g., 1.00E+02): "))
    time_pulse = float(input("time_pulse (e.g., 1.00E-11): "))
    num_photon = float(input("num_photon (e.g., 1): "))
    time_excitation = float(input("time_excitation (e.g., 1.00E-09): "))
    time_decay = float(input("time_decay (e.g., 1.00E-03): "))

    return {
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
        'time_pulse' : time_pulse,
        'num_photon' : num_photon,
        'time_excitation' : time_excitation,
        'time_decay' : time_decay
    }

def get_5states_params():
    print("\nPlease enter the parameters for the 5-states module:")

    k_abss0s2 = float(input("k_abss0s2 (e.g., 1.00E+13): "))
    k_iscs1t1 = float(input("k_iscs1t1 (e.g., 1.00E+07): "))
    k_iscs1t2 = float(input("k_iscs1t2 (e.g., 1.00E+07): "))
    k_iscs2t1 = float(input("k_iscs2t1 (e.g., 1.00E+07): "))
    k_iscs2t2 = float(input("k_iscs2t2 (e.g., 1.00E+07): "))
    k_isct1s0 = float(input("k_isct1s0 (e.g., 1.00E+04): "))
    k_risct1s1 = float(input("k_risct1s1 (e.g., 1.00E+05): "))
    k_risct1s2 = float(input("k_risct1s2 (e.g., 1.00E+06): "))
    k_risct2s1 = float(input("k_risct2s1 (e.g., 1.00E+05): "))
    k_risct2s2 = float(input("k_risct2s2 (e.g., 1.00E+05): "))
    k_fls1s0 = float(input("k_fls1s0 (e.g., 1.00E+07): "))
    k_fls2s0 = float(input("k_fls2s0 (e.g., 0.00E+00): "))
    k_ics1s0 = float(input("k_ics1s0 (e.g., 1.00E+07): "))
    k_ics2s1 = float(input("k_ics2s1 (e.g., 1.00E+12): "))
    k_ics1s2 = float(input("k_ics1s2 (e.g., 0.00E+00): "))
    k_ict2t1 = float(input("k_ict2t1 (e.g., 1.00E+12): "))
    k_ict1t2 = float(input("k_ict1t2 (e.g., 0.00E+00): "))
    k_pht1s0 = float(input("k_pht1s0 (e.g., 1.00E+02): "))
    time_pulse = float(input("time_pulse (e.g., 1.00E-11): "))
    num_photon = float(input("num_photon (e.g., 1): "))
    time_excitation = float(input("time_excitation (e.g., 1.00E-09): "))
    time_decay = float(input("time_decay (e.g., 1.00E-03): "))

    return {
        'k_abss0s2': k_abss0s2,
        'k_iscs1t1': k_iscs1t1,
        'k_iscs1t2': k_iscs1t2,
        'k_iscs2t1': k_iscs2t1,
        'k_iscs2t2': k_iscs2t2,
        'k_isct1s0': k_isct1s0,
        'k_risct1s1': k_risct1s1,
        'k_risct1s2': k_risct1s2,
        'k_risct2s1': k_risct2s1,
        'k_risct2s2': k_risct2s2,
        'k_fls1s0': k_fls1s0,
        'k_fls2s0': k_fls2s0,
        'k_ics1s0': k_ics1s0,
        'k_ics2s1': k_ics2s1,
        'k_ics1s2': k_ics1s2,
        'k_ict2t1': k_ict2t1,
        'k_ict1t2': k_ict1t2,
        'k_pht1s0': k_pht1s0,
        'time_pulse' : time_pulse,
        'num_photon' : num_photon,
        'time_excitation' : time_excitation,
        'time_decay' : time_decay
    }

def read_params_from_inp(filepath):
    params = {}
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().rstrip(',') 
                try:
                    value = float(value)
                except ValueError:
                    raise ValueError(f"Parameter '{key}' has an invalid numeric value: {value}")
                params[key] = value
    return params

def get_params_from_inp():
    filepath = input("Enter the path to the *.inp file: ").strip()
    try:
        params = read_params_from_inp(filepath)
        print("Parameters loaded from file successfully.")
        return params
    except Exception as e:
        print(Fore.RED + f"Error reading input file: {e}")
        sys.exit(1)

def main():
    print_kinluv_logo()
    print(author_info)
    print(Fore.CYAN + "\nWelcome to KinLuv!\n")
    print(Fore.MAGENTA + "KinLuv provides the following modules for the kinetic calculations") 
    print(Fore.YELLOW + "a. 2-states")
    print(Fore.YELLOW + "b. 3-states")
    print(Fore.YELLOW + "c. 4-states")
    print(Fore.YELLOW + "d. 5-states")
    
    module_choice = input(Fore.MAGENTA + "Enter the number of the module you want to use: ")
    input_choice = input("Which way do you want to input parameters: (F)ile or (M)anual? ").strip().lower()

    if input_choice == 'f':
        params = get_params_from_inp()
    elif input_choice == 'm':
        if module_choice == 'a':
            params = get_2states_params()
        elif module_choice == 'b':
            params = get_3states_params()
        elif module_choice == 'c':
            params = get_4states_params()
        elif module_choice == 'd':
            params = get_5states_params()
        else:
            print(Fore.RED + "Invalid module choice. Please choose a, b, c, or d.")
            return
    else:
        print(Fore.RED + "Invalid input method. Please choose F or M.")
        return

    if module_choice == 'a':
        run_module('states2', params)
    elif module_choice == 'b':
        run_module('states3', params)
    elif module_choice == 'c':
        run_module('states4', params)
    elif module_choice == 'd':
        run_module('states5', params)
    else:
        print(Fore.RED + "Invalid module choice. Please choose a, b, c, or d.")

if __name__ == "__main__":
    main()

