## Carbon Budget, Target and Trend

In this section, we will present the foundations for building and understanding carbon metrics. The main tools are the carbon budget, the reduction target and the carbon trend.

The absolute carbon emissions of issuer $i$ for the scope $j$ at time $t$ is denoted as $CE_{i,j}(t)$, and is generally measured annualy, in tC02e. $j$ is omited when possible, to simplify the notation.
### Carbon Budget

#### Gross Carbon Budget 

A carbon budget defines the amount of GHG emissions that a country or a company produces over the time period $[t_0, t]$.

It corresponds to the area of the region bounded by the function $CE_i(t)$:

\begin{equation}
CB_i(t_0,t) = \int^t_{t_0}CE_i(s)ds
\end{equation}

This defines a gross carbon budget.

```Python
# figure 1, part with CE^*i = 0 and gross carbon budget
```

#### Net Carbon Budget

The issuer $i$ has generally an objective to keep its GHG emissions under an emissions level $CE^*_i$. In that case, the carbon budget is:

\begin{equation}
CB_i(t_0,t) = \int^t_{t_0}(CE_i(s) - CE^*_i)df = -(t - t_0) \cdot CE^*_i + \int^t_{t_0} CE_i(s)ds
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

```Python
#figure 1, CE^* = 3 and net carbon budget
```

### Carbon Reduction

We assume $t_{Last}$ to be the last reporting date. It implies that the carbon emissions $CE_i(t)$ of the issuer $i$ are only observable when $t \leq t_{Last}$. For $t > t_{Last}$ we define the estimated carbon emissions as:

\begin{equation}
\hat{CE_i}(t) = (1 - \mathfrak{R}_i(t_{Last},t)) \cdot CE_i(t_{Last})
\end{equation}

where $\mathfrak{R}_i(t_{Last},t)$ is the carbon reduction between $t_{Last}$ and $t$. 

With $t_{Last} \in [t_0, t]$ we have the following expression for the carbon budget:

\begin{equation}
CB_i(t_0,t) = (t - t_{Last})(CE_i(t_{Last}) - CE_i^*) - (t_{Last} - t_0) \cdot CE^*_i + \int^{t_{Last}}_{t_0} CE_i(s)ds - CE_i(t_{Last}) \int^t_{t_{Last}}\mathfrak{R}_i(t_{Last}, s)ds
\end{equation}

When computing the carbon budget from the last reporting date ($t_0 = t_{Last}$), it reduces to:

\begin{equation}
CB_i(t_{Last},t) = (t - t_{Last})(CE_i(t_{Last}) - CE^*_i) - CE_i(t_{Last}) \int^t_{t_{Last}}\mathfrak{R}_i(t_{Last}, s)ds
\end{equation}

The issue here is about the availability of $\mathfrak{R}_i(t_{Last},t)$ for all issuers. One practical solution is to consider a benchmark reduction pathway, using a global carbon reduction scenario for example.

With the IPCC (2021) scenario for example, we need to reduce total emissions by at least 7% every year between 2019 and 2050 if we want to achieve net zero emissions by 2050. 

Using the global approach, the reduction for issuer $i$ is equal to the reduction calculate for the global scenario:

\begin{equation}
\mathfrak{R}_i(t_{Last},t) = \mathfrak{R}_{Global}(t_{Last}, t)
\end{equation}

However, this solution is not optimal since there is no difference between issuers. 

Another solution is to use a sector scenario:

\begin{equation}
\mathfrak{R}_i(t_{Last},t) = \mathfrak{R}_{Sector}(t_{Last}, t)
\end{equation}

if $i \in Sector(s)$

Still, these benchmark solutions ignore the idiosyncratic aspect of carbon reduction. 

```Python
#Figure 3 page 7
```

### Carbon Reduction Targets

A first solution to take into account the idiosyncratic aspect of carbon reduction is the use of carbon reduction targets defined by companies. These targets are generally defined at a scope emissions level with different time horizons.

In this section, we present the methodology to compute annual reduction rates implied by the targets and dicuss how to deal with overlapping targets.

Carbon reduction target setting is defined from the space:

\begin{equation}
\mathfrak{T} = \{k \in [1,m] : (i, j, t^k_1, t^k_2, \mathfrak{R}_{i,j}(t^k_1, t^k_2))\}
\end{equation}

with $k$ the target index, $m$ the number of historical targets, $i$ the issuer, $j$ the scope, $t^k_1$ the beginning of the target period, $t^k_2$ the end of the target period, and $\mathfrak{R}_{i,j}(t^k_1, t^k_2)$ the carbon reduction between $t^k_1$ and $t^k_2$ for the scope $j$ announced by the issuer $i$.

We have the linear annual reduction rate for scope $j$ and target $k$ at time $t$:

\begin{equation}
\mathfrak{R}_{i,j}^k = 𝟙\{t \in [t_1^k, t_2^k]\} \cdot \frac{\mathfrak{R}_{i,j}(t^k_1, t^k_2)}{t^k_2 - t^k_1}
\end{equation}

We can then aggregate the different targets to obtain the linear annual reduction rate for scope $j$:

\begin{equation}
\mathfrak{R}_{i,j}(t) = \sum^m_{k=1}\mathfrak{R}^k_{i,j}(t)
\end{equation}

We can then convert these reported targets into absolute emissions reduction as follows:

\begin{equation}
\mathfrak{R}_i(t) = \frac{1}{\sum^3_{j=1}CE_{i,j}(t_0)} \cdot \sum^3_{j=1}CE_{i,j}(t_0) \cdot \mathfrak{R}_{i,j}(t)
\end{equation}

After this conversion, the carbon reduction $\mathfrak{R}_i(t)$ no longer depends on the scope and the target period. Once we have established the reduction along the time horizon, we have the implied trajectory of the company emissions:

\begin{equation}
CE_i^{Target}(t) := \hat{CE}_i(t) = (1 - \mathfrak{R}_i(t_{Last},t)) \cdot CE_i(t_{Last})
\end{equation}

where:

\begin{equation}
\mathfrak{R}_i(t_{Last},t) = \sum^t_{s = t_{Last} + 1} \mathfrak{R}_i(s)
\end{equation}

And we can finally compute the carbon budget according to the carbon targets declared by the issuer.

Let's consider an illustrative example from Le Guenedal et al. (2022):

| $k$  |  Release Date | Scope | $t^k_1$  | $t^k_2$   | $\mathfrak{R}(t^k_1,t^k_2)$|
|---|---|---|---|---|---|
| 1  | 01/08/2013  | $SC_1$  | 2015  | 2030  | 45% |
| 2  | 01/10/2019  | $SC_2$  | 2020  |  2040 | 40% |
| 3  | 01/01/2019  | $SC_3$  | 2025  | 2050  | 25% |

Dates $t^k_1$ and $t_k^2$ correspond to the 1st January. In August 2013, the company announced its willingness to reduce its carbon emissions by 45% between January 2015 and January 2030. We assume that $CE_{i,1}(2020) = 10.33$, $CE_{i,2}(2020)=7.72$ and $CE_{i,3}(2020) = 21.86$.

In Python:
```Python
#Figure 4 page 10
# we apply the formula up to the the linear annual reduction rate
```

In practice however, we can face carbon targets issuer updateding its expectations and change is reduction policy, with resulting overlapping dates, such as the following:


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

In Python:
```Python
#Figure 4 page 10
# same results but once the overlapping dates are fixed.
```

### Carbon Trend

Another alternative to the benchmark global or sector reduction scenario is the carbon trend proposed by Le Guenedal et al. (2022). The authors define the carbon trend by considering a linear constrant trend model. The corresponding linear regression model is:

\begin{equation}
CE_i(t) = \beta_{i,0} + \beta_{i,1}t + u_i(t)
\end{equation}

where $t \in [t_{First}, t_{Last}]$. Using the least squares method, we can estimate the parameters $\beta_{i,0}$ and $\beta_{i,1}$. We can then build the carbon trajectory implied by the current rend by applying the projection:

\begin{equation}
CE^{Trend}_i(t) := \hat{CE}_i(t) = \hat{\beta}_{i,0} + \hat{\beta}_{i,1}t
\end{equation}

for $t > t_{Last}$. The underlying idea is then to extrapolate the past trajectory. 

Let's assume that $t_p$ is a pivot date (generally the current year). We can have the following reformulation:

\begin{equation}
CE_i(t) = \beta^{'}_{i,0} + \beta^{'}_{i,1}(t - t_p) + u_i(t)
\end{equation}

with the relationships: $\beta_{i,0} = \beta^{'}_{i,0}-\beta^{'}_{i,1}t_p$ and $\beta_{i,1} = \beta^{'}_{i,1}$.

If we have the current date as the pivot date $t_p = t_0$, we have $\hat{CE}_i(t) = \beta^{'}_{i,0} + \beta^{'}_{i,1}(t-t_0)$ and $\hat{CE}_i(t_0) \beta^{'}_{i,0}$.

If we want to rescale the trend such that $\hat{CE}_i(t_0) = CE_i(t_0)$, we need to obtain $\beta^{'}_{i,0} = CE_i(t_0)$. We then need to change the intercept of the trend model, that is now equal to $\tilde{\beta}_{i,0} = CE_i(t_0) - \hat{\beta}_{i,1}t_0$.

Let's apply it on an illustrative example from Le Guenedal et al. (2022):

| Year | $CE_i(t)$ | 
|---|---|
| 2007  | 57.82 |
| 2008  | 58.36 |
| 2009  | 57.70 |
| 2010  | 55.03 |
| 2011  | 51.73 |
| 2012  | 46.44 |
| 2013  | 47.19 |
| 2014  | 46.18 |
| 2015  | 45.37 |
| 2016  | 40.75 |
| 2017  | 39.40 |
| 2018  | 36.16 |
| 2019  | 38.71 |
| 2020  | 39.91 |

```Python
# computation to get the trend as example 4 in page 11
```

```Python
# Figure 5 page 13
```

## Emissions Metrics

### Static Measures: Duration, Gap, Slope and Budget

#### Duration

#### Gap 

#### Slope

#### Budget

### Dynamic Measures: Time Contribution, Velocity, Burn-Out Scenario

#### Dynamic Analysis of the Track Record

#### Velocity

#### Burn-Out Scenario

## Participation, Ambition and Credibility for an Effective Portfolio Alignment Strategy

### Participation

This dimension of the PAC framework helps to answer the question: is the trend of the issuer in line with the net zero emissions scenario? 

This dimension generally depends on the past observations and corresponds to the track record analysis of historical carbon emissions.

```Python
# Figure 9 page 27, participation
```

### Ambition 

This dimension answers to the question: is the commitment of the issuer to fight climate change ambitious? In particular, it helps to understand if the target trajector is above, below or in line with the NZE consensus scenario.

This dimension compares the target trajectory on one side and the NZE scenario or the trend on the other side. We measure to what extent companies are willing to reverse their current carbon emissions and have objectives that match the NZE scenario.

```Python
# Figure 9 page 27 ambition
```

### Credibility 

Finally, this last dimension address the most important issue: is the target setting of the issuer relevant and robust? 

Indeed, we may wonder if the target trajectory is a too ambitious promise and a form of greenwashing or a plausible scenario.

We can measure the credibility of the targets by comparing the current trend of carbon emissions and the reduction targets or by analyzing the recent dynamics of the track record.

```Python
# Figure 9 page 27, credibility
```