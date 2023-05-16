## Advanced Emissions Metrics

As an introduction to alternative metrics to be used for an effective portfolio alignment strategy, we've [introduced carbon trend into our optimization problem](../climate_investing/self_decarbonization.md) in the previous part of this course. 

More advanced static and dynamic metrics have been proposed by Le Guenedal et al. (2022). These metrics rely on the concepts of carbon budget, target and trend that we've covered in the previous section. 

In this section, we will cover the duration, gap, slope and budget measures proposed as static metrics, and the time contribution, velocity and burn-out scenario as advanced dynamic metrics.



### Static Measures: Duration, Gap, Slope and Budget

Let's consider a static approach, where $t^*$ is the target horizon. We can denote $CE_i^{NZE}(t^*)$ as the net zero emissions scenario for issuer $i$, with $t_0$ the current date.

We can compute $CE^{NZE}_i(t^*)$ by using the issuer's targets or using a consensus scenario:

\begin{equation}
CE^{NZE}_i(t^*) = (1 - \mathfrak{R}^*(t_0,t^*)) \cdot CE_i(t_0)
\end{equation}

where $\mathfrak{R}^*(t_0,t^*)$ is the carbon reduction between $t_0$ and $t^*$ expected for this issuer. For example, it can be equal to the expected reduction for the sector of the issuer in order to achieve an NZE scenario.

Let's make an example with an electricity company. The corresponding IEA NZE scenario is (in GtCO2eq):

| Year  |  2020 | 2025 | 2030 | 2035 | 2040 | 2045 | 2050 |
|---|---|---|---|---|---|---|---|
|$CE_{Electricity}(t)$|  13.5   | 10.8  | 5.8  | 2.1 | -0.1 | -0.3 | -0.4 |

We can obtain the corresponding reduction pathway $\mathfrak{R}^*(t_0,t^*)$ with linearly interpolated  carbon emissions from this scenario:

\begin{equation}
\mathfrak{R}^*(t_0,t^*) = 1 - \frac{CE^{NZE}(t)}{CE^{NZE}(t_0)}
\end{equation}

In Python we have:

```Python
import pandas as pd

years = [2020, 2025, 2030, 2035, 2040, 2045, 2050]
emissions = [13.5, 10.8, 5.8, 2.1, -0.1, -0.3, -0.4]

import scipy.interpolate

y_interp = scipy.interpolate.interp1d(years, emissions)

full_years = [i for i in range(years[0], years[-1]+1)]
emissions_interpolated = y_interp(full_years)
reduction_pathway = 1 - emissions_interpolated / emissions_interpolated[0]

import matplotlib.pyplot as plt 

plt.plot(full_years, reduction_pathway)
plt.ylabel("Reduction rate")
plt.figure(figsize = (10, 10))
plt.show()
```

```{figure} reduction_rate_elec.png
---
name: reduction_rate_elec
---
Figure: Reduction Rate for the Electricity Sector (IEA)
```

We can now obtain $CE^{NZE}_i(t)$:

```Python
import pandas as pd

import numpy as np

data = pd.DataFrame({'Year':[i for i in range(2010, 2020)],
                     'Historical Emissions':[4.8, 
                                             4.950,
                                             5.100,
                                             5.175,
                                             5.175,
                                             5.175,
                                             5.175,
                                             5.100,
                                             5.025,
                                             4.950]})

def get_emissions_scenario(reduction_pathway:np.array, ce_last:float):
  return (1 - reduction_pathway) * ce_last

emissions_scenario = get_emissions_scenario(reduction_pathway, 4.950)

plt.plot(data['Year'], data["Historical Emissions"])
plt.plot([i for i in range(2020, 2051)], emissions_scenario)
plt.scatter(data['Year'], data["Historical Emissions"])
plt.scatter([i for i in range(2020, 2051)], emissions_scenario)
plt.axvline(2020, color='r') # vertical

plt.ylabel("Carbon Emissions")
plt.figure(figsize = (10, 10))
plt.show()
```


```{figure} ce_nze.png
---
name: ce_nze
---
Figure: Carbon Emissions Scenario Deduced from the IEA Electricity NZE scenario
```

#### Duration

Using the generic notation $\hat{CE}_i(t)$ to name $CE^{Target}_i(t)$ and $CE^{Trend}_i(t)$, we define the time to reach the NZE scenario (or NZE duration in short) as:

\begin{equation}
\tau_i = \{inf \; t: \hat{CE}_i(t) \leq CE^{NZE}_i(t^*)\}
\end{equation}

If $\hat{CE}_i(t) = CE^{Target}_i(t)$, we have the NZE duration $\tau_i^{Target}$. It measures if the carbon targets announced by the company are in line with the NZE scenario $CE^{NZE}_i(t^*)$.

If $\hat{CE}_i(t) = CE_i^{Target}(t)$, we have the NZE duration $\tau^{Trend}_i$. It measures if the issuer's track record is in line with its targets or the NZE scenario.

Recalling that :

\begin{equation}
CE_i^{Trend}(t) = \hat{\beta}_{i,0} + \hat{\beta}_{i,1}(t)
\end{equation}

We have two cases:

1. The slope $\hat{\beta}_{i,1}$ is positive: $CE^{Trend}_i(t)$ is an increasing function. In that case, there is a solution only if the current carbon emissions $CE_i(t_0)$ are less than the NZE scenario:

\begin{equation}
\tau_i^{Trend} = 
\begin{cases}
  t_0 & \text{if $CE_i(t_0) \leq CE^{NZE}_i(t)$} \\
  +\infty & \text{otherwise}
\end{cases}
\end{equation}

2. The slope $\hat{\beta}_{i,1}$ is negative: $CE_i^{Trend}(t)$ is a decreasing function and we have:

\begin{equation}
CE_i^{Trend}(t) \leq CE^{NZE}_i(t^*) \Leftrightarrow \hat{\beta}_{i,0} + \hat{\beta}_{i,1}t \leq CE^{NZE}_i(t^*)
\end{equation}

\begin{equation}
\Leftrightarrow t \geq \frac{CE^{NZE}_i(t) - \hat{\beta}_{i,0}}{\hat{\beta}_{i,1}}
\end{equation}

\begin{equation}
\Leftrightarrow t \geq t_0 + \frac{CE^{NZE}_i(t^*) - (\hat{\beta}_{i,0}+\hat{\beta}_{i,1}{t_0})}{\hat{\beta}_{i,1}}
\end{equation}

\begin{equation}
\Leftrightarrow t \geq t_0 + \frac{CE^{NZE}_i(t^*) - \hat{\beta}^{'}_{i,0}}{\hat{\beta}_{i,1}}
\end{equation}

where $\hat{\beta}^{'}_{i,0} = \hat{\beta}_{i,0} + \hat{\beta}_{i,1}t_0$ is the intercept of the trend model when we use $t_0$ as the pivot date.
We then have:

\begin{equation}
\tau^{Trend}_i = t_0 + (\frac{CE^{NZE}_i(t^*) - \hat{\beta}^{'}_{i,0}}{\hat{\beta}_{i,1}})
\end{equation}

```Python
# reproduce example 5 page 13
```

```Python
# reproduce figure 25 on page 66
```

#### Gap 

The gap measure corresponds to the expected distance between the estimated carbon emissions and the NZE scenario:

\begin{equation}
Gap_i(t^*) = \hat{CE}_i(t^*) - CE^{NZE}_i(t^*)
\end{equation}

Again, we can use the target scenario:

\begin{equation}
Gap_i^{Target}(t^*) = CE_i^{Target}(t^*) - CE^{NZE}_i(t^*)
\end{equation}

or the trend model:

\begin{equation}
Gap^{Trend}_i(t^*) = CE^{Trend}_i(t^*) - CE^{NZE}_i(t^*)
\end{equation}

```Python
# example page 14
```

#### Slope

The slope corresponds to the value of $\hat{\beta}_{i,1}$ such that the gap is closed, meaning that $Gap_i^{Trend}(t^*) = 0$. We then have:

\begin{equation}
Gap^{Trend}_i(t^*) = 0 \Leftrightarrow
\hat{\beta}_{i,0} + \hat{\beta}_{i,1}t^* - CE^{NZE}_i(t^*) = 0
\end{equation}

\begin{equation}
\Leftrightarrow \hat{\beta}_{i,1} = \frac{CE^{NZE}_i(t^*) - \hat{\beta}_{i,0}}{t^*}
\end{equation}

However, $\hat{\beta}_{i,1}$ depends on the intercept of the trend model in the previous equation. We need further transformations. We assume that $\hat{CE}_i(t_0) = CE_i(t_0)$ and we use the current date $t_0$ as the pivot date. We then have:

\begin{equation}
Gap_i^{Trend}(t^*) = 0 \Leftrightarrow \hat{\beta}^{'}_{i,0} + \hat{\beta}_{i,1}(t^* - t_0) - CE^{NZE}_i(t^*) = 0
\end{equation}

\begin{equation}
\Leftrightarrow \hat{\beta}_{i,1} = \frac{CE^{NZE}_i(t^*) - CE_i(t_0)}{t^* - t_0}
\end{equation}

Because we have $\hat{\beta}^{'}_{i,0} = \hat{CE}_i(t_0)$ and $\hat{CE}_i(t_0) = CE_i(t_0)$, we can deduce that the slope to close the gap is equal to:

\begin{equation}
Slope_i(t^*) = \frac{CE^{NZE}_i(t^*) - CE_i(t_0)}{t^* - t_0}
\end{equation}

We can expect the slope to be generally negative because the gap is negative if the NZE scenario has not already been reached. The slope is a decreasing function of the gap: the higher the gap, the steeper the slope.

Finally, we can normalize this slope metric using the current slope $\hat{\beta}_{i,1}$ of the trend model, in order to obtain the slope multiplier:

\begin{equation}
m_i^{Slope} = \frac{Slope_i(t^*)}{\hat{\beta}_{i,1}}
\end{equation}

```Python
# example 5 from page 15
```

#### Budget

The budget metric corresponds to the carbon budget between the date $t_0$ and the NZE date $t^*$, such as:

\begin{equation}
CB_i(t_0, t^*) = \int^{t^*}_{t_0}(\hat{CE}_i(s) - CE^{NZE}_i(t^*))ds
\end{equation}

As before, we can compute the budget metric either with respect to the target trajectory or the trend. 

```Python
# Reproduce figure 6 page 15
```

### Dynamic Measures: Time Contribution, Velocity, Burn-Out Scenario

While we've covered static metrics for a target date $t^*$ that generally only needs the current emissions $CE_i(t_0)$ in the previous section, Le Guenedal et al. (2022) also proposed dynamic metrics that depend on a future reporting date. We will cover these metrics in this section.

#### Time Contribution

We consider $t_1 > t_0$ a future reporting date. We have:

\begin{equation}
CB_i(t_0, t^*) = \int^{t_1}_{t_0}(\hat{CE}_i(s) - CE^{NZE}_i(t^*))ds + 
\int^{t^*}_{t_1}(\hat{CE}_i(s) - CE^{NZE}_i(t^*))ds 
\end{equation}

When the current date becomes $t_1$, we have:

\begin{equation}
CB_i(t_0,t^*) = CB_i(t_0,t_1) + CB_i(t_1,t^*)
\end{equation}

where the first component $CB_i(t_0,t_1)$ corresponds to the observed / realized carbon emissions and the component $CB_i(t_1, t^*)$ corresponds to the estimated future carbon emissions. This last component corresponds to the mathematical expectation of future carbon emissions.
Having a new reported value $CE_i(t_1)$ of carbon emissions can change the expectations:

\begin{equation}
\mathbb{E}[CE_i(t)|F_{t_0}] \neq \mathbb{E}[CE_i(t)|F_{t_1}]
\end{equation}

for $t \geq t_1$.

For example, $CE_i(t_1)$ can change the carbon trend $CE_i^{Trend}(t)$ because of the next estimated intercept or slope. Or the issuer can announce new carbon targets at ime $t_1$ and the estimates $CE_i^{Target}(t)$ will be different.

To perform the corresponding dynamic analysis, $CB_i(t_0, t_1, t^*)$ is defined as the carbon budget between the starting date $t_0$ and the target date $t^*$, which is evaluated at the current date $t_1$.

We rewrite the previous decomposition of the carbon budget as:

\begin{equation}
CB_i(t_0,t,t^*) = CB_i(t_0,t_1,t_1) + CB_i(t_1,t_1,t^*)
\end{equation}

Le Guenedal et al. (2022) defines the contribution $TC_i(t1 |t_0, t^*)$ of the new information observed at the date $t_1$, satisfying:

\begin{equation}
CB_i(t_0, t_1, t^*) = CB_i(t_0,t_0,t^*) + TC_i(t_1 | t_0, t^*)
\end{equation}

If we have $TC_i(t_1 |t_0, t^*) \leq 0$, the new information allows the carbon budget to be reduced. If $TC_i(t_1 |t_0, t^*) > 0$, it has a positive contribution and increases the carbon budget. It is called the time contribution of year $t_1$. 

We have:

\begin{equation}
TC_i(t_1 | t_0, t^*) = CB_i(t_0,t_1, t^*) - CB_i(t_0,t_0,t^*)
\end{equation}

\begin{equation}
= \int^{t^*}_{t_0}(\mathbb{E}[CE_i(s)|F_{t_1}] - CE^{NZE}_i(t^*))ds - \int^{t^*}_{t_0}(\mathbb{E}[CE_i(s)|F_{t_0}] - CE^{NZE}_i(t^*))ds
\end{equation}

\begin{equation}
= \int^{t^*}_{t_0}(\mathbb{E}[CE_i(s) |F_{t_1}] - \mathbb{E}[CE_i(s)|F_{t_0}])ds
\end{equation}

The time contribution is then made up of two components:

\begin{equation}
TC_i(t_1 |t_0, t^*) = TC^{error}_i(t_1 |t_0, t^*) + TC_i^{revision}(t_1 |t_0, t^*)
\end{equation}

where $TC^{error}_i(t_1 |t_0, t^*)$ measures the forecast error between the observed trajectory and the estimate produced at time $t_0$:

\begin{equation}
TC_i^{error}(t_1 | t_0, t^*) = \int^{t_1}_{t_0}(CE_i(s) - \mathbb{E}[CE_i(s)|F_{t_0}])ds
\end{equation}

and $TC^{revision}_i(t_1 |t_0, t^*)$ corresponds to the forecast revision:

\begin{equation}
TC_i^{revision}(t_1 | t_0, t^*) = \int^{t^*}_{t_1}(\mathbb{E}[CE_i(s) |F_{t_1}] - \mathbb{E}[CE_i(s)|F_{t_0}])ds
\end{equation}

By construction:

- $TC^{error}_i(t_0 | t_0, t^*) = 0$ and $TC^{revision}_i(t_0 |t_0, t^*) = TC_i(t_0 | t_0, t^*)$ at the starting date $t_0$

- $TC^{error}_i(t^*|t_0,t^*) = TC_i(t^* |t_0, t^*)$ and $TC^{revision}_i(t^* |t_0,t^*) = 0$ at the target date $t^*$

Finally, we can normalize the previous quantities by current carbon emissions and the corresponding time period:

\begin{equation}
\bar{TC}_i(t_1 |t_0, t^*) = \frac{TC_i(t_1|t_0,t^*)}{(t^* - t_0) \cdot CE_i(t_0)}
\end{equation}

\begin{equation}
\bar{TC}^{error}_i(t_1 |t_0, t^*) = \frac{TC^{error}_i(t_1 |t_0, t^*)}{(t_1 - t_0) \cdot CE_i(t_0)}
\end{equation}

\begin{equation}
\bar{TC}^{revision}_i(t_1 |t_0, t^*) = \frac{TC^{revision}_i(t_1 |t_0, t^*)}{(t^*-t_1) _cdot CE_i(t_0)}
\end{equation}

And we have the following breakdown:

\begin{equation}
\bar{TC}_i(t_1 | t_0, t^*) = \omega_0 \cdot \bar{TC}^{error}_i(t_1 |t_0, t^*) + \omega_1 \cdot \bar{TC}^{revision}_i (t_1 |t_0, t^*)
\end{equation}

where $\omega_0 = \frac{t_1 - t_0}{t^* - t_0}$ and $\omega_1 = \frac{t^* - t_1}{t^* - t_0}$.

```Python
# example 6 page 18
```

```Python
# table 9 page 19
```

```Python
# Figure 7 page 19
```

```Python
# Figure 8 page 20
```

#### Velocity and Zero-Velocity Scenario

In the previous sections, we've seen the importance of the slope change $\Delta \hat{\beta}_{i,1}(t_1,t_2) = \hat{\beta}_{i,1}(t_2) - \hat{\beta}_{i,1}(t_1)$ between the dates $t_1$ and $t_2$.

In this section, we cover the velocity indicator proposed by Le Guenedal et al. (2022), analyzing the slope change.

Le Guenedal et al. (2022) define the velocity metric $v_i(t_1,t_2)$ as:

\begin{equation}
v_i(t_1,t_2) := \frac{\Delta \hat{\beta}_{i,1}(t_1, t_2)}{t_2 - t_1}
\end{equation}

It is expressed in MtCO2e. Le Guenedal et al. (2022) also define the $h$-step velocity as:

\begin{equation}
v_i^{(h)}(t) = v_i(t-h,t)
\end{equation}

For example, the one-step velocity measures the change of the slope by adding a new observation:

\begin{equation}
v_i^{(1)}(t) = \hat{\beta}_{i,1}(t) - \hat{\beta}_{i,1}(t - 1)
\end{equation}

The velocity measures the unit variation of the trend slope. If a net zero emissions commitment implies a negative trend $\hat{\beta}_{i,1}(t) < 0$, it can take many years for a company to change the sign of the trend slope in case of bad track record. 

We can thus use this velocity measure to check if the company is making significant efforts, that is to check if $v_i^{h}(t) < 0$.

```Python
# reproduce the table 10 page 21
```

Based on this definition of the velocity metric, Le Guenedal et al. (2022) proposed a zero-velocity scenario. 

It starts from the fact that:

\begin{equation}
v_i^{(1)}(t+1) = \hat{\beta}_{i,1}(t+1) - \hat{\beta}_{i,1}(t)
\end{equation}
\begin{equation}
= \phi(n)(12(n+2) \cdot \hat{CE}_i(t) - 18(n+1) \cdot \tilde{CE}_i(t) + 6(n - 1) \cdot CE_i(t+1))
\end{equation}

where $n$ is the number of available observations until the date $t$, and:

\begin{equation}
\phi(n) = \frac{1}{(n-1)(n+1)(n+2)}
\end{equation}

We thus have:

\begin{equation}
v^{(1)}_i(t+1) \leq 0 \Leftrightarrow CE_i(t+1) \leq ZV_i^{1}(t+1)
\end{equation}

where $ZV_i^{1}(t+1)$ corresponds to the value of carbon emissions to obtain a zero velocity. It is computed as:

\begin{equation}
ZV_i^{(1)}(t+1) = \frac{18(n+1) \cdot \tilde{CE}_i(t) - 12(n + 2) \cdot \bar{CE}_i(t)}{6(n-1)}
\end{equation}

In the case where $CE_i(s) = CE_i$ for all $s \leq t$, we have:

\begin{equation}
\tilde{CE}_i(t) = \bar{CE}_i(t) = CE_i
\end{equation}

and:

\begin{equation}
ZV_i^{(1)}(t+1) = CE_i
\end{equation}

```Python
# Table 13 page 22
```

#### Burn-Out Scenario

Le Guenedal et al. (2022) proposed a last indicator: the burn-out scenario. It refers to a sudden and violent reduction of carbon emissions in order to satisfy the NZE trajectory. 

To recall, the gap is the expected distance between the estimated carbon emissions and the NZE scenario. The burn-out scenario is then the value of the carbon emissions next year such that the gap is equal to zero, such as the NZE scenario will be achieved on average.

We have $\mathfrak{R}^{Target}_i(t+1, t^*)$ the reduction rate between the date $t+1$ and the NZE date $t^*$ when considering the issuer's carbon targets.

We have:

\begin{equation}
\hat{CE}_i(t^*) = (1 - \mathfrak{R}^{Target}_i(t+1, t^*)) \cdot CE_i(t+1)
\end{equation}

The burn-out scenario satisfies the equation $\hat{CE}_i(t^*) = CE^{NZE}_i(t^*)$, then $BO^{Target}_i(t+1, CE^{NZE}_i(t^*))$ the burn-out scenario is defined as:

\begin{equation}
BO^{Target}_i(t+1, CE^{NZE}_i(t^*)) = \frac{CE^{NZE}_i(t^*)}{1 - \mathfrak{R}^{Target}_i(t+1, t^*)}
\end{equation}

Considering the linear trend model, we have:

\begin{equation}
\hat{CE}_i(t^*) = \hat{\beta}_{i,0}(t+1) + \hat{\beta}_{i,1}(t+1) \cdot t^*
\end{equation}

where:

\begin{equation}
\hat{\beta}_{i,0}(t+1) = \hat{\beta}_{i,0}(t) + \Delta \hat{\beta}_{i,0}(t, t+1)
\end{equation}

\begin{equation}
\hat{\beta}_{i,1}(t+1) = \hat{\beta}_{i,1}(t) + \Delta \hat{\beta}_{i,1}(t,t+1)
\end{equation}

and where $\Delta \hat{\beta}_{i,0}(t,t+1)$ and $\Delta \hat{\beta}_{i,1}(t,t+1)$ are the variations of the intercept and the slope due to new carbon emissions $CE_i(t+1)$.

We finally have:

\begin{equation}
BO^{Trend}_i(t+1, CE^{NZE}_i(t^*)) = 
\{CE_i(t+1):\hat{\beta}_{i,0}(t+1) + \hat{\beta}_{i,1}(t+1) \cdot t^* = CE^{NZE}_i(t^*)\}
\end{equation}

```Python
# Table 15 page 24
```