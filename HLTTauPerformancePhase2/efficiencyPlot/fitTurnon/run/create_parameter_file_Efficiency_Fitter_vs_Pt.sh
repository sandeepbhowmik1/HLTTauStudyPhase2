#!/bin/sh

fileName_In=$1
fileName_Out=$2
scriptOut=$3

#fileName_In='/home/sbhowmik/NTuple_Phase2/TallinnL1PFTau/NTuple_test_TallinnL1PFTauAnalyzer_VBFHToTauTau_forEfficiency_20190505.root'
#fileName_Out='/home/sbhowmik/Phase2/Tallinn/CMSSW_10_5_0_pre1/src/L1TauAnalyzer/L1PFTauAnalyzer/script/efficiencyPlot/results/fitOutput_efficiency_TallinnL1PFTau_VBFHToTauTau_vs_Pt_20190505.root'
#scriptOut='parameter_TallinnL1PFTau_Efficiency_Fitter_mc_vs_Pt.par'

varNameTag=(hltTauPtNoCut hltTauPt25 hltTauPt30 hltTauPt35 hltTauPt40 hltTauPt45)

#fileOut=parameter_${tauTag}_Efficiency_Fitter_mc_vs_Pt.par
fileOut=${scriptOut}

echo "OutputFile: ${fileName_Out}" | cat >>$fileOut
echo "NCPU: 4" | cat >>$fileOut

echo "Turnon.N: 6" | cat >>$fileOut

for ((i_varName=0; i_varName<6; i_varName++))
do

    i_var=$((${i_varName}+1))

    echo "Turnon.${i_var}.Name: Phase2_HLTTau_${varNameTag[i_varName]}" | cat >>$fileOut
    echo "Turnon.${i_var}.File: ${fileName_In}" | cat >>$fileOut
    echo "Turnon.${i_var}.Tree: HLTTauAnalyzer" | cat >>$fileOut
    echo "Turnon.${i_var}.XVar: tauPt" | cat >>$fileOut
    echo "Turnon.${i_var}.Cut: ${varNameTag[i_varName]}" | cat >>$fileOut
    echo "Turnon.${i_var}.WeightVar: bkgSubW" | cat >>$fileOut
    echo "Turnon.${i_var}.Binning: 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100 120 150 200 300 500 1000" | cat >>$fileOut
    echo "Turnon.${i_var}.FitRange:0 500" | cat >>$fileOut
    echo "Turnon.${i_var}.CB.Max: 1. 0.9 1." | cat >>$fileOut
    echo "Turnon.${i_var}.CB.Alpha: 3. 0.01 50." | cat >>$fileOut
    echo "Turnon.${i_var}.CB.N: 10. 1.001 100." | cat >>$fileOut
    echo "Turnon.${i_var}.CB.Mean: 30. 0. 120." | cat >>$fileOut
    echo "Turnon.${i_var}.CB.Sigma: 2. 0.01 10" | cat >>$fileOut

done
