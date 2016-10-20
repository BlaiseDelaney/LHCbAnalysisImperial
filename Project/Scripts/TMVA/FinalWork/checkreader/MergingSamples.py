from ROOT import *
from math import log, acos
'''
fin = TFile('/vols/lhcb/palvare1/B2pphgamma/BDT/training_samples.root')
t_sig = fin.Get("SignalTree") 

fout = TFile('SignalForMerging.root', 'recreate')
tSIg = t_sig.CloneTree()
tSIg.Write('DecayTree')
fout.Close()
fout = TFile('SignalForMerging.root')
t2 = fout.Get('DecayTree')

f1 = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/B_training_sampled.root')
t1 = f1.Get('DecayTree')


print t1.GetEntries(), t2.GetEntries()


tM = TFile('mergedSb.root')
tM.ls()
treef = tM.Get('DecayTree')
print treef.GetEntries()
'''


