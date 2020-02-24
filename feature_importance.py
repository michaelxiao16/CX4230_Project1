import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import normalize


def main():
    """
    Pull data from csv file, filter out all features not relevant to the simulation. Normalize all vectors so all
    features are between 0 and 1, then perform regression. Return the sorted list of features for use in the
    simulation
    :return: features (unsorted), coefficients, and sorted_features
    """
    with open("static/boston_housing.csv") as f:
        features = f.readline()
        features = features.split(',')
        # features[-1] = "medv"
        del features[-1]
        del features[11:12]
        del features[9]
        del features[1:7]
    data = np.genfromtxt('static/boston_housing.csv', delimiter=',', dtype=float)
    data = data[1:]
    data_x = np.hstack((data[:, 0:1], data[:, 7:9], np.reshape(data[:, 10], (data.shape[0], 1)),
                      np.reshape(data[:, 12], (data.shape[0], 1))))
    data_y = data[:, -1]
    data_x = normalize(data_x, axis=1)
    reg = LinearRegression().fit(data_x, data_y)
    coeffs = reg.coef_
    score = reg.score(data_x, data_y)
    print(score)
    sorted_features = [x for _, x in sorted(zip(coeffs, features))]
    return features, coeffs, sorted_features


def get_feature_vector():
    _, coeffs, _ = main()
    coeffs = sorted(coeffs)
    return coeffs


if __name__ == '__main__':
    print(main())
