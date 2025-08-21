# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def s3plot_kinetics(
    s3excitation_solver, s3decay_solver, t_plot_excitation, t_plot_decay, fig_path=None, data_path=None
):
    # calculate S0, S1, and T1 for excitation and decay
    S0_excitation = [s3excitation_solver.S0_sol.subs(s3excitation_solver.t, t_val) for t_val in t_plot_excitation]
    S1_excitation = [s3excitation_solver.S1_sol.subs(s3excitation_solver.t, t_val) for t_val in t_plot_excitation]
    T1_excitation = [s3excitation_solver.T1_sol.subs(s3excitation_solver.t, t_val) for t_val in t_plot_excitation]
    S0_decay = [s3decay_solver.S0_sol.subs(s3decay_solver.t, t_val) for t_val in t_plot_decay]
    S1_decay = [s3decay_solver.S1_sol.subs(s3decay_solver.t, t_val) for t_val in t_plot_decay]
    T1_decay = [s3decay_solver.T1_sol.subs(s3decay_solver.t, t_val) for t_val in t_plot_decay]

    # save data to a txt file
    with open(data_path, "w") as file:
        
        file.write("Excitation Kinetics:\n")
        file.write(f"{'Time (s)':<15}{'S0':<20}{'S1':<20}{'T1':<20}\n")
        file.write("-" * 80 + "\n")
        for t, s0, s1, t1 in zip(t_plot_excitation, S0_excitation, S1_excitation, T1_excitation):
            file.write(f"{t:<15.4e}{float(s0):<20.6e}{float(s1):<20.6e}{float(t1):<20.6e}\n")

        file.write("\nDecay Kinetics:\n")
        file.write(f"{'Time (s)':<15}{'S0':<20}{'S1':<20}{'T1':<20}\n")
        file.write("-" * 80 + "\n")
        for t, s0, s1, t1 in zip(t_plot_decay, S0_decay, S1_decay, T1_decay):
            file.write(f"{t:<15.4e}{float(s0):<20.6e}{float(s1):<20.6e}{float(t1):<20.6e}\n")

    print(f"Kinetics data successfully saved to {data_path}\n")

    plt.figure(figsize=(14, 6), facecolor='whitesmoke')

    # excitation kinetics plot
    plt.subplot(1, 2, 1)
    plt.plot(t_plot_excitation, S0_excitation, label='S0 (Excitation)', color='blue', linewidth=2)
    plt.plot(t_plot_excitation, S1_excitation, label='S1 (Excitation)', color='green', linewidth=2)
    plt.plot(t_plot_excitation, T1_excitation, label='T1 (Excitation)', color='purple', linewidth=2)
    plt.yscale('log')
    plt.title('Excitation Kinetics', fontsize=16, fontweight='bold', color='red')
    plt.xlabel('Time (s)', fontsize=14)
    plt.ylabel('Counts (au)', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12, loc='upper right', framealpha=0.8)
    plt.gca().set_facecolor('lightgrey')

    x_min_exc, x_max_exc = min(t_plot_excitation), max(t_plot_excitation)
    y_max_exc = max(max(S0_excitation), max(S1_excitation), max(T1_excitation), 1.1)
    plt.xlim(x_min_exc - 0.05 * (x_max_exc - x_min_exc), x_max_exc + 0.05 * (x_max_exc - x_min_exc))
    plt.ylim(1e-10, float(y_max_exc * 1.05))

    # decay kinetics plot
    plt.subplot(1, 2, 2)
    plt.plot(t_plot_decay, S0_decay, label='S0 (Decay)', color='blue', linewidth=2)
    plt.plot(t_plot_decay, S1_decay, label='S1 (Decay)', color='green', linewidth=2)
    plt.plot(t_plot_decay, T1_decay, label='T1 (Decay)', color='purple', linewidth=2)
    plt.yscale('log')
    plt.title('Decay Kinetics', fontsize=16, fontweight='bold', color='red')
    plt.xlabel('Time (s)', fontsize=14)
    plt.ylabel('Counts (au)', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12, loc='upper right', framealpha=0.8)
    plt.gca().set_facecolor('lightgrey')

    x_min_dec, x_max_dec = min(t_plot_decay), max(t_plot_decay)
    y_max_dec = max(max(S0_decay), max(S1_decay), max(T1_decay), 1.1)
    plt.xlim(x_min_dec - 0.05 * (x_max_dec - x_min_dec), x_max_dec + 0.05 * (x_max_dec - x_min_dec))
    plt.ylim(1e-10, float(y_max_dec * 1.05))

    plt.tight_layout()

    if fig_path:
        plt.savefig(fig_path, format='pdf', dpi=300, bbox_inches='tight')
        print(f"Figure successfully saved to {fig_path}\n")

