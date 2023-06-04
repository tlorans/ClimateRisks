# Integrating the Decarbonization Dimension

## Portfolio Decarbonization Pathway

If a decarbonization pathway is generally valid for an economy or a country, we must have in mind that it is defined in terms of absolute carbon emissions. However, portfolio decarbonization uses carbon intensity, and not absolute carbon emissions. We thus need to introduce the relationship of carbon emissions and carbon intensity pathway.

### Carbon Emissions and Carbon Intensity Pathway Relationship

Let's recall that the carbon intensity $CI(t)$ is defined as the ratio between the carbon emissions $CE(t)$ and a normalization variable $Y(t)$ (a physical or monetary value):

\begin{equation}
CI(t) = \frac{CE(t)}{Y(t)}
\end{equation}

If $\mathfrak{R}_{CI}(t_0)$ and $\mathfrak{R}_{CE}(t,t_0)$ are the reduction rates of carbon intensity and emissions between the base date $t_0$ and $t$, we have the following relationship (Barahhou et al., 2022):

\begin{equation}
\mathfrak{R}_{CI}(t_0,t) = \frac{g_Y(t_0,t) + \mathfrak{R}_{CE}(t_0,t)}{1 + g_Y(t_0,t)}
\end{equation}

Where $g_Y(t_0,t)$ is the growth rate of the normalization variable. As we assume that $g_Y(t_0,t) \geq 0$ and $0 \leq \mathfrak{R}_{CE}(t_0,t) \leq 1$, we have the property that the reduction rate of the carbon intensity is always greater than the reduction rate of the carbon emissions:

\begin{equation}
\mathfrak{R}_{CI}(t_0,t) \geq \mathfrak{R}_{CE}(t_0,t)
\end{equation}


The emissions decarbonization pathway $\mathfrak{R}_{CE}(t_0,t)$ is called the economic decarbonization pathway, while the intensity decarbonization pathway $\mathfrak{R}_{CI}(t_0,t)$ is called the financial decarbonization pathway.

We can simplify the financial / economic pathway relationship by considering both the annual growth rate of normalization variable $g_{Y}$ and the annual reduction rate of carbon emissions $\Delta \mathfrak{R}_{CE}$ as constant. We then have the compound growth rate of the normalization variable:

\begin{equation}
g_Y(t_0,t) = (1 + g_Y)^{t-t_0} - 1
\end{equation}

And the carbon reduction rate as:

\begin{equation}
\mathfrak{R}_{CE}(t_0,t) = 1 - (1 - \Delta \mathfrak{R}_{CE})^{t - t_0}
\end{equation}

Then, the relationship between the financial and the economic decarbonization pathway becomes (Barahhou et al., 2022):

\begin{equation}
\mathfrak{R}_{CI}(t_0,t) = 1 - (1 - \frac{(g_Y + \Delta \mathfrak{R}_{CE})}{1 + g_Y})^{t - t_0}
\end{equation}

We can create a new dataclass `FinancialDecarbonizationPathway`:
```Python
@dataclass 
class FinancialDecarbonizationPathway:

  delta_R_CE:float # Average yearly reduction rate (absolute emissions)
  g_Y:float # constant growth rate of the normalization variable

  def get_decarbonization_pathway(self, t_0:int, t:int):
    pathway = []
    for i in range(t_0,t+1):
      r = 1 - (1 - (self.g_Y + self.delta_R_CE) / (1 + self.g_Y))**(i - t_0)
      pathway.append(r)      
    
    return pathway
```
And then determine the reduction rate with $g_Y = 0.03$ and $\Delta \mathfrak{R}_{CE} = 0.07$:

```Python
test = FinancialDecarbonizationPathway(delta_R_CE = 0.07, g_Y = 0.03)
pathway = test.get_decarbonization_pathway(t_0 = 2020, t = 2050)
```

### From Economic to Financial Decarbonization Pathway

With a given economic decarbonization pathway $\mathfrak{R}_{CE}(t_0,t)$ and given normalization variable growth $g_Y(t_0,t)$, we can approximate the relationship between the economic and the financial decarbonization pathway.

We can illustrate this transformation from economic to financial decarbonization pathway, starting with the International Energy Agency (IEA) NZE Scenario (IEA, 2021) {cite:p}`bouckaert2021net`.

The IEA NZE scenario is the following (in GtCO2eq):
| Year  | 2019 | 2020 | 2025 | 2030 | 2035 | 2040 | 2045 | 2050 |
|---|---|---|---|---|---|---|---|---|
|$CE(t)$| 35.90  | 33.90   | 30.30  | 21.50  | 13.70 | 7.77 | 4.30 | 1.94 |


We linearly interpolate carbon emissions from this scenario and then obtain the corresponding decarbonization pathway $\mathfrak{R}_{CE}(t_0,t)$ with the carbon emissions scenario:
\begin{equation}
\mathfrak{R}_{CE}(t_0,t) = 1 - \frac{CE(t)}{CE(t_0)}
\end{equation}

```Python
import pandas as pd

years = [2020, 2025, 2030, 2035, 2040, 2045, 2050]
emissions = [33.90, 30.30, 21.50, 13.70, 7.77, 4.30, 1.94]

import scipy.interpolate

y_interp = scipy.interpolate.interp1d(years, emissions)

full_years = [i for i in range(years[0], years[-1]+1)]
emissions_interpolated = y_interp(full_years)

reduction_rate = [1 - emissions_interpolated[i] / emissions_interpolated[0] for i in range(len(emissions_interpolated))]
```


With $\mathfrak{R}_{CE}(t_0,t)$, we can estimate the financial decarbonization pathway for different values of the constant growth rate $g_Y$:
\begin{equation}
\mathfrak{R}_{CI}(t_0,t) = \frac{g_Y(t_0,t) + \mathfrak{R}_{CE}(t_0,t)}{1 + g_Y(t_0,t)}
\end{equation}

with $g_Y(t_0,t) = (1 + g_Y)^{t-t_0} - 1$.

Let's make an example with $g_Y = 0.03$:
```Python
g_Y = 0.03
growth_trajectory = [(1 + g_Y)**(full_years[i] - full_years[0]) - 1 for i in range(len(full_years))]
intensity_reduction = [(growth_trajectory[i] + reduction_rate[i])/(1 + growth_trajectory[i]) for i in range(len(full_years))]
```

Let's compare the financial decarbonization pathway deduced from the IEA scenario to the Paris-Aligned Benchmarks (PAB) decarbonization pathway.
The PAB's intensity decarbonization is stated as:
1. A year-on-year self-decarbonization $\Delta \mathfrak{R}_{CI}$ of 7\% on average per annum, based on scope 1, 2 and 3 carbon emissions intensities.
2. A minimum carbon intensity reduction $\mathfrak{R}_{CI}^-$ at 50\% compared to the invetable universe.

This financial decarbonization pathway is thus:

\begin{equation}
\mathfrak{R}_{CI}(t_0, t) = 1 - (1 - 7\%)^{t-t_0}(1 - 50\%)
\end{equation}

```Python
pab_reduction_rate = [1 - (1 - 0.07)**(full_years[i]-full_years[0])*(1 - 0.5) for i in range(len(full_years))]

plt.plot(full_years, intensity_reduction)
plt.plot(full_years, pab_reduction_rate)

plt.ylabel("Intensity reduction rate")
plt.legend(['IEA','PAB'])
plt.figure(figsize = (10, 10))
plt.show()
```

```{figure} ieavspab.png
---
name: ieavspab
---
Figure: Financial decarbonization pathway $\mathfrak{R}_{CI}(2020,2050)$ from the IEA scenario, with $g_Y = 0.03$ vs. PAB decarbonization pathway
```

We can see that the PAB financial decarbonization pathway is far more aggressive than the IEA-deduced pathway.

### Key Takeaways

- Portfolio decarbonization uses intensity decarbonization pathway (financial decarbonization pathway)

- With assumption about $g_Y$ the growth of the normalization variable, we can deduce a financial decarbonization pathway from an economic (decarbonization pathway based on absolute emissions) one

## Portfolio Alignment

In this section, we show how portfolio alignment with a decarbonization pathway changes the nature of portfolio decarbonization, making it a dynamic approach by nature. 

We first expose the issues arising when performing portfolio alignment with the PAB decarbonization pathway following the approach from Barahhou et al. (2022), using last available carbon intensity.

Then, we introduce issuers carbon footprint dynamics following Le Guenedal et Roncalli (2022) {cite:p}`le2022portfolio`. 

### A Dynamic Approach

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
& & argmin \frac{1}{2} (x(t)-b^{augmented}(t))^T \Sigma(t)(x(t)-b^{augmented}(t))\\
& \text{subject to}
& & \begin{bmatrix}
A_{Energy} + A_{Utilities} \\
A_{Cement} \\
A_{Steel} \\
A_{Chemicals} \\
A_{Textile \; \& \; Leather} \\
A_{Aluminium} \\
A_{Buildings} \\
A_{Food \; Processing} \\
A_{Transport} \\
A_{Others}
\end{bmatrix}^Tx(t) = \begin{bmatrix}
b_{Energy}(t) + b_{Utilities}(t) \\
b_{Cement}(t) \\
b_{Steel}(t) \\
b_{Chemicals}(t) \\
b_{Textile \; \& \; Leather}(t) \\
b_{Aluminium}(t) \\
b_{Buildings}(t) \\
b_{Food \; Processing}(t) \\
b_{Transport}(t) \\
b_{Others}(t)
\end{bmatrix}\\
& & &  0_u \leq x(t) \leq \mathbb{1}\{i \notin \text{Oil or Coal}\} \\
& & & 
\begin{bmatrix}
- cs_{Clean \; Energy} \\
- cs_{Clean \; Transportation} \\
- cs_{Buildings \; Efficiency} \\
CI
\end{bmatrix}^T x(t) \leq \begin{bmatrix} - (1 + G(t)) \cdot \begin{bmatrix} b_{Clean \; Energy}(t_0) \\
b_{Clean \; Transportation}(t_0) \\
b_{Buildings \; Efficiency}(t_0)
\end{bmatrix} \\
(1 - \mathfrak{R}_{CI}(t_0,t))CI(b(t_0))
\end{bmatrix}
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

### Integrating Carbon Footprint Dynamics

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

### Sector-Consistent Alignment

While we've seen in the previous section how to ensure portfolio alignment with an intensity decarbonization pathway based on a NZE scenario, one should question the idea to use the same decarbonization pathways for all stocks in the portfolio. As we have previously seen, portfolio decarbonization should take into account sectors.

On the other side, Teske et al. (2022) have provided GICS-level decarbonization pathways. 

In what follows, we show how to perform portfolio alignment at sector level.

We now assume that we want to reduce the carbon footprint at the sector level. In this case, we can denote by $CI(x; Sector_j)$ the carbon intensity of the $j^{th}$ sector, with (Roncalli, 2023):

\begin{equation}
CI(x;Sector_j) = \sum_{i \in Sector_j} \tilde{x_i} CI_i
\end{equation}

With $\tilde{x}_i$ the normalized weight in the sector bucket, such as:

\begin{equation}
\tilde{x}_i = \frac{x_i}{\sum_{k \in Sector_j}x_k}
\end{equation}

Equivalently:

\begin{equation}
CI(x;Sector_j) = \frac{(s_j \circ CI)^T x}{s^T_j x}
\end{equation}

With $a \circ b$ is the Hadamard product (element-wise product): $(a \circ b)_i = a_ib_i$.

Imposing a portfolio alignment at the sector level is equivalent to modify the constraint to become:

\begin{equation}
CI(x(t); Sector_j) \leq (1 - \mathfrak{R}_{CI}(t_0,t;Sector_j))CI(b(t_0;Sector_j))
\end{equation}

In order to find the QP form to integrate into our problem, we need a few transformations (because we need to find the form $G^Tx \leq h$):

\begin{equation}
(*) ↔ CI(x(t); Sector_j) \leq (1 - \mathfrak{R}_{CI}(t_0,t;Sector_j))CI(b(t_0;Sector_j))
\end{equation}

\begin{equation}
↔ (s_j \circ CI)^T x \leq (1 - \mathfrak{R}_{CI}(t_0,t;Sector_j))CI(b(t_0;Sector_j))(s_j^T x)
\end{equation}

\begin{equation}
↔ ((s_j \circ CI) - (1 - \mathfrak{R}_{CI}(t_0,t;Sector_j))CI(b(t_0;Sector_j)) s_j)^T x \leq 0
\end{equation}

\begin{equation}
↔ (s_j \circ (CI - (1 - \mathfrak{R}_{CI}(t_0,t;Sector_j))CI(b(t_0;Sector_j))^T x \leq 0
\end{equation}

We thus have:

\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \; \frac{1}{2} (x(t)-b^{augmented}(t))^T \Sigma(t)(x(t)-b^{augmented}(t))\\
& \text{subject to}
& & 1_u^Tx(t) = 1\\
& & &  0_u \leq x(t) \leq \mathbb{1}\{i \notin \text{Oil or Coal}\} \\
& & & 
\begin{bmatrix}
- cs_{Clean \; Energy} \\
- cs_{Clean \; Transportation} \\
- cs_{Buildings \; Efficiency} \\
(s_{Energy} \circ (CI^{Trend} - (1 - \mathfrak{R}_{CI}(t_0,t;Energy))CI(b(t_0;Energy)) \\
(s_{Utilities} \circ (CI^{Trend} - (1 - \mathfrak{R}_{CI}(t_0,t;Utilities))CI(b(t_0;Utilities)) \\
(s_{Cement} \circ (CI^{Trend} - (1 - \mathfrak{R}_{CI}(t_0,t;Cement))CI(b(t_0;Cement)) \\
(s_{Steel} \circ (CI^{Trend} - (1 - \mathfrak{R}_{CI}(t_0,t;Steel))CI(b(t_0;Steel)) \\
(s_{Chemicals} \circ (CI^{Trend} - (1 - \mathfrak{R}_{CI}(t_0,t;Chemicals))CI(b(t_0;Chemicals)) \\
(s_{Textile \; \& \; Leather} \circ (CI^{Trend} - (1 - \mathfrak{R}_{CI}(t_0,t;Textile \; \& \; Leather))CI(b(t_0;Textile \; \& \; Leather)) \\
(s_{Aluminium} \circ (CI^{Trend} - (1 - \mathfrak{R}_{CI}(t_0,t;Aluminium))CI(b(t_0;Aluminium)) \\
(s_{Buildings} \circ (CI^{Trend} - (1 - \mathfrak{R}_{CI}(t_0,t;Buildings))CI(b(t_0;Buildings)) \\
(s_{Food \; Processing} \circ (CI^{Trend} - (1 - \mathfrak{R}_{CI}(t_0,t;Food \; Processing))CI(b(t_0;Food \; Processing)) \\
(s_{Others} \circ (CI^{Trend} - (1 - \mathfrak{R}_{CI}(t_0,t;Others))CI(b(t_0;Others))
\end{bmatrix}^T x(t) \leq \begin{bmatrix} - (1 + G(t)) \cdot \begin{bmatrix} b_{Clean \; Energy}(t_0) \\
b_{Clean \; Transportation}(t_0) \\
b_{Buildings \; Efficiency}(t_0)
\end{bmatrix} \\
0 \\
0 \\
0\\
0\\
0 \\
0 \\
0 \\
0 \\
0 \\
0
\end{bmatrix}
\end{aligned}
\end{equation*}


### Key Takeaways

- Portfolio alignment with a decarbonization pathway, such as the methodology proposed by Barahhou et al. (2022), derived from a NZE scenario, is a dynamic exercice by nature

- Thus portfolio alignment changed the nature of the decarbonized portfolio problem, making it dynamic

- Portolio alignment can be conducted at sector level
