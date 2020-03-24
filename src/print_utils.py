import utils as utils


def pretty_print(d, indent=0):
    """Pretty printing for dict-data type"""
    i = 0
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty_print(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))


def print_recovery_ratios(recovery_ratios):
    print("Recovery ratios for all nights:")
    for i, ratio in enumerate(recovery_ratios):
        print('Night {} – Recovery ratio: {:2.2}'.format(i, ratio))
    print("–––––––––––––––––––––––––––")


def print_recovery_nights(recovery_nights):
    print("Nights with recovery ratio over baseline:")
    for i, value in enumerate(recovery_nights):
        recovered = 'True' if value == 1 else 'False'
        print('Night {} – Recovery ratio over baseline: {}'.format(i, recovered))
    print("–––––––––––––––––––––––––––")


def print_features(rr_i):
    """Prints different features computed from RR-interval"""
    # # Time domain features
    time_domain_features = utils.return_time_domain_features(rr_i)
    print("Time-domain features")
    pretty_print(time_domain_features)
    print("–––––––––––––––––––––––––––")

    # # Poincare-plot features
    poincare_plot_features = utils.return_poincare_plot_features(
        rr_i)
    print("Poincare-plot features")
    pretty_print(poincare_plot_features)
    print("–––––––––––––––––––––––––––")

    # # Geometrical features
    geometrical_features = utils.return_geometrical_features(
        rr_i)
    print("Geometrical features")
    pretty_print(geometrical_features)
    print("–––––––––––––––––––––––––––")

    # # Frequency-domain  features
    frequency_domain_features = utils.return_frequency_domain_features(
        rr_i)
    print("Frequency-domain features")
    pretty_print(frequency_domain_features)
    print("–––––––––––––––––––––––––––")
