from pyadh import *
from pyadh.default_p import *
from pyadh.TwophaseDarcyCoefficients import *
#medium type and physical parameters are set here
from twp_darcy_modelParams import *
name = "twp_darcy_split_infil_1d_sat_bcb"

#psk model type
model= 'BCB'#'VGM'

#for convenience , to get bcs straight
def seVGM(psic,alVG,nVG,mVG):
    if psic <= 0: return 1.0
    tmp1 = pow(alVG*psic,nVG)
    tmp2 = pow(1.+tmp1,-mVG)
    return min(max(tmp2,0.0),1.0)
def pcVGM(se,alVG,nVG,mVG):
    if se >= 1.: return 0.0
    tmp1 = pow(se,-1./mVG)
    tmp2 = pow(tmp1-1.0,1.0/nVG)/alVG
    return tmp2
def seBCB(psic,pdBC,lamBC):
    if psic <= pdBC: return 1.0
    tmp1 = pow(pdBC/psic,lamBC)
    return min(max(tmp1,0.0),1.0)
def pcBCB(se,pdBC,lamBC):
    if se >= 1.0: return 0.0
    tmp1 = pow(se,-1.0/lamBC)
    return pdBC*tmp1

se2pc = None
pc2se = None
if model == 'VGM':
    se2pc = lambda se : pcVGM(se,mvg_alpha,mvg_n,mvg_m)
    pc2se = lambda pc : seVGM(pc,mvg_alpha,mvg_n,mvg_m)
elif model == 'BCB':
    se2pc = lambda se : pcBCB(se,bc_pd,bc_lambda)
    pc2se = lambda pc : seBCB(pc,bc_pd,bc_lambda)
#

#spatial domain
L = (10.0,1.0,1.0)
#auxiliary parameters and problem setup 
#where get a 'break' in ic's from bottom to top value 
xICbreak = L[0]


g    = [-gmag]                      # gravity  with direction
Se_top = 0.8#0.95#1.0                        # effective saturation top
Sw_top= Se_top*(sw_max-sw_min) + sw_min
psi_top = 0.1     #psi_w at top

waterTable =  -1.0#elevation of water table 
psiTable= 0.0     #psi_w at water table
#psi_w at z=0
psi_bottom = psiTable + g[0]/gmag*(0.0-waterTable)#waterTable - 0.0
psinTable  = 0.0
psin_bottom= psinTable + rhon/rhow*g[0]/gmag*(0.0-waterTable)#waterTable - 0.0
pc_bottom  = psin_bottom-psi_bottom
Se_bottom =  pc2se(pc_bottom)#0.05#1.0e-3                  # effective saturation bottom
Sw_bottom= Se_bottom*(sw_max-sw_min) + sw_min

hour = 3600.0 #[s]
T = 24.0*hour #clay 24.0*hour#12*hour                          # time [s]


analyticalSolutions = None
phase = 'saturation'
coefficients = TwophaseDarcy_split_saturation(g=g, 
                                              rhon=rhon,
                                              rhow=rhow,
                                              mun    = mun,
                                              muw    = muw,
                                              Ksw=Ksw,
                                              psk_model=model,
                                              vg_alpha = mvg_alpha,
                                              vg_m  = mvg_m,
                                              bc_pd  = bc_pd, 
                                              bc_lambda = bc_lambda,
                                              omega  = omega,
                                              Sw_max = sw_max,
                                              Sw_min = sw_min)

#now define the Dirichlet boundary conditions

def getDBC_sw(x,flag):
    if x[0] == L[0]:
        return lambda x,t: Se_top*(sw_max - sw_min)+sw_min
    if x[0] == 0.0:
        return lambda x,t: Se_bottom*(sw_max - sw_min)+sw_min

dirichletConditions = {0:getDBC_sw}

class sw_IC:
    def __init__(self):
        pass
    def uOfXT(self,x,t):
        if x[0] >= xICbreak:
            return Sw_top
        pc = pc_bottom + (rhon/rhow - 1.0)*g[0]/gmag*x[0]
        se = pc2se(pc)
        return se*(sw_max - sw_min) + sw_min

initialConditions  = {0:sw_IC()}

fluxBoundaryConditions = {0:'outFlow'}


advectiveFluxBoundaryConditions =  {}
diffusiveFluxBoundaryConditions = {0:{},1:{}}
