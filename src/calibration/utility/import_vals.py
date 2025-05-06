def importData(filename):
    # getting all data
    params = {}
    with open(filename, "r") as file:
        data = file.readlines()

        titles = data[0].split(",")[1:]
        for title in titles:
            params[title] = {}
        lower = data[1].split(",")[1:]
        upper = data[2].split(",")[1:]
        guess = data[3].split(",")[1:]
        for i in range(len(lower)):
            params[titles[i]]["Lower Bound"] = lower[i]
            params[titles[i]]["Upper Bound"] = upper[i]
            params[titles[i]]["Guess"] = guess[i]

    return params

# data = (importData("bounds.csv"))
# print(data)
