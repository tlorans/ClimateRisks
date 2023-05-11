# Decarbonization Metrics

In this part, we follow Le Guenedal et al. (2022) {cite}`le2022net` and proposed carbon metrics by the authors to perform portfolio alignment.

First, we cover the foundations of carbon data and analytics, by defining the concepts of carbon budget, reduction target and trend.

Second, we focus on several metrics proposed by Le Guenedal et al. (2022), both static and dynamic.

Finally, we addres the Participation, Ambition and Credibility (PAC) framework proposed as an analytic grid that can be use for portfolio alignment.

## Basics

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

```Python
#Figure 4 page 10
```

### Carbon Trend

```Python
# Figure 5 page 13
```

## Emissions Metrics

### Static Measures 

#### Duration

#### Gap 

#### Slope

#### Budget

### Dynamic Measures

#### Dynamic Analysis of the Track Record

#### Velocity

#### Burn-Out Scenario

## Participation, Ambition and Credibility for an Effective Portfolio Alignment Strategy

### Participation

```Python
# Figure 9 page 27, participation
```

### Ambition 

```Python
# Figure 9 page 27 ambition
```

### Credibility 

```Python
# Figure 9 page 27, credibility
```