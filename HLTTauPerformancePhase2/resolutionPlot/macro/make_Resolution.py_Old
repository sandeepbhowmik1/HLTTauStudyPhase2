from ROOT import *
import numpy as n
import math
import sys
TH1.SetDefaultSumw2();

fileName_In = sys.argv[1]
fileName_Out = sys.argv[2]

fileIn = TFile.Open(fileName_In)
treeIn = fileIn.Get("HLTTauAnalyzer")
fileOut = TFile (fileName_Out, 'recreate')

#fileName_In = "/home/sbhowmik/NTuple_Phase2/HLTTau/NTuple_test_HLTTauAnalyzer_VBFHToTauTau_20190502_Resolution.root"
#fileName_Out = "/home/sbhowmik/Phase2/Tallinn/CMSSW_10_5_0_pre1/src/L1TauAnalyzer/HLTTauAnalyzer/script/resolutionPlot/results/plotOutput_HLTTau_NTuple_VBFHToTauTau_20190502.root"

workingPointNames=["hltTauPtNoCut", "hltTauPt25", "hltTauPt30", "hltTauPt35", "hltTauPt40", "hltTauPt45"]

hist_Et_Resolution_for_hltTauPtNoCut = TH1F ("hist_Et_Resolution_for_hltTauPtNoCut", "hist_Et_Resolution_for_hltTauPtNoCut", 60, 0, 3)
hist_Et_Resolution_for_hltTauPt25 = TH1F ("hist_Et_Resolution_for_hltTauPt25", "hist_Et_Resolution_for_hltTauPt25", 60, 0, 3)
hist_Et_Resolution_for_hltTauPt30 = TH1F ("hist_Et_Resolution_for_hltTauPt30", "hist_Et_Resolution_for_hltTauPt30", 60, 0, 3)
hist_Et_Resolution_for_hltTauPt35 = TH1F ("hist_Et_Resolution_for_hltTauPt35", "hist_Et_Resolution_for_hltTauPt35", 60, 0, 3)
hist_Et_Resolution_for_hltTauPt40 = TH1F ("hist_Et_Resolution_for_hltTauPt40", "hist_Et_Resolution_for_hltTauPt40", 60, 0, 3)
hist_Et_Resolution_for_hltTauPt45 = TH1F ("hist_Et_Resolution_for_hltTauPt45", "hist_Et_Resolution_for_hltTauPt45", 60, 0, 3)

hist_Eta_Resolution_for_hltTauPtNoCut = TH1F ("hist_Eta_Resolution_for_hltTauPtNoCut", "hist_Eta_Resolution_for_hltTauPtNoCut", 50, -0.3, 0.3)
hist_Eta_Resolution_for_hltTauPt25 = TH1F ("hist_Eta_Resolution_for_hltTauPt25", "hist_Eta_Resolution_for_hltTauPt25", 50, -0.3, 0.3)
hist_Eta_Resolution_for_hltTauPt30 = TH1F ("hist_Eta_Resolution_for_hltTauPt30", "hist_Eta_Resolution_for_hltTauPt30", 50, -0.3, 0.3)
hist_Eta_Resolution_for_hltTauPt35 = TH1F ("hist_Eta_Resolution_for_hltTauPt35", "hist_Eta_Resolution_for_hltTauPt35", 50, -0.3, 0.3)
hist_Eta_Resolution_for_hltTauPt40 = TH1F ("hist_Eta_Resolution_for_hltTauPt40", "hist_Eta_Resolution_for_hltTauPt40", 50, -0.3, 0.3)
hist_Eta_Resolution_for_hltTauPt45 = TH1F ("hist_Eta_Resolution_for_hltTauPt45", "hist_Eta_Resolution_for_hltTauPt45", 50, -0.3, 0.3)

hist_Phi_Resolution_for_hltTauPtNoCut = TH1F ("hist_Phi_Resolution_for_hltTauPtNoCut", "hist_Phi_Resolution_for_hltTauPtNoCut", 50, -0.3, 0.3)
hist_Phi_Resolution_for_hltTauPt25 = TH1F ("hist_Phi_Resolution_for_hltTauPt25", "hist_Phi_Resolution_for_hltTauPt25", 50, -0.3, 0.3)
hist_Phi_Resolution_for_hltTauPt30 = TH1F ("hist_Phi_Resolution_for_hltTauPt30", "hist_Phi_Resolution_for_hltTauPt30", 50, -0.3, 0.3)
hist_Phi_Resolution_for_hltTauPt35 = TH1F ("hist_Phi_Resolution_for_hltTauPt35", "hist_Phi_Resolution_for_hltTauPt35", 50, -0.3, 0.3)
hist_Phi_Resolution_for_hltTauPt40 = TH1F ("hist_Phi_Resolution_for_hltTauPt40", "hist_Phi_Resolution_for_hltTauPt40", 50, -0.3, 0.3)
hist_Phi_Resolution_for_hltTauPt45 = TH1F ("hist_Phi_Resolution_for_hltTauPt45", "hist_Phi_Resolution_for_hltTauPt45", 50, -0.3, 0.3)

for i in range (0, len(workingPointNames)):
    hist_Name_Et_Resolution = "hist_Et_Resolution_for_%s" % workingPointNames[i]
    hist_Name_Eta_Resolution = "hist_Eta_Resolution_for_%s" % workingPointNames[i]
    hist_Name_Phi_Resolution = "hist_Phi_Resolution_for_%s" % workingPointNames[i]
 
    cut = "%s" % workingPointNames[i]

    treeIn.Draw("hltTauPt / tauPt >> %s" % hist_Name_Et_Resolution, "%s==1" % cut)
    treeIn.Draw("hltTauEta - tauEta >> %s" % hist_Name_Eta_Resolution, "%s==1" % cut)
    treeIn.Draw("hltTauPhi - tauPhi >> %s" % hist_Name_Phi_Resolution, "%s==1" % cut)

fileOut.Write()
fileOut.Close()
