The files Lambda_c_KpPi_enhancedBKD.pdf and Lambda_c_EnhancedBkd_pipK.pdf were
created with the intention of enhancing the background of the midID's, thus 
enhancing our study of potential Lambda_c decays in the peaking background.

Specifically, for Lambda_c_EnhancedBkd_pipK.pdf: 

        p pbar K -> pi- pbar K+:
                cuts = {"proton_PIDp"  : 5,
                        "proton_PIDpminus" : 2,>
                        "proton_PIDpK" : 2,
                        "Kaon_PIDK"    : 2,
                        "Kaon_PIDpK"   : -1, 
                        "vertex_chi2_ndof" : 5,
                        }

                selection = "pplus_PIDp<%(proton_PIDp)s && p~minus_PIDp>%(proton_PIDpminus)s"\
                        "&& (p~minus_PIDp - p~minus_PIDK)>%(proton_PIDpK)s"\
                        "&& Kplus_PIDK>%(Kaon_PIDK)s"\
                        "&& (Kplus_PIDp - Kplus_PIDK)<%(Kaon_PIDpK)s"\
                        "&& (K_1_plus_ENDVERTEX_CHI2/K_1_plus_ENDVERTEX_NDOF)<%(vertex_chi2_ndof)s"%cuts i


For Lambda_c_KpPi_enchancedBKD.pdf:

        p pbar K -> K+ pbar pi-:
                cuts = {"proton_PIDp"  : 5,
                        "proton_PIDpminus" : 2,
                        "proton_PIDpK" : 2,
                        "Kaon_PIDK"    : 5,
                        "Kaon_PIDpK"   : -1, 
                        "vertex_chi2_ndof" : 5,
                        }

                selection = "pplus_PIDp<%(proton_PIDp)s && p~minus_PIDp>%(proton_PIDpminus)s"\
                        "&& (p~minus_PIDp - p~minus_PIDK)>%(proton_PIDpK)s"\
                        "&& Kplus_PIDK<%(Kaon_PIDK)s"\
                        "&& (K_1_plus_ENDVERTEX_CHI2/K_1_plus_ENDVERTEX_NDOF)<%(vertex_chi2_ndof)s"%cuts



The other two .pdf files were created previously, with loose(r, compared to first attempt) PID cuts 
and no enhanced BKD to correctly associate each track with the (isolated, PID-selected) corresponding 
midID.


The following files were produced using the criteria of the first two scripts, except the tolerance on PID cut 
for K_1_plus reduced chi2 is pushed to 9:
    -Lambda_c_KpPi_enhancedBKD_badlyvertexed.pdf
    -Lambda_c_EnhancedBkd_pipK_badlyvertexed.pdf
