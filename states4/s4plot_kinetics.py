# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import numpy as np

def s4plot_kinetics(solution_excitation, solution_decay, fig_path=None, data_path=None):

    if data_path:
        with open(data_path, "w") as file:
            file.write("Excitation Kinetics:\n")
            file.write(f"{'Time (s)':<15}{'S0':<20}{'S1':<20}{'T1':<20}{'T2':<20}\n")
            file.write("-" * 80 + "\n")
            for t, s0, s1, t1, t2 in zip(solution_excitation.t, solution_excitation.y[0], solution_excitation.y[1], solution_excitation.y[2],
                                              solution_excitation.y[3]):
                file.write(f"{t:<15.4e}{float(s0):<20.6e}{float(s1):<20.6e}{float(t1):<20.6e}{float(t2):<20.6e}\n")

            file.write("\nDecay Kinetics:\n")
            file.write(f"{'Time (s)':<15}{'S0':<20}{'S1':<20}{'T1':<20}{'T2':<20}\n")
            file.write("-" * 80 + "\n")
            for t, s0, s1, t1, t2 in zip(solution_decay.t, solution_decay.y[0], solution_decay.y[1], solution_decay.y[2],
                                              solution_decay.y[3]):
                file.write(f"{t:<15.4e}{float(s0):<20.6e}{float(s1):<20.6e}{float(t1):<20.6e}{float(t2):<20.6e}\n")

        print(f"Kinetics data successfully saved to {data_path}\n")

    plt.figure(figsize=(14, 6), facecolor='whitesmoke') 

    plt.subplot(1, 2, 1)
    for idx, state in enumerate(['S0', 'S1', 'T1', 'T2']):
        plt.plot(solution_excitation.t, solution_excitation.y[idx], label=f'{state}(Excitation)', linewidth=2)

    plt.title('Excitation Kinetics', fontsize=16, fontweight='bold', color='red')
    plt.xlabel('Time (s)', fontsize=14)
    plt.ylabel('Counts (au)', fontsize=14)
    plt.yscale('log')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12, loc='upper right', framealpha=0.8)
    plt.gca().set_facecolor('lightgrey')

    x_min_exc, x_max_exc = min(solution_excitation.t), max(solution_excitation.t)
    y_max_exc = max(np.max(solution_excitation.y[0]), np.max(solution_excitation.y[1]), np.max(solution_excitation.y[2]),
                    np.max(solution_excitation.y[3]),  1.1)

    plt.xlim(x_min_exc - 0.05 * (x_max_exc - x_min_exc), x_max_exc + 0.05 * (x_max_exc - x_min_exc))
    plt.ylim(1e-10, float(y_max_exc * 1.05))  

    plt.subplot(1, 2, 2)
    for idx, state in enumerate(['S0', 'S1', 'T1', 'T2']):
        plt.plot(solution_decay.t, solution_decay.y[idx], label=f'{state}(Decay)', linewidth=2)

    plt.title('Decay Kinetics', fontsize=16, fontweight='bold', color='red')
    plt.xlabel('Time (s)', fontsize=14)
    plt.ylabel('Counts (au)', fontsize=14)
    plt.yscale('log')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12, loc='upper right', framealpha=0.8)
    plt.gca().set_facecolor('lightgrey')

    x_min_de, x_max_de = min(solution_decay.t), max(solution_decay.t)
    y_max_de = max(np.max(solution_decay.y[0]), np.max(solution_decay.y[1]), np.max(solution_decay.y[2]),
                    np.max(solution_decay.y[3]), 1.1)

    plt.xlim(x_min_de - 0.05 * (x_max_de - x_min_de), x_max_de + 0.05 * (x_max_de - x_min_de))
    plt.ylim(1e-10, float(y_max_de * 1.05)) 

    plt.tight_layout()

    if fig_path:
        plt.savefig(fig_path, dpi=300, format="pdf", bbox_inches='tight')  
        print(f"Figure successfully saved to {fig_path}\n")

