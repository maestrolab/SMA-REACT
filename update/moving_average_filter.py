# IMPORT STATEMENTS
import matplotlib.pyplot as plt
import re


def movavg_filter(df, temp_title, disp_title, fluke_check=False, fluke_temp_title=""):
    ###############################################################################################################
    ###############################################################################################################
    #                                              MOVING AVERAGE FILTERS                                         #
    ###############################################################################################################
    ###############################################################################################################
    # Finding Load column
    load = ['Load', 'LOAD', 'load']  # List of possible names for Load

    for column in df:  # Finding Load column by searching all columns in dataframe
        List = column.split()
        for item in List:
            if item in load:
                key = item
                if len(item) > 1:
                    unit = List[1]
                break

    search = key + ' ' + unit
    unit = re.sub('[()]', '', unit)

    List_loads = df.loc[:, search]

    ######################################## ASKING USER WHAT THEY WANT TO FILTER #################################

    print()
    print("A moving average filter can be applied to the Load, Temperature, and Extension.")
    print()
    print("Please list the measurements from the list above to which you would like to apply a moving average filter. Type 'all' if you would like to apply the filter to all measurements, and type 'done' if you don't want to apply a moving average filter to any measurement or when you are finished: ")

    allowable_inputs = ['load', 'temperature', 'extension', 'all', 'done']
    mov_avg_set = set()

    while True:
        user_inp = input().lower()
        if user_inp.lower() == 'done':
            break
        while user_inp not in allowable_inputs:
            print()
            print('Invalid input, please type the name of one of the measurements from the list [Load, Temperature, Extension, All, Done].')
            print('Input:')
            user_inp = input().lower()
        mov_avg_set.add(user_inp)

    # metadata_dict['Filtered Measurements'] = mov_avg_set

    if 'all' in mov_avg_set:
        temp_MovAvg_points = []
        if fluke_check:
            fluke_temp_MovAvg_points = []
        ext_MovAvg_points = []
        load_MovAvg_points = []
    else:
        if 'temperature' in mov_avg_set:
            temp_MovAvg_points = []
            if fluke_check:
                fluke_temp_MovAvg_points = []
        if 'extension' in mov_avg_set:
            ext_MovAvg_points = []
        if 'load' in mov_avg_set:
            load_MovAvg_points = []

    ################################################# SATISFACTION LOOP ###########################################
    # Checking user satisfaction with filter
    if len(mov_avg_set) != 0:
        satisfaction = 'no'
        while satisfaction == 'no':

            for measurement in mov_avg_set:

                if measurement == 'temperature':
                    number_of_points = int(input('How many datapoints would you like to use for the temperature moving average? '))
                    df['MTS Temperature Moving Average'] = df[temp_title].rolling(window=number_of_points).mean()
                    temp_MovAvg_points.append(number_of_points)
                    if fluke_check:
                        number_of_points = int(input('How many datapoints would you like to use for the fluke temperature moving average? '))
                        df['Fluke Temperature Moving Average'] = df[fluke_temp_title].rolling(window=number_of_points).mean()
                        fluke_temp_MovAvg_points.append(number_of_points)

                if measurement == 'load':
                    number_of_points = int(input('How many datapoints would you like to use for the load moving average? '))
                    mv_avg_load_col_name = 'Load Moving Average (' + unit + ')'
                    df[mv_avg_load_col_name] = df[search].rolling(window=number_of_points).mean()
                    load_MovAvg_points.append(number_of_points)

                if measurement == 'extension':
                    number_of_points = int(input('How many datapoints would you like to use for the extension moving average? '))
                    df['Extension Moving Average'] = df[disp_title].rolling(window=number_of_points).mean()
                    ext_MovAvg_points.append(number_of_points)

                if measurement == 'all':
                    number_of_points = int(input('How many datapoints would you like to use for the temperature moving average? '))
                    temp_MovAvg_points.append(number_of_points)
                    df['MTS Temperature Moving Average'] = df[temp_title].rolling(window=number_of_points).mean()
                    if fluke_check:
                        number_of_points = int(input('How many datapoints would you like to use for the fluke temperature moving average? '))
                        df['Fluke Temperature Moving Average'] = df[fluke_temp_title].rolling(window=number_of_points).mean()
                        fluke_temp_MovAvg_points.append(number_of_points)

                    number_of_points = int(input('How many datapoints would you like to use for the load moving average? '))
                    load_MovAvg_points.append(number_of_points)
                    mv_avg_load_col_name = 'Load Moving Average (' + unit + ')'
                    df[mv_avg_load_col_name] = df[search].rolling(window=number_of_points).mean()

                    number_of_points = int(input('How many datapoints would you like to use for the extension moving average? '))
                    ext_MovAvg_points.append(number_of_points)
                    df['Extension Moving Average'] = df[disp_title].rolling(window=number_of_points).mean()

            # Plotting different scenarios so user can say if they are satisfied
            mts_temp = df[temp_title].tolist()
            if fluke_check:
                fluke_temp = df[fluke_temp_title].tolist()
                filtered_fluke_temp = df["Fluke Temperature Moving Average"]
            extension = df[disp_title]
            load = df[search]


            # DONE
            if mov_avg_set == {'temperature', 'load'}:
                filtered_temp = df['MTS Temperature Moving Average']
                filtered_load = df[mv_avg_load_col_name]
                plt.subplot(2, 3, 1)
                plt.plot(mts_temp, load)
                plt.plot(filtered_temp, filtered_load)
                plt.legend(["Unfiltered", "Filtered"])
                plt.title("Filtered Load and Filtered MTS Temperature")
                plt.xlabel("MTS Temperature [C]")
                plt.ylabel(f"Load [{unit}]")
                plt.subplot(2, 3, 2)
                plt.plot(mts_temp, load)
                plt.plot(mts_temp, filtered_load)
                plt.legend(["Unfiltered", "Filtered"])
                plt.title("Filtered Load and Unfiltered MTS Temperature")
                plt.xlabel("MTS Temperature [C]")
                plt.ylabel(f"Load [{unit}]")
                plt.subplot(2, 3, 3)
                plt.plot(mts_temp, load)
                plt.plot(filtered_temp, load)
                plt.legend(["Unfiltered", "Filtered"])
                plt.title("Unfiltered Load and Filtered MTS Temperature")
                plt.xlabel("MTS Temperature [C]")
                plt.ylabel(f"Load [{unit}]")
                if fluke_check:
                    plt.subplot(2, 3, 4)
                    plt.plot(fluke_temp, load)
                    plt.plot(filtered_fluke_temp, filtered_load)
                    plt.legend(["Unfiltered", "Filtered"])
                    plt.title("Filtered Load and Filtered Fluke Temperature")
                    plt.xlabel("Fluke Temperature [C]")
                    plt.ylabel(f"Load [{unit}]")
                    plt.subplot(2, 3, 5)
                    plt.plot(fluke_temp, load)
                    plt.plot(fluke_temp, filtered_load)
                    plt.legend(["Unfiltered", "Filtered"])
                    plt.title("Filtered Load and Unfiltered Fluke Temperature")
                    plt.xlabel("Fluke Temperature [C]")
                    plt.ylabel(f"Load [{unit}]")
                    plt.subplot(2, 3, 6)
                    plt.plot(fluke_temp, load)
                    plt.plot(filtered_fluke_temp, load)
                    plt.legend(["Unfiltered", "Filtered"])
                    plt.title("Unfiltered Load and Filtered Fluke Temperature")
                    plt.xlabel("Fluke Temperature [C]")
                    plt.ylabel(f"Load [{unit}]")
                plt.show()

            # DONE
            if mov_avg_set == {'temperature', 'extension'}:
                filtered_temp = df['MTS Temperature Moving Average']
                filtered_extension = df['Extension Moving Average']
                plt.subplot(2, 3, 1)
                plt.plot(mts_temp, extension)
                plt.plot(filtered_temp, filtered_extension)
                plt.legend(["Unfiltered", "Filtered"])
                plt.title("Filtered Extension and Filtered MTS Temperature")
                plt.xlabel("MTS Temperature [C]")
                plt.ylabel("Extension [mm]")
                plt.subplot(2, 3, 2)
                plt.plot(mts_temp, extension)
                plt.plot(mts_temp, filtered_extension)
                plt.legend(["Unfiltered", "Filtered"])
                plt.title("Filtered Extension and Unfiltered MTS Temperature")
                plt.xlabel("MTS Temperature [C]")
                plt.ylabel("Extension [mm]")
                plt.subplot(2, 3, 3)
                plt.plot(mts_temp, extension)
                plt.plot(filtered_temp, extension)
                plt.legend(["Unfiltered", "Filtered"])
                plt.title("Unfiltered Extension and Filtered MTS Temperature")
                plt.xlabel("MTS Temperature [C]")
                plt.ylabel("Extension [mm]")
                if fluke_check:
                    plt.subplot(2, 3, 4)
                    plt.plot(fluke_temp, extension)
                    plt.plot(filtered_fluke_temp, filtered_extension)
                    plt.legend(["Unfiltered", "Filtered"])
                    plt.title("Filtered Extension and Filtered Fluke Temperature")
                    plt.xlabel("Fluke Temperature [C]")
                    plt.ylabel("Extension [mm]")
                    plt.subplot(2, 3, 5)
                    plt.plot(fluke_temp, extension)
                    plt.plot(fluke_temp, filtered_extension)
                    plt.legend(["Unfiltered", "Filtered"])
                    plt.title("Filtered Extension and Unfiltered Fluke Temperature")
                    plt.xlabel("Fluke Temperature [C]")
                    plt.ylabel("Extension [mm]")
                    plt.subplot(2, 3, 6)
                    plt.plot(fluke_temp, extension)
                    plt.plot(filtered_fluke_temp, extension)
                    plt.legend(["Unfiltered", "Filtered"])
                    plt.title("Unfiltered Extension and Filtered Fluke Temperature")
                    plt.xlabel("Fluke Temperature [C]")
                    plt.ylabel("Extension [mm]")
                plt.show()

            # DONE
            if mov_avg_set == {'all'}:
                print()
                print('-----------------------------------------------------------------------------------------------------------------------')
                print('Note: All graphs are printed with unfiltered temperature and unfiltered measurement (load or extension) for comparison.')
                print('-----------------------------------------------------------------------------------------------------------------------')
                print()
                fig, axs = plt.subplots(2, 3)
                filtered_temp = df['MTS Temperature Moving Average']
                filtered_extension = df['Extension Moving Average']
                filtered_load = df[mv_avg_load_col_name]

                axs[0, 0].plot(mts_temp, extension)
                axs[0, 0].plot(filtered_temp, filtered_extension)
                axs[0, 0].legend(["Unfiltered measurements", "Filtered measurements"])
                axs[0, 0].set_title("Filtered Extension and Filtered MTS Temp")

                axs[0, 1].plot(mts_temp, extension)
                axs[0, 1].plot(mts_temp, filtered_extension)
                axs[0, 1].legend(["Unfiltered measurements", "Filtered measurements"])
                axs[0, 1].set_title("Filtered Extension and Unfiltered MTS Temp")

                axs[0, 2].plot(mts_temp, extension)
                axs[0, 2].plot(filtered_temp, extension)
                axs[0, 2].legend(["Unfiltered measurements", "Filtered measurements"])
                axs[0, 2].set_title("Unfiltered Extension and Filtered MTS Temp")

                axs[1, 0].plot(mts_temp, load)
                axs[1, 0].plot(filtered_temp, filtered_load)
                axs[1, 0].legend(["Unfiltered measurements", "Filtered measurements"])
                axs[1, 0].set_title("Filtered Load and Filtered MTS Temp")

                axs[1, 1].plot(mts_temp, load)
                axs[1, 1].plot(mts_temp, filtered_load)
                axs[1, 1].legend(["Unfiltered measurements", "Filtered measurements"])
                axs[1, 1].set_title("Filtered Load and Unfiltered MTS Temp")

                axs[1, 2].plot(mts_temp, load)
                axs[1, 2].plot(filtered_temp, load)
                axs[1, 2].legend(["Unfiltered measurements", "Filtered measurements"])
                axs[1, 2].set_title("Unfiltered Load and Filtered MTS Temp")
                plt.show()
                if fluke_check:
                    fig, axs = plt.subplots(2,3)
                    axs[0, 0].plot(fluke_temp, extension)
                    axs[0, 0].plot(filtered_fluke_temp, filtered_extension)
                    axs[0, 0].legend(["Unfiltered measurements", "Filtered measurements"])
                    axs[0, 0].set_title("Filtered Extension and Filtered Fluke Temp")

                    axs[0, 1].plot(fluke_temp, extension)
                    axs[0, 1].plot(fluke_temp, filtered_extension)
                    axs[0, 1].legend(["Unfiltered measurements", "Filtered measurements"])
                    axs[0, 1].set_title("Filtered Extension and Unfiltered Fluke Temp")

                    axs[0, 2].plot(fluke_temp, extension)
                    axs[0, 2].plot(filtered_fluke_temp, extension)
                    axs[0, 2].legend(["Unfiltered measurements", "Filtered measurements"])
                    axs[0, 2].set_title("Unfiltered Extension and Filtered Fluke Temp")

                    axs[1, 0].plot(fluke_temp, load)
                    axs[1, 0].plot(filtered_fluke_temp, filtered_load)
                    axs[1, 0].legend(["Unfiltered measurements", "Filtered measurements"])
                    axs[1, 0].set_title("Filtered Load and Filtered Fluke Temp")

                    axs[1, 1].plot(fluke_temp, load)
                    axs[1, 1].plot(fluke_temp, filtered_load)
                    axs[1, 1].legend(["Unfiltered measurements", "Filtered measurements"])
                    axs[1, 1].set_title("Filtered Load and Unfiltered Fluke Temp")

                    axs[1, 2].plot(fluke_temp, load)
                    axs[1, 2].plot(filtered_fluke_temp, load)
                    axs[1, 2].legend(["Unfiltered measurements", "Filtered measurements"])
                    axs[1, 2].set_title("Unfiltered Load and Filtered Fluke Temp")
                    plt.show()

                # DONE
            if mov_avg_set == {'load', 'extension'}:
                filtered_load = df[mv_avg_load_col_name]
                filtered_extension = df['Extension Moving Average']
                plt.subplot(2, 2, 1)
                plt.plot(mts_temp, extension)
                plt.plot(mts_temp, filtered_extension)
                plt.legend(["Unfiltered extension", "Filtered extension"])
                plt.title("Extension vs. MTS Temperature")
                plt.xlabel("MTS Temperature [C]")
                plt.ylabel("Extension [mm]")
                plt.subplot(2, 2, 2)
                plt.plot(mts_temp, load)
                plt.plot(mts_temp, filtered_load)
                plt.legend(["Unfiltered load", "Filtered load"])
                plt.title("Load vs. MTS Temperature")
                plt.xlabel("MTS Temperature [C]")
                plt.ylabel(f"Load [{unit}]")
                if fluke_check:
                    plt.subplot(2, 2, 3)
                    plt.plot(fluke_temp, extension)
                    plt.plot(fluke_temp, filtered_extension)
                    plt.legend(["Unfiltered extension", "Filtered extension"])
                    plt.title("Extension vs. Fluke Temperature")
                    plt.xlabel("Fluke Temperature [C]")
                    plt.ylabel("Extension [mm]")
                    plt.subplot(2, 2, 4)
                    plt.plot(fluke_temp, load)
                    plt.plot(fluke_temp, filtered_load)
                    plt.legend(["Unfiltered load", "Filtered load"])
                    plt.title("Load vs. Fluke Temperature")
                    plt.xlabel("Fluke Temperature [C]")
                    plt.ylabel(f"Load [{unit}]")
                plt.show()

            # DONE
            if mov_avg_set == {'load'}:
                filtered_load = df[mv_avg_load_col_name]
                plt.subplot(1,2,1)
                plt.plot(mts_temp, load)
                plt.plot(mts_temp, filtered_load)
                plt.legend(["Unfiltered load", "Filtered load"])
                plt.title("Load vs. MTS Temperature")
                plt.xlabel("MTS Temperature [C]")
                plt.ylabel(f"Load [{unit}]")
                if fluke_check:
                    plt.subplot(1,2,2)
                    plt.plot(fluke_temp, load)
                    plt.plot(fluke_temp, filtered_load)
                    plt.legend(["Unfiltered load", "Filtered load"])
                    plt.title("Load vs. Fluke Temperature")
                    plt.xlabel("Fluke Temperature [C]")
                    plt.ylabel(f"Load [{unit}]")
                plt.show()

            # DONE
            if mov_avg_set == {'extension'}:
                filtered_extension = df['Extension Moving Average']
                plt.subplot(1,2,1)
                plt.plot(mts_temp, extension)
                plt.plot(mts_temp, filtered_extension)
                plt.legend(["Unfiltered extension", "Filtered extension"])
                plt.title("Extension vs. MTS Temperature")
                plt.xlabel("MTS Temperature [C]")
                plt.ylabel("Extension [mm]")
                if fluke_check:
                    plt.subplot(1,2,2)
                    plt.plot(fluke_temp, extension)
                    plt.plot(fluke_temp, filtered_extension)
                    plt.legend(["Unfiltered extension", "Filtered extension"])
                    plt.title("Extension vs. Fluke Temperature")
                    plt.xlabel("Fluke Temperature [C]")
                    plt.ylabel("Extension [mm]")
                plt.show()

            if mov_avg_set == {'temperature'}:
                print()
                print('------------------------------------------------------------------------------------------------------------------------------------------')
                print('Note: These plots show the unfiltered load and unfiltered extensions plotted with both filtered and unfiltered temperature for comparison.')
                print('------------------------------------------------------------------------------------------------------------------------------------------')
                print()
                filtered_temp = df['MTS Temperature Moving Average']
                fluke_filtered_temp = df["Fluke Temperature Moving Average"]
                plt.subplot(2, 2, 1)
                plt.plot(mts_temp, extension)
                plt.plot(filtered_temp, extension)
                plt.legend(["Unfiltered Temperature", "Filtered Temperature"])
                plt.title("Extension vs. MTS Temperature")
                plt.xlabel("MTS Temperature [C]")
                plt.ylabel("Extension [mm]")
                plt.subplot(2, 2, 2)
                plt.plot(mts_temp, load)
                plt.plot(filtered_temp, load)
                plt.legend(["Unfiltered Temperature", "Filtered Temperature"])
                plt.title("Load vs. MTS Temperature")
                plt.xlabel("MTS Temperature [C]")
                plt.ylabel(f"Load [{unit}]")
                if fluke_check:
                    plt.subplot(2, 2, 3)
                    plt.plot(fluke_temp, extension)
                    plt.plot(fluke_filtered_temp, extension)
                    plt.legend(["Unfiltered Temperature", "Filtered Temperature"])
                    plt.title("Extension vs. Fluke Temperature")
                    plt.xlabel("Fluke Temperature [C]")
                    plt.ylabel("Extension [mm]")
                    plt.subplot(2, 2, 4)
                    plt.plot(fluke_temp, load)
                    plt.plot(fluke_filtered_temp, load)
                    plt.legend(["Unfiltered Temperature", "Filtered Temperature"])
                    plt.title("Load vs. Fluke Temperature")
                    plt.xlabel("Fluke Temperature [C]")
                    plt.ylabel(f"Load [{unit}]")
                plt.show()

            print()
            print('Please close plot window to continue.')
            print()
            satisfaction = input('Are you satisfied with the filtered data or would you like to try filtering again using a different number of data points? [yes or no] ').lower()

    return List_loads, mov_avg_set, unit
