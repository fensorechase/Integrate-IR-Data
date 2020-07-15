"""
7-1-20
@author Chase Fensore

Description: this program accepts user input for the upper & lower limits of integration. Then, it parses through a folder (path modifiable below)
full of .csv files, integrates data between the user-defined integration limits, and writes the area under the curve to an output file called "origname___i.csv"
in the same directory as path.
"""

import pandas as pd
import numpy as np
import scipy # scipy full library
from scipy import integrate as integrate # Integrate function from scipy
import os
import glob
import csv
import re


def main():
    # Folder that holds IR files
    path = r"C://Allen Lab 2020//IR_Data"
    # The following lines will find all of the files of a given type in the path's folder
    extension = 'csv'
    os.chdir(path)
    result = glob.glob('*.{}'.format(extension))
    #Here are the files that fit your criterion that are within the path file
    all_files = glob.glob(path + "/*.csv")

    # Read user input. min_wave, max_wave
    min_wave = float(input("Enter minimum wavelength(i.e. lower integration limit: "))
    max_wave = float(input("Enter maximum wavelength(i.e. upper integration limit: "))


    for filename in all_files:
        col_list = ["Frame", "Wavelength", "Intensity"]
        df = pd.read_csv(filename, index_col=False, usecols=col_list)

        #COLLECT X DATA
        x_list = df["Wavelength"]

        """
        In this section, we trim the x-limits such that lower_index is the 1st value greater than the user-input min wavelength.
        Similarly, the upper integration limit index is trimmed such that upper_index is the 1st value greater than the user-input max wavelength
        """
        try:
            lower_index = next(x for x, val in enumerate(x_list) if val > min_wave)
            # Return index of wn input by user
        except ValueError:
            print('ERROR: cannot find lower index')
        try:
            upper_index = next(x for x, val in enumerate(x_list) if val > max_wave)
            # Return index of wn input by user
        except ValueError:
            print('ERROR: cannot find upper index')


        x_list = x_list[lower_index+2 : upper_index+2] # Index adjustment ...Trim the array for Phosphate region
        x_list = x_list.values.tolist() # Convert to python list # x_list.to_numpy()

        #COLLECT Y DATA
        y = df["Intensity"]
        y = y[lower_index+2 : upper_index+2] # Index Adjustment  ...Trim the array for Phosphate region
        y_list = y.values.tolist() # Convert to python list


        dx = average_step_size(x_list, lower_index, upper_index)# 121 : 287 ...Find average step size in 800-1300 region
        #print("MEAN STEP SIZE: ", dx)
        # We're trimming python list to user-defined indices


        #Finally, calculate area of the 800-1300 region.
        area = simpsons(y_list, dx)
        #print("AREA UNDER CURVE: ", area)

        #TODO: between [800, 1300]; Phosphate?...Wavelength = (1/wavenum * 10^7)

        # CREATE OUTPUT FILENAME
        filename = re.sub('.csv','',filename)
        filename=filename+"_i.csv"      # filename: OUTPUT FILE NAME

            #Finally, write area under curve to output file.
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file, delimiter = ',')
            out_list = [area]
            writer.writerow(out_list)
        if not file.closed:
            file.close()


"""
Returns the average distance between consecutive elements of the array, arr, from lower_index through upper_index-1.

NOTE: lower_index, upper_index are NOT necessary, since we re-zero indices in python list.
"""
def average_step_size(list, lower_index, upper_index):

    i = 0
    sum = 0
    while i < (len(list)-1):
        temp = list[i+1] - list[i]
        sum += temp
        i = i+1

    return sum / i


"""
Uses Simpson's Rule to calculate the area under a curve.

arr : list of y values
n : number of rectangles (data points - 1)
dx : average step size

@returns area under the curve of the implied function
"""
def simpsons(arr, dx):
    i = 0 # index
    sum = 0
    for num in arr:

        if i==0:
            # first value, multiply by 1
            sum += arr[i]
        elif i == (len(arr)-1):
            # last value, multiply by 1
            sum += arr[i]
        elif i%2 == 0:
            #even index, multipy by 2
            sum += 2*arr[i]
        elif i%2 == 1:
            #odd index, multiply by 4
            sum += 4*arr[i]
        else:
            "ERROR"
        i = i+1

    return (dx/3)*sum


if __name__ == '__main__':
    main()

#FURTHER INSPIRATION: https://docs.scipy.org/doc/scipy-0.18.1/reference/tutorial/integrate.html
