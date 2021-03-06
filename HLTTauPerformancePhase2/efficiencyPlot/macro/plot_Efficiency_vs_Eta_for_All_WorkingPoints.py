import ROOT
import Efficiency_plot_macro as EfficiencyPlot
import sys

fileName_In = sys.argv[1]
fileName_In_txt = sys.argv[2]
fileName_Out = sys.argv[3]

#fileName_In = "/home/sbhowmik/Phase2/Tallinn/CMSSW_10_5_0_pre1/src/HLTauAnalyzer/HLTTauAnalyzer/script/efficiencyPlot/results/fitOutput_HLTTau_NTuple_VBFHToTauTau.root"
#fileName_In = "/home/sbhowmik/Phase2/Tallinn/CMSSW_10_5_0_pre1/src/HLTauAnalyzer/HLTTauAnalyzer/script/efficiencyPlot/results/fitOutput_HLTTau_NTuple_VBFHToTauTau.root"
#fileName_Out = "/home/sbhowmik/Phase2/Tallinn/CMSSW_10_5_0_pre1/src/HLTauAnalyzer/HLTTauAnalyzer/script/efficiencyPlot/plots/plot_compare_Efficiency_HLTTau_vs_HLTTau_Pt"

with open(fileName_In_txt,'r') as f:
    for line in f:
        words = line.split()
        if words[0]=='DoubleTau' and words[1]=='NoCut' :
            pt_Threshold_NoCut = words[4]
        if words[0]=='DoubleTau' and words[1]=='dZ' :
            pt_Threshold_dZ = words[4]
        if words[0]=='DoubleTau' and words[1]=='VLoose' :
            pt_Threshold_VLoose = words[4]
        if words[0]=='DoubleTau' and words[1]=='Loose' :
            pt_Threshold_Loose = words[4]
        if words[0]=='DoubleTau' and words[1]=='Medium' :
            pt_Threshold_Medium = words[4]
        if words[0]=='DoubleTau' and words[1]=='Tight' :
            pt_Threshold_Tight = words[4]


fileIn_HLTTau = ROOT.TFile.Open(fileName_In)

hist_HLTTau = []
fit_HLTTau = []
efficiency_HLTTau = []
plots = []

workingPointNames=["hltTauNoCut","hltTaudZ", "hltTauVLoose", "hltTauLoose", "hltTauMedium", "hltTauTight"]
#workingPointNames=["hltLoose", "hltMedium", "hltTight"]
workingPoints = ["No cut (No p_{T} Threshold )", "dz cut (p_{T} Threshold = %s GeV)" % pt_Threshold_dZ, "dz cut + Very Loose (p_{T} Threshold = %s GeV)" % pt_Threshold_VLoose, "dz cut + Loose (p_{T} Threshold = %s GeV)" % pt_Threshold_Loose, "dz cut + Medium (p_{T} Threshold = %s GeV)" % pt_Threshold_Medium, "dz cut + Tight (p_{T} Threshold = %s GeV)" % pt_Threshold_Tight]
#workingPoints = ["Loose (p_{T} Threshold=%sGeV)" % hltTauPt_Threshold[2], "Medium (p_{T} Threshold=%sGeV)" % hltTauPt_Threshold[1], "Tight (p_{T} Threshold=%sGeV)" % hltTauPt_Threshold[0]]
#workingPoints = ["#tau p_{T} > 5 Gev and #mu p_{T} > %s GeV" % hltTauPt_Threshold[5], "#tau p_{T} > 10 Gev and #mu p_{T} > %s GeV" % hltTauPt_Threshold[4], "#tau p_{T} > 15 Gev and #mu p_{T} > %s GeV" % hltTauPt_Threshold[3], "#tau p_{T} > 20 Gev and #mu p_{T} > %s GeV" % hltTauPt_Threshold[2], "#tau p_{T} > 25 Gev and #mu p_{T} > %s GeV" % hltTauPt_Threshold[1], "#tau p_{T} > 30 Gev and #mu p_{T} > %s GeV" % hltTauPt_Threshold[0]]

plotRangeNames=["2p4"]
plotRanges=[2.4]
#plotRangeNames=["1p4"]
#plotRanges=[1.4]

for k in range (0, len(plotRanges)):
    count=0
    plots.append(EfficiencyPlot.EfficiencyPlot())
    for i in range (0, len(workingPointNames)):
        count+=1
        if(count==5):
            count+=1
        hist_HLTTau.append(fileIn_HLTTau.Get("histo_Phase2_HLTTau_"+workingPointNames[i]))
        hist_HLTTau[-1].__class__ = ROOT.RooHist
        fit_HLTTau.append(fileIn_HLTTau.Get("fit_Phase2_HLTTau_"+workingPointNames[i]))
        fit_HLTTau[-1].__class__ = ROOT.RooCurve
        efficiency_HLTTau.append(EfficiencyPlot.Efficiency(Name="HLTTau", Histo=hist_HLTTau[-1], Fit=fit_HLTTau[-1],
                                                               MarkerColor=(count), MarkerStyle=20, LineColor=(count),LineStyle=1,
                                                               Legend=workingPoints[i]))

        plots[-1].addEfficiency(efficiency_HLTTau[-1])
    plots[-1].xposText =0.65
    plots[-1].yposText =0.3
    #plots[-1].xposText =0.60
    #plots[-1].yposText =0.550
    plots[-1].extraText1 = "#tau_{h}#tau_{h} Trigger"
    plots[-1].extraText2 = "HLT"
    plots[-1].extraText3 = "gen #tau_{h} p_{T} > 20"
    plots[-1].extraText4 = "Rate 12 kHz"
    plots[-1].extraText5 = ""
    plots[-1].name = fileName_Out + "_" + plotRangeNames[k]
    plots[-1].xRange = (-plotRanges[k], plotRanges[k])
    plots[-1].xTitle = "gen #tau_{h} #eta"
    #plots[-1].xTitle = "Offline #tau_{h} p_{T} [GeV]"
    plots[-1].legendPosition = (0.12, 0.725, 0.85, 0.898)
    #plots[-1].legendPosition = (0.34, 0.15, 0.85, 0.3)

canvas = []
for plot in plots:
    canvas.append(plot.plot())

fileIn_HLTTau.Close()


