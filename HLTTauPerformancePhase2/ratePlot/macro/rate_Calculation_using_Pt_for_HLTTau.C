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
  TString fileName_In = "/home/sbhowmik/NTuple_Phase2/L1PFTau/NTuple_test_L1PFTauAnalyzer_NeutrinoGun_20190502.root";
  TString treeName_In = "L1PFTauAnalyzer/L1PFTauAnalyzer";
  TString fileName_Out = "/home/sbhowmik/Phase2/Tallinn/CMSSW_10_5_0_pre1/src/L1TauAnalyzer/L1PFTauAnalyzer/script/ratePlot/results/hist_rate_L1PFTau_NeutrinoGun.root";
*/


void rate_Calculation_using_Pt_for_HLTTau(TString fileName_In, TString treeName_In, TString fileName_Out)
{

  TFile fileIn(fileName_In.Data(),"READ");
  TTree* treeIn = (TTree*)fileIn.Get(treeName_In);
  TFile fileOut(fileName_Out, "RECREATE");
  TTree* treeOut = new TTree("HLTTauAnalyzer", "HLTTauAnalyzer");

  double targetRate_singleTau = 50.0 ; 
  double targetRate_DoubleoTau = 12.0 ; 
  double tau_eta_max = 2.4;
  //double tau_eta_max = 1.4;
  double tau_eta_min = 0;
  double tau_Pt_min = 0.0;
  double tauLeadTrack_Pt_min = 5.0;
  double dzMax = 0.20;

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
  vector<int>   *hltTauTightIso =  0;
  vector<int>   *hltTauMediumIso =  0;
  vector<int>   *hltTauLooseIso =  0;
  vector<int>   *hltTauVLooseIso =  0;
  vector<int>   *hltTauTightRelIso =  0;
  vector<int>   *hltTauMediumRelIso =  0;
  vector<int>   *hltTauLooseRelIso =  0;
  vector<int>   *hltTauVLooseRelIso =  0;
  vector<float>   *hltTauZ =  0;
  vector<float>   *hltTauLeadTrackPt =  0;
  Int_t          Denominator = 0;
  //vector<float>   *hltTauBDT =  0;

  treeIn->SetBranchAddress("EventNumber", &EventNumber);
  treeIn->SetBranchAddress("RunNumber", &RunNumber);
  treeIn->SetBranchAddress("lumi", &lumi);
  treeIn->SetBranchAddress("hltTauPt", &hltTauPt);
  treeIn->SetBranchAddress("hltTauEta", &hltTauEta);
  treeIn->SetBranchAddress("hltTauTightIso", &hltTauTightIso);
  treeIn->SetBranchAddress("hltTauMediumIso", &hltTauMediumIso);
  treeIn->SetBranchAddress("hltTauLooseIso", &hltTauLooseIso);
  treeIn->SetBranchAddress("hltTauVLooseIso", &hltTauVLooseIso);
  treeIn->SetBranchAddress("hltTauTightRelIso", &hltTauTightRelIso);
  treeIn->SetBranchAddress("hltTauMediumRelIso", &hltTauMediumRelIso);
  treeIn->SetBranchAddress("hltTauLooseRelIso", &hltTauLooseRelIso);
  treeIn->SetBranchAddress("hltTauVLooseRelIso", &hltTauVLooseRelIso);
  treeIn->SetBranchAddress("hltTauZ", &hltTauZ);
  treeIn->SetBranchAddress("hltTauLeadTrackPt", &hltTauLeadTrackPt);
  //treeIn->SetBranchAddress("hltTauBDT", &hltTauBDT);

  treeOut -> Branch("EventNumber",&EventNumber,"EventNumber/l");
  treeOut -> Branch("RunNumber",&RunNumber,"RunNumber/I");
  treeOut -> Branch("lumi",&lumi,"lumi/I");

  TH1F* hist_Single_hltTauPt_NoCut    = new TH1F("Pt_Single_HLTTau_NoCut","Pt_Single_HLTTau_NoCut",250,0.,250.);
  TH1F* hist_Single_hltTauPt_dZ        = new TH1F("Pt_Single_HLTTau_dZ","Pt_Single_HLTTau_dZ",250,0.,250.);
  TH1F* hist_Single_hltTauPt_Tight     = new TH1F("Pt_Single_HLTTau_Tight","Pt_Single_HLTTau_Tight",250,0.,250.);
  TH1F* hist_Single_hltTauPt_Medium    = new TH1F("Pt_Single_HLTTau_Medium","Pt_Single_HLTTau_Medium",250,0.,250.);
  TH1F* hist_Single_hltTauPt_Loose     = new TH1F("Pt_Single_HLTTau_Loose","Pt_Single_HLTTau_Loose",250,0.,250.);
  TH1F* hist_Single_hltTauPt_VLoose    = new TH1F("Pt_Single_HLTTau_VLoose","Pt_Single_HLTTau_VLoose",250,0.,250.);

  TH1F* hist_Rate_Single_hltTauPt_NoCut    = new TH1F("Rate_Single_HLTTau_NoCut","Rate_Single_HLTTau_NoCut",250,0.,250.);
  TH1F* hist_Rate_Single_hltTauPt_dZ        = new TH1F("Rate_Single_HLTTau_dZ","Rate_Single_HLTTau_dZ",250,0.,250.);
  TH1F* hist_Rate_Single_hltTauPt_Tight     = new TH1F("Rate_Single_HLTTau_Tight","Rate_Single_HLTTau_Tight",250,0.,250.);
  TH1F* hist_Rate_Single_hltTauPt_Medium    = new TH1F("Rate_Single_HLTTau_Medium","Rate_Single_HLTTau_Medium",250,0.,250.);
  TH1F* hist_Rate_Single_hltTauPt_Loose     = new TH1F("Rate_Single_HLTTau_Loose","Rate_Single_HLTTau_Loose",250,0.,250.);
  TH1F* hist_Rate_Single_hltTauPt_VLoose    = new TH1F("Rate_Single_HLTTau_VLoose","Rate_Single_HLTTau_VLoose",250,0.,250.);

  TH2F* hist_Double_hltTauPt_NoCut    = new TH2F("Pt_Double_HLTTau_NoCut","Pt_Double_HLTTau_NoCut",250,0.,250., 250,0.,250.);
  TH2F* hist_Double_hltTauPt_dZ        = new TH2F("Pt_Double_HLTTau_dZ","Pt_Double_HLTTau_dZ",250,0.,250., 250,0.,250.);
  TH2F* hist_Double_hltTauPt_Tight     = new TH2F("Pt_Double_HLTTau_Tight","Pt_Double_HLTTau_Tight",250,0.,250., 250,0.,250.);
  TH2F* hist_Double_hltTauPt_Medium    = new TH2F("Pt_Double_HLTTau_Medium","Pt_Double_HLTTau_Medium",250,0.,250., 250,0.,250.);
  TH2F* hist_Double_hltTauPt_Loose     = new TH2F("Pt_Double_HLTTau_Loose","Pt_Double_HLTTau_Loose",250,0.,250., 250,0.,250.);
  TH2F* hist_Double_hltTauPt_VLoose    = new TH2F("Pt_Double_HLTTau_VLoose","Pt_Double_HLTTau_VLoose",250,0.,250., 250,0.,250.);

  TH1F* hist_Rate_Double_hltTauPt_NoCut    = new TH1F("Rate_Double_HLTTau_NoCut","Rate_Double_HLTTau_NoCut",250,0.,250.);
  TH1F* hist_Rate_Double_hltTauPt_dZ        = new TH1F("Rate_Double_HLTTau_dZ","Rate_Double_HLTTau_dZ",250,0.,250.);
  TH1F* hist_Rate_Double_hltTauPt_Tight     = new TH1F("Rate_Double_HLTTau_Tight","Rate_Double_HLTTau_Tight",250,0.,250.);
  TH1F* hist_Rate_Double_hltTauPt_Medium    = new TH1F("Rate_Double_HLTTau_Medium","Rate_Double_HLTTau_Medium",250,0.,250.);
  TH1F* hist_Rate_Double_hltTauPt_Loose     = new TH1F("Rate_Double_HLTTau_Loose","Rate_Double_HLTTau_Loose",250,0.,250.);
  TH1F* hist_Rate_Double_hltTauPt_VLoose    = new TH1F("Rate_Double_HLTTau_VLoose","Rate_Double_HLTTau_VLoose",250,0.,250.);

  float freq = 28.0E6 / 1000; // to make scale in kHz 
  float pu = 200;
  float scale = freq;

  bool firstTrue_SingleTau_NoCut = true;
  bool firstTrue_SingleTau_dZ = true;
  bool firstTrue_SingleTau_VLoose = true;
  bool firstTrue_SingleTau_Loose = true;
  bool firstTrue_SingleTau_Medium = true;
  bool firstTrue_SingleTau_Tight = true;

  bool firstTrue_DoubleTau_NoCut = true;
  bool firstTrue_DoubleTau_dZ = true;
  bool firstTrue_DoubleTau_VLoose = true;
  bool firstTrue_DoubleTau_Loose = true;
  bool firstTrue_DoubleTau_Medium = true;
  bool firstTrue_DoubleTau_Tight = true;

  for(UInt_t i_event = 0 ; i_event < treeIn->GetEntries() ; ++i_event){
    treeIn->GetEntry(i_event);
    if(i_event%10000==0) cout<<"Entry #"<<i_event<<endl; 

    ++Denominator;

    // Start For Single Tau
    float max_HLTTau_Pt_NoCut = 0.;
    float max_HLTTau_Pt_dZ = 0.;
    float max_HLTTau_Pt_Tight = 0.;
    float max_HLTTau_Pt_Medium = 0.;
    float max_HLTTau_Pt_Loose = 0.;
    float max_HLTTau_Pt_VLoose = 0.;

    for(UInt_t iHLTTau = 0 ; iHLTTau < hltTauPt->size() ; ++iHLTTau){
      if(fabs(hltTauEta->at(iHLTTau))>tau_eta_max) continue;
      if(fabs(hltTauEta->at(iHLTTau))<tau_eta_min) continue;
      if (hltTauPt->at(iHLTTau) <= tau_Pt_min) continue;
      if (hltTauLeadTrackPt->at(iHLTTau) <= tauLeadTrack_Pt_min) continue;

      if ( hltTauPt->at(iHLTTau) > max_HLTTau_Pt_NoCut ) max_HLTTau_Pt_NoCut = hltTauPt->at(iHLTTau);
      if ( hltTauPt->at(iHLTTau) > max_HLTTau_Pt_dZ ) max_HLTTau_Pt_dZ = hltTauPt->at(iHLTTau);
      if (hltTauTightRelIso->at(iHLTTau)==1){
      //if (hltTauBDT->at(iHLTTau)>-0.7){
	if ( hltTauPt->at(iHLTTau) > max_HLTTau_Pt_Tight ) max_HLTTau_Pt_Tight = hltTauPt->at(iHLTTau);
      }
      if (hltTauMediumRelIso->at(iHLTTau)==1){
      //if (hltTauBDT->at(iHLTTau)>-0.9){
	if ( hltTauPt->at(iHLTTau) > max_HLTTau_Pt_Medium ) max_HLTTau_Pt_Medium = hltTauPt->at(iHLTTau);
      }
      if (hltTauLooseRelIso->at(iHLTTau)==1){
      //if (hltTauBDT->at(iHLTTau)>-0.925){
	if ( hltTauPt->at(iHLTTau) > max_HLTTau_Pt_Loose ) max_HLTTau_Pt_Loose = hltTauPt->at(iHLTTau);
      }
      if (hltTauVLooseRelIso->at(iHLTTau)==1){
      //if (hltTauBDT->at(iHLTTau)>-0.95){
	if ( hltTauPt->at(iHLTTau) > max_HLTTau_Pt_VLoose ) max_HLTTau_Pt_VLoose = hltTauPt->at(iHLTTau);
      }
    }
    if(max_HLTTau_Pt_NoCut!=0){
      hist_Single_hltTauPt_NoCut->Fill(max_HLTTau_Pt_NoCut);
    }
    if(max_HLTTau_Pt_dZ!=0){
      hist_Single_hltTauPt_dZ->Fill(max_HLTTau_Pt_dZ);
    }
    if(max_HLTTau_Pt_Tight!=0){
      hist_Single_hltTauPt_Tight->Fill(max_HLTTau_Pt_Tight);
    }
    if(max_HLTTau_Pt_Medium!=0){
      hist_Single_hltTauPt_Medium->Fill(max_HLTTau_Pt_Medium);
    }
    if(max_HLTTau_Pt_Loose!=0){
      hist_Single_hltTauPt_Loose->Fill(max_HLTTau_Pt_Loose);
    }
    if(max_HLTTau_Pt_VLoose!=0){
      hist_Single_hltTauPt_VLoose->Fill(max_HLTTau_Pt_VLoose);
    }
    // End For Single Tau 
    
    
    // Start For Di Tau
 
    bool dzPass_NoCut=false;
    bool dzPass_dZ=false;
    bool dzPass_Tight=false;
    bool dzPass_Medium=false;
    bool dzPass_Loose=false;
    bool dzPass_VLoose=false;
    bool dzPass_Tight_Pt40=false;
    
    for(UInt_t iHLTTau = 0 ; iHLTTau < hltTauPt->size() ; ++iHLTTau){
      if(fabs(hltTauEta->at(iHLTTau))>tau_eta_max) continue;
      if(fabs(hltTauEta->at(iHLTTau))<tau_eta_min) continue;
      if (hltTauPt->at(iHLTTau) <= tau_Pt_min) continue;
      if (hltTauLeadTrackPt->at(iHLTTau) <= tauLeadTrack_Pt_min) continue;

      if (!dzPass_NoCut){
	for(UInt_t kHLTTau = iHLTTau+1 ; kHLTTau < hltTauPt->size() ; ++kHLTTau){
	  if(fabs(hltTauEta->at(kHLTTau))>tau_eta_max) continue;
	  if(fabs(hltTauEta->at(kHLTTau))<tau_eta_min) continue;
	  if (hltTauPt->at(kHLTTau) <= tau_Pt_min) continue;
	  if (hltTauLeadTrackPt->at(kHLTTau) <= tauLeadTrack_Pt_min) continue;
	  
	  hist_Double_hltTauPt_NoCut->Fill(hltTauPt->at(iHLTTau), hltTauPt->at(kHLTTau));
	  dzPass_NoCut=true;
	  break;
	}
      }
      
      if (!dzPass_dZ){
	for(UInt_t kHLTTau = iHLTTau+1 ; kHLTTau < hltTauPt->size() ; ++kHLTTau){
	  if(fabs(hltTauEta->at(kHLTTau))>tau_eta_max) continue;
	  if(fabs(hltTauEta->at(kHLTTau))<tau_eta_min) continue;
	  if (hltTauPt->at(kHLTTau) <= tau_Pt_min) continue;
	  if (hltTauLeadTrackPt->at(kHLTTau) <= tauLeadTrack_Pt_min) continue;

	  double dz = TMath::Abs(hltTauZ->at(iHLTTau) - hltTauZ->at(kHLTTau));
	  if(dz<dzMax){
	    //if(dz<dzMax || (hltTauPt->at(iHLTTau)>75 && hltTauPt->at(kHLTTau)>75)){
	    hist_Double_hltTauPt_dZ->Fill(hltTauPt->at(iHLTTau), hltTauPt->at(kHLTTau));
	    dzPass_dZ=true;
	    break;
	  }
	}
      }

      if (hltTauTightRelIso->at(iHLTTau)==1 && !dzPass_Tight){
      //if (hltTauBDT->at(iHLTTau)>-0.7 && !dzPass_Tight){
	for(UInt_t kHLTTau = iHLTTau+1 ; kHLTTau < hltTauPt->size() ; ++kHLTTau){
	  if(fabs(hltTauEta->at(kHLTTau))>tau_eta_max) continue;
	  if(fabs(hltTauEta->at(kHLTTau))<tau_eta_min) continue;
	  if (hltTauPt->at(kHLTTau) <= tau_Pt_min) continue;
          if (hltTauLeadTrackPt->at(kHLTTau) <= tauLeadTrack_Pt_min) continue;
	  
	  if (hltTauTightRelIso->at(kHLTTau)==1){
	  //if (hltTauBDT->at(kHLTTau)>-0.7){
	    double dz = TMath::Abs(hltTauZ->at(iHLTTau) - hltTauZ->at(kHLTTau));
	    if(dz<dzMax){
	      //if(dz<dzMax || (hltTauPt->at(iHLTTau)>75 && hltTauPt->at(kHLTTau)>75)){
	      hist_Double_hltTauPt_Tight->Fill(hltTauPt->at(iHLTTau), hltTauPt->at(kHLTTau));
	      dzPass_Tight=true;
	      break;
	    }
	  }
	}
      }

      if (hltTauMediumRelIso->at(iHLTTau)==1 && !dzPass_Medium){
      //if (hltTauBDT->at(iHLTTau)>-0.9 && !dzPass_Medium){
	for(UInt_t kHLTTau = iHLTTau+1 ; kHLTTau < hltTauPt->size() ; ++kHLTTau){
	  if(fabs(hltTauEta->at(kHLTTau))>tau_eta_max) continue;
	  if(fabs(hltTauEta->at(kHLTTau))<tau_eta_min) continue;
	  if (hltTauPt->at(kHLTTau) <= tau_Pt_min) continue;
          if (hltTauLeadTrackPt->at(kHLTTau) <= tauLeadTrack_Pt_min) continue;

	  if (hltTauMediumRelIso->at(kHLTTau)==1){
	    //if (hltTauBDT->at(kHLTTau)>-0.9){
	    double dz = TMath::Abs(hltTauZ->at(iHLTTau) - hltTauZ->at(kHLTTau));
	    if(dz<dzMax){
	      //if(dz<dzMax || (hltTauPt->at(iHLTTau)>75 && hltTauPt->at(kHLTTau)>75)){
	      hist_Double_hltTauPt_Medium->Fill(hltTauPt->at(iHLTTau), hltTauPt->at(kHLTTau));
	      dzPass_Medium=true;
	      break;
	    }
	  }
	}
      }

      if (hltTauLooseRelIso->at(iHLTTau)==1 && !dzPass_Loose){
	//if (hltTauBDT->at(iHLTTau)>-0.925 && !dzPass_Loose){
	for(UInt_t kHLTTau = iHLTTau+1 ; kHLTTau < hltTauPt->size() ; ++kHLTTau){
	  if(fabs(hltTauEta->at(kHLTTau))>tau_eta_max) continue;
	  if(fabs(hltTauEta->at(kHLTTau))<tau_eta_min) continue;
	  if (hltTauPt->at(kHLTTau) <= tau_Pt_min) continue;
          if (hltTauLeadTrackPt->at(kHLTTau) <= tauLeadTrack_Pt_min) continue;
	  
	  if (hltTauLooseRelIso->at(kHLTTau)==1){
	    //if (hltTauBDT->at(kHLTTau)>-0.925){
	    double dz = TMath::Abs(hltTauZ->at(iHLTTau) - hltTauZ->at(kHLTTau));
	    if(dz<dzMax){
	      //if(dz<dzMax || (hltTauPt->at(iHLTTau)>75 && hltTauPt->at(kHLTTau)>75)){
	      hist_Double_hltTauPt_Loose->Fill(hltTauPt->at(iHLTTau), hltTauPt->at(kHLTTau));
	      dzPass_Loose=true;
	      break;
	    }
	  }
	}
      }
      
      if (hltTauVLooseRelIso->at(iHLTTau)==1 && !dzPass_VLoose){
      //if (hltTauBDT->at(iHLTTau)>-0.95 && !dzPass_VLoose){
	for(UInt_t kHLTTau = iHLTTau+1 ; kHLTTau < hltTauPt->size() ; ++kHLTTau){
	  if(fabs(hltTauEta->at(kHLTTau))>tau_eta_max) continue;
	  if(fabs(hltTauEta->at(kHLTTau))<tau_eta_min) continue;
	  if (hltTauPt->at(kHLTTau) <= tau_Pt_min) continue;
          if (hltTauLeadTrackPt->at(kHLTTau) <= tauLeadTrack_Pt_min) continue;
	  
	  if (hltTauVLooseRelIso->at(kHLTTau)==1){
	    //if (hltTauBDT->at(kHLTTau)>-0.95){
	    double dz = TMath::Abs(hltTauZ->at(iHLTTau) - hltTauZ->at(kHLTTau));
	    if(dz<dzMax){
	    //if(dz<dzMax || (hltTauPt->at(iHLTTau)>75 && hltTauPt->at(kHLTTau)>75)){
	      hist_Double_hltTauPt_VLoose->Fill(hltTauPt->at(iHLTTau), hltTauPt->at(kHLTTau));
	      dzPass_VLoose=true;
	      break;
	    }
	  }
	}
      }

      if (hltTauTightRelIso->at(iHLTTau)==1 && !dzPass_Tight_Pt40 && hltTauPt->at(iHLTTau) > 40){
	for(UInt_t kHLTTau = iHLTTau+1 ; kHLTTau < hltTauPt->size() ; ++kHLTTau){
	  if(fabs(hltTauEta->at(kHLTTau))>tau_eta_max) continue;
          if(fabs(hltTauEta->at(kHLTTau))<tau_eta_min) continue;
          if (hltTauPt->at(kHLTTau) <= tau_Pt_min) continue;
          if (hltTauLeadTrackPt->at(kHLTTau) <= tauLeadTrack_Pt_min) continue;
	  if (hltTauTightRelIso->at(kHLTTau)==1){
	    double dz = TMath::Abs(hltTauZ->at(iHLTTau) - hltTauZ->at(kHLTTau));
	    if (dz<dzMax && hltTauPt->at(kHLTTau) > 40){
	      cout <<"EventNumber "<<EventNumber<<" RunNumber "<<RunNumber<<" lumi "<<lumi<<endl;

              fileOut_txt << RunNumber<<":"<<lumi<<":"<<EventNumber<<endl;

	      treeOut->Fill();
	      dzPass_Tight_Pt40=true;
	      break;
	    }
	  }
	}
      }
      
    } //for(UInt_t iHLTTau = 0 ; iHLTTau < hltTauPt->size() ; ++iHLTTau){
    
      // End For Di Tau 
    
    
  } // for(UInt_t i = 0 ; i < treeIn->GetEntries() ; ++i)
  
  cout<<"Denominator = "<<Denominator<<endl;








  for(UInt_t i_PtBin = 1 ; i_PtBin <= 251 ; ++i_PtBin){
    hist_Rate_Single_hltTauPt_NoCut->SetBinContent(i_PtBin+1, hist_Single_hltTauPt_NoCut->Integral(i_PtBin+1,251)/Denominator*freq);
    hist_Rate_Single_hltTauPt_dZ->SetBinContent(i_PtBin+1, hist_Single_hltTauPt_dZ->Integral(i_PtBin+1,251)/Denominator*freq);
    hist_Rate_Single_hltTauPt_VLoose->SetBinContent(i_PtBin+1, hist_Single_hltTauPt_VLoose->Integral(i_PtBin+1,251)/Denominator*freq);
    hist_Rate_Single_hltTauPt_Loose->SetBinContent(i_PtBin+1, hist_Single_hltTauPt_Loose->Integral(i_PtBin+1,251)/Denominator*freq);
    hist_Rate_Single_hltTauPt_Medium->SetBinContent(i_PtBin+1, hist_Single_hltTauPt_Medium->Integral(i_PtBin+1,251)/Denominator*freq);
    hist_Rate_Single_hltTauPt_Tight->SetBinContent(i_PtBin+1, hist_Single_hltTauPt_Tight->Integral(i_PtBin+1,251)/Denominator*freq);
    
    if(firstTrue_SingleTau_NoCut && hist_Rate_Single_hltTauPt_NoCut->GetBinContent(i_PtBin+1) <= targetRate_singleTau){
      cout << "SingleTau NoCut " << hist_Rate_Single_hltTauPt_NoCut->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "SingleTau NoCut " << hist_Rate_Single_hltTauPt_NoCut->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      firstTrue_SingleTau_NoCut = false;
    }
    if(firstTrue_SingleTau_dZ && hist_Rate_Single_hltTauPt_dZ->GetBinContent(i_PtBin+1) <= targetRate_singleTau){
      cout << "SingleTau dZ " << hist_Rate_Single_hltTauPt_dZ->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "SingleTau dZ " << hist_Rate_Single_hltTauPt_dZ->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      firstTrue_SingleTau_dZ = false;
    }
    if(firstTrue_SingleTau_VLoose && hist_Rate_Single_hltTauPt_VLoose->GetBinContent(i_PtBin+1) <= targetRate_singleTau){
      cout << "SingleTau VLoose " << hist_Rate_Single_hltTauPt_VLoose->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "SingleTau VLoose " << hist_Rate_Single_hltTauPt_VLoose->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      firstTrue_SingleTau_VLoose = false;
    }
    if(firstTrue_SingleTau_Loose && hist_Rate_Single_hltTauPt_Loose->GetBinContent(i_PtBin+1) <= targetRate_singleTau){
      cout << "SingleTau Loose " << hist_Rate_Single_hltTauPt_Loose->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "SingleTau Loose " << hist_Rate_Single_hltTauPt_Loose->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      firstTrue_SingleTau_Loose = false;
    }
    if(firstTrue_SingleTau_Medium && hist_Rate_Single_hltTauPt_Medium->GetBinContent(i_PtBin+1) <= targetRate_singleTau){
      cout << "SingleTau Medium " << hist_Rate_Single_hltTauPt_Medium->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "SingleTau Medium " << hist_Rate_Single_hltTauPt_Medium->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      firstTrue_SingleTau_Medium = false;
    }
    if(firstTrue_SingleTau_Tight && hist_Rate_Single_hltTauPt_Tight->GetBinContent(i_PtBin+1) <= targetRate_singleTau){
      cout << "SingleTau Tight " << hist_Rate_Single_hltTauPt_Tight->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "SingleTau Tight " << hist_Rate_Single_hltTauPt_Tight->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      firstTrue_SingleTau_Tight = false;
    }
    
    hist_Rate_Double_hltTauPt_NoCut->SetBinContent(i_PtBin+1, hist_Double_hltTauPt_NoCut->Integral(i_PtBin+1,251,i_PtBin+1,251)/Denominator*freq);
    hist_Rate_Double_hltTauPt_dZ->SetBinContent(i_PtBin+1, hist_Double_hltTauPt_dZ->Integral(i_PtBin+1,251,i_PtBin+1,251)/Denominator*freq);
    hist_Rate_Double_hltTauPt_VLoose->SetBinContent(i_PtBin+1, hist_Double_hltTauPt_VLoose->Integral(i_PtBin+1,251,i_PtBin+1,251)/Denominator*freq);
    hist_Rate_Double_hltTauPt_Loose->SetBinContent(i_PtBin+1, hist_Double_hltTauPt_Loose->Integral(i_PtBin+1,251,i_PtBin+1,251)/Denominator*freq);
    hist_Rate_Double_hltTauPt_Medium->SetBinContent(i_PtBin+1, hist_Double_hltTauPt_Medium->Integral(i_PtBin+1,251,i_PtBin+1,251)/Denominator*freq);
    hist_Rate_Double_hltTauPt_Tight->SetBinContent(i_PtBin+1, hist_Double_hltTauPt_Tight->Integral(i_PtBin+1,251,i_PtBin+1,251)/Denominator*freq);

    if(firstTrue_DoubleTau_NoCut && hist_Rate_Double_hltTauPt_NoCut->GetBinContent(i_PtBin+1) <= targetRate_DoubleoTau){
      cout << "DoubleTau NoCut " << hist_Rate_Double_hltTauPt_NoCut->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "DoubleTau NoCut " << hist_Rate_Double_hltTauPt_NoCut->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      firstTrue_DoubleTau_NoCut = false;
    }
    if(firstTrue_DoubleTau_dZ && hist_Rate_Double_hltTauPt_dZ->GetBinContent(i_PtBin+1) <= targetRate_DoubleoTau){
      cout << "DoubleTau dZ " << hist_Rate_Double_hltTauPt_dZ->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "DoubleTau dZ " << hist_Rate_Double_hltTauPt_dZ->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      firstTrue_DoubleTau_dZ = false;
    }
    if(firstTrue_DoubleTau_VLoose && hist_Rate_Double_hltTauPt_VLoose->GetBinContent(i_PtBin+1) <= targetRate_DoubleoTau){
      cout << "DoubleTau VLoose " << hist_Rate_Double_hltTauPt_VLoose->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "DoubleTau VLoose " << hist_Rate_Double_hltTauPt_VLoose->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      firstTrue_DoubleTau_VLoose = false;
    }
    if(firstTrue_DoubleTau_Loose && hist_Rate_Double_hltTauPt_Loose->GetBinContent(i_PtBin+1) <= targetRate_DoubleoTau){
      cout << "DoubleTau Loose " << hist_Rate_Double_hltTauPt_Loose->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "DoubleTau Loose " << hist_Rate_Double_hltTauPt_Loose->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      firstTrue_DoubleTau_Loose = false;
    }
    if(firstTrue_DoubleTau_Medium && hist_Rate_Double_hltTauPt_Medium->GetBinContent(i_PtBin+1) <= targetRate_DoubleoTau){
      cout << "DoubleTau Medium " << hist_Rate_Double_hltTauPt_Medium->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "DoubleTau Medium " << hist_Rate_Double_hltTauPt_Medium->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      firstTrue_DoubleTau_Medium = false;
    }
    if(firstTrue_DoubleTau_Tight && hist_Rate_Double_hltTauPt_Tight->GetBinContent(i_PtBin+1) <= targetRate_DoubleoTau){
      cout << "DoubleTau Tight " << hist_Rate_Double_hltTauPt_Tight->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      fileOut_txt << "DoubleTau Tight " << hist_Rate_Double_hltTauPt_Tight->GetBinContent(i_PtBin+1) << " kHz " << i_PtBin << " GeV " << endl;
      firstTrue_DoubleTau_Tight = false;
    }
  }


  hist_Single_hltTauPt_NoCut->Write();
  hist_Single_hltTauPt_dZ->Write();
  hist_Single_hltTauPt_Tight->Write();
  hist_Single_hltTauPt_Medium->Write();
  hist_Single_hltTauPt_Loose->Write();
  hist_Single_hltTauPt_VLoose->Write();

  hist_Rate_Single_hltTauPt_NoCut->Write();
  hist_Rate_Single_hltTauPt_dZ->Write();
  hist_Rate_Single_hltTauPt_Tight->Write();
  hist_Rate_Single_hltTauPt_Medium->Write();
  hist_Rate_Single_hltTauPt_Loose->Write();
  hist_Rate_Single_hltTauPt_VLoose->Write();

  hist_Double_hltTauPt_NoCut->Write();
  hist_Double_hltTauPt_dZ->Write();
  hist_Double_hltTauPt_Tight->Write();
  hist_Double_hltTauPt_Medium->Write();
  hist_Double_hltTauPt_Loose->Write();
  hist_Double_hltTauPt_VLoose->Write();

  hist_Rate_Double_hltTauPt_NoCut->Write();
  hist_Rate_Double_hltTauPt_dZ->Write();
  hist_Rate_Double_hltTauPt_Tight->Write();
  hist_Rate_Double_hltTauPt_Medium->Write();
  hist_Rate_Double_hltTauPt_Loose->Write();
  hist_Rate_Double_hltTauPt_VLoose->Write();

  fileOut.Write();


  return;
}
