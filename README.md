# OneTon_Water
Scripts for analyzing data from one ton water detector

#### update on 3/12/2018 ####
"Read_MultipleFiles_WriteTree_v2_calledByLabVIEW_v7.py"

    Reads the h5 file and save information into ROOT Tree.
    Developed my own (simple) method to count number of pulses in digitizer waveforms.
    The code is tested to run fine on the cluster in batch mode (processing multiple files).
#### end ####

1. Read_MultipleFiles_WriteTree_v2.py

This is the python script to read (one or more) h5 files collected from the water detector and to save a ROOT tree with all signals (with a focus on the two CAEN 4CH digitizers).

-> To use it, one needs to input (by editing the file): the raw data file in zip format (path and name), the path to save ROOT tree. It will unzip the .zip file, process .h5 and save .root, then delete .h5, the original .zip file will not be changed. 

-> Three different trigger types will be determined for each event.

-> Waveform from digitizers are dealt event by event, baseline and threshold is determined event by event.

2. Read_Tree_make_plots_v1.C

This script reads (one or more) ROOT trees and save the histograms in a ROOT file.

-> Inputs are (by editing the file) just filename and path in the beginning a few lines.

-> In the output ROOT file, histograms for QDC, digitizers are stored for every channel. Other modules (TDC, Scaler) are not included yet, but it is very straight forward.
