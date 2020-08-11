from ROOT import *
import ROOT
import operator
import array
ROOT.gSystem.Load('libRooFit')
import sys

fileName_In = sys.argv[1]
fileName_Out = sys.argv[2]

#fileName_In = '/home/sbhowmik/Phase2/Tallinn/CMSSW_10_5_0_pre1/src/L1TauAnalyzer/L1PFTauAnalyzer/script/ratePlot/results/hist_rate_L1HPSPFTau_NeutrinoGun_20190505.root'
#fileName_In_L1PFTau = '/home/sbhowmik/Phase2/Tallinn/CMSSW_10_5_0_pre1/src/L1TauAnalyzer/L1PFTauAnalyzer/script/ratePlot/results/hist_rate_L1PFTau_NeutrinoGun_20190505.root'
#fileName_Out = '/home/sbhowmik/Phase2/Tallinn/CMSSW_10_5_0_pre1/src/L1TauAnalyzer/L1PFTauAnalyzer/script/ratePlot/plots/plot_compare_Rate_L1PFTau_vs_L1HPSPFTau_20190505'

def SetLucaStyle ():
    LS = TStyle (gStyle) #copy some of the basics of defualt style...
    LS.SetName("LucaStyle")
    LS.SetTitle("Luca Style")
    # pad
    LS.SetOptStat(000000)
    #LS.SetTickLength(0.02,"X")
    #LS.SetTickLength(0.02,"Y")
    #LS.SetPadTickY(1)
    #LS.SetPadTickX(1)
    LS.SetPadGridY(1);
    LS.SetPadGridX(1);
    #LS.SetPadBottomMargin(0.13)
    LS.SetPadLeftMargin(0.11)
    LS.SetCanvasDefH(800)
    LS.SetCanvasDefW(800)
    # axis

    LS.cd() 
    return LS


#############################################

SetLucaStyle()

fileIn = TFile (fileName_In)

objTypes = ["Et", "Eta", "Phi"]
#workingPoints=["hltTauPtNoCut", "hltTauPt25", "hltTauPt30", "hltTauPt35", "hltTauPt40", "hltTauPt45"]
#workingPointNames = ["No cut (No p_{T} Threshold )", "HLT #tau p_{T} > 25 Gev", "HLT #tau p_{T} > 30 Gev", "HLT #tau p_{T} > 35 Gev", "HLT #tau p_{T} > 40 Gev", "HLT #tau p_{T} > 45 Gev"]
workingPoints = ["hltTauPtNoCut"]
workingPointNames = ["HLT #tau p_{T} > 20 Gev"]
workingPoints = ["NoCut", "dZ", "VLoose", "Loose", "Medium", "Tight"]
workingPointNames = ["No cut", "dz cut", "dz cut + Very Loose", "dz cut + Loose", "dz cut + Medium", "dz cut + Tight"]


titles = {
    "Et" : "; HLT #tau_{h} p_{T} / True #tau_{h} p_{T}; a.u.",
    "Eta" : "; HLT #tau_{h} #eta - True #tau_{h} #eta; a.u.",
    "Phi" : "; HLT #tau_{h} #varphi - True #tau_{h} #varphi; a.u.",
}

c1 = TCanvas ("c1", "c1", 800, 800)
#c1.SetLogy()
#c1.SetLogx()

xpos  = 0.11
ypos  = 0.91
cmsTextSize   = 0.03
CMSbox       = ROOT.TLatex  (xpos, ypos, "#scale[1.5]{CMS} ")
CMSbox       = ROOT.TLatex  (xpos, ypos, "#scale[1.5]{CMS}           Phase-2 Simulation              PU=200            14 TeV")
CMSbox.SetNDC()
CMSbox.SetTextSize(cmsTextSize)

lumi = "57 fb^{-1} (13 TeV)"
lumi = ""
lumibox = ROOT.TLatex  (0.7, 0.91, lumi)
lumibox.SetNDC()
lumibox.SetTextSize(cmsTextSize)

xposText = 0.63
yposText = 0.61
extraTextSize   = 0.035
extraTextBox1 = ROOT.TLatex  (xposText, yposText, "#tau_{h}#tau_{h} Trigger")
extraTextBox1.SetNDC()
extraTextBox1.SetTextSize(extraTextSize)

extraTextBox2 = ROOT.TLatex  (xposText, yposText - 0.06, "HLT")
extraTextBox2.SetNDC()
extraTextBox2.SetTextSize(extraTextSize)

extraTextBox3 = ROOT.TLatex  (xposText, yposText - 0.12, "|#eta| < 2.4")
#extraTextBox3 = ROOT.TLatex  (xposText, yposText - 0.12, "1.4 < |#eta| < 2.4")
extraTextBox3.SetNDC()
extraTextBox3.SetTextSize(extraTextSize)

extraTextBox4 = ROOT.TLatex  (xposText, yposText - 0.18, "")
extraTextBox4.SetNDC()
extraTextBox4.SetTextSize(extraTextSize)

extraTextBox5 = ROOT.TLatex  (xposText, yposText - 0.24, "")
extraTextBox5.SetNDC()
extraTextBox5.SetTextSize(extraTextSize)

legend = ROOT.TLegend(0.52, 0.66, 0.89, 0.88)
legend.SetLineColor(0)
legend.SetFillColor(0)
legend.SetTextSize(extraTextSize)



first = True
idxTau=0
for objType in objTypes:
    count=0
    for i in range (0, len(workingPoints)):
        count+=1
        if(count==5):
            count+=1
        hist_HLTTau = fileIn.Get("hist_%s_Resolution_for_%s" % (objType,workingPoints[i]))
        if(objType=="Et"):
            fit_HLTTau = hist_HLTTau.GetFunction("CBFuncAsymm");
            hist_HLTTau.SetAxisRange(0, 3)
        else:
            fit_HLTTau = hist_HLTTau.GetFunction("CBFunc");
            hist_HLTTau.SetAxisRange(-0.3, 0.3)
        if objType in titles:
            hist_HLTTau.SetTitle(titles[objType])
        hist_HLTTau.SetLineColor(count)
        hist_HLTTau.SetMarkerColor(count)
        hist_HLTTau.SetMarkerStyle(8)
        hist_HLTTau.SetMarkerSize(1.0)
        if (i==0):
            mm = hist_HLTTau.GetMaximum()
        hist_HLTTau.SetMaximum(1.15*mm)
        hist_HLTTau.SetMinimum(0)
        hist_HLTTau.GetXaxis().SetTitleOffset(0.9)
        hist_HLTTau.GetXaxis().SetTitleSize(0.05)
        hist_HLTTau.GetYaxis().SetTitleOffset(0.9)
        hist_HLTTau.GetYaxis().SetTitleSize(0.05)
        fit_HLTTau.SetLineColor(count)
        fit_HLTTau.SetLineWidth(2)
        fit_HLTTau.SetNpx(1000)
        fit_HLTTau.SetBit(TF1.kNotDraw)
        if (i==0):
            hist_HLTTau.Draw("p ")
        else:
            hist_HLTTau.Draw("p  same")
        fit_HLTTau.Draw("l same")
        if (idxTau==0):
            legend.AddEntry(hist_HLTTau,  workingPointNames[i],  "lp") 
    legend.Draw()
    CMSbox.Draw()
    lumibox.Draw()
    extraTextBox1.Draw()
    extraTextBox2.Draw()
    extraTextBox3.Draw()
    extraTextBox4.Draw()
    extraTextBox5.Draw()

    c1.Print(fileName_Out + "_" + objType + ".pdf", "pdf")
    c1.Print(fileName_Out + "_" + objType + ".png", "png")
    c1.Print(fileName_Out + "_" + objType + ".root", "root")
    idxTau+=1



