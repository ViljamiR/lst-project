from itertools import islice
import seaborn as sns
import matplotlib.pyplot as plt
import hrvanalysis as hrv


def plot_time_series(T, Y, title=" "):
    sns.lineplot(x=T, y=Y).set(title=title)
    plt.show()


def plot_two_variable_ts(data, var1, var2, title=" "):
    fig, ax = plt.subplots()
    sns.lineplot(x='time', y=var1, data=data, alpha=0.8, marker='o', linewidth=0, ms=2, mew=0.1, color="orange").set(
        title=title)
    ax.set_ylabel(var1)

    ax2 = ax.twinx()
    sns.lineplot(x='time', y=var2, data=data,
                 linewidth=0, marker="o", ms=2, mew=0.1)
    ax2.set_ylabel(var)
    plt.show()


def save_df_to_csv(df, filename):
    df.to_csv(filename,
              index=False, header=True)


def return_sliding_window(input_list, n, step_size):
    iterable = iter(input_list)
    result = list(islice(iterable, n, None, step_size))
    if len(result) == n:
        yield result
    for elem in iterable:
        result = result[1:] + list((elem,))
        yield result


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


def return_sliding_window_data(rr_i, w_size, feature_fun, feature_name):
    results = []
    for i in range(len(rr_i)-w_size-1):
        data_window = rr_i[i:i+w_size-1]
        features = feature_fun(data_window)
        results.append(return_single_feature(features, feature_name))
    return results


def return_sliding_window_time(time_data, rr_i,  w_size):
    # Args:
    # time_data: pd.Dataframe
    # w_size: int
    timestamps = []
    for i in range(len(rr_i)-w_size-1):
        timestamps.append(time_data.iloc[int(i + w_size/2)])
    return timestamps
