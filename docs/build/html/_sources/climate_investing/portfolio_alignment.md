## Portfolio Alignment with a Sound Decarbonization Pathway

We've seen in the previous part that traditional carbon risk hedging strategy involves static portfolio decarbonization.

However, as stated by Barahhou et al. (2022), net zero investing changed the static dimension of climate investing by highlighting the need for portfolio alignment to a sound decarbonization pathway. As a decarbonization pathway is by nature dynamic, a portfolio alignment strategy calls for the implementation of a dynamic strategy.

In the first section, we will focus on the concept of decarbonization pathway. Then, we will show how to implement a dynamic portfolio decarbonization strategy, in line with a decarbonization pathway.


### What is a Sound Decarbonization Pathway?

A net zero investment portfolio starts with a Net Zero Emissions (NZE) scenario. A decarbonization pathway summarizes the NZE scenario.

The decarbonization pathway has two statuses (Barahhou et al., 2022):
- it is the exogenous pathway that the economy must follow to limit the probability of reaching 1.5°C
- it becomes the endogenous pathway if the world closes the gap between current and needed invetments to finance transition to a low-carbon economy

In this part, we will give a definition of a NZE scenario with the carbon budget constraint and study the relationship between a NZE scenario and a decarbonization pathway. Then, we will see how to derive an intensity decarbonization pathway from an emissions scenario.

#### Carbon Budget Constraint

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

##### Decarbonization Pathway

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

##### From Decarbonization Pathway to Carbon Budget

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

#### Decarbonization Pathway for Portfolio

If a decarbonization pathway is generally valid for an economy or a country, we must have in mind that it is defined in terms of absolute carbon emissions. However, portfolio decarbonization uses carbon intensity, and not absolute carbon emissions. We thus need to introduce the relationship of carbon emissions and carbon intensity pathway.

##### Carbon Emissions and Carbon Intensity Pathway Relationship

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

##### From Economic to Financial Decarbonization Pathway

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



### Portfolio Alignment as a Dynamic Portfolio Decarbonization

We've seen in the low-carbon strategy framework how investors can conduct a portfolio decarbonization with a static approach, compared to a reference universe. On the other side, net zero investing involves portfolio alignment with a decarbonization pathway $\mathfrak{R}_{CI}(t_0,t)$. Because we introduce a pathway between $t_0$ and $t$, the problem now involves a dynamic strategy.

#### Dynamic Portfolio's Decarbonization

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

### Key Takeaways

- Net Zero Emissions scenario is a carbon pathway with a resulting carbon budget compliant with global warming mitigation objective

- Portfolio decarbonization pathway uses carbon intensity decarbonization pathway rather than carbon emissions pathway

- We can deduce financial decarbonization pathway from an economic decarbonization pathway, starting with a NZE scenario

- PAB's intensity decarbonization pathways is far more aggressive than the intensity decarbonization pathway deduced from the IEA NZE scenario
