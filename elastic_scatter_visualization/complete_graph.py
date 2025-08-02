import numpy as np
import matplotlib.pyplot as plt
import data_all
import interpolation as inter


def data_plot(x, y, x_name, y_name, data_type, data_label, data_title, data_name, save_state):  # plots data
    fig, ax = plt.subplots(figsize=(10, 6))

    for i in range(len(x)):
        ax.plot(x[i], y[i], data_type[i], linewidth=1.0, label=data_label[i])

    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    ax.set_yscale('log')

    plt.legend()
    # plt.tight_layout()
    plt.grid()
    plt.title(data_title)
    if save_state:
        plt.savefig(f"{data_name}.pdf")
        print(f"File saved as \"{data_name}.pdf\"")
    else:
        plt.show()


def data_convert(arr, angle, area):  # converts phits data to mb/sr
    barn_coversion = 1.0E-24 * (16.69 / 180.95 / 1.66E-024) * 0.01
    area_tot = []
    count = []
    for i in range(len(angle)):
        area_tot.append(2 * np.pi * (1 - np.cos((angle[i] + 2.5) * np.pi / 180)))
        count.append(arr[i] * area[i])
    area_diff = [area_tot[0]]
    for i in range(len(area_tot) - 1):
        area_diff.append(area_tot[i + 1] - area_tot[i])
    count_final = []
    for i in range(len(area_diff)):
        count_final.append((count[i] / area_diff[i]) / barn_coversion)
    return count_final


def make_comp_graph(ta_data, border_x, border_y, fit_params, energy_target, names, labels, save_graph, graph_name):
    phits_data_corr = []
    x_phits_all = []

    # data conversion
    for data in ta_data:
        if len(data) == len(data_all.x_phits):
            phits_data_corr.append(data_convert(data, data_all.x_phits, data_all.phits_area))
            x_phits_all.append(data_all.x_phits)
        else:
            phits_data_corr.append(data_convert(data, data_all.x_phits_old, data_all.phits_area_old))
            x_phits_all.append(data_all.x_phits_old)



    # create data for target energy
    common_x = np.linspace(5, np.max(border_x[1]), 1000)
    target_y = inter.fit_func(common_x, *fit_params, energy_target)

    data_x = [border_x[0], *x_phits_all, border_x[1], common_x]
    data_y = [border_y[0], *phits_data_corr, border_y[1], target_y]
    data_plot(data_x, data_y, r"$\theta$ ($^{\circ}$)", r"$\mathrm{d}\sigma / \mathrm{d} \Omega$ (mb/sr)", labels,
              names, *graph_name, save_graph)
