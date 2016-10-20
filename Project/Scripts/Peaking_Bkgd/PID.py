from ROOT import *
from math import *

path_origin = "/vols/lhcb/palvare1/B2pphgamma/B2ppKgamma/"

#path_destination = "./home/hep/bd1316/Public/Project/MC/B2pppi/"

fname = "B2pphgamma_S21_protonID" 
fin = TFile(path_origin+fname+".root")
tin = fin.Get("B2pphgamma_Tuple/DecayTree")

cv = TCanvas()
#cv.Divide(2,3)

#cv.cd(1)
tin.Draw("(K_1_plus_ENDVERTEX_CHI2/K_1_plus_ENDVERTEX_NDOF)>>h1(100, -20, 20)")
tin.SetLineColor(1)
#cv.Update()
'''
cv.cd(2)
tin.Draw("(p~minus_PIDp)>>h2(100, -200, 200")
tin.SetLineColor(2)
cv.Update()

cv.cd(3)
tin.Draw("(pplus_PIDp - pplus_PIDK)>>h3(100, -200, 200)")
tin.SetLineColor(3)
cv.Update()

cv.cd(4)
tin.Draw("(p~minus_PIDp - p~minus_PIDK)>>h4(100, -200, 200)")
tin.SetLineColor(4)
cv.Update()

cv.cd(5)
tin.Draw("(piplus_PIDK)>>h5(100, -200, 200)")
tin.SetLineColor(5)
cv.Update()

cv.cd(6)
tin.Draw("(piplus_PIDp)>>h6(100, -100, 200)")
tin.SetLineColor(6)
cv.Update()

cv2 = TCanvas()
tin.Draw("(B_plus_ENDVERTEX_CHI2/B_plus_ENDVERTEX_NDOF)>>h7(100, -50, 50)")
tin.SetLineColor(7)


'''
