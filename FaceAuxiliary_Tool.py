import maya.cmds as cm
import maya.mel as ml

if cm.window('Auxiliary', ex=True):
    cm.deleteUI('Auxiliary')
cm.window('Auxiliary', title="FaceAuxiliary_Tool", wh=(700, 500))
Fl = cm.formLayout("Fl")
Frl = cm.frameLayout("Frl", label="眉弓设置", p=Fl)
TfbGrp = cm.textFieldButtonGrp('Tfbg', l='选择位置线:', bl=">>>获取<<<", bc="Get_e()", adj=2, editable=False)
IsGrp01 = cm.intSliderGrp('IsGrp01', field=True, label='次级控制器数量：', minValue=3, maxValue=60, value=1)
IsGrp02 = cm.intSliderGrp('IsGrp02', field=True, label='调整控制器数量：', minValue=5, maxValue=100, value=1)
Bt = cm.button(label='确定', c='Brow()')
cm.formLayout(Fl, edit=True, attachForm=[(Frl, "top", 0), (Frl, "left", 0), (Frl, "right", 0)])
cm.setParent("..")
cm.showWindow('Auxiliary')


def Get_e():
    # Sel=cm.ls(sl=True,fl=True)
    Sele = ml.eval('string $sel[]=`ls -sl -fl`;stringArrayToString($sel,\",\");')
    cm.textFieldButtonGrp(TfbGrp, e=True, tx=Sele)


def Brow():
    Info = cm.textFieldGrp(TfbGrp, q=True, tx=True)
    Sec = cm.intSliderGrp(IsGrp01, q=True, v=True)
    Tw = cm.intSliderGrp(IsGrp02, q=True, v=True)
    cm.select(Info.split(","))
    Cbr = cm.polyToCurve(form=2, degree=1, conformToSmoothMeshPreview=1, n="Brow_L_Cv")
    Lbr = cm.rebuildCurve(Cbr[0], ch=1, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=Tw - 1, d=1, tol=0.01)
    Rbr = cm.duplicate(Lbr[0], rr=True, n="Brow_R_Cv")
    cm.setAttr(Rbr[0] + ".sx", -1)
    cm.makeIdentity(apply=True, t=0, r=0, s=1, n=0, pn=1)
    # Sp=cm.getAttr(Br[0]+"Shape.s")
    cm.select(cl=True)
    for i in range(0, Tw):
        Lwt = cm.xform(Lbr[0] + ".cv[" + str(i) + "]", ws=True, q=True, t=True)
        Rwt = cm.xform(Rbr[0] + ".cv[" + str(i) + "]", ws=True, q=True, t=True)
        Ljnt = cm.joint(n="brow_L0" + str(i) + "_fur_jnt", p=(Lwt[0], Lwt[1], Lwt[2]), a=True)
        select(cl=True)
        Rjnt = cm.joint(n="brow_R0" + str(i) + "_fur_jnt", p=(Rwt[0], Rwt[1], Rwt[2]), a=True)
        select(cl=True)
        if (i % 2 == 0) and (Sec):
            Lsc = cm.circle(c=(0, 0, 0), nr=(0, 0, 1), sw=360, r=1, d=3, ut=0, tol=0.01, s=8, ch=1,
                            n="brow_L_sec_0" + str(i) + "_ctl")
            Lscj = cm.joint(n="brow_L_sec_0" + str(i) + "_jnt")
            Lbnpo = cm.group(Lsc[0], n="brow_L_sec_0" + str(i) + "_bufferNpo")
            Lnpo = cm.group(Lsc[0], n="brow_L_sec_0" + str(i) + "_npo")
            cm.setAttr(Lbnpo + ".t", Lwt[0], Lwt[1], Lwt[2])
            Rsc = cm.circle(c=(0, 0, 0), nr=(0, 0, 1), sw=360, r=1, d=3, ut=0, tol=0.01, s=8, ch=1,
                            n="brow_R_sec_0" + str(i) + "_ctl")
            Rscj = cm.joint(n="brow_R_sec_0" + str(i) + "_jnt")
            Rbnpo = cm.group(Rsc[0], n="brow_R_sec_0" + str(i) + "_bufferNpo")
            Rnpo = cm.group(Rsc[0], n="brow_R_sec_0" + str(i) + "_npo")
            cm.setAttr(Rbnpo + ".t", Rwt[0], Rwt[1], Rwt[2])
            select(cl=True)
            Sec -= 1
    cm.select(cl=True)

# Ctl=cm.curve(d=1,p=[(-0.165186, 0.165186, 0.57),(0.165186, 0.165186, 0.57),(0.165186, -0.165186, 0.57),(-0.165186, -0.165186, 0.57),(-0.165186,0.165186,0.57),(-0.165186, 0.165186, -0.43),(0.165186, 0.165186, -0.43),( 0.165186, -0.165186, -0.43),(-0.165186, -0.165186, -0.43),(-0.165186, 0.165186, -0.43),(-0.165186, 0.165186, 0.57),(0.165186, 0.165186, 0.57),(0.165186, 0.165186, -0.43),(0.165186, -0.165186, -0.43),(0.165186, -0.165186, 0.57),(-0.165186, -0.165186, 0.57),(-0.165186, -0.165186, -0.43)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],n="brow_L0"+str(i)+"_tweakBrow_ctl")
# Grp=cm.group(Ctl[0],q