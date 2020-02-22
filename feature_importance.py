import numpy as np
from sklearn.linear_model import LinearRegression


def main():
    with open("static/boston_housing.csv") as f:
        features = f.readline()
        features = features.split(',')
        # features[-1] = "medv"
        del features[-1]
        del features[3]
        del features[4]
    data = np.genfromtxt('static/boston_housing.csv', delimiter=',', dtype=float)
    data = data[1:]
    data = np.hstack((data[:, 0:3], data[:, 5:]))
    data_x = data[:, :-1]
    data_y = data[:, -1]
    reg = LinearRegression().fit(data_x, data_y)
    coeffs = reg.coef_
    score = reg.score(data_x, data_y)
    print(score)
    sorted_features = [x for _,x in sorted(zip(coeffs, features))]
    return features, coeffs, sorted_features


if __name__ == '__main__':
    print(main())
