import utils as utils


def pretty_print(d, indent=0):
    """Pretty printing for dict-data type"""
    i = 0
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))


def print_features(rr_i):
    """Prints different features computed from RR-interval"""
    # # Time domain features
    time_domain_features = utils.return_time_domain_features(rr_i)
    print("Time-domain features")
    pretty_print(time_domain_features)

    # # Poincare-plot features
    poincare_plot_features = utils.return_poincare_plot_features(
        rr_i)
    print("Poincare-plot features")
    pretty_print(poincare_plot_features)

    # # Geometrical features
    geometrical_features = utils.return_geometrical_features(
        rr_i)
    print("Geometrical features")
    pretty_print(geometrical_features)

    # # Frequency-domain  features
    frequency_domain_features = utils.return_frequency_domain_features(
        rr_i)
    print("Frequency-domain features")
    pretty_print(frequency_domain_features)
