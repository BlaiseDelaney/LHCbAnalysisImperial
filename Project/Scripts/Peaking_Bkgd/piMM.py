#!/usr/bin/env python

from ROOT import *
from math import *



def MM(tree, hist): 


    p_plus = TLorentzVector()
    p_minus = TLorentzVector() #pbar
    K_plus = TLorentzVector() 
    K_minus = TLorentzVector()
    gamma = TLorentzVector()  
    pi_plus = TLorentzVector()
    pi_minus = TLorentzVector()

    for i in tree:  
    
        p_plus.SetXYZM(i.pplus_PX, i.pplus_PY, i.pplus_PZ, mp)
        p_minus.SetXYZM(getattr(i,"p~minus_PX"), getattr(i,"p~minus_PY"), getattr(i,"p~minus_PZ"), mp)
        pi_plus.SetXYZM(i.Kplus_PX, i.Kplus_PY, i.Kplus_PZ, mpi)
        gamma.SetXYZM(i.gamma_PX, i.gamma_PY, i.gamma_PZ, 0.)

        hist.Fill((p_plus + p_minus + pi_plus).M()) 
       
            
path_origin1 = "/vols/lhcb/bd1316/B2ppKgamma/"
path_origin2 = "/vols/lhcb/palvare1/B2pphgamma/B2ppKgamma/"
path_destination = "/home/hep/bd1316/public_html/Temp/"


fname1 = "B2pphgamma_S21_protonID_PID_pi_selected"
fname2 = "B2pphgamma_S21_protonID" 

fin1 = TFile(path_origin1+fname1+".root")
tin1 = fin1.Get("DecayTree")

fin2 = TFile(path_origin2+fname2+".root")
tin2 = fin2.Get("B2pphgamma_Tuple/DecayTree")


#mass vals
mp = 938.27
mk = 493.677
mpi = 139.57

#histograms
nbins = 100
h_pppi_mass = TH1F("hpppi_mass","",nbins,4000,7000)
h_pppiPID_mass = TH1F("hpppiPID_mass","",nbins,4000,7000)


MM(tin2, h_pppi_mass)
MM(tin1, h_pppiPID_mass)



#Draw and save histograms
cv = TCanvas()
cv.Divide(2,1)
cv.cd(1)
h_pppi_mass.SetFillStyle(3004)
h_pppi_mass.SetLineColor(kBlue)
h_pppi_mass.SetFillColor(kBlue-7)
h_pppi_mass.Draw()
h_pppi_mass.SetTitle("p#bar{p}#pi^{+} No Cuts")
h_pppi_mass.GetXaxis().SetTitle("M_{p#bar{p}#pi^{+}} [MeV]")

cv.cd(2)
h_pppiPID_mass.SetFillStyle(3004)
h_pppiPID_mass.SetLineColor(kRed)
h_pppiPID_mass.SetFillColor(kRed-7)
h_pppiPID_mass.Draw()
h_pppiPID_mass.SetTitle("p#bar{p}#pi^{+} PID Cuts")
h_pppiPID_mass.GetXaxis().SetTitle("M_{p#bar{p}#pi^{+}} [MeV]")

cv.SaveAs(path_destination+"W_O_PIDcuts_nogamma.pdf")
