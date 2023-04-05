## Portfolio Alignment

We've seen in the low-carbon strategy framework how investors can conduct a portfolio decarbonization with a static approach. On the other side, net zero investing involves portfolio alignment with a decarbonization pathway, rather than a simple static decarbonization. It involves a dynamic strategy in order to comply with the given net zero scenario.

The dynamic problem is trickier since it involves rebalancing decisions and depends on the future behavior of corporate issuers. 

In this part, we are going to compare the approach for performing a portfolio alignment with the Paris-Aligned Benchmarks (PAB) and the NZE frameworks. The main difference between both approaches is that portfolio alignment is conducted at the portfolio level in the PABs, while portfolio alignment is checked at the stock level in the NZE approach.

### Sequential Decarbonization at Portfolio Level

Let's first address the PAB approach of sequential portfolio decarbonization. 

#### Decarbonization Pathway

The portfolio intensity decarbonization is stated as:

1. A year-on-year self-decarbonization $\Delta \mathfrak{R}_{CI}$ of 7\% on average per annum, based on scope 1, 2 and 3 carbon emissions intensities.
2. A minimum carbon intensity reduction $\mathfrak{R}_{CI}^-$ at 50\% compared to the invetable universe.

The financial decarbonization pathway is thus:

\begin{equation}
\mathfrak{R}_{CI}(t_0, t) = 1 - (1 - 7\%)^{t-t_0}(1 - 50\%)
\end{equation}

```Python
# reproduce figure 17 page 30 of portfolio construction with climate measures
```

At date $t$, the PAB label imposes the following inequality constraint for the portfolio $x(t)$:

\begin{equation}
CI(x(t)) \leq (1 - \mathfrak{R}_{CI}(t_0,t))CI(b(t_0))
\end{equation}

The base year $t_0$ thus defines the reference level of the carbon intensity, as the reference level is $CI(b(t_0))$ and not $CI(b(t))$. This is a first important difference compared to the low-carbon strategy.

#### Sequential Optimization Problem
The one-period optimization problem or sequential optimization process:

```Python
# show figure of projected decarbonation
```

```Python
#show figure of projected tracking error
```

### Sequential Decarbonization at Stock Level

#### Net Zero Metric

Carbon emission trends.

```Python
# reproduce figure 20 for few stocks in page 38 of portfolio construction with climate risk
```

#### NZE Optimization Problem

The optimization problem is the same as the sequential optimization problem except that we explicitly introduce the NZE trajectories for the individual carbon intensity trajectories.

```Python
# Reproduce Table 11 in page 40 of Portfolio Construction with Carbon Risk
```
