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

// double CB symmetric (two-sided tails)
double CrystalBall
(double* x, double* par){ 
  //http://en.wikipedia.org/wiki/Crystal_Ball_function 
  double xcur = x[0]; 
  double alpha = par[0]; 
  double n = par[1]; 
  double mu = par[2]; 
  double sigma = par[3]; 
  double N = par[4]; 
  TF1* exp = new TF1("exp","exp(x)",1e-20,1e20); 
  double A; double B; 
  if (alpha < 0){ 
    A = pow((n/(-1*alpha)),n)*exp->Eval((-1)*alpha*alpha/2); 
    B = n/(-1*alpha) + alpha;} 
  else { 
    A = pow((n/alpha),n)*exp->Eval((-1)*alpha*alpha/2); 
    B = n/alpha - alpha;} 
    double f; 
  if (TMath::Abs((xcur-mu)/sigma) < TMath::Abs(alpha) ) 
    f = N*exp->Eval((-1)*(xcur-mu)*(xcur-mu)/(2*sigma*sigma)); 
  else if (((xcur-mu)/sigma) < (-1.)*alpha )
    f = N*A*pow((B- (xcur-mu)/sigma),(-1*n)); // left tail
  else
    f = N*A*pow( (B- (mu-xcur)/sigma),(-1*n)); // right tail
  delete exp; 
  return f; 
} 

// double CB asymmetric
double DoubleCrystalBall
(double* x, double* par){ 
  //http://en.wikipedia.org/wiki/Crystal_Ball_function 
  double xcur = x[0]; 
  double alphaL = par[0]; 
  double nL = par[1]; 
  double alphaR = par[2]; 
  double nR = par[3]; 

  double mu = par[4]; 
  double sigma = par[5]; 
  double N = par[6]; 
 
  TF1* exp = new TF1("exp","exp(x)",1e-20,1e20); 
  double AL; double BL; double AR; double BR; 
 
  if (alphaL < 0){ 
    AL = pow((nL/(-1*alphaL)),nL)*exp->Eval((-1)*alphaL*alphaL/2); 
    BL = nL/(-1*alphaL) + alphaL;} 
  else { 
    AL = pow((nL/alphaL),nL)*exp->Eval((-1)*alphaL*alphaL/2); 
    BL = nL/alphaL - alphaL;} 

  if (alphaR < 0){ 
    AR = pow((nR/(-1*alphaR)),nR)*exp->Eval((-1)*alphaR*alphaR/2); 
    BR = nR/(-1*alphaR) + alphaR;} 
  else { 
    AR = pow((nR/alphaR),nR)*exp->Eval((-1)*alphaR*alphaR/2); 
    BR = nR/alphaR - alphaR;} 
   

    double f; 
  if ( ((xcur-mu)/sigma) > (-1.)*alphaL  && ((xcur-mu)/sigma) < (1.)*alphaR) 
    f = N*exp->Eval((-1)*(xcur-mu)*(xcur-mu)/(2*sigma*sigma)); 
  
  // left
  else if ( ((xcur-mu)/sigma) <= (-1.)*alphaL )
    f = N*AL*pow((BL- (xcur-mu)/sigma),(-1*nL)); // left tail
  //right
  else
    f = N*AR*pow( (BR- (mu-xcur)/sigma),(-1*nR)); // right tail
  delete exp; 
  return f; 
} 

/*
  void fit_Resolution()
  {
  TString fileName_In = "/home/sbhowmik/Phase2/Tallinn/CMSSW_10_5_0_pre1/src/L1TauAnalyzer/L1PFTauAnalyzer/script/resolutionPlot/results/plotOutput_resolution_TallinnL1PFTau_VBFHToTauTau20190505.root";
  TString fileName_Out = "/home/sbhowmik/Phase2/Tallinn/CMSSW_10_5_0_pre1/src/L1TauAnalyzer/L1PFTauAnalyzer/script/resolutionPlot/results/fitted_plotOutput_resolution_TallinnL1PFTau_VBFHToTauTau20190505.root";
*/

void fit_Resolution(TString fileName_In, TString fileName_Out)
{

  TFile* fileIn = new TFile(fileName_In);
  TFile* fileOut = new TFile(fileName_Out, "RECREATE");

  vector<TString> hist_Name_Et_Resolution {"hist_Et_Resolution_for_hltTauPtNoCut", "hist_Et_Resolution_for_hltTauPt25", "hist_Et_Resolution_for_hltTauPt30", "hist_Et_Resolution_for_hltTauPt35", "hist_Et_Resolution_for_hltTauPt40", "hist_Et_Resolution_for_hltTauPt45"};

  vector<TString> hist_Name_Eta_Resolution {"hist_Eta_Resolution_for_hltTauPtNoCut", "hist_Eta_Resolution_for_hltTauPt25", "hist_Eta_Resolution_for_hltTauPt30", "hist_Eta_Resolution_for_hltTauPt35", "hist_Eta_Resolution_for_hltTauPt40", "hist_Eta_Resolution_for_hltTauPt45"};

  vector<TString> hist_Name_Phi_Resolution {"hist_Phi_Resolution_for_hltTauPtNoCut", "hist_Phi_Resolution_for_hltTauPt25", "hist_Phi_Resolution_for_hltTauPt30", "hist_Phi_Resolution_for_hltTauPt35", "hist_Phi_Resolution_for_hltTauPt40", "hist_Phi_Resolution_for_hltTauPt45"};

  TH1::SetDefaultSumw2();

  TF1* CBFuncAsymm = new TF1("CBFuncAsymm",&DoubleCrystalBall,0.,3.,7);
  for (TString name : hist_Name_Et_Resolution)
    {
      cout << "... fitting: " << name << endl;
      TH1F* hist_resolution = (TH1F*) fileIn->Get(name);
      hist_resolution->Scale(1./hist_resolution->Integral());
      CBFuncAsymm->SetParameters(0.9, 4.3, 1.3, 4.3, hist_resolution->GetMean(), hist_resolution->GetRMS(), 1.);
      hist_resolution->Fit("CBFuncAsymm");
      fileOut->cd();
      hist_resolution->Write();
    }


  TF1* CBFunc = new TF1("CBFunc",&CrystalBall,-0.3,0.3,5);
  for (TString name : hist_Name_Eta_Resolution)
    {
      cout << "... fitting: " << name << endl;
      TH1F* hist_resolution = (TH1F*) fileIn->Get(name);
      hist_resolution->Scale(1./hist_resolution->Integral());
      CBFunc->SetParameters(3, 1, 0, 0.05, 0.06);
      hist_resolution->Fit("CBFunc");
      fileOut->cd();
      hist_resolution->Write();
    }

  for (TString name : hist_Name_Phi_Resolution)
    {
      cout << "... fitting: " << name << endl;
      TH1F* hist_resolution = (TH1F*) fileIn->Get(name);
      hist_resolution->Scale(1./hist_resolution->Integral());
      CBFunc->SetParameters(3, 1, 0, 0.05, 0.06);
      hist_resolution->Fit("CBFunc");
      fileOut->cd();
      hist_resolution->Write();
    }


  fileOut->Close();
}

