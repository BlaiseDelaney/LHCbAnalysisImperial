#!/usr/bin/env python

from ROOT import *
from math import *


c1 = TCanvas("c1", "")
c1.Divide(2,2)

pad1 = TPad("pad1", "", 0.03, 0.5, 0.5, 0.92) 
pad1.Draw()

pad2 = TPad("pad2", "", 0.5, 0.5, 0.95, 0.92) 
pad2.Draw()

pad3 = TPad("pad3", "", 0.03, 0.03, 0.5, 0.45) 
pad3.Draw()

pad4 = TPad("pad4", "", 0.5, 0.03, 0.95, 0.5) 
pad4.Draw()

nbins = 100
gStyle.SetOptStat(0)

hist = TH2F("hist", "", nbins, 2000, 4000, nbins, 4000, 6000)
hist3D = TH2F("hist3D", "", nbins,2000, 4000, nbins, 4000, 6000)

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

        hist.Fill( ((p_plus+p_minus).M()), ((p_plus+p_minus+K_plus).M()) )
        hist3D.Fill( ((p_plus+p_minus).M()), ((p_plus+p_minus+K_plus).M()) )
        
        

path_origin = "/vols/lhcb/bd1316/B2ppKgamma/B2ppKgamma/"
fname1 = "B2pphgamma_S21_protonID_PID_K_selected_soft"
fin1 = TFile(path_origin+fname1+".root")
tin1 = fin1.Get("DecayTree")

#mass vals
mp = 938.27
mk = 493.677
mpi = 139.57
nbins = 1000


MM(tin1)

projx = hist.ProjectionX()
projy =hist.ProjectionY()


pad1.cd()
pad1.SetLeftMargin(0.15)
pad1.SetBottomMargin(0.15)
hist.Draw("CONTZ")
hist.GetYaxis().SetTitleSize(0.05)
hist.GetXaxis().SetTitleSize(0.05)
hist.GetYaxis().SetTitleOffset(1.)
hist.GetXaxis().SetTitleOffset(1.)
hist.GetYaxis().SetTitle("M_{p#bar{p}K^{+}} [MeV]")
hist.GetXaxis().SetTitle("M_{p#bar{p}} [MeV]")

pad4.cd()
hist3D.Draw("SURF2")
hist3D.GetYaxis().SetTitle("M_{p#bar{p}K^{+}} [MeV]")
hist3D.GetXaxis().SetTitle("M_{p#bar{p}} [MeV]")
hist3D.GetXaxis().SetTitleOffset(2.)
hist3D.GetYaxis().SetTitleOffset(2.)


pad3.cd()
pad3.SetBottomMargin(0.15)
projx.SetFillStyle(3005)
projx.SetFillColor(kBlue-7)
projx.Draw("HIST")
projx.GetXaxis().SetTitle("M_{p#bar{p}} [MeV]")

pad2.cd()
pad2.SetBottomMargin(0.15)
projy.SetFillStyle(3005)
projy.SetFillColor(kRed-7)
projy.SetLineColor(kRed)
projy.Draw("HIST")
projy.GetXaxis().SetTitle("M_{p#bar{p}K^{+}} [MeV]")
out_path_pdf = "/home/hep/bd1316/public_html/Temp/2Dhist_B2ppK/"
c1.SaveAs(out_path_pdf+"Mpp_MppK_loosePID.pdf")

