from ROOT import *
import array
from math import log, acos

reader = TMVA.Reader()

Var_names = ['loggamma_PT','logKplus_IPCHI2_OWNPV','logacosB_plus_DIRA_OWNPV','logB_plus_PT','K_1_plus_MM','logK_1_plus_IPCHI2_OWNPV','logpplus_IPCHI2_OWNPV','logp~minus_IPCHI2_OWNPV','logB_plus_IPCHI2_OWNPV','logK_1_plus_ENDVERTEX_CHI2']

Vars = {}
for varname in Var_names: Vars[varname] = array.array('f',[0])

reader.AddVariable("loggamma_PT:=log(gamma_PT)",Vars['loggamma_PT'])
reader.AddVariable("logKplus_IPCHI2_OWNPV:=log(Kplus_IPCHI2_OWNPV)",Vars['logKplus_IPCHI2_OWNPV'])
reader.AddVariable("logacosB_plus_DIRA_OWNPV:=log(acos(B_plus_DIRA_OWNPV))",Vars['logacosB_plus_DIRA_OWNPV'])
reader.AddVariable("logB_plus_PT:=log(B_plus_PT)",Vars['logB_plus_PT'])
reader.AddVariable("K_1_plus_MM",Vars['K_1_plus_MM'])
reader.AddVariable("logK_1_plus_IPCHI2_OWNPV:=log(K_1_plus_IPCHI2_OWNPV)",Vars['logK_1_plus_IPCHI2_OWNPV'])
reader.AddVariable("logpplus_IPCHI2_OWNPV:=log(pplus_IPCHI2_OWNPV)",Vars['logpplus_IPCHI2_OWNPV'])
reader.AddVariable("logp~minus_IPCHI2_OWNPV:=log(p~minus_IPCHI2_OWNPV)",Vars['logp~minus_IPCHI2_OWNPV'])
reader.AddVariable("logB_plus_IPCHI2_OWNPV:=log(B_plus_IPCHI2_OWNPV)",Vars['logB_plus_IPCHI2_OWNPV'])
reader.AddVariable("logK_1_plus_ENDVERTEX_CHI2:=log(K_1_plus_ENDVERTEX_CHI2)",Vars['logK_1_plus_ENDVERTEX_CHI2'])



reader.BookMVA("BDT","weights/MyClassification_BDT.weights.xml")


fin = TFile("mergedSb.root")#W/O cuts applied so B_plus_MM between 5000 and 5000 MeV and (pplus+p~minus).M() not in range of J/psi mass +/- 100 MeV
tin= fin.Get("DecayTree")
print type(tin)
tin.GetEntries()

BDT = array.array('f',[0])

fout = TFile('CheckBDTVals.root',"RECREATE")
tout = tin.CopyTree('0')
tout.Branch('BDT', BDT,'BDT/F')

N = tin.GetEntries()
     
for n in range(N):
    if n%1000 == 1:
        print "Applying:   "+str(n) +' of '+str(N) +' events evaluated.'
    tin.GetEntry(n)

    Vars['loggamma_PT'][0] = log(getattr(tin, 'gamma_PT'))
    Vars['logKplus_IPCHI2_OWNPV'][0] = log(getattr(tin, 'Kplus_IPCHI2_OWNPV'))
    Vars['logacosB_plus_DIRA_OWNPV'][0] = log(acos(getattr(tin, 'B_plus_DIRA_OWNPV')))
    Vars['logB_plus_PT'][0] = log(getattr(tin, 'B_plus_PT'))
    Vars['K_1_plus_MM'][0] = getattr(tin, 'K_1_plus_MM')
    Vars['logK_1_plus_IPCHI2_OWNPV'][0] = log(getattr(tin, 'K_1_plus_IPCHI2_OWNPV'))
    Vars['logpplus_IPCHI2_OWNPV'][0] = log(getattr(tin, 'pplus_IPCHI2_OWNPV'))
    Vars['logp~minus_IPCHI2_OWNPV'][0] = log(getattr(tin, 'p~minus_IPCHI2_OWNPV'))
    Vars['logB_plus_IPCHI2_OWNPV'][0] = log(getattr(tin, 'B_plus_IPCHI2_OWNPV'))
    Vars['logK_1_plus_ENDVERTEX_CHI2'][0] = log(getattr(tin, 'K_1_plus_ENDVERTEX_CHI2'))
    
    BDT[0] = reader.EvaluateMVA('BDT')
    tout.Fill()
     
fout.Write("", TObject.kOverwrite)

print tout.GetEntries()
fout.Close()
