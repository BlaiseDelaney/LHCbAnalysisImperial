from ROOT import *

#Ftotal = TFile('/vols/lhcb/palvare1/B2pphgamma/B2ppKgamma/B2pphgamma_S21_protonID.root')
#Ftotal = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/B_training_sampled.root')
#Ftotal = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/FINALrc_OUT.root')
#Ftotal = TFile("/vols/lhcb/bd1316/B2ppKgamma/TMVA/readerBDT_noJPsicut_final.root")
#Ttotal = Ftotal.Get('B2pphgamma_Tuple/DecayTree')
#Ttotal = Ftotal.Get('DecayTree')
fin = TFile('/vols/lhcb/bd1316/B2ppKgamma/TMVA/FINALcutsANA/B2ppKgamma_trimmedMOCK.root')
tin= fin.Get("DecayTree")

tin.SetBranchStatus("*",0)
tin.SetBranchStatus("runNumber",1)
tin.SetBranchStatus("eventNumber",1)

eventList=[]
nplicates = []



N = tin.GetEntries()
print N

container = []

k = 0
for i in tin:
    if k%1000 == 1:
        print "Looking at:   "+str(k) +' of '+str(N) +' events evaluated.'
  
    ientry = str(i.eventNumber)+str(i.runNumber)    
    container.append(ientry)


print len(container)

copies = []
IDs = []
for entry in container:
    copy_counter = 0
    print entry
    print copy_counter
    if entry in IDs:
        copy_counter +=1
        print "copy! %s"%entry
    if entry not in IDs:
        print 'new item'
        IDs.append(entry)
    if copy_counter != 0:
        print 'check (copy + 1), %d'%(copy_counter+1)
        copies.append(copy_counter+1)
    print

print copies
print len(copies)


temp = []
temp_cp = []
originals = []
s = 0
for item in container:
    l = 0
    original = 0
    if item in temp:
        s +=1
        l += 1
    if item not in temp:
        original += 1
        originals.append(original)
        temp.append(item)
    temp_cp.append(l)
#print 'check copies (see if numbers are consistent), s = ', s
#print temp_cp
#
print len(originals)
print s 
print tin.GetEntries() - len(originals)
