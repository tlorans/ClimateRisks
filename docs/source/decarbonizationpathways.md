## Decarbonization Pathways

To be able to implement a net zero investing policy, investors have to define a net zero scenario, which is summarized by a decarbonization pathway.

### Paris-Aligned Benchmark Pathway

One of the most known decarbonization pathways in finance is the Paris-Aligned Benchmarks (PAB) one. It is structured among the following principles:

1. A year-on-year self-decarbonization $\Delta \mathfrak{R}$ on average per annum, based on scope 1, 2 and 3 (progressive phase-in) emissions intensity
2. A minimum carbon intensity reduction $\mathfrak{R}^-$ compared to the investable universe
3. A minimum exposure to sectors that are highly exposed to climate transition
4. A set of exclusions rules

The PAB's decarbonization pathway is then defined as:

\begin{equation}
\mathfrak{R}(t_0,t) = 1 - (1 - \Delta \mathfrak{R})^{t-t_0}(1 - \mathfrak{R^-})
\end{equation}

Where $t_0$ is the base year, $t$ the year index and $\mathfrak{R}(t_0,t)$ is the reduction rate of the carbon footprint between $t_0$ and $t$.

For the PAB, $\mathfrak{R}^-$ is equal to 50\%, $\Delta \mathfrak{R}$ to 7\%. 

```Python
# Reproduce figure 1 page 6 in Net Zero Investment Portfolios Part 1
```

While PAB is the most known pathway in finance, its construction lacks of theoretical and solid fundations. It has been created such that the carbon footprint is close to zero by 2050, but has no physical or economic foundations.

Indeed, a net zero emissions (NZE) scenario corresponds to a carbon pathway, which is compatible with a carbon budget.

### Carbon Budget Constraint

The carbon budget defines the amount of CO2eq emissions that an organization produces over the time period $[t_0,t]$. The carbon budget constraint corresponds to the constraint that a carbon budget is limited by a maximum level, in order to attain a specific target. As an example, the IPCC (2018) gives an estimate of the remaining carbon budget of 580 GtC02eq for a 50% probability of limiting warming to 1.5°C.

Let's $CE(t)$ being the global carbon emissions at time $t$ and $CB(t_0,t)$ the global carbon budget between $t_0$ and $t$. A NZE scenario can be defined by a carbon patwhay that satisfies the following constraints:

\begin{equation}
CB(t_0, 2050) \leq CB^+
\end{equation}
\begin{equation}
CE(2050) \approx 0
\end{equation}

Where $CB^+$ is the maximum carbon budget. For example, with the estimates from the IPCC (2018), we would have $t_0 = 2019$ and $CB^+ = 580$.

From Le Guenedal et al. (2022), we find the carbon budget with a given value for $\mathfrak{R}^-$ and $\Delta \mathfrak{R}$ such as:

\begin{equation}
CB(t_0,t) = (\frac{(1 - \Delta \mathfrak{R})^{t-t_0} - 1}{ln(1 - \Delta \mathfrak{R})})(1 - \mathfrak{R}^-)CE(t_0)
\end{equation}

```Python
# reproduce results in Table 1 p7 in Net Zero Portfolio, an integrated approach
```

### Reduction Rates