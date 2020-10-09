# -*- coding: utf-8 -*-

import maya.cmds as cm
import maya.mel as ml
import os

def show_ui():
    if cm.window('Auxiliary', ex=True):
        cm.deleteUI('Auxiliary')
    cm.window('Auxiliary', title="FaceAuxiliary_Tool", wh=(1000, 500))
    Fl = cm.formLayout("Fl")
    #--------------------
    Frl = cm.frameLayout("Frl", label="Eyebrow set", p=Fl)
    TfbGrp = cm.textFieldButtonGrp('Tfbg', l='Location selection line:', bl=">>>Get<<<", bc="Brow_get()", adj=2, editable=False)
    IsGrp01 = cm.intSliderGrp('IsGrp01', field=True, label='Secondary Number：', minValue=5, maxValue=60, value=1)
    IsGrp02 = cm.intSliderGrp('IsGrp02', field=True, label='Tweak Number：', minValue=9, maxValue=100, value=1)
    #--------------------
    Efrl = cm.frameLayout("Efrl", label="Eyelid set", p=Fl)
    EtfbGrp = cm.textFieldButtonGrp('Etfbg', l='Location selection line:', bl=">>>Getします<<<", bc="Eyelid_get()", adj=2, editable=False)
    EisGrp01 = cm.intSliderGrp('EisGrp01', field=True, label='Secondary Number：', minValue=8, maxValue=60, value=1)
    
    #-------------------
    Cfrl = cm.frameLayout("Cfrl", label="Cheek set", p=Fl)
    CtfbGrp = cm.textFieldButtonGrp('Ctfbg', l='Location selection UP line:', bl=">>>Get<<<", bc="Cheek_up_get()", adj=2, editable=False)
    CisGrp01 = cm.intSliderGrp('CisGrp01', field=True, label='Secondary Number：', minValue=3, maxValue=60, value=1)
    CtfbGrp02 = cm.textFieldButtonGrp('Ctfbg02', l='Location selection LOW line:', bl=">>>Get<<<", bc="Cheek_low_get()", adj=2, editable=False)
    CisGrp02 = cm.intSliderGrp('CisGrp02', field=True, label='Secondary Number：', minValue=5, maxValue=60, value=1)
    #-------------------
    Lfrl = cm.frameLayout("Lfrl", label="Lips set", p=Fl)
    LtfbGrp = cm.textFieldButtonGrp('Ltfbg', l='Location selection line:', bl=">>>Get<<<", bc="Lips_get()", adj=2, editable=False)
    #LisGrp01 = cm.intSliderGrp('LisGrp01', field=True, label='二次コントローラーの数：', minValue=8, maxValue=60, value=1)
    LisGrp02 = cm.intSliderGrp('LisGrp02', field=True, label='Secondary Number：', minValue=16, maxValue=100, value=1)
    bt = cm.button(label='Apply', c='Execute()')
    cm.formLayout(Fl, edit=True, attachForm=[(Frl, "top", 0), (Frl, "left", 0), (Frl, "right", 0),(Efrl, "top", 110), (Efrl, "left", 0), (Efrl, "right", 0),(Cfrl, "top",195), (Cfrl, "left", 0), (Cfrl, "right", 0),(Lfrl, "top",340), (Lfrl, "left", 0), (Lfrl, "right", 0)])
    cm.setParent("..")
    cm.showWindow('Auxiliary')
                

def Brow_get():
    # Sel=cm.ls(sl=True,fl=True)
    Sele = ml.eval('string $sel[]=`ls -sl -fl`;stringArrayToString($sel,\",\");')
    cm.textFieldButtonGrp(TfbGrp, e=True, tx=Sele)
def Eyelid_get():
    # Sel=cm.ls(sl=True,fl=True)
    Esele = ml.eval('string $sel[]=`ls -sl -fl`;stringArrayToString($sel,\",\");')
    cm.textFieldButtonGrp(EtfbGrp, e=True, tx=Esele)

def Cheek_up_get():
    # Sel=cm.ls(sl=True,fl=True)
    Csele_up = ml.eval('string $sel[]=`ls -sl -fl`;stringArrayToString($sel,\",\");')
    cm.textFieldButtonGrp(CtfbGrp, e=True, tx=Csele_up)
def Cheek_low_get():
    Csele_low= ml.eval('string $sel[]=`ls -sl -fl`;stringArrayToString($sel,\",\");')
    cm.textFieldButtonGrp(CtfbGrp02, e=True, tx=Csele_low)


def Lips_get():
    # Sel=cm.ls(sl=True,fl=True)
    Lsele = ml.eval('string $sel[]=`ls -sl -fl`;stringArrayToString($sel,\",\");')
    cm.textFieldButtonGrp(LtfbGrp, e=True, tx=Lsele)


def Execute():
    #Get information
    Info = cm.textFieldGrp(TfbGrp, q=True, tx=True)
    Sec = cm.intSliderGrp(IsGrp01, q=True, v=True)
    Tw = cm.intSliderGrp(IsGrp02, q=True, v=True)
    
    Einfo = cm.textFieldGrp(EtfbGrp, q=True, tx=True)
    Esec = cm.intSliderGrp(EisGrp01, q=True, v=True)
    
    Cinfo_up = cm.textFieldGrp(CtfbGrp, q=True, tx=True)
    Cinfo_low = cm.textFieldGrp(CtfbGrp02, q=True, tx=True)
    Csec_up = cm.intSliderGrp(CisGrp01, q=True, v=True)
    Csec_low = cm.intSliderGrp(CisGrp02, q=True, v=True)
   
    Linfo = cm.textFieldGrp(LtfbGrp, q=True, tx=True)
    #Lsec = cm.intSliderGrp(LisGrp01, q=True, v=True)
    Ltw = cm.intSliderGrp(LisGrp02, q=True, v=True)
    Lsk=[]
    Rsk=[]
    Elsk=[]
    Ersk=[]
    Clsk_up=[]
    Crsk_up=[]
    Csk_low=[]
    Llsk=[]
    
    #Eyebrow set
    if (len(Info)!=0):
        cm.select(Info.split(","))
        Cbr = cm.polyToCurve(form=2, degree=1, conformToSmoothMeshPreview=1, n="Brow_L_Cv")
        Lbr = cm.rebuildCurve(Cbr[0], ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=Tw - 1, d=3, tol=0.01)
        Rbr = cm.duplicate(Lbr[0], rr=True, n="Brow_R_Cv")
        cm.setAttr(Rbr[0] + ".sx", -1)
        cm.makeIdentity(apply=True, t=0, r=0, s=1, n=0, pn=1)
        # Sp=cm.getAttr(Br[0]+"Shape.s")
        cm.select(cl=True)
        for i in range(0, Tw):
            #Lwt = cm.xform(Lbr[0] + ".cv[" + str(i) + "]", ws=True, q=True, t=True)
            #Rwt = cm.xform(Rbr[0] + ".cv[" + str(i) + "]", ws=True, q=True, t=True)
            Ltc=cm.curve(d=1,p=[(-0.165186, 0.165186, 0.57),(0.165186, 0.165186, 0.57),(0.165186, -0.165186, 0.57),(-0.165186, -0.165186, 0.57),(-0.165186,0.165186,0.57),(-0.165186, 0.165186, -0.43),(0.165186, 0.165186, -0.43),( 0.165186, -0.165186, -0.43),(-0.165186, -0.165186, -0.43),(-0.165186, 0.165186, -0.43),(-0.165186, 0.165186, 0.57),(0.165186, 0.165186, 0.57),(0.165186, 0.165186, -0.43),(0.165186, -0.165186, -0.43),(0.165186, -0.165186, 0.57),(-0.165186, -0.165186, 0.57),(-0.165186, -0.165186, -0.43)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],n="brow_L0"+str(i)+"_tweakBrow_ctl")
            Ltcj = cm.joint(n="brow_L0" + str(i) + "_tweakBrow_ctrl_jnt")
            Ltnpo = cm.group(Ltc, n="brow_L0" + str(i) + "_tweakBrow_npo")
            cm.pathAnimation(Ltnpo,Lbr[0],fm=True,f=True, fa= "x", ua= "y", wut= "vector", wu=( 0, 1, 0), iu= False, inverseFront= False, b= False,stu=0,etu=100)
            cm.select(cl=True)
            Rtc=cm.curve(d=1,p=[(-0.165186, 0.165186, 0.57),(0.165186, 0.165186, 0.57),(0.165186, -0.165186, 0.57),(-0.165186, -0.165186, 0.57),(-0.165186,0.165186,0.57),(-0.165186, 0.165186, -0.43),(0.165186, 0.165186, -0.43),( 0.165186, -0.165186, -0.43),(-0.165186, -0.165186, -0.43),(-0.165186, 0.165186, -0.43),(-0.165186, 0.165186, 0.57),(0.165186, 0.165186, 0.57),(0.165186, 0.165186, -0.43),(0.165186, -0.165186, -0.43),(0.165186, -0.165186, 0.57),(-0.165186, -0.165186, 0.57),(-0.165186, -0.165186, -0.43)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],n="brow_R0"+str(i)+"_tweakBrow_ctl")
            Rtcj = cm.joint(n="brow_R0" + str(i) + "_ftweakBrow_ctrl_jnt")
            Rtnpo = cm.group(Rtc, n="brow_R0" + str(i) + "_tweakBrow_npo")
            cm.pathAnimation(Rtnpo,Rbr[0],fm=True,f=True, fa= "x", ua= "y", wut= "vector", wu=( 0, 1, 0), iu= False, inverseFront= False, b= False,stu=0,etu=100)
            cm.select(cl=True)
            Lmp=cm.listConnections(Ltnpo+".rx",s=True)
            cm.cutKey(Lmp[0],cl=True,at= "u")
            cm.setAttr(Lmp[0]+".uValue",i/(Tw-1.0))
            Rmp=cm.listConnections(Rtnpo+".rx",s=True)
            cm.cutKey(Rmp[0],cl=True,at= "u")
            cm.setAttr(Rmp[0]+".uValue",i/(Tw-1.0))
            cm.select(cl=True)
            if (i % 2 == 0) and (Sec):
                Lsc = cm.circle(c=(0, 0, 0), nr=(0, 0, 1), sw=360, r=0.5, d=3, ut=0, tol=0.01, s=8, ch=1,n="brow_L_sec_0" + str(i) + "_ctl")
                Lscj = cm.joint(n="brow_L_sec_0" + str(i) + "_jnt")
                Lbnpo = cm.group(Lsc[0], n="brow_L_sec_0" + str(i) + "_bufferNpo")
                Lnpo = cm.group(Lsc[0], n="brow_L_sec_0" + str(i) + "_npo")
                Lwt=cm.xform(Ltcj, ws=True, q=True, t=True)
                cm.setAttr(Lbnpo + ".t", Lwt[0], Lwt[1], Lwt[2])
                Lsk.append(Lscj)
                Rsc = cm.circle(c=(0, 0, 0), nr=(0, 0, 1), sw=360, r=0.5, d=3, ut=0, tol=0.01, s=8, ch=1,n="brow_R_sec_0" + str(i) + "_ctl")
                Rscj = cm.joint(n="brow_R_sec_0" + str(i) + "_jnt")
                Rbnpo = cm.group(Rsc[0], n="brow_R_sec_0" + str(i) + "_bufferNpo")
                Rnpo = cm.group(Rsc[0], n="brow_R_sec_0" + str(i) + "_npo")
                Rwt=cm.xform(Rtcj, ws=True, q=True, t=True)
                cm.setAttr(Rbnpo + ".t", Rwt[0], Rwt[1], Rwt[2])
                Rsk.append(Rscj)
                cm.select(cl=True)
                Sec -= 1
        cm.select(cl=True)
        cm.skinCluster(Lsk,Lbr[0],dr=4)
        cm.skinCluster(Rsk,Rbr[0],dr=4)
    
    #Eyelid set
    if (len(Einfo)!=0):
        cm.select(Einfo.split(","))
        Ecbr = cm.polyToCurve(form=2, degree=1, conformToSmoothMeshPreview=1, n="Eyelid_L_Cv")
        Elbr = cm.rebuildCurve(Ecbr[0], ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=Esec - 1, d=3, tol=0.01)
        Erbr = cm.duplicate(Elbr[0], rr=True, n="Eyelid_R_Cv")
        cm.setAttr(Erbr[0] + ".sx", -1)
        cm.makeIdentity(apply=True, t=0, r=0, s=1, n=0, pn=1)
        cm.select(cl=True)
        for i in range(0, Esec):
            Eltc=cm.curve(d=1, p=[(0, 1*0.2, 0),(0,0.92388*0.2,0.382683*0.2),(0,0.707107*0.2,0.707107*0.2),(0,0.382683*0.2,0.92388*0.2),(0,0,1*0.2),(0,-0.382683*0.2,0.92388*0.2),(0,-0.707107*0.2,0.707107*0.2),(0,-0.92388*0.2,0.382683*0.2),(0,-1*0.2,0),(0,-0.92388*0.2,-0.382683*0.2),(0,-0.707107*0.2,-0.707107*0.2),(0,-0.382683*0.2,-0.92388*0.2),(0,0,-1*0.2),(0,0.382683*0.2,-0.92388*0.2),(0,0.707107*0.2,-0.707107*0.2),(0,0.92388*0.2,-0.382683*0.2),(0,1*0.2,0),(0.382683*0.2,0.92388*0.2,0),(0.707107*0.2,0.707107*0.2,0),(0.92388*0.2,0.382683*0.2,0),(1*0.2,0,0),(0.92388*0.2,-0.382683*0.2,0),(0.707107*0.2,-0.707107*0.2,0),(0.382683*0.2,-0.92388*0.2,0),(0,-1*0.2,0),(-0.382683*0.2, -0.92388*0.2, 0),(-0.707107*0.2,-0.707107*0.2,0),(-0.92388*0.2,-0.382683*0.2,0),(-1*0.2,0,0),(-0.92388*0.2,0.382683*0.2,0),(-0.707107*0.2,0.707107*0.2,0),(-0.382683*0.2,0.92388*0.2,0),(0,1*0.2,0),(0,0.92388*0.2,-0.382683*0.2),(0, 0.707107*0.2, -0.707107*0.2),(0, 0.382683*0.2, -0.92388*0.2),(0, 0, -1*0.2),(-0.382683*0.2,0,-0.92388*0.2),(-0.707107*0.2,0,-0.707107*0.2),(-0.92388*0.2,0,-0.382683*0.2),(-1*0.2,0,0),(-0.92388*0.2,0,0.382683*0.2),(-0.707107*0.2,0,0.707107*0.2),(-0.382683*0.2,0,0.92388*0.2),(0,0,1*0.2),(0.382683*0.2,0,0.92388*0.2),(0.707107*0.2,0,0.707107*0.2),(0.92388*0.2,0,0.382683*0.2),(1*0.2,0,0),(0.92388*0.2,0,-0.382683*0.2),(0.707107*0.2,0,-0.707107*0.2),(0.382683*0.2,0,-0.92388*0.2),(0,0,-1*0.2)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52],n="eyelid_L0"+str(i)+"_tweak_ctl")  
            Eltcj = cm.joint(n="eyelid_L0" + str(i) + "_tweak_ctl_jnt")
            Eltnpo = cm.group(Eltc, n="eyelid_L0" + str(i) + "_tweak_npo")
            cm.pathAnimation(Eltnpo,Elbr[0],fm=True,f=True, fa= "x", ua= "y", wut= "vector", wu=( 0, 1, 0), iu= False, inverseFront= False, b= False,stu=0,etu=100)
            Elsk.append(Eltcj)
            cm.select(cl=True)
            Ertc=cm.curve(d=1, p=[(0, 1*0.2, 0),(0,0.92388*0.2,0.382683*0.2),(0,0.707107*0.2,0.707107*0.2),(0,0.382683*0.2,0.92388*0.2),(0,0,1*0.2),(0,-0.382683*0.2,0.92388*0.2),(0,-0.707107*0.2,0.707107*0.2),(0,-0.92388*0.2,0.382683*0.2),(0,-1*0.2,0),(0,-0.92388*0.2,-0.382683*0.2),(0,-0.707107*0.2,-0.707107*0.2),(0,-0.382683*0.2,-0.92388*0.2),(0,0,-1*0.2),(0,0.382683*0.2,-0.92388*0.2),(0,0.707107*0.2,-0.707107*0.2),(0,0.92388*0.2,-0.382683*0.2),(0,1*0.2,0),(0.382683*0.2,0.92388*0.2,0),(0.707107*0.2,0.707107*0.2,0),(0.92388*0.2,0.382683*0.2,0),(1*0.2,0,0),(0.92388*0.2,-0.382683*0.2,0),(0.707107*0.2,-0.707107*0.2,0),(0.382683*0.2,-0.92388*0.2,0),(0,-1*0.2,0),(-0.382683*0.2, -0.92388*0.2, 0),(-0.707107*0.2,-0.707107*0.2,0),(-0.92388*0.2,-0.382683*0.2,0),(-1*0.2,0,0),(-0.92388*0.2,0.382683*0.2,0),(-0.707107*0.2,0.707107*0.2,0),(-0.382683*0.2,0.92388*0.2,0),(0,1*0.2,0),(0,0.92388*0.2,-0.382683*0.2),(0, 0.707107*0.2, -0.707107*0.2),(0, 0.382683*0.2, -0.92388*0.2),(0, 0, -1*0.2),(-0.382683*0.2,0,-0.92388*0.2),(-0.707107*0.2,0,-0.707107*0.2),(-0.92388*0.2,0,-0.382683*0.2),(-1*0.2,0,0),(-0.92388*0.2,0,0.382683*0.2),(-0.707107*0.2,0,0.707107*0.2),(-0.382683*0.2,0,0.92388*0.2),(0,0,1*0.2),(0.382683*0.2,0,0.92388*0.2),(0.707107*0.2,0,0.707107*0.2),(0.92388*0.2,0,0.382683*0.2),(1*0.2,0,0),(0.92388*0.2,0,-0.382683*0.2),(0.707107*0.2,0,-0.707107*0.2),(0.382683*0.2,0,-0.92388*0.2),(0,0,-1*0.2)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52],n="eyelid_R0"+str(i)+"_tweak_ctl")
            Ertcj = cm.joint(n="eyelid_R0" + str(i) + "_tweak_ctl_jnt")
            Ertnpo = cm.group(Ertc, n="eyelid_R0" + str(i) + "_tweak_npo")
            cm.pathAnimation(Ertnpo,Erbr[0],fm=True,f=True, fa= "x", ua= "y", wut= "vector", wu=( 0, 1, 0), iu= False, inverseFront= False, b= False,stu=0,etu=100)
            Ersk.append(Ertcj)
            cm.select(cl=True)
            Elmp=cm.listConnections(Eltnpo+".rx",s=True)
            cm.cutKey(Elmp[0],cl=True,at= "u")
            cm.setAttr(Elmp[0]+".uValue",i/(Esec-0.0))
            Ermp=cm.listConnections(Ertnpo+".rx",s=True)
            cm.cutKey(Ermp[0],cl=True,at= "u")
            cm.setAttr(Ermp[0]+".uValue",i/(Esec-0.0))
            cm.select(cl=True)
        cm.select(cl=True)
        cm.delete(Elbr[0])
        cm.delete(Erbr[0])
        #cm.skinCluster(Elsk,Elbr[0],dr=4)
        #cm.skinCluster(Ersk,Erbr[0],dr=4)
    #Cheek up set
    if (len(Cinfo_up)!=0):  
        cm.select(Cinfo_up.split(","))
        Ccbr_up = cm.polyToCurve(form=2, degree=1, conformToSmoothMeshPreview=1, n="Cheek_Lup_Cv")
        Clbr_up = cm.rebuildCurve(Ccbr_up[0], ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=Csec_up - 1, d=3, tol=0.01)
        Crbr_up = cm.duplicate(Clbr_up[0], rr=True, n="Cheek_Rup_Cv")
        cm.setAttr(Crbr_up[0] + ".sx", -1)
        cm.makeIdentity(apply=True, t=0, r=0, s=1, n=0, pn=1)
        cm.select(cl=True)
        for i in range(0,Csec_up):
            Cltc_up=cm.curve(d=1,p=[(-0.4,0.4,0.4),(-0.4,0.4,-0.4),(0.4,0.4, -0.4),(0.4,0.4,0.4),(-0.4,0.4,0.4),(-0.4,-0.4,0.4),(-0.4,-0.4,-0.4),(-0.4,0.4,-0.4),(-0.4,0.4,0.4),(-0.4,-0.4,0.4),(0.4,-0.4,0.4),(0.4,0.4,0.4),(0.4,0.4,-0.4),(0.4,-0.4,-0.4),(0.4,-0.4,0.4),(0.4,-0.4,-0.4),(-0.4,-0.4,-0.4)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],n="Cheek_L0"+str(i)+"_tweakUp_ctl")
            Cltcj_up = cm.joint(n="Cheek_L0" + str(i) + "_tweakUp_ctl_jnt")
            Cltnpo_up = cm.group(Cltc_up, n="Cheek_L0" + str(i) + "_tweakUp_npo")
            cm.pathAnimation(Cltnpo_up,Clbr_up[0],fm=True,f=True, fa= "x", ua= "y", wut= "vector", wu=( 0, 1, 0), iu= False, inverseFront= False, b= False,stu=0,etu=100)
            #Clsk_up.append(Cltcj_up)
            cm.select(cl=True)
            Crtc_up=cm.curve(d=1,p=[(-0.4,0.4,0.4),(-0.4,0.4,-0.4),(0.4,0.4, -0.4),(0.4,0.4,0.4),(-0.4,0.4,0.4),(-0.4,-0.4,0.4),(-0.4,-0.4,-0.4),(-0.4,0.4,-0.4),(-0.4,0.4,0.4),(-0.4,-0.4,0.4),(0.4,-0.4,0.4),(0.4,0.4,0.4),(0.4,0.4,-0.4),(0.4,-0.4,-0.4),(0.4,-0.4,0.4),(0.4,-0.4,-0.4),(-0.4,-0.4,-0.4)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],n="Cheek_R0"+str(i)+"_tweakUp_ctl")
            Crtcj_up = cm.joint(n="Cheek_R0" + str(i) + "_tweakUp_ctl_jnt")
            Crtnpo_up = cm.group(Crtc_up, n="Cheek_R0" + str(i) + "_tweakUp_npo")
            cm.pathAnimation(Crtnpo_up,Crbr_up[0],fm=True,f=True, fa= "x", ua= "y", wut= "vector", wu=( 0, 1, 0), iu= False, inverseFront= False, b= False,stu=0,etu=100)
            #Crsk_up.append(Crtcj_up)
            cm.select(cl=True)
            Clmp_up=cm.listConnections(Cltnpo_up+".rx",s=True)
            cm.cutKey(Clmp_up[0],cl=True,at= "u")
            cm.setAttr(Clmp_up[0]+".uValue",i/(Csec_up-1.0))
            Crmp_up=cm.listConnections(Crtnpo_up+".rx",s=True)
            cm.cutKey(Crmp_up[0],cl=True,at= "u")
            cm.setAttr(Crmp_up[0]+".uValue",i/(Csec_up-1.0))
            cm.select(cl=True)
        cm.delete(Clbr_up[0])
        cm.delete(Crbr_up[0])
    #Cheek low set     
    if (len(Cinfo_low)!=0):  
        cm.select(Cinfo_low.split(","))
        Ccbr_low = cm.polyToCurve(form=2, degree=1, conformToSmoothMeshPreview=1, n="Cheek_low_Cv")
        Clbr_low = cm.rebuildCurve(Ccbr_low[0], ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=Csec_low - 1, d=3, tol=0.01)
        cm.select(cl=True)
        for i in range(0,Csec_low):
            Cltc_low=cm.curve(d=1,p=[(-0.4,0.4,0.4),(-0.4,0.4,-0.4),(0.4,0.4, -0.4),(0.4,0.4,0.4),(-0.4,0.4,0.4),(-0.4,-0.4,0.4),(-0.4,-0.4,-0.4),(-0.4,0.4,-0.4),(-0.4,0.4,0.4),(-0.4,-0.4,0.4),(0.4,-0.4,0.4),(0.4,0.4,0.4),(0.4,0.4,-0.4),(0.4,-0.4,-0.4),(0.4,-0.4,0.4),(0.4,-0.4,-0.4),(-0.4,-0.4,-0.4)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],n="Cheek_L0"+str(i)+"_tweakLow_ctl")
            Cltcj_low = cm.joint(n="Cheek_L0" + str(i) + "_tweakLow_ctl_jnt")
            Cltnpo_low = cm.group(Cltc_low, n="Cheek_L0" + str(i) + "_tweakLow_npo")
            cm.pathAnimation(Cltnpo_low,Clbr_low[0],fm=True,f=True, fa= "x", ua= "y", wut= "vector", wu=( 0, 1, 0), iu= False, inverseFront= False, b= False,stu=0,etu=100)
            #Clsk_up.append(Cltcj_low)
            cm.select(cl=True)
            Clmp_low=cm.listConnections(Cltnpo_low+".rx",s=True)
            cm.cutKey(Clmp_low[0],cl=True,at= "u")
            cm.setAttr(Clmp_low[0]+".uValue",i/(Csec_low-1.0))
            cm.select(cl=True)
        cm.delete(Clbr_low[0])
    #Lips set
    if (len(Linfo)!=0):
        cm.select(Linfo.split(","))
        Lcbr = cm.polyToCurve(form=2, degree=1, conformToSmoothMeshPreview=1, n="Lips_Cv")
        Llbr = cm.rebuildCurve(Lcbr[0], ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=Ltw - 1, d=3, tol=0.01)
        cm.select(cl=True)
        for i in range(0, Ltw):
            Lltc=cm.curve(d=1,p=[( 0.125,0,0.125),(-0.125,0,0.125),(-0.125,0,-0.125),(0.125,0,-0.125),(0.125,0,0.125),( 0,0.25,0),(-0.125,0,0.125),( -0.125, 0, -0.125),(0, 0.25, 0),(0.125, 0, -0.125),(0.125, 0, 0.125),(0, 0.25 ,0), (-0.125, 0, 0.125)], k=[ 0,4,8,12,16,24.485281,32.970563,36.970563,45.455844,53.941125,57.941125,66.426407,74.911688],n="Lips_0"+str(i)+"_tweakBrow_ctl")
            cm.setAttr(Lltc+".rx",-90)
            cm.makeIdentity(apply=True, t=0, r=1, s=0, n=0, pn=1)
            Lltcj = cm.joint(n="Lips_0" + str(i) + "_tweakBrow_ctrl_jnt")
            Lltnpo = cm.group(Lltc, n="Lips_0" + str(i) + "_tweakBrow_npo")
            cm.pathAnimation(Lltnpo,Llbr[0],fm=True,f=True, fa= "x", ua= "y", wut= "vector", wu=( 0, 1, 0), iu= False, inverseFront= False, b= False,stu=0,etu=100)
            cm.select(cl=True)
            Llmp=cm.listConnections(Lltnpo+".rx",s=True)
            cm.cutKey(Llmp[0],cl=True,at= "u")
            cm.setAttr(Llmp[0]+".uValue",i/(Ltw-0.0))
            cm.select(cl=True)
          # if (i % 2 == 0) and (Lsec):
          #      Llsc = cm.circle(c=(0, 0, 0), nr=(0, 0, 1), sw=360, r=0.5, d=3, ut=0, tol=0.01, s=8, ch=1,n="Lips_sec_0" + str(i) + "_ctl")
          #     Llscj = cm.joint(n="Lips_sec_0" + str(i) + "_jnt")
          #     Llbnpo = cm.group(Llsc[0], n="Lips_sec_0" + str(i) + "_bufferNpo")
          #     Llnpo = cm.group(Llsc[0], n="Lips_sec_0" + str(i) + "_npo")
          #    Llwt=cm.xform(Lltcj, ws=True, q=True, t=True)
          #    cm.setAttr(Llbnpo + ".t", Llwt[0], Llwt[1], Llwt[2])
          #    Llsk.append(Llscj)
          #    cm.select(cl=True)
          #   Sec -= 1
        
        cm.select(cl=True)
        #cm.skinCluster(Llsk,Llbr[0],dr=4)
        cm.delete(Llbr[0])
        
if __name__=="__main__":
   show_ui()
