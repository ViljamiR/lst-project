import pandas as pd
import numpy as np
from hrvanalysis import plot_poincare
from hrvanalysis import remove_outliers, remove_ectopic_beats, interpolate_nan_values
from hrvanalysis import plot_psd


def main():
    print("Importing dataset")
    sleep_data = pd.read_csv("./sleep_16_2.csv")
    print("---------------------")
    print("Resulting dataset")
    print(sleep_data.head())
    sleep_not_null = sleep_data[sleep_data.hrv.notnull()]
    print(sleep_not_null)

    nn_intervals_list = list(sleep_data.hrv)

    # # This remove outliers from signal
    rr_intervals_without_outliers = remove_outliers(rr_intervals=nn_intervals_list,
                                                    low_rri=25, high_rri=200)
    len(rr_intervals_without_outliers)
    # # # This replace outliers nan values with linear interpolation
    # interpolated_rr_intervals = interpolate_nan_values(rr_intervals=rr_intervals_without_outliers,
    #                                                    interpolation_method="linear")

    # print(interpolated_rr_intervals)

    # # This remove ectopic beats from signal

    nn_intervals_list = np.array(remove_ectopic_beats(
        rr_intervals=rr_intervals_without_outliers, method="malik"))
    # nn_intervals_list = np.array(remove_ectopic_beats(
    #     rr_intervals=interpolated_rr_intervals, method="malik"))

    nn_intervals_list = nn_intervals_list[~np.isnan(nn_intervals_list)]

    print(nn_intervals_list[0:500])
    plot_poincare(list(nn_intervals_list), plot_sd_features=True)

    # plot_psd(nn_intervals_list, method="welch")
    # plot_psd(nn_intervals_list, method="lomb")
    # plot_psd(rr_intervals_without_outliers, method="lomb")


main()
