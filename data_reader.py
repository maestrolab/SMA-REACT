# IMPORT STATEMENTS
import pandas as pd
import datetime


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
        self.temperature_title = ""
        self.column_headers = []

    def extract_txt(self):  # OPENING FILE AND EXTRACTING DATA
        with open(self.file, 'r') as f:
            text = f.readline()
            # finding the line with variable names
            while text.lower().find("time" or "duration") == -1:
                text = f.readline()
            if "\t" in text:
                separator = "\t"
            else:
                separator = ","
            chop_text = text.split(separator)
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
            if raw_data[i] == "\n" or raw_data[i].strip() == "":
                continue
            str_data = raw_data[i].split(separator)
            if (len(str_data) != len(labels)):
                continue
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

        # CONVERTING TO SECONDS IN THE TIME COLUMN IF NECESSARY
        if labels[0][labels[0].rindex(" ") + 1:] == "(h)":
            self.data[labels[0]] = [v*3600 for v in self.data[labels[0]]]
        if labels[0][labels[0].rindex(" ") + 1:] == "(m)":
            self.data[labels[0]] = [v * 60 for v in self.data[labels[0]]]

        # CREATING A DATAFRAME FROM THE DICTIONARY
        self.dataframe = pd.DataFrame.from_dict(self.data)


    # def get_columns(self):  # OPENING FILE AND EXTRACTING DATA
    #     # CONVERTS CSV FILE TO EXCEL FILE IF NEEDED
    #     if self.file.endswith(".csv"):
    #         file = pd.read_csv(self.file, encoding='unicode_escape', names=range(15))
    #         file.to_excel("converted.xlsx")
    #         self.file = "converted.xlsx"
    #
    #     # FINDING THE START TIME
    #     raw_data = pd.read_excel(self.file)
    #     for col in raw_data.columns:
    #         condition = raw_data[col] == "Start Time"
    #         index_list = raw_data.index[condition].tolist()
    #         if len(index_list) > 0:
    #             break
    #     self.start_time = raw_data.iloc[index_list[0] + 1][col]
    #
    #     # CREATES A DATAFRAME WITH UNNECESSARY ROWS AT TOP REMOVED
    #     for column in raw_data.columns:
    #         condition = raw_data[column] == "Duration"
    #         index_list = raw_data.index[condition].tolist()
    #         if len(index_list) > 0:
    #             break
    #     del raw_data
    #     raw_data = pd.read_excel(self.file, skiprows=index_list[0] + 1)
    #
    #     # ADDS DATA TO DICTIONARY
    #     for i in range(len(raw_data.columns)):
    #         self.data[raw_data.columns[i]] = list(())
    #         self.data[raw_data.columns[i]].extend(raw_data.iloc[:, i])
    #
    #     # CONVERTS DICTIONARY TO DATAFRAME AND DROPS UNNECESSARY VALUES AT END
    #     self.dataframe = pd.DataFrame.from_dict(self.data)
    #     first_nan = self.dataframe.loc[pd.isna(self.dataframe["Sample"])]
    #     self.dataframe = self.dataframe.drop(self.dataframe.index[range(first_nan.index[0], len(self.dataframe.index))])
    #
    #     # FINDING WHICH COLUMNS TO USE FOR THE FLUKE
    #     column_headers = self.dataframe.columns.tolist()
    #     column_headers = [m for m in column_headers if str(m).lower().find("unnamed") < 0 and type(m) != int]
    #     self.column_headers = column_headers
    #
    # def extract_other(self, header_choice):
    #     #print(column_headers)
    #     col_list = ["Duration"]
    #     #print("Enter title of column used for temperature (type done when finished): ")
    #     # done = False
    #     # while not done:
    #     #     col_title = input()
    #     #     col_title = col_title.lower()
    #     #     col_title = col_title.title()
    #     #     if col_title == "Done":
    #     #         done = True
    #     #     else:
    #     #         col_list.append(col_title)
    #     col_list.append(header_choice)
    #     self.dataframe = self.dataframe[col_list]
    #     self.temperature_title = col_list[1]
    #
    #     # REARRANGING DATAFRAME WITH TIME IN FIRST COLUMN
    #     column_list = self.dataframe.columns.tolist()
    #     for b in self.dataframe.columns:
    #         if b.lower().find("time") >= 0 or b.lower().find("duration") >= 0:
    #             column_list.remove(b)
    #             column_list.insert(0, b)
    #             self.dataframe = self.dataframe.reindex(columns=column_list)


    def extract_fluke(self):
        if self.file.endswith(".xlsx"):
            to_convert = pd.read_excel(self.file)
            to_convert.to_csv(self.file[:self.file.index(".xlsx")], index=None)
            self.file = self.file[:self.file.index(".xlsx")]

        with open(self.file) as file:
            # FINDING START TIME
            line = file.readline()
            while not "Start Time" in line:
                line = file.readline()
            stime_index = line.split(",").index("Start Time")
            line = file.readline()
            self.start_time = line.split(",")[stime_index]

            # FINDING THE LABELS
            while not "Duration" in line:
                line = file.readline()
            labels = line.split(",")
            labels = [x.strip() for x in labels]

            # PARSING DATA
            data = {}
            for label in labels:
                data[label] = []

            while (True):
                line = file.readline()
                vals = line.split(",")
                blank = True
                for i in range(len(vals)):
                    if not blank:
                        break
                    if vals[i].strip() != "":
                        blank = False
                if blank:
                    break
                # if len(vals) != len(labels):
                #     break
                for i in range(len(vals)):
                    data[labels[i]].append(vals[i].strip())

            # DELETING UNNECESSARY DATA
            copy_dict = {}
            for label in data.keys():
                if label != "":
                    copy_dict[label] = data[label]


            # CONVERTING TO DATAFRAME
            self.dataframe = pd.DataFrame.from_dict(copy_dict)


            # CONVERTING DURATIONS TO TIME ELAPSED
            self.dataframe = self.dataframe.head(-1)
            durations = self.dataframe["Duration"].tolist()
            for z in range(len(durations)):
                if type(durations[z]) == str:
                    if durations[z].count(":") == 2:
                        durations[z] = datetime.datetime.strptime(durations[z], "%H:%M:%S.%f")
                    elif durations[z].count(":") == 1:
                        durations[z] = datetime.datetime.strptime(durations[z], "%M:%S.%f")
            for i in range(len(durations)):
                durations[i] = datetime.timedelta(hours=durations[i].hour, minutes=durations[i].minute,
                                                  seconds=durations[i].second,
                                                  microseconds=durations[i].microsecond)
                durations[i] = durations[i].total_seconds()
            for j in range(1, len(durations)):
                durations[j] = durations[j] + durations[j - 1]
            for k in range(len(durations)):
                durations[k] = round(durations[k], 3)
            self.dataframe["Duration"] = durations


    def extract_DSC(self):
        # getting all data from file
        with open(self.file, "r") as dsc_file:
            dsc_data = dsc_file.readlines()

        # finding how many lines to skip and getting the steps
        index = 0
        steps = ""
        current_step = 0
        for i in range(len(dsc_data)):
            if dsc_data[i][:3].find(")") >= 0:
                if int(dsc_data[i][:dsc_data[i].find(")")]) > current_step:
                    current_step += 1
                    steps += (dsc_data[i])
            if dsc_data[i].lower().find("heat flow") >= 0:
                index = i
                break

        # stripping unnecessary data
        dsc_data = dsc_data[index - 1:]
        for i in range(len(dsc_data)):
            dsc_data[i] = dsc_data[i].replace("\n", "")
            dsc_data[i] = dsc_data[i].strip()

        # getting the column labels
        col_labels1 = dsc_data[0].split("\t")
        col_labels2 = dsc_data[1].split("\t")
        col_labels1 = [x.replace(" ", "") for x in col_labels1]
        col_labels2 = [x.replace(" ", "") for x in col_labels2]
        labels = [col_labels1[0]]
        dsc_data.pop(1)
        dsc_data.pop(0)
        for i in range(len(col_labels2)):
            labels.append(col_labels1[i + 1] + " " + col_labels2[i])

        # extracting the data to a dataframe
        dsc_dict = {}
        dsc_dict["Step"] = []
        cycle_num = 1
        eof = False
        for j in range(len(dsc_data)):
            data = dsc_data[j].split("\t")
            if len(data) < len(labels):
                cycle_num += 1
                continue
            dsc_dict["Step"].append(cycle_num)
            for i in range(len(labels)):
                try:
                    dsc_dict[labels[i]].append(float(data[i]))
                except KeyError:
                    dsc_dict[labels[i]] = []
                    dsc_dict[labels[i]].append(float(data[i]))
                except ValueError:
                    eof = True
            if eof:
                break
        dsc = pd.DataFrame.from_dict(dsc_dict)
        self.dataframe = dsc

        return steps

    def extract(self):  # EXTRACTS BASED ON FILE EXTENSION
        if self.file.endswith(".txt"):
            self.extract_txt()
        elif self.file.endswith(".csv") or self.file.endswith(".xlsx"):
            self.extract_fluke()
        else:
            print("File type not supported.")
