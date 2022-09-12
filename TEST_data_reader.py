# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 01:10:34 2021

@author: Tiago
"""


# IMPORT STATEMENTS
import pandas as pd


# FUNCTION DEFINITIONS
# function that checks whether or not a value can be converted to a float
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# checks to see if the column labels in a dataframe contain "Duration"
def check_in_row(table):
    test = False
    index = 0
    while not test and index < len(table.columns.tolist()):
        if table.columns.tolist()[index] == "Duration":
            test = True
        else:
            index += 1
    return test



class reader:
    def __init__(self, file):
        self.file = file
        self.data = {}
        self.dataframe = pd.DataFrame()
        self.start_time = 0

    def extract_txt(self):  # OPENING FILE AND EXTRACTING DATA
        with open(self.file, 'r') as f:
            text = f.readline()
            chop_text = text.split(",")
            # finding the line with variable names
            while chop_text[0].lower().find("time" or "duration") == -1:
                text = f.readline()
                chop_text = text.split(",")
            raw_data = f.readlines()

            # REMOVING BLANK LINES FROM THE DATA
            raw_data = [h for h in raw_data if h != "\n"]

            # CREATING AN ARRAY OF VARIABLE LABELS
            labels = list(())
            for txt in chop_text:
                x = txt.replace('"', '')
                x = x.replace("\n", '')
                labels.append(x)

            # CREATING A DICTIONARY TO STORE ALL THE DATA
            for w in range(len(labels)):
                self.data[labels[w]] = list(())

            # ADDING DATA TO THE DICTIONARY
            for i in range(len(raw_data)):
                str_data = raw_data[i].split(',')
                # remove any quotation marks in the numeric data
                for k in range(len(str_data)):
                    str_data[k] = str_data[k].replace('"', '')
                    str_data[k] = str_data[k].replace('\n', '')
                    # convert all the numbers to floats if they can be and add to dictionary
                    if isfloat(str_data[k]):
                        y = float(str_data[k])
                    else:
                        y = str_data[k]
                    self.data[labels[k]].append(y)
        # CREATING A DATAFRAME FROM THE DICTIONARY
        self.dataframe = pd.DataFrame.from_dict(self.data)


    def extract_other(self):  # OPENING FILE AND EXTRACTING DATA
        # CONVERTS CSV FILE TO EXCEL FILE IF NEEDED
        if self.file.endswith(".csv"):
            file = pd.read_csv(self.file, encoding='unicode_escape', names=range(15))
            file.to_excel("converted.xlsx")
            self.file = "converted.xlsx"

        # FINDING THE START TIME
        raw_data = pd.read_excel(self.file)
        for col in raw_data.columns:
            condition = raw_data[col] == "Start Time"
            index_list = raw_data.index[condition].tolist()
            if len(index_list) > 0:
                break
        self.start_time = raw_data.iloc[index_list[0] + 1][col]

        # CREATES A DATAFRAME WITH UNNECESSARY ROWS AT TOP REMOVED
        for column in raw_data.columns:
            condition = raw_data[column] == "Duration"
            index_list = raw_data.index[condition].tolist()
            if len(index_list) > 0:
                break
        del raw_data
        raw_data = pd.read_excel(self.file, skiprows=index_list[0] + 1)

        # ADDS DATA TO DICTIONARY
        for i in range(len(raw_data.columns)):
            self.data[raw_data.columns[i]] = list(())
            self.data[raw_data.columns[i]].extend(raw_data.iloc[:, i])

        # CONVERTS DICTIONARY TO DATAFRAME AND DROPS UNNECESSARY VALUES AT END
        self.dataframe = pd.DataFrame.from_dict(self.data)
        first_nan = self.dataframe.loc[pd.isna(self.dataframe["Sample"])]
        self.dataframe = self.dataframe.drop(self.dataframe.index[range(first_nan.index[0], len(self.dataframe.index))])

        # FINDING WHICH COLUMNS TO USE FOR THE FLUKE
        column_headers = self.dataframe.columns.tolist()
        column_headers = [m for m in column_headers if str(m).lower().find("unnamed") < 0 and type(m) != int]
        print(column_headers)
        col_list = ["Duration"]
        # print("Enter title of columns required from fluke data excluding duration (type done when finished): ")
        # done = False
        # while not done:
        #     col_title = input()
        #     col_title = col_title.lower()
        #     col_title = col_title.title()
        #     if col_title == "Done":
        #         done = True
        #     else:
        #         col_list.append(col_title)
        
        ######
        column_headers = ["Sample",'Duration','Average']
        self.dataframe = self.dataframe[column_headers]

        # REARRANGING DATAFRAME WITH TIME IN FIRST COLUMN
        column_list = self.dataframe.columns.tolist()
        for b in self.dataframe.columns:
            if b.lower().find("time") >= 0 or b.lower().find("duration") >= 0:
                column_list.remove(b)
                column_list.insert(0, b)
                self.dataframe = self.dataframe.reindex(columns=column_list)

    def extract(self):  # EXTRACTS BASED ON FILE EXTENSION
        if self.file.endswith(".txt"):
            self.extract_txt()
        elif self.file.endswith(".csv") or self.file.endswith(".xlsx"):
            self.extract_other()
        else:
            print("File type not supported.")