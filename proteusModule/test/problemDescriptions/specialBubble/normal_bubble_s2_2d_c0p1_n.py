from pyadh import *
from pyadh.default_n import *
from normal_bubble_s2_2d_p import *
from bubble import *

timeIntegration = NoIntegration
#timeIntegration = PsiTCtte
timeIntegrator = SteadyStateIntegrator

femSpaces = {0:C0_AffineLinearOnSimplexWithNodalBasis}

elementQuadrature = SimplexGaussQuadrature(nd,4)

elementBoundaryQuadrature = SimplexGaussQuadrature(nd-1,4)

#elementQuadrature = SimplexLobattoQuadrature(nd,1)
#
#elementBoundaryQuadrature = SimplexLobattoQuadrature(nd-1,1)

subgridError = None
shockCapturing = None
massLumping = False
reactionLumping=False
#numericalFluxType = Diffusion_IIPG_exterior
multilevelNonlinearSolver  = Newton
fullNewtonFlag = False
tolFac = 1.0e-8
atol = 1.0e-8 #1e-4
maxNonlinearIts = 100
matrix = SparseMatrix
multilevelLinearSolver = LU
levelLinearSolver = LU
linTolFac = 0.001
conservativeFlux = None