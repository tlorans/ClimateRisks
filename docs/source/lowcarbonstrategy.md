## Low-Carbon Strategy

As a first climate risks hedging strategy, we propose to follow Andersson et al. (2016) {cite:p}`andersson2016hedging` and Roncalli (2023), with a simple low-carbon index strategy.

The strategy consists in (i) reducing the weighted-average carbon intensity (WACI of the portoflio) while (ii) minimizing the tracking error relative to a benchmark.

The underlying assuption is that carbon risk is unpriced by the market. The financial aspect of carbon risk is then a risk of abrupt pricing by the market, once the markets participants integrate it. By reducing the portfolio's WACI, Andersson et al. (2016) suppose that the portfolio's carbon risk (here, the repricing risk associated with an abrupt carbon tax or carbon policy implementation) will be reduced. 

This carbon risk-hedging strategy is widely followed by index providers and asset managers, and can be defined as a low-carbon strategy.

In what follow, we will test two alternatives formulations for the climate objective: 
- the threshold approach, which consists in reducing the portfolio's WACI by changing the weights of stocks;
- the order-statistic approach, which consists in excluding the $m$ most emitting stocks.

### Threshold Approach

With the threshold approach, the objective is to minimize the tracking error with the benchmark while imposing a reduction $\mathfrak{R}$ in terms of carbon intensity. In practice, implementing such approach involves the weighted-average carbon intensity (WACI) computation and the introduction of a new constraint in a portfolio optimization problem with the presence of a benchmark (Roncalli, 2023).
#### Weighted-Average Carbon Intensity

The weighted-average carbon intensity (WACI) of the benchmark is:

\begin{equation}
CI(b) = b^T CI
\end{equation}

With $CI = (CI_1, ..., CI_n)$ the vector of carbon intensities.

The same is for the WACI of the portfolio:

\begin{equation}
CI(x) = x^T CI
\end{equation}

Let's implement a `CarbonPortfolio` dataclass:
```Python
from dataclasses import dataclass
import numpy as np

@dataclass 
class CarbonPortfolio:
  """
  A class that implement informations and methods needed for a carbon portfolio.
  """
  x: np.array # Weights
  CI: np.array # Carbon Intensities
  Sigma: np.matrix # Covariance Matrix


  def get_waci(self) -> float:
    return self.x.T @ self.CI
```
#### Integrating Carbon Intensity Reduction as a Constraint

The low-carbon strategy involves the reduction $\mathfrak{R}$ of the portfolio's carbon intensity $CI(x)$ compared to the benchmark's carbon intensity $CI(b)$. It can be viewed as the following constraint:

\begin{equation}
CI(x) \leq (1 - \mathfrak{R})CI(b)
\end{equation}

The optimization problem becomes:

\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2}(x-b)^T \Sigma (x - b)\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & & 0_n \leq x \leq 1_n \\
&&&  CI(x) \leq (1 - ℜ) CI(b)
\end{aligned}
\end{equation*}

with the following QP parameters:

\begin{equation*}
\begin{aligned}
& Q = \Sigma \\
& R = \Sigma b \\
& A = 1^T_n \\
& B = 1 \\
& C = CI^T \\
& D = CI^{+} = (1 - ℜ)CI(b) \\
& x^- = 0_n \\
& x^+ = 1_n
\end{aligned}
\end{equation*}

If `qpsolvers` is not installed yet:

```Python
!pip install qpsolvers 
```

We define a `LowCarbonStrategy` dataclass, because every low-carbon approaches will use the same information:
```Python
from abc import ABC, abstractmethod

@dataclass
class LowCarbonStrategy:
  b: np.array # Benchmark Weights
  CI:np.array # Carbon Intensity
  Sigma: np.matrix # Covariance Matrix


  def get_portfolio(self) -> CarbonPortfolio:
    pass
```

Now, we define a `ThresholdApproach` dataclass that inherits from `LowCarbonStrategy`:
```Python
from qpsolvers import solve_qp

@dataclass
class ThresholdApproach(LowCarbonStrategy):

  def get_portfolio(self, reduction_rate:float) -> CarbonPortfolio:
    """QP Formulation"""
    Q = self.Sigma
    R = self.Sigma @ self.b
    A = np.ones(len(self.b)).T # fully invested
    B = np.array([1.]) # fully invested
    x_inf = np.zeros(len(self.b)) # long-only position
    x_sup = np.ones(len(self.b)) # long-only position
    C = self.CI.T # resulting WACI
    D = (1 - reduction_rate) * self.b.T @ self.CI # reduction imposed

    x_optim = solve_qp(P = Q,
              q = -R, # we put a minus here because this QP solver consider +x^T R
              A = A, 
              b = B,
              G = C,
              h = D,
              lb = x_inf,
              ub = x_sup,
              solver = 'osqp')

    return CarbonPortfolio(x = x_optim, 
                           Sigma = self.Sigma, CI = self.CI)
```

Let's work on an example (from Roncalli, 2023) with the following benchmark weights $b$ and carbon intensities $CI$:

```Python
b = np.array([0.20,
              0.19,
              0.17,
              0.13,
              0.12,
              0.08,
              0.06,
              0.05])

CI = np.array([100.5,
               97.2,
               250.4,
               352.3,
               27.1,
               54.2,
               78.6,
               426.7])
```

We can use the market one-factor model to estimate the covariance matrix, based on stocks betas $\beta$, idiosyncratic volatilities $\tilde{\sigma}$
and market volatiltiy $\sigma_m$:

\begin{equation}
\Sigma = \beta \beta^T \sigma_m^2 + D
\end{equation}

Where $D$ is a diagonal matrix with $\tilde{\sigma}^2$ on its diagonal.

```Python
betas = np.array([0.30,
                  1.80,
                  0.85,
                  0.83,
                  1.47,
                  0.94,
                  1.67,
                  1.08])

sigmas = np.array([0.10,
                   0.05,
                   0.06,
                   0.12,
                   0.15,
                   0.04,
                   0.08,
                   0.07])

Sigma = betas @ betas.T * 0.18**2 + np.diag(sigmas**2)
```

We can now instantiate our threshold construction approach:

```Python
low_carbon_portfolio = ThresholdApproach(b = b, 
                                         CI = CI,
                                         Sigma = Sigma)
```

And let's simulate it with reduction rates $\mathfrak{R}$ between 0 and 70\%:

```Python
from numpy import arange

list_R = arange(0.0,0.7, 0.05)
list_portfolios = []


for R in list_R:
  list_portfolios.append(low_carbon_portfolio.get_portfolio(reduction_rate = R))

def get_tracking_error_volatility(x:np.array, 
                                  b:np.array,
                                  Sigma:np.array) -> float:
  return np.sqrt((x - b).T @ Sigma @ (x - b))

import matplotlib.pyplot as plt

reduction_rate = [reduction * 100 for reduction in list_R]
te = [get_tracking_error_volatility(x = portfolio.x, b = b, Sigma = Sigma) * 100 for portfolio in list_portfolios]

plt.figure(figsize = (10, 10))
plt.plot(reduction_rate, te)
plt.xlabel("Carbon Intensity Reduction (in %)")
plt.ylabel("Tracking Error Volatility (in %)")
plt.title("Efficient Decarbonization Frontier with Threshold Approach")
plt.show()
```

```{figure} thresholdapproach.png
---
name: thresholdapproach
---
Figure: Efficient Decarbonization Frontier with Threshold Approach
```

Because we impose a constraint and minimize the TE risk, the resulting portfolio will have fewer stocks than the initial benchmark $b$. This imply that the portfolio $x$ is less diversified than the initial benchmark $b$. In order to explicitly control the number of removed stocks, Andersson et al. (2016) and Roncalli (2023) propose another methodology: the order-statistic approach.
### Order-Statistic Approach

Andersson et al. (2016) and Roncalli et al. (2021) propose a second approach by eliminating the $m$ worst performing issuers in terms of carbon intensity.

We note $CI_{i:n}$ the order statistics of $[CI_1, ..., CI_n]$:

\begin{equation}
minCI_i = CI_{1:n} \leq ... \leq CI_{n:n} = max CI_i
\end{equation}

The carbon intensity bound $CI^{m,n}$ is defined as:

\begin{equation}
CI^{m,n} = CI_{n-m+1:n}
\end{equation}

Where $CI_{n-m+1:n}$ is the $(n-m+1)$-th order statistic of $[CI_1, ..., CI_n]$

Eliminating the $m$ worst performing assets is then equivalent to imposing the following constraint:

\begin{equation}
CI_i \geq CI^{m,n} → x_i = 0
\end{equation}

To implement this decarbonization strategy, the resulting weightings can be determined by:
- finding the optimal weightings that minimize the TE volatility
- reweighting the remaining stocks with a naïve approach

Contrary to the threshold approach, the reduction rate $\mathfrak{R}$ is not a parameter, but an output of the order-statistic approach. We thus need to define a function computing the resulting reduction rate compated to the benchmark, such as:

\begin{equation}
\mathfrak{R}(x|b) = 1 - \frac{x^T \cdot CI}{b^T \cdot CI}
\end{equation}

```Python
def get_waci_reduction(x:np.array,
                       b:np.array,
                       CI:np.array) -> float:
    return 1 - (x.T @ CI) / (b.T @ CI)
```

#### Optimal Weights with TE Minimization

We can introduce the order-statistic approach into our optimization problem with the new constraint. The optimization problem becomes:


\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2}x^T \Sigma x - x^T \Sigma b\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & & 0_n \leq x \leq x^+ \\
& & & x+ =  𝟙\{CI_i < CI^{m,n}\}
\end{aligned}
\end{equation*}

Where $x_i^+ = 𝟙\{CI_i < CI^{m,n}\}$, which is a vector of zeros and ones (zero if the stock is excluded, 1 otherwise).

And the following QP parameters:

\begin{equation*}
\begin{aligned}
& Q = \Sigma \\
& R = \Sigma b \\
& A = 1^T_n \\
& B = 1 \\
& x^- = 0_n \\
& x^+ = 𝟙\{CI_i < CI^{m,n}\}
\end{aligned}
\end{equation*}

```Python
# implement the second method: order-statistic approach

@dataclass
class LowCarbonStrategy(PortfolioConstruction):
  b: np.array # Benchmark Weights
  CI:np.array # Carbon Intensity
  
  def threshold_approach():
    pass

  def order_statistic_approach():
      if reweighting = "te_minimization"
    pass 

  def get_portfolio(self) -> CarbonPortfolio:
    pass
```

#### Naive Re-weighting

A "naive" solution consists in re-weighting the remaining stocks:

\begin{equation}
x_i = \frac{𝟙\{CI_i < CI^{m,n}\}b_i}{\sum^n_{k=1} 𝟙\{CI_k < CI^{m,n}\}b_k}
\end{equation}

```Python
# implement the second method: order-statistic approach

@dataclass
class LowCarbonStrategy(PortfolioConstruction):
  b: np.array # Benchmark Weights
  CI:np.array # Carbon Intensity
  
  def threshold_approach():
    pass

  def order_statistic_approach():
      if reweighting = "te_minimization":
        pass
      elif reweighting = "naive":
        pass

    pass 

  def get_portfolio(self) -> CarbonPortfolio:
    pass
```

### Key Takeaways

We've covered the most frequent carbon risk-hedging strategy with the low-carbon strategy approach. It relies on minimizing the tracking error volatiltiy relative to a CW benchmark while diminishing the exposure to carbon risk, measured with the carbon intensity. This is a fundamental-based approach (carbon intensity is the fundamental data of the carbon risk).

We've seen that the max-threshold approach dominates the order-statistic with TE minimization and the order-statistic with naïve reweighting in terms of decarbonization and tracking error volatility trade-off.

The main assumption of the low-carbon strategy is the absence of carbon risk pricing. We will relax this assumption in the next part.
