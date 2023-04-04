## Net Zero Decarbonization Pathways

To be able to implement a net zero investing policy, investors have to define a net zero emissions (NZE) scenario, which is summarized by a decarbonization pathway.

### Net Zero Emissions (NZE) Scenario as a Carbon Budget Constraint

A net zero emissions (NZE) scenario corresponds to an emissions scenario, which is compatible with a carbon budget corresponding to a certain objective of global warming mitigation.

As an example, the IPCC (2018) gives an estimate of a remaining carbon budget of 580 GtC02eq for a 50% probability of limiting the warming to 1.5°C. The objective is to limit the global warming to 1.5°C while the corresponding carbon budget is 580 GTCO2eq. What is missing in this statement is the corresponding emissions scenario. We will see later how to determine a carbon pathway (or emission scenario) based on a carbon budget.

A NZE scenario can then be defined by a carbon pathway that satisfies the following constraints (Roncalli et al., 2022):

\begin{equation}
CB(t_0, 2050) \leq CB^+
\end{equation}
\begin{equation}
CE(2050) \approx 0
\end{equation}

With $CE(t)$ the global carbon emissions at time $t$, $CB(t_0,t)$ the global carbon budget between $t_0$ and $t$ and $CB^+$ the maximum carbon budget to attain a given objective of global warming mitigation. If we consider the AR5 results of IPCC (2018), we can set $CB^+ = 580$.

The carbon budget defines the amount of CO2eq emissions produced over the time period $[t_0,t]$ for a given emissions scenario. Checking if a given emissions scenario complies with the Net Zero objective corresponds to checking if the corresponding carbon budget respect the constraint above, with a carbon emissions level in 2050 close to 0.

### From Decarbonization Pathway to Net Zero Compliance

#### Decarbonization Pathway

A decarbonization pathway summarized an emissions scenario. It is structured among the following principles:
1. A year-on-year self-decarbonization $\Delta \mathfrak{R}$ on average per annum emissions
2. A minimum carbon reduction $\mathfrak{R}^-$

A decarbonization pathway is then defined as:

\begin{equation}
\mathfrak{R}(t_0,t) = 1 - (1 - \Delta \mathfrak{R})^{t-t_0}(1 - \mathfrak{R^-})
\end{equation}


Where $t_0$ is the base year, $t$ the year index and $\mathfrak{R}(t_0,t)$ is the reduction rate of the carbon footprint between $t_0$ and $t$.


```Python
# Reproduce figure 1 page 6 in Net Zero Investment Portfolios Part 1
```

#### From Decarbonization Pathway to Carbon Budget


From Le Guenedal et al. (2022), we find the carbon budget with a given value for $\mathfrak{R}^-$, $\Delta \mathfrak{R}$ and $CE(t_0)$ with:

\begin{equation}
CB(t_0,t) = (\frac{(1 - \Delta \mathfrak{R})^{t-t_0} - 1}{ln(1 - \Delta \mathfrak{R})})(1 - \mathfrak{R}^-)CE(t_0)
\end{equation}

```Python
# reproduce results in Table 1 p7 in Net Zero Portfolio, an integrated approach
```

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


While PAB is the most known pathway in finance, its construction lacks of theoretical and solid fundations. It has been created such that the carbon footprint is close to zero by 2050, but has no physical or economic foundations.

Indeed, a net zero emissions (NZE) scenario corresponds to a carbon pathway, which is compatible with a carbon budget.

### Carbon Budget Constraint

The carbon budget defines the amount of CO2eq emissions that an organization produces over the time period $[t_0,t]$. The carbon budget constraint corresponds to the constraint that a carbon budget is limited by a maximum level, in order to attain a specific target. As an example, the IPCC (2018) gives an estimate of the remaining carbon budget of 580 GtC02eq for a 50% probability of limiting warming to 1.5°C.

Let's $CE(t)$ being the global carbon emissions at time $t$ and $CB(t_0,t)$ the global carbon budget between $t_0$ and $t$. A NZE scenario can be defined by a carbon pathwhay that satisfies the following constraints:

\begin{equation}
CB(t_0, 2050) \leq CB^+
\end{equation}
\begin{equation}
CE(2050) \approx 0
\end{equation}

Where $CB^+$ is the maximum carbon budget. For example, with the estimates from the IPCC (2018), we would have $t_0 = 2019$ and $CB^+ = 580$.


#### Estimating the Carbon Budget From a Decarbonization Pathway



#### Estimating a Carbon Budget From an Emissions Scenario 

Let's now take the International Energy Agency (IEA) net zero scenario. Wa can compute the carbon budget $CB(2019, 2050)$ by considering the carbon pathway as a piecewise linear function. We assume that $CE(s)$ is known for $s \in \{t_0,...,t_m = t\}$ and $CE(s)$ 


#### Emissions Scenario Compliance to Net Zero Objective with Constant Reduction Rate

Using the IEA scneario, we obtain $CB(2019, 2050) = 512.35$. Since $CB(2019, 2050) \leq CB^+$ and $CE(2050) = 1.94$, we can consider the IEA scenario as a 2050 net zero emissions scenario.

```Python
# Reproduce Figure 9.18 p355 of the handbook
#done by setting CE 2019 = 36 Gt and assuming a constant compound reduction rate R
```


### Reduction Rates