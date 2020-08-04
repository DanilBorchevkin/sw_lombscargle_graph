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

def plot_graph(data, out_filepath, to_display=False, save_to_disk=True):
    '''
    Plot grapth and return its data
    '''

    output_data = list()
    t = list()
    y = list()

    for val_pair in data:
        t.append(float(val_pair[1]))
        y.append(float(val_pair[0]))

    # Main magic of the grapth
    frequency, power = LombScargle(t, y).autopower()
    plt.plot(frequency, power)

    if to_display:
        plt.show()

    if save_to_disk:
        plt.savefig(out_filepath)

    # Generate output
    for val in frequency:
        output_data.append([frequency, power])

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

            output_data = plot_graph(read_data, out_png_filepath)
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