#!/usr/bin/python
from ROOT import *
TMVA.Tools.Instance()


### Visualising the results
##############################
TMVA.TMVAGUI("/vols/lhcb/bd1316/B2ppKgamma/TMVA/FINALcutsANA/lBDTfinal.root")
#TMVA.TMVAGUI("/vols/lhcb/bd1316/B2ppKgamma/TMVA/trainingBDT_MCcorrectedMOCK.root")

###Keep GUI alive
gApplication.Run()
