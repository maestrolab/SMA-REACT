# IMPORT STATEMENTS
from analyze_mts_only import analyze_mts
from analyze_fluke_and_mts import analyze_fmts

check = input("Do you have fluke data to analyze (Yes/No)? ")
if check.lower() == "yes":
    analyze_fmts()
else:
    analyze_mts()
