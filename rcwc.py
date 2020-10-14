# Python implementation of optimization-based algorithm from paper

import numpy as np
import cvxpy as cp

np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

def rcwc(A, b, is_verbose=True, weights=None, solveroptions={}):
    """
    A: m x n matrix with A_ij being an indicator for whether element j appears in sample set i
    b: m x n matrix with b_ij being the weights for element j in target set i corresponding to target set mean
    """
    m, n = A.shape
    V = cp.Variable(shape=(n,n), PSD=True)
    constraints = [V[j,j] <= 1 for j in range(n)]
    objective = 0
    for i in range(m):
        row_mask = np.nonzero(A[i,:])[0]
        rowcol_mask = np.ix_(row_mask, row_mask)
        objterm = cp.quad_form(b[i,:], V) - cp.matrix_frac(V[row_mask,:] @ b[i,:], V[rowcol_mask])
        if weights is not None:
            objterm *= weights[i]
        objective += objterm
    if weights is None:
        objective /= m
    prob = cp.Problem(cp.Maximize(objective), constraints)

    prob.solve(verbose=is_verbose, solver=cp.MOSEK, **solveroptions)
    print(prob.value)
    Vhat = V.value
    a = np.zeros((m,n))
    for i in range(m):
        row_mask = np.nonzero(A[i,:])[0]
        rowcol_mask = np.ix_(row_mask, row_mask)
        a[i,row_mask] = np.linalg.inv(Vhat[rowcol_mask]) @ Vhat[row_mask,:] @ b[i,:]
    
    a[A == 0] = 0
    return a

def best_linear(A, b, x):
    m, n = A.shape
    a = cp.Variable(shape=(m, n))
    constraints = [a[A == 0] == 0]
    objective = cp.max(
        cp.sum(
            cp.square(cp.matmul(b, x.T) - cp.matmul(a, x.T)),
            axis = 0
        )
    )
    prob = cp.Problem(cp.Minimize(objective), constraints)

    prob.solve(verbose=False)
    ahat = a.value
    ahat[A == 0] = 0
    return ahat

def evaluate_weights_grothendieck(a, b, is_verbose=False, weights=None):
    m, n = a.shape
    M = np.zeros((n,n))
    for i in range(m):
        if weights is not None:
            M += weights[i] * np.outer(a[i,:] - b[i,:],a[i,:] - b[i,:])
        else:
            M += np.outer(a[i,:] - b[i,:],a[i,:] - b[i,:])
    V = cp.Variable((n,n), PSD=True)
    constraints = [V[j,j] <= 1 for j in range(n)]
    objective = cp.sum(cp.multiply(M, V))
    prob = cp.Problem(cp.Maximize(objective), constraints)

    prob.solve(verbose=is_verbose, solver=cp.MOSEK,) 
    result = prob.value
    if weights is None:
        result /= m
    return result

def evaluate_weights(a, b, x):
    m, n = a.shape
    expected_error = 1/m * np.sum(
        np.square(b @ x.T - a @ x.T),
        axis=0
    )

    return expected_error