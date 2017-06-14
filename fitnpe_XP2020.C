// fit ADC spectra from PMT to extract mean number of photo electrons

// fit parameters: 
//                    par0 = pedestal position
//                    par1 = pedestal width
//                    par2 = Single photo electron peak position
//                    par3 = Single photo electron peak width
//                    par4 = exponential background decrease
//                    par5 = background parameter probability
//                    par6 = mean number of photo electrons

#define PI 3.1415926

Double_t Gn_Bg(Int_t n, Double_t *x, Double_t *par) {
  
  // convolution of Gausian N with exponential background
  // this simulates tails 

  Double_t a = par[4];
  Double_t ped = par[0]; // pedestal position
  Double_t ps  = par[1]; // pedestal width
  
  Double_t pos = ped + ((Double_t) n ) * par[2]; // nth gauss peak position
  Double_t s   = TMath::Sqrt( ps * ps + 
		       ((Double_t) n ) * par[3] * par[3]); // nth gauss width


  Double_t y = x[0] - pos - a*s*s;
  Double_t sy = 1.;
  if (y!=0.)
    sy = TMath::Abs(y)/y;

  Double_t res1 = a/2.*TMath::Exp(-a*y)*
    ( TMath::Erf( TMath::Abs(ped-pos-a*s*s)/s/sqrt(2.) ) +
      sy * TMath::Erf( TMath::Abs(y)/s/sqrt(2.) ) );

  return res1;
  
}


Double_t Gn(Int_t n, Double_t *x, Double_t *par){


  // nth gaussain convoluted with pedestal 

  Double_t ped = par[0]; // pedestal position
  Double_t ps  = par[1]; // pedestal width
  Double_t pos = ped + ((Double_t) n ) * par[2]; // nth gauss peak position
  Double_t s   = TMath::Sqrt( ps * ps + 
		       ((Double_t) n ) * par[3] * par[3]); // nth gauss width

  Double_t y = x[0];
  Double_t e = y-pos;
  Double_t gn = 1./s/TMath::Sqrt(2.*PI)*exp(-e*e/2./s/s);

  return gn;

}


Double_t Conv(Double_t *x, Double_t *par){


  Double_t mu = par[6]; // mean number of photo electrons
  Double_t w = par[5]; // background probability parameter

  Double_t sum = 0.;

  //
  Double_t Amplitude = par[7]; // number of entries in spectrum

  for (Int_t i=0;i<20;i++){

    Double_t a = TMath::Power(mu,(Double_t)i)*
      TMath::Exp(-mu)/TMath::Factorial(i);

    Double_t b = (1.-w) * Gn(i,x,par);
    Double_t c = 0.;

    Double_t pos = par[0]+(Double_t) i * par[2];
    Double_t sig1 = TMath::Sqrt(par[1]*par[1]+par[3]*par[3]*(Double_t)i);

    if (x[0]>par[0]) {
      c = w * Gn_Bg(i,x,par);
    }

    sum += a * ( b + c ) * Amplitude;
    
  }
  

  return sum;


}

Double_t IdealResponse(Double_t *x,Double_t *par){
    Double_t mu = par[0];
    Double_t q = par[1];
    Double_t sigma = par[2];
    Double_t amplitude = par[3];
    Double_t sum=0;
    for(Int_t n=1; n<50; n++){
        sum += TMath::Power(mu,n)*TMath::Exp(-1.0*mu)/TMath::Factorial(n)*TMath::Exp(-1.0*(x[0]-q*n)**2/(2.0*n*sigma**2))/(sigma*TMath::Sqrt(2.0*PI*n));
    }
    return sum*amplitude;
}

void drawIdeal(){
      gStyle->SetOptFit(1111);
      TF1* Fideal = new TF1("Fideal",IdealResponse,25,3000,4);
      Fideal->SetParNames("Npe","SpeP","SpeW");
      Fideal->SetParameter(0,1);
      Fideal->SetParameter(1,90);
      Fideal->SetParameter(2,34);
      Fideal->Draw();
}

void fitIdeal(fstream &fout, TH1F *adc, int iii){
      gStyle->SetOptFit(1111);
      TF1* Fideal = new TF1("Fideal",IdealResponse,0,500,4);
      Fideal->SetParNames("Npe","Peak","Width","Amplitude");
      Fideal->SetLineColor(1); Fideal->SetLineStyle(2);

      Fideal->SetParameter(0,10);
      if(iii==0){
          Fideal->SetParameter(1,117);
          Fideal->SetParameter(2,44);
      }
      if(iii==1){
          Fideal->SetParameter(1,115);
          Fideal->SetParameter(2,59);
      }
      if(iii==2){
          Fideal->SetParameter(1,85.0/0.86);
          Fideal->SetParameter(2,37.0/0.86);
      }
      if(iii==3){
          Fideal->SetParameter(1,123);
          Fideal->SetParameter(2,49);
      }
      if(iii==4){
          Fideal->SetParameter(1,127);
          Fideal->SetParameter(2,44);
      }
      if(iii==5){
          Fideal->SetParameter(0,0.8);
          Fideal->SetParameter(1,116);
          Fideal->SetParameter(2,42);
      }
 
      Double_t amp = 0;
      Double_t par[4];
      for(Int_t i=20;i<adc->GetNbinsX();i++)
            amp += adc->GetBinContent(i+1);
      Fideal->SetParameter(3,amp);
      //adc->Fit("Fideal","RQ");

      for(int i=0;i<3;i++){
          //if(iii !=5) 
          adc->Fit("Fideal","R","",par[1]-1.2*par[2],500); //par[1]-1.2*par[2]
          //else adc->Fit("Fideal","R","",60,1000); //par[1]-1.2*par[2]
          Fideal->GetParameters(par);
          Fideal->SetParameters(par);

      }
      Fideal->GetParameters(par);
      fout<<adc->GetName()<<"\t";
      for(Int_t j=0;j<4;j++){
          fout<<par[j]<<"\t"<<Fideal->GetParError(j)<<"\t";
      }
      fout<<endl;
      adc->GetXaxis()->SetRangeUser(0,500);
      adc->Draw();
}

void fitadc(TString datadir, Int_t RunNumber, TH1F *adc){


  // fit the full adc spectra incuding pedestal with gaussians
  // to extract the mean number of photo electrons

  cout<<"begin"<<endl;
  gStyle->SetOptFit(1111);
  TF1 *fitf = new TF1("fitf",Conv,0.,2000.,8);

  fitf->SetParNames("P0","s0","P1","s1","a","w","mu","Norm");
  fitf->SetParLimits(0,0.,22.);     // pedestal position
  fitf->SetParLimits(1,0.0,5);     // pedestal width
  fitf->SetParLimits(2,5.,120.);   // Single photo-electron peak
  fitf->SetParLimits(3,2.,60.);     // width of it
  fitf->SetParLimits(4,0.0,100.);      // exponential background
  fitf->SetParLimits(5,0.0,1.);       // background probability
  fitf->SetParLimits(6,.5,3.);       // mean number of photo electrons
  
  fitf->SetParameter(0,7);  // fix pedestal position
  fitf->SetParameter(1,2);   // fix pedestal width
  fitf->SetParameter(2,90);  // fix 1 photon peak position
  fitf->SetParameter(3,35);  // fix width
  fitf->SetParameter(4,0);
  fitf->SetParameter(5,0.05);
  fitf->SetParameter(6,1.3);  
  
  Int_t mbin = adc->GetMaximumBin(); 
  cout<<"maximum found at bin "<<mbin<<endl;
  
  Double_t lowli = (Double_t) mbin - 3.;
  Double_t higli = (Double_t) mbin + 3.;
  adc->Fit("gaus","R","",lowli,higli);
  TF1 *gf = adc->GetFunction("gaus");
  Double_t gp = gf->GetParameter(1);
  Double_t gw = gf->GetParameter(2);
  cout<<"First ped = "<<gp<<"\twidth = "<<gw<<endl;
  lowli = gp-1.*gw;
  higli = gp+1.*gw;
  adc->Fit("gaus","R","",lowli,higli);
  gf = adc->GetFunction("gaus");
  gp = gf->GetParameter(1);
  gw = gf->GetParameter(2);
  // cout<<"Minuit status: "<<gMinuit->GetStatus()<<endl;

  cout<< "Pedestal= "<<gp<<"       Width="<<gw<<endl;
  fitf->FixParameter(0,0);  // fix pedestal position
  fitf->FixParameter(1,gw);   // fix pedestal width
  
  fitf->SetLineColor(2);
  
//  Double_t Norm = adc->GetEntries();

 Double_t Norm=0,iternator=0;
 for (Int_t i=0;i<1500;i++)
  {iternator=adc->GetBinContent(i);
   Norm +=iternator;
  }
  cout<<"Normalization factor: "<<Norm<<endl;
  fitf->SetParameter(7,Norm);       // set normalization
  //fitf->ReleaseParameter(7);
  
  
  // determine maximum in historgram other than the pedestal
  
  Double_t P1Pos = fitf->GetParameter(2)+gp;
  Double_t YMax = adc->GetBinContent((Int_t)P1Pos);
  Double_t bincontent, bincontent15;
  Int_t binmax, bin15;
  for (Int_t XBin=P1Pos-7;XBin<1500;XBin++){
    bincontent = adc->GetBinContent(XBin);
    if (bincontent>YMax){
      YMax = bincontent;
      binmax = XBin;
cout<<"Bin reading"<<binmax<<endl;
cout<<"Yvalue "<<YMax<<endl;
    }
  }
  YMax *= 2.0;
  
  Double_t Lower_limit = 25;
  Double_t Higher_limit = 1000;
 
  Int_t Fit_status = adc->Fit("fitf","R","",Lower_limit, Higher_limit);
  cout<<"start setting ymax"<<endl;
  
  //adc->SetMaximum(YMax);  //set y-axis upper limit 
  adc->GetXaxis()->SetRange(0,1000);
  cout<<"success setting ymax"<<endl; 
  TPaveStats *st = (TPaveStats*)adc->GetListOfFunctions()->FindObject("stats");
  
  //adc->Draw();

  Double_t chi2 = fitf->GetChisquare();
  Double_t NFreePar =  (Double_t)fitf->GetNDF();
  Double_t chi2PerDeg = chi2/NFreePar;

  ofstream FOut;

  char ffil[128];
  sprintf(ffil,"%s/fitresults_kuraray.txt",datadir.Data());
  FOut.open(ffil, ios::out | ios::app);

  cout<<"start print numbers "<<endl;
  cout<<RunNumber<<"  ";
  cout<<fitf->GetParameter(0)<<"  "<<fitf->GetParError(0)<<"  ";
  cout<<fitf->GetParameter(1)<<"  "<<fitf->GetParError(1)<<"  ";
  cout<<fitf->GetParameter(2)<<"  "<<fitf->GetParError(2)<<"  ";
  cout<<fitf->GetParameter(3)<<"  "<<fitf->GetParError(3)<<"  ";
  cout<<fitf->GetParameter(4)<<"  "<<fitf->GetParError(4)<<"  ";
  cout<<fitf->GetParameter(5)<<"  "<<fitf->GetParError(5)<<"  ";
  cout<<fitf->GetParameter(6)<<"  "<<fitf->GetParError(6)<<"  ";
  cout<<Lower_limit<<"  "<<Higher_limit<<"  "<<chi2PerDeg<<"  ";
  cout<<Fit_status<<endl;

 cout<<"start print numbers to file "<<endl;
  
  FOut<<RunNumber<<"  ";
  FOut<<fitf->GetParameter(0)<<"  "<<fitf->GetParError(0)<<"  ";
  FOut<<fitf->GetParameter(1)<<"  "<<fitf->GetParError(1)<<"  ";
  FOut<<fitf->GetParameter(2)<<"  "<<fitf->GetParError(2)<<"  ";
  FOut<<fitf->GetParameter(3)<<"  "<<fitf->GetParError(3)<<"  ";
  FOut<<fitf->GetParameter(4)<<"  "<<fitf->GetParError(4)<<"  ";
  FOut<<fitf->GetParameter(5)<<"  "<<fitf->GetParError(5)<<"  ";
  FOut<<fitf->GetParameter(6)<<"  "<<fitf->GetParError(6)<<"  ";
  FOut<<Lower_limit<<"  "<<Higher_limit<<"  "<<chi2PerDeg<<"  ";
  FOut<<Fit_status<<endl;
  
  FOut.close();

}

