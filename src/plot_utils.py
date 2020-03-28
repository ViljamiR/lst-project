import seaborn as sns
import matplotlib.pyplot as plt


def plot_lf_hf(lf_hf_df, timestamps, w_size, treshold):

    title = "LF/HF-ratio (window size: {}s) ".format(w_size)

    # LF/HF-ratio >= 1
    df1 = lf_hf_df[lf_hf_df.lf_hf >= treshold]
    # LF/HF-ratio < 1
    df2 = lf_hf_df[lf_hf_df.lf_hf < treshold]

    # Plotting LF/HF-ratio >= 1 using red color
    sns.lineplot(x=df1.time, y=df1.lf_hf, c='#FF7A60',
                 marker='o', linewidth=0, ms=3, mew=0.1).set(title=title)

    # Plotting LF/HF-ratio >= 1 using green color
    sns.lineplot(x=df2.time, y=df2.lf_hf, c='#41E870',
                 marker='o', linewidth=0, ms=3, mew=0.1).set(title=title)

    l1 = 'LF/HF-ratio >= {}'.format(treshold)
    l2 = 'LF/HF-ratio < {}'.format(treshold)
    plt.legend([l1, l2], loc=1)

    # Set limit to exclude outliers
    plt.ylim(0, 5)
    plt.show()


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
    ax2.set_ylabel(var2)

    fig.legend([var1, var2], loc=1)
    plt.show()
