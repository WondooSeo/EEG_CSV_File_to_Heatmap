'''''''''

Copyright ⓒ 2020 Won-Doo Seo(Neurorobotics Lab in Yonsei University), All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

------------------------------------------------

What can I do with it?

You can make EEG csv file to heatmap file.
Raw data go through Butterworth highpass filter, cut-off as 30Hz, sampling frequency as 1000, order as 4,
then adjust the data, and absolte it. Absolted data go through Butterworth lowpass filter, cut-off as 15Hz,
sampling frequency as 1000, order as 4, and normalize it. Finally, those data become a heatmap.

------------------------------------------------

How I preprocess the csv file?

First, you have to make csv data as;
    (In this example, a, b, etc is data.)
    ch1 ch2 ch3 ch4 ...
    a   b   c   d   ...
    e   f   g   h   ...
    .   .   .   .
    .   .   .   .
    .   .   .   .
If your csv file has no header, you may have to revise this file.

------------------------------------------------

How I use it?

ⓐ Write file name at var file_name.
ⓑ You can manipulate the heatmap window size. Set var nWindowSize.
ⓒ If you succeeded runnung this file, you can get heatmap csv data file, and heatmap plot png.

'''''''''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt

''''''

# fs : sampling frequency

def butter_highpass_filter(data, cutoff, fs, order):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data, padlen=0)
    return y

def butter_highpass(cutoff, fs, order):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data, padlen=0)
    return y

def butter_lowpass(cutoff, fs, order):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

''''''

file_name = ('anger4')

df = pd.read_csv(file_name + '.csv')

file_header = (list(df))
#print(type(file_header)) → class 'list'
file_header = list(filter(None, file_header)) # For erasing non column
file_header_len = len(file_header)

nWindowSize = 20
data_temp = []

for header_len in range (0, file_header_len):
    s = df[file_header[header_len]]

    # Set highpass filter, cut-off as 30Hz, sampling frequency as 1000, order as 4
    result = butter_highpass_filter(s, 30, 1000, 4)

    init_data_sum = 0
    init_data_iter = 0

    for i in range (0, 10):
        init_data_sum += result[i]
        init_data_iter += 1

    init_data_mean = init_data_sum/init_data_iter

    result_adjusted = result - init_data_mean

    abs_result_adjusted = abs(result_adjusted)

    # Set lowpass filter, cut-off as 15Hz, sampling frequency as 1000, order as 4
    low_abs_result_adjusted = butter_lowpass_filter(abs_result_adjusted, 15, 1000, 4)
    #print(type(low_abs_result_adjusted)) → <class 'numpy.ndarray'>

    # Normalization
    Zmax, Zmin = low_abs_result_adjusted.max(), low_abs_result_adjusted.min()
    norm_low_abs_result_adjusted = (low_abs_result_adjusted - Zmin) / (Zmax - Zmin)

    # Bank summation
    bank_all = []
    data_size = np.size(norm_low_abs_result_adjusted)
    sum_iter = np.around(data_size / nWindowSize)
    for_loop_count = 0 # Check the loop count until it becomes sum_iter
    bank_temp = 0 # Sum of all elements of a count
    bank_num = 0 # Naming the bank_temp

    for i in range(0, data_size):
        bank_temp += norm_low_abs_result_adjusted[i]
        for_loop_count += 1
        if for_loop_count == sum_iter or i == data_size-1:
            avg_temp = bank_temp / for_loop_count
            #bank_all.append([bank_num, avg_temp])
            bank_all.append(avg_temp)
            bank_num += 1
            for_loop_count = 0
            bank_temp = 0

    # Normalize the bank
    Nmax, Nmin = np.max(bank_all), np.min(bank_all)
    norm_bank_all = (bank_all - Nmin) / (Nmax - Nmin)

    data_temp.append(norm_bank_all)


# Making heatmap
plt.imshow(data_temp, cmap='jet', interpolation='nearest')
plt.colorbar(orientation='vertical')
plt.savefig(file_name+'_heatmap.png', dpi=600)

temp_T = np.transpose(data_temp)

data_to_csv = pd.DataFrame(temp_T)
file_path = file_name+'_heatmap.csv'
data_to_csv.to_csv(file_path, header=None, index=None)
