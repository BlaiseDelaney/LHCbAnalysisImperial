from ROOT import *
import array
from math import log, acos

reader = TMVA.Reader()

Var_names = ['gamma_PT','Kplus_IPCHI2_OWNPV','B_plus_DIRA_OWNPV','B_plus_PT','K_1_plus_MM','K_1_plus_IPCHI2_OWNPV','pplus_IPCHI2_OWNPV','p~minus_IPCHI2_OWNPV','B_plus_IPCHI2_OWNPV','K_1_plus_ENDVERTEX_CHI2']

Vars = {}
for varname in Var_names: Vars[varname] = array.array('f',[0])

reader.AddVariable("loggamma_PT:=log(gamma_PT)",Vars['gamma_PT'])
reader.AddVariable("logKplus_IPCHI2_OWNPV:=log(Kplus_IPCHI2_OWNPV)",Vars['Kplus_IPCHI2_OWNPV'])
reader.AddVariable("logacosB_plus_DIRA_OWNPV:=log(acos(B_plus_DIRA_OWNPV))",Vars['B_plus_DIRA_OWNPV'])
reader.AddVariable("logB_plus_PT:=log(B_plus_PT)",Vars['B_plus_PT'])
reader.AddVariable("K_1_plus_MM",Vars['K_1_plus_MM'])
reader.AddVariable("logK_1_plus_IPCHI2_OWNPV:=log(K_1_plus_IPCHI2_OWNPV)",Vars['K_1_plus_IPCHI2_OWNPV'])
reader.AddVariable("logpplus_IPCHI2_OWNPV:=log(pplus_IPCHI2_OWNPV)",Vars['pplus_IPCHI2_OWNPV'])
reader.AddVariable("logp~minus_IPCHI2_OWNPV:=log(p~minus_IPCHI2_OWNPV)",Vars['p~minus_IPCHI2_OWNPV'])
reader.AddVariable("logB_plus_IPCHI2_OWNPV:=log(B_plus_IPCHI2_OWNPV)",Vars['B_plus_IPCHI2_OWNPV'])
reader.AddVariable("logK_1_plus_ENDVERTEX_CHI2:=log(K_1_plus_ENDVERTEX_CHI2)",Vars['K_1_plus_ENDVERTEX_CHI2'])


#reader.BookMVA("BDT_tuned","weights/MyClassification_BDT_checkreader.weights.xml")
reader.BookMVA("BDT","weights/MyClassification_BDT_tuned.weights.xml")


fin = TFile("/vols/lhcb/bd1316/B2ppKgamma/TMVA/MLforReaderNoJPsiCutOpt.root")#W/O cuts applied so B_plus_MM between 5000 and 5000 MeV and (pplus+p~minus).M() not in range of J/psi mass +/- 100 MeV
tin= fin.Get("DecayTree")
tin.GetEntries()

BDT = array.array('f',[0])

fout = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/FINAL_reader.root',"RECREATE")
tout = tin.CopyTree('0')
tout.Branch('BDT', BDT,'BDT/F')

N = tin.GetEntries()
     
for n in range(N):
    if n%1000 == 1:
        print "Applying:   "+str(n) +' of '+str(N) +' events evaluated.'
    tin.GetEntry(n)

    for varname in Var_names: Vars[varname][0] = getattr(tin,varname)
    
    BDT[0] = reader.EvaluateMVA('BDT')
    tout.Fill()
     
fout.Write("", TObject.kOverwrite)

print tout.GetEntries()
fout.Close()
