from ROOT import *
import math

#fin = TFile('/vols/lhcb/palvare1/B2pphgamma/BDT/training_samples.root')
fin = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/TMVA_MCcorrected.root')
t_bkgd = fin.Get('BkgTree')
t_signal = fin.Get('SignalTree')

#fout = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/B_training_sampled.root', 'recreate')
fout = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/B_training_sampledUpdated.root', 'recreate')
fout.cd()
SB_tout = t_bkgd.CloneTree(0)

S_nentries = t_signal.GetEntries()
B_nentries = t_bkgd.GetEntries()

print "Background tree has %d entries"%B_nentries
print "Signal tree has %d entries"%S_nentries


rand = TRandom3(0)
N = S_nentries

for i in range(0, N):
    j = rand.Integer(B_nentries)
    t_bkgd.GetEntry(j)
    SB_tout.Fill()
           
        
SB_nentries = SB_tout.GetEntries()
print "Sampled backgroundtree has %d entries"%SB_nentries

SB_tout.Write()
fout.Close()

