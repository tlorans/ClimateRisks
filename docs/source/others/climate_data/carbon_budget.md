## Carbon Budget, Target and Trend

In this section, we will present the foundations for building and understanding metrics proposed by Le Guenedal et al. (2022). The main tools are the carbon budget, the reduction target and the carbon trend.

The absolute carbon emissions of issuer $i$ for the scope $j$ at time $t$ is denoted as $CE_{i,j}(t)$, and is generally measured annualy, in tC02e. $j$ is omited when possible, to simplify the notation.
### Carbon Budget

A carbon budget defines the amount of GHG emissions that a country or a company produces over the time period $[t_0, t]$.

It corresponds to the area of the region bounded by the function $CE_i(t)$:

\begin{equation}
CB_i(t_0,t) = \int^t_{t_0}CE_i(s)ds
\end{equation}

This defines a gross carbon budget.

The carbon budget can be approximated with the right Riemann sum with an annual step (Le Guenedal et al. 2022), with $\Delta t = 1$:

\begin{equation}
CB_i(t_0,t) \approx \sum^{m}_{k=1}(CE_i(t_0 + k\Delta t)) \cdot \Delta t
\end{equation}

\begin{equation}
= \sum^t_{s = t_0 + 1}(CE_i(s))
\end{equation}

Let's illustrate it with an example from Le Guenedal et al. (2022) in Python:
```Python

import pandas as pd

import numpy as np

data = pd.DataFrame({'Year':[i for i in range(2010, 2021)]+[2025, 2030, 2035, 2040, 2050],
                     'Historical Emissions':[4.8, 
                                             4.950,
                                             5.100,
                                             5.175,
                                             5.175,
                                             5.175,
                                             5.175,
                                             5.100,
                                             5.025,
                                             4.950,
                                             np.nan,
                                             np.nan,
                                             np.nan,
                                             np.nan,
                                             np.nan,
                                             np.nan],
                     'Estimated Emissions':[np.nan,
                                            np.nan,
                                            np.nan,
                                            np.nan,
                                            np.nan,
                                            np.nan,
                                            np.nan,
                                            np.nan,
                                            np.nan,
                                            np.nan,
                                            4.875,
                                            4.200,
                                            3.300,
                                            1.500,
                                            0.750,
                                            0.150
                     ]
})
```

and plot a graph representation of the gross carbon budget between 2020 and 2035:

```Python
import matplotlib.pyplot as plt

plt.plot(data['Year'], data["Historical Emissions"])
plt.plot(data['Year'], data["Estimated Emissions"])
plt.scatter(data['Year'], data["Historical Emissions"])
plt.scatter(data['Year'], data["Estimated Emissions"])
plt.axvline(2020, color='r') # vertical
plt.axvline(2035, color='r') # vertical
plt.fill_between(
    data["Year"],
    data["Estimated Emissions"],
    where = (data["Year"] >= 2020) & (data["Year"] <= 2035),
    alpha = 0.2
)
plt.ylim(ymin=0)
plt.ylabel("Carbon Emissions")
plt.figure(figsize = (10, 10))
plt.show()
```
```{figure} gross_carbon_budget.png
---
name: gross_carbon_budget
---
Figure: Gross Carbon Budget
```

We can now approximate the gross carbon budget as:

```Python
def get_gross_carbon_budget(data:pd.DataFrame, start:int, end:int):
  # We assume linear interpolation between two dates
  period_data =data.iloc[np.where(((data['Year'] >= start) & (data["Year"] <= end)))]
  y_interp = scipy.interpolate.interp1d(period_data.Year, period_data["Estimated Emissions"])
  full_years = [i for i in range(list(period_data["Year"])[0], list(period_data["Year"])[-1]+1)]
  emissions_interpolated = y_interp(full_years)
  emissions_interpolated
  
  # We apply simplified right Riemann Sum with yearly data
  return sum(emissions_interpolated[1:end])

get_gross_carbon_budget(data, start = 2020, end = 2035)
```

And we obtain:
```
51.74999999999999
```


The issuer $i$ has generally an objective to keep its GHG emissions under an emissions level $CE^*_i$. In that case, the carbon budget is:

\begin{equation}
CB_i(t_0,t) = \int^t_{t_0}(CE_i(s) - CE^*_i)ds = -(t - t_0) \cdot CE^*_i + \int^t_{t_0} CE_i(s)ds
\end{equation}

This carbon budget corresponds to a net carbon budget. In this case, the objective of the company is that emissions converge towards the objective at the target date $t^*$, such that:

\begin{equation}
CE_i(t^*) \approx CE^*_i
\end{equation}

Once the objective is met, the goal of the company is to maintain a carbon budget close to zero: 

\begin{equation}
CB_i(t^*,t) \approx 0
\end{equation}

when $t > t^*$.

Again, we can approximate the net carbon budget with the right Riemann sum with an annual step:

\begin{equation}
CB_i(t_0,t) \approx \sum^t_{s=t_0 + 1}(CE_i(s) - CE^*_i)
\end{equation}

Let's make an example with $CE^*_i = 3$:

```Python
import matplotlib.pyplot as plt

plt.plot(data['Year'], data["Historical Emissions"])
plt.plot(data['Year'], data["Estimated Emissions"])
plt.scatter(data['Year'], data["Historical Emissions"])
plt.scatter(data['Year'], data["Estimated Emissions"])
plt.axvline(2020, color='r') # vertical
plt.axvline(2035, color='r') # vertical
plt.axhline(3, color = 'black')
plt.fill_between(
    data["Year"],
    3,
    data["Estimated Emissions"],
    where = (data["Year"] >= 2020) & (data["Year"] <= 2035),
    alpha = 0.2
)
plt.ylim(ymin=0)
plt.ylabel("Carbon Emissions")
plt.figure(figsize = (10, 10))
plt.show()
```

```{figure} net_carbon_budget.png
---
name: net_carbon_budget
---
Figure: Net Carbon Budget
```

And we can implement the net carbon budget approximation:

```Python
def get_net_carbon_budget(data:pd.DataFrame, start:int, end:int, target:float):
  # We assume linear interpolation between two dates
  period_data =data.iloc[np.where(((data['Year'] >= start) & (data["Year"] <= end)))]
  y_interp = scipy.interpolate.interp1d(period_data.Year, period_data["Estimated Emissions"])
  full_years = [i for i in range(list(period_data["Year"])[0], list(period_data["Year"])[-1]+1)]
  emissions_interpolated = y_interp(full_years)
  emissions_interpolated
  
  # We apply simplified right Riemann Sum with yearly data
  return sum(emissions_interpolated[1:end] - target)

get_net_carbon_budget(data, 2020, 2035, 3)
```

Which gives:

```
6.75
```
### Carbon Reduction Targets

Some companies define carbon reduction targets. These targets are generally defined at a scope emissions level with different time horizons. Carbon reduction target setting is defined from the space:

\begin{equation}
\mathfrak{T} = \{k \in [1,m] : (i, j, t^k_1, t^k_2, \mathfrak{R}_{i,j}(t^k_1, t^k_2))\}
\end{equation}

with $k$ the target index, $m$ the number of historical targets, $i$ the issuer, $j$ the scope, $t^k_1$ the beginning of the target period, $t^k_2$ the end of the target period, and $\mathfrak{R}_{i,j}(t^k_1, t^k_2)$ the carbon reduction between $t^k_1$ and $t^k_2$ for the scope $j$ announced by the issuer $i$.


Let's start with an illustrative example from Le Guenedal et al. (2022):

| $k$  |  Release Date | Scope | $t^k_1$  | $t^k_2$   | $\mathfrak{R}(t^k_1,t^k_2)$|
|---|---|---|---|---|---|
| 1  | 01/08/2013  | $SC_1$  | 2015  | 2030  | 45% |
| 2  | 01/10/2019  | $SC_2$  | 2020  |  2040 | 40% |
| 3  | 01/01/2019  | $SC_3$  | 2025  | 2050  | 25% |

Dates $t^k_1$ and $t_k^2$ correspond to the 1st January. In August 2013, the company announced its willingness to reduce its carbon emissions by 45% between January 2015 and January 2030. We assume that $CE_{i,1}(2020) = 10.33$, $CE_{i,2}(2020)=7.72$ and $CE_{i,3}(2020) = 21.86$.

First, we can deduce the linear annual reduction rate for scope $j$ and target $k$ at time $t$:

\begin{equation}
\mathfrak{R}_{i,j}^k = 𝟙\{t \in [t_1^k, t_2^k]\} \cdot \frac{\mathfrak{R}_{i,j}(t^k_1, t^k_2)}{t^k_2 - t^k_1}
\end{equation}

In Python, it can be implemented as:
```Python
def get_linear_annual_by_target(start:int, end:int, target:float):
  t_k = np.array([i for i in range(2015, 2051)])
  t_R_scope = np.zeros(len(t_k))
  t_R_scope[np.where(((t_k >= start) & (t_k < end)))] = 1 # vector of dummies
  return t_R_scope  * target / (end - start) # linear annual reduction rate
```

And let's plot the results:
```Python
R_scope_1 = get_linear_annual_by_target(2015, 2030, 0.45)
R_scope_2 = get_linear_annual_by_target(2020, 2040, 0.4)
R_scope_3 = get_linear_annual_by_target(2025, 2050, 0.25)

plt.plot([i for i in range(2015, 2051)], R_scope_1 * 100)
plt.plot([i for i in range(2015, 2051)], R_scope_2 * 100)
plt.plot([i for i in range(2015, 2051)], R_scope_3 * 100)
plt.ylim(ymax=5)
plt.ylabel("Annual Reduction Rate")
plt.legend(["Scope 1","Scope 2", "Scope 3"])
plt.figure(figsize = (10, 10))
plt.show()
```

```{figure} linear_reduction_rate.png
---
name: linear_reduction_rate
---
Figure: Linear Reduction Rate Deduced from Targets
```

If needed, we can then aggregate the different targets to obtain the linear annual reduction rate for scope $j$:

\begin{equation}
\mathfrak{R}_{i,j}(t) = \sum^m_{k=1}\mathfrak{R}^k_{i,j}(t)
\end{equation}

In our illustrative example, this is not necessary as we have only one target $k$ by scope $j$.

We can then convert these reported targets into absolute emissions reduction as follows:

\begin{equation}
\mathfrak{R}_i(t) = \frac{1}{\sum^3_{j=1}CE_{i,j}(t_0)} \cdot \sum^3_{j=1}CE_{i,j}(t_0) \cdot \mathfrak{R}_{i,j}(t)
\end{equation}

Let's also implement it in Python:

```Python
R_total = 1 / (10.33 + 7.72 + 21.86) * (10.33 * R_scope_1 + 7.72 * R_scope_2 + 21.86 * R_scope_3)

plt.plot([i for i in range(2015, 2051)], R_total * 100)
plt.ylim(ymax=2)
plt.ylabel("Annual Reduction Rate")
plt.figure(figsize = (10, 10))
plt.show()
```


```{figure} annual_reduction_rate.png
---
name: annual_reduction_rate
---
Figure: Total Emissions Annual Reduction Rate Deduced From Linear Annual Reduction Rate by Scope
```

After this conversion, the carbon reduction $\mathfrak{R}_i(t)$ no longer depends on the scope and the target period. 

Once we have established the reduction along the time horizon, we have the implied trajectory of the company emissions:

\begin{equation}
CE_i^{Target}(t) := \hat{CE}_i(t) = (1 - \mathfrak{R}_i(t_{Last},t)) \cdot CE_i(t_{Last})
\end{equation}

where:

\begin{equation}
\mathfrak{R}_i(t_{Last},t) = \sum^t_{s = t_{Last} + 1} \mathfrak{R}_i(s)
\end{equation}

We can plot the reduction $\mathfrak{R}_{2015,t}$:

```Python
plt.plot([i for i in range(2015, 2051)], np.cumsum(R_total) * 100)
plt.ylim(ymin = 0)
plt.ylabel("Total Reduction Rate")
plt.figure(figsize = (10, 10))
plt.show()
```

```{figure} total_reduction_rate.png
---
name: total_reduction_rate
---
Figure: Total Reduction Rate
```

And we can obtain the targeted carbon emissions level $CE^{Target}_i(t)$:

```Python
def get_targeted_emissions(reduction_pathway:np.array, ce_last:float):
  return (1 - reduction_pathway) * ce_last

ce_target = get_targeted_emissions(reduction_pathway, 10.33 + 7.72 + 21.86)[5:] # to start to get the CE target from 2020 data

import matplotlib.pyplot as plt

plt.figure(figsize = (10, 10))
plt.ylabel("Carbon Emissions")
plt.plot([i for i in range(2020, 2051)], ce_target)
plt.ylim(ymin = 0)
plt.ylim(ymax = 40)
plt.show()
```


```{figure} ce_target.png
---
name: ce_target
---
Figure: Emissions Target
```

In practice however, we can face carbon targets issuer updating its expectations and change is reduction policy, with resulting overlapping dates, such as the following:


| $k$  |  Release Date | Scope | $t^k_1$  | $t^k_2$   | $\mathfrak{R}(t^k_1,t^k_2)$|
|---|---|---|---|---|---|
| 1  | 01/08/2013  | $SC_1$  | 2015  | 2030  | 45% |
| 2  | 01/03/2016  | $SC_1$  | 2017  |  2032 | 60% |
| 3  | 01/10/2010  | $SC_2$  | 2019  | 2039  | 40% |
| 4  | 01/11/2019  | $SC_{1+2+3}$  | 2020  | 2050  | 75% |

To overcome this issue, we can implement the algorithm proposed by Le Guenedal et al. (2022):
- each target are translated into a vector of emissions reduction per year, with the associated scopes ($SC_1$, $SC_2$ and $SC_3$)
- we iterate from the most recent target $\mathfrak{R_i}(t_B)$ to the oldest target $\mathfrak{R_i}(t_A)$: at each step, we decide if we should bring the older target into the combined target or if we should replace the combined target with the older target


```{figure} algo_targets.png
---
name: algo_targets
---
Figure: Carbon Target Aggregation, from Le Guenedal et al. (2022)
```

The decision trigger is the overlap between scopes:
- if the older target's scopes are complementary with the current combined target, we add the targets (add-up case)
- if the older target has a better (overlapping) scope emissions coverage, we retain the older target (replace case)

### Carbon Trend

Another alternative to the benchmark global or sector reduction scenario is the carbon trend proposed by Le Guenedal et al. (2022).
We've already covered the carbon trend in the [previous part of this course](../climate_investing/self_decarbonization.md). 
