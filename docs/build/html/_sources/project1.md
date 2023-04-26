## Project 1: Portfolio Optimization in Practice

In order to implement the Markowitz approach, the estimation of the covariance matrix of stock returns is required. The standard statistical approach is to retrieve the history of past stock returns and compute the sample covariance matrix $\hat{\Sigma}$.

However, the sample covariance matrix is estimated with a lot of errors when the number of stocks $n$ is larger than the historical return observations $T$ (the condition $T >> n$ is not verified). Using the sample covariance matrix as an input of the Markowitz framework will lead to lack of robustness for the resulting portfolio.

To overcome this issue, shrinkage methods of the covariance are used in practice, in order to obtain a more reliable estimate of the covariance matrix to be used in the mean-variance framework. We will see how to apply the Ledoit-Wolf (2003b) {cite:p}`ledoit2003honey` approach.
### Sample Covariance Matrix and Portfolio Stability Issue

We can illustate the stability issue resulting from the sample covariance matrix with an example from Roncalli (2013). We will generate two sample covariance matrices with different correlation (we assume the cross-correlation is equal to 0.8 in the first example, to 0.9 in the second example):
```Python
import numpy as np
mu = np.array([0.08, 0.08, 0.05])
sigma = np.array([0.2, 0.21, 0.1])
rho_A = np.array([[1., 0.8, 0.8],
               [0.8, 1, 0.8 ],
               [0.8, 0.8, 1.]])
Sigma_A = np.diag(sigma) @ rho_A @ np.diag(sigma)
rho_B = np.array([[1., 0.9, 0.9],
               [0.9, 1, 0.9 ],
               [0.9, 0.9, 1.]])
Sigma_B = np.diag(sigma) @ rho_B @ np.diag(sigma)
```

Let's now use the code for portfolio construction as before:
```Python
from dataclasses import dataclass 

@dataclass 
class Portfolio:
  """A simple dataclass storing the basics information of a porfolio and 
  implementing the methods for the two moments computation.
  """
  x: np.array # Weights
  mu: np.array # Expected Returns
  Sigma: np.matrix # Covariance Matrix

  def get_expected_returns(self) -> float:
    return self.x.T @ self.mu

  def get_variance(self) -> float:
    return self.x.T @ self.Sigma @ self.x


from qpsolvers import solve_qp

@dataclass
class MeanVariance:

  mu: np.array # Expected Returns
  Sigma: np.matrix # Covariance Matrix
  
  def get_portfolio(self, gamma:float) -> Portfolio:
    """QP Formulation"""

    x_optim = solve_qp(P = self.Sigma,
              q = -(gamma * self.mu),
              A = np.ones(len(self.mu)).T, # fully invested
              b = np.array([1.]), # fully invested
              lb = np.zeros(len(self.mu)), # long-only position
              ub = np.ones(len(self.mu)), # long-only position
              solver = 'osqp')

    return Portfolio(x = x_optim, mu = self.mu, Sigma = self.Sigma)

portfolio_A = MeanVariance(mu = mu, Sigma = Sigma_A)
weights_A = portfolio_A.get_portfolio(gamma = 0.5).x

portfolio_B = MeanVariance(mu = mu, Sigma = Sigma_B)
weights_B = portfolio_B.get_portfolio(gamma = 0.5).x

import matplotlib.pyplot as plt
x = np.arange(3)
width = 0.4
plt.figure(figsize = (10, 10))
plt.bar(x-0.2, weights_A, width)
plt.bar(x+0.2, weights_B, width)
plt.xticks(x, ["A","B","C"])
plt.ylabel("$x^*$")
plt.legend(["Sigma A", "Sigma B"])
plt.show()
``` 

```{figure} impactcovmatrix.png
---
name: impactcovmatrix
---
Figure: Optimum weights with $\rho = 0.8$ vs. $\rho = 0.9$
```
We see that a slight difference in terms of estimated cross-correlation leads to significantly different sample covariance matrices, and then to really different optimal weights!

### Shrinkage Methods: the Ledoit-Wolf Approach


In order to overcome unreliable sample covariance, shrinkage methods are used in practice for a better estimate of the covariance matrix.
Shrinkage methods approaches modify the sample covariance matrix $\hat{\Sigma}$ by a new estimate $\tilde{\Sigma}$ in order to take into account uncertainties. $\tilde{\Sigma}$ generally takes the form of a weighted sum of $\hat{\Sigma}$ and a correction term. 

The Ledoit-Wolf approach (2003a) {cite:p}`ledoit2003improved` proposes to combine two estimators for the covariance matrix: $\hat{\Sigma}$ and $\hat{\Phi}$.

$\hat{\Sigma}$, the sample covariance matrix is known to be unbiased but includes a lot of estimations errors where the number of observations periods is not significantly higher than the number of assets. The sample covariance can be computed as:
\begin{equation}
\hat{\Sigma} = \frac{ (R_t - \bar{R})^T \cdot (R_t - \bar{R}) }{T}
\end{equation}

$\hat{\Phi}$, a structured estimator  (shrinkage target) converges quickly but is a biased estimator. Ledoit and Wolf  proposed to use either the single-factor matrix of Sharpe (2003a) or the constant correlation model (2003b) as the shrinkage target. Thereafter, we will use the second one.

The Ledoit-Wolf approach combines both estimators to obtain a more efficient one, such as:

\begin{equation}
\tilde{\Sigma}_{\delta} = \delta \hat{\Phi} + (1 - \delta) \hat{\Sigma}
\end{equation}


With $\delta$ the shrinkage intensity, between 0 and 1.

The method involves two stages:
- determining the shrinkage target $\hat{\Phi}$
- determining the shrinkage intensity $\delta$

#### Finding the Skrinkage Target

As a first stage, we need to find the shrinkage target $\hat{\Phi}$. As we follow Ledoit and Wolf (2003b), $\hat{\Phi}$ is the empirical covariance matrix with a constant correlation $\bar{\rho}$, with:

\begin{equation}
\hat{\Phi}_{i,i} = \hat{\Sigma}_{i,i} 
\end{equation}

and 

\begin{equation}
\hat{\Phi}_{i,j} = \bar{\rho} \sqrt{\hat{\Sigma}_{i,i} \hat{\Sigma}_{j,j}} 
\end{equation}

We then need to determine $\bar{\rho}$.

We have:

\begin{equation}
\bar{\rho} = \frac{2}{(N-1)N}\sum^{n-1}_{i=1} \sum^n_{j=i+1} \frac{\hat{\Sigma}_{i,j}}{\sqrt{\hat{\Sigma}_{i,i}\hat{\Sigma}_{jj}}}
\end{equation} 

Let's implement these firsts elements in Python. The code below is directly inspired from [here](https://github.com/WLM1ke/LedoitWolf). Special thanks to its author.

```Python
from dataclasses import dataclass 

@dataclass 
class LedoitWolf:
  R: np.array # returns of t observation of n stocks

  def get_shrinkage(self) -> np.array:
    # sample covariance
    t, n = self.R.shape
    R_bar = np.mean(self.R, axis = 0, keepdims = True)
    Sigma_hat = (self.R - R_bar).T @ (self.R - R_bar) / t

    # rho_bar
    var = np.diag(Sigma_hat).reshape(-1, 1)
    sqrt_var = var ** 0.5 
    unit_cor_var = sqrt_var @ sqrt_var.T
    rho_bar = ((Sigma_hat / unit_cor_var).sum() - n) / n / (n-1)
    
    # shrinkage target 
    shrinkage_target = rho_bar * unit_cor_var
    np.fill_diagonal(shrinkage_target, var)

    return rho_bar, shrinkage_target
```

```Python
R_example = np.array([[0.0309, 0.0056, 0.0011],
     [0.0056, 0.0739, 0.0148], 
     [0.0011, 0.0148, 0.0489]])

test = LedoitWolf(R = R_example)
test.get_shrinkage()
```

```
(-0.4713495148122541,
 array([[ 0.00017204, -0.0001871 , -0.00012425],
        [-0.0001871 ,  0.00091582, -0.00028668],
        [-0.00012425, -0.00028668,  0.00040393]]))
```

#### Finding the Shrinkage Intensity

Then, the problem is now to estimate the optimal value of $\delta$. Ledoit and Wolf consider the quadratic loss $L(\delta)$ defined as:

\begin{equation}
L(\delta) = ||\delta \hat{\Phi} + (1 - \delta)\hat{\Sigma} - \Sigma||^2
\end{equation}

That is, the norm of the difference between the shrinkage estimator $\tilde{\Sigma}_{\delta}$, with $\Sigma$ the true covariance matrix.

They show that the optimal shrinkage intensity $\delta$, solving the minimization problem $\delta^* = arg min \mathbb{E}[L(\delta)]$ is:

\begin{equation}
\delta^* = max(0, min(\frac{1}{T} \frac{\pi - \rho}{\gamma}, 1))
\end{equation}

Where:

\begin{equation}
\pi = \sum_{i=1}^n \sum_{j=1}^n \pi_{i,j}
\end{equation}

\begin{equation}
\rho = \sum_{i = 1}^n \pi_{i,i} + \sum_{i=1}^n \sum_{j \neq i} \frac{\bar{\rho}}{2}(\sqrt{\frac{\hat{\Sigma}_{j,j}}{\hat{\Sigma}_{i,i}}} \eta_{i,j} + \sqrt{\frac{\hat{\Sigma}_{i,i}}{\hat{\Sigma}_{j,j}}} \eta_{j,i})
\end{equation}

\begin{equation}
\gamma = \sum^n_{i = 1} \sum^n_{j=1} (\hat{\Phi}_{i,j} - \hat{\Sigma}_{i,j})^2
\end{equation}

with:

\begin{equation}
\pi_{i,j} = \frac{1}{T} \sum^n_{t=1}((R_{i,t} - \bar{R}_i)(R_{j,t} - \bar{R}_j) - \hat{\Sigma}_{i,j})^2
\end{equation}

and 

\begin{equation}
\eta_{i,j} = \frac{1}{T} \sum^n_{t=1} ((R_{i,t} - \bar{R}_i)^2 - \hat{\Sigma}_{i,j})((R_{i,t} - \bar{R}_i)(R_{j,t} - \bar{R}_j) - \hat{\Sigma}_{i,j})
\end{equation}

Let's implement the rest of the `get_shrinkage` method:

```Python
from dataclasses import dataclass 

@dataclass 
class LedoitWolf:
  R: np.array # returns of t observation of n stocks

  def get_shrinkage(self) -> np.array:
    # sample covariance
    t, n = self.R.shape
    R_bar = np.mean(self.R, axis = 0, keepdims = True)
    Sigma_hat = (self.R - R_bar).T @ (self.R - R_bar) / t

    # rho_bar
    var = np.diag(Sigma_hat).reshape(-1, 1)
    sqrt_var = var ** 0.5 
    unit_cor_var = sqrt_var @ sqrt_var.T
    rho_bar = ((Sigma_hat / unit_cor_var).sum() - n) / n / (n-1)
    
    # shrinkage target 
    shrinkage_target = rho_bar * unit_cor_var
    np.fill_diagonal(shrinkage_target, var)

    # pi
    y = (self.R - R_bar)**2
    pi_mat = ((y.T @ y) / t - Sigma_hat**2) 
    pi = pi_mat.sum()

    # rho 
    eta_mat = (((self.R - R_bar)**3).T @ (self.R - R_bar)) / t - var * Sigma_hat
    np.fill_diagonal(eta_mat, 0)
    rho = (
        np.diag(pi_mat).sum()
        + rho_bar * ( 1 / sqrt_var @ sqrt_var.T * eta_mat).sum()
    )

    # gamma 
    gamma = np.linalg.norm(Sigma_hat - shrinkage_target, "fro") ** 2

    # shrinkage intensity
    shrinkage_intensity = max(0, min(1, (pi - rho) / gamma / t))

    # new sigma
    Sigma = shrinkage_intensity * shrinkage_target + (1 - shrinkage_intensity) * Sigma_hat

    return  Sigma, rho_bar, shrinkage_intensity
```

```Python
test = LedoitWolf(R = R_example)
test.get_shrinkage()
```

```
(array([[ 0.00017204, -0.0001871 , -0.00012425],
        [-0.0001871 ,  0.00091582, -0.00028668],
        [-0.00012425, -0.00028668,  0.00040393]]),
 -0.4713495148122541,
 1)
```

### Your Turn!

In this part, you will be asked to build your first mean variance portfolio. 

First, download the set of data we will work with for the rest of this course:

```Python
import pandas as pd
url = 'https://github.com/shokru/carbon_emissions/blob/main/data_fin.xlsx?raw=true'
data = pd.read_excel(url)
```

#### Exercise 1

1. Compute the sample covariance matrix
2. Compute the sample expected return
3. Build a mean-variance portfolio, with $\gamma = 0.5$

#### Exercise 2

Same as Exercise 1, but with an estimate of the covariance matrix with the Ledoit-Wolf shrinkage approach.