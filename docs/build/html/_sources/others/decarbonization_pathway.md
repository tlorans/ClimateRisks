
# Decarbonization Pathway

In this part, we will give a definition of a net zero emissions (NZE) scenario with the carbon budget constraint and study the relationship between a NZE scenario and a decarbonization pathway. Then, we will see how to derive an intensity decarbonization pathway from an emissions scenario.

## Net Zero Emissions Scenario

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

## Decarbonization Pathway

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
