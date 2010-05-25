from pyadh import *
from pyadh.default_p import *
import blockDomain3d
"""
Heterogenous Poisson's equation in 2D on a block heterogeneous domain
"""
name = "gw_block_3d_anis4x4x4_c0p1"
##\page Tests Test Problems 
# \ref gw_block_3d_p.py "Heterogeneous Poisson's equation"
#

##\ingroup test
#\file gw_block_3d_p.py
#
#\brief single phase flow in block heterogeneous domain
#constant head on left and right

nd = 3
right = 1.0; back = 1.0; top = 1.0
nblocks = [4,4,4]

polyfile = "blockDomain3d"
L,boundaryTags,regions = blockDomain3d.genPoly(polyfileBase=polyfile,
                                               nx=nblocks[0],
                                               ny=nblocks[1],
                                               nz=nblocks[2],
                                               Lx=right,Ly=back,Lz=top)

#left and right heads
head_left = 1.0
head_right= 0.0
initialConditions = None

Ident = numpy.zeros((nd,nd),'d')
Ident[0,0]=1.0; Ident[1,1] = 1.0; Ident[2,2] = 1.0;


#try low conductivity block in upper right corner
hydraulicConductivities = {}
#no sources
sources = {}
def hydraulicConductivity_0(x,t):
    return numpy.array([[10.0,0.0,1.0],[0.0,8.0,1.0],[1.0,1.0,5.0]])
def hydraulicConductivity_1(x,t):
    return numpy.array([[1.0e-4,0.0,0.0],[0.0,1.0e-4,0.0],[0.0,0.0,1.0e-4]])
def nosource(x,t):
    return 0.0
for k in range(nblocks[2]):
    for j in range(nblocks[1]):
        for i in range(nblocks[0]):
            sources[regions[(i,j,k)][-1]] = nosource
            if i >= nblocks[0]-2 and j >= nblocks[1]-2 and k >= nblocks[2]-2: 
                hydraulicConductivities[regions[(i,j,k)][-1]] = hydraulicConductivity_1
            else:
                hydraulicConductivities[regions[(i,j,k)][-1]] = hydraulicConductivity_0
            

def headBCs(x,tag):
    if tag == boundaryTags['left'] and x[1] > L[1]*0.5 and x[2] > L[2]*0.5:
        return lambda x,t: head_left
    if tag == boundaryTags['right'] and x[2] < L[2]*0.5:
        return lambda x,t: head_right
def noFlowBCs(x,tag):
    if tag == boundaryTags['top']:
        return lambda x,t: 0.0
    if tag == boundaryTags['bottom']:
        return lambda x,t: 0.0
    if tag == boundaryTags['front']:
        return lambda x,t: 0.0
    if tag == boundaryTags['back']:
        return lambda x,t: 0.0
    if tag == boundaryTags['left']  and x[1] <= L[1]*0.5 and x[2] <= L[2]*0.5:
        return lambda x,t: 0.0
    if tag == boundaryTags['right'] and x[2] >= L[2]*0.5:
        return lambda x,t: head_right
class velEx:
    def __init__(self,duex,aex):
        self.duex = duex
        self.aex = aex
    def uOfX(self,X):
        du = self.duex.duOfX(X)
        A  = numpy.reshape(self.aex(X),(2,2))
        return -numpy.dot(A,du)
    def uOfXT(self,X,T):
        return self.uOfX(X)



##################################################
class SinglePhaseDarcyCoefficients(TC_base):
    def __init__(self,a_types,source_types,nc=1,nd=2,
                 timeVaryingCoefficients=False):
        self.a_types = a_types
        self.source_types = source_types
        self.nd = nd
        self.timeVaryingCoefficients=timeVaryingCoefficients
        mass = {}
        advection = {}
        diffusion = {}
        potential = {}
        reaction  = {}
        hamiltonian = {}
        for i in range(nc):
            diffusion[i] = {i : {i:'constant'}}
            reaction[i]  = {i : 'constant'}
            advection[i] = {i : 'constant'} #now include for gravity type terms
            potential[i] = {i : 'u'}
        #end i
        TC_base.__init__(self,
                         nc,
                         mass,
                         advection,
                         diffusion,
                         potential,
                         reaction,
                         hamiltonian)
    def initializeMesh(self,mesh):
        self.elementMaterialTypes = mesh.elementMaterialTypes
        self.exteriorElementBoundaryTypes =  numpy.zeros((mesh.nExteriorElementBoundaries_global),'i')
        for ebNE in range(mesh.nExteriorElementBoundaries_global):
            ebN = mesh.exteriorElementBoundariesArray[ebNE]
            eN  = mesh.elementBoundaryElementsArray[ebN,0]
            self.exteriorElementBoundaryTypes[ebNE] = self.elementMaterialTypes[eN]
        self.elementBoundaryTypes = numpy.zeros((mesh.nElementBoundaries_global,2),'i')
        self.elementBoundariesArray = mesh.elementBoundariesArray
        for ebN in range(mesh.nElementBoundaries_global):
            eN_left = mesh.elementBoundaryElementsArray[ebN,0]
            eN_right= mesh.elementBoundaryElementsArray[ebN,1]
            self.elementBoundaryTypes[ebN,0] = self.elementMaterialTypes[eN_left]
            if eN_right >= 0:
                self.elementBoundaryTypes[ebN,1] = self.elementMaterialTypes[eN_right]
            else:
                self.elementBoundaryTypes[ebN,1] = self.elementMaterialTypes[eN_left]
            
    def initializeElementQuadrature(self,t,cq):
        for ci in range(self.nc):
            cq[('f',ci)].flat[:] = 0.0
            for eN in range(cq['x'].shape[0]):
                material=self.elementMaterialTypes[eN]
                for k in range(cq['x'].shape[1]):
                    cq[('a',ci,ci)][eN,k,:,:] = self.a_types[material](cq['x'][eN,k],t)[:,:]
                    cq[('r',ci)][eN,k]        =-self.source_types[material](cq['x'][eN,k],t)
        #ci                        
    def initializeElementBoundaryQuadrature(self,t,cebq,cebq_global):
        nd = self.nd
        #use harmonic average for a, arith average for f
        for ci in range(self.nc):
            if cebq_global.has_key(('f',ci)): cebq_global[('f',ci)].flat[:] = 0.0
            if cebq.has_key(('f',ci)): cebq[('f',ci)].flat[:] = 0.0
            for ebN in range(cebq_global['x'].shape[0]):
                material_left = self.elementBoundaryTypes[ebN,0]
                material_right= self.elementBoundaryTypes[ebN,1]
                for k in range(cebq_global['x'].shape[1]):
                    if cebq_global.has_key(('r',ci)):
                        cebq_global[('r',ci)][eN,k] =-0.5*(self.source_types[material_left](cebq_global['x'][ebN,k],t)+
                                                           self.source_types[material_right](cebq_global['x'][ebN,k],t))
                    if cebq_global.has_key(('a',ci,ci)):
                        for i in range(nd):
                            for j in range(nd):
                                x = cebq_global['x'][ebN,k];
                                numer = 2.0*self.a_types[material_left](x,t)[i,j]*self.a_types[material_right](x,t)[i,j]
                                denom = self.a_types[material_left](x,t)[i,j] + self.a_types[material_right](x,t)[i,j] + 1.0e-20
                                cebq_global[('a',ci,ci)][eN,k,i,j] = numer/denom
            for eN in range(cebq['x'].shape[0]):
                for ebN_local in range(cebq['x'].shape[1]):
                    ebN = self.elementBoundariesArray[eN,ebN_local]
                    material_left = self.elementBoundaryTypes[ebN,0]
                    material_right= self.elementBoundaryTypes[ebN,1]
                    for k in range(cebq['x'].shape[2]):
                        x = cebq['x'][eN,ebN_local,k]
                        if cebq.has_key(('r',ci)):
                            cebq[('r',ci)][eN,ebN_local,k] =-0.5*(self.source_types[material_left](x,t)+
                                                                  self.source_types[material_right](x,t))
                        if cebq.has_key(('a',ci,ci)):
                            for i in range(nd):
                                for j in range(nd):
                                    numer = 2.0*self.a_types[material_left](x,t)[i,j]*self.a_types[material_right](x,t)[i,j]
                                    denom = self.a_types[material_left](x,t)[i,j] + self.a_types[material_right](x,t)[i,j] + 1.0e-20
                                    cebq[('a',ci,ci)][eN,ebN_local,k,i,j] = numer/denom
                    #
                #
            #
        #
    def initializeGlobalExteriorElementBoundaryQuadrature(self,t,cebqe):
        nd = self.nd
        for ci in range(self.nc):
            if cebqe.has_key(('f',ci)): cebqe[('f',ci)].flat[:] = 0.0
            for ebNE in range(cebqe['x'].shape[0]):
                material = self.exteriorElementBoundaryTypes[ebNE]
                for k in range(cebqe['x'].shape[1]):
                    x = cebqe['x'][ebNE,k]
                    if cebqe.has_key(('r',ci)):
                        cebqe[('r',ci)][ebNE,k] = -self.source_types[material](x,t)
                    if cebqe.has_key(('a',ci,ci)):
                        cebqe[('a',ci,ci)][ebNE,k,:,:] = self.a_types[material](x,t)[:,:]
                #
            #
        #
    def evaluate(self,t,c):
        pass #need to put in eval for time varying coefficients
        #mwf debug
        #print "eval c[('a',ci,ci)]= %s" % c[('a',0,0)]
    #end def
########################################

analyticalSolution = None
dirichletConditions = {0:headBCs}

analyticalSolutionVelocity = None

coefficients = SinglePhaseDarcyCoefficients(hydraulicConductivities,sources,nc=1,nd=nd)
   

fluxBoundaryConditions = {0:'setFlow'}

advectiveFluxBoundaryConditions =  {0:noFlowBCs}#{0:dummyBCs}

diffusiveFluxBoundaryConditions = {0:{0:noFlowBCs}}

