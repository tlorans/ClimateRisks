## Duration, Gap and Slope

As an introduction to alternative metrics to be used for an effective portfolio alignment strategy, we've [introduced carbon trend into our optimization problem](../climate_investing/self_decarbonization.md) in the previous part of this course. 

More advanced metrics have been proposed by Le Guenedal et al. (2022). These metrics rely on the concepts of carbon budget, target and trend that we've covered in the previous section. 

Let's consider a static approach, where $t^*$ is the target horizon. We can denote $CE_i^{NZE}(t^*)$ as the net zero emissions scenario for issuer $i$, with $t_0$ the current date.

We can compute $CE^{NZE}_i(t^*)$ by using the issuer's targets or using a consensus scenario:

\begin{equation}
CE^{NZE}_i(t^*) = (1 - \mathfrak{R}^*(t_0,t^*)) \cdot CE_i(t_0)
\end{equation}

where $\mathfrak{R}^*(t_0,t^*)$ is the carbon reduction between $t_0$ and $t^*$ expected for this issuer. For example, it can be equal to the expected reduction for the sector of the issuer in order to achieve an NZE scenario.

For a company in the electricity sector, we can use the corresponding IEA NZE scenario for example (in GtCO2eq):

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
### Duration: How Many Time to Attain the NZE Scenario?

The duration is defined as the time to reach the NZE scenario (or duration):

\begin{equation}
\tau_i^{Trend} = \{inf \; t: CE^{Trend}_i(t) \leq CE^{NZE}_i(t^*)\}
\end{equation}

It measures if the issuer's track record is in line with its targets or the NZE scenario (depending on what we use as the basis for CE^{NZE}_i(t^*)).

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

Let's consider the following example from Le Guenedal et al. (2022):

| Year  |  $CE_i(t)$ |
|---|---|
| 2015 |   45.37  |
| 2016 |   40.75  |
| 2017 |   39.40  |
| 2018 |   36.16  |
| 2019 |   38.71  |
| 2020 |   39.91  |

Let's compute $CE_i^{Trend}$ with $\hat{\beta}_{i,0} = 3637.73$ and $\hat{\beta}_{i,1} = - 1.7832$, we have:

\begin{equation}
CE_i^{Trend}(t) = 3637.73 - 1.7832 \cdot t
\end{equation}
\begin{equation}
= 35.67 - 1.7832 \cdot ( t - 2020)
\end{equation}

We can also rescale the trend such that $CE^{Trend}_i(2020) = CE_i(2020)$:

\begin{equation}
CE^{Trend}_i(t) = 39.91 - 1.7832 \cdot (t - 2020)
\end{equation}

We assume that the NZE scenario for 2030 is a reduction of carbon emissions by 30%:

\begin{equation}
CE^{NZE}_i(2030) = 39.91 \times (1 - 30\%) = 27.94
\end{equation}

Let's plot it in Python to have a sense of the duration concept:
```Python
ce_past = np.array([45.37,40.75, 39.40, 36.16, 38.71,39.91]) 
years = np.array([i for i in range(2015, 2051)])

ce_trend = 35.67 - 1.7832 * (years[5:] - 2020)
ce_trend_rescaled = 39.91 - 1.7832 * (years[5:] - 2020)

plt.plot(years[:6], ce_past)
plt.plot(years[5:], ce_trend)
plt.plot(years[5:], ce_trend_rescaled)
plt.scatter(years[:6], ce_past)
plt.scatter(years[5:], ce_trend)
plt.scatter(years[5:], ce_trend_rescaled)

plt.axhline(27.94, color='r') # vertical
plt.ylim(ymin = 0)
plt.ylabel("Carbon Emissions")
plt.legend(["Historical Emissions","Trend Model", "Trend Model - Rescaled"])

plt.figure(figsize = (10, 10))
plt.show()
```

```{figure} duration.png
---
name: duration
---
Figure: Trend Model vs. $CE^{NZE}_i(2030) = 27.94$
```

And we obtain $\tau^{Trend}_i$ with:

```Python
2020 + (27.94 - (3637.73 - 1.7832 * 2020)) / (- 1.7832)
```
with the following result:
```
2024.3326603858234
```

### Gap: How Far the Trend is From the NZE scenario?

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
### Slope: Is the Required Effort to Attain the NZE Scenario Sustainable?

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


If we take the same previous example, with $CE_i(2020) = 39.91$ and $CE^{NZE}_i(2030) = 27.94$ we thus have:

\begin{equation}
Slope_i(2030) = \frac{27.94 - 39.91}{2030 - 2020} = - 1.1973
\end{equation}

The result means that in order to achieve the NZE scenario by 2030, the company mist reduce its carbon emissions by 1.1973 MtC02e per year.

Finally, we can normalize this slope metric using the current slope $\hat{\beta}_{i,1}$ of the trend model, in order to obtain the slope multiplier:

\begin{equation}
m_i^{Slope} = \frac{Slope_i(t^*)}{\hat{\beta}_{i,1}}
\end{equation}

With the previous example, the slope multiplier is equal to 67.14%. It means that the efforts are less important that what the company has done in the past (represented by $\hat{\beta}_{i,1}$).