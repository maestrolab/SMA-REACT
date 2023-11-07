# IMPORT STATEMENTS
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
# matplotlib.use("GTKAgg")

def plotColorbars(fig, axis, alpha_val, cycle_count):
    cbar_red = plt.cm.ScalarMappable(cmap="Reds", norm=plt.Normalize(vmin=0, vmax=1))
    cbar = fig.colorbar(cbar_red, label="Cycle", orientation="vertical", shrink=0.6, ax=axis)
    cbar.set_ticks([x * alpha_val for x in range(1, cycle_count + 1)])
    cbar.set_ticklabels([x for x in range(1, cycle_count + 1)])
    cbar_blue = plt.cm.ScalarMappable(cmap="Blues", norm=plt.Normalize(vmin=0, vmax=1))
    cbar = fig.colorbar(cbar_blue, orientation="vertical", shrink=0.6, pad=0.15, ax=axis)
    cbar.set_ticks([x * alpha_val for x in range(1, cycle_count + 1)])
    cbar.set_ticklabels([x for x in range(1, cycle_count + 1)])


def plotSST(df, temp_title, stress_title, bandpass, no_cycles, fluke_check = False, fluke_temp_title = ""):
    # creating figure
    fig = plt.figure()
    if fluke_check:
        ax = fig.add_subplot(121, projection='3d')
    else:
        ax = fig.add_subplot(111, projection="3d")

    # temperature units
    if "(" in temp_title:
        temp_units = temp_title[temp_title.index("("):]
    else:
        temp_units = "(C)"

    # axes labels
    ax.set_xlabel("MTS Temperature {}".format(temp_units))
    ax.set_ylabel("Strain")
    ax.set_zlabel(stress_title)

    # plotting without cycles
    if no_cycles:
        if bandpass:
            strain = df["Filtered Strain"]
        else:
            strain = df["Strain"]
        ax.plot(df[temp_title], strain, df[stress_title])

    else:
        # transparency
        cycle_count = df["Cycle"].max() + 1
        min_cycle = df["Cycle"].min()
        alpha_val = 1 / (cycle_count - min_cycle)

        # check if colorbar is needed
        colorbar = False
        if cycle_count >= 5:
            colorbar = True

        # plotting
        for i in range(min_cycle, cycle_count):
            cycle_df = df.loc[df['Cycle'] == i]
            temps = cycle_df[temp_title].to_numpy()
            if bandpass:
                strain = cycle_df["Filtered Strain"].to_numpy()
            else:
                strain = cycle_df["Strain"].to_numpy()
            stresses = cycle_df[stress_title].to_numpy()

            cool_heat_cutoff = np.nanargmin(temps)
            cooling_temps = temps[0:cool_heat_cutoff + 1]
            cooling_strain = strain[0:cool_heat_cutoff + 1]
            heating_temps = temps[cool_heat_cutoff:]
            heating_strain = strain[cool_heat_cutoff:]
            cooling_stress = stresses[0:cool_heat_cutoff + 1]
            heating_stress = stresses[cool_heat_cutoff:]

            if not colorbar:
                ax.plot(cooling_temps, cooling_strain, cooling_stress, color="blue", alpha= (i - min_cycle + 1) * alpha_val, label="Cycle {}".format(i+1))
                ax.plot(heating_temps, heating_strain, heating_stress, color="red", alpha= (i - min_cycle + 1) * alpha_val, label="Cycle {}".format(i+1))
            else:
                ax.plot(cooling_temps, cooling_strain, cooling_stress, color="blue", alpha=(i - min_cycle + 1) * alpha_val)
                ax.plot(heating_temps, heating_strain, heating_stress, color="red", alpha=(i - min_cycle + 1) * alpha_val)

        # colorbar
        if not colorbar:
            ax.legend(loc="best")
        else:
            plotColorbars(fig, ax, alpha_val, cycle_count)

    # same thing for fluke if needed
    if fluke_check:
        ax2 = fig.add_subplot(122, projection="3d")

        # temperature units
        if "(" in fluke_temp_title:
            temp_units = fluke_temp_title[fluke_temp_title.index("("):]
        else:
            temp_units = "(C)"

        # axes labels
        ax2.set_xlabel("Fluke Temperature {}".format(temp_units))
        ax2.set_ylabel("Strain")
        ax2.set_zlabel(stress_title)

        if no_cycles:
            if bandpass:
                strain = df["Filtered Strain"]
            else:
                strain = df["Strain"]
            ax2.plot(df[fluke_temp_title], strain, df[stress_title])
        else:
            for i in range(min_cycle, cycle_count):
                cycle_df = df.loc[df['Cycle'] == i]
                temps = cycle_df[fluke_temp_title].to_numpy()
                if bandpass:
                    strain = cycle_df["Filtered Strain"].to_numpy()
                else:
                    strain = cycle_df["Strain"].to_numpy()
                stresses = cycle_df[stress_title].to_numpy()

                cool_heat_cutoff = np.nanargmin(temps)
                cooling_temps = temps[0:cool_heat_cutoff + 1]
                cooling_strain = strain[0:cool_heat_cutoff + 1]
                heating_temps = temps[cool_heat_cutoff:]
                heating_strain = strain[cool_heat_cutoff:]
                cooling_stress = stresses[0:cool_heat_cutoff + 1]
                heating_stress = stresses[cool_heat_cutoff:]

                if not colorbar:
                    ax2.plot(cooling_temps, cooling_strain, cooling_stress, color="blue", alpha=(i - min_cycle + 1) * alpha_val,
                            label="Cycle {}".format(i + 1))
                    ax2.plot(heating_temps, heating_strain, heating_stress, color="red", alpha=(i - min_cycle + 1) * alpha_val,
                            label="Cycle {}".format(i + 1))
                else:
                    ax2.plot(cooling_temps, cooling_strain, cooling_stress, color="blue", alpha=(i - min_cycle + 1) * alpha_val)
                    ax2.plot(heating_temps, heating_strain, heating_stress, color="red", alpha=(i - min_cycle + 1) * alpha_val)

            # colorbar
            if not colorbar:
                ax2.legend(loc="best")
            else:
                plotColorbars(fig, ax2, alpha_val, cycle_count)

    fig.suptitle("Temperature vs. Strain vs. Stress")
    return fig