void Read_Tree_make_plots_v1(){
    // prepare for filenames to be processed.
    // the logic here is to read ROOT tree files and plot histograms
    // more trees can be read at same time, but only one ROOT file will be saved (histograms get higher statistics).
    const int NbOfFilesToRead = 2;
    string filepath = "./../Water_1T_data_sample/";
    string rootfilename[NbOfFilesToRead] ={"run7925","run7925"};
    string postfix = "_Tree.root";
    string outputrootfilename = "./ResultsDir/run7925_Histos.root";

    // some mapping inforamtion
    string sTriggerType[4]={"AllTrig","MultiTrig","CosmicTrig","LedTrig"};
    string sQDC1ChMap[8]={"H0","H1","H2","H3","H4","H5","",""};
    string sQDC2ChMap[8]={"S0","","S2","S3","S4","S5","S1",""};
    string sDigiChMap[8]={"Digi1_CH0_S0","Digi1_CH1_S1","Digi1_CH2_S2","Digi1_CH3_S3","Digi2_CH0_S4","Digi2_CH1_S5","Digi2_CH2_S6","Digi2_CH3_S7"}

    // define the histograms
    // each has 4 trigger types: all, multiplicity, cosmic and led.
    // root file to save histograms
    TFile* rtfile = new TFile(outputrootfilename.c_str(),"recreate");
    TDirectory* dirQDC = rtfile->mkdir("QDC");
    TDirectory* dirDigitizer = rtfile->mkdir("Digitizer");
    TH1F* hQDC1[8][4];
    TH1F* hQDC2[8][4];
    TH1F* hDigiCharge[6][4];
    TH1F* hDigiAmp[6][4];
    TH1F* hDigiST[6][4];
    TH1F* hDigiRT[6][4];
    TH1F* hDigiPW[6][4];
    // initialze the histograms
    for(int i=0;i<8;i++){
        char tempname[50];
        for(int j=0;j<4;j++){
            //QDC1 & QDC2 histogram
            if(strcmp(sQDC1ChMap[i].c_str(),"")!=0){
                sprintf(tempname,"hQDC1_CH%d_%s_%s",i, sQDC1ChMap[i],sTriggerType[j]);
                hQDC1[i][j] = new TH1F(tempname,"",1000,0,1000);
                hQDC1[i][j]->SetXTitle("QDC channel");
                hQDC1[i][j]->SetYTitle("Counts");
            //cout<<hQDC1[i][j]->GetName()<<endl;
            }
            if(strcmp(sQDC2ChMap[i].c_str(),"")!=0){
                sprintf(tempname,"hQDC2_CH%d_%s_%s",i,sQDC2ChMap[i],sTriggerType[j]);
                hQDC2[i][j] = new TH1F(tempname,"",1000,0,1000);
                hQDC2[i][j]->SetXTitle("QDC channel");
                hQDC2[i][j]->SetYTitle("Counts");
            }
    
            //Digitizers
            if(i<6){
                sprintf(tempname,"hCharge_%s_%s",sDigiChMap[i],sTriggerType[j]);
                hDigiCharge[i][j] = new TH1F(tempname,"",1500,0,3000);
                hDigiCharge[i][j]->SetXTitle("ADC channel");
                hDigiCharge[i][j]->SetYTitle("Counts");
                sprintf(tempname,"hAmp_%s_%s",sDigiChMap[i],sTriggerType[j]);
                hDigiAmp[i][j] = new TH1F(tempname,"",1500,0,3000);
                hDigiAmp[i][j]->SetXTitle("ADC channel");
                hDigiAmp[i][j]->SetYTitle("Counts");
                sprintf(tempname,"hStartTime_%s_%s",sDigiChMap[i],sTriggerType[j]);
                hDigiST[i][j] = new TH1F(tempname,"",300,850,1150);
                hDigiST[i][j]->SetXTitle("Time bin number");
                hDigiST[i][j]->SetYTitle("Counts");
                sprintf(tempname,"hRiseTime_%s_%s",sDigiChMap[i],sTriggerType[j]);
                hDigiRT[i][j] = new TH1F(tempname,"",80,-20,60);
                hDigiRT[i][j]->SetXTitle("Time bin number");
                hDigiRT[i][j]->SetYTitle("Counts");
                sprintf(tempname,"hPulseWidth_%s_%s",sDigiChMap[i],sTriggerType[j]);
                hDigiPW[i][j] = new TH1F(tempname,"",310,-10,300);    
                hDigiPW[i][j]->SetXTitle("Time bin number");
                hDigiPW[i][j]->SetYTitle("Counts");
            }
        }
    }//end initialzing histogramgs

    // starting reading ROOT tree files and fill histograms
    for(int aa = 0; aa<NbOfFilesToRead; aa++){
        string thisfilename = filepath + rootfilename[aa] + postfix;
        cout<<thisfilename<<endl;
        TFile* rootfile = new TFile(thisfilename.c_str(),"read");
        TTree* tree = (TTree*)rootfile->Get("OneTonEvent");

        // the branchses in that tree
        TBranch* bEvtNumber = tree->GetBranch("EvtNumber");
        TBranch* bEvtTime = tree->GetBranch("EvtTime");
        TBranch* bTemperatureBox = tree->GetBranch("TemperatureBox");
        TBranch* bTemperatureRack = tree->GetBranch("TemperatureRack");
        TBranch* bResistivity = tree->GetBranch("Resistivity");
        TBranch* bQDC1 = tree->GetBranch("QDC1");
        TBranch* bQDC2 = tree->GetBranch("QDC2");
        TBranch* bTDC = tree->GetBranch("TDC");
        TBranch* bScaler = tree->GetBranch("Scaler");
        TBranch* bDigitizerCharge = tree->GetBranch("DigitizerCharge");
        TBranch* bDigitizerAmplitude = tree->GetBranch("DigitizerAmplitude");
        TBranch* bDigitizerStartTimeBin = tree->GetBranch("DigitizerStartTimeBin");
        TBranch* bDigitizerRiseTime = tree->GetBranch("DigitizerRiseTime");
        TBranch* bDigitizerPulseWidth = tree->GetBranch("DigitizerPulseWidth");
        TBranch* bDigitizerPedMean = tree->GetBranch("DigitizerPedMean");
        TBranch* bDigitizerPedWidth = tree->GetBranch("DigitizerPedWidth");
        TBranch* bTrigType = tree->GetBranch("TrigType")   ;
        // variables of the tree branches
        int evtNb;
        double evtT;
        float evtTempBox;
        float evtTempRack;
        float evtResist;
        float evtQDC1[8]     ;
        float evtQDC2[8];
        float evtTDC[16];
        float evtScaler[17];
        float evtDigiCharge[6];
        float evtDigiAmplitude[6];
        float evtDigiST[6]; //start time bin
        float evtDigiRT[6]; //rise time
        float evtDigiPW[6]; // pulse width
        float evtDigiPM[6]; // pedestal mean
        float evtDigiPS[6];//  pedestal width
        int evtTrigType;
        bEvtNumber->SetAddress(&evtNb);
        bEvtTime->SetAddress(&evtT);
        bTemperatureBox->SetAddress(&evtTempBox);
        bTemperatureRack->SetAddress(&evtTempRack);
        bResistivity->SetAddress(&evtResist);
        bQDC1->SetAddress(&evtQDC1);
        bQDC2->SetAddress(&evtQDC2);
        bTDC->SetAddress(&evtTDC);
        bScaler->SetAddress(&evtScaler);
        bDigitizerCharge->SetAddress(&evtDigiCharge);
        bDigitizerAmplitude->SetAddress(&evtDigiAmplitude);
        bDigitizerStartTimeBin->SetAddress(&evtDigiST);
        bDigitizerRiseTime->SetAddress(&evtDigiRT);
        bDigitizerPulseWidth->SetAddress(&evtDigiPW);
        bDigitizerPedMean->SetAddress(&evtDigiPM);
        bDigitizerPedWidth->SetAddress(&evtDigiPS);
        bTrigType->SetAddress(&evtTrigType);

        int nentries = (int)tree->GetEntries();
        for(int i=0;i<nentries;i++){
            if(i%100 ==0) cout<<i<<endl;
            bEvtNumber->GetEntry(i);
            bEvtTime->GetEntry(i);
            bTemperatureBox->GetEntry(i);
            bTemperatureRack->GetEntry(i);

            bResistivity->GetEntry(i);
            bQDC1->GetEntry(i);
            bQDC2->GetEntry(i);
            bTDC->GetEntry(i);
            bScaler->GetEntry(i);
            bDigitizerCharge->GetEntry(i);
            bDigitizerAmplitude->GetEntry(i);
            bDigitizerStartTimeBin->GetEntry(i);
            bDigitizerRiseTime->GetEntry(i);
            bDigitizerPulseWidth->GetEntry(i);
            bDigitizerPedMean->GetEntry(i);
            bDigitizerPedWidth->GetEntry(i);
            bTrigType->GetEntry(i);
            bEvtTime->GetEntry(i);

            for(int k=0;k<8;k++){
               if(strcmp(sQDC1ChMap[k].c_str(),"")!=0){
                   //cout<<k<<"\t"<<evtQDC1[k]<<endl;
                   hQDC1[k][0]->Fill(evtQDC1[k]);
                   hQDC1[k][evtTrigType]->Fill(evtQDC1[k]);
               }
               if(strcmp(sQDC2ChMap[k].c_str(),"")!=0){
                   hQDC2[k][0]->Fill(evtQDC2[k]);
                   hQDC2[k][evtTrigType]->Fill(evtQDC2[k]);
               }

               if(k<6){
                  if( (evtDigiAmplitude[k]) > (5.0*evtDigiPS[k]) ){
                    hDigiCharge[k][0]->Fill(evtDigiCharge[k]);
                    hDigiAmp[k][0]->Fill(evtDigiAmplitude[k]);
                    hDigiST[k][0]->Fill(evtDigiST[k]);
                    hDigiRT[k][0]->Fill(evtDigiRT[k]);
                    hDigiPW[k][0]->Fill(evtDigiPW[k]);
 
                    hDigiCharge[k][evtTrigType]->Fill(evtDigiCharge[k]);
                    hDigiAmp[k][evtTrigType]->Fill(evtDigiAmplitude[k]);
                    hDigiST[k][evtTrigType]->Fill(evtDigiST[k]);
                    hDigiRT[k][evtTrigType]->Fill(evtDigiRT[k]);
                    hDigiPW[k][evtTrigType]->Fill(evtDigiPW[k]);

                  }
               }

            }
        }

        rootfile->Close();
  }//end reading ROOT tree

    for(int i=0;i<8;i++){
        for(int j=0;j<4;j++){
            dirQDC->cd();
            if(strcmp(sQDC1ChMap[i].c_str(),"")!=0) hQDC1[i][j]->Write();
            if(strcmp(sQDC2ChMap[i].c_str(),"")!=0) hQDC2[i][j]->Write();
            dirDigitizer->cd();
            if(i<6){
                hDigiCharge[i][j]->Write();
                hDigiAmp[i][j]->Write();
                hDigiST[i][j]->Write();
                hDigiRT[i][j]->Write();
                hDigiPW[i][j]->Write();
            }
        }
    }
    rtfile->Close();
}
