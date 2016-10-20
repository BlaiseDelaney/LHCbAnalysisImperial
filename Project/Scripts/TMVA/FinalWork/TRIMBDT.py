#!/usr/bin/env python
##VERSION WITH *CORRECT* MC sample

from ROOT import *
from decimal import *
import numpy as np
import matplotlib.pyplot as plt

#signal MC
f_sigMC = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/TMVA_MCcorrected.root')
t_sig_all = f_sigMC.Get('SignalTree') #truth-matched

##Test tree form BDT training
#BDTout = TFile("/vols/lhcb/bd1316/B2ppKgamma/TMVA/FINALcutsANA/lBDTfinal.root")
#Ttest = BDTout.Get("TestTree")  

##BDT evaluated high mass band
fBDT_bkg = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/FINALcutsANA/B2ppKgamma_bkg.root')
tBDT_bkg = fBDT_bkg.Get('DecayTree')


##BDT evaluated B2ppKgamma MC
fBDT_sig = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/FINALcutsANA/B2pppigammaMC_sig.root')
tBDT_sig = fBDT_sig.Get('DecayTree')

##BDT applied to data in B+ nominal mass interval (S + B)
Bdata = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/FINALCutOpt.root')
Btree = Bdata.Get('DecayTree')




##LHCb data
f_bkg_all = TFile("/vols/lhcb/palvare1/B2pphgamma/B2ppKgamma/B2pphgamma_S21_protonID.root")
t_bkg_all = f_bkg_all.Get("B2pphgamma_Tuple/DecayTree")

##Bkg sample, high mass band
f_bkg = TFile('/vols/lhcb/palvare1/B2pphgamma/BDT/training_samples.root')
t_bkg = f_bkg.Get('BkgTree')

##BDT cut values
nbins = 20
cutvals = np.linspace(-1., 1., nbins, dtype=float)
PIDvals = np.linspace(0, 50, nbins, dtype=int)

S_reconstructed=[]
B_reconstructed=[]

##Constants (LHCb)
##----------------
#bb_CrosSec = 1.09e-4 #b-bbar cross section, possibly value not up to date
luminosity = 3. #integrated luminosity 3 fb^(-1)  <------How to deal with units?
MC_events = 1000000.
B_plus_production = 44.5e+9
#B_hadronisation = 0.404 #hadronisation to B+, value probably wrong, to be checked after code is complete
B_frac = 1.e-6



##Extrapolating signal in B+ nominal mass interval
##------------------------------------------------
def calcSignal(cut_val, test_treeS, PIDval):
    #npassed =test_tree.GetEntries('classID==0. && BDT>=%f'%cut_val)#signal events in BDT output
    npassed =test_treeS.GetEntries('pplus_PIDp>=%f && p~minus_PIDp >= %f && BDT>=%f'%(PIDval,PIDval,cut_val))#sig events in BDT output
    #EffMC = float(npassed*2.)/float(MC_events)
    EffMC = float(npassed)/float(MC_events)
    Signal = float(2.*B_plus_production*luminosity*B_frac*EffMC)#multiply by 2 since TTest is 1/3 of the signal and background samples  ####INFER!!!!
    print "BDT output signal population = ", npassed
    print "Monte Carlo efficiency = %f"%EffMC
    print '\033[1;32mEXTRAPOLATED SIGNAL = %d\033[1;m'%Signal
    return Signal


##Extrapolating background in B+ nominal mass interval
##----------------------------------------------------
def calcBkg(cut_val, treeN1, treeN2, test_treeB, PIDval):    
    N1 = treeN1.GetEntries() #high mass band population
    N2 = treeN2.GetEntries('B_plus_MM > 5230 && B_plus_MM < 5330') #B+ interval population
    R = float(N2)/float(N1)
    #npassedB = Ttest.GetEntries('classID==1. && BDT>=%f'%cut_val)#bkg events in BDT output
    npassedB =test_treeB.GetEntries('pplus_PIDp>=%f && p~minus_PIDp>=%f && BDT>=%f'%(PIDval,PIDval,cut_val))#bkg events in BDT output
    HiMassB = npassedB
    print "BKG TtestTree is fraction of high-mass band B: %d (t_bkg population = %d)"%(HiMassB, t_bkg.GetEntries())
    BKG = HiMassB*R
    print '\033[1;36mEXTRAPOLATED BKG =%d\033[1;m'%BKG
    return BKG


##Find optimal cut
##----------------
FigMerits = [] 
for cut_value in cutvals:
    print '\033[1;35mCut Value = %f\033[1;m'%cut_value
    temp_fig = []
    tempS = []
    tempB = []
    for PIDvalue in PIDvals:
        print '\033[1;38mPID Value = %f\033[1;m'%PIDvalue

        S = calcSignal(cut_value, tBDT_sig, PIDvalue)
        print S
        B = calcBkg(cut_value, t_bkg, t_bkg_all, tBDT_bkg, PIDvalue)
        print B
        print "S+B = %d"%(S+B)
        print "LHCb data in interval 5280 +/- 50 MeV (B+ mass) = ", t_bkg_all.GetEntries('B_plus_MM > 5230 && B_plus_MM < 5330')#'B_plus_MM > 5000 && B_plus_MM < 6000')
        #S_reconstructed.append(S)
        #B_reconstructed.append(B)
        tempS.append(S)
        tempB.append(B)
        if float(np.sqrt(S+B)) != 0:
            #FigMerits.append(S/float(np.sqrt(S+B)))
            temp_fig.append(S/float(np.sqrt(S+B)))
            
        else:
            print "Warning: for cut value %f S or B are null, appending 0.0."%cut_value
            #FigMerits.append(0.0)
            temp_fig.append(0.0)
        print
    print temp_fig        
    print max(temp_fig)
    FigMerits.append(max(temp_fig))
    S_reconstructed.append(tempS[np.argmax(temp_fig)])
    B_reconstructed.append(tempB[np.argmax(temp_fig)])
    print 
    print 



print "++++++++++++++++++++++++++++++++++"
print "PRE_BDT STATS"

#npassed1 =Ttest.GetEntries('classID==0')
npassed1 =tBDT_sig.GetEntries()
print "Ttest S = %d, MC S sample (truthmateched!) = %d"%(npassed1, t_sig_all.GetEntries())
EffMC1 = float(npassed1)/float(MC_events)
Signal1 = float(2.*B_plus_production*luminosity*B_frac*EffMC1)
print "TOTAL RECTONSTRUCTED SIGNAL = ", Signal1

N21 = t_bkg_all.GetEntries('B_plus_MM > 5230 && B_plus_MM < 5330') #B+ interval population
N11 = t_bkg.GetEntries() #high mass band poulation
R1 = float(N21)/float(N11)
npassedB1 = tBDT_bkg.GetEntries()
print "Ttest B = %d, high-mass band population =%d"%(npassedB1, t_bkg.GetEntries()) 

BKG1 = float(npassedB1)*R1
print "TOTAL RECONSTRUCTED BKG = ", BKG1
print "++++++++++++++++++++++++++++++++++\n"



print FigMerits
opt_val = cutvals[np.argmax(FigMerits)]
opt_PID = PIDvals[np.argmax(FigMerits)]
opt_S_events = S_reconstructed[np.argmax(FigMerits)]
opt_B_events = B_reconstructed[np.argmax(FigMerits)]

print '\033[1;34mOptimal BDT cut: %f, PID value: %f, with %d signal events and %d bkg using S/sqrt(S+B) as figure of merit.\033[1;m'%(opt_val, opt_PID, opt_S_events, opt_B_events)
print "Average Signal Reconstr. = ", np.mean(S_reconstructed)
print "Average Background Reconstr. = ", np.mean(B_reconstructed)
'''
print 'B+ population',  Btree.GetEntries('B_plus_MM > 5230 && B_plus_MM < 5330')


## Selection example
cuts = {"proton_PIDp"  : 2,
        "proton_PIDpK" : 2,
        "Kaon_PIDK"    : 2,
        "Kaon_PIDpK"   : -2,
        "vertex_chi2_ndof" : 5,
        "bdt_cut_val" : opt_val
        }

selection = "pplus_PIDp>%(proton_PIDp)s && p~minus_PIDp>%(proton_PIDp)s"\
            "&& (pplus_PIDp - pplus_PIDK)>%(proton_PIDpK)s && (p~minus_PIDp - p~minus_PIDK)>%(proton_PIDpK)s"\
            "&& Kplus_PIDK>%(Kaon_PIDK)s && (Kplus_PIDp-Kplus_PIDK)<%(Kaon_PIDpK)s"\
            "&& (K_1_plus_ENDVERTEX_CHI2/K_1_plus_ENDVERTEX_NDOF)<%(vertex_chi2_ndof)s"\
            "&& BDT>=%(bdt_cut_val)s"%cuts


fout = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/FINALcutsANA/B2ppKgamma_trimmedMOCK.root', 'recreate')
tin  = Btree.CopyTree(selection)
tin.Write('DecayTree')

mp = 938.27
mk = 493.677
mpi = 139.57


## Making some plots
nbins = 100
h_ppKg_mass = TH1F("hppKg_mass","hppKg_mass",nbins,4900,6100)

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
    h_ppKg_mass.Fill((p_plus + p_minus + K_plus + gamma).M())



cv = TCanvas()
h_ppKg_mass.SetLineColor(kBlue)
#h_ppKg_mass.SetLineWidth(2)
#h_ppKg_mass.SetFillColor(kBlue-10)
#h_ppKg_mass.SetFillStyle(1001)
h_ppKg_mass.Draw()

cv.SaveAs('FINALTRIMMEDDATA.eps')
print 'B+ population',tin.GetEntries('B_plus_MM > 5230 && B_plus_MM < 5330')
'''

'''
##plots
##-----
plt1 = plt.figure()
plt.grid()

plt.xticks(np.arange(min(cutvals), max(cutvals), 0.2))
plt.plot(cutvals, FigMerits, 'k.')
plt.ylabel(r'S/sqrt(S+B)')
plt.xlabel(r'BDT cut value')


plt.axvline(opt_val, color='r', linestyle='dashed',label='Optimised cut @ %f'%opt_val)
legend = plt.legend(loc='best', shadow=False)


normS = [float(i)/sum(S_reconstructed) for i in S_reconstructed]
normB = [float(i)/sum(B_reconstructed) for i in B_reconstructed]

plt2 = plt.figure()
plt.grid()
plt.xticks(np.arange(min(cutvals), max(cutvals), 0.2))

plt.axvline(opt_val, color='r', linestyle='dashed',label='Optimised cut @ %f'%opt_val)
plt.plot(cutvals, normB, '-g', linewidth = 2.0, label = 'B')
plt.plot(cutvals, normS, '-b', linewidth = 2.0, label = 'S')
plt.xlabel(r'BDT cut value')
legend = plt.legend(loc='best', shadow=False)
plt.ylabel(r'Normalised reconstructed events')

#plt.show()
plt1.savefig('/home/hep/bd1316/public_html/TMVA/BDTcut_FifMerit.pdf') 
plt2.savefig('/home/hep/bd1316/public_html/TMVA/BDTcut_NormSBevents.pdf') 


cv = TCanvas()
Ttest.Draw("BDT>>hSig(100, -1., 1.)","classID == 0")  # signal
normS = hSig.GetEntries()
#hSig.Scale(1./normS)
#hSig.Draw()
Ttest.Draw("BDT","","same", "classID == 1")  # background
#normB = hBg.GetEntries()
#hBg.Scale(1./normB)
#hSig.SetLineColor(kRed); hSig.SetLineWidth(2)  # signal histogram
#hBg.SetLineColor(kBlue); hBg.SetLineWidth(2)   # background histogram
cv.Update()   
'''
