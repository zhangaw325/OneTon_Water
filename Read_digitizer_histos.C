//#include "fitPMT_NPE.C"
#include "fitnpe_XP2020.C"
#include "Read_Tree_make_plots_v1.C"

void Read_digitizer_histos(){

    gStyle->SetOptFit(1111);

    Read_Tree_make_plots_v1();

    TVirtualFitter::SetDefaultFitter("Minuit2");
    ROOT::Math::MinimizerOptions::SetDefaultMinimizer("Minuit2");

    TFile* rootfile = new TFile("./run8393-8400-26.5ns.root","read");
    string ParTextFile = "run8393-8400-26.5ns_par.txt";
    TCanvas* cDigiCharge = new TCanvas();
    cDigiCharge->SetName("digiCharge_LedTrig");
    cDigiCharge->Divide(3,2);
    TH1F* hDigiChargeLedTrig[6];
    //TH2F* hScatterChargeSTLedTrig[6];
    string sDigiChMap[8]={"Digi1_CH0_S0","Digi1_CH1_S1","Digi1_CH2_S2","Digi1_CH3_S3","Digi2_CH0_S4","Digi2_CH1_S5","Digi2_CH2_S6","Digi2_CH3_S7"}
    char hTitleDigiChargeLedTrig[50];
    fstream fout(ParTextFile.c_str(),ios::out); //fout.close();
    for(int i=0;i<6;i++){
        cDigiCharge->cd(i+1);
        sprintf(hTitleDigiChargeLedTrig,"Digitizer/hCharge_%s_LedTrig;1",sDigiChMap[i]);
        //sprintf(hTitleDigiChargeLedTrig,"Digitizer/hCharge_vs_PW_%s_LedTrig;1",sDigiChMap[i]);
        cout<<hTitleDigiChargeLedTrig<<endl;
        hDigiChargeLedTrig[i] = (TH1F*)rootfile->Get(hTitleDigiChargeLedTrig);
        hDigiChargeLedTrig[i]->SetTitle(hTitleDigiChargeLedTrig);
        hDigiChargeLedTrig[i]->SetXTitle("ADC channel");
        //hDigiChargeLedTrig[i]->GetXaxis()->SetRangeUser(0,500);
        //fitadc("",1,hDigiChargeLedTrig[i]);

        
        fitIdeal(fout,hDigiChargeLedTrig[i],i);

        cDigiCharge->Modified(); cDigiCharge->Update();
        TPaveStats *ps = (TPaveStats*) hDigiChargeLedTrig[i]->GetListOfFunctions()->FindObject("stats");
        ps->SetX1NDC(0.3);
        ps->SetX2NDC(0.9);
        ps->SetY1NDC(0.5);
        ps->SetY2NDC(0.9);
        ps->Draw();
        cDigiCharge->Modified(); cDigiCharge->Update();


        //hDigiChargeLedTrig[i]->Draw();
    }

    string sQDC2ChMap[8]={"S0","","S2","S3","S4","S5","S1",""};
    TH1F* hQDC2LedTrig[8];
    char hTitleQDC2LedTrig[50];
    TCanvas* cQDC2 = new TCanvas();
    cQDC2->SetName("QDC2_LedTrig");
    cQDC2->Divide(3,2);
    int mm = 0;
    for(int i=0;i<8;i++){
        if(i==1 || i==7) continue;
        mm++;
        cQDC2->cd(mm);
        sprintf(hTitleQDC2LedTrig,"QDC/hQDC2_CH%d_%s_LedTrig;1",i,sQDC2ChMap[i]);
        hQDC2LedTrig[i] = (TH1F*)rootfile->Get(hTitleQDC2LedTrig);
        //hQDC2LedTrig[i]->Draw();
    }
    cQDC2->Close();
}
