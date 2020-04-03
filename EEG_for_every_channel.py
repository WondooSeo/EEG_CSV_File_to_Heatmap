'''
# Ch1 - Ch8
# In Pandas, don't have to worry about header
Frontalis = []
Procerus = []
Orbiculari_oculi = []
Zygomatic_major_minor = []
Risorius = []
Orbicularis_oris = []
Masseter = []
Depressor_labii_inferioris = []
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt
#import scipy as sp
#import scipy.fftpack
#import seaborn as sns

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

df = pd.read_csv('anger1.csv')

file_header = (list(df))
#print(type(file_header)) → class 'list'
file_header = list(filter(None, file_header)) # For erasing non column
file_header_len = len(file_header)

'''
Not using this code;
df_fft = sp.fftpack.fft(df)
rev_df_fft = np.abs(df_fft)
#sample_freq = sp.fftpack.fftfreq(df.size, d=0.02)
result_ifft = sp.fftpack.ifft(result)
'''

nWindowSize = 20
temp_temp = []

for header_len in range (0, file_header_len):
    s = df[file_header[header_len]]

    # Set highpass filter, cut-off as 30Hz, sampling frequency as 1000, order as 4
    result = butter_highpass_filter(s, 30, 1000, 4)
    #print(result)

    init_data_sum = 0
    init_data_iter = 0

    for i in range (0, 10):
        init_data_sum += result[i]
        init_data_iter += 1

    init_data_mean = init_data_sum/init_data_iter
    #print(init_data_mean)

    result_adjusted = result - init_data_mean
    #print(result_adjusted)

    abs_result_adjusted = abs(result_adjusted)
    #print(abs_result_adjusted)

    # Set lowpass filter, cut-off as 15Hz, sampling frequency as 1000, order as 4
    low_abs_result_adjusted = butter_lowpass_filter(abs_result_adjusted, 15, 1000, 4)
    #print(type(low_abs_result_adjusted)) → <class 'numpy.ndarray'>

    # Normalization
    Zmax, Zmin = low_abs_result_adjusted.max(), low_abs_result_adjusted.min()
    norm_low_abs_result_adjusted = (low_abs_result_adjusted - Zmin) / (Zmax - Zmin)

    #plt.plot(norm_low_abs_result_adjusted)
    #plt.show()
    #print(np.size(norm_low_abs_result_adjusted)) → 1984

    # Bank summation
    bank_all = []
    data_size = np.size(norm_low_abs_result_adjusted)
    sum_iter = np.around(data_size / nWindowSize)
    for_loop_count = 0 # Check the loop count until it becomes sum_iter
    bank_temp = 0 # Sum of all elements of a count
    bank_num = 0 # Naming the bank_temp

    '''
    TypeError: 'int' object is not callable → when var and func names are same
    '''

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
    #print(bank_all) → GOOD
    #print(np.size(bank_all))

    # Normalize the bank
    Zmax, Zmin = np.max(bank_all), np.min(bank_all)
    norm_bank_all = (bank_all - Zmin) / (Zmax - Zmin)

    temp_temp.append(norm_bank_all)

# Making heatmap
plt.imshow(temp_temp, cmap='jet', interpolation='nearest')
plt.colorbar(orientation='vertical')
#plt.set_yticklabels(file_header, minor=False)
plt.show()

print(temp_temp)
