import numpy as np
import matplotlib.pyplot as plt
import data_all


def data_plot(x, y, x2, y2, x_name, y_name, data_label, data_model, data_title, data_name, save_state):  # plots data
    # set number of subplots based on even or odd size of the array
    if len(x) % 2 == 0:
        fig, ax = plt.subplots(len(x) // 2, 2, figsize=(12, 5 * (len(x) // 2)))
    else:
        fig, ax = plt.subplots(len(x) // 2 + 1, 2, figsize=(12, 5 * (len(x) // 2 + 1)))

    # plot data to left or right
    for i in range(len(x)):
        index_switch = i % 2
        ax[i // 2, index_switch].plot(x[i], y[i], "rx", linewidth=1.0, label=data_label[i])
        ax[i // 2, index_switch].plot(x2[i], y2[i], 'b-', linewidth=0.8, label=data_model[i])
        ax[i // 2, index_switch].set_xlabel(x_name)
        ax[i // 2, index_switch].set_ylabel(y_name)
        ax[i // 2, index_switch].set_title(data_title[i])
        ax[i // 2, index_switch].set_yscale("log")
        ax[i // 2, index_switch].legend()
        ax[i // 2, index_switch].grid()

    # remove last empty plot if lenght is odd
    if len(x) % 2 != 0:
        for l in ax[len(x) // 2 - 1, 1].get_xaxis().get_majorticklabels():
            l.set_visible(True)
        fig.delaxes(ax[len(x) // 2, 1])

    plt.tight_layout()
    if save_state:
        plt.savefig(f"Phits_element_graph_{data_name}.pdf")
        print(f"File saved as \"Phits_element_graph_{data_name}.pdf\"")
    else:
        plt.show()


def data_convert(arr, angle, area):  # converts phits data to mb/sr
    barn_coversion = 1.0E-24 * (16.69 / 180.95 / 1.66E-024) * 1E-4
    area_tot = []
    count = []
    for a in range(len(angle)):
        area_tot.append(2 * np.pi * (1 - np.cos((angle[a] + 2.5) * np.pi / 180)))
        count.append(arr[a] * area[a])
    area_diff = [area_tot[0]]
    for b in range(len(area_tot) - 1):
        area_diff.append(area_tot[b + 1] - area_tot[b])
    count_final = []
    for c in range(len(area_diff)):
        count_final.append((count[c] / area_diff[c]) / barn_coversion)
    return count_final


def make_elemnts_graph(elem_x, elem_y, elem_phits, save_graph):
    data_x = []
    data_y = []
    data_phits_y = []
    data_phits_x = []

    # data conversion
    for i in range(len(elem_x)):
        data_x.append(elem_x[i])
        data_y.append(elem_y[i])
        if len(elem_phits[0]) == len(data_all.x_phits):
            data_phits_y.append(data_convert(elem_phits[i], data_all.x_phits, data_all.phits_area))
            data_phits_x.append(data_all.x_phits)
        else:
            data_phits_y.append(data_convert(elem_phits[i], data_all.x_phits_old, data_all.phits_area_old))
            data_phits_x.append(data_all.x_phits_old)

    data_plot(data_x, data_y, data_phits_x, data_phits_y, r"$\theta$ ($^{\circ}$)",
              r"$\mathrm{d}\sigma / \mathrm{d} \Omega$ (mb/sr)", data_all.Diff_names_exfor, data_all.Diff_names_phits,
              data_all.Diff_names_target, data_all.Diff_names_file, save_graph)
