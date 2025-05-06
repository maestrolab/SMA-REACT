
def exportData(data, filename):
    with open(filename, "w") as output:
        titles = " ," + ",".join(data.keys()) + "\n"
        output.write(titles)
        lower_line = ["Lower Bound"]
        upper_line = ["Upper Bound"]
        guess_line = ["Guess"]
        for key, val in data.items():
            if "Lower Bound" in val:
                lower_line.append(str(val["Lower Bound"]))
            else:
                lower_line.append(" ")
            if "Upper Bound" in val:
                upper_line.append(str(val["Upper Bound"]))
            else:
                upper_line.append(" ")
            if "Guess" in val:
                guess_line.append(str(val["Guess"]))
            else:
                guess_line.append(" ")
            lower = ",".join(lower_line) + "\n"
            upper = ",".join(upper_line) + "\n"
            guess = ",".join(guess_line) + "\n"
        output.write(lower)
        output.write(upper)
        output.write(guess)


