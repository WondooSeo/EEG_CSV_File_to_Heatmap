# Copyright ⓒ 2020 Won-Doo Seo(Neurorobotics Lab in Yonsei University), All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

# What can I do with it?

You can make EEG csv file to heatmap file.
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
