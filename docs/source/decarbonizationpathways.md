## Decarbonization Pathway

To implement a net zero investing policy, investors have to start with a net zero emissions (NZE) scenario and the corresponding decarbonization pathway. The decarbonization pathway of the NZE has two statuses:
- it is the exogenous pathway that the economy must follow to limit the probability of reaching 1.5°C
- it becomes the endoenous pathway if the world close the gap between current and needed invetments to finance transition to a low-carbon economy

In this part, we will give a definition of a NZE scenario with the carbon budget constraint and how to check if a decarbonization pathway complies with a NZE scenario. Then, we will address the portfolio's decarbonization pathway, based on carbon intensity rather than absolute emissions. 

### Carbon Budget Constraint

As stated by Barahhou et al. (2022), a net zero emissions (NZE) scenario corresponds to an emissions scenario, which is compatible with a carbon budget. 
The carbon budget defines the amount of CO2eq emissions produced over the time period $[t_0,t]$ for a given emissions scenario. The carbon budget corresponds to a certain objective of global warming mitigation.

As an example, the IPCC (2018 {cite:p}`masson2018global`) gives an estimate of a remaining carbon budget of 580 GtC02eq for a 50% probability of limiting the warming to 1.5°C. The objective is to limit the global warming to 1.5°C while the corresponding carbon budget is 580 GTCO2eq. What is missing in this statement is the corresponding emissions scenario. We will see later how to determine a carbon pathway (or emission scenario) based on a carbon budget.

More formally, a NZE scenario can then be defined by a carbon pathway that satisfies the following constraints (Barahhou et al., 2022):

\begin{equation}
CB(t_0, 2050) \leq CB^+
\end{equation}
\begin{equation}
CE(2050) \approx 0
\end{equation}

With $CE(t)$ the global carbon emissions at time $t$, $CB(t_0,t)$ the global carbon budget between $t_0$ and $t$ and $CB^+$ the maximum carbon budget to attain a given objective of global warming mitigation. If we consider the AR5 results of IPCC (2018), we can set $CB^+ = 580$.

A NZE scenario and the corresponding decarbonization pathway must thus comply with the carbon budget constraint above, with a carbon emissions level in 2050 close to 0.
#### Decarbonization Pathway

A decarbonization pathway summarizes an emissions scenario. It is structured among the following principles (Barahhou et al. 2022):
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

From Le Guenedal et al. (2022 {cite:p}`le2022net`), we can find the carbon budget with a given value for $\mathfrak{R}^-$, $\Delta \mathfrak{R}$ and $CE(t_0)$ with:

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

We then can say that our example decarbonization pathway complies with the carbon budget constraint for a NZE scenario.
### Decarbonization Pathway for Portfolio

If a decarbonization pathway is generally valid for an economy or a country, we must have in mind that it is defined in terms of absolute carbon emissions in this case. However, portfolio decarbonization uses carbon intensity, and not absolute carbon emissions. We thus need to introduce the relationship of carbon emissions and carbon intensity pathway.

#### Carbon Emissions and Carbon Intensity Pathway Relationship

The carbon intensity $CI(t)$ is defined as the ratio between the carbon emissions $CE(t)$ and a normalization variable $Y(t)$ (a physical or monetary value):

\begin{equation}
CI(t) = \frac{CE(t)}{Y(t)}
\end{equation}

If $\mathfrak{R}_{CI}(t_0)$ and $\mathfrak{R}_{CE}(t,t_0)$ are the reduction rates of carbon intensity and emissions between the base date $t_0$ and $t$, we have the following relationship:

\begin{equation}
\mathfrak{R}_{CI}(t_0,t) = \frac{g_Y(t_0,t) + \mathfrak{R}_{CE}(t_0,t)}{1 + g_Y(t_0,t)}
\end{equation}

Where $g_Y(t_0,t)$ is the growth rate of the normalization variable. As we assume that $g_Y(t_0,t) \geq 0$ and $0 \leq \mathfrak{R}_{CE}(t_0,t) \leq 1$, we have the property that the reduction rate of the carbon intensity is always greater than the reduction rate of the carbon emissions:

\begin{equation}
\mathfrak{R}_{CI}(t_0,t) \geq \mathfrak{R}_{CE}(t_0,t)
\end{equation}


The emissions decarbonization pathway $\mathfrak{R}_{CE}(t_0,t)$ is called the economic decarbonization pathway, while the intensity decarbonization pathway $\mathfrak{R}_{CI}(t_0,t)$ is called the financial decarbonization pathway.

We generally simplify the financial / economic pathway relationship by considering both the annual growth rate of normalization variable $g_{Y}$ and the annual reduction rate of carbon emissions $\Delta \mathfrak{R}_{CE}$ as constant. We then have the compound growth rate of the normalization variable:

\begin{equation}
g_Y(t_0,t) = (1 + g_Y)^{t-t_0} - 1
\end{equation}

And the carbon reduction rate as:

\begin{equation}
\mathfrak{R}_{CE}(t_0,t) = 1 - (1 - \Delta \mathfrak{R}_{CE})^{t - t_0}
\end{equation}

Then, the relationship between the financial and the economic decarbonization pathway becomes:

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

Let's compare the financial decarbonization pathway deduced from the IEA scenario to the PAB decarbonization pathway.
The PAB's intensity decarbonization is stated as:
1. A year-on-year self-decarbonization $\Delta \mathfrak{R}_{CI}$ of 7\% on average per annum, based on scope 1, 2 and 3 carbon emissions intensities.
2. A minimum carbon intensity reduction $\mathfrak{R}_{CI}^-$ at 50\% compared to the invetable universe.

This financial decarbonization pathway is thus:

\begin{equation}
\mathfrak{R}_{CI}(t_0, t) = 1 - (1 - 7\%)^{t-t_0}(1 - 50\%)
\end{equation}

```Python
# reproduce Table 2 Intensity decarbonization pathway
# page 10 in NZE integrated approach
```

PAB financial decarbonization very aggressive pathway compared to the IEA deduced pathway for the next ten years.

We will see in the next part that $\mathfrak{R}^-_{CI}$ and $\Delta \mathfrak{R}_{CI}$ are the key parameters for implementing portfolio alignment with NZE scenario. We can these parameters with the following regression model estimated by least squares:

\begin{equation}
\mathfrak{R}_{CI}(t_0,t) = f_1(t; \mathfrak{R^-}_{CI}, \Delta \mathfrak{R}_{CI}) + \epsilon(t)
\end{equation}

```Python
### compute delta R CI and R min
```

### Key Takeaways

- Net Zero Emissions Scenario is a carbon pathway with a resulting carbon budget compliant with global warming mitigation objective

- The investor can use the carbon budget constraint to check if a given decarbonization pathway corresponds to a NZE

- Portfolio decarbonization pathway use carbon intensity decarbonization pathway rather than carbon emissions pathway

- The investor can deduce an intensity decarbonization pathway from a decarbonization pathway

- PAB and CAB are ad-hoc portfolio intensity decarbonization pathways that doesn't rely on a global emissions scenario

- PAB and CAB resulting intensity decarbonization pathways are far more aggressive than the intensity decarbonization pathway deduced from the IEA Scenario