# IMPORT STATEMENTS
import matplotlib.pyplot as plt
import numpy as np

# plots the two colorbars given the figure
def plotColorbars(figure, axis, alpha_val, cycle_count):
    cbar_red = plt.cm.ScalarMappable(cmap="Reds", norm=plt.Normalize(vmin=0, vmax=1))
    cbar = figure.colorbar(cbar_red, label="Cycle", orientation="vertical", pad=0.0, ax=axis)
    cbar.set_ticks([x * alpha_val for x in range(1, cycle_count + 1)])
    cbar.set_ticklabels([x for x in range(1, cycle_count + 1)])
    cbar.ax.yaxis.set_ticks_position("left")
    cbar.ax.yaxis.set_label_position("left")
    cbar_blue = plt.cm.ScalarMappable(cmap="Blues", norm=plt.Normalize(vmin=0, vmax=1))
    cbar2 = figure.colorbar(cbar_blue, orientation="vertical", pad=0.0, ax=axis)
    cbar2.set_ticks([x * alpha_val for x in range(1, cycle_count + 1)])
    cbar2.set_ticklabels([x for x in range(1, cycle_count + 1)])


# finds the first non nan value in a pandas series
def firstAndLastNonNAN(x_series, y_series):
    first = 0
    last = -1
    for i in range(max(len(x_series), len(y_series))):
        if not np.isnan(x_series.iloc[i]) and not np.isnan(y_series.iloc[i]):
            first = i
            break
    for j in range(len(x_series) - 1, -1, -1):
        if not np.isnan(x_series.iloc[j]) and not np.isnan(y_series.iloc[j]):
            last = j
            break
    return first, last


def plot_temp_vs_strain(df, temperature_title, bandpass_choice, no_cycles, fluke_check=False, fluke_temp_title=""):
    # creating the figure
    fig1 = plt.figure()
    if fluke_check:
        ax1 = fig1.add_subplot(121)
    else:
        ax1 = fig1.add_subplot(111)

    # colorbar error
    colorbar_error = False

    # start and end point annotations
    first_index, last_index = firstAndLastNonNAN(df[temperature_title], df["Strain"])
    ax1.text(df[temperature_title].iloc[first_index], df["Strain"].iloc[first_index], "Starting Point", ha="right")
    ax1.text(df[temperature_title].iloc[-1], df["Strain"].iloc[-1], "Ending Point", ha="right")

    # plotting without cycles
    if (no_cycles):
        if bandpass_choice:
            strain = df["Filtered Strain"]
        else:
            strain = df["Strain"]
        ax1.plot(df[temperature_title], strain)
    # plotting with cycles
    else:
        max_cycle = df["Cycle"].max() + 1
        min_cycle = df["Cycle"].min()
        alpha_val = 1 / (max_cycle - min_cycle)

        # colorbar is necessary for at least  5 cycles
        colorbar = False
        if (max_cycle) >= 5:
            colorbar = True

        # cooling and heating state
        cool_heat_flag = []

        # plotting by cycle
        for i in range(min_cycle, max_cycle):
            cycle_df = df.loc[df['Cycle'] == i]
            temps = cycle_df[temperature_title].to_numpy()
            if bandpass_choice:
                strain = cycle_df["Filtered Strain"].to_numpy()
            else:
                strain = cycle_df["Strain"].to_numpy()

            cool_heat_cutoff = np.nanargmin(temps)
            cooling_temps = temps[0:cool_heat_cutoff + 1]
            cooling_strain = strain[0:cool_heat_cutoff + 1]
            heating_temps = temps[cool_heat_cutoff:]
            heating_strain = strain[cool_heat_cutoff:]

            # recording the cooling heating state
            cool_heat_flag.extend(["Cooling" for x in range(len(cooling_temps))])
            cool_heat_flag.extend(["Heating" for x in range(len(heating_temps) - 1)])


            if not colorbar:
                ax1.plot(cooling_temps, cooling_strain, color="blue", alpha= (i - min_cycle + 1) * alpha_val, label="Cycle {}".format(i+1))
                ax1.plot(heating_temps, heating_strain, color="red", alpha= (i - min_cycle + 1) * alpha_val, label="Cycle {}".format(i+1))
            else:
                ax1.plot(cooling_temps, cooling_strain, color="blue", alpha=(i - min_cycle + 1) * alpha_val)
                ax1.plot(heating_temps, heating_strain, color="red", alpha=(i - min_cycle + 1) * alpha_val)

        if (not colorbar):
            ax1.legend(loc="best")
        else:
            try:
                plotColorbars(fig1, ax1, alpha_val, max_cycle)
            except:
                colorbar_error = True

        df.insert(1, "Cooling/Heating State", cool_heat_flag)

    # getting the units of the mts temperature
    if "(" in temperature_title:
        temp_units = temperature_title[temperature_title.index("("):]
    else:
        temp_units = "(C)"

    # axes labels
    ax1.set_xlabel("MTS Temperature {}".format(temp_units), fontname="Arial", fontsize=20)
    ax1.set_ylabel("Strain", fontname="Arial", fontsize=20)
    ax1.tick_params(axis="both", which="major", labelsize=16)
    ax1.tick_params(axis="both", which="minor", labelsize=16)


    if fluke_check:
        # new subplot for fluke
        ax2 = fig1.add_subplot(122)

        # start and end point annotations
        first_index, last_index = firstAndLastNonNAN(df[fluke_temp_title], df["Strain"])
        ax2.text(df[fluke_temp_title].iloc[first_index], df["Strain"].iloc[first_index], "Starting Point", ha="right")
        ax2.text(df[fluke_temp_title].iloc[-1], df["Strain"].iloc[-1], "Ending Point", ha="right")

        # plotting without cycles
        if (no_cycles):
            if bandpass_choice:
                strain = df["Filtered Strain"]
            else:
                strain = df["Strain"]
            ax2.plot(df[fluke_temp_title], strain)

        # plotting with cycles
        else:
            max_cycle = df["Cycle"].max() + 1
            min_cycle = df["Cycle"].min()
            alpha_val = 1 / (max_cycle - min_cycle)

            # colorbar necessary if at least 5 cycles
            colorbar = False
            if (max_cycle) >= 5:
                colorbar = True

            # plotting by cycle
            for i in range(min_cycle, max_cycle):
                cycle_df = df.loc[df['Cycle'] == i]
                temps = cycle_df[fluke_temp_title].to_numpy()
                if bandpass_choice:
                    strain = cycle_df["Filtered Strain"].to_numpy()
                else:
                    strain = cycle_df["Strain"].to_numpy()

                cool_heat_cutoff = np.nanargmin(temps)
                cooling_temps = temps[0:cool_heat_cutoff]
                cooling_strain = strain[0:cool_heat_cutoff]
                heating_temps = temps[cool_heat_cutoff:]
                heating_strain = strain[cool_heat_cutoff:]

                if not colorbar:
                    ax2.plot(cooling_temps, cooling_strain, color="blue", alpha= (i - min_cycle + 1) * alpha_val, label="Cycle {}".format(i+1))
                    ax2.plot(heating_temps, heating_strain, color="red", alpha= (i - min_cycle + 1) * alpha_val, label="Cycle {}".format(i+1))
                else:
                    ax2.plot(cooling_temps, cooling_strain, color="blue", alpha=(i - min_cycle + 1) * alpha_val)
                    ax2.plot(heating_temps, heating_strain, color="red", alpha=(i - min_cycle + 1) * alpha_val)

            if not colorbar:
                ax2.legend(loc="best")
            else:
                try:
                    plotColorbars(fig1, ax2, alpha_val, max_cycle)
                except:
                    colorbar_error = True

        # finding units for temperature (default is celsius)
        if "(" in fluke_temp_title:
            temp_units = fluke_temp_title[fluke_temp_title.index("("):]
        else:
            temp_units = "(C)"

        # axes labels
        ax2.set_xlabel("Fluke Temperature {}".format(temp_units), fontname="Arial", fontsize=20)
        ax2.set_ylabel("Strain", fontname="Arial", fontsize=20)
        ax2.tick_params(axis="both", which="major", labelsize=16)
        ax2.tick_params(axis="both", which="minor", labelsize=16)

    # title
    fig1.suptitle("Temperature vs. Strain")
    return fig1, colorbar_error
