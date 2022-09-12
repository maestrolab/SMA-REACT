# IMPORT STATEMENTS
import matplotlib.pyplot as plt
import numpy as np


def plot_temp_vs_strain(df, temperature_title, fluke_check=False, fluke_temp_title=""):
    alpha_val = 1 / (max(df["Cycle"].tolist()) + 1)
    plt.subplot(1, 2, 1)
    for i in range(max(df["Cycle"].tolist()) + 1):
        cycle_df = df.loc[df['Cycle'] == i]
        temps = cycle_df[temperature_title].to_numpy()
        strain = cycle_df["Strain"].to_numpy()

        cool_heat_cutoff = np.argmin(temps)
        cooling_temps = temps[0:cool_heat_cutoff]
        cooling_strain = strain[0:cool_heat_cutoff]
        heating_temps = temps[cool_heat_cutoff:]
        heating_strain = strain[cool_heat_cutoff:]
        # for j in range(len(cooling_temps)-1, 0, -1):
        #     if cooling_temps[j] > cooling_temps[j-1]:
        #         cooling_temps = np.delete(cooling_temps, j)
        #         cooling_strain = np.delete(cooling_strain, j)
        # close_index_list = []
        # print(cooling_temps)
        # print(cooling_strain)
        # for z in range(20):
        #     distance = np.sqrt((cooling_strain[z+1]-cooling_strain[z])**2 + (cooling_temps[z+1]-cooling_temps[z])**2)
        #     distance = cooling_strain[z+1] - cooling_strain[z]
        #     print(distance)
        #     if distance <= 0.0001:
        #         close_index_list.append(z)
        # print(close_index_list)

        plt.plot(cooling_temps, cooling_strain, color="blue", alpha= (i + 1) * alpha_val, label="Cycle {}".format(i+1))
        plt.plot(heating_temps, heating_strain, color="red", alpha= (i + 1) * alpha_val, label="Cycle {}".format(i+1))
    plt.xlabel("MTS Temperature (°C)")
    plt.ylabel("Strain")
    plt.legend(loc="best")
    if fluke_check:
        plt.subplot(1, 2, 2)
        for i in range(max(df["Cycle"].tolist()) + 1):
            cycle_df = df.loc[df['Cycle'] == i]
            temps = cycle_df[fluke_temp_title].to_numpy()
            strain = cycle_df["Strain"].to_numpy()

            cool_heat_cutoff = np.argmin(temps)
            cooling_temps = temps[0:cool_heat_cutoff]
            cooling_strain = strain[0:cool_heat_cutoff]
            heating_temps = temps[cool_heat_cutoff:]
            heating_strain = strain[cool_heat_cutoff:]

            plt.plot(cooling_temps, cooling_strain, color="blue", alpha= (i + 1) * alpha_val, label="Cycle {}".format(i+1))
            plt.plot(heating_temps, heating_strain, color="red", alpha= (i + 1) * alpha_val, label="Cycle {}".format(i+1))
        plt.xlabel("Fluke Temperature (°C)")
        plt.ylabel("Strain")
        plt.legend(loc="best")
    plt.suptitle("Temperature vs. Strain")
    plt.show()