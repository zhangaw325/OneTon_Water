import h5py
import numpy as np
import matplotlib.pyplot as plt
#import graphUtils
from ROOT import TCanvas, TH1F, TGraph, TH1D, TLegend, TFile, TDirectory, TTree
import datetime
import time
from array import array

#some initial numbers
NbQDC1CH = 8  #QDC1 CHs 0 1 2 3 4 5 are used for H0, 1, 2, 3, 4, 5. now just include unused channels in tree
NbQDC2CH = 8  #QDC2 CHs 0 6 2 3 4 5 are used for S0, 1, 2, 3, 4, 5.
NbTDCCH = 16
NbScalerCH = 17
NbDigiCH = 6
NSamples = 2560 # Number of samples for each digitizer channel

#prepare file names to be read
hdf5_file_name = ['/media/sf_E_DRIVE/Research/BNL-EDG/1T_Water_data/Water_1T_data_sample/run7925.h5','/media/sf_E_DRIVE/Research/BNL-EDG/1T_Water_data/Water_1T_data_sample/run7926.h5','/media/sf_E_DRIVE/Research/BNL-EDG/1T_Water_data/Water_1T_data_sample/run7927.h5','/media/sf_E_DRIVE/Research/BNL-EDG/1T_Water_data/Water_1T_data_sample/run7928.h5','/media/sf_E_DRIVE/Research/BNL-EDG/1T_Water_data/Water_1T_data_sample/run7929.h5','/media/sf_E_DRIVE/Research/BNL-EDG/1T_Water_data/Water_1T_data_sample/run7930.h5','/media/sf_E_DRIVE/Research/BNL-EDG/1T_Water_data/Water_1T_data_sample/run7931.h5','/media/sf_E_DRIVE/Research/BNL-EDG/1T_Water_data/Water_1T_data_sample/run7932.h5']

#prepare histograms and ROOT file
rootfile = TFile("./ResultsDir/Tree-Run7925-7932-v1.root","recreate")
mytree = TTree( 'OneTonEvent', 'My Event Tree' )

EvtNumber = array('i', [0])
EvtTime = array('d',[0]) #need to think
TemperatureBox = array('f',[0.])
TemperatureRack = array('f',[0.])
Resistivity = array('f',[0.])
QDC1 = array('f',NbQDC1CH*[0.])
QDC2 = array('f',NbQDC2CH*[0.])
TDC = array('f',NbTDCCH*[0.])
Scaler = array('f',NbScalerCH*[0.])
DigitizerCharge = array('f',NbDigiCH*[0.])
DigitizerAmplitude = array('f',NbDigiCH*[0.])
DigitizerStartTimeBin = array('f',NbDigiCH*[0.])
DigitizerRiseTime =  array('f',NbDigiCH*[0.])
DigitizerPulseWidth = array('f',NbDigiCH*[0.])
DigitizerPedMean = array('f',NbDigiCH*[0.])
DigitizerPedWidth = array('f',NbDigiCH*[0.])
TrigType = array('i',[0]) # I'' use 1 -> multiplicity, 2 -> Cosmic and 3->LED triggers

mytree.Branch("EvtNumber",EvtNumber,"EvtNumber/I")
mytree.Branch("EvtTime",EvtTime,"EvtTime/D")
mytree.Branch("TemperatureBox",TemperatureBox,"TemperatureBox/F")
mytree.Branch("TemperatureRack",TemperatureRack,"TemperatureRack/F")
mytree.Branch("Resistivity",Resistivity,"Resistivity/F")
mytree.Branch("QDC1",QDC1,"QDC1[8]/F")
mytree.Branch("QDC2",QDC2,"QDC2[8]/F")
mytree.Branch("TDC",TDC,"TDC[16]/I")
mytree.Branch("Scaler",Scaler,"Scaler[17]/F")
mytree.Branch("DigitizerCharge",DigitizerCharge,"DigitizerCharge[6]/F")
mytree.Branch("DigitizerAmplitude",DigitizerAmplitude,"DigitizerAmplitude[6]/F")
mytree.Branch("DigitizerStartTimeBin",DigitizerStartTimeBin,"DigitizerStartTimeBin[6]/F")
mytree.Branch("DigitizerRiseTime",DigitizerRiseTime,"DigitizerRiseTime[6]/F")
mytree.Branch("DigitizerPulseWidth",DigitizerPulseWidth,"DigitizerPulseWidth[6]/F")
mytree.Branch("DigitizerPedMean",DigitizerPedMean,"DigitizerPedMean[6]/F")
mytree.Branch("DigitizerPedWidth",DigitizerPedWidth,"DigitizerPedWidth[6]/F")
mytree.Branch("TrigType",TrigType,"TrigType/I")

#histograms for holding digitizer waveform pedestals
hDigi1_ped_list = []
hDigi2_ped_list = []
for i in range(0,4,1):
    histname = "Digi_1_ped_Ch_" + str(i)
    thishist4 = TH1F(histname,"",80,-8,8)
    thishist4.SetXTitle("Pedestal (ADC channels)")
    thishist4.SetYTitle("Counts")
    thishist4.SetLineWidth(2)
    thishist4.SetLineColor(i+1)
    hDigi1_ped_list.append(thishist4)
    #digi2
    histname = "Digi_2_ped_Ch_" + str(i)
    thishist4 = TH1F(histname,"",80,-8,8)
    thishist4.SetXTitle("Pedestal (ADC channels)")
    thishist4.SetYTitle("Counts")
    thishist4.SetLineWidth(2)
    thishist4.SetLineColor(i+1)
    hDigi2_ped_list.append(thishist4)

totalEvtNumber = 0
for filename in hdf5_file_name: 
    file = h5py.File(filename,'r')
    #CalData1 = file['Calibration']['Digitizer_1']['Pedestal']
    #CalData2 = file['Calibration']['Digitizer_2']['Pedestal']
    EvtDir = file['Events']
    #read h5 file and fill histograms
    #timeCnt = 0;
    initCnts=[] #initial counts (the first event) in scaler, all active channels
    initTime=0 #initial time (the first event)
    # I will use trigFlag for MultiTrig (1), CosmicTrig (2) and LedTrig (3)
    trigFlag = 0
    for evtkey in EvtDir.keys():
        if not(evtkey=='evt_table'):
            EvtNumber[0] = totalEvtNumber
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
            trig_temp1, trig_temp2, trig_temp3, thistrig = 0, 0, 0, 1
            for ch, num in thisTDC:
                if int(ch) == 7: # multiplicity
                    trig_temp1 = 1
                if int(ch) == 6: # cosmic
                    trig_temp2 = 2
                if int(ch) == 8: # led trigger
                    trig_temp3 = 3
                if int(ch) == 9:
                    thistrig = 1
            if thistrig==1 and trig_temp1 == 1 and trig_temp2 != 2 and trig_temp3 != 3:
                trigFlag = 1
            if thistrig==1 and trig_temp1 != 1 and trig_temp2 == 2 and trig_temp3 != 3:
                trigFlag = 2
            if thistrig==1 and trig_temp1 != 1 and trig_temp2 != 2 and trig_temp3 == 3:
                trigFlag = 3
            TrigType[0] = trigFlag
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
            for ch, num in thisTDC:
                TDC[int(ch)] = num
            #process ADC data
            digi1_ped_mean = []
            digi1_threshold = []
            digi2_ped_mean = []
            digi2_threshold = []
            mean, mean2 = 0, 0
            sigma, sigma2 = 0, 0
            if np.mod(int(evtkey),1) == 0:
                if np.mod(int(totalEvtNumber),100) ==0:    print evtkey, totalEvtNumber
                #get pedestals
                for ch in range(0,4,1):
                    for bin in range(0,2560,1):
                        if bin >= 100 and bin<=800:
                            hDigi1_ped_list[ch].Fill(thisDigi1[ch][bin])
                    #fit pedestal digi 1
                    hDigi1_ped_list[ch].Fit("gaus","Q")
                    mean = hDigi1_ped_list[ch].GetFunction("gaus").GetParameter(1)
                    sigma = hDigi1_ped_list[ch].GetFunction("gaus").GetParameter(2)
                    digi1_ped_mean.append(mean)
                    digi1_threshold.append(mean-5.0*sigma)
                    DigitizerPedMean[ch] = mean
                    DigitizerPedWidth[ch] = sigma
                for ch in range(0,2,1):
                    for bin in range(0,2560,1):
                        if bin >= 100 and bin<=800:
                            hDigi2_ped_list[ch].Fill(thisDigi2[ch][bin])
                    #fit pedestal digi 2
                    hDigi2_ped_list[ch].Fit("gaus","Q")
                    mean2 = hDigi2_ped_list[ch].GetFunction("gaus").GetParameter(1)
                    sigma2 = hDigi2_ped_list[ch].GetFunction("gaus").GetParameter(2)
                    digi2_ped_mean.append(mean2)
                    digi2_threshold.append(mean2-5.0*sigma2)
                    DigitizerPedMean[ch+4] = mean2
                    DigitizerPedWidth[ch+4] = sigma2
                #get charge speactrum
                for ch in range(0,4,1):
                    thischarge = 0
                    startT = 0
                    maxT = 0
                    endT = 0
                    for bin in range(801,1050,1):
                        if thisDigi1[ch][bin] < digi1_threshold[ch]:
                            startT = bin
                            break
                    maxq = thisDigi1[ch][800]
                    for bin in range(801,1050,1):
                        if thisDigi1[ch][bin] < digi1_threshold[ch]:
                            thischarge += thisDigi1[ch][bin] - digi1_ped_mean[ch]
                            if thisDigi1[ch][bin]<maxq:
                                maxq = thisDigi1[ch][bin]
                                maxT = bin
                    for bin in range(maxT,1050,1):
                        if thisDigi1[ch][bin] > digi1_threshold[ch]:
                            endT = bin
                            break
                    if maxq < digi1_threshold[ch]:
                        DigitizerAmplitude[ch] = -1.0*(maxq-digi1_ped_mean[ch])
                        DigitizerCharge[ch] = -1.0*thischarge
                        DigitizerPulseWidth[ch]= endT-startT
                        DigitizerStartTimeBin[ch] = startT
                        #print startT, DigitizerStartTimeBin[ch]
                        DigitizerRiseTime[ch] = maxT - startT
                #for digi 2
                for ch in range(0,2,1):
                    thischarge = 0
                    startT2 = 0
                    maxT2 = 0
                    endT2 = 0
                    for bin in range(801,1050,1):
                        if thisDigi2[ch][bin] < digi2_threshold[ch]:
                            startT2 = bin
                            break
                    maxq2 = thisDigi2[ch][800]
                    for bin in range(801,1050,1):
                        if thisDigi2[ch][bin] < digi2_threshold[ch]:
                            thischarge += thisDigi2[ch][bin]-digi2_ped_mean[ch]
                            if thisDigi2[ch][bin]<maxq2:
                                maxq2 = thisDigi2[ch][bin]
                                maxT2 = bin
                    for bin in range(maxT,1050,1):
                        if thisDigi2[ch][bin] > digi2_threshold[ch]:
                            endT2 = bin
                            break
                    if maxq2 < digi2_threshold[ch]:
                        DigitizerAmplitude[ch+4] = -1.0*(maxq2-digi2_ped_mean[ch])
                        DigitizerCharge[ch+4] = -1.0*thischarge
                        DigitizerPulseWidth[ch+4]= endT2-startT2
                        DigitizerStartTimeBin[ch+4] = startT2
                        DigitizerRiseTime[ch+4] = maxT2 - startT2
                for i in range(0,4,1):
                     for bin in range(0,80,1):
                        hDigi1_ped_list[i].SetBinContent(bin,0)
                        hDigi2_ped_list[i].SetBinContent(bin,0)
            mytree.Fill()
            #if int(evtkey) == 10:    break
    file.close()

#draw histograms of QDC channels
rootfile.cd()
rootfile.Write()
rootfile.Close()


