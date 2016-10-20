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
        "proton_PIDK" : 2,
        "proton_PIDpK" : -2,
        "proton_PIDpbarK" : 2,
        "Kaon_PIDK"    : 2,
        "vertex_chi2_ndof" : 5,
        }

#removed pplus_PIDp - pplus_PIDK < negative number
selection = "pplus_PIDp<%(proton_PIDp)s && p~minus_PIDp>%(proton_PIDp)s"\
            "&& (p~minus_PIDp - p~minus_PIDK)>%(proton_PIDpbarK)s"\
            "&& Kplus_PIDK<%(Kaon_PIDK)s"\
            "&& (K_1_plus_ENDVERTEX_CHI2/K_1_plus_ENDVERTEX_NDOF)<%(vertex_chi2_ndof)s"%cuts 

fout = TFile(path_destination+fname+"_PID_Lambda_c_pKpi.root","RECREATE")
fout.cd()

tin  = tin2.CopyTree(selection)


#tin.Write()
#fout.Close()
def MM(tree): 


    p_plus = TLorentzVector()
    p_minus = TLorentzVector() #pbar
    K_plus = TLorentzVector() 
    K_minus = TLorentzVector()
    pi_plus = TLorentzVector()
    pi_minus = TLorentzVector()

    for i in tree:  
    

        K_plus.SetXYZM(i.pplus_PX, i.pplus_PY, i.pplus_PZ, mk)
        p_minus.SetXYZM(getattr(i,"p~minus_PX"), getattr(i,"p~minus_PY"), getattr(i,"p~minus_PZ"), mp)
        pi_minus.SetXYZM(i.Kplus_PX, i.Kplus_PY, i.Kplus_PZ, mpi)

        h_pKpi_mass.Fill((p_minus + K_plus + pi_minus).M()) 

#mass vals
mp = 938.27
mk = 493.677
mpi = 139.57

#histograms
nbins = 100
h_pKpi_mass = TH1F("hpKpi_mass","hpKpi_mass",nbins,200,6000)


MM(tin)


#Draw and save histograms
cv = TCanvas()
h_pKpi_mass.SetFillStyle(3004)
h_pKpi_mass.SetLineColor(kBlue)
h_pKpi_mass.SetFillColor(kBlue-7)
h_pKpi_mass.Draw()
h_pKpi_mass.SetTitle("#Lambda_{c}#rightarrow#bar{p}K^{+}#pi^{-}")
h_pKpi_mass.GetXaxis().SetTitle("M_{#bar{p}K^{+}#pi^{-}} [MeV]")


out_path_pdf = "/home/hep/bd1316/public_html/Temp/"
cv.SaveAs(out_path_pdf+"Lambda_c_pKpi_EnhancedBkg.pdf")

