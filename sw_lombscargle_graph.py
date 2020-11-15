# -*- coding: utf-8 -*-
"""
Plot graph according to the DAT file 
@author: Danil Borchevkin
"""

import csv
import glob
import os
from astropy.timeseries import LombScargle
import matplotlib.pyplot as plt
import scipy.signal as signal
import numpy as np

def read_file_data(filepath):
    '''
    Read data in [[val,time],[val, time]] format
    '''

    data = None

    with open(filepath, 'r') as dest_f:
        data_iter = csv.reader(dest_f,delimiter="\t")
        data = [data for data in data_iter]

    return data

def save_to_ascii_file(data_list, out_filepath, header=[]):
    '''
    Save data in format [[],[]] into DAT file 
    - CSV 
    - with \t delimeter 
    - \n line endings
    '''
    write_list = []

    for data in data_list:
        output_str = ""
        for val in data:
            output_str += str(val) + "\t"
        output_str = output_str[:-1]
        output_str += "\n"
        write_list.append(output_str)

    with open(out_filepath,"w") as f:
        f.writelines(write_list)

def plot_graph(data, out_filepath, lb_freq_start=0.01, lb_freq_end=4.0, lb_freq_num=100000, to_display=False, save_to_disk=True):
    '''
    Plot grapth and return its data

    Params
    data - input data in list of lists with pair value and time
    out_filepath - out file name path for create
    lb_freq_start - start frequency of lombscargle graph
    lb_freq_end - end frequency of lombscargle graph
    lb_freq_num - number of points in lombscargle graph
    to_display - if set to true then graph will be shown on the display
    save_to_disk - if set to true then graph will be saved on the disk

    Return
    List of lists of graph values in form [freq, pgram_value]
    '''

    output_data = list()

    x = list()
    y = list()

    for val_pair in data:
        x.append(float(val_pair[1]))
        y.append(float(val_pair[0]))

    # Define the array of frequencies for which to compute the periodogram:
    f = np.linspace(lb_freq_start, lb_freq_end, lb_freq_num)

    #Calculate Lomb-Scargle periodogram:
    pgram = signal.lombscargle(x, y, f, normalize=False)

    #Now make a plot of the input data:
    plt.subplot(2, 1, 1)
    plt.plot(x, y, 'b+')
    #Then plot the normalized periodogram:
    plt.subplot(2, 1, 2)
    plt.plot(f, pgram)

    if to_display:
        plt.show()

    if save_to_disk:
        plt.savefig(out_filepath)

    # Generate output
    for idx, freq in enumerate(f):
        output_data.append([freq, pgram[idx]])

    return output_data

def main():
    print("Script is started")

    files = glob.glob("./input/*.dat")    

    for filepath in files:
        print("Process >> " + filepath)

        try:
            read_data = read_file_data(filepath)
            out_dat_filepath = "./output/" + os.path.basename(filepath) + ".dat"
            out_png_filepath = "./output/" + os.path.basename(filepath) + ".png"

            output_data = plot_graph(read_data, 
                                    out_png_filepath,
                                    lb_freq_start=0.01,
                                    lb_freq_end=4.0,
                                    lb_freq_num=100000)
                                    
            print("Saved PNG to >> " + out_png_filepath)

            save_to_ascii_file(output_data, out_dat_filepath)
            print("Saved DAT to >> " + out_dat_filepath)
    
        except Exception as e:
            print("Cannot process >> ", filepath)
            print("Reason >> " + str(e))
            
        finally:
            print()

    print("Script is finished")

if __name__ == "__main__":
    main()