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
import scipy as sp
import scipy.fftpack
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

df = pd.read_csv('anger1.csv')
s = df['Ch2']

'''
Not using this code;
df_fft = sp.fftpack.fft(df)
rev_df_fft = np.abs(df_fft)
#sample_freq = sp.fftpack.fftfreq(df.size, d=0.02)
'''

# Set highpass filter, cut-off as 30Hz, sampling frequency as 1000, order as 4
result = butter_highpass_filter(s, 30, 1000, 4)
#print(result)

# result_ifft = sp.fftpack.ifft(result)

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

# print(type(low_abs_result_adjusted)) → <class 'numpy.ndarray'>

# Normalization
Zmax, Zmin = low_abs_result_adjusted.max(), low_abs_result_adjusted.min()
norm_low_abs_result_adjusted = (low_abs_result_adjusted - Zmin) / (Zmax - Zmin)

'''
plt.figure()
plt.plot(low_abs_result_adjusted, label='low_abs_adj')
plt.plot(norm_low_abs_result_adjusted, label='norm_low_abs_adj')
plt.legend(loc='upper left')
plt.show()
'''

# print(norm_low_abs_result_adjusted.size) → 1984

