#!/usr/bin/env python
from ROOT import *
from math import *

path_origin = "/vols/lhcb/palvare1/B2pphgamma/B2ppKgamma/"
path_destination = "/vols/lhcb/bd1316/B2ppKgamma/"

fname = "B2pphgamma_S21_protonID" #complete TTree
fin = TFile(path_origin+fname+".root")
tin2 = fin.Get("B2pphgamma_Tuple/DecayTree")

cuts = {"proton_PIDp"  : 3,
        "proton_PIDpK" : 3,
        "Kaon_PIDK"    : 3,
        "Kaon_PIDpK"   : -1, 
        "vertex_chi2_ndof" : 9,
        }

selection = "pplus_PIDp>%(proton_PIDp)s && p~minus_PIDp>%(proton_PIDp)s"\
            "&& (pplus_PIDp - pplus_PIDK)>%(proton_PIDpK)s && (p~minus_PIDp - p~minus_PIDK)>%(proton_PIDpK)s"\
            "&& Kplus_PIDK>%(Kaon_PIDK)s && (Kplus_PIDp-Kplus_PIDK)<%(Kaon_PIDpK)s"\
            "&& (K_1_plus_ENDVERTEX_CHI2/K_1_plus_ENDVERTEX_NDOF)<%(vertex_chi2_ndof)s"%cuts 

fout = TFile(path_destination+fname+"_PID_K_selected_Paula.root","recreate")
tin  = tin2.CopyTree(selection)

fout.cd()
tin.Write()
fout.Close()
