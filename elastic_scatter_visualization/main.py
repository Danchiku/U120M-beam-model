import numpy as np
import scipy.constants as sc
import interpolation as inter
import different_elements as diff_el
import complete_graph as graph
import different_energies as diff_en
import data_all


def raw_conversion(angle, raw, e_0, z_1, z_2):  # converts arbitrary units to mb/sr
    output = []
    for i in range(len(raw)):
        output.append((((z_1 * z_2 * sc.e) / (4 * sc.pi * sc.epsilon_0 * 4 * e_0)) ** 2 * 1 / (
                np.sin((angle[i] * np.pi / 180) / 2) ** 4)) * raw[i] * 1E+28)
    return output


if __name__ == "__main__":
    save_state = False
    Target_energy = 33  # MeV

    # Ta data import
    Ta_phits_data = [data_all.Ta_y_phits_0, data_all.Ta_y_phits_1, data_all.Ta_y_phits_2, data_all.Ta_y_phits_3,
                     data_all.Ta_y_phits_4, data_all.Ta_y_phits_5]
    Ta_exfor_border_x = [data_all.Ta_x_55, data_all.Ta_x_13]
    Ta_exfor_border_y = [data_all.Ta_y_55, data_all.Ta_y_13]
    Ta_names = data_all.Ta_names_comp

    # Interpolation Ta data import
    datasets_Ta = [
        {"Angle": np.array(data_all.Ta_x_94), "Energy": 94.8, "Cross_section": np.array(data_all.Ta_y_94)},
        {"Angle": np.array(data_all.Ta_x_57), "Energy": 57.0, "Cross_section": np.array(data_all.Ta_y_57)},
        {"Angle": np.array(data_all.Ta_x_55), "Energy": 55.0, "Cross_section": np.array(data_all.Ta_y_55)},
        {"Angle": np.array(data_all.Ta_x_13), "Energy": 13.7, "Cross_section": np.array(data_all.Ta_y_13)},
        {"Angle": np.array(data_all.Ta_x_9), "Energy": 9.7, "Cross_section": np.array(data_all.Ta_y_9)}
    ]
    Ta_names.append(f"Intepolovaných {Target_energy} MeV")

    # W data import
    W_phits_data = [data_all.W_y_phits_0, data_all.W_y_phits_1, data_all.W_y_phits_2, data_all.W_y_phits_3,
                    data_all.W_y_phits_4, data_all.W_y_phits_5, data_all.W_y_phits_6]
    W_exfor_border_x = [data_all.W_x_55, data_all.W_x_16]
    W_y_16 = raw_conversion(data_all.W_x_16, data_all.W_y_16_raw, 5.0e6, 1, 74)
    W_exfor_border_y = [data_all.W_y_55, W_y_16]
    W_names = data_all.W_names_comp

    # Interpolation W data import
    datasets_W = [
        {"Angle": np.array(data_all.W_x_65), "Energy": 65.0,
         "Cross_section": np.array(np.multiply(data_all.W_y_65, 1E-3))},
        {"Angle": np.array(data_all.W_x_55), "Energy": 55.0, "Cross_section": np.array(data_all.W_y_55)},
        {"Angle": np.array(data_all.W_x_16), "Energy": 16.0, "Cross_section": np.array(W_y_16)}
    ]
    W_names.append(f"Intepolovaných {Target_energy} MeV")

    # different elements import
    diff_elem_x = [data_all.C_32_x, data_all.Al_30_x, data_all.Cu_30_x, data_all.Au_28_x]
    diff_elem_y = [data_all.C_32_y, data_all.Al_30_y, data_all.Cu_30_y, data_all.Au_28_y]
    diff_elem_phits = [data_all.y_phits_C, data_all.y_phits_Al, data_all.y_phits_Cu, data_all.y_phits_Au]

    # different energies phits Ta
    Ta_phits_energies_Jendl = [data_all.Ta_y_phits_94, data_all.Ta_y_phits_57, data_all.Ta_y_phits_9]
    Ta_phits_energies_Tendl = [data_all.Ta_y_tendl_94, data_all.Ta_y_tendl_57, data_all.Ta_y_tendl_9]
    Ta_exfor_ener_x = [data_all.Ta_x_94, data_all.Ta_x_57, data_all.Ta_x_9]
    Ta_exfor_ener_y = [data_all.Ta_y_94, data_all.Ta_y_57, data_all.Ta_y_9]

    # Run programs
    fit_param_Ta = inter.make_inter_graph(datasets_Ta, Target_energy, ["Tantal", "Ta"], save_state)
    fit_param_W = inter.make_inter_graph(datasets_W, Target_energy, ["Wolfrám", "W"], save_state)
    graph.make_comp_graph(Ta_phits_data, Ta_exfor_border_x, Ta_exfor_border_y, fit_param_Ta, Target_energy, Ta_names,
                          data_all.Ta_labels, save_state, ["Tantal", "Phits_diff_graph_Ta"])
    graph.make_comp_graph(W_phits_data, W_exfor_border_x, W_exfor_border_y, fit_param_W, Target_energy, W_names,
                          data_all.W_labels, save_state, ["Wolfrám", "Phits_diff_graph_W"])
    diff_el.make_elemnts_graph(diff_elem_x, diff_elem_y, diff_elem_phits, save_state)
    diff_en.make_energies_graph(Ta_phits_energies_Jendl, Ta_phits_energies_Tendl, Ta_exfor_ener_x, Ta_exfor_ener_y,
                                data_all.Ta_libraries, data_all.Ta_energies, data_all.Ta_en_colors, save_state,
                                ["Tantal", "Phits_diff_energies_Ta"])
