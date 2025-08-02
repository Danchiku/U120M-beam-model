import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def data_read(file_name, line_start, line_end, split_char, flatten):  # read file
    matrix_data = []
    try:
        with open(file_name, "r") as f:
            file = f.readlines()
            for i in range(line_start - 1, line_end):
                line = file[i]
                temp = []
                values = line.strip().split(split_char)
                values = list(filter(None, values))
                for item in values:  # load all columns
                    temp.append(np.float64(item))
                matrix_data.append(temp)
        print(f"Loaded file \"{file_name}\"")
        f.close()
        if flatten:
            matrix_data = sum(matrix_data, [])
        return np.array(matrix_data)
    except FileNotFoundError:
        print(f"File \"{file_name}\" not found")


def data_plot(x, y, x_name, y_name, data_label, data_title, data_name, plot_type, save_state):  # plots data
    fig, ax = plt.subplots(figsize=(10, 6))

    for i in range(len(x)):
        if plot_type == "line":
            ax.plot(x[i], y[i], linewidth=1.0, label=data_label[i])
        else:
            diff = (x[i][1] - x[i][0]) / 2
            edges = np.linspace(x[i][0] - diff, x[i][-1] + diff, len(x[i]) + 1)
            # ax.bar(x[i], y[i], width=x[i][1] - x[i][0], edgecolor="white", linewidth=0.7, label=data_label[i])
            ax.stairs(y[i], edges, label=data_label[i])

    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    match plot_type:
        case "line":
            ax.set_xscale('log')
            # ax.set_yscale('log')
        case "stairs":
            ax.set_yscale('log')
            ax.set_xlim(0, 33.0)

    plt.legend()
    # plt.tight_layout()
    plt.grid()
    plt.title(data_title)
    if save_state:
        plt.savefig(f"{data_name}.pdf")
        print(f"File saved as \"{data_name}.pdf\"")
    else:
        plt.show()


def flux_calculation(matrix, surface):  # Correct unit calculation
    flux = 0
    error = np.zeros(len(matrix))
    bin_width = matrix[0, 1] - matrix[0, 0]
    for i in range(len(matrix)):
        flux += bin_width * matrix[i, 2]  # bin size * flux to integrate
        error[i] = matrix[i, 3] * matrix[i, 2] * bin_width
    total_error = np.sqrt(np.sum(np.square(error)))
    return flux * surface, total_error * surface


def double_bins(matrix):  # doubles bin width for better statistic
    temp = []
    for i in range(0, len(matrix), 2):
        try:
            temp.append([matrix[i, 1], matrix[i, 2] + matrix[i + 1, 2]])
        except IndexError:
            pass
    return np.array(temp)


def deposit_error(matrix, errors):  # Calculates sum of all pixels and total absolute error
    absolute_errors = matrix * errors
    total_error = np.sqrt(np.sum(np.square(absolute_errors)))
    total_values = np.sum(matrix)
    return total_values, total_error


if __name__ == "__main__":
    save = False
    particles = 10 * 30 * 1E9
    detector_surface = 1.408 * 4  # cm^2

    # Flux data
    data_flux_30 = data_read("deg30/xy_cross_en_spect_TPX3_sum10_deg30.out", 106, 205, " ", False)
    data_flux_45 = data_read("deg45/xy_cross_en_spect_TPX3_sum10_deg45.out", 106, 205, " ", False)
    data_flux_60 = data_read("deg60/xy_cross_en_spect_TPX3_sum.out", 106, 205, " ", False)

    flux_30_p, flux_error_30_p = flux_calculation(data_flux_30, detector_surface)
    flux_45_p, flux_error_45_p = flux_calculation(data_flux_45, detector_surface)
    flux_60_p, flux_error_60_p = flux_calculation(data_flux_60, detector_surface)

    # Deposited energy data for all particles
    data_energy_30 = data_read("deg30/deposit_TPX3_sum10_deg30.out", 186, 6739, " ", True)
    data_energy_error_30 = data_read("deg30/deposit_TPX3_sum10_deg30_err.out", 186, 6739, " ", True)
    data_energy_45 = data_read("deg45/deposit_TPX3_sum10_deg45.out", 186, 6739, " ", True)
    data_energy_error_45 = data_read("deg45/deposit_TPX3_sum10_deg45_err.out", 186, 6739, " ", True)
    data_energy_60 = data_read("deg60/deposit_TPX3_sum.out", 186, 6739, " ", True)
    data_energy_error_60 = data_read("deg60/deposit_TPX3_sum_err.out", 186, 6739, " ", True)

    deposit_30, error_30 = deposit_error(data_energy_30, data_energy_error_30)
    deposit_45, error_45 = deposit_error(data_energy_45, data_energy_error_45)
    deposit_60, error_60 = deposit_error(data_energy_60, data_energy_error_60)

    # Deposited energy data for protons
    data_energy_30_p = data_read("deg30/deposit_TPX3_sum10_deg30.out", 9112, 15665, " ", True)
    data_energy_error_30_p = data_read("deg30/deposit_TPX3_sum10_deg30_err.out", 9112, 15665, " ", True)
    data_energy_45_p = data_read("deg45/deposit_TPX3_sum10_deg45.out", 9112, 15665, " ", True)
    data_energy_error_45_p = data_read("deg45/deposit_TPX3_sum10_deg45_err.out", 9112, 15665, " ", True)
    data_energy_60_p = data_read("deg60/deposit_TPX3_sum.out", 9112, 15665, " ", True)
    data_energy_error_60_p = data_read("deg60/deposit_TPX3_sum_err.out", 9112, 15665, " ", True)

    deposit_30_p, error_30_p = deposit_error(data_energy_30_p, data_energy_error_30_p)
    deposit_45_p, error_45_p = deposit_error(data_energy_45_p, data_energy_error_45_p)
    deposit_60_p, error_60_p = deposit_error(data_energy_60_p, data_energy_error_60_p)

    # Experiment data
    spectrum_table = pd.read_excel("TPX3_spectrum.xlsx", sheet_name="Energy_Spectra", usecols="F,H,I", nrows=204)
    spectrum_table = spectrum_table.to_numpy()

    print("--------------------------------------------------------------")

    print(f"Proton flux 30deg = {flux_30_p} +- {flux_error_30_p} 1/proton")
    print(f"Proton flux 45deg = {flux_45_p} +- {flux_error_45_p} 1/proton")
    print(f"Proton flux 60deg = {flux_60_p} +- {flux_error_60_p} 1/proton")

    print("--------------------------------------------------------------")

    print(f"Deposited energy 30deg - all = {deposit_30} +- {error_30} MeV/proton")
    print(f"Deposited energy 45deg - all = {deposit_45} +- {error_45} MeV/proton")
    print(f"Deposited energy 60deg - all = {deposit_60} +- {error_60} MeV/proton")

    print("--------------------------------------------------------------")

    print(f"Deposited energy 30deg - protons = {deposit_30_p} +- {error_30_p} MeV/proton")
    print(f"Deposited energy 45deg - protons = {deposit_45_p} +- {error_45_p} MeV/proton")
    print(f"Deposited energy 60deg - protons = {deposit_60_p} +- {error_60_p} MeV/proton")

    flux_doublebin_30 = double_bins(data_flux_30)
    flux_doublebin_45 = double_bins(data_flux_45)
    flux_doublebin_60 = double_bins(data_flux_60)

    data_plot([flux_doublebin_30[:, 0], flux_doublebin_45[:, 0], flux_doublebin_60[:, 0]],
              [flux_doublebin_30[:, 1], flux_doublebin_45[:, 1], flux_doublebin_60[:, 1]], r"$E$ (MeV)",
              r"$\Phi$ (1/cm$^{2}$/MeV/proton)", ["30 stupňov", "45 stupňov", "60 stupňov"],
              "Energetické spektrum fluencie protónov pre pozície detektoru", "proton_flux_all", "stairs", save)

    data_plot([spectrum_table[:, 0], spectrum_table[:, 0]], [spectrum_table[:, 1], spectrum_table[:, 2]], r"$E$ (keV)",
              r"$N$ (#)", ["Všetky častice", "Protóny"], "Spektrum deponovanej energie častíc na detektore",
              "det_flux_all", "line", save)
