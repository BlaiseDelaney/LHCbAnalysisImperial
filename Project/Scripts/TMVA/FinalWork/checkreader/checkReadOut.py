from ROOT import *

fin = TFile('trainingBDT.root')
tinTest = fin.Get('TestTree')
tinTrain = fin.Get('TrainTree')

print type(tinTest), type(tinTrain)

cv = TCanvas()
cv.Divide(3,2)
cv.cd(1)

tinTest.Draw('BDT>>htest(100, -1., 1.)')
tinTrain.Draw('BDT>>htrain(100, -1., 1.)')

htest.SetLineColor(kRed)
htrain.SetLineWidth(kBlue)
htest.SetLineWidth(2)
htrain.SetLineWidth(2)

hs = THStack("hs","")
hs.Add(htest)
hs.Add(htrain)
  
hs.Draw()


cv.cd(2)
fReader = TFile('CheckBDTVals.root')
tReader = fReader.Get('DecayTree')

tReader.Draw('BDT>>hread(100, -1., 1.)')

cv.cd(3)

tinTest.Draw('BDT>>test(100, -1., 1.)')
test.SetLineColor(kRed - 10)

cv.cd(4)
tinTest.Draw('BDT>>train(100, -1., 1.)')
train.SetLineColor(kBlue - 10)

cv.cd(5)
tinTrain.Draw('BDT>>htrainonverse(100, -1., 1.)')
tinTest.Draw('BDT>>htestinverse(100, -1., 1.)')

htestinverse.SetLineColor(kRed)
htrainonverse.SetLineWidth(kBlue)
htestinverse.SetLineWidth(2)
htrainonverse.SetLineWidth(2)

hsinverse = THStack("hs","")
hsinverse.Add(htrainonverse)
hsinverse.Add(htestinverse)
  
hsinverse.Draw()

cv.cd(6)
tinTrain.Draw('BDT>>htt(100, -1., 1.)')
tinTest.Draw('BDT>>htr(100, -1., 1.)')

htt.SetLineColor(kRed)
htr.SetLineWidth(kBlue)




tReader.Draw('BDT>>hreadf(100, -1., 1.)')
#hreadf.SetLineColor('kGreen')
hreadf.SetFillColor(kGreen)
hreadf.SetFillStyle(3004)

hsi = THStack("hsi","")
hsi.Add(htt)
hsi.Add(htr)
hsi.Draw()
hsi.Add(hreadf)  
hsi.Draw('nostack')


cv.SaveAs('ReadOut.pdf')
