## Emissions Metrics


### Static Measures: Duration, Gap, Slope and Budget

Let's consider a static approach, where $t^*$ is the target horizon. We can denote $CE_i^{NZE}(t^*)$ as the net zero emissions scenario for issuer $i$, with $t_0$ the current date.

We can compute $CE^{NZE}_i(t^*)$ by using the issuer's targets or using a consensus scenario:

\begin{equation}
CE^{NZE}_i(t^*) = (1 - \mathfrak{R}^*(t_0,t^*)) \cdot CE_i(t_0)
\end{equation}

where $\mathfrak{R}^*(t_0,t^*)$ is the carbon reduction between $t_0$ and $t^*$ expected for this issuer. For example, it can be equal to the expected reduction for the sector of the issuer in order to achieve an NZE scenario.

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

#### Velocity

#### Burn-Out Scenario
