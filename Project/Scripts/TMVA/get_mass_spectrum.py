from ROOT import *
from math import *


path = "/vols/lhcb/palvare1/B2pphgamma/B2ppKgamma/"
fname = "B2pphgamma_S21_2011_MD_protonID"
fin = TFile(path+fname+".root")
tin2 = fin.Get("B2pphgamma_Tuple/DecayTree")


## Selection example
cuts = {"proton_PIDp"  : 5,
        "proton_PIDpK" : 5,
        "Kaon_PIDK"    : 5,
        "Kaon_PIDpK"   : -5,
        "vertex_chi2_ndof" : 5,
        }

selection = "pplus_PIDp>%(proton_PIDp)s && p~minus_PIDp>%(proton_PIDp)s"\
            "&& (pplus_PIDp - pplus_PIDK)>%(proton_PIDpK)s && (p~minus_PIDp - p~minus_PIDK)>%(proton_PIDpK)s"\
            "&& Kplus_PIDK>%(Kaon_PIDK)s && (Kplus_PIDp-Kplus_PIDK)>%(Kaon_PIDpK)s"\
            "&& (B_plus_ENDVERTEX_CHI2/B_plus_ENDVERTEX_NDOF)<%(vertex_chi2_ndof)s"%cuts


fout = TFile(path+fname+"_selected.root","recreate")
tin  = tin2.CopyTree(selection)

mp = 938.27
mk = 493.677
mpi = 139.57


## Making some plots
nbins = 100
h_ppKg_mass = TH1F("hppKg_mass","hppKg_mass",nbins,4000,7000)
h_pppig_mass = TH1F("hpppig_mass","hpppig_mass",nbins,4000,7000)
# h_pp_mass = TH1F("hpp_mass","hpp_mass",nbins,2600,5000)
# h_ppK_mass = TH1F("hppK_mass","hppK_mass",nbins,1700,7000)
# h_pppi_mass = TH1F("hpppi_mass","hpppi_mass",nbins,1700,7000)

p_plus = TLorentzVector()
p_minus = TLorentzVector()
K_plus = TLorentzVector()
gamma = TLorentzVector()
pi_plus = TLorentzVector()

for i in tin:

    p_plus.SetXYZM(i.pplus_PX, i.pplus_PY, i.pplus_PZ, mp)
    p_minus.SetXYZM(getattr(i,"p~minus_PX"), getattr(i,"p~minus_PY"), getattr(i,"p~minus_PZ"), mp)
    K_plus.SetXYZM(i.Kplus_PX, i.Kplus_PY, i.Kplus_PZ, mk)
    gamma.SetXYZM(i.gamma_PX, i.gamma_PY, i.gamma_PZ, 0.)

    ## Mass ppKgamma
    h_ppKg_mass.Fill((p_plus + p_minus + K_plus + gamma).M())

    ## Mass ppKgamma
    pi_plus.SetXYZM(i.Kplus_PX, i.Kplus_PY, i.Kplus_PZ, mpi)
    h_pppig_mass.Fill((p_plus + p_minus + pi_plus + gamma).M())


cv = TCanvas()
cv.Divide(2,1)
cv.cd(1)
h_ppKg_mass.SetLineColor(kRed)
h_ppKg_mass.Draw()
cv.cd(2)
h_pppig_mass.Draw()

# cv3 = TCanvas()
# cv3.Divide(2,1)
# cv3.cd(1)
# h_ppK_mass.Draw()
# cv3.cd(2)
# h_pppi_mass.Draw()

# cv2 = TCanvas()
# h_pp_mass.Draw()

