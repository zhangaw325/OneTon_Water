import h5py
import numpy as np
#import matplotlib.pyplot as plt
#import graphUtils
import ROOT
from ROOT import TH1F, TTree, TFile, TSpectrum, TCanvas, TLine
import datetime
import time
import timeit
from array import array
import zipfile
import os
import sys

ROOT.gROOT.SetBatch(1)

#some initial numbers
NbQDC1CH = 8  #QDC1 CHs 0 1 2 3 4 5 are used for H0, 1, 2, 3, 4, 5. now just include unused channels in tree
NbQDC2CH = 8  #QDC2 CHs 0 6 2 3 4 5 are used for S0, 1, 2, 3, 4, 5.
NbTDCCH = 16
NbScalerCH = 17
NbDigiCH = 8
NSamples = 2560 # Number of samples for each digitizer channel

#prepare file names to be read
rawdatapath = "./"
hdf5_file_zip_name = []
hdf5_file_zip_name.append(sys.argv[1])
directory_to_extract_to = "./"

hdf5_file_name = []
for aZipfile in hdf5_file_zip_name:
    aname = rawdatapath + aZipfile
    zip_ref = zipfile.ZipFile(aname, 'r')
    zip_ref.extractall(directory_to_extract_to)
    zip_ref.close()
    h5filename = str.replace(aZipfile,".zip",".h5")
    hdf5_file_name.append(h5filename)    

start_time = timeit.default_timer()

# start reading the files
totalEvtNumber = 0
for filename in hdf5_file_name:
    #prepare histograms and ROOT file
    #for each .h5 file create a ROOT Tree
    rootfilename = str.replace(filename,".h5","_Tree_v7.root")
    rootfile = TFile(rootfilename,"recreate")
    print rootfilename
    print filename
    mytree = TTree( 'OneTonEvent', 'My Event Tree' )
    #the variables to be stored in the ROOT Tree
    EvtNumber = array('i', [0]) #event number, a signle integer
    EvtTime = array('d',[0]) #need to think
    TemperatureBox = array('f',[0.])  #event temperature in the dark room, a float 
    TemperatureRack = array('f',[0.]) #event temperature at the daq rack, a float
    Resistivity = array('f',[0.])     #event resistivity, a float
    QDC1 = array('f',NbQDC1CH*[0.])   #event QDC1, array, size 8, float
    QDC2 = array('f',NbQDC2CH*[0.])   #event QDC2, array, size 8,float
    TDC = array('f',NbTDCCH*[0.])     #event TDC, array, size 16, float
    Scaler = array('f',NbScalerCH*[0.]) #event Scaler, array, size 17, float
    TrigType = array('i',[0]) # I'' use 1 -> multiplicity, 2 -> Cosmic and 3->LED triggers
    TrigTypeFlag_Multi = array('i',[0]) #trigger type multipliticy, integer numbers,
    TrigTypeFlag_Hodo = array('i',[0])  #trigger type hodoscope
    TrigTypeFlag_Led = array('i',[0])   #trigger type led
    #digitizer variables                         #in my old method, I treat every waveform either one or zero pulse!
    DigitizerCharge = array('f',NbDigiCH*[0.])   #digitizer charge, array, size 8, float, in the old method, this charge is an integration of a fixed time window
    DigitizerAmplitude = array('f',NbDigiCH*[0.])#digitizer amplitude, array, size 8, float, used in old method
    DigitizerStartTimeBin = array('f',NbDigiCH*[0.])#digitizer start time bin, old method
    DigitizerRiseTime =  array('f',NbDigiCH*[0.]) #digitizer rise time, old method
    DigitizerPulseWidth = array('f',NbDigiCH*[0.])
    DigitizerFullPulseWidth = array('f',NbDigiCH*[0.])
    #digitizer pedestal
    DigitizerPedMean = array('f',NbDigiCH*[0.]) #array of 8, float
    DigitizerPedWidth = array('f',NbDigiCH*[0.])
    #digitizer, new method, counting number of pulses
    DigitizerNumberOfPulses = array('i',NbDigiCH*[0]) #in new method, I need to count the number of pulses in each waveform.
    #digitizer charge, start bin, end bin
    DigitizerPulseCharge = np.array([ [0.0]*20 for i in range(8)], np.dtype('d')) # 8 PMT channels, each assume maximum 20 pulses, this is a 8 by 20 array, for more than 20 pulses, only save the first 20 pulses the event. The final number of pulses is stored for later easier process.
    DigitizerPulseStartBin = np.array([ [0.0]*20 for i in range(8)], np.dtype('d')) # 8 PMT channel, each assume maximum 20 pulses, this is a 8 by 20 array. stores start bin of each found pulse
    DigitizerPulseEndBin = np.array([ [0.0]*20 for i in range(8)], np.dtype('d')) # 8 PMT channel, each assume maximum 20 pulses, this is a 8 by 20 array. stores end bin of each found pulse
    MuonDecayTime = array('i',NbDigiCH*[0]) #this info is not checked, could be wrong. But leave it here for now.
    #
    mytree.Branch("EvtNumber",EvtNumber,"EvtNumber/I")
    mytree.Branch("EvtTime",EvtTime,"EvtTime/D")
    mytree.Branch("TemperatureBox",TemperatureBox,"TemperatureBox/F")
    mytree.Branch("TemperatureRack",TemperatureRack,"TemperatureRack/F")
    mytree.Branch("Resistivity",Resistivity,"Resistivity/F")
    mytree.Branch("QDC1",QDC1,"QDC1[8]/F")
    mytree.Branch("QDC2",QDC2,"QDC2[8]/F")
    mytree.Branch("TDC",TDC,"TDC[16]/F")
    mytree.Branch("Scaler",Scaler,"Scaler[17]/F")
    mytree.Branch("DigitizerCharge",DigitizerCharge,"DigitizerCharge[8]/F")
    mytree.Branch("DigitizerAmplitude",DigitizerAmplitude,"DigitizerAmplitude[8]/F")
    mytree.Branch("DigitizerStartTimeBin",DigitizerStartTimeBin,"DigitizerStartTimeBin[8]/F")
    mytree.Branch("DigitizerRiseTime",DigitizerRiseTime,"DigitizerRiseTime[8]/F")
    mytree.Branch("DigitizerPulseWidth",DigitizerPulseWidth,"DigitizerPulseWidth[8]/F")
    mytree.Branch("DigitizerFullPulseWidth",DigitizerFullPulseWidth,"DigitizerFullPulseWidth[8]/F")
    mytree.Branch("DigitizerPedMean",DigitizerPedMean,"DigitizerPedMean[8]/F")
    mytree.Branch("DigitizerPedWidth",DigitizerPedWidth,"DigitizerPedWidth[8]/F")
    mytree.Branch("TrigType",TrigType,"TrigType/I")
    mytree.Branch("TrigTypeFlag_Multi",TrigTypeFlag_Multi,"TrigTypeFlag_Multi/I")
    mytree.Branch("TrigTypeFlag_Hodo",TrigTypeFlag_Hodo,"TrigTypeFlag_Hodo/I")
    mytree.Branch("TrigTypeFlag_Led",TrigTypeFlag_Led,"TrigTypeFlag_Led/I")
    # new method, to store digitizer number of pulses and charges etc.
    mytree.Branch("DigitizerNumberOfPulses",DigitizerNumberOfPulses,"DigitizerNumberOfPulses[8]/I")
    mytree.Branch('DigitizerPulseCharge', DigitizerPulseCharge, 'DigitizerPulseCharge[8][20]/D') # 8 PMT channels, each assume maximum 20 pulses
    mytree.Branch('DigitizerPulseStartBin', DigitizerPulseStartBin, 'DigitizerPulseStartBin[8][20]/D') # 8 PMT channel, each assume maximum 20 pulses
    mytree.Branch('DigitizerPulseEndBin', DigitizerPulseEndBin, 'DigitizerPulseEndBin[8][20]/D') # 8 PMT channel, each assume maximum 20 pulses
    mytree.Branch("MuonDecayTime",MuonDecayTime,"MuonDecayTime[8]/I")
    #
    file = h5py.File(filename,'r') # open one h5 file
    #CalData1 = file['Calibration']['Digitizer_1']['Pedestal']
    #CalData2 = file['Calibration']['Digitizer_2']['Pedestal']
    EvtDir = file['Events'] # get the Events card
    #timeCnt = 0;
    initCnts=[] #initial counts (the first event) in scaler, all active channels
    initTime=0 #initial time (the first event)
    for evtkey in EvtDir.keys():
        if not(evtkey=='evt_table'):
            EvtNumber[0] = int(evtkey)
#            if EvtNumber[0]>2 and EvtNumber[0]<1900:
#                continue;
            totalEvtNumber += 1
            thisDigi1 = EvtDir[evtkey]["Digitizer_1"]
            thisDigi2 = EvtDir[evtkey]["Digitizer_2"]
            thisQDC1 = EvtDir[evtkey]["QDC_1"]
            thisQDC2 = EvtDir[evtkey]["QDC_2"]
            thisTDC  = EvtDir[evtkey]["TDC"]
            thisScaler = EvtDir[evtkey]["Scaler"]
            thisTime = EvtDir[evtkey]['Event_Time']
            thisResistivity = EvtDir[evtkey]['Event_Resistivity']
            thisTemperature = EvtDir[evtkey]['Event_Temp']
            thisTempeAtRack = EvtDir[evtkey]['Event_TempRack']
            EvtTime[0]=thisTime[()]
            TemperatureBox[0]=thisTemperature[()]
            TemperatureRack[0]=thisTempeAtRack[()]
            Resistivity[0]=thisResistivity[()]
            # determine the trigger type using TDC information
            # I will use trigFlag for MultiTrig (1), CosmicTrig (2) and LedTrig (3)
            trigFlag = 0
            trig_temp1, trig_temp2, trig_temp3, thistrig = 0, 0, 0, 1 # this is the old method
            TrigFlag_Multi, TrigFlag_Hodo, TrigFlag_Led = 0, 0, 0 # this is the new method, it is (tested) same as the old method
            for ch, num in thisTDC:
                if int(ch) == 7: # multiplicity
                    trig_temp1 = 1
                    TrigFlag_Multi = 1
                if int(ch) == 6: # cosmic
                    trig_temp2 = 2
                    TrigFlag_Hodo = 1
                if int(ch) == 8: # led trigger
                    trig_temp3 = 3
                    TrigFlag_Led = 1
                if int(ch) == 9: # all trigger, should be always 1
                    thistrig = 1
            if thistrig==1 and trig_temp1 == 1 and trig_temp2 != 2 and trig_temp3 != 3:
                trigFlag = 1 #multiplicity trigger only
            if thistrig==1 and trig_temp1 != 1 and trig_temp2 == 2 and trig_temp3 != 3:
                trigFlag = 2 #cosmic trigger only
            if thistrig==1 and trig_temp1 != 1 and trig_temp2 != 2 and trig_temp3 == 3:
                trigFlag = 3 #LED trigger only
            TrigType[0] = trigFlag
            TrigTypeFlag_Multi[0] = TrigFlag_Multi
            TrigTypeFlag_Hodo[0] = TrigFlag_Hodo
            TrigTypeFlag_Led[0] = TrigFlag_Led
            #process QDC data
            for ch, num, c, d in thisQDC1:
                QDC1[int(ch)] = num
            for ch, num, c, d in thisQDC2:
                QDC2[int(ch)] = num
            #process Scaler data
            i=0
            if int(evtkey) == 1:
                for counts in thisScaler:
                    initTime = thisTime[()]
                    initCnts.append(counts)
            else:
                for counts in thisScaler:
                    rate = (counts - initCnts[i])/(thisTime[()] - initTime)
                    Scaler[i] = rate
                    i += 1
            #process TDC data
            # Before assigning values, clear the TDC array.
            # intentatively, I set the array to have -1. Later when processing results, if I see -1, that means no entry for the channel in the event.
            for ch in range(0,16,1):
                TDC[ch] = -1.0
            for ch, num in thisTDC: # cont. in the data, only TDC channels with entries are stored.
                TDC[int(ch)] = num
            #process digitizer data
            digi1_ped_mean = []
            digi1_threshold = []
            digi2_ped_mean = []
            digi2_threshold = []
            mean, mean2 = 0, 0
            sigma, sigma2 = 0, 0
            if np.mod(int(evtkey),1) == 0:
                if np.mod(int(evtkey),100) ==0:    print evtkey, totalEvtNumber
                #prepare for digitizer pedestals
                #get pedestals digitizer 1
                for ch in range(0,4,1):
                    # use bins 1500-2560, and reduce bias by removing some possible signals in that range,
                    # I assume baseline should be less than +-10 ADC units, this is decided after looking at the processed pedestals
                    subwavelist = [] # make a sub waveform list to hold those bins for pedestals
                    for bin in range(1500,2560,1):
                        if abs(thisDigi1[ch][bin])<10:
                            subwavelist.append(thisDigi1[ch][bin])
                    mean = np.mean(subwavelist)
                    sigma = np.std(subwavelist)
                    del subwavelist
                    digi1_ped_mean.append(mean)
                    digi1_threshold.append(mean-5.0*sigma)
                    DigitizerPedMean[ch] = mean
                    DigitizerPedWidth[ch] = sigma
                #get pedestals digitizer 2
                for ch in range(0,4,1):
                    subwavelist = []
                    for bin in range(1500,2560,1):
                        if abs(thisDigi2[ch][bin])<10:
                            subwavelist.append(thisDigi2[ch][bin])
                    mean2 = np.mean(subwavelist)
                    sigma2 = np.std(subwavelist)
                    del subwavelist
                    digi2_ped_mean.append(mean2)
                    digi2_threshold.append(mean2-5.0*sigma2)
                    DigitizerPedMean[ch+4] = mean2
                    DigitizerPedWidth[ch+4] = sigma2
                #prepare for digitizer waveform pulse finding and charge integration
                #initialize the 2d arrays that hold pmt pulse charge, startbin,...
                for pmtNNN in range(8):
                    for pulseN in range(20):
                        DigitizerPulseCharge[pmtNNN][pulseN] = 0.0
                        DigitizerPulseStartBin[pmtNNN][pulseN] = 0.0
                        DigitizerPulseEndBin[pmtNNN][pulseN] = 0.0
                # for digitizer 1
                for ch in range(0,4,1):
                    #begin my own algorithm for pulse finding
                    maximum = thisDigi1[ch][np.argmin(thisDigi1[ch][80:])+80] # get the amplitude of the pulse. note: dont consider the first 80 bins because of some weird small pulse in the beginning of the waveform!!
                    DigitizerAmplitude[ch] = -1.0*(maximum-digi1_ped_mean[ch])
                    nPulses = 0
                    flagStartFound = 0
                    #flagEndFound = 0
                    #if no signal (maximum is below threshold), no need to do anything, but fill nPulses=0 is needed
                    if maximum >= digi1_threshold[ch]:
                        DigitizerNumberOfPulses[ch] = nPulses
                        continue
                    bin=80
                    while bin>=80 and bin<(2560-4):
                        #find the start bin of a pulse in a waveform
                        #To define a cross over event: two bins below threshold and two bins above threshold
                        if nPulses==20: #maximum number of pulses, if 20 pulses are found then stop the searching
                            break
                        #Okay, begin my searching. Find the first signal rising cross-threshold
                        if flagStartFound==0:
                            if thisDigi1[ch][bin]>digi1_threshold[ch] and thisDigi1[ch][bin+1]>digi1_threshold[ch] and thisDigi1[ch][bin+2]<digi1_threshold[ch] and thisDigi1[ch][bin+3]<thisDigi1[ch][bin+2]:
                                #if the condition is true, then it crosses threshold between bin+1 and bin+2
                                DigitizerPulseStartBin[ch][nPulses] = bin - 1
                                flagStartFound = 1
                        #then, find the signal falling cross-threshold
                        if flagStartFound==1:
                            if thisDigi1[ch][bin]<digi1_threshold[ch] and thisDigi1[ch][bin+1]<digi1_threshold[ch] and thisDigi1[ch][bin+2]>digi1_threshold[ch] and thisDigi1[ch][bin+3]>digi1_threshold[ch]:
                                DigitizerPulseEndBin[ch][nPulses] = bin+5
                                nPulses+=1
                                flagStartFound = 0
                        bin+=1
                    #Combine some of the found pulses if they are separated <= 25 ns.
                    peakxL = []
                    peakxR = []
                    if nPulses>0:
                        realN = 1
                        peakxL.append(DigitizerPulseStartBin[ch][0])
                        peakxR.append(DigitizerPulseEndBin[ch][0])
                        for oldN in range(1,nPulses,1):
                            if ( DigitizerPulseStartBin[ch][oldN] - peakxR[realN-1] ) <= 25:
                                peakxR[realN-1] = DigitizerPulseEndBin[ch][oldN]
                            else:
                                realN = realN + 1
                                peakxL.append(DigitizerPulseStartBin[ch][oldN])
                                peakxR.append(DigitizerPulseEndBin[ch][oldN])
                        nPulses = realN
                    #remove the bad peaks in the spectrum whose width is <=10 ns.
                    nremove = 0
                    for cnt in range(0,nPulses,1):
                        if (peakxR[cnt-nremove]-peakxL[cnt-nremove]) <= 10:
                            peakxR.remove(peakxR[cnt-nremove])
                            peakxL.remove(peakxL[cnt-nremove])
                            nPulses = nPulses-1
                            nremove = nremove + 1
                    #print "evt " + str(int(evtkey)) + ", ch " + str(ch) + ", pulses " + str(nPulses)
                    #for ncnt in range(0,nPulses,1):
                    #    print "start at ", peakxL[ncnt], ", end at ", peakxR[ncnt]
                    if nPulses>20:
                        print "evt ", int(evtkey), "ch ", ch, "nPulses ", nPulses
                        nPulses=20
                    #Now compute charge integration
                    for nn in range(nPulses):
                        DigitizerPulseCharge[ch][nn] = np.sum(thisDigi1[ch][int(peakxL[nn]):int(peakxR[nn])])-digi1_ped_mean[ch]*(peakxR[nn]-peakxL[nn]+1)
                        DigitizerPulseStartBin[ch][nn] = peakxL[nn]
                        DigitizerPulseEndBin[ch][nn] = peakxR[nn]
                    DigitizerNumberOfPulses[ch] = nPulses
                #for digitizer 2
                for ch in range(0,4,1):
                    #begin my own algorithm for pulse finding
                    maximum = thisDigi2[ch][np.argmin(thisDigi2[ch][80:])+80]
                    DigitizerAmplitude[ch+4] = -1.0*(maximum-digi2_ped_mean[ch])
                    nPulses = 0
                    flagStartFound = 0
                    #flagEndFound = 0
                    if maximum >= digi2_threshold[ch]:
                        DigitizerNumberOfPulses[ch+4] = nPulses
                        continue
                    bin=80
                    while bin>=80 and bin<(2560-4):
                        #find the start bin of a pulse in a waveform
                        #To define a cross over threshold: two bins below threshold and two bins above threshold
                        if nPulses==20: #maximum number of pulses 
                            break
                        if flagStartFound==0:
                            if thisDigi2[ch][bin]>digi2_threshold[ch] and thisDigi2[ch][bin+1]>digi2_threshold[ch] and thisDigi2[ch][bin+2]<digi2_threshold[ch] and thisDigi2[ch][bin+3]<thisDigi2[ch][bin+2]:
                                #if the condition is true, then it crosses threshold between bin+1 and bin+2
                                DigitizerPulseStartBin[ch+4][nPulses] = bin - 1
                                flagStartFound = 1
                        if flagStartFound==1:
                            if thisDigi2[ch][bin]<digi2_threshold[ch] and thisDigi2[ch][bin+1]<digi2_threshold[ch] and thisDigi2[ch][bin+2]>digi2_threshold[ch] and thisDigi2[ch][bin+3]>digi2_threshold[ch]:
                                DigitizerPulseEndBin[ch+4][nPulses] = bin+5
                                nPulses+=1
                                flagStartFound = 0
                        bin+=1
                    peakxL = []
                    peakxR = []
                    if nPulses>0:
                        realN = 1
                        peakxL.append(DigitizerPulseStartBin[ch+4][0])
                        peakxR.append(DigitizerPulseEndBin[ch+4][0])
                        for oldN in range(1,nPulses,1):
                            if ( DigitizerPulseStartBin[ch+4][oldN] - peakxR[realN-1] ) <= 25:
                                peakxR[realN-1] = DigitizerPulseEndBin[ch+4][oldN]
                            else:
                                realN = realN + 1
                                peakxL.append(DigitizerPulseStartBin[ch+4][oldN])
                                peakxR.append(DigitizerPulseEndBin[ch+4][oldN])
                        nPulses = realN
                    #remove the bad peaks in the spectrum whose width is <=10 ns.
                    nremove = 0
                    for cnt in range(0,nPulses,1):
                        if (peakxR[cnt-nremove]-peakxL[cnt-nremove]) <= 10:
                            peakxR.remove(peakxR[cnt-nremove])
                            peakxL.remove(peakxL[cnt-nremove])
                            nPulses = nPulses-1
                            nremove = nremove + 1
                    #print "evt " + str(int(evtkey)) + ", ch " + str(ch+4) + ", pulses " + str(nPulses)
                    #for ncnt in range(nPulses):
                    #    print "start at ", peakxL[ncnt], ", end at ", peakxR[ncnt]
                    if nPulses>20:
                        print "evt ", int(evtkey), "ch ", ch+4, "nPulses ", nPulses
                        nPulses = 20
                    #Now compute charge integration
                    for nn in range(nPulses):
                        DigitizerPulseCharge[ch+4][nn] = np.sum(thisDigi2[ch][int(peakxL[nn]):int(peakxR[nn])])-digi2_ped_mean[ch]*(peakxR[nn]-peakxL[nn]+1)
                        DigitizerPulseStartBin[ch+4][nn] = peakxL[nn]
                        DigitizerPulseEndBin[ch+4][nn] = peakxR[nn]
                    DigitizerNumberOfPulses[ch+4] = nPulses
            mytree.Fill()
            #if int(evtkey) >20:    break
    rootfile.cd()
    rootfile.Write()
    rootfile.Close()
    file.close()
    os.remove(filename)

elaspsed = timeit.default_timer() - start_time

print "Time: ", elaspsed, " seconds."

#draw histograms of QDC channels



