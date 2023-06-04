# Portfolio Alignment

In this section, we show how portfolio alignment with a decarbonization pathway changes the nature of portfolio decarbonization, making it a dynamic approach by nature. 

We first expose the issues arising when performing portfolio alignment with the PAB decarbonization pathway following the approach from Barahhou et al. (2022), using last available carbon intensity.

Then, we introduce issuers carbon footprint dynamics following Le Guenedal et Roncalli (2022) {cite:p}`le2022portfolio`. 
## A Dynamic Approach

Let's introduce the portfolio alignment strategy, that changes the nature of the portfolio decarbonization strategy.


At date $t$, the portfolio alignment imposes the following inequality constraint for the portfolio $x(t)$ (Barahhou et al. (2022)):

\begin{equation}
CI(x(t)) \leq (1 - \mathfrak{R}_{CI}(t_0,t))CI(b(t_0))
\end{equation}

The base year $t_0$ thus defines the reference level of the carbon intensity, as the reference level is $CI(b(t_0))$ and not $CI(b(t))$. This is a first important difference compared to the static strategy proposed by Andersson et al. (2016).

Then, the decarbonization problem becomes dynamic, with $t > t_1$ with $t_1$ the current year (Barahhou et al., 2022):
\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2} (x(t)-b(t))^T \Sigma(t)(x(t)-b(t))\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & &  0_n \leq x \leq 1_n \\
& & & CI(x(t)) \leq (1 - \mathfrak{R}_{CI}(t_0,t))CI(b(t_0))
\end{aligned}
\end{equation*}

In this problem, finding $x^*(t)$ at time $t$ requires to know the covariance matrix $\Sigma(t)$, the carbon intensities $CI(t)$ and the investable universe $b(t)$. However, in the current year $t_1$ the observations are only available for $t_0$ and $t_1$. We can however do the exercise by assuming that the world does not change. In this case, we can assume that the covariance matrix, the carbon intensities and the investable universe remain constant, such as (Barahhou et al., 2022):

\begin{equation}
\Sigma(t) = \Sigma(t_0)
\end{equation}
\begin{equation}
CI(t) = CI(t_0)
\end{equation}
\begin{equation}
b(t) = b(t_0)
\end{equation}


Thus, we have the following QP parameters:

\begin{equation*}
\begin{aligned}
& P = \Sigma(t) \\
& q = - \Sigma(t) b(t) \\
& A = 1^T_n \\
& b = 1 \\
& G = CI^T(t) \\
& h = (1 - \mathfrak{R}_{CI}(t_0,t))CI(b(t_0))\\
& lb = 0_n \\
& ub = 1_n
\end{aligned}
\end{equation*}

Let's first implement the `CarbonPortfolio` and `NetZeroPortfolio` dataclasses:
```Python
from dataclasses import dataclass
import numpy as np

@dataclass 
class CarbonPortfolio:

  x: np.array # Weights
  CI: np.array # Carbon Intensity
  Sigma: np.matrix # Covariance Matrix

  def get_waci(self) -> float:
    return self.x.T @ self.CI


from qpsolvers import solve_qp 

@dataclass 
class NetZeroPortfolio:
  b:np.array # Benchmark weights
  CI:np.array # Carbon intensity
  Sigma: np.matrix # Covariance matrix

  def get_portfolio(self, decarbonization_pathway:np.array) -> list[CarbonPortfolio]:
    
    dynamic_portfolio = []

    for t in range(len(decarbonization_pathway)):
      """QP Formulation"""

      x_optim = solve_qp(P = self.Sigma,
                q = -self.Sigma @ self.b, # we put a minus here because this QP solver consider +x^T R
                A = np.ones(len(self.b)).T, 
                b = np.array([1.]),
                G = self.CI.T, # resulting WACI
                h = (1 - decarbonization_pathway[t]) * self.b.T @ self.CI, # reduction imposed
                lb = np.zeros(len(self.b)),
                ub = np.ones(len(self.b)),
                solver = 'osqp')
      dynamic_portfolio.append(CarbonPortfolio(x = x_optim, 
                           Sigma = self.Sigma, CI = self.CI) )
    
    return dynamic_portfolio
```

We can use again the same example:

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

Now let's create the PAB's decarbonization pathway:

```Python
years = [i for i in range(2020, 2051)]
pab_decarbonization_patwhay = [1 - (1 - 0.07)**(years[i]-years[0])*(1 - 0.5) for i in range(len(years))]
```

We can now instantiate our problem and run the `get_portfolio` method:

```Python
test_dynamic_portfolio = NetZeroPortfolio(b = b,
                             CI = CI,
                             Sigma = Sigma)

resulting_pab = test_dynamic_portfolio.get_portfolio(decarbonization_pathway= pab_decarbonization_patwhay)
```

Let's represent the evolution of the tracking error volatility:

```Python
def get_tracking_error_volatility(x:np.array, 
                                  b:np.array,
                                  Sigma:np.array) -> float:
  return np.sqrt((x - b).T @ Sigma @ (x - b))


te = []

for portfolio in resulting_pab:
  if portfolio.x is not None:
    te.append(get_tracking_error_volatility(x = portfolio.x, b = b, Sigma = Sigma) * 100)
  else:
    te.append(np.nan)


import matplotlib.pyplot as plt

plt.figure(figsize = (10, 10))
plt.plot(years, te)
plt.xlim([2020, 2050])
plt.ylabel("Tracking Error Volatility (in %)")
plt.title("Tracking error volatility of dynamic net zero portfolio")
plt.show()
```


```{figure} tedynamicportfolio.png
---
name: tedynamicportfolio
---
Figure: Tracking error volatility of dynamic net zero portfolio
```


We can see that, using last available carbon intensities, we cannot find optimal solution after 2036. The more we more towards 2050, the more important the carbon intensity required by the decarbonization pathway is. This leads to more and more concentrated portfolio, until we don't find any solutions anymore.

## Integrating Carbon Footprint Dynamics

In the previous section, we have performed a portfolio alignment by using the last available carbon intensity (ie. backward-looking data).

In this section, we consider the decarbonization path of the issuers, as in Le Guenedal and Roncalli (2022) and Barahhou et al. (2022). This approach should help in finding optimal solutions and smoothing the expected future tracking error from the benchmark.

In order to have an idea of the potential issuers carbon footprint dynamics, we can exploit the historical trajectory of the past carbon emissions. We can follow Le Guenedal et al. (2022) and estimate the associated linear trend model and project the future carbon emissions by assuming that the issuer will do the same efforts in the future than in the past.

Le Guenedal et al. (2022) define the carbon trend by considering the following linear constant trend model:

\begin{equation}
CE(t) = \beta_0 + \beta_1 \cdot t + u(t)
\end{equation}

The parameters $\beta_0$ and $\beta_1$ can be estimated with the least squares methods on a sample of observations. 

The projected carbon trajectory is then given by:

\begin{equation}
CE^{Trend}(t) = \hat{CE}(t) = \hat{\beta_0} + \hat{\beta_1}t
\end{equation}

The underlying idea heare is to extrapolate the past trajectory. However, we need to reformulate our previous model. Indeed, it is not easy to interpret as $\hat{\beta_0} = \hat{CE(0)}$ when $t = 0$. We can add a base year $t_0$, that converts our model to:

\begin{equation}
CE(t) = \beta'_0 + \beta'_1(t - t_0) + u(t)
\end{equation}

And the carbon trajectory is now given by:

\begin{equation}
CE^{Trend}(t) = \hat{\beta'_0} + \hat{\beta'_1}(t - t_0)
\end{equation}

This change is just a matter of facilitating the interpretration. Indeed, the two models are equivalent and give the same value $\hat{CE}(t)$ with:

\begin{equation}
\beta^{'}_0 = \beta_0 + \beta_1 t_0
\end{equation}

and 

\begin{equation}
\beta^{'}_1 = \beta_1
\end{equation}

The only change resulting from the new formulation is that now $\hat{\beta}'_0 = \hat{CE}(t_0)$

Let's implement this with an example in Python:
```Python
years = [i for i in range(2007, 2021)]
emissions = [57.8, 58.4, 57.9, 55.1,
            51.6, 48.3, 47.1, 46.1,
            44.4, 42.7, 41.4, 40.2, 41.9, 45.0]

import pandas as pd
import statsmodels.api as sm

X = pd.Series([years[t] - years[-1] for t in range(len(years))])
X = sm.add_constant(X)
Y = pd.Series(emissions)
model = sm.OLS(Y, X)
results = model.fit()
results.params
```
Our estimates for $\hat{\beta_0}'$ and $\hat{\beta_1}'$ are:

```
const    38.988571
0        -1.451209
dtype: float64
```

And now we can define a function `forecast_carbon_emissions` for determining $CE^{Trend}(t)$:

```Python
beta_0 = results.params["const"]
beta_1 = results.params[0]

def forecast_carbon_emissions(beta_0:float, beta_1:float, t:int) -> float:
  carbon_trend = beta_0 + beta_1 * (t - 2020)
  return carbon_trend

forecast_carbon_emissions(beta_0 = beta_0,
                          beta_1 = beta_1,
                          t = 2025)
```

And the result is:

```
31.73252747252748
```

We can apply the same process on the carbon intensity $CI^{Trend}(t)$, rather than the carbon emissions level.
The optimization problem is the same as the previous optimization problem except that we include projected trends (of carbon intensity) in place of current intensities for the portfolio's WACI:

\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2} (x(t)-b(t))^T \Sigma(t)(x(t)-b(t))\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & &  0_n \leq x \leq 1_n \\
& & & CI^{trend}(x(t)) \leq (1 - \mathfrak{R}_{CI}(t_0,t))CI(b(t_0)) \\
\end{aligned}
\end{equation*}


For stocks with a negative slope, $CI^{Trend}_i(t+1) < CI^{Trend}_i(t)$, increasing the potential stocks satisfying the portfolio alignment condition.

In the second part of this course, we will introduce more forward-looking metrics, proposed by Le Guenedal et al. (2022).
