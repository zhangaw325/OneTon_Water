//ideal PMT response function
#include "fitnpe_XP2020.C"

void ReadResults_EachSignalChannel(){
    gStyle->SetOptStat(1111);
    gStyle->SetOptFit(1111);
    fstream fout("SPE_Fit_Par.txt",ios::out);

    TFile* rootfile = new TFile("run9042-9053-24ns.root","read");
    TH1F* hS0Led = (TH1F*)rootfile->Get("Digitizer/hCharge_Digi1_CH0_S0_LedTrig;1");
    TH1F* hS0Splitter = (TH1F*)rootfile->Get("Digitizer/hCharge_Digi1_CH0_S0_LEDTrig_S0Only;1");

    TH1F* hS1Led = (TH1F*)rootfile->Get("Digitizer/hCharge_Digi1_CH1_S1_LedTrig;1");
    TH1F* hS1Splitter = (TH1F*)rootfile->Get("Digitizer/hCharge_Digi1_CH1_S1_LEDTrig_S1Only;1");

    TH1F* hS2Led = (TH1F*)rootfile->Get("Digitizer/hCharge_Digi1_CH2_S2_LedTrig;1");
    TH1F* hS2Splitter = (TH1F*)rootfile->Get("Digitizer/hCharge_Digi1_CH2_S2_LEDTrig_S2Only;1");

    TH1F* hS3Led = (TH1F*)rootfile->Get("Digitizer/hCharge_Digi1_CH3_S3_LedTrig;1");
    TH1F* hS3Splitter = (TH1F*)rootfile->Get("Digitizer/hCharge_Digi1_CH3_S3_LEDTrig_S3Only;1");

    TH1F* hS4Led = (TH1F*)rootfile->Get("Digitizer/hCharge_Digi2_CH0_S4_LedTrig;1");
    TH1F* hS4Splitter = (TH1F*)rootfile->Get("Digitizer/hCharge_Digi2_CH0_S4_LEDTrig_S4Only;1");

    TH1F* hS5Led = (TH1F*)rootfile->Get("Digitizer/hCharge_Digi2_CH1_S5_LedTrig;1");
    TH1F* hS5Splitter = (TH1F*)rootfile->Get("Digitizer/hCharge_Digi2_CH1_S5_LEDTrig_S5Only;1");
    //hS0Led->SetLineColor(1);
    //hS0Splitter->SetLineColor(1);     hS0Splitter->SetLineStyle(2); 

    TCanvas* c = new TCanvas();
    c->Divide(3,2);
    TPaveStats *st = 0;

    c->cd(1);
    hS0Led->Draw();
    fitIdeal(fout,hS0Led,0);
    c->Update();
    st = (TPaveStats*)hS0Led->GetListOfFunctions()->FindObject("stats");
    st->SetY1NDC(0.6); st->SetY2NDC(0.9);
    st->SetX1NDC(0.5); st->SetX2NDC(0.9);
    c->Update();
    hS0Splitter->SetLineColor(2); hS0Splitter->SetLineStyle(2); hS0Splitter->Draw("sames");
    c->Update();
    st = (TPaveStats*)hS0Splitter->GetListOfFunctions()->FindObject("stats");
    st->SetY1NDC(0.3); st->SetY2NDC(0.6);
    st->SetX1NDC(0.5); st->SetX2NDC(0.9);
    c->Modified(); c->Update();

    c->cd(2);
    hS1Led->Draw();
    fitIdeal(fout,hS1Led,1);
    c->Update();
    st = (TPaveStats*)hS1Led->GetListOfFunctions()->FindObject("stats");
    st->SetY1NDC(0.6); st->SetY2NDC(0.9);
    st->SetX1NDC(0.5); st->SetX2NDC(0.9);
    c->Update();

    hS1Splitter->SetLineColor(2); hS1Splitter->SetLineStyle(2); hS1Splitter->Draw("sames");
    c->Update();
    st = (TPaveStats*)hS1Splitter->GetListOfFunctions()->FindObject("stats");
    st->SetY1NDC(0.3); st->SetY2NDC(0.6);
    st->SetX1NDC(0.5); st->SetX2NDC(0.9);
    c->Modified(); c->Update();


    c->cd(3);
    hS2Led->Draw(); hS2Led->GetXaxis()->SetRangeUser(0,500);
    //fitIdeal(fout,hS2Led,2);
    c->Update();
    st = (TPaveStats*)hS2Led->GetListOfFunctions()->FindObject("stats");
    st->SetY1NDC(0.6); st->SetY2NDC(0.9);
    st->SetX1NDC(0.5); st->SetX2NDC(0.9);
    c->Update();

    hS2Splitter->SetLineColor(2); hS2Splitter->SetLineStyle(2); hS2Splitter->Draw("sames");
    c->Update();
    st = (TPaveStats*)hS2Splitter->GetListOfFunctions()->FindObject("stats");
    st->SetY1NDC(0.3); st->SetY2NDC(0.6);
    st->SetX1NDC(0.5); st->SetX2NDC(0.9);
    c->Modified(); c->Update();


    c->cd(4);
    hS3Led->Draw();
    fitIdeal(fout,hS3Led,3);
    c->Update();
    st = (TPaveStats*)hS3Led->GetListOfFunctions()->FindObject("stats");
    st->SetY1NDC(0.6); st->SetY2NDC(0.9);
    st->SetX1NDC(0.5); st->SetX2NDC(0.9);
    c->Update();

    hS3Splitter->SetLineColor(2); hS3Splitter->SetLineStyle(2); hS3Splitter->Draw("sames");
    c->Update();
    st = (TPaveStats*)hS3Splitter->GetListOfFunctions()->FindObject("stats");
    st->SetY1NDC(0.3); st->SetY2NDC(0.6);
    st->SetX1NDC(0.5); st->SetX2NDC(0.9);
    c->Modified(); c->Update();


    c->cd(5);
    hS4Led->Draw();
    fitIdeal(fout,hS4Led,4);
    c->Update();
    st = (TPaveStats*)hS4Led->GetListOfFunctions()->FindObject("stats");
    st->SetY1NDC(0.6); st->SetY2NDC(0.9);
    st->SetX1NDC(0.5); st->SetX2NDC(0.9);
    c->Update();

    hS4Splitter->SetLineColor(2); hS4Splitter->SetLineStyle(2); hS4Splitter->Draw("sames");
    c->Update();
    st = (TPaveStats*)hS4Splitter->GetListOfFunctions()->FindObject("stats");
    st->SetY1NDC(0.3); st->SetY2NDC(0.6);
    st->SetX1NDC(0.5); st->SetX2NDC(0.9);
    c->Modified(); c->Update();


    c->cd(6);
    hS5Led->Draw();
    fitIdeal(fout,hS5Led,5);
    c->Update();
    st = (TPaveStats*)hS5Led->GetListOfFunctions()->FindObject("stats");
    st->SetY1NDC(0.6); st->SetY2NDC(0.9);
    st->SetX1NDC(0.5); st->SetX2NDC(0.9);
    c->Update();

    hS5Splitter->SetLineColor(2); hS5Splitter->SetLineStyle(2); hS5Splitter->Draw("sames");
    c->Update();
    st = (TPaveStats*)hS5Splitter->GetListOfFunctions()->FindObject("stats");
    st->SetY1NDC(0.3); st->SetY2NDC(0.6);
    st->SetX1NDC(0.5); st->SetX2NDC(0.9);
    c->Modified(); c->Update();
    c->Modified(); c->Update();

}
