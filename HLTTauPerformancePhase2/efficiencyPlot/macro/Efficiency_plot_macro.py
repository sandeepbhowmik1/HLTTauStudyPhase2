import ROOT
import operator
import array


ROOT.gSystem.Load('libRooFit')


class Efficiency:
    def __init__(self, **args):
        self.name        = args.get("Name", "turnon")     
        #self.legend      = args.get("Legend","")
        self.legend      = args.get("Legend","Turn-on")
        self.histo       = args.get("Histo", None)
        self.fit         = args.get("Fit", None)
        self.markerColor = args.get("MarkerColor", ROOT.kBlack)
        self.markerStyle = args.get("MarkerStyle", 20)
        self.lineColor   = args.get("LineColor", ROOT.kBlack)
        self.lineStyle   = args.get("LineStyle", 1)
        self.histo.SetName(self.name+"_histo")
        self.fit.SetName(self.name+"_fit")



class EfficiencyPlot:
    def __init__(self, **args):
        self.name  = ""
        self.turnons = []
        self.plotDir = ""
        self.xRange = (10, 300)
        #self.xTitle = "p_{T}^{#tau, offline} [GeV]"
        self.xTitle = "p_{T}^{#tau, gen} [GeV]"
        #self.xTitle = "Number of vertices"
        #self.xTitle = "#eta^{#tau, offline}"
        self.legendPosition = (0.1,0.2,0.85,0.6)
        self.setPlotStyle()
        #self.workingPoint = args.get("WorkingPoint", "")
        self.xposText = 0.65
        self.yposText = 0.60
        self.extraText1 = "#tau_{h}#tau_{h} Trigger"
        self.extraText2 = "HPS@L1"
        self.extraText3 = "|#eta| < 2.172"
        self.extraText4 = "Rate 12 kHz"
        self.extraText5 = "True #tau_{h} p_{T} > 30 GeV"


    def addEfficiency(self, turnon):
        self.turnons.append(turnon)

    def plot(self):
        canvas = ROOT.TCanvas("c_"+self.name, self.name, 800, 800)
        canvas.SetGrid()
        #canvas.SetLogx()
        hDummy = ROOT.TH1F("hDummy_"+self.name, self.name, 1, self.xRange[0], self.xRange[1])
        #hDummy.SetAxisRange(0, 1.29, "Y")
        hDummy.SetAxisRange(0, 1.01, "Y")
        hDummy.SetXTitle(self.xTitle)
        #hDummy.SetYTitle("Test")
        hDummy.SetYTitle("Efficiency")
        hDummy.Draw()

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

        xposText = 0.65
        yposText = 0.60
        extraTextSize   = 0.035
        extraTextBox1 = ROOT.TLatex  (self.xposText, self.yposText, self.extraText1)
        extraTextBox1.SetNDC()
        extraTextBox1.SetTextSize(extraTextSize)

        extraTextBox2 = ROOT.TLatex  (self.xposText, self.yposText - 0.05, self.extraText2)
        extraTextBox2.SetNDC()
        extraTextBox2.SetTextSize(extraTextSize)

        extraTextBox3 = ROOT.TLatex  (self.xposText, self.yposText - 0.10, self.extraText3)
        extraTextBox3.SetNDC()
        extraTextBox3.SetTextSize(extraTextSize)

        extraTextBox4 = ROOT.TLatex  (self.xposText, self.yposText - 0.15, self.extraText4)
        extraTextBox4.SetNDC()
        extraTextBox4.SetTextSize(extraTextSize)

        extraTextBox5 = ROOT.TLatex  (self.xposText, self.yposText - 0.20, self.extraText5)
        extraTextBox5.SetNDC()
        extraTextBox5.SetTextSize(extraTextSize)

        legend = ROOT.TLegend(self.legendPosition[0],self.legendPosition[1],self.legendPosition[2],self.legendPosition[3])
        legend.SetLineColor(0)
        legend.SetFillColor(0)
	legend.SetTextSize(extraTextSize)

        for turnon in self.turnons:
            histo = turnon.histo
            histo.SetMarkerStyle(turnon.markerStyle)
            histo.SetMarkerColor(turnon.markerColor)
            histo.SetLineColor(turnon.markerColor)
            fit = turnon.fit
            fit.SetLineStyle(turnon.lineStyle)
            fit.SetLineColor(turnon.lineColor)
            fit.SetLineWidth(3)
            histo.Draw("pe same")
            #fit.Draw("l same")
            legend.AddEntry(histo, turnon.legend, "lp")
            legend.Draw()
        CMSbox.Draw()
        lumibox.Draw()
        extraTextBox1.Draw()
        extraTextBox2.Draw()
        extraTextBox3.Draw()
        extraTextBox4.Draw()
        extraTextBox5.Draw()

        canvas.Print(self.name+".pdf", "pdf")
        canvas.Print(self.name+".png", "png")
        canvas.Print(self.name+".root", "root")
        return canvas

    def setPlotStyle(self):
        #ROOT.gROOT.SetStyle("Plain")
        #ROOT.gStyle.SetOptStat()
        #ROOT.gStyle.SetOptFit(0)
        ROOT.gStyle.SetOptTitle(0)
        #ROOT.gStyle.SetFrameLineWidth(1)
        #ROOT.gStyle.SetPadBottomMargin(0.13)
        ROOT.gStyle.SetPadLeftMargin(0.11)
        #ROOT.gStyle.SetPadTopMargin(0.06)
        #ROOT.gStyle.SetPadRightMargin(0.05)

        #ROOT.gStyle.SetLabelFont(42,"X")
        #ROOT.gStyle.SetLabelFont(42,"Y")
        #ROOT.gStyle.SetLabelSize(0.04,"X")
        #ROOT.gStyle.SetLabelSize(0.04,"Y")
        #ROOT.gStyle.SetLabelOffset(0.01,"Y")
        #ROOT.gStyle.SetTickLength(0.02,"X")
        #ROOT.gStyle.SetTickLength(0.02,"Y")
        #ROOT.gStyle.SetLineWidth(1)
        #ROOT.gStyle.SetTickLength(0.02 ,"Z")

        #ROOT.gStyle.SetTitleSize(0.04)
        #ROOT.gStyle.SetTitleFont(42,"X")
        #ROOT.gStyle.SetTitleFont(42,"Y")
        ROOT.gStyle.SetTitleSize(0.05,"X")
        ROOT.gStyle.SetTitleSize(0.05,"Y")
        ROOT.gStyle.SetTitleOffset(.9,"X")
        ROOT.gStyle.SetTitleOffset(.9,"Y")
        ROOT.gStyle.SetOptStat(000000)
        #ROOT.gStyle.SetPalette(1)
        #ROOT.gStyle.SetPaintTextFormat("3.2f")
        #ROOT.gROOT.ForceStyle()
