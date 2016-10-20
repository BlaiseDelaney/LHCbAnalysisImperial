from ROOT import *

fin = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/FINALcutsANA/B2ppKgamma_trimmedMOCK.root')
tin= fin.Get("DecayTree")
tin_entries = tin.GetEntries()

cv = TCanvas()
print "Original ttree has %d entries"%tin_entries

fout = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/FINALcutsANA/JPsiInTrimmed.root','recreate')
t_data = tin.CloneTree(0)
p_plus = TLorentzVector()
p_minus = TLorentzVector() #pbar

mp = 938.27

#JPsi->p ppbar
for i in tin:
        
        p_plus.SetXYZM(i.pplus_PX, i.pplus_PY, i.pplus_PZ, mp)
        p_minus.SetXYZM(getattr(i,"p~minus_PX"), getattr(i,"p~minus_PY"), getattr(i,"p~minus_PZ"), mp)
        
        if ( (p_plus+p_minus).M()>3071.916 and (p_plus + p_minus).M()<3121.916 ):             
           t_data.Fill()

t_data.Write('DecayTree')





Noutentries = t_data.GetEntries()
print "Outfile has a tree with %d entries"%Noutentries



## Selection example
cuts = {"proton_PIDp"  : 2,
        "proton_PIDpK" : 2,
        "Kaon_PIDK"    : 2,
        "Kaon_PIDpK"   : -2,
        "vertex_chi2_ndof" : 5,
        }

selection = "pplus_PIDp>%(proton_PIDp)s && p~minus_PIDp>%(proton_PIDp)s"\
            "&& (pplus_PIDp - pplus_PIDK)>%(proton_PIDpK)s && (p~minus_PIDp - p~minus_PIDK)>%(proton_PIDpK)s"\
            "&& Kplus_PIDK>%(Kaon_PIDK)s && (Kplus_PIDp-Kplus_PIDK)<%(Kaon_PIDpK)s"\
            "&& (K_1_plus_ENDVERTEX_CHI2/K_1_plus_ENDVERTEX_NDOF)<%(vertex_chi2_ndof)s"%cuts



mp = 938.27
mk = 493.677
mpi = 139.57


## Making some plots
nbins = 100
h_ppKg_mass = TH1F("hpp","hpp",nbins,5000,6000)

p_plus = TLorentzVector()
p_minus = TLorentzVector()
K_plus = TLorentzVector()
gamma = TLorentzVector()

for i in t_data:

    p_plus.SetXYZM(i.pplus_PX, i.pplus_PY, i.pplus_PZ, mp)
    p_minus.SetXYZM(getattr(i,"p~minus_PX"), getattr(i,"p~minus_PY"), getattr(i,"p~minus_PZ"), mp)
    K_plus.SetXYZM(i.Kplus_PX, i.Kplus_PY, i.Kplus_PZ, mk)
    gamma.SetXYZM(i.gamma_PX, i.gamma_PY, i.gamma_PZ, 0.)

    ## Mass ppKgamma
    h_ppKg_mass.Fill((p_plus + p_minus + K_plus + gamma).M())



h_ppKg_mass.SetLineColor(kRed)
h_ppKg_mass.SetLineWidth(1)
#h_ppKg_mass.SetFillColor(kRed-10)

#h_ppKg_mass.SetFillStyle(1001)

h_ppKg_mass_original = TH1F("hppKg_mass_original","hppKg_mass_original",nbins,5000,6000)

p_plus = TLorentzVector()
p_minus = TLorentzVector()
K_plus = TLorentzVector()
gamma = TLorentzVector()

for i in tin:

    p_plus.SetXYZM(i.pplus_PX, i.pplus_PY, i.pplus_PZ, mp)
    p_minus.SetXYZM(getattr(i,"p~minus_PX"), getattr(i,"p~minus_PY"), getattr(i,"p~minus_PZ"), mp)
    K_plus.SetXYZM(i.Kplus_PX, i.Kplus_PY, i.Kplus_PZ, mk)
    gamma.SetXYZM(i.gamma_PX, i.gamma_PY, i.gamma_PZ, 0.)

    ## Mass ppKgamma
    h_ppKg_mass_original.Fill((p_plus + p_minus + K_plus + gamma).M())



h_ppKg_mass_original.SetLineColor(kBlue)
h_ppKg_mass_original.SetLineWidth(1)
h_ppKg_mass_original.SetFillColor(kBlue-10)
h_ppKg_mass_original.SetFillStyle(1001)

h_pppig_mass = TH1F("hpppig_mass","hpppig_mass",nbins,5000,6000)
pi_plus = TLorentzVector()

for i in tin:

    p_plus.SetXYZM(i.pplus_PX, i.pplus_PY, i.pplus_PZ, mp)
    p_minus.SetXYZM(getattr(i,"p~minus_PX"), getattr(i,"p~minus_PY"), getattr(i,"p~minus_PZ"), mp)
    K_plus.SetXYZM(i.Kplus_PX, i.Kplus_PY, i.Kplus_PZ, mk)
    gamma.SetXYZM(i.gamma_PX, i.gamma_PY, i.gamma_PZ, 0.)

    pi_plus.SetXYZM(i.Kplus_PX, i.Kplus_PY, i.Kplus_PZ, mpi)
    h_pppig_mass.Fill((p_plus + p_minus + pi_plus + gamma).M())

h_pppig_mass.SetLineColor(kGreen+1)
h_pppig_mass.SetLineWidth(1)

hsi = THStack("hsi","")
hsi.Add(h_ppKg_mass_original)
hsi.Add(h_ppKg_mass)
hsi.Add(h_pppig_mass)
hsi.Draw('nostack')


legend=TLegend(0.6,0.6,0.88,0.8)
legend.AddEntry(h_ppKg_mass_original,'B^{+}#rightarrowp#bar{p}K^{+}#gamma' , "lf")
legend.AddEntry(h_ppKg_mass,'B^{+}#rightarrowp#bar{p}#pi^{+}#gamma' , "l")
legend.AddEntry(h_pppig_mass,'B^{+}#rightarrowJ/#psi(#rightarrowp#bar{p})K^{+}#gamma' , "l")
legend.SetTextFont(12)
legend.SetBorderSize(0)
legend.Draw()

hsi.GetXaxis().SetTitle("M(p#bar{p}K^{+}#gamma) (MeV/c^{2})")
hsi.GetYaxis().SetTitle("Candidates/(10 MeV/c^{2})")
hsi.GetYaxis().SetTitleFont(42)
hsi.GetXaxis().SetTitleFont(42)


cv.SaveAs('FINALTRIMMEDDATAnoJpsi.eps')


cv1 = TCanvas()
h_ppKg_mass.Add(h_pppig_mass, -1)
h_ppKg_mass.Draw()
cv1.SaveAs('S-PkgBkg.eps')
fout.Close()

