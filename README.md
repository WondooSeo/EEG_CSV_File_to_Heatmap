※ _This project is licensed under the terms of the MIT license._ ※

# What can I do with it?

You can make EEG csv file to heatmap file. [^1] [^2]
Raw data go through Butterworth highpass filter, cut-off as 30Hz, sampling frequency as 1000, order as 4,
then adjust the data, and absolte it. Absolted data go through Butterworth lowpass filter, cut-off as 15Hz,
sampling frequency as 1000, order as 4, and normalize it. Finally, those data become a heatmap.

# How I preprocess the csv file?

First, you have to make csv data as;
    (In this example, a, b, etc is data.)
    
    ch1 ch2 ch3 ch4 ...
    a   b   c   d   ...
    e   f   g   h   ...
    .   .   .   .
    .   .   .   .
    .   .   .   .
    
If your csv file has no header, you may have to revise this python file(or csv file).

# How I use it?

ⓐ Write file name at var file_name.

ⓑ You can manipulate the heatmap window size. Set var nWindowSize.

ⓒ If you succeeded runnung this file, you can get heatmap csv data file, and heatmap plot png.

[^1]:  Won-Doo Seo* and Han Ul Yoon, "Simultaneous Inter-channel Activation of EEG Signal and Brain Functional Connectivity," Proceedings of KIIS Spring Conference, Vol. 30, No. 1, pp. 145-146, Jun, 2020
[^2]: Won-Doo Seo* and Han Ul Yoon, "Simultaneous Inter-Channel EEG Activation and Brain Functional Connectivity," Journal of the KIIS, Vol. 30, No. 6, pp. 465-471, Dec, 2020
