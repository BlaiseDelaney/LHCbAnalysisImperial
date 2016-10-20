#!/usr/bin/env python

from ROOT import *
from math import *

#misID = "p_pbar_Kpi_gamma_nocuts"
misID1 = "p_pbar_K"
misID2 = "p_pbar_pi"


#list all combination of mis(ID) (long winded)
def MM(tree, h): 


    p_plus = TLorentzVector()
    p_minus = TLorentzVector() #pbar
    K_plus = TLorentzVector() 
    K_minus = TLorentzVector()
    gamma = TLorentzVector()  
    pi_plus = TLorentzVector()
    pi_minus = TLorentzVector()

    for i in tree:  
    
        if h == misID1: 

            p_plus.SetXYZM(i.pplus_PX, i.pplus_PY, i.pplus_PZ, mp)
            p_minus.SetXYZM(getattr(i,"p~minus_PX"), getattr(i,"p~minus_PY"), getattr(i,"p~minus_PZ"), mp)
            K_plus.SetXYZM(i.Kplus_PX, i.Kplus_PY, i.Kplus_PZ, mk)
            gamma.SetXYZM(i.gamma_PX, i.gamma_PY, i.gamma_PZ, 0.)

            #h_ppKg_mass.Fill((p_plus + p_minus + K_plus + gamma).M()) 
            #h_ppKg_mass.Fill((p_plus + p_minus + K_plus).M()) 
            h_ppKg_mass.Fill((p_plus + p_minus).M()) 
        
        if h == misID2: 

            p_plus.SetXYZM(i.pplus_PX, i.pplus_PY, i.pplus_PZ, mp)
            p_minus.SetXYZM(getattr(i,"p~minus_PX"), getattr(i,"p~minus_PY"), getattr(i,"p~minus_PZ"), mp)
            pi_plus.SetXYZM(i.Kplus_PX, i.Kplus_PY, i.Kplus_PZ, mpi)
            gamma.SetXYZM(i.gamma_PX, i.gamma_PY, i.gamma_PZ, 0.)

            #h_pppig_mass.Fill((p_plus + p_minus + pi_plus + gamma).M()) 
            h_pppig_mass.Fill((p_plus + p_minus + pi_plus).M()) 
   

path_origin = '/vols/lhcb/bd1316/B2ppKgamma/TMVA/'
fname1 = 'ML_data'
'''            
path_origin = "/vols/lhcb/bd1316/B2ppKgamma/"

fname1 = "B2pphgamma_S21_protonID_PID_K_selected_soft"
fname2 = "B2pphgamma_S21_protonID_PID_pi_selected_soft"
#fname1= "PIDK_B2ppKg_soft"  #loose PID couts
#fname2 = "PIDpi_B2pppig_soft" #loose PID couts
'''


fin1 = TFile(path_origin+fname1+".root")
tin1 = fin1.Get("ML_Tree")


'''
fin2 = TFile(path_origin+fname2+".root")
tin2 = fin2.Get("DecayTree")
'''

#mass vals
mp = 938.27
mk = 493.677
mpi = 139.57

#histograms
nbins = 100
h_ppKg_mass = TH1F("hppKg_mass","h_ppbar_K_loosecuts_mass",nbins,0,7000)
h_pppig_mass = TH1F("hpppig_mass","h_ppbar_pi_loosecuts_mass",nbins,4000,7000)


MM(tin1, misID1)
#MM(tin2, misID2)



#Draw and save histograms
cv = TCanvas()
cv.Divide(2,1)
cv.cd(1)
h_ppKg_mass.SetFillStyle(1001)
h_ppKg_mass.SetLineColor(kBlue)
h_ppKg_mass.SetFillColor(kBlue-7)
h_ppKg_mass.Draw()
h_ppKg_mass.SetTitle("B^{+}#rightarrowp#bar{p}K^{+}#gamma")
h_ppKg_mass.GetXaxis().SetTitle("M_{p#bar{p}K^{+}} [MeV]")

cv.cd(2)
h_pppig_mass.SetFillStyle(1001)
h_pppig_mass.SetLineColor(kRed)
h_pppig_mass.SetFillColor(kRed-7)
h_pppig_mass.Draw()
h_pppig_mass.SetTitle("B^{+}#rightarrowp#bar{p}#pi^{+}#gamma")
h_pppig_mass.GetXaxis().SetTitle("M_{p#bar{p}#pi^{+}} [MeV]")

#out_path_pdf = "/home/hep/bd1316/public_html/Temp/PID_loose/"
#cv.SaveAs(out_path_pdf+"B2ppK_loosePID_nogamma.pdf")
