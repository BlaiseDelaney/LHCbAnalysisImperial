#!/usr/bin/env python
from ROOT import *
from math import *

path_origin = "/vols/lhcb/palvare1/B2pphgamma/B2ppKgamma/"
path_destination = "/vols/lhcb/bd1316/B2ppKgamma/"

fname = "B2pphgamma_S21_protonID" #complete TTree

fin = TFile(path_origin+fname+".root")
tin2 = fin.Get("B2pphgamma_Tuple/DecayTree")

fout = TFile(path_destination+fname+"_Lambda_c_BkdEnhancedPiPK","RECREATE")
fout.cd()


cuts = {"proton_PIDp"  : 5,
        "proton_PIDpminus" : 2,
        "proton_PIDpK" : 2,
        "Kaon_PIDK"    : 2,
        "Kaon_PIDpK"   : -1, 
        "vertex_chi2_ndof" : 9,
        }

selection = "pplus_PIDp<%(proton_PIDp)s && p~minus_PIDp>%(proton_PIDpminus)s"\
            "&& (p~minus_PIDp - p~minus_PIDK)>%(proton_PIDpK)s"\
            "&& Kplus_PIDK>%(Kaon_PIDK)s"\
            "&& (Kplus_PIDp - Kplus_PIDK)<%(Kaon_PIDpK)s"\
            "&& (B_plus_ENDVERTEX_CHI2/B_plus_ENDVERTEX_NDOF)<%(vertex_chi2_ndof)s"%cuts 

tin  = tin2.CopyTree(selection)
print type(tin)

def MM(tree): 


    p_plus = TLorentzVector()
    p_minus = TLorentzVector() #pbar
    K_plus = TLorentzVector() 
    K_minus = TLorentzVector()
    pi_plus = TLorentzVector()
    pi_minus = TLorentzVector()

    for i in tree:  
    

        K_plus.SetXYZM(i.Kplus_PX, i.Kplus_PY, i.Kplus_PZ, mk)
        p_minus.SetXYZM(getattr(i,"p~minus_PX"), getattr(i,"p~minus_PY"), getattr(i,"p~minus_PZ"), mp)
        pi_minus.SetXYZM(i.pplus_PX, i.pplus_PY, i.pplus_PZ, mpi)

        h_pKpi_mass.Fill((p_minus + K_plus + pi_minus).M()) 

#mass vals
mp = 938.27
mk = 493.677
mpi = 139.57

#histograms
nbins = 100
h_pKpi_mass = TH1F("hpKpi_mass","hpKpi_mass",nbins,1500,3000)


MM(tin)


#Draw and save histograms
cv = TCanvas()
h_pKpi_mass.SetFillStyle(3004)
h_pKpi_mass.SetLineColor(kBlue)
h_pKpi_mass.SetFillColor(kBlue-7)
h_pKpi_mass.Draw()
h_pKpi_mass.SetTitle("#Lambda_{c}#rightarrow#pi^{-}#bar{p}K^{+}")
h_pKpi_mass.GetXaxis().SetTitle("M_{#pi^{-}#bar{p}K^{+}} [MeV]")


out_path_pdf = "/home/hep/bd1316/public_html/Temp/"
cv.SaveAs(out_path_pdf+"Lambda_c_EnhancedBkd_pipK_Bbadlyvertexed.pdf")

#tin.Write()
#fout.Close()

