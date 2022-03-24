import numpy as np
from numpy.linalg import svd
import matplotlib.pyplot as plt
from IPython.display import clear_output

def get_cost(X, Y, A):
    """Given two sets of vectors, returns the cost of transport between them"""
    return X@A@Y.T

def Sinkhorn(mu1, mu2, Phi, sigma=0.1, max_iter=100):
    """The Sinkhorn algorithm to compute a, b functions"""
    b = np.ones_like(mu2)
    K = np.exp(Phi/sigma)
    for _ in range(max_iter):
        a = mu1/(K.dot(b))
        b = mu2/(K.T.dot(a))
        
    return a, b

def get_distr(a, b, Phi, sigma=0.1):
    """Given a, b functions retunrs the distribution of mass"""
    return ((np.diag(a).dot(np.exp(Phi/sigma))).dot(np.diag(b)))

def proximal_descent(A, X, mu1, Y, mu2, t=0.1, l=0.1, sigma=0.1, n_steps=100, verbose=True, svd_flag=False):
    """Gradient descent, to estimate the matrix A, given optimal matching"""
    X_size = X.shape[0]
    Y_size = Y.shape[0]
    size = min(X_size, Y_size)
    
    history_coeffs = []
    history_grad = []

    for i in range(n_steps):
        Phi = get_cost(X, Y, A)
        a, b = Sinkhorn(mu1, mu2, Phi, sigma)
        pi_A = get_distr(a, b, Phi, sigma)
        pi_hat = np.zeros_like(pi_A)
        np.fill_diagonal(pi_hat, 1/size)
        coeffs = pi_A - pi_hat
        
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