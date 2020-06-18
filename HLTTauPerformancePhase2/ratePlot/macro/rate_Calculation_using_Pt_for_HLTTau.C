#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>
#include <iostream>
#include <TLorentzVector.h>
#include <TH1.h>
#include <TH2.h>
#include <TH3.h>
#include <TMath.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TPaveText.h>
#include <TStyle.h>
#include <TROOT.h>
#include <sstream>
#include <TBranchElement.h>
#include <fstream>
#include <map>

using namespace std;

/*
  void rate_Calculation()
  {
  TString fileName_In = "/home/sbhowmik/NTuple_Phase2/HLTTau/NTuple_test_HLTTauAnalyzer_NeutrinoGun_20190502.root";
  TString treeName_In = "HLTTauAnalyzer/HLTTauAnalyzer";
  TString fileName_Out = "/home/sbhowmik/Phase2/Tallinn/CMSSW_10_5_0_pre1/src/HLTTauAnalyzer/HLTTauAnalyzer/script/ratePlot/results/hist_rate_HLTTau_NeutrinoGun.root";
*/


void rate_Calculation_using_Pt_for_HLTTau(TString fileName_In, TString treeName_In, TString fileName_Out)
{

  TFile fileIn(fileName_In.Data(),"READ");
  TTree* treeIn = (TTree*)fileIn.Get(treeName_In);
  TFile fileOut(fileName_Out, "RECREATE");

  double targetRate_singleTau = 50.0 ; 
  double targetRate_DoubleoTau = 12.0 ; 
  double eta_max_HLTTau = 2.4;
  double dzMax = 0.40;

  char outfile[200];
  char outfilx[200];
  int len = strlen(fileName_Out);
  strncpy(outfilx, fileName_Out, len-4);
  outfilx[len-4]='\0';
  sprintf (outfile,"%stxt",outfilx);
  ofstream fileOut_txt(outfile);

  ULong64_t       EventNumber =  0;
  Int_t           RunNumber =  0;
  Int_t           lumi =  0;
  vector<float>   *hltTauPt =  0;
  vector<float>   *hltTauEta =  0;
  Int_t          Denominator = 0;

  treeIn->SetBranchAddress("EventNumber", &EventNumber);
  treeIn->SetBranchAddress("RunNumber", &RunNumber);
  treeIn->SetBranchAddress("lumi", &lumi);
  treeIn->SetBranchAddress("hltTauPt", &hltTauPt);
  treeIn->SetBranchAddress("hltTauEta", &hltTauEta);

  TH1F* hist_Single_hltTauPt    = new TH1F("Pt_Single_HLTTau","Pt_Single_HLTTau",250,0.,250.);

  TH1F* hist_Rate_Single_hltTauPt    = new TH1F("Rate_Single_HLTTau","Rate_Single_HLTTau",250,0.,250.);

  TH2F* hist_Double_hltTauPt    = new TH2F("Pt_Double_HLTTau","Pt_Double_HLTTau",250,0.,250., 250,0.,250.);

  TH1F* hist_Rate_Double_hltTauPt    = new TH1F("Rate_Double_HLTTau","Rate_Double_HLTTau",250,0.,250.);

  float freq = 28.0E6 / 1000; // to make scale in kHz 
  float pu = 200;
  float scale = freq;

  bool firstTrue_SingleTau = true;

  bool firstTrue_DoubleTau = true;

  for(UInt_t i_event = 0 ; i_event < treeIn->GetEntries() ; ++i_event){
    treeIn->GetEntry(i_event);
    if(i_event%10000==0) cout<<"Entry #"<<i_event<<endl; 

    ++Denominator;

    // Start For Single Tau
    float max_HLTTau_Pt = 0.;

    for(UInt_t iHLTTau = 0 ; iHLTTau < hltTauPt->size() ; ++iHLTTau){
      if(fabs(hltTauEta->at(iHLTTau))>eta_max_HLTTau) continue;
      if (hltTauPt->at(iHLTTau) <= 0) continue;

      if ( hltTauPt->at(iHLTTau) > max_HLTTau_Pt ) max_HLTTau_Pt = hltTauPt->at(iHLTTau);
    }
    if(max_HLTTau_Pt!=0){
      hist_Single_hltTauPt->Fill(max_HLTTau_Pt);
    }
    // End For Single Tau 
    
    
    // Start For Di Tau
 
    bool diTau_Pass=false;
    
    for(UInt_t iHLTTau = 0 ; iHLTTau < hltTauPt->size() ; ++iHLTTau){
      if(fabs(hltTauEta->at(iHLTTau))>eta_max_HLTTau) continue;
      if (hltTauPt->at(iHLTTau) <= 0) continue;
      
      if (!diTau_Pass){
	for(UInt_t kHLTTau = iHLTTau+1 ; kHLTTau < hltTauPt->size() ; ++kHLTTau){
	  if(fabs(hltTauEta->at(kHLTTau))>eta_max_HLTTau) continue;
	  if (hltTauPt->at(kHLTTau) <= 0) continue;
	  
	  hist_Double_hltTauPt->Fill(hltTauPt->at(iHLTTau), hltTauPt->at(kHLTTau));
	  diTau_Pass=true;
	  break;
	}
      }
    } //for(UInt_t iHLTTau = 0 ; iHLTTau < hltTauPt->size() ; ++iHLTTau){
    
      // End For Di Tau 
    
    
  } // for(UInt_t i = 0 ; i < treeIn->GetEntries() ; ++i)
  
  cout<<"Denominator = "<<Denominator<<endl;








  for(UInt_t i_PtBin = 1 ; i_PtBin <= 251 ; ++i_PtBin){
    hist_Rate_Single_hltTauPt->SetBinContent(i_PtBin+1, hist_Single_hltTauPt->Integral(i_PtBin+1,251)/Denominator*freq);
    
    if(firstTrue_SingleTau && hist_Rate_Single_hltTauPt->GetBinContent(i_PtBin+1) <= targetRate_singleTau){
      cout << "SingleTau Rate " << hist_Rate_Single_hltTauPt->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "SingleTau Rate " << hist_Rate_Single_hltTauPt->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      firstTrue_SingleTau = false;
    }

    
    hist_Rate_Double_hltTauPt->SetBinContent(i_PtBin+1, hist_Double_hltTauPt->Integral(i_PtBin+1,251,i_PtBin+1,251)/Denominator*freq);

    if(firstTrue_DoubleTau && hist_Rate_Double_hltTauPt->GetBinContent(i_PtBin+1) <= targetRate_DoubleoTau){
      cout << "DoubleTau Rate " << hist_Rate_Double_hltTauPt->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "DoubleTau Rate " << hist_Rate_Double_hltTauPt->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      firstTrue_DoubleTau = false;
    }
  }
  
  hist_Single_hltTauPt->Write();

  hist_Rate_Single_hltTauPt->Write();

  hist_Double_hltTauPt->Write();

  hist_Rate_Double_hltTauPt->Write();



  return;
}
