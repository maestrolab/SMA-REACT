# IMPORT STATEMENTS
import pandas as pd
import pickle
import datetime
import csv


def export_all(df, startTime, crossShape, crossArea, unitOut, origLength, dispUnits, filename):
    # CREATING METADATA
    metadata_dict = dict()
    metadata_dict["Date Run"] = datetime.datetime.now()
    metadata_dict["Start Time"] = startTime
    metadata_dict["Cross Section"] = crossShape
    metadata_dict["Cross Sectional Area"] = str(crossArea) + " ({}^2)".format(unitOut)
    metadata_dict["Length"] = str(origLength) + " " + dispUnits

    # CREATING METADATA DATAFRAME
    metadata_list = [(key + ": " + str(value)) for key, value in metadata_dict.items() if type(value) != dict]
    metadata = pd.DataFrame()
    metadata["Metadata"] = metadata_list

    # CREATING METADATA PICKLE
    pkl_data = df.to_dict()
    pkl_data = {**pkl_data, **metadata_dict}
    meta_pkl = open("metadata.pkl", "wb")
    pickle.dump(pkl_data, meta_pkl)
    meta_pkl.close()

    # CREATING METADATA CSV
    with open("metadata.csv", "w") as metafile:
        csv_writer = csv.writer(metafile)
        for key, value in metadata_dict.items():
            csv_writer.writerow([key, value])

    # EXPORTING THE DATA FRAME TO AN EXCEL FILE
    writer = pd.ExcelWriter(filename)
    df.to_excel(writer, sheet_name="Data")
    metadata.to_excel(writer, sheet_name="Metadata", index=False)
    writer.save()
    writer.close()


# function that prints headers and asks user to pick one
def header_choice(list1, str_calc):
    for col_index in range(len(list1)):
        for index in range(-1, -(len(list1[col_index]) - 1), -1):
            if list1[col_index][index] == " ":
                list1[col_index] = list1[col_index][:index]
                break
    print(list1)
    for ind in range(len(list1)):
        list1[ind] = list1[ind].lower().replace(" ", "")
    title = input("Enter the column from above you would like to use for {}: ".format(str_calc))
    title_check = False
    while not title_check:
        if title.lower().replace(" ", "") in list1:
            title_check = True
        else:
            print("That {} does not exist".format(str_calc))
            title = input("Enter the column from above you would like to use for {}: ".format(str_calc))
    list2 = list1.copy()
    return title, list2