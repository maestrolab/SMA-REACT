# IMPORT STATEMENTS
from scipy.signal import butter, lfilter


def lowpassFilter(order, sample_rate, cutoff, data):
    nyq = 0.5 * sample_rate
    norm_cutoff = cutoff/nyq
    b, a = butter(order, norm_cutoff, fs=sample_rate, btype="low", analog=False, output="ba")
    # data = df["Strain"].to_numpy()
    filtered_data = lfilter(b, a, data)
    # df["Filtered Strain"] = filtered_data
    return filtered_data