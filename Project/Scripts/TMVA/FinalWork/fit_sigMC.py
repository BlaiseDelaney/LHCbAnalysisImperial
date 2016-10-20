from ROOT import *
fMC = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/TMVA_MCcorrected.root')
tMC = fMC.Get('SignalTree')


## building the model
mass = RooRealVar("B_plus_MM","B_plus_MM",5100,6000)


B_mass = RooRealVar("B_mass","B_mass",5280,5280-50,5280+50)
B_width = RooRealVar("B_width","B_width",30,0,100)

SigPDF = RooGaussian("SigPDF","SigPDF",mass,B_mass,B_width)

NSig = RooRealVar("NSig","NSig",500, 0, 3000)


## getting the data
data = RooDataSet("data","data",tMC,RooArgSet(mass))


## fitting
mass.setRange("signal", 5230, 5330)
fitresS = SigPDF.fitTo(data, RooFit.Range("signal"), RooFit.Save(1))


cv = TCanvas()
fr = mass.frame()
fr.SetTitle('#it{B}^{+}#rightarrow#it{K^{+}p#bar{p}#gamma}')
fr.SetTitleFont(12)
data.plotOn(fr)
SigPDF.plotOn(fr)
B_mass.setVal(5262.87)
B_width.setVal(44.2603)
SigPDF.plotOn(fr)


fr.GetXaxis().SetTitle("M(#it{p#bar{p}K^{+}#gamma}) (MeV/c^{2})")
fr.GetXaxis().SetTitleFont(42)
fr.Draw()


pars = SigPDF.getVariables()
pars.Print('v')
