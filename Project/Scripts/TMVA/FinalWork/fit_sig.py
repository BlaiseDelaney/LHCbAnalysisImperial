from ROOT import *

fin = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/FINALcutsANA/B2ppKgamma_trimmedMOCK.root')
tin = fin.Get('DecayTree')
tin.SetBranchStatus("*",0)
tin.SetBranchStatus("B_plus_MM",1)
tin.SetBranchStatus("pplus_PX",1)
tin.SetBranchStatus("pplus_PY",1)
tin.SetBranchStatus("pplus_PZ",1)
tin.SetBranchStatus("nCandidate",1)
tin.SetBranchStatus("eventNumber",1)
tin.SetBranchStatus("runNumber",1)



tdata = tin.CloneTree(0)

p_plus = TLorentzVector()
p_minus = TLorentzVector() #pbar

mp = 938.27


IDs = []
counter_copy = 0
for i in tin:
    REn = str(i.runNumber)+str(i.eventNumber)

    p_plus.SetXYZM(i.pplus_PX, i.pplus_PY, i.pplus_PZ, mp)
    p_minus.SetXYZM(getattr(i,"p~minus_PX"), getattr(i,"p~minus_PY"), getattr(i,"p~minus_PZ"), mp)
    if ( (p_plus+p_minus).M()>(3096.916+50) or (p_plus + p_minus).M()<(3096.916-50) ):             
        if REn in IDs:
            counter_copy+=1
        if REn not in IDs:
            IDs.append(REn)
            tdata.Fill()

print counter_copy
print tdata.GetEntries()

## building the model
mass = RooRealVar("B_plus_MM","B_plus_MM",5100,6000)

c_exp = RooRealVar("#tau_{bkg}","Exp arg constant",-0.01,0)
BkgPDF = RooExponential("BkgPDF","BkgPDF",mass,c_exp)

B_mass = RooRealVar("#mu","#mu",5280,5280-50,5280+50)
B_width = RooRealVar("#sigma","#sigma",30,0,100)
SigPDF = RooGaussian("SigPDF","SigPDF",mass,B_mass,B_width)

NSig = RooRealVar("Signal yield","Signal yield",500, 0, 3000)
NBkg = RooRealVar("Bkg yield","Background yield",5000, 0, 3000000)

model = RooAddPdf("model","model",RooArgList(SigPDF,BkgPDF), RooArgList(NSig,NBkg))

## getting the data
data = RooDataSet("data","data",tdata,RooArgSet(mass))


## fitting
fitres = model.fitTo(data,RooFit.Extended(), RooFit.Save(1))


cv = TCanvas()
fr = mass.frame()
fr.SetTitle('#it{B}^{+}#rightarrow#it{K^{+}p#bar{p}#gamma}')
fr.SetTitleFont(12)
data.plotOn(fr)
model.plotOn(fr,RooFit.Components("BkgPDF"),RooFit.LineColor(kGreen),RooFit.LineStyle(kDashed))
model.plotOn(fr,RooFit.Components("SigPDF"),RooFit.LineColor(kRed),RooFit.LineStyle(kDashed))
model.plotOn(fr)
fr.GetXaxis().SetTitle("M(#it{K^{+}p#bar{p}#gamma}) (MeV/c^{2})")
fr.GetXaxis().SetTitleFont(42)

model.paramOn(fr,RooFit.Layout(0.55, 0.89, 0.85))
fr.getAttText().SetTextFont(132)

fr.Draw()
print 'Signal yield = %d'%NSig.getVal()
print 'Background yield = %d'%NBkg.getVal()
params = model.getComponents()
sig = params.find('SigPDF')
sigVars = sig.getVariables()
sigVars.Print('v')

cv.SaveAs('/home/hep/bd1316/public_html/Fit_B2ppKgamma.pdf')
cv.SaveAs('/home/hep/bd1316/public_html/Fit_B2ppKgamma.eps')

