import pandas as pd
import numpy as np
import hrvanalysis as hrv
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from hrvanalysis import plot_poincare
from hrvanalysis import remove_outliers, remove_ectopic_beats, interpolate_nan_values
from hrvanalysis import plot_psd

from utils import return_sliding_window, plot_time_series
import utils as utils


def save_to_csv(df, filename):
    df.to_csv(filename,
              index=False, header=True)


def pretty(d, indent=0):
    i = 0
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))


def main():
    print("Importing dataset")
    sleep_data = pd.read_csv(".data/sleep_16_2.csv")
    # sleep_data_full = pd.read_csv("./sleep_full.csv")

    # sleep_data_full.time = pd.to_datetime(sleep_data_full.time, unit='s')
    print("---------------------")
    print("Resulting dataset")
    print(sleep_data.head())
    sleep_data.time = pd.to_datetime(sleep_data.time, unit='s')

    # sleep_not_null = sleep_data[sleep_data.hrv > 0]
    # rr_data = sleep_data[sleep_data.bbt0 > 0]
    # rr_data = rr_data[rr_data.bbt0 < 1500]
    # print(sleep_not_null)
    # save_to_csv(rr_data.bbt0, "clean_hrv.csv")

    sleep_data.bbt0 = sleep_data.bbt0.replace(0, 750)
    print(sleep_data.head())
    sleep_data.loc[(sleep_data.bbt0 > 1500), 'bbt0'] = 1500
    # print(sleep_data.head())
    # print(sleep_data.bbt0.mean())

    nn_intervals_list = list(sleep_data.bbt0)

    sns.set()

    # Plotting heart rate
    # sns.lineplot(x='time', y='hr', data=sleep_data,
    #              marker="o", linewidth=0,  alpha=0.9, ms=3, mew=0.1).set(title="HR")
    # plt.show()

    # Plotting heart rate and Heart rate variability
    utils.plot_two_variable_ts(sleep_data, 'hr', 'hrv', 'HRV and HR')

    # ax2 = ax.twinx()
    # sns.lineplot(x='time', y='hrv', data=sleep_data,
    #              linewidth=0, marker="o", ms=2, mew=0.1)
    # ax2.set_ylabel("heart rate variability")
    # plt.show()

    # # This remove outliers from signal
    # rr_intervals_without_outliers = remove_outliers(rr_intervals=nn_intervals_list,
    #                                                 low_rri=500, high_rri=1500)
    # # # This replace outliers nan values with linear interpolation
    # interpolated_rr_intervals = interpolate_nan_values(rr_intervals=rr_intervals_without_outliers,
    #                                                    interpolation_method="linear")

    # # This remove ectopic beats from signal
    # nn_intervals_list = np.array(remove_ectopic_beats(
    #     rr_intervals=rr_intervals_without_outliers, method="malik"))

    # # time_domain_features = hrv.get_time_domain_features(nn_intervals_list)

    # # Time domain features
    time_domain_features = utils.return_time_domain_features(nn_intervals_list)
    print("Time-domain features")
    print(time_domain_features)
    pretty(time_domain_features)

    # # Poincare-plot features
    poincare_plot_features = utils.return_poincare_plot_features(
        nn_intervals_list)
    print("Poincare-plot features")
    print(poincare_plot_features)
    pretty(poincare_plot_features)

    # # Geometrical features
    geometrical_features = utils.return_geometrical_features(
        nn_intervals_list)
    print("Geometrical features")
    print(geometrical_features)
    pretty(geometrical_features)

    # # Frequency-domain  features
    frequency_domain_features = utils.return_frequency_domain_features(
        nn_intervals_list)
    print("Frequency-domain features")
    print(frequency_domain_features)
    pretty(frequency_domain_features)

    w_size = 300

    # Get timestamps for sliding window
    timestamps = utils.return_sliding_window_time(
        sleep_data.time, nn_intervals_list, w_size)

    # Get LF/HF-ratio for sliding window
    print("Computing the LF/HF-ratio")
    lf_hf_results = utils.return_sliding_window_data(
        nn_intervals_list, w_size, utils.return_frequency_domain_features, 'lf_hf_ratio')

    # # Plotting beat to beat-data
    # plot_time_series(sleep_data.time, sleep_data.bbt0)

    # # Plotting LF/HF-data
    sns.set()
    title = "LF/HF-ratio (window size: {}) ".format(w_size)
    plot_time_series(timestamps, lf_hf_results, title=title)


main()
