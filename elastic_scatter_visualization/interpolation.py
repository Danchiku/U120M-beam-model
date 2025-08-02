import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as sc
from scipy.optimize import curve_fit

Angle_all, Cross_all, Energy_all = [], [], []
fit_equation = 4  # 1: angle^energy, 2: energy^angle, 3: weighted, 4: Rutherford scattering


def model(angle, a, b, c, d, energy):  # fit function
    match fit_equation:
        case 1:  # angle^(energy)
            return np.exp(a * angle ** (b * energy + d) + c)
        case 2:  # energy^(angle)
            return np.exp(a * energy ** (b * angle + d) + c)
        case 3:  # sqrt(angle^(energy) * energy^(angle))
            return np.exp(a * np.sqrt(angle ** (b * energy + d) * energy ** (b * angle + d)) + c)
        case 4:  # Rutherford scattering
            return a * ((73 * sc.e) / (8 * np.pi * sc.epsilon_0 * energy * 1E6 * np.sin(
                ((angle * b + c) / 2) * np.pi / 180) ** 2)) ** 2 * 1.0E28
        case _:
            print("Invalid fit function")


def fit_func(angle, a, b, c, d, energy_fixed):  # fit function with fixed variable
    return model(angle, a, b, c, d, energy_fixed)


def wrapped_function(angle, a, b, c, d):  # defined fit function with fixed variable
    return np.array([fit_func(angle_i, a, b, c, d, energy_i) for angle_i, energy_i in zip(angle, Energy_all)])


def make_inter_graph(data_inter, energy_target, element, save_graph):
    # combine all data into ane dataset
    for data in data_inter:
        Angle_all.extend(data["Angle"])
        Cross_all.extend(data["Cross_section"])
        Energy_all.extend([data["Energy"]] * len(data["Angle"]))

    # choose the best initial conditions
    match fit_equation:
        case 1:  # angle^(energy)
            fit_guess = [31.874, -0.002, -8.97, -0.27]
            fit_bounds = [[0.0, -1.0, -50.0, -2.0], [100.0, 1.0, 50.0, 2.0]]
        case 2:  # energy^(angle)
            fit_guess = [10, -0.01, -3.6, 0.2]
            fit_bounds = [[0.0, -1.0, -10.0, 0.0], [20.0, 1.0, -1.0, 1.0]]
        case 3:  # sqrt(angle^(energy) * energy^(angle))
            fit_guess = [12.4, -0.0197, -2.6, 0.06]
            fit_bounds = [[0.0, -1.0, -10.0, 0.0], [20.0, 0.0, 0.0, 1.0]]
        case 4:  # Rutherford scattering
            fit_guess = [0.1, 0.9, -1.0, 0.0]
            fit_bounds = [[0.01, 0.0, -10.0, 0.0], [1.0, 1.0, 0.0, 1.0]]
        case _:
            fit_guess = [0.0, 0.0, 0.0, 0.0]
            fit_bounds = [[0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 1.0, 1.0]]

    # fit two variable function
    # noinspection PyTupleAssignmentBalance
    popt, pcov = curve_fit(wrapped_function, Angle_all, Cross_all, p0=fit_guess, bounds=fit_bounds)
    print("{} fitted parameters: a = {}, b = {}, c = {}, d = {}".format(element[1], *popt))

    # plot datasets and fit
    min_angle = []
    max_angle = []
    plt.figure(figsize=(10, 6))
    for data in data_inter:
        angle_vals = data["Angle"]
        energy_fixed = data["Energy"]
        cross_vals = data["Cross_section"]

        plt.scatter(angle_vals, cross_vals, marker="x", linewidth=1.0, label=f"Dáta {energy_fixed} MeV")

        min_temp = min(angle_vals)
        max_temp = max(angle_vals)
        min_angle.append(min_temp)
        max_angle.append(max_temp)
        angle_fit = np.linspace(min_temp, max_temp, 1000)
        cross_fit = fit_func(angle_fit, *popt, energy_fixed)
        # cross_fit = fit_func(angle_fit, *fit_guess, Energy_fixed)
        plt.plot(angle_fit, cross_fit, linestyle="--", linewidth=1.0, label=f"Fit {energy_fixed} MeV")

    # plot interpolated target energy
    common_x = np.linspace(min(min_angle), max(max_angle), 1000)
    target_fit = fit_func(common_x, *popt, energy_target)
    plt.plot(common_x, target_fit, "k-", linewidth=1.0, label=f"Interpolovaných {energy_target} MeV")

    plt.legend()
    plt.xlabel(r"$\theta$ ($^{\circ}$)")
    plt.ylabel(r"$\mathrm{d}\sigma / \mathrm{d} \Omega$ (mb/sr)")
    plt.yscale("log")
    plt.title(f"{element[0]} - Interpolácia pre {energy_target} MeV")
    plt.grid(True)
    plt.legend(loc="upper right")
    if save_graph:
        plt.savefig(f"Interpolation_{energy_target}_MeV_{element[1]}_all.pdf")
        print(f"File saved as \"Interpolation_{energy_target}_MeV_{element[1]}_all.pdf\"")
    else:
        plt.show()
    return popt
