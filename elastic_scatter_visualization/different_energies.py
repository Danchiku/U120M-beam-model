import numpy as np
import matplotlib.pyplot as plt
import data_all


def data_plot(x1, y1, y2, x, y, x_name, y_name, data_type, data_label, libs, data_title, data_name, save_state):  # plots data
    fig, ax = plt.subplots(figsize=(10, 6))

    for i in range(len(x1)):
        ax.plot(x1[i], y1[i], data_type[i] + "-", linewidth=1.0, label=(data_label[i] + ", PHITS + " + libs[0]))
        ax.plot(x1[i], y2[i], data_type[i] + "--", linewidth=1.0, label=(data_label[i] + ", PHITS + " + libs[1]))
        ax.plot(x[i], y[i], data_type[i] + "x", linewidth=1.0, label=(data_label[i] + ", EXFOR"))

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


def make_energies_graph(ta_data_1, ta_data_2, exfor_x, exfor_y, libraries, names, labels, save_graph, graph_name):
    phits_data_corr_1 = []
    phits_data_corr_2 = []
    x_phits_all = []

    # data conversion
    for i in range(len(ta_data_1)):
        if len(ta_data_1[0]) == len(data_all.x_phits):
            phits_data_corr_1.append(data_convert(ta_data_1[i], data_all.x_phits, data_all.phits_area))
            phits_data_corr_2.append(data_convert(ta_data_2[i], data_all.x_phits, data_all.phits_area))
            x_phits_all.append(data_all.x_phits)
        else:
            phits_data_corr_1.append(data_convert(ta_data_1[i], data_all.x_phits_old, data_all.phits_area_old))
            phits_data_corr_2.append(data_convert(ta_data_2[i], data_all.x_phits_old, data_all.phits_area_old))
            x_phits_all.append(data_all.x_phits_old)

    data_plot(x_phits_all, phits_data_corr_1, phits_data_corr_2, exfor_x, exfor_y, r"$\theta$ ($^{\circ}$)",
              r"$\mathrm{d}\sigma / \mathrm{d} \Omega$ (mb/sr)", labels, names, libraries, *graph_name, save_graph)
