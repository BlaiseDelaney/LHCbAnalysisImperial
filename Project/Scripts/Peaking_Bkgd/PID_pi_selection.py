#!/usr/bin/env python
from ROOT import *
from math import *

path_origin = "/vols/lhcb/palvare1/B2pphgamma/B2ppKgamma/"
#path_origin = "/vols/lhcb/palvare1/B2pphgamma/B2ppKgamma_MC/"
path_destination = "/vols/lhcb/bd1316/B2ppKgamma/"

fname = "B2pphgamma_S21_protonID" #complete TTree
#fname = "B2ppKgamma_S21"
fin = TFile(path_origin+fname+".root")
tin2 = fin.Get("B2pphgamma_Tuple/DecayTree")

cuts = {"proton_PIDp"  : 2,
        "proton_PIDpK" : 2,
        "Kaon_PIDK"    : -1,
        "vertex_chi2_ndof" : 9,
        }

selection = "pplus_PIDp>%(proton_PIDp)s && p~minus_PIDp>%(proton_PIDp)s"\
            "&& (pplus_PIDp - pplus_PIDK)>%(proton_PIDpK)s && (p~minus_PIDp - p~minus_PIDK)>%(proton_PIDpK)s"\
            "&& Kplus_PIDK<%(Kaon_PIDK)s"\
            "&& (B_plus_ENDVERTEX_CHI2/B_plus_ENDVERTEX_NDOF)<%(vertex_chi2_ndof)s"%cuts 

fout = TFile(path_destination+fname+"_PID_pi_selected_soft.root","RECREATE")
fout.cd()
tin  = tin2.CopyTree(selection)
#tin.SetDirectory(0) #potential fix, found online


#fout.cd()
tin.Write()
fout.Close()

