import numpy as np
from numpy.linalg import svd
import matplotlib.pyplot as plt
from IPython.display import clear_output

def get_cost(X, Y, A):
    """
    Given two sets of vectors, returns the cost of transport between them

    Parameters
    ----------
    X : np.array, dims = (Batch_Size, N_x)
        The array of X vectors for matching problem
        
    Y : np.array, dims = (Batch_Size, N_y)
        The array of Y vectors for matching problem
        
    A : np.array, dims = (N_x, N_y)
        The matrix to specify the cost function

    """
    
    return X@A@Y.T

def Sinkhorn(mu1, mu2, Phi, sigma=0.1, max_iter=100):
    """
    The Sinkhorn algorithm to compute a, b functions
    
    Parameters
    ----------
    mu1 : np.array, dims = (N_x)
        Marginal distribution of x's
        
    mu2 : np.array, dims = (N_y)
        Marginal distribution of y's
        
    sigma : float, optional
        The entropy regulerization strength (default is 0.1)
        
    max_iter : int, optional
        Number of cycles of Sinkhorn to perform (default is 100)

    """
    
    b = np.ones_like(mu2)
    K = np.exp(Phi/sigma)
    for _ in range(max_iter):
        a = mu1/(K.dot(b))
        b = mu2/(K.T.dot(a))
        
    return a, b

def get_distr(a, b, Phi, sigma=0.1):
    """
    Given a, b functions retunrs the distribution of mass
    
    Parameters
    ----------
    a : np.array, dims = (N_x)
        Vector a computed by Sinkhorn
        
    b : np.array, dims = (N_y)
        Vector b computed by Sinkhorn
        
    sigma : float, optional
        The entropy regulerization strength (default is 0.1)
        
    """
    
    return ((np.diag(a).dot(np.exp(Phi/sigma))).dot(np.diag(b)))

def proximal_descent(A, X, mu1, Y, mu2, t=0.1, l=0.1, sigma=0.1, n_steps=100, verbose=True, svd_flag=False, pi_hat=None):
    """
    Gradient descent, to estimate the matrix A, given optimal matching
        
    Parameters
    ----------
    A : np.array, dims = (N_x, N_y)
        The matrix to specify the cost function
        
    X : np.array, dims = (Batch_Size, N_x)
        The array of X vectors for matching problem
    
    mu1 : np.array, dims = (N_x)
        Marginal distribution of x's
        
    Y : np.array, dims = (Batch_Size, N_y)
        The array of Y vectors for matching problem
        
    mu2 : np.array, dims = (N_y)
        Marginal distribution of y's
        
    t : float, optional
        Size step of graident descent (default is 0.1)
        
    sigma : float, optional
        The entropy regulerization strength (default is 0.1)
    
    n_steps : int, optional
        Number of cycles of Gradient Descent to perform (default is 100)
        
    verbose : bool, optional
        Wether to plot the training proccess or not (default is True)
        
    svd_flag : bool, optional
        Wether to use nuclear norm regulerization (default is False)
        
    pi_hat : np.array, None, optional
        Defines the default distribution of optimal matching, if None then diagonal matrix with uniform distribution on the diagonal is used (default is False)
    """
    
    X_size, X_features_size = X.shape
    Y_size, Y_features_size = Y.shape
    size = min(X_size, Y_size)
    
    history_coeffs = []
    history_grad = []
    
    if pi_hat is not None:
        pi = pi_hat
    else:
        pi = np.zeros((X_size, Y_size))
        np.fill_diagonal(pi, 1/size)

    for i in range(n_steps):
        Phi = get_cost(X, Y, A)
        a, b = Sinkhorn(mu1, mu2, Phi, sigma)
        pi_A = get_distr(a, b, Phi, sigma)

        coeffs = pi_A - pi
        
        grad = X.T@coeffs@Y
        A -= t*(grad)

        if svd_flag and l != 0:
            U, s, V = svd(A)
            _s = s - t*l
            _s *= (s > 0)

            A = U@np.diag(_s)@V

        history_coeffs.append(np.abs(coeffs).sum())
        history_grad.append(np.abs(grad).sum())

        if verbose:
            if not i%10:
                clear_output(wait=True)

                plt.figure(figsize=(14, 7))
                ax = plt.subplot(121)
                ax.plot(history_coeffs)
                ax.set_title("Distances Between measures")

                ax = plt.subplot(122)
                ax.plot(history_grad)
                ax.set_title("L1 Norm of Gradient")

                plt.show()
                
    return A, history_coeffs, history_grad