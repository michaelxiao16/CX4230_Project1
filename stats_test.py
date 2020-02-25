import scipy.stats
import numpy as np
from random import randint
from main import GRID_COLS, GRID_ROWS, main_sim_loop


def confidence_interval(mean, std, n, confidence_level=0.95):
    confidence_value = confidence_level + (1 - confidence_level)/2
    h = std * scipy.stats.norm.ppf(confidence_value)/np.sqrt(n)
    return mean - h, mean + h


def disparity_random():
    businesses = ((randint(0, GRID_ROWS - 1), randint(0, GRID_COLS - 1)),)
    educations = ((randint(0, GRID_ROWS - 1), randint(0, GRID_COLS - 1)),)
    crimes = ((randint(0, GRID_ROWS - 1), randint(0, GRID_COLS - 1)),)
    dis = main_sim_loop(business_center=businesses, education_center=educations, crime_centers=crimes, input_year=100, type_event="")
    return dis


def disparity_education():
    businesses = ((randint(0, GRID_ROWS - 1), randint(0, GRID_COLS - 1)),)
    educations = ((randint(0, GRID_ROWS - 1), randint(0, GRID_COLS - 1)),)
    crimes = ((randint(0, GRID_ROWS - 1), randint(0, GRID_COLS - 1)),)
    dis = main_sim_loop(business_center=businesses, education_center=educations, crime_centers=crimes,
                        input_year=30, type_event="education")
    return dis


def disparity_business():
    businesses = ((randint(0, GRID_ROWS - 1), randint(0, GRID_COLS - 1)),)
    educations = ((randint(0, GRID_ROWS - 1), randint(0, GRID_COLS - 1)),)
    crimes = ((randint(0, GRID_ROWS - 1), randint(0, GRID_COLS - 1)),)
    dis = main_sim_loop(business_center=businesses, education_center=educations, crime_centers=crimes,
                        input_year=30, type_event="business")
    return dis


def build_business_confidence(num_trials=30):
    vals = [disparity_business() for i in range(num_trials)]
    avg = np.average(vals)
    print(avg)
    std = np.std(vals)
    print(std)
    interval = confidence_interval(avg, std, num_trials)
    print(interval)
    return interval


def build_education_confidence(num_trials=30):
    vals = [disparity_education() for i in range(num_trials)]
    avg = np.average(vals)
    print(avg)
    std = np.std(vals)
    print(std)
    interval = confidence_interval(avg, std, num_trials)
    print(interval)
    return interval



def build_rand_confidence(num_trials=30):
    vals = [disparity_random() for i in range(num_trials)]
    print(vals)
    avg = np.average(vals)
    print(avg)
    std = np.std(vals)
    print(std)
    interval = confidence_interval(avg, std, num_trials)
    print(interval)
    return interval


def disparity_crime():
    businesses = ((randint(0, GRID_ROWS - 1), randint(0, GRID_COLS - 1)),)
    educations = ((randint(0, GRID_ROWS - 1), randint(0, GRID_COLS - 1)),)
    crimes = ((randint(0, GRID_ROWS - 1), randint(0, GRID_COLS - 1)), (randint(0, GRID_ROWS - 1), randint(0, GRID_COLS - 1)))
    dis = main_sim_loop(business_center=businesses, education_center=educations, crime_centers=crimes,
                        input_year=30, type_event="crime")
    return dis


def build_crime_confidence(num_trials=30):
    vals = [disparity_crime() for i in range(num_trials)]
    print(vals)
    avg = np.average(vals)
    print(avg)
    std = np.std(vals)
    print(std)
    interval = confidence_interval(avg, std, num_trials)
    print(interval)
    return interval


if __name__ == '__main__':
    # print(build_rand_confidence())
    # print(build_education_confidence())
    # print(build_crime_confidence())
    print(build_business_confidence())

