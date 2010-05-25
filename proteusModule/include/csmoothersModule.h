#ifndef SMOOTHERSMODULE_H
#define SMOOTHERSMODULE_H

#include "Python.h"
#include PYADH_LAPACK_H

/**
 \file csmoothersModule.h
 \brief The python interface to smoothers
*/

/**
  \defgroup csmoothers csmoothers
  \brief The python interface to the smoothers library
   @{
*/  
typedef struct 
{
  PyObject_HEAD
  int N;
  int *subdomain_dim;
  int **l2g_L;
  double **subdomain_L,
    **subdomain_R,
    **subdomain_dX;
  PYADH_LAPACK_INTEGER** subdomain_pivots;
} ASMFactor;
/** @} */
#endif