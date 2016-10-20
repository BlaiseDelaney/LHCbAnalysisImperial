from ROOT import *
from math import log, acos
### Defining TMVA factory
##############################
fin = TFile('/vols/lhcb/palvare1/B2pphgamma/BDT/training_samples.root')
t_sig = fin.Get("SignalTree") 

#t_bkg = fdata.Get('BkgTree')
fsampled = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/B_training_sampled.root')
t_bkg = fsampled.Get('DecayTree')

B_nentries = t_bkg.GetEntries()
S_nentries = t_sig.GetEntries()
print B_nentries, S_nentries


t_bkg.SetBranchStatus("*",0)
t_bkg.SetBranchStatus("gamma_PT",1)
t_bkg.SetBranchStatus("Kplus_IPCHI2_OWNPV",1)
t_bkg.SetBranchStatus("B_plus_DIRA_OWNPV",1)
t_bkg.SetBranchStatus("B_plus_PT",1)
t_bkg.SetBranchStatus("K_1_plus_MM",1)
t_bkg.SetBranchStatus("K_1_plus_IPCHI2_OWNPV",1)
t_bkg.SetBranchStatus("pplus_IPCHI2_OWNPV",1)
t_bkg.SetBranchStatus("p~minus_IPCHI2_OWNPV",1)
t_bkg.SetBranchStatus("B_plus_IPCHI2_OWNPV",1)
t_bkg.SetBranchStatus("K_1_plus_ENDVERTEX_CHI2",1)

fout = TFile("trainingBDT.root","recreate")
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
factory.AddVariable("logKplus_IPCHI2_OWNPV:=log(Kplus_IPCHI2_OWNPV)", "F")
factory.AddVariable("logacosB_plus_DIRA_OWNPV:=log(acos(B_plus_DIRA_OWNPV))","F")
factory.AddVariable("logB_plus_PT:=log(B_plus_PT)","F")
factory.AddVariable("K_1_plus_MM","F")
factory.AddVariable("logK_1_plus_IPCHI2_OWNPV:=log(K_1_plus_IPCHI2_OWNPV)","F")
factory.AddVariable("logpplus_IPCHI2_OWNPV:=log(pplus_IPCHI2_OWNPV)", "F")
factory.AddVariable("logp~minus_IPCHI2_OWNPV:=log(p~minus_IPCHI2_OWNPV)", "F")
factory.AddVariable("logB_plus_IPCHI2_OWNPV:=log(B_plus_IPCHI2_OWNPV)","F")
factory.AddVariable("logK_1_plus_ENDVERTEX_CHI2:=log(K_1_plus_ENDVERTEX_CHI2)","F")


'''
factory.AddVariable("gamma_PT", "F")
factory.AddVariable("Kplus_IPCHI2_OWNPV", "F")
factory.AddVariable("B_plus_DIRA_OWNPV","F")
factory.AddVariable("B_plus_PT","F")
factory.AddVariable("K_1_plus_MM","F")
factory.AddVariable("K_1_plus_IPCHI2_OWNPV","F")
factory.AddVariable("pplus_IPCHI2_OWNPV", "F")
factory.AddVariable("p~minus_IPCHI2_OWNPV", "F")
factory.AddVariable("B_plus_IPCHI2_OWNPV","F")
factory.AddVariable("K_1_plus_ENDVERTEX_CHI2","F")
'''

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

                                   
                           
## Defining the classifiers to train
factory.BookMethod(TMVA.Types.kBDT, "BDT",
                            ":".join(["!H",
                                      "!V",
                                      "NTrees=300",
                                      "MaxDepth=4",
                                      "BoostType=AdaBoost",
                                      "AdaBoostBeta=0.3",
                                      "SeparationType=GiniIndex",
                                      "nCuts=-1",
                                      "PruneMethod=CostComplexity",
                                      "PruneStrength=-1"
                                      ]))


### Traingin and testing
##############################
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
