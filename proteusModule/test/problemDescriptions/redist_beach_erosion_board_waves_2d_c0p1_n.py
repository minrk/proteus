from pyadh import *
from pyadh.default_n import *
from redist_beach_erosion_board_waves_2d_p import *
from beach_erosion_board_waves import *

if rdtimeIntegration == 'newton':    
    timeIntegration = NoIntegration
    stepController = Newton_controller
elif rdtimeIntegration == 'tte':
    timeIntegration = BackwardEuler_cfl
    timeIntegration = PsiTCtte
elif rdtimeIntegration == 'osher-fmm':
    timeIntegration = BackwardEuler_cfl
    stepController = Osher_FMM_controller
    runCFL=1.0
else:
    timeIntegration = BackwardEuler_cfl
    stepController = Osher_PsiTC_controller 
   #stepController = Osher_controller
    runCFL=1.0
#     timeIntegration = PsiTCtte
#     stepController = PsiTCtte_controller
#     rtol_res[0] = 0.0
#     atol_res[0] = 0.1*L[0]/(nn-1.0)#10% of he
#runCFL=1.0
#DT=None

if spaceOrder == 1:
    femSpaces = {0:C0_AffineLinearOnSimplexWithNodalBasis}
if spaceOrder == 2:
    femSpaces = {0:C0_AffineQuadraticOnSimplexWithNodalBasis}

elementQuadrature = SimplexGaussQuadrature(nd,sloshbox_quad_order)

elementBoundaryQuadrature = SimplexGaussQuadrature(nd-1,sloshbox_quad_order)

subgridErrorType = HamiltonJacobi_ASGS
if LevelModelType == RDLS.OneLevelRDLS and not RDLS.debugRDLS:
    subgridErrorType = HamiltonJacobi_ASGS_opt
if rdtimeIntegration == 'newton':
    subgridError = subgridErrorType(coefficients,nd,stabFlag='2',lag=False)
else:
    subgridError = subgridErrorType(coefficients,nd,stabFlag='2',lag=True)
    
#subgridError = HamiltonJacobi_ASGS(coefficients,nd,lag=True)

shockCapturing = None
#shockCapturing = ResGrad_SC(coefficients,nd,shockCapturingFactor=0.9,lag=False)
if rdtimeIntegration == 'newton':    
    shockCapturing = ResGradQuad_SC(coefficients,nd,shockCapturingFactor=rd_shockCapturingFactor,lag=False)
else:
    shockCapturing = ResGradQuad_SC(coefficients,nd,shockCapturingFactor=rd_shockCapturingFactor,lag=True)
    
massLumping = False


#multilevelNonlinearSolver  = MultilevelEikonalSolver
#levelNonlinearSolver = UnstructuredFMMandFSWsolvers.FMMEikonalSolver
nonlinearSmoother = NLGaussSeidel
multilevelNonlinearSolver  = Newton
levelNonlinearSolver = Newton
if rdtimeIntegration != 'newton':    
    maxLineSearches = 0
    levelNonlinearSolverConvergenceTest='rits'
    maxNonlinearIts = 1 #1 for PTC
else:
    maxLineSearches=100
    levelNonlinearSolverConvergenceTest='rits'
    maxNonlinearIts = 25 #1 for PTC

fullNewtonFlag = True

#this needs to be set appropriately for pseudo-transient
tolFac = 0.0

if rdtimeIntegration != 'newton':
    nl_atol_res = atolRedistance#1.0e-4
else:
    nl_atol_res = atolRedistance#0.01*he#1.0e-4#0.01*L[0]/nnx

atol_res[0] = 1.0e-6 #for pseudo transient
rtol_res[0] = 0.0

if LevelModelType == RDLS.OneLevelRDLS:
    numericalFluxType = DoNothing
else:    
    numericalFluxType = NF_base#None

maxNonlinearIts = 50 #1 for PTC

matrix = SparseMatrix

if usePETSc:
    if LevelModelType == RDLS.OneLevelRDLS:
        numericalFluxType = DoNothing
    else:    
        numericalFluxType = NF_base#None

    multilevelLinearSolver = PETSc
    
    levelLinearSolver = PETSc
else:
    multilevelLinearSolver = LU
    
    levelLinearSolver = LU

linearSmoother = GaussSeidel

linTolFac = 0.001

conservativeFlux = None