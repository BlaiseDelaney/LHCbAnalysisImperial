from ROOT import *
from math import *


path_origin = "/vols/lhcb/palvare1/B2pphgamma/B2ppKgamma/"
path_destination = "/home/hep/bd1316/public_html/Temp/"

fname = "B2pphgamma_S21_protonID" 
fin = TFile(path_origin+fname+".root")
tin = fin.Get("B2pphgamma_Tuple/DecayTree")

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



pad1.cd()
pad1.SetLeftMargin(0.15)
pad1.SetBottomMargin(0.15)
tin.Draw("(K_1_plus_ENDVERTEX_CHI2/K_1_plus_ENDVERTEX_NDOF):(B_plus_ENDVERTEX_CHI2/B_plus_ENDVERTEX_NDOF)>>h2(100, -2, 10, 100, -2, 10)")
#gStyle.SetPalette(53)
h2.Draw("CONTZ")
h2.GetYaxis().SetTitleSize(0.05)
h2.GetXaxis().SetTitleSize(0.05)
h2.GetYaxis().SetTitleOffset(1.)
h2.GetXaxis().SetTitleOffset(1.)
h2.GetYaxis().SetTitle("Reduced #chi^{2}_{ppK}")
h2.GetXaxis().SetTitle("Reduced #chi^{2}_{B^{+}}")
h2.SetTitle("Reduced #chi^{2}_{ppK} vs Reduced #chi^{2}_{B^{+}} ")

pad4.cd()
tin.Draw("(K_1_plus_ENDVERTEX_CHI2/K_1_plus_ENDVERTEX_NDOF):(B_plus_ENDVERTEX_CHI2/B_plus_ENDVERTEX_NDOF)>>hist3D(100, -2, 10, 100, -2, 10)")
#gStyle.SetPalette(53)
hist3D.Draw("SURF2")
hist3D.GetYaxis().SetTitle("Reduced #chi^{2}_{ppK}")
hist3D.GetXaxis().SetTitle("Reduced #chi^{2}_{B^{+}}")
hist3D.GetXaxis().SetTitleOffset(2.)
hist3D.GetYaxis().SetTitleOffset(2.)
hist3D.SetTitle("Reduced #chi^{2}_{ppK} vs Reduced #chi^{2}_{B^{+}} ")

pad3.cd()
pad3.SetBottomMargin(0.15)
tin.Draw("(B_plus_ENDVERTEX_CHI2/B_plus_ENDVERTEX_NDOF)>>projx(100, -2, 10")
projx.SetFillStyle(3005)
projx.SetFillColor(kBlue)
projx.SetLineColor(kBlue)
projx.Draw("HIST")
projx.SetTitle("Reduced #chi^{2}_{B^{+}}")

pad2.cd()
pad2.SetBottomMargin(0.15)
tin.Draw("(K_1_plus_ENDVERTEX_CHI2/K_1_plus_ENDVERTEX_NDOF)>>projy(100, -2, 10)")
projy.SetFillStyle(3005)
projy.SetFillColor(kRed)
projy.SetLineColor(kRed)
projy.Draw("HIST")
projy.SetTitle("Reduced #chi^{2}_{ppK}")

c1.SaveAs(path_destination+"chi2red_compare.pdf")

