from pyadh import *
from pyadh.default_n import *
from la_rotatingcircle_2d_p import *

timeOrder = 1
nStagesTime = timeOrder
DT=None
runCFL = 0.45

class SSPRKwrap(SSPRKintegration):
    """
    wrap SSPRK so default constructor uses
    the order I want and runCFL without
    changing VectorTransport
    """
    def __init__(self,vt):
        SSPRKintegration.__init__(self,vt,timeOrder,runCFL)
        return
    #
#end wrapper
#BackwardEuler, ForwardEuler
timeIntegration = SSPRKwrap 
stepController=Min_dt_RKcontroller

femSpaces = {0:DG_Constants}

#elementQuadrature = SimplexLobattoQuadrature(nd,1)

#elementBoundaryQuadrature = SimplexLobattoQuadrature(nd-1,1)

elementQuadrature = SimplexGaussQuadrature(nd,3)

elementBoundaryQuadrature = SimplexGaussQuadrature(nd-1,3)

nLevels = 4

subgridError = None

numericalFluxType = Advection_DiagonalUpwind

shockCapturing = None

multilevelNonlinearSolver  = NLNI

levelNonlinearSolver = Newton

nonlinearSmoother = NLGaussSeidel

fullNewtonFlag = True

tolFac = 0.01

nl_atol_res = 1.0e-8

matrix = SparseMatrix

multilevelLinearSolver = LU

levelLinearSolver = LU

linearSmoother = GaussSeidel

linTolFac = 0.001

conservativeFlux = None

checkMass = True


archiveFlag = ArchiveFlags.EVERY_USER_STEP