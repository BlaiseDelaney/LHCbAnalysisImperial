from ROOT import *

### Creating ML data
##############################
fin = TFile("/vols/lhcb/palvare1/B2pphgamma/B2ppKgamma/B2pphgamma_S21_protonID.root") # real data
tin= fin.Get("B2pphgamma_Tuple/DecayTree")

print tin.GetEntries('B_plus_MM > 4300 && B_plus_MM < 6750')



fout = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/MLforReaderNoJPsiCutOpt.root','recreate')
t_data = tin.CopyTree('B_plus_MM > 4300 && B_plus_MM < 6750')
t_data.Write('DecayTree')
print t_data.GetEntries()
'''


tin_entries = tin.GetEntries()
print "Original ttree has %d entries"%tin_entries

p_plus = TLorentzVector()
p_minus = TLorentzVector() #pbar

mp = 938.27


for i in tin:
        
        #p_plus.SetXYZM(i.pplus_PX, i.pplus_PY, i.pplus_PZ, mp)
        #p_minus.SetXYZM(getattr(i,"p~minus_PX"), getattr(i,"p~minus_PY"), getattr(i,"p~minus_PZ"), mp)
        
        #B+ mass range and remove the J/psi mass +/- 100 MeV
        if ( i.B_plus_MM>=5000 and i.B_plus_MM<=6000):
           #if ( (p_plus+p_minus).M()>3196.916 or (p_plus + p_minus).M()<2996.916 ):             
           t_data.Fill()


Noutentries = t_data.GetEntries()
print "Outfile has a tree with %d entries"%Noutentries



t_data.Write()
'''
