# IMPORT STATEMENTS
from matplotlib.figure import Figure
import matplotlib
# matplotlib.use("GTKAgg")


def plotSubplot(axis, x1, y1, x2, y2, x_axis_title, y_axis_title, subplot_title):
    axis.plot(x1, y1)
    axis.plot(x2, y2)
    axis.set_title(subplot_title)
    axis.legend(["Unfiltered", "Filtered"])
    axis.set_xlabel(x_axis_title)
    axis.set_ylabel(y_axis_title)


def movavg_filter(df, temp_title, disp_title, load_title, mov_avg_set, datapoints, fluke_check=False, fluke_temp_title=""):
    ################################################# SATISFACTION LOOP ###########################################
    # Checking user satisfaction with filter
    for measurement in mov_avg_set:

        if measurement.lower() == 'temperature':
            number_of_points = datapoints["MTS Temperature"]
            df['MTS Temperature Moving Average'] = df[temp_title].rolling(window=number_of_points).mean()
            if fluke_check:
                number_of_points = datapoints["Fluke Temperature"]
                df['Fluke Temperature Moving Average'] = df[fluke_temp_title].rolling(window=number_of_points).mean()

        if measurement.lower() == 'load':
            number_of_points = datapoints["Load"]
            df['Load Moving Average'] = df[load_title].rolling(window=number_of_points).mean()

        if measurement.lower() == 'displacement':
            number_of_points = datapoints["Displacement"]
            df['Displacement Moving Average'] = df[disp_title].rolling(window=number_of_points).mean()

        if measurement == 'all':
            number_of_points = datapoints["MTS Temperature"]
            df['MTS Temperature Moving Average'] = df[temp_title].rolling(window=number_of_points).mean()
            if fluke_check:
                number_of_points = datapoints["Fluke Temperature"]
                df['Fluke Temperature Moving Average'] = df[fluke_temp_title].rolling(window=number_of_points).mean()

            number_of_points = datapoints["Load"]
            df['Load Moving Average'] = df[load_title].rolling(window=number_of_points).mean()

            number_of_points = datapoints["Displacement"]
            df['Displacement Moving Average'] = df[disp_title].rolling(window=number_of_points).mean()

    # Plotting
    mts_temp = df[temp_title].tolist()
    if fluke_check:
        fluke_temp = df[fluke_temp_title].tolist()
    extension = df[disp_title]
    load = df[load_title]
    mts_figure = Figure()
    both_figure = Figure()


    # DONE
    if mov_avg_set == {'temperature', 'load'}:
        filtered_temp = df['MTS Temperature Moving Average']
        filtered_load = df['Load Moving Average']

        ax1 = mts_figure.add_subplot(131)
        plotSubplot(ax1, mts_temp, load, filtered_temp, filtered_load, "MTS Temperature", "Load",
                    "Filtered Load and Filtered MTS Temperature")

        ax2 = mts_figure.add_subplot(132)
        plotSubplot(ax2, mts_temp, load, mts_temp, filtered_load, "MTS Temperature", "Load",
                    "Filtered Load and Unfiltered MTS Temperature")

        ax3 = mts_figure.add_subplot(133)
        plotSubplot(ax3, mts_temp, load, filtered_temp, load, "MTS Temperature", "Load",
                    "Unfiltered Load and Filtered MTS Temperature")
        if fluke_check:
            filtered_fluke_temp = df["Fluke Temperature Moving Average"]
            ax4 = both_figure.add_subplot(131)
            plotSubplot(ax4, fluke_temp, load, filtered_fluke_temp, filtered_load, "Fluke Temperature", "Load",
                        "Filtered Load and Filtered Fluke Temperature")

            ax5 = both_figure.add_subplot(132)
            plotSubplot(ax5, fluke_temp, load, fluke_temp, filtered_load, "Fluke Temperature", "Load",
                        "Filtered Load and Unfiltered Fluke Temperature")

            ax6 = both_figure.add_subplot(133)
            plotSubplot(ax6, fluke_temp, load, filtered_fluke_temp, load, "Fluke Temperature", "Load",
                        "Unfiltered Load and Filtered Fluke Temperature")

    # DONE
    if mov_avg_set == {'temperature', 'displacement'}:
        filtered_temp = df['MTS Temperature Moving Average']
        filtered_extension = df['Displacement Moving Average']

        ax1 = mts_figure.add_subplot(131)
        plotSubplot(ax1, mts_temp, extension, filtered_temp, filtered_extension, "MTS Temperature",
                    "Displacement", "Filtered Extension and Filtered MTS Temperature")

        ax2 = mts_figure.add_subplot(132)
        plotSubplot(ax2, mts_temp, extension, mts_temp, filtered_extension, "MTS Temperature",
                    "Displacement", "Filtered Extension and Unfiltered MTS Temperature")

        ax3 = mts_figure.add_subplot(133)
        plotSubplot(ax3, mts_temp, extension, filtered_temp, extension, "MTS Temperature",
                    "Displacement", "Unfiltered Extension and Filtered MTS Temperature")
        if fluke_check:
            filtered_fluke_temp = df["Fluke Temperature Moving Average"]

            ax4 = both_figure.add_subplot(131)
            plotSubplot(ax4, fluke_temp, extension, filtered_fluke_temp, filtered_extension, "Fluke Temperature"
                        , "Displacement", "Filtered Extension and Filtered Fluke Temperature")

            ax5 = both_figure.add_subplot(132)
            plotSubplot(ax5, fluke_temp, extension, fluke_temp, filtered_extension, "Fluke Temperature"
                        , "Displacement", "Filtered Extension and Unfiltered Fluke Temperature")

            ax6 = both_figure.add_subplot(133)
            plotSubplot(ax6, fluke_temp, extension, filtered_fluke_temp, extension, "Fluke Temperature"
                        , "Displacement", "Unfiltered Extension and Filtered Fluke Temperature")
        #plt.show()

    # DONE
    if mov_avg_set == {'all'}:
        filtered_temp = df['MTS Temperature Moving Average']
        filtered_extension = df['Displacement Moving Average']
        filtered_load = df['Load Moving Average']

        ax1 = mts_figure.add_subplot(231)
        plotSubplot(ax1, mts_temp, extension, filtered_temp, filtered_extension, "MTS Temperature",
                    "Displacement", "Filtered Displacement and Filtered MTS Temperature")

        ax2 = mts_figure.add_subplot(232)
        plotSubplot(ax2, mts_temp, extension, mts_temp, filtered_extension, "MTS Temperature",
                    "Displacement", "Filtered Displacement and Unfiltered MTS Temperature")

        ax3 = mts_figure.add_subplot(233)
        plotSubplot(ax3, mts_temp, extension, filtered_temp, extension, "MTS Temperature",
                    "Displacement", "Unfiltered Displacement and Filtered MTS Temperature")

        ax4 = mts_figure.add_subplot(234)
        plotSubplot(ax4, mts_temp, load, filtered_temp, filtered_load, "MTS Temperature",
                    "Load", "Filtered Load and Filtered MTS Temperature")

        ax5 = mts_figure.add_subplot(235)
        plotSubplot(ax5, mts_temp, load, mts_temp, filtered_load, "MTS Temperature",
                    "Load", "Filtered Load and Unfiltered MTS Temperature")

        ax6 = mts_figure.add_subplot(236)
        plotSubplot(ax6, mts_temp, load, filtered_temp, load, "MTS Temperature",
                    "Load", "Unfiltered Load and Filtered MTS Temperature")
        if fluke_check:
            filtered_fluke_temp = df["Fluke Temperature Moving Average"]

            mx1 = both_figure.add_subplot(231)
            plotSubplot(mx1, fluke_temp, extension, filtered_fluke_temp, filtered_extension, "Fluke Temperature"
                        , "Displacement", "Filtered Displacement and Filtered Fluke Temperature")

            mx2 = both_figure.add_subplot(232)
            plotSubplot(mx2, fluke_temp, extension, fluke_temp, filtered_extension, "Fluke Temperature"
                        , "Displacement", "Filtered Displacement and Unfiltered Fluke Temperature")

            mx3 = both_figure.add_subplot(233)
            plotSubplot(mx3, fluke_temp, extension, filtered_fluke_temp, extension, "Fluke Temperature"
                        , "Displacement", "Unfiltered Displacement and Filtered Fluke Temperature")

            mx4 = both_figure.add_subplot(234)
            plotSubplot(mx4, fluke_temp, load, filtered_fluke_temp, filtered_load, "Fluke Temperature"
                        , "Load", "Filtered Load and Filtered Fluke Temperature")

            mx5 = both_figure.add_subplot(235)
            plotSubplot(mx5, fluke_temp, load, fluke_temp, filtered_load, "Fluke Temperature"
                        , "Load", "Filtered Load and Unfiltered Fluke Temperature")

            mx6 = both_figure.add_subplot(236)
            plotSubplot(mx6, fluke_temp, load, filtered_fluke_temp, load, "Fluke Temperature"
                        , "Load", "Unfiltered Load and Filtered Fluke Temperature")

        # DONE
    if mov_avg_set == {'load', 'displacement'}:
        filtered_load = df["Load Moving Average"]
        filtered_extension = df['Displacement Moving Average']

        ax1 = mts_figure.add_subplot(121)
        plotSubplot(ax1, mts_temp, extension, mts_temp, filtered_extension, "MTS Temperature", "Displacement",
                    "Filtered Displacement and MTS Temperature")

        ax2 = mts_figure.add_subplot(122)
        plotSubplot(ax2, mts_temp, load, mts_temp, filtered_load, "MTS Temperature", "Load",
                    "Filtered Load and MTS Temperature")
        if fluke_check:
            ax3 = both_figure.add_subplot(121)
            plotSubplot(ax3, fluke_temp, extension, fluke_temp, filtered_extension, "Fluke Temperature",
                        "Displacement",
                        "Filtered Displacement and Fluke Temperature")

            ax4 = both_figure.add_subplot(122)
            plotSubplot(ax4, fluke_temp, load, fluke_temp, filtered_load, "Fluke Temperature",
                        "Load",
                        "Filtered Load and Fluke Temperature")

    # DONE
    if mov_avg_set == {'load'}:
        filtered_load = df["Load Moving Average"]

        ax1 = mts_figure.add_subplot(111)
        plotSubplot(ax1, mts_temp, load, mts_temp, filtered_load, "MTS Temperature", "Load",
                    "Filtered Load and MTS Temperature")
        if fluke_check:
            ax2 = both_figure.add_subplot(111)
            plotSubplot(ax2, fluke_temp, load, fluke_temp, filtered_load, "Fluke Temperature", "Load",
                        "Filtered Load and Fluke Temperature")

    # DONE
    if mov_avg_set == {'displacement'}:
        filtered_extension = df['Displacement Moving Average']

        ax1 = mts_figure.add_subplot(111)
        plotSubplot(ax1, mts_temp, extension, mts_temp, filtered_extension, "MTS Temperature", "Displacement",
                    "Filtered Displacement and MTS Temperature")
        if fluke_check:
            ax2 = both_figure.add_subplot(111)
            plotSubplot(ax2, fluke_temp, extension, fluke_temp, filtered_extension, "Fluke Temperature",
                        "Displacement",
                        "Filtered Displacement and Fluke Temperature")

    if mov_avg_set == {'temperature'}:
        filtered_temp = df['MTS Temperature Moving Average']

        ax1 = mts_figure.add_subplot(121)
        plotSubplot(ax1, mts_temp, extension, filtered_temp, extension, "MTS Temperature", "Displacement",
                    "Displacement and Filtered MTS Temperature")

        ax2 = mts_figure.add_subplot(122)
        plotSubplot(ax2, mts_temp, load, filtered_temp, load, "MTS Temperature", "Load",
                    "Load and Filtered MTS Temperature")
        if fluke_check:
            fluke_filtered_temp = df["Fluke Temperature Moving Average"]
            ax3 = both_figure.add_subplot(121)
            plotSubplot(ax3, fluke_temp, extension, fluke_filtered_temp, extension, "Fluke Temperature",
                        "Displacement", "Displacment and Filtered Fluke Temperature")

            ax4 = both_figure.add_subplot(122)
            plotSubplot(ax4, fluke_temp, load, fluke_filtered_temp, load, "Fluke Temperature", "Load",
                        "Load and Filtered Fluke Temperature")
        #plt.show()

            satisfaction = "yes"

    if fluke_check:
        return mts_figure, both_figure
    else:
        return mts_figure
