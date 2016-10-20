#!/usr/bin/python
from ROOT import *
TMVA.Tools.Instance()


### Visualising the results
##############################
TMVA.TMVAGUI("trainingBDT.root")
#TMVA.TMVAGUI("/vols/lhcb/bd1316/B2ppKgamma/TMVA/trainingBDT_MCcorrectedMOCK.root")

###Keep GUI alive
gApplication.Run()
