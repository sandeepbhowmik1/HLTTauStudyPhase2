import os, subprocess, sys


# ----------- *** Start Modification *** -------------------------------------

pathRootTree = '/home/sbhowmik/RootTree/HLTTau/Phase2/'

tagNTuple = ''
#tagRootTree = '20200618'
#tagPlot = '20200618'

#tagRootTree = 'hps_OnlineVtx_20200629'
#tagPlot = 'hps_OnlineVtx_20200701'
tagRootTree = 'hps_OfflineVtx_20200806'
tagPlot = 'hps_OfflineVtx_eta2p4_20200806'

workingDir = os.getcwd()

pathPlot = os.path.join(workingDir, "plots")

tauType = 'genTau' # genTau or recoGMTau to compare with l1Tau
#tauType = 'recoGMTau'

sampleType=["Signal", "Background"]
#sampleType=["Signal"]
#sampleType=["Background"] 

#nTau=["Single", "Double"]
nTau=["Double"]

#recoType=["Gen", "Reco"]
recoType=["Gen"]

algoType=["HLTTau"]

fileType=["rootTree", "bdt", "hist"] 
fileType=["rootTree"]

#objType=["Pt", "Eta", "Nvtx"]
objType=["Pt", "Eta"]

dzType=["with_dZ", "without_dZ"]
#dzType=["without_dZ"]

# ------------ *** End Modification *** --------------------------------------



# ------------ Define command to execute -------------------------------------
def run_cmd(command):
  print "executing command = '%s'" % command
  p = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  stdout, stderr = p.communicate()
  return stdout


# -------------- plot rate vs tau pt ----------------------------------

for j in range (0, len(algoType)): 
  scriptFile = os.path.join(workingDir, "ratePlot/macro", "rate_Calculation_using_Pt_for_"+algoType[j]+".C")
  #scriptFile = os.path.join(workingDir, "ratePlot/macro", "rate_Calculation_using_loop_for_"+algoType[j]+".C")
  fileName_In = os.path.join(pathRootTree, "rootTree_test_"+algoType[j]+"Analyzer_Background_"+tagRootTree+".root")
  treeName_In = algoType[j]+'Analyzer/HLTTauAnalyzer'
  fileName_Out = os.path.join(workingDir, "ratePlot/results", "hist_Rate_for_"+algoType[j]+"_Background_"+tagPlot+".root")
  run_cmd('root -b -n -q -l \'%s(\"%s\", \"%s\", \"%s\")\'' % (scriptFile, fileName_In, treeName_In, fileName_Out))
  scriptPlot = os.path.join(workingDir, "ratePlot/macro", "plot_Rate_for_All_WorkingPoints.py")
  fileName_Out_Plot = os.path.join(workingDir, "ratePlot/plots", "plot_Rate_for_All_WorkingPoints_"+algoType[j]+"_"+tagPlot)
  run_cmd('python %s %s %s' % (scriptPlot, fileName_Out, fileName_Out_Plot))



# -----------Convert root tree for efficiency plot ------------

for i in range (0, len(nTau)):
  for j in range (0, len(recoType)):
    for k in range (0, len(algoType)):
      for l in range (0, len(dzType)):
        scriptFile = os.path.join(workingDir, "efficiencyPlot/macro", "convertTreeFor_EfficiencyPlot_for_"+nTau[i]+"_"+recoType[j]+"_"+algoType[k]+"_"+dzType[l]+".py")
        fileName_In = os.path.join(pathRootTree, "rootTree_test_"+algoType[k]+"Analyzer_Signal_"+tagRootTree+".root")
        treeName_In = algoType[k]+'Analyzer/HLTTauAnalyzer'
        fileName_In_txt = os.path.join(workingDir, "ratePlot/results", "hist_Rate_for_"+algoType[k]+"_Background_"+tagPlot+".txt")
        fileName_Out = os.path.join(pathRootTree, "rootTree_Signal_Efficiency_for_"+nTau[i]+"_"+recoType[j]+"_"+algoType[k]+"_"+dzType[l]+"_"+tagPlot+".root")
        run_cmd('python %s %s %s %s %s' % (scriptFile, fileName_In, treeName_In, fileName_In_txt, fileName_Out))
      rootFiles=os.path.join(pathRootTree, "rootTree_Signal_Efficiency_for_"+nTau[i]+"_"+recoType[j]+"_"+algoType[k]+"_*"+tagPlot+".root")
      haddFile=os.path.join(pathRootTree, "rootTree_Signal_Efficiency_for_"+nTau[i]+"_"+recoType[j]+"_"+algoType[k]+"_"+tagPlot+".root")
      run_cmd('rm %s' % haddFile)
      run_cmd('hadd %s %s' % (haddFile, rootFiles))


# -------------- Plot efficiency turn-on vs Pt -------------------------------

scriptDir = os.path.join(workingDir, "efficiencyPlot/fitTurnon/run")
for i in range (0, len(objType)):
  scriptFile = os.path.join(scriptDir, "create_parameter_file_Efficiency_Fitter_vs_"+objType[i]+".sh")
  for j in range (0, len(nTau)):
    for k in range (0, len(recoType)):
      for l in range (0, len(algoType)):
        fileName_In = os.path.join(pathRootTree, "rootTree_Signal_Efficiency_for_"+nTau[j]+"_"+recoType[k]+"_"+algoType[l]+"_"+tagPlot+".root")
        fileName_Out = os.path.join(workingDir, "efficiencyPlot/results", "fitOutput_Efficiency_vs_"+objType[i]+"_for_"+nTau[j]+"_"+recoType[k]+"_"+algoType[l]+"_"+tagPlot+".root")
        scriptOut = "parameter_file_Efficiency_Fitter_vs_"+objType[i]+"_for_"+nTau[j]+"_"+recoType[k]+"_"+algoType[l]+"_"+tagPlot+".par"
        run_cmd('bash %s %s %s %s' % (scriptFile, fileName_In, fileName_Out, scriptOut))
        run_cmd('mv %s %s' % (scriptOut, scriptDir))
        scriptFit = os.path.join(workingDir, "efficiencyPlot/fitTurnon", "fit.exe")
        parFile = os.path.join(scriptDir, scriptOut)
        run_cmd('%s %s' %(scriptFit, parFile))

        scriptPlot = os.path.join(workingDir, "efficiencyPlot/macro", "plot_Efficiency_vs_"+objType[i]+"_for_All_WorkingPoints.py")
        fileName_In_txt = os.path.join(workingDir, "ratePlot/results", "hist_Rate_for_"+algoType[l]+"_Background_"+tagPlot+".txt")
        fileName_Out_Plot = os.path.join(workingDir, "efficiencyPlot/plots", "plot_Efficiency_vs_"+objType[i]+"_for_"+nTau[j]+"_"+recoType[k]+"_"+algoType[l]+"_"+tagPlot)
        run_cmd('python %s %s %s %s' % (scriptPlot, fileName_Out, fileName_In_txt, fileName_Out_Plot))




# -----------Convert root tree for resolution plot ------------   

for i in range (0, len(nTau)):
  for j in range (0, len(recoType)):
    for k in range (0, len(algoType)):
      scriptFile = os.path.join(workingDir, "resolutionPlot/macro", "convertTreeFor_ResolutionPlot_for_"+nTau[i]+"_"+recoType[j]+"_"+algoType[k]+".py")
      fileName_In = os.path.join(pathRootTree, "rootTree_test_"+algoType[k]+"Analyzer_Signal_"+tagRootTree+".root")
      treeName_In = algoType[k]+'Analyzer/HLTTauAnalyzer'
      fileName_In_txt = os.path.join(workingDir, "ratePlot/results", "hist_Rate_for_"+algoType[k]+"_Background_"+tagPlot+".txt")
      fileName_Out = os.path.join(pathRootTree, "rootTree_Signal_Resolution_for_"+nTau[i]+"_"+recoType[j]+"_"+algoType[k]+"_"+tagPlot+".root")
      run_cmd('python %s %s %s %s %s' % (scriptFile, fileName_In, treeName_In, fileName_In_txt, fileName_Out))


# -------------- Plot resolution -----------------------------------------  

for i in range (0, len(nTau)):
  for j in range (0, len(recoType)):
    for k in range (0, len(algoType)):
      scriptFile = os.path.join(workingDir, "resolutionPlot/macro", "make_Resolution.py")
      fileName_In = os.path.join(pathRootTree, "rootTree_Signal_Resolution_for_"+nTau[i]+"_"+recoType[j]+"_"+algoType[k]+"_"+tagPlot+".root")
      fileName_Out = os.path.join(workingDir, "resolutionPlot/results", "hist_Resolution_for_"+nTau[i]+"_"+recoType[j]+"_"+algoType[k]+"_"+tagPlot+".root")
      run_cmd('python %s %s %s' % (scriptFile, fileName_In, fileName_Out))
      scriptFit = os.path.join(workingDir, "resolutionPlot/macro", "fit_Resolution.C")
      fileName_fitOut = os.path.join(workingDir, "resolutionPlot/results", "fitted_Hist_Resolution_for_"+nTau[i]+"_"+recoType[j]+"_"+algoType[k]+"_"+tagPlot+".root")
      run_cmd('root -b -n -q -l \'%s(\"%s\", \"%s\")\'' % (scriptFit, fileName_Out, fileName_fitOut))
      scriptPlot = os.path.join(workingDir, "resolutionPlot/macro", "plot_Resolution_for_All_WorkingPoints.py")
      fileName_Out_Plot = os.path.join(workingDir, "resolutionPlot/plots", "plot_Resolution_for_"+nTau[i]+"_"+recoType[j]+"_"+algoType[k]+"_"+tagPlot)
      run_cmd('python %s %s %s' % (scriptPlot, fileName_fitOut, fileName_Out_Plot))



# ---------------- Keep relavant plots to plot directory ------------------

run_cmd('rm %s/*png' % pathPlot)
run_cmd('rm %s/*txt' % pathPlot)  
run_cmd('cp %s %s' % (workingDir+"/ratePlot/plots/"+"*"+tagPlot+"*.png", pathPlot))
run_cmd('cp %s %s' % (workingDir+"/efficiencyPlot/results/"+"*"+tagPlot+"*.txt", pathPlot)) 
run_cmd('cp %s %s' % (workingDir+"/efficiencyPlot/plots/"+"*"+tagPlot+"*.png", pathPlot))
run_cmd('cp %s %s' % (workingDir+"/resolutionPlot/plots/"+"*"+tagPlot+"*.png", pathPlot))

# ----------------- Clean all directory for results --------------------
'''
run_cmd('rm %s/*' % (os.path.join(workingDir, "plots")))
run_cmd('rm %s/*' % (os.path.join(workingDir, "ratePlot/results")))
run_cmd('rm %s/*' % (os.path.join(workingDir, "ratePlot/plots")))
run_cmd('rm %s/*.par' % (os.path.join(workingDir, "efficiencyPlot/fitTurnon/run")))
run_cmd('rm %s/*' % (os.path.join(workingDir, "efficiencyPlot/results")))
run_cmd('rm %s/*' % (os.path.join(workingDir, "efficiencyPlot/plots")))
run_cmd('rm %s/*' % (os.path.join(workingDir, "resolutionPlot/results")))
run_cmd('rm %s/*' % (os.path.join(workingDir, "resolutionPlot/plots")))
'''




