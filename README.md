# OneTon_Water
Scripts for analyzing data from one ton water detector

1. Read_MultipleFiles_WriteTree_v2.py

This is the python script to read (one or more) h5 files collected from the water detector and to save a ROOT tree with all signals (with a focus on the two CAEN 4CH digitizers).

-> To use it, one needs to input (by editing the file): the raw data file in zip format (path and name), the path to save ROOT tree. It will unzip the .zip file, process .h5 and save .root, then delete .h5, the original .zip file will not be changed. 

-> Three different trigger types will be determined for each event.

-> Waveform from digitizers are dealt event by event, baseline and threshold is determined event by event.
