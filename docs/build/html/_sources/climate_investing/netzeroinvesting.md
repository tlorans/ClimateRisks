# Net Zero Investing

Before the surge of net zero investors, insurers and asset managers alliances, climate investing mainly involved decarbonizing portfolios or constructing low-carbon indices with the low-carbon strategy that we have seen in the first part of this course.

But, as stated by Barahhou et al. (2022) {cite:p}`barahhou2022net`, net zero investing has changed the scope of climate investing, as the corresponding strategy cannot be considered as a simple tilt of a business-as-usual portfolio.

Indeed, according to the framework proposed by Barahhou et al. (2022), a net zero portfolio:

- starts with a sound decarbonization pathway of a net zero emissions scenario
- has a dynamic decarbonization dimension, respecting the endogenous aspect of the decarbonization pathway and implying self-decarbonization of the portfolio
- encompasses the transition dimension, to ensure that the portfolio is financing the transition towards a low-carbon economy

The purpose of this part is to give you an overview of the net zero portfolio construction framework proposed by Barahhou et al. (2022). 

Net zero portfolio starts with a net zero emissions scenario, which is a physical concept, based on carbon budget. We will see how to assess a decarbonization pathway compliance to a net zero objective, and how to derive the portfolio's decarbonization (based on carbon intensity) pathway from it.

Net zero portfolio implies self-decarbonization rather than sequential decarbonization (meaning decarbonization based on rebalancement only). We will see how to determine from which component portfolio's decarbonization comes from, leading to the notion of net zero backtesting. We will see that adding carbon footprint dynamics metric helps in improving the self-decarbonization property of the portfolio.

Finally, the net zero portfolio integrates the transition dimension. We will see how a green intensity measure can help in ensuring that the portfolio contributes to the transition towards a low-carbon economy.

In all these dimensions, we will compare the approach promoted by the Paris-Aligned Benchmarks framework to the framework proposed by Barahhou et al. (2022).

## Decarbonization Pathway

A net zero investment portfolio starts with a Net Zero Emissions (NZE) scenario. A decarbonization pathway summarizes the NZE scenario.

The decarbonization pathway has two statuses (Barahhou et al., 2022):
- it is the exogenous pathway that the economy must follow to limit the probability of reaching 1.5°C
- it becomes the endogenous pathway if the world closes the gap between current and needed invetments to finance transition to a low-carbon economy

In this part, we will give a definition of a NZE scenario with the carbon budget constraint and study the relationship between a NZE scenario and a decarbonization pathway. Then, we will see how to derive an intensity decarbonization pathway from an emissions scenario.

### Carbon Budget Constraint

As stated by Barahhou et al. (2022), a net zero emissions (NZE) scenario corresponds to an emissions scenario, which is compatible with a carbon budget. 
The carbon budget defines the amount of CO2eq emissions produced over the time period $[t_0,t]$ for a given emissions scenario. 

As an example, the IPCC (2018) {cite:p}`masson2018global` gives an estimate of a remaining carbon budget of 580 GtC02eq for a 50% probability of limiting the warming to 1.5°C. The objective is to limit the global warming to 1.5°C while the corresponding carbon budget is 580 GTCO2eq.

More formally, a NZE scenario can be defined by a carbon pathway that satisfies the following constraints (Barahhou et al., 2022):

\begin{equation}
CB(t_0, 2050) \leq CB^+
\end{equation}
\begin{equation}
CE(2050) \approx 0
\end{equation}

With $CE(t)$ the global carbon emissions at time $t$, $CB(t_0,t)$ the global carbon budget between $t_0$ and $t$ and $CB^+$ the maximum carbon budget to attain a given objective of global warming mitigation. If we consider the AR5 results of IPCC (2018), we can set $CB^+ = 580$.

A NZE scenario and the corresponding decarbonization pathway must thus comply with the carbon budget constraint above, with a carbon emissions level in 2050 close to 0.
#### Decarbonization Pathway

A decarbonization pathway is structured among the following parameters (Barahhou et al. 2022):
1. An average yearly reduction rate $\Delta \mathfrak{R}$ 
2. A minimum carbon reduction $\mathfrak{R}^-$

A decarbonization pathway is then defined as:

\begin{equation}
\mathfrak{R}(t_0,t) = 1 - (1 - \Delta \mathfrak{R})^{t-t_0}(1 - \mathfrak{R^-})
\end{equation}


Where $t_0$ is the base year, $t$ the year index and $\mathfrak{R}(t_0,t)$ is the reduction rate of the carbon emissions between $t_0$ and $t$.


Let's make an example of a decarbonization pathway in Python. We first create a dataclass `DecarbonizationPathway`:
```Python
from dataclasses import dataclass
import numpy as np

@dataclass 
class DecarbonizationPathway:

  delta_R:float # Average yearly reduction rate
  R_min:float # Minimum reduction rate

  def get_decarbonization_pathway(self, t_0:int, t:int):
    pathway = []
    for i in range(t_0,t+1):
      r = 1 - (1 - self.delta_R)**(i-t_0)*(1 - self.R_min)
      pathway.append(r)
    
    return pathway
```

Then instantiate it with $\Delta \mathfrak{R} = 0.07$ and $\mathfrak{R}^- = 0.3$:

```Python
test = DecarbonizationPathway(delta_R = 0.07, R_min = 0.3)
pathway = test.get_decarbonization_pathway(t_0 = 2020, t = 2050)
```
We can then plot the results:

```Python
import matplotlib.pyplot as plt 

plt.plot([i for i in range(2020, 2050 + 1)], pathway)
plt.ylabel("Reduction rate")
plt.figure(figsize = (10, 10))
plt.show()
```

```{figure} reductionrate.png
---
name: reductionrate
---
Figure: Decarbonization Pathway with $\Delta \mathfrak{R} = 0.07$ and $\mathfrak{R}^- = 0.30$
```

Starting with the decarbonization pathway, we can deduce the emissions scenario (Barahhou et al., 2022):

\begin{equation}
CE(t) = (1 - \Delta \mathfrak{R})^{t - t_0}(1 - \mathfrak{R}^-) CE(t_0)
\end{equation}

We can add a new method to the `DecarbonizationPathway` dataclass:
```Python
from dataclasses import dataclass
import numpy as np

@dataclass 
class DecarbonizationPathway:

  delta_R:float # Average yearly reduction rate
  R_min:float # Minimum reduction rate

  def get_decarbonization_pathway(self, t_0:int, t:int):
    pathway = []
    for i in range(t_0,t+1):
      r = 1 - (1 - self.delta_R)**(i-t_0)*(1 - self.R_min)
      pathway.append(r)      
    
    return pathway

  def get_emissions_scenario(self, t_0:int, t:int, CE_start:float):
    scenario = [CE_start]
    for i in range(t_0, t+1):
      ce = (1 - self.delta_R)**(i - t_0) * (1 - self.R_min) * CE_start
      scenario.append(ce)

    return scenario
```

And then compute the emissions scenario and plot the results:
```Python
test = DecarbonizationPathway(delta_R = 0.07, R_min = 0.3)
scenario = test.get_emissions_scenario(t_0 = 2020, t = 2050, CE_start = 36)

import matplotlib.pyplot as plt 

plt.plot([i for i in range(2019, 2050 + 1)], scenario)
plt.ylabel("Carbon Emissions (GtC02eq)")
plt.figure(figsize = (10, 10))
plt.show()
```

```{figure} emissionsscenario.png
---
name: emissionscenario
---
Figure: Carbon Emissions Scenario with $\Delta \mathfrak{R} = 0.07$ and $\mathfrak{R}^- = 0.30$
```

#### From Decarbonization Pathway to Carbon Budget

From Le Guenedal et al. (2022 {cite:p}`le2022net`), we can find the corresponding carbon budget with a given value for $\mathfrak{R}^-$, $\Delta \mathfrak{R}$ and $CE(t_0)$ with:

\begin{equation}
CB(t_0,t) = (\frac{(1 - \Delta \mathfrak{R})^{t-t_0} - 1}{ln(1 - \Delta \mathfrak{R})})(1 - \mathfrak{R}^-)CE(t_0)
\end{equation}

We can add a new method to the `DecarbonizationPathway` dataclass:
```Python
@dataclass 
class DecarbonizationPathway:

  delta_R:float # Average yearly reduction rate
  R_min:float # Minimum reduction rate

  def get_decarbonization_pathway(self, t_0:int, t:int):
    pathway = []
    for i in range(t_0,t+1):
      r = 1 - (1 - self.delta_R)**(i-t_0)*(1 - self.R_min)
      pathway.append(r)      
    
    return pathway

  def get_emissions_scenario(self, t_0:int, t:int, CE_start:float):
    scenario = [CE_start]
    for i in range(t_0, t+1):
      ce = (1 - self.delta_R)**(i - t_0) * (1 - self.R_min) * CE_start
      scenario.append(ce)

    return scenario
    
  def get_carbon_budget(self, t_0:int, t:int, CE_start:float):
    return ((1 - self.delta_R)**(t - t_0) - 1)/(np.log(1 - self.delta_R))*(1 - self.R_min)*CE_start
```

With a given decarbonization pathway, we can then estimate $CB(t_0,2050)$ and $CE(2050)$ to check if the carbon budget holds. In our previous example we have:

```Python
test = DecarbonizationPathway(delta_R = 0.07, R_min = 0.3)
test.get_carbon_budget(t_0 = 2020, t = 2050, CE_start = 36)
```
```
307.8810311773137
```
Which is less than $CB^+$.

And:
```Python
test.get_emissions_scenario(t_0 = 2020, t = 2050, CE_start = 36)[-1]
```
```
2.8568602567587567
```
Which is close to zero.

We then can say that in previous example, the decarbonization pathway complies with the carbon budget constraint for a NZE scenario.
### Decarbonization Pathway for Portfolio

If a decarbonization pathway is generally valid for an economy or a country, we must have in mind that it is defined in terms of absolute carbon emissions. However, portfolio decarbonization uses carbon intensity, and not absolute carbon emissions. We thus need to introduce the relationship of carbon emissions and carbon intensity pathway.

#### Carbon Emissions and Carbon Intensity Pathway Relationship

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
plt.plot([i for i in range(2020, 2050 + 1)], pathway)
plt.ylabel("Reduction rate")
plt.figure(figsize = (10, 10))
plt.show()
```

```{figure} financialpathway.png
---
name: financialpathway
---
Figure: Financial decarbonization pathway with $\Delta \mathfrak{R}_{CE} = 0.07$ and $g_Y = 0.03$
```

#### From Economic to Financial Decarbonization Pathway

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

import matplotlib.pyplot as plt 

plt.plot(full_years, reduction_rate)
plt.ylabel("Reduction rate")
plt.figure(figsize = (10, 10))
plt.show()
```

```{figure} ieareductionrate.png
---
name: reductionrate
---
Figure: Decarbonization pathway $\mathfrak{R}_{CE}(2020,2050)$ from the IEA scenario
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

plt.plot(full_years, intensity_reduction)
plt.ylabel("Intensity reduction rate")
plt.figure(figsize = (10, 10))
plt.show()
```


```{figure} intensityieareductionrate.png
---
name: intensityieareductionrate
---
Figure: Financial decarbonization pathway $\mathfrak{R}_{CI}(2020,2050)$ from the IEA scenario, with $g_Y = 0.03$
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

We can see that the PAB financial decarbonization pathway is far too much aggressive compared with the IEA deduced pathway.

### Key Takeaways

- Net Zero Emissions scenario is a carbon pathway with a resulting carbon budget compliant with global warming mitigation objective

- Portfolio decarbonization pathway uses carbon intensity decarbonization pathway rather than carbon emissions pathway

- We can deduce financial decarbonization pathway from an economic decarbonization pathway, starting with a NZE scenario

- PAB's intensity decarbonization pathways is far more aggressive than the intensity decarbonization pathway deduced from the IEA NZE scenario


## Portfolio Alignment

We've seen in the low-carbon strategy framework how investors can conduct a portfolio decarbonization with a static approach, compared to a reference universe. On the other side, net zero investing involves portfolio alignment with a decarbonization pathway $\mathfrak{R}_{CI}(t_0,t)$. Because we introduce a pathway between $t_0$ and $t$, the problem now involves a dynamic strategy.

Furthermore, a net zero investing strategy needs to include a mechanism that respect the endogenous aspect of the decarbonization pathway. In particular, a net zero portfolio implies the self-decarbonization of the portolio to respect the endogenous aspect of the decarbonization pathway, as stated by Barahhou et al. (2022).

In this part, we are going to compare the approach for performing a portfolio alignment with the Paris-Aligned Benchmarks (PAB) and the net zero investment portfolio framework proposed by Barahhou et al. (2022). Introducing the concept of Net Zero Backtesting, we'll see that the dynamic decarbonization in the PAB relies on sequential decarbonization rather than self-decarbonization, because the issuers' carbon footprint dynamics are not taken into account. We will introduce a carbon footprint dynamic measure, following Barahhou et al. (2022), in order to maximize the self-decarbonization property of the net zero portfolio. 

### Dynamic Portfolio's Decarbonization

Let's first address the PAB approach of the dynamic portfolio decarbonization. 

At date $t$, the PAB label imposes the following inequality constraint for the portfolio $x(t)$:

\begin{equation}
CI(x(t)) \leq (1 - \mathfrak{R}_{CI}(t_0,t))CI(b(t_0))
\end{equation}

The base year $t_0$ thus defines the reference level of the carbon intensity, as the reference level is $CI(b(t_0))$ and not $CI(b(t))$. This is a first important difference compared to the low-carbon strategy.

In this case, the decarbonization problem becomes dynamic (Barahhou et al., 2022):
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


We can see that, with the assumption that the world doesn't change, we cannot find optimal solution after 2036. 
Furthermore, dynamic decarbonization leads to progressive deviation from the benchmark, and then to explosive tracking error volatility.

### Net Zero Backtesting

The objective of net zero investment portfolio, according to the framework proposed by Barahhou et al. (2022), is to promote self-decarbonization rather than sequential decarbonization (ie. decarbonization obtained by the dynamic of the issuers' decarbonization rather than with successive or sequential decarbonization obtained by rebalancement). Indeed, as stated by Barahhou et al. (2022), net zero investing must include a mechanism that respects the endogenous aspect of the decarbonization pathway. If the time-varying decarbonization is only due to rebalancing process, it is clear that the portfolio cannot be claim to be net zero.

Let $CI(t,x;I_t)$ be the carbon intensity of portfolio $x$ calculated at time $t$ with the information $I_t$ available at time $t$. The portfolio $x(t)$'s WACI must satisfy the following constraint (Barahhou et al., 2022):

\begin{equation}
CI(t, x(t); I_t) \leq (1 - \mathfrak{R}_{CI}(t_0,t))CI(t_0,b(t_0); I_{t_0})
\end{equation}

Where $b(t_0)$ is the benchmark at time $t_0$. 

Let's know formulate this same constraint, but taking into account the fact that the portfolio is rebalanced at time $t+1$ and we will choose a new portfolio $x(t+1)$. The new constraint is then:

\begin{equation}
CI(t + 1, x(t+1); I_{t+1}) \leq (1 - \mathfrak{R}_{CI}(t_0, t+1))CI(t_0, b(t_0);I_{t_0})
\end{equation}

The information on the right hand scale are known (because we only need information from the starting date $I_{t_0}$). The information on the left hand scale depends on the information available in the future rebalance date $I_{t+1}$. We don't have to rebalance (ie. adding carbon reduction by new sequential decarbonization in order to respect the constraint) if:

\begin{equation}
CI(t + 1, x(t); I_{t+1}) \leq (1 - \mathfrak{R}_{CI}(t_0, t+1))CI(t_0, b(t_0);I_{t_0})
\end{equation}

That is if the portfolio $x(t)$ (before the rebalance in $t+1$) has a WACI in $t+1$ that respect the constraint. If not, we need to rebalance in $t+1$ in order to obtain a new set of weights and a new portfolio $x(t+1)$.

The variation between two rebalancing dates $CI(t+1, x(t + 1);I_{t+1}) - CI(t, x(t), I_t)$ is decomposed between two components:

1. The self-decarbonization $CI(t+1, x(t);I_{t+1}) - CI(t, x(t), I_t)$ (the decarbonization due to issuers' self-decarbonization)
2. The additional decarbonization with sequential decarbonization $CI(t+1, x(t + 1);I_{t+1}) - CI(t + 1, x(t), I_{t+1})$ (the decarbonization achieved by rebalancing the portfolio from $x(t)$ to $x(t+1)$)

The self-decarbonization ratio is finally defined as (Barahhou et al., 2022):

\begin{equation}
SR(t+1) = \frac{CI(t, x(t);I_{t}) - CI(t + 1, x(t), I_{t+1})}{CI(t, x(t);I_{t}) - CI(t + 1, x(t + 1), I_{t+1})}
\end{equation}

The higher value for the self-decarbonization ratio $SR(t+1)$ is reached when we do not have to rebalance the portfolio, with the decarbonization achieved through self-decarbonization rather than sequential decarbonization. This is a first step towards the backesting of net zero portoflios. 

To maximize the self-decarbonization ratio, we need to have an idea about the dynamics of the carbon footprint, that is an estimate of $CI(t+1, x(t); I_t)$.

To illustrate this concept of net zero backtesting with the use of the self-decarbonization ratio, let's take this example from Barahhou et al. (2022):

| $s$  | $(1 - \mathfrak{R}_{CI}(t_0, s))CI(t_0, b(t_0);I_{t_0})$ | $CI(s, x(s); I_s)$ | $CI(s + 1, x(s); I_{s+1})$ |   
|---|---|---|---|
|t| 100.0  | 100.0  | 99.0  |  
|t + 1| 93.0  | 93.0  | 91.2  | 
|t + 2| 86.5  | 86.5  | 91.3  | 
|t + 3| 80.4  | 80.4  | 78.1  | 
|t + 4| 74.8  | 74.8  | 74.2  | 
|t + 5| 69.6  | 69.6  | 70.7  | 
|t + 6| 64.7  | 64.7  | 62.0  | 
|t + 7| 60.2  | 60.2  | 60.0  | 
|t + 8| 55.9  | 55.9  | 58.3  | 
|t + 9| 52.0  | 52.0  | 53.5  | 
|t + 10| 48.4  | 48.4  | 50.5  | 

Let's apply this example in Python. First, we create a `NetZeroBacktesting` with the methods we need:
```Python

@dataclass 
class NetZeroBacktesting:

  CI_s_star: np.array # Targets
  CI_s_x: np.array # Carbon Intensity of the portfolio x at s
  CI_s_plus_one_x: np.array # Carbon intensity of the portfolio x at s+1

  def get_self_decarbonization_ratio(self):
    sr_s = []

    for t in range(len(self.CI_s_star)-1):
      sr = (self.CI_s_x[t] - self.CI_s_plus_one_x[t]) / (self.CI_s_x[t] - self.CI_s_x[t+1])
      sr_s.append(sr)
    
    return sr_s

  def get_self_decarbonization(self):
    return [self.CI_s_plus_one_x[t] - self.CI_s_x[t] for t in range(0, len(self.CI_s_x) - 1)]
    
  def get_sequential_decarbonization(self):
    return [self.CI_s_x[t+1] - self.CI_s_plus_one_x[t] for t in range(0, len(self.CI_s_x)-1)]
```

Then we can implement our example:
```Python
CI_s_star = [100.0, 93.0, 86.5, 80.4, 74.8, 69.6, 64.7, 60.2, 55.9, 52.0, 48.4]
CI_s_x =  [100.0, 93.0, 86.5, 80.4, 74.8, 69.6, 64.7, 60.2, 55.9, 52.0, 48.4]
CI_s_plus_one_x = [99.0, 91.2, 91.3, 78.1, 74.2, 70.7, 62.0, 60.0, 58.3, 53.5, 50.5]

test = NetZeroBacktesting(CI_s_star = CI_s_star,
                          CI_s_x = CI_s_x,
                          CI_s_plus_one_x = CI_s_plus_one_x)
```

And let's plot the results:

```Python
self_decarbonization = np.array(test.get_self_decarbonization())
negative_decarbonization = np.zeros(len(self_decarbonization))
negative_decarbonization[np.where(self_decarbonization > 0)] = self_decarbonization[np.where(self_decarbonization > 0)]
self_decarbonization[np.where(self_decarbonization > 0)] = 0
sequential_decarbonization = np.array(test.get_sequential_decarbonization())

import matplotlib.pyplot as plt 

s = ["t+1","t+2", "t+3","t+4","t+5","t+6","t+7","t+8","t+9","t+10"]

fig, ax = plt.subplots()
fig.set_size_inches(10, 10)

ax.bar(s, sequential_decarbonization, label='Sequential decarbonization', color ='b')
ax.bar(s, self_decarbonization,
       label='Self-decarbonization', color = 'g')
ax.bar(s, negative_decarbonization,
       label='Negative decarbonization', color = 'r')
ax.legend()
```

```{figure} nzebacktestingsequential.png
---
name: nzebacktestingsequential
---
Figure: Sequential versus self-decarbonization
```

In this example, we can see that almost all yearly portfolio decarbonization comes from the rebalancement process (sequential decarbonization). This is typically what we can expect by applying the PAB methodology. Indeed, because the PAB approach doesn't integrate any information about carbon footprint dynamics, the PAB's decarbonization is almost entirely due to sequential decarbonization.

### Integrating Carbon Footprint Dynamics

In the previous section, we have performed a portfolio alignment by considering a global decarbonization path for the portfolio, as recommended by the PAB approach. In this section, we consider the decarbonization path of the issuers, as in Le Guenedal and Roncalli (2022 {cite:p}`le2022portfolio`) and Barahhou et al. (2022). This approach should help in improving the self-decarbonization ratio of the portfolio.

In order to have an idea of the potential issuers carbon footprint dynamics, we can exploit the historical trajectory of the past carbon emissions. We can therefore, as Roncalli et al. (2022), estimate the associated linear trend model and project the future carbon emissions by assuming that the issuer will do the same efforts in the future than in the past.

Le Guenedal et and Roncalli (2022) define the carbon trend by considering the following linear constant trend model:

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
\beta'_0 = \beta_° + \beta_1 t_0
\end{equation}

and 

\begin{equation}
\beta'_1 = \beta_1
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

### Key Takeaways 

- Net zero portfolios introduce the notion of portfolio alignment, with a dynamic decarbonization compared to a reference base year. This contrasts with the low-carbon strategy.

- Barahhou et al. (2022) introduced the concept of net zero backtesting: as net zero investing promotes self-decarbonization rather than sequential decarbonization, investors need to be able to verify where does the portfolio's decarbonization comes from, with the self-decarbonization ratio for example.

- Improving the self-decarbonization ratio calls for the integration of issuers' carbon footprint dynamics. It constrats with the PAB's approach, that doesn't include any forward-looking information. PAB's decarbonization comes almost entirely from sequential decarbonization.

- We introduce a measure of carbon footprint dynamics in our optimization problem, that could help in improving the self-decarbonization ratio.


## Integrating the Transition Dimension

While we've addressed the decarbonization dimension in the previous part, net zero portfolio needs also to integrate the transition dimension. Indeed, one of the main objective of a net zero investor is to finance the transition to a low-carbon economy (Barahhou et al., 2022).


The PAB addresses the transition dimension by imposing a weight constraint on what is defined as climate impact sectors. However, using the green intensity measure proposed by Barahhou et al. (2022), it has been observed that the PAB constraint has no positive impact on the resulting green intensity. 

Furthermore, Barahhou et al. (2022) observed a negative relationship between the decarbonization and the transition dimensions. This negative relationship calls for the inclusion of a green intensity constraint.

### Controlling for Climate Impact Sectors

The PAB label requires the portfolio's exposure to sectors highly exposed to climate change to be at least equal to the exposure in the investment universe. According to the TEG (2018 {cite:p}`hoepner2018teg`, 2019 {cite:p}`hoepner2019handbook`), we can distinguish two types of sectors:

1. High climate impact sectors (HCIS or $CIS_{High}$)
2. Low climate impact sectors (LCIS or $CIS_{Low}$)

The HCIS are sectors that are identified as key to the low-carbon transition. They corresponds to the following NACE classes:
- A. Agriculture, Forestry and Fishing
- B. Mining and Quarrying
- C. Manufacturing
- D. Electricity, Gas, Steam and Air Conditioning Supply
- E. Water Supply, Sewerage, Waste Management and Remediation Activities
- F. Construction
- G. Wholesale and Retail Trade, Repair of Motor Vehicles and Motorcycles
- H. Transportation and Storage
- L. Real Estate Activities

We have $CIS_{High}(x) = \sum_{i \in CIS_{High}}x_i$ the HCIS weight of the portfolio $x$. At each rebalancing date $t$, we must verify that:

\begin{equation}
CIS_{High}(x(t)) \geq  CIS_{High}(b(t))
\end{equation}

The PAB's optimization problem becomes (Le Guenedal and Roncalli, 2022):

\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2} (x(t)-b(t))^T \Sigma(t)(x(t)-b(t))\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & &  0_n \leq x \leq 1_n \\
& & & CI(x(t)) \leq (1 - \mathfrak{R}_{CI}(t_0,t))CI (b(t_0)) \\
& & & CIS_{High}(x(t)) \geq CIS_{High}(b(t))
\end{aligned}
\end{equation*}

Regarding the QP parameters, the last two constraints can be casted into $Gx \leq h$ with:

\begin{equation}
G = \begin{bmatrix}
CI^T \\
- CIS_{High}^T
\end{bmatrix}
\end{equation}

and 

\begin{equation}
h = \begin{bmatrix}
(1 - \mathfrak{R}_{CI}(t_0,t))CI (b(t_0)) \\
- CIS_{High}(b(t))
\end{bmatrix}
\end{equation}

### Financing the Transition

If the idea behing the concept of HCIS in the PAB approach was to ensure that the resulting portfolio promotes activities contributing to the low-carbon transition, the constraint applied at the portfolio level has many drawbacks. Indeed, the constraint tends to encourages substitutions between sectors or industries and not substitutions between issuers within a same sector. As stated by Barahhou et al. (2022), the trade-off is not between green electricity and brown electricity for example, but between electricity generation and health care equipment. This approach doesn't contribute to financing the transition, which is an objective of a net zero portfolio. To assess if a portfolio is really contributing to the low-carbon transition, Barahhou et al. (2022) propose a green intensity measure. 

A green intensity measure starts with a green taxonomy. The most famous example is the European green taxonomy. Developed by the TEG (2020 {cite:p}`eutaxo2020`), the EU green taxonomy defines economic activities which make a contribution to environmental objectives while do no significant harm to the other environmental objectives (DNSH constraint) and comply with minimum social safeguards (MS constraint). Other taxonomies exist, such as the climate solutions listed by the Project Drawdown (2017 {cite:p}`hawken2017drawdown`) for each important sectors. Proprietary taxonomies from data vendors can also be used.

A bottom-up approach to measure the green intensity of a portfolio starts with the green revenue share at the issuer level:

\begin{equation}
GI_i = \frac{GR_i}{TR_i}
\end{equation}

Where $GR_i$ and $TR_i$ are respectively the green revenues and the total turnover of the issuer $i$.

The green intensity of the portfolio is then:

\begin{equation}
GI(x) = \sum^n_{i=1}x_i \cdot GI_i
\end{equation}

### Controlling for Green Intensity

As Barahhou et al. (2022) observed, there is a decreasing function between the green intensity and the reduction level. This negative correlation between decarbonization and transition dimensions calls for the introduction of a green intensity constraint. This is for preventing the aligned portfolios from having a lower green intensity.

We finally add the green intensity constraint to our previous optimization problem that includes the carbon footprint dynamics (Barahhou et al., 2022):
\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2} (x(t)-b(t))^T \Sigma(t)(x(t)-b(t))\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & &  0_n \leq x \leq 1_n \\
& & & CI^{Trend}(x(t)) \leq (1 - \mathfrak{R}_{CI}(t_0,t))CI(b(t_0)) \\
& & & GI(t,x) \geq (1 + G(t)) \cdot GI(t_0, b(t_0))
\end{aligned}
\end{equation*}

With $G(t)$ is a greeness multiplier. The underlying idea is to maintain a green intensity for the net zero portfolio that is higher than the green intensity of the benchmark.

### Key Takeaways

- Financing the transition is one of the objective of net zero portfolios
- PAB approach to integrate the transition dimension relies on the HCIS constraint
- A measure to assess the contribution to the transition to a low-carbon economy has been proposed by Barahhou et al. (2022): the green intensity
- The HCIS constraint from the PAB falls short in improving the green intensity of the portoflio compared to the benchmark, and then underlies failures in the PAB's integration of the transition dimension
- In fact, the decarbonization and the transition dimensions seems to be negatively correlated
- This negative correlation calls for the direct inclusion of a green intensity constraint for net zero portfolios construction