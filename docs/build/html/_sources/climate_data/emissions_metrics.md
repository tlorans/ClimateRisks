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

```Python
# example page 14
```

#### Slope

```Python
# example 5 from page 15
```

#### Budget

### Dynamic Measures: Time Contribution, Velocity, Burn-Out Scenario

#### Dynamic Analysis of the Track Record

#### Velocity

#### Burn-Out Scenario
