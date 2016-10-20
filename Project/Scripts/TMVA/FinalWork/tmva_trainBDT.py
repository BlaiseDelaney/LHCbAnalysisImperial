from ROOT import *
from math import log, acos

'''
### Creating training samples
##############################
f_sig = TFile("/vols/lhcb/palvare1/B2pphgamma/B2ppKgamma_MC/B2pphgamma_S21_v2.root")
t_sig_all = f_sig.Get("B2ppKgamma_Tuple/DecayTree")

f_bkg = TFile("/vols/lhcb/palvare1/B2pphgamma/B2ppKgamma/B2pphgamma_S21_protonID.root")
t_bkg_all = f_bkg.Get("B2pphgamma_Tuple/DecayTree")
fout = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/TMVA_MCcorrected.root','recreate')
fout.cd()
t_sig = t_sig_all.CopyTree("B_plus_BKGCAT<55") ## Truthmatching of the MC
t_sig.Write("SignalTree")
t_bkg = t_bkg_all.CopyTree("B_plus_MM>6000 && B_plus_MM<7000") ## Higher mass sideband 
t_bkg.Write("BkgTree")
'''



### Defining TMVA factory
##############################
#fdata = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/TMVA_MCcorrected.root')

#t_bkg = fdata.Get("BkgTree")
#t_sig = fdata.Get('SignalTree')

#fsampled = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/B_training_sampledUpdated.root')
#t_bkg = fsampled.Get('DecayTree')


fbkg = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/JointSamples/highMassBand.root')
t_bkg = fbkg.Get('DecayTree')
fsig = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/JointSamples/B2pppigammaMC_truthmatched.root')
t_sig = fsig.Get('DecayTree')

print type(t_sig)
print t_sig.GetEntries('piplus_IPCHI2_OWNPV')

B_nentries = t_bkg.GetEntries()
S_nentries = t_sig.GetEntries()



t_bkg.SetBranchStatus("*",0)
t_bkg.SetBranchStatus("gamma_PT",1)
t_bkg.SetBranchStatus("piplus_IPCHI2_OWNPV",1)
t_bkg.SetBranchStatus("B_plus_DIRA_OWNPV",1)
t_bkg.SetBranchStatus("B_plus_PT",1)
t_bkg.SetBranchStatus("K_1_plus_MM",1)
t_bkg.SetBranchStatus("K_1_plus_IPCHI2_OWNPV",1)
t_bkg.SetBranchStatus("pplus_IPCHI2_OWNPV",1)
t_bkg.SetBranchStatus("p~minus_IPCHI2_OWNPV",1)
t_bkg.SetBranchStatus("B_plus_IPCHI2_OWNPV",1)
t_bkg.SetBranchStatus("K_1_plus_ENDVERTEX_CHI2",1)
t_bkg.SetBranchStatus("pplus_PIDp",1)
t_bkg.SetBranchStatus("p~minus_PIDp",1)

fout = TFile("/vols/lhcb/bd1316/B2ppKgamma/TMVA/FINALcutsANA/lBDTfinal_B2pppigamma.root","recreate")
TMVA.Tools.Instance()

factory = TMVA.Factory('MyClassification', fout,
                            ":".join([
                                    "!V",
                                    "!Silent",
                                    "Color",
                                    "DrawProgressBar",
                                    "Transformations=I;D;P;G,D",
                                    "AnalysisType=Classification"]))
                                
factory.AddVariable("loggamma_PT:=log(gamma_PT)", "F")
factory.AddVariable("logpiplus_IPCHI2_OWNPV:=log(piplus_IPCHI2_OWNPV)", "F")
factory.AddVariable("logacosB_plus_DIRA_OWNPV:=log(acos(B_plus_DIRA_OWNPV))","F")
factory.AddVariable("logB_plus_PT:=log(B_plus_PT)","F")
factory.AddVariable("K_1_plus_MM","F")
factory.AddVariable("logK_1_plus_IPCHI2_OWNPV:=log(K_1_plus_IPCHI2_OWNPV)","F")
factory.AddVariable("logpplus_IPCHI2_OWNPV:=log(pplus_IPCHI2_OWNPV)", "F")
factory.AddVariable("logp~minus_IPCHI2_OWNPV:=log(p~minus_IPCHI2_OWNPV)", "F")
factory.AddVariable("logB_plus_IPCHI2_OWNPV:=log(B_plus_IPCHI2_OWNPV)","F")
factory.AddVariable("logK_1_plus_ENDVERTEX_CHI2:=log(K_1_plus_ENDVERTEX_CHI2)","F")
factory.AddVariable("p~minus","F")
factory.AddVariable("pplus_PIDp","F")



factory.AddSignalTree(t_sig)
factory.AddBackgroundTree(t_bkg)

# cuts
Cut = TCut("1") 

#prepare for training and testing
factory.PrepareTrainingAndTestTree(Cut,
                                   ":".join(["nTrain_Signal=0",
                                             "nTrain_Background=0",
                                             "nTest_Signal=0",
                                             "nTest_Background=0",
                                             "SplitMode=Random",
                                             "SplitSeed=0",
                                             "NormMode=NumEvents",
                                             "!V"]))

                                   
                           
## defining the classifiers to train
factory.BookMethod(TMVA.Types.kBDT, "BDT_B2pppigamma",
                            ":".join(["!h",
                                      "!v",
                                      "ntrees=300",
                                      "maxdepth=4",
                                      "boosttype=AdaBoost",
                                      "adaboostbeta=0.3",
                                      "separationtype=GiniIndex",
                                      "ncuts=-1",
                                      "prunemethod=CostComplexity",
                                      "prunestrength=-1"
                                      ]))


## Defining the classifiers to trai
### Traingin and testing
##############################
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

print "Sample Entries = %d, %d (S and B)"%(S_nentries, B_nentries)
