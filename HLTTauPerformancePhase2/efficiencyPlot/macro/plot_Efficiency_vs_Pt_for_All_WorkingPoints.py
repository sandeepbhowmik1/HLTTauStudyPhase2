import ROOT
import Efficiency_plot_macro as EfficiencyPlot
import sys

fileName_In = sys.argv[1]
fileName_Out = sys.argv[2]

#fileName_In = "/home/sbhowmik/Phase2/Tallinn/CMSSW_10_5_0_pre1/src/L1TauAnalyzer/HLTTauAnalyzer/script/efficiencyPlot/results/fitOutput_HLTTau_NTuple_VBFHToTauTau.root"
#fileName_Out = "/home/sbhowmik/Phase2/Tallinn/CMSSW_10_5_0_pre1/src/L1TauAnalyzer/HLTTauAnalyzer/script/efficiencyPlot/plots/plot_compare_Efficiency_HLTTau_vs_HLTTau_Pt"

fileIn_HLTTau = ROOT.TFile.Open(fileName_In)

hist_HLTTau = []
fit_HLTTau = []
efficiency_HLTTau = []
plots = []
workingPointNames=["hltTauPtNoCut", "hltTauPt25", "hltTauPt30", "hltTauPt35", "hltTauPt40", "hltTauPt45"]

workingPoints = ["No cut (No p_{T} Threshold )", "HLT #tau p_{T} > 25 Gev", "HLT #tau p_{T} > 30 Gev", "HLT #tau p_{T} > 35 Gev", "HLT #tau p_{T} > 40 Gev", "HLT #tau p_{T} > 45 Gev"]

#plotRanges=[500, 1000]
plotRanges=[100, 500]

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
    plots[-1].xposText =0.60
    plots[-1].yposText =0.26
    plots[-1].extraText1 = "#tau_{h} Trigger"
    plots[-1].extraText2 = "HLT"
    plots[-1].extraText3 = "|#eta| < 2.4"
    plots[-1].extraText4 = "Rate 12 kHz"
    plots[-1].extraText4 = ""
    plots[-1].extraText5 = ""
    plots[-1].name = fileName_Out + "_" + str(plotRanges[k])
    plots[-1].xRange = (0, plotRanges[k]+1)
    plots[-1].xTitle = "gen #tau_{h} p_{T} (GeV)"
    #plots[-1].xTitle = "Offline #tau_{h} p_{T} [GeV]"
    plots[-1].legendPosition = (0.12, 0.725, 0.85, 0.898)
    #plots[-1].legendPosition = (0.34, 0.15, 0.85, 0.3)

canvas = []
for plot in plots:
    canvas.append(plot.plot())

fileIn_HLTTau.Close()


