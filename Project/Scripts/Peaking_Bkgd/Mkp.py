#!/usr/bin/env python

from ROOT import *
from math import *

#misID = "p_pbar_Kpi_gamma_nocuts"
misID1 = "p_pbar_K"
misID2 = "p_pbar_pi"

c1 = TCanvas("c1", "")
c1.Divide(2,2)

pad1 = TPad("pad1", "", 0.03, 0.5, 0.5, 0.92) 
pad1.Draw()

pad2 = TPad("pad2", "", 0.5, 0.5, 0.95, 0.92) 
pad2.Draw()

pad3 = TPad("pad3", "", 0.03, 0.03, 0.5, 0.45) 
pad3.Draw()

pad4 = TPad("pad4", "", 0.5, 0.05, 0.95, 0.4) 
pad4.Draw()

nbins = 100
gStyle.SetOptStat(0)

hist = TH1F("hist", "", nbins, 1000, 6000)
hist2D = TH2F("hist2D", "", nbins, 0, 2000, nbins, 0, 2000)
projx = TH1F("projx", "", nbins, 0, 2000)
projy = TH1F("projy", "", nbins, 0, 2000)

def MM(tree): 


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
        K_plus.SetXYZM(i.Kplus_PX, i.Kplus_PY, i.Kplus_PZ, mk)
        gamma.SetXYZM(i.gamma_PX, i.gamma_PY, i.gamma_PZ, 0.)

        hist.Fill( (p_minus + K_plus).M() ) 
        hist2D.Fill( ((p_minus).M()), ((K_plus).M()))
        projx.Fill(p_minus.M())
        projy.Fill(K_plus.M())
        


path_origin = "/vols/lhcb/bd1316/B2ppKgamma/"
fname1 = "B2pphgamma_S21_protonID_PID_K_selected"
fin1 = TFile(path_origin+fname1+".root")
tin1 = fin1.Get("DecayTree")


#mass vals
mp = 938.27
mk = 493.677
mpi = 139.57


MM(tin1)



pad1.cd()
pad1.SetLeftMargin(0.15)
pad1.SetBottomMargin(0.15)
hist.Draw("HIST")
hist.SetFillStyle(3004)
hist.SetFillColor(kBlack)
hist.SetLineColor(kBlack)
hist.GetYaxis().SetTitleSize(0.05)
hist.GetXaxis().SetTitleSize(0.05)
hist.GetYaxis().SetTitleOffset(1.)
hist.GetXaxis().SetTitleOffset(1.)
hist.GetXaxis().SetTitle("M_{#bar{p}K^{+}} [MeV]")

pad4.cd()
hist2D.Draw("CONTZ")
hist2D.GetYaxis().SetTitle("M_{K} [MeV]")
hist2D.GetXaxis().SetTitle("M_{#bar{p}} [MeV]")
hist2D.GetXaxis().SetTitleOffset(1.)
hist2D.GetYaxis().SetTitleOffset(1.)


pad3.cd()
pad3.SetBottomMargin(0.15)
projx.SetLineColor(kBlue-7)
projx.Draw("HIST")
projx.GetXaxis().SetTitle("M_{#bar{p}} [MeV]")

pad2.cd()
pad2.SetBottomMargin(0.15)
projy.SetLineColor(kRed)
projy.Draw("HIST")
projy.GetXaxis().SetTitle("M_{K^{+}} [MeV]")

out_path_pdf = "/home/hep/bd1316/public_html/Temp/2Dhist_B2ppK/"
c1.SaveAs(out_path_pdf+"Mp_MK.pdf")


