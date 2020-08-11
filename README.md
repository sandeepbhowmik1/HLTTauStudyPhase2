# HLTTauStudyPhase2


go to inside of any $CMSSW_BASE/src/

cmsenv



# To make plots	



git clone https://github.com/sandeepbhowmik1/HLTTauStudyPhase2


cd HLTTauStudyPhase2/HLTTauPerformancePhase2/efficiencyPlot/fitTurnon


make clean

rm obj/*

make


cd HLTTauStudyPhase2/HLTTauPerformancePhase2

python commandsToMakePlots.py


see the plots in

cd HLTTauStudyPhase2/HLTTauPerformancePhase2/plots/



