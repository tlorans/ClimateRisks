# Portfolio Decarbonization Pathway

If a decarbonization pathway is generally valid for an economy or a country, we must have in mind that it is defined in terms of absolute carbon emissions. However, portfolio decarbonization uses carbon intensity, and not absolute carbon emissions. We thus need to introduce the relationship of carbon emissions and carbon intensity pathway.

## Carbon Emissions and Carbon Intensity Pathway Relationship

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

## From Economic to Financial Decarbonization Pathway

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
