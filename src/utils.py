from itertools import islice
import seaborn as sns
import matplotlib.pyplot as plt
import hrvanalysis as hrv
import numpy as np


def save_df_to_csv(df, filename):
    df.to_csv(filename,
              index=False, header=True)


def return_time_domain_features(rr_i):
    time_domain_features = hrv.get_time_domain_features(
        rr_i)
    return time_domain_features


def return_poincare_plot_features(rr_i):
    poincare_plot_features = hrv.get_poincare_plot_features(
        rr_i)
    return poincare_plot_features


def return_geometrical_features(rr_i):
    geometrical_features = hrv.get_geometrical_features(
        rr_i)
    return geometrical_features


def return_frequency_domain_features(rr_i):
    frequency_domain_features = hrv.get_frequency_domain_features(
        rr_i)
    return frequency_domain_features


def return_single_feature(feature_dict, feature_name):
    return feature_dict[feature_name]


def calculate_baseline_recovery_ratio(rr_is, threshold=1.5, w_size=300):
    """
    This function calculates the baseline recovery ratio for a list of nights

    Input:
        - rr_i              list of lists of beat-to-beat intervals
        - threshold         cut off value for calling recovery
        - w_size            window size for sliding window
    Output:
        - recovery_ratio    Recovery ratio for one night
    """

    return np.mean(return_recovery_ratios(rr_is, threshold, w_size))


def calculate_recovery_ratio(rr_i, threshold=1.5, w_size=300):
    """
    This function calculates the recovery ratio for one night given rr i data

    Input:
        - rr_i              beat-to-beat intervals
        - threshold         cut off value (LF/HF) for calling recovery
        - w_size            window size for sliding window
    Output:
        - recovery_ratio    Recovery ratio for one night
    """
    freq = return_frequency_domain_features(rr_i)
    lf_hf_ratio_data = np.array(return_sliding_window_data(
        rr_i, w_size, return_frequency_domain_features, "lf_hf_ratio"))
    lows = len(lf_hf_ratio_data[lf_hf_ratio_data < threshold])

    recovery_ratio = lows / len(lf_hf_ratio_data)

    return recovery_ratio


def return_recovery_ratios(rr_is, threshold=1.5, w_size=300):
    """
    This function calculates the recovery ratio list of nights given RR-interval data

    Input:
        - rr_i              list of lists of beat-to-beat intervals
        - threshold         cut off value for calling recovery
        - w_size            window size for sliding window
    Output:
        - recovery_ratios    Recovery ratio for each night
    """
    return [calculate_recovery_ratio(rr_i, threshold, w_size) for rr_i in rr_is]


def return_recovery_nights(recovery_ratios, threshold):
    """
    This function returns recovery nights, where recovery ratio was over treshold value
    Input:
        - recovery_ratios   list of recovery ratios
        - threshold         cut off value for calling recovery
    Output:
        - recovered_nights  Array indicating which night had recovery ratio over treshold-value
    """
    return [1 if ratio > threshold else 0 for ratio in recovery_ratios]


def return_sliding_window_data(rr_i, w_size, feature_fun, feature_name):
    results = []
    for i in range(len(rr_i)-w_size-1):
        data_window = rr_i[i:i+w_size-1]
        features = feature_fun(data_window)
        results.append(return_single_feature(features, feature_name))
    return results


def return_sliding_window_time(time_data, rr_i, w_size):

    timestamps = []
    for i in range(len(rr_i)-w_size-1):
        timestamps.append(time_data.iloc[int(i + w_size/2)])
    return timestamps


def return_low_lf_hf_ratio(lf_hf_df):
    """Returns the percentage of data points with low LF/HF-ratio  """
    # LF/HF-ratio >= 1
    df1 = lf_hf_df[lf_hf_df.lf_hf >= 1]
    # LF/HF-ratio < 1
    df2 = lf_hf_df[lf_hf_df.lf_hf < 1]
    return len(df2.lf_hf) / len(lf_hf_df.lf_hf)
