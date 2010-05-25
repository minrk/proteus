from pyadh import *
from pyadh.default_n import *
from obstacleInFlume3d import *
from vof_obstacleInFlume_3d_p import *

elementQuadrature = SimplexGaussQuadrature(nd,obstacleInFlume_quad_order)

elementBoundaryQuadrature = SimplexGaussQuadrature(nd-1,obstacleInFlume_quad_order)


timeIntegration = BackwardEuler_cfl
stepController=Min_dt_controller
timeIntegration = BackwardEuler
stepController=FixedStep
femSpaces = {0:C0_AffineLinearOnSimplexWithNodalBasis}
shockCapturing = ResGradQuad_SC(coefficients,nd,shockCapturingFactor=vof_shockCapturingFactor,lag=True)#linear
subgridError = Advection_ASGS(coefficients=coefficients,nd=nd,lag=False)
massLumping = False
numericalFluxType = Advection_DiagonalUpwind_IIPG_exterior

# timeOrder=1
# nStagesTime = timeOrder
# class SSPRKwrap(LinearSSPRKintegration):
#     """
#     wrap SSPRK so default constructor uses
#     the order I want and runCFL without
#     changing VectorTransport
#     """
#     def __init__(self,vt):
#         LinearSSPRKintegration.__init__(self,vt,timeOrder,runCFL)
#         return
# timeIntegration = SSPRKwrap 
# stepController=Min_dt_RKcontroller
# femSpaces = {0:DG_AffineP0_OnSimplexWithMonomialBasis}
# subgridError = None
# numericalFluxType = Advection_DiagonalUpwind
# shockCapturing = None
# subgridError = None
# massLumping = False

multilevelNonlinearSolver  = Newton

levelNonlinearSolver = Newton

nonlinearSolverConvergenceTest='rits'
levelnonlinearSolverConvergenceTest='rits'

nonlinearSmoother = NLGaussSeidel

fullNewtonFlag = True

tolFac = 0.0

nonlinearSolverConvergenceTest='rits'
nl_atol_res = 1.0e-4#0.001*he#1.0e-4
linearSolverConvergenceTest = 'r-true'

maxNonlinearIts = 1

matrix = SparseMatrix

multilevelLinearSolver = LU

levelLinearSolver = LU

if usePETSc:
    multilevelLinearSolver = PETSc
    levelLinearSolver = PETSc
   
linearSmoother = GaussSeidel

linTolFac = 0.001

conservativeFlux = None