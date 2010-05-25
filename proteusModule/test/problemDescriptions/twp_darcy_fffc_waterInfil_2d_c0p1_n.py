from pyadh import *
from pyadh.default_n import *
from twp_darcy_fffc_waterInfil_2d_p import *

#timeIntegrator = ForwardIntegrator
timeIntegration = FLCBDF
stepController = FLCBDF_controller
rtol_u[0] = 1.0e-5
atol_u[0] = 1.0e-5
rtol_u[1] = 1.0e-5
atol_u[1] = 1.0e-5
#DT = None
nDTout = 50#int(T/DT)

femSpaces = {0:C0_AffineLinearOnSimplexWithNodalBasis,
             1:C0_AffineLinearOnSimplexWithNodalBasis}

elementQuadrature = SimplexGaussQuadrature(nd,3)
elementBoundaryQuadrature = SimplexGaussQuadrature(nd-1,3)

#elementQuadrature = SimplexLobattoQuadrature(nd,1)
#elementBoundaryQuadrature = SimplexLobattoQuadrature(nd-1,1)


#triangleOptions += "A"
#triangleOptions = "q30Dena0.005A"   
#triangleOptions = "pq30Dena0.001A"
triangleOptions = "pq30Dena0.0025A"
nLevels = 1


massLumping=False

#subgridError = None

subgridError = FFDarcyFC_ASGS(coefficients,nd,stabFlag='2',lag=True)

shockCapturing = None
shockCapturing = ResGradFFDarcy_SC(coefficients,nd,shockCapturingFactor=0.5,lag=True)
#shockCapturing = ResGradFFDarcyDelayLag_SC(coefficients,nd,shockCapturingFactor=0.6,lag=False,
#                                           nStepsToDelay=10)


multilevelNonlinearSolver  = Newton

levelNonlinearSolver = Newton

maxNonlinearIts = 20#025
maxLineSearches = 10#0

fullNewtonFlag = True

tolFac = 0.0

nl_atol_res = 1.0e-8

matrix = SparseMatrix

multilevelLinearSolver = PETSc#PETSc LU

levelLinearSolver = PETSc#PETSc LU
#pick number of layers to use in overlap 
#"-ksp_type cg -pc_type asm -pc_asm_type basic -ksp_atol  1.0e-10 -ksp_rtol 1.0e-10 -ksp_monitor_draw" or
#-pc_type lu -pc_factor_mat_solver_package
nLayersOfOverlapForParallel = 2
#type of partition
parallelPartitioningType = MeshParallelPartitioningTypes.node
#parallelPartitioningType = MeshParallelPartitioningTypes.element
numericalFluxType = DarcyFCFF_IIPG_exterior

linTolFac = 0.0001

conservativeFlux = {0:'pwl',1:'pwl'}
