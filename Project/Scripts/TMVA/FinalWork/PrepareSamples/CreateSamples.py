from ROOT import *
from math import log, acos

### Creating training samples
##############################
f_sig = TFile("/vols/lhcb/palvare1/B2pphgamma/B2ppKgamma_MC/B2pphgamma_S21_v2.root")
t_sig_all = f_sig.Get("B2ppKgamma_Tuple/DecayTree")

f_bkg = TFile("/vols/lhcb/palvare1/B2pphgamma/B2ppKgamma/B2pphgamma_S21_protonID.root")
t_bkg_all = f_bkg.Get("B2pphgamma_Tuple/DecayTree")
fout = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/TMVA_MCcorrected.root','recreate')
fout.cd()
t_sig = t_sig_all.CopyTree("B_plus_BKGCAT<55") ## Truthmatching of the MC
t_sig.Write("SignalTree")
#t_bkg = t_bkg_all.CopyTree("B_plus_MM>6000 && B_plus_MM<7000") ## Higher mass sideband 
#t_bkg.Write("BkgTree")


