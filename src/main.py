import pandas as pd
import numpy as np
import hrvanalysis as hrv
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from hrvanalysis import plot_poincare
from hrvanalysis import remove_outliers, remove_ectopic_beats, interpolate_nan_values
from hrvanalysis import plot_psd

import utils as utils
import print_utils as print_utils
import plot_utils as plot_utils


def main():
    print("Importing dataset")
    sleep_data_1 = pd.read_csv("./sleep_16_2.csv")
    sleep_data_2 = pd.read_csv("./data/03-16-03-17.csv")
    sleep_data_3 = pd.read_csv("./data/03-17-03-18.csv")
    sleep_data = [sleep_data_1, sleep_data_2, sleep_data_3]

    print("---------------------")
    print("Resulting dataset")
    print(sleep_data_1.head())

    # Add two hours to correct the time column
    for sleep in sleep_data:
        sleep.time = pd.to_datetime(
            sleep.time, unit='s')

    # sleep_not_null = sleep_data_1[sleep_data_1.hrv > 0]
    # rr_data = sleep_data_1[sleep_data_1.bbt0 > 0]
    # rr_data = rr_data[rr_data.bbt0 < 1500]

    print(sleep_data_1.head())
    nn_intervals_list = []
    # Enable this when debugging
    for sleep in sleep_data:
        # REMOVE THIS
        sleep = sleep.iloc[1:10000]
        sleep.bbt0 = sleep.bbt0.replace(0, 750)
        sleep.loc[(sleep.bbt0 > 1500), 'bbt0'] = 1500
        # print(sleep_data_1.head())
        # print(sleep_data_1.bbt0.mean())

        nn_intervals_list.append(list(sleep.bbt0))

    sns.set()

    # Plotting heart rate
    # sns.lineplot(x='time', y='hr', data=sleep_data_1,
    #              marker="o", linewidth=0,  alpha=0.9, ms=3, mew=0.1).set(title="HR")
    # plt.show()

    # Plotting heart rate and Heart rate variability
    # plot_utils.plot_two_variable_ts(sleep_data_1, 'hr', 'hrv', 'HRV and HR')

    # Printing list of features for whole dataset
    for nn in nn_intervals_list:
        print_utils.print_features(nn)

    # Set window size for sliding window
    w_size = 300
    # Get timestamps for sliding window
    timestamps = utils.return_sliding_window_time(
        sleep_data_1.time, nn_intervals_list[0], w_size)

    # Get LF/HF-ratio for sliding window
    print("Computing the LF/HF-ratios")
    lf_hf_results = utils.return_sliding_window_data(
        nn_intervals_list[0], w_size, utils.return_frequency_domain_features, 'lf_hf_ratio')
    print("Done")
    print("–––––––––––––––––––––––––––")

    d = {'lf_hf': lf_hf_results, 'time': timestamps}
    lf_hf_results = pd.DataFrame(d)

    # Plotting LF/HF-data
    print("Plotting the LF/HF-ratios")
    plot_utils.plot_lf_hf(lf_hf_results, timestamps, w_size, treshold=1.5)

    # Ratio of low LF/HF
    ratio = utils.return_low_lf_hf_ratio(lf_hf_results)

    print("Percentage of low LF/HF-ratios: {}".format(ratio))

    # Baseline recovery ratio
    baseline_recovery_ratio = utils.calculate_baseline_recovery_ratio(
        nn_intervals_list)
    print("–––––––––––––––––––––––––––")
    print('Baseline recovery ratio: {:2.2}'.format(baseline_recovery_ratio))
    print("–––––––––––––––––––––––––––")

    # Recovery ratios for all nights
    # print("Recovery ratios for all nights:")
    recovery_ratios = utils.return_recovery_ratios(nn_intervals_list)
    print_utils.print_recovery_ratios(recovery_ratios)

    # Return nights with recovery ratio over baseline ratio
    recovery_nights = utils.return_recovery_nights(
        recovery_ratios, baseline_recovery_ratio)

    print_utils.print_recovery_nights(recovery_nights)

    night_idxs = [i for i in range(len(recovery_nights))]

    # Generate dataframe
    night_df = utils.generate_dataframe([night_idxs, recovery_ratios, recovery_nights], ['night_index',
                                                                                         'recovery_ratios', 'recovered'])

    print(night_df)

    # Saving dataset
    utils.save_df_to_csv(night_df, 'recovery_data.csv')

    # RMDSD for whole night

    total_rmssd = utils.return_time_domain_features(
        nn_intervals_list[0])['rmssd']

    print("RMSSD for whole night: {}".format(total_rmssd))
    print("Computing the  RMMSD-values")

    rmssd_results = utils.return_sliding_window_data(
        nn_intervals_list[0], w_size, utils.return_time_domain_features, 'rmssd')
    d = {'rmssd': rmssd_results, 'time': timestamps}
    rmssd_results = pd.DataFrame(d)
    print("Done")
    print("–––––––––––––––––––––––––––")

    #
    # Plotting RMMSD-data
    # print("Plotting the RMMSD-values")

    # title = "RMSSD-values (window size: {}s) ".format(w_size)

    # sns.lineplot(x=timestamps, y=[r for r in rmssd_results.rmssd],
    #              marker='o', linewidth=0, ms=3, mew=0.1).set(title=title)

    # plt.axhline(total_rmssd, linestyle='--', c='red')
    # plt.show()


main()
