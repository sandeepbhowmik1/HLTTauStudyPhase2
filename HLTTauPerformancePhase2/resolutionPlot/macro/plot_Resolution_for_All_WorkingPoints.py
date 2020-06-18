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
workingPoints=["hltTauPtNoCut", "hltTauPt25", "hltTauPt30", "hltTauPt35", "hltTauPt40", "hltTauPt45"]
workingPointNames = ["No cut (No p_{T} Threshold )", "HLT #tau p_{T} > 25 Gev", "HLT #tau p_{T} > 30 Gev", "HLT #tau p_{T} > 35 Gev", "HLT #tau p_{T} > 40 Gev", "HLT #tau p_{T} > 45 Gev"]

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
        hist_L1PFTau = fileIn.Get("hist_%s_Resolution_for_%s" % (objType,workingPoints[i]))
        if(objType=="Et"):
            fit_L1PFTau = hist_L1PFTau.GetFunction("CBFuncAsymm");
            hist_L1PFTau.SetAxisRange(0, 3)
        else:
            fit_L1PFTau = hist_L1PFTau.GetFunction("CBFunc");
            hist_L1PFTau.SetAxisRange(-0.3, 0.3)
        if objType in titles:
            hist_L1PFTau.SetTitle(titles[objType])
        hist_L1PFTau.SetLineColor(count)
        hist_L1PFTau.SetMarkerColor(count)
        hist_L1PFTau.SetMarkerStyle(8)
        hist_L1PFTau.SetMarkerSize(1.0)
        if (i==0):
            mm = hist_L1PFTau.GetMaximum()
        hist_L1PFTau.SetMaximum(1.15*mm)
        hist_L1PFTau.SetMinimum(0)
        hist_L1PFTau.GetXaxis().SetTitleOffset(0.9)
        hist_L1PFTau.GetXaxis().SetTitleSize(0.05)
        hist_L1PFTau.GetYaxis().SetTitleOffset(0.9)
        hist_L1PFTau.GetYaxis().SetTitleSize(0.05)
        fit_L1PFTau.SetLineColor(count)
        fit_L1PFTau.SetLineWidth(2)
        fit_L1PFTau.SetNpx(1000)
        fit_L1PFTau.SetBit(TF1.kNotDraw)
        if (i==0):
            hist_L1PFTau.Draw("p ")
        else:
            hist_L1PFTau.Draw("p  same")
        fit_L1PFTau.Draw("l same")
        if (idxTau==0):
            legend.AddEntry(hist_L1PFTau,  workingPoints[i],  "lp") 
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



