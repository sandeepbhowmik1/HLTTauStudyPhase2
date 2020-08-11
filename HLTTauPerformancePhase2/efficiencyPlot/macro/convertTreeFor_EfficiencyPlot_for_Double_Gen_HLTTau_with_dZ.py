from ROOT import *
import numpy as n
import math
import sys

fileName_In = sys.argv[1]
treeName_In = sys.argv[2]
fileName_In_txt = sys.argv[3] 
fileName_Out = sys.argv[4]

#fileName_In = "/home/sbhowmik/NTuple_Phase2/HLTTau/NTuple_test_HLTTauAnalyzer_VBFHToTauTau_20190610_5.root"
#treeName_In = "HLTTauAnalyzer/HLTTauAnalyzer"
#fileName_In_txt = "/home/sbhowmik/Phase2/Test/CMSSW_10_5_0_pre1/src/HLTTAUauAnalyzer/HLTTauAnalyzer/script/ratePlot/results/hist_rate_HLTTau_NeutrinoGun_20190605_3.txt"
#fileName_Out = "/home/sbhowmik/NTuple_Phase2/HLTTau/NTuple_test_HLTTauAnalyzer_VBFHToTauTau_forEfficiency_20190610_5.root"

with open(fileName_In_txt,'r') as f:
    for line in f:
        words = line.split()
        if words[0]=='DoubleTau' and words[1]=='NoCut' :
            rate_Target_NoCut = words[2]
            pt_Threshold_NoCut = words[4]
        if words[0]=='DoubleTau' and words[1]=='dZ' :
            rate_Target_dZ = words[2]
            pt_Threshold_dZ = words[4]
        if words[0]=='DoubleTau' and words[1]=='VLoose' :
            rate_Target_VLoose = words[2]
            pt_Threshold_VLoose = words[4]
        if words[0]=='DoubleTau' and words[1]=='Loose' :
            rate_Target_Loose = words[2]
            pt_Threshold_Loose = words[4]
        if words[0]=='DoubleTau' and words[1]=='Medium' :
            rate_Target_Medium = words[2]
            pt_Threshold_Medium = words[4]
        if words[0]=='DoubleTau' and words[1]=='Tight' :
            rate_Target_Tight = words[2]
            pt_Threshold_Tight = words[4]

print "rate_Target_NoCut ", rate_Target_NoCut, "pt_Threshold_NoCut", pt_Threshold_NoCut
print "rate_Target_dZ ", rate_Target_dZ, "pt_Threshold_dZ", pt_Threshold_dZ
print "rate_Target_VLoose ", rate_Target_VLoose, "pt_Threshold_VLoose", pt_Threshold_VLoose
print "rate_Target_Loose ", rate_Target_Loose, "pt_Threshold_Loose", pt_Threshold_Loose
print "rate_Target_Medium ", rate_Target_Medium, "pt_Threshold_Medium", pt_Threshold_Medium
print "rate_Target_Tight ", rate_Target_Tight, "pt_Threshold_Tight", pt_Threshold_Tight


fileIn = TFile.Open(fileName_In)
treeIn = fileIn.Get(treeName_In)
fileOut = TFile (fileName_Out, 'recreate')
treeOut = TTree("HLTTauAnalyzer", "HLTTauAnalyzer")

bkgSubW = n.zeros(1, dtype=float)
tauPt = n.zeros(1, dtype=float)
tauEta = n.zeros(1, dtype=float)
tauPhi = n.zeros(1, dtype=float)
hltTauPt = n.zeros(1, dtype=float)
hltTauEta = n.zeros(1, dtype=float)
hltTauPhi = n.zeros(1, dtype=float)
hltTauNoCut = n.zeros(1, dtype=int)
hltTaudZ = n.zeros(1, dtype=int)
hltTauVLoose = n.zeros(1, dtype=int)
hltTauLoose = n.zeros(1, dtype=int)
hltTauMedium = n.zeros(1, dtype=int)
hltTauTight = n.zeros(1, dtype=int)
#Nvtx = n.zeros(1, dtype=float)

treeOut.Branch("bkgSubW", bkgSubW, "bkgSubW/D")
treeOut.Branch("tauPt", tauPt, "tauPt/D")
treeOut.Branch("tauEta", tauEta, "tauEta/D")
treeOut.Branch("tauPhi", tauPhi, "tauPhi/D")
treeOut.Branch("hltTauPt", hltTauPt, "hltTauPt/D")
treeOut.Branch("hltTauEta", hltTauEta, "hltTauEta/D")
treeOut.Branch("hltTauPhi", hltTauPhi, "hltTauPhi/D")
treeOut.Branch("hltTauNoCut", hltTauNoCut, "hltTauNoCut/I")
treeOut.Branch("hltTaudZ", hltTaudZ, "hltTaudZ/I")
treeOut.Branch("hltTauVLoose", hltTauVLoose, "hltTauVLoose/I")
treeOut.Branch("hltTauLoose", hltTauLoose, "hltTauLoose/I")
treeOut.Branch("hltTauMedium", hltTauMedium, "hltTauMedium/I")
treeOut.Branch("hltTauTight", hltTauTight, "hltTauTight/I")
#treeOut.Branch("Nvtx", Nvtx, "Nvtx/D")

etaMax = 2.4
#etaMax = 2.17
#etaMax = 1.4
etaMin = 0

def sort_PFTaus(old_PFTau_Pts):
    new_PFTau_Pts = []
    for i in range (0, len(old_PFTau_Pts)):
        i_hltTauPt = old_PFTau_Pts[i]
        temp_hltTauPt = 0
        for j in range (0, len(old_PFTau_Pts)):
            j_hltTauPt = old_PFTau_Pts[j]
            if j_hltTauPt > i_hltTauPt :
                temp_hltTauPt = j_hltTauPt
            else :
                temp_hltTauPt = i_hltTauPt
                new_PFTau_Pts.append(temp_hltTauPt)
    return new_PFTau_Pts

def Is_dZPass(hltTauau1Pt, hltTauau1_Z, hltTauau2Pt, hltTauau2_Z):
    dz = abs(hltTauau1_Z - hltTauau2_Z)
    #if dz < 0.40:
    if dz < 0.20:
    #if (dz < 1.0) or (hltTauau1Pt > 75.0 and hltTauau2Pt > 75.0):
        return True
    return False

nentries = treeIn.GetEntries()
print "nentries ", nentries

for ev in range (0, nentries):
    treeIn.GetEntry(ev)
    if (ev%10000 == 0) : print ev, "/", nentries
    bkgSubW[0] = 1. 
    
    gentauPt_ = []
    gentauEta_ = []
    gentauPhi_ = []
    #Nvtx_ = []
    Ngentau_ = 0
    
    # CV: read generator-level hadronic tau information from TTree
    for i in range(0, treeIn.genTauPt.size()):
        if abs(treeIn.genTauEta[i]) > double(etaMax):
            continue
        if abs(treeIn.genTauEta[i]) < double(etaMin):
            continue
        if abs(treeIn.genTauPt[i]) < 20.0:
            continue
        gentauPt_.append(treeIn.genTauPt[i])
        gentauEta_.append(treeIn.genTauEta[i])
        gentauPhi_.append(treeIn.genTauPhi[i])
        #Nvtx_.append(treeIn.l1VertexN)
        Ngentau_ = Ngentau_ + 1

    hltTauPt_ = []
    hltTauEta_ = []
    hltTauPhi_ = []
    hltTauNoCut_ = []
    hltTaudZ_ = []
    hltTauVLoose_ = []
    hltTauLoose_ = []
    hltTauMedium_ = []
    hltTauTight_ = []
    hltTauZ_ = []
    NhltTau_ = 0
    
    # CV: read HLTTau information from TTree
    for i in range(0, treeIn.hltTauPt.size()):
        if (treeIn.hltTauLeadTrackPt < 5.0):
            continue
        hltTauPt_.append(treeIn.hltTauPt[i])
        hltTauEta_.append(treeIn.hltTauEta[i])
        hltTauPhi_.append(treeIn.hltTauPhi[i]) 
        hltTauNoCut_.append(1)
        hltTaudZ_.append(1 if treeIn.hltTauPt[i] > (double)(pt_Threshold_dZ) else 0)
        hltTauVLoose_.append(1 if treeIn.hltTauVLooseRelIso[i] and treeIn.hltTauPt[i] > (double)(pt_Threshold_VLoose) else 0)
        hltTauLoose_.append(1 if treeIn.hltTauLooseRelIso[i] and treeIn.hltTauPt[i] > (double)(pt_Threshold_Loose) else 0)
        hltTauMedium_.append(1 if treeIn.hltTauMediumRelIso[i] and treeIn.hltTauPt[i] > (double)(pt_Threshold_Medium) else 0)
        hltTauTight_.append(1 if treeIn.hltTauTightRelIso[i] and treeIn.hltTauPt[i] > (double)(pt_Threshold_Tight) else 0)

        #hltTauVLoose_.append(1 if treeIn.hltTauBDT[i] > -0.95 and treeIn.hltTauPt[i] > (double)(pt_Threshold_VLoose) else 0)
        #hltTauLoose_.append(1 if treeIn.hltTauBDT[i] > -0.925 and treeIn.hltTauPt[i] > (double)(pt_Threshold_Loose) else 0)
        #hltTauMedium_.append(1 if treeIn.hltTauBDT[i] > -0.9 and treeIn.hltTauPt[i] > (double)(pt_Threshold_Medium) else 0)
        #hltTauTight_.append(1 if treeIn.hltTauBDT[i] > -0.7 and treeIn.hltTauPt[i] > (double)(pt_Threshold_Tight) else 0)

        hltTauZ_.append(treeIn.hltTauZ[i])
        NhltTau_ = NhltTau_ + 1

    gentau_to_hltTau_map = {} # key = index in gentau collection, value = index in hltTau collection

    for i in range(0, Ngentau_):

        minDeltaR = 0.5 # CV: maximum eta-phi distance for matching gentau to hltTau collection
        match = None
        for j in range(0, NhltTau_):
            DeltaR = math.sqrt((gentauEta_[i] - hltTauEta_[j])**2 + (gentauPhi_[i] - hltTauPhi_[j])**2)
            if DeltaR < minDeltaR:
                minDeltaR = DeltaR
                match = j

        gentau_to_hltTau_map[i] = match

    pt_Threshold_tag = 20.0
    hltTau_tag = hltTauLoose_ 

    if Ngentau_ == 2:
        for itag in range(0, Ngentau_): 
            jtag = gentau_to_hltTau_map[itag]
            if jtag is None:
	        continue 
            # CV: tag hltTau passes loose pT and isolation selection
            #     and is therefore a "good" hltTau for the purpose of building a hltTau pair
            if (hltTauPt_[jtag] > pt_Threshold_tag) and (hltTau_tag[jtag] == 1): 
                for iprobe in range(0, Ngentau_):
                    if itag == iprobe:
	                continue 

                    tauPt[0] = gentauPt_[iprobe]
                    tauEta[0] = gentauPhi_[iprobe]
                    tauPhi[0] = gentauPhi_[iprobe]
                    #Nvtx[0] = Nvtx_[iprobe]
                    hltTauPt[0] = 0
                    hltTauEta[0] = 0
                    hltTauPhi[0] = 0
                    hltTauNoCut[0] = 0
                    hltTaudZ[0] = 0
                    hltTauVLoose[0] = 0
                    hltTauLoose[0] = 0
                    hltTauMedium[0] = 0
                    hltTauTight[0] = 0

                    jprobe = gentau_to_hltTau_map[iprobe]
                    #if (jprobe is not None):
                    if (jprobe is not None) and (Is_dZPass(hltTauPt_[jtag], hltTauZ_[jtag], hltTauPt_[jprobe], hltTauZ_[jprobe])):
                        hltTauPt[0] = hltTauPt_[jprobe]
                        hltTauEta[0] = hltTauEta_[jprobe]
                        hltTauPhi[0] = hltTauPhi_[jprobe]
                        hltTauNoCut[0] = hltTauNoCut_[jprobe]
                        hltTaudZ[0] = hltTaudZ_[jprobe]
                        hltTauVLoose[0] = hltTauVLoose_[jprobe]
                        hltTauLoose[0] = hltTauLoose_[jprobe]
                        hltTauMedium[0] = hltTauMedium_[jprobe]
                        hltTauTight[0] = hltTauTight_[jprobe]
                        
                    treeOut.Fill()

treeOut.Write()
fileOut.Close()
