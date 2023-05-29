
## Towards a Dynamic Decarbonization Strategy

While we've seen the low-carbon strategy in the previous section, minimizing the tracking error relative to a benchmark index while reducing the portfolio's carbon footprint, one could ask if the approach is sufficient for a strategy contributing to the transition towards a net zero economy. Indeed, the previous approach performs portfolio decarbonization by underweighting relatively high-emitters stocks and overwheighting low-emitters stocks, without reference other than the benchmark universe. Furthermore, it is a purely static approach

In fact, we know that the objective of mitigation policies, if soundly implemented, should be to abate emissions such that the economy follows a net zero emissions (NZE) scenario. In that context, portfolio decarbonization becomes a portfolio alignment exercice (Barahhou et al., 2022) {cite:p}`barahhou2022net`, that is portfolio decarbonization in respect with a NZE scenario. The acknowledgement of such scenario calls for a dynamic strategy.

In this part, we will give a definition of a net zero emissions (NZE) scenario with the carbon budget constraint and study the relationship between a NZE scenario and a decarbonization pathway. These dynamic decarbonization reference are the very foundation of the need for a dynamic approach in portfolio decarbonization.

### Net Zero Emissions Scenario

As stated by Barahhou et al. (2022), a net zero emissions (NZE) scenario corresponds to an emissions scenario, which is compatible with a carbon budget. 
The carbon budget defines the amount of CO2eq emissions produced over the time period $[t_0,t]$ for a given emissions scenario. 

NZE scenario is informative as it represents a possible target for government while implementing mitigation policies.

As an example, the IPCC (2018) {cite:p}`masson2018global` gives an estimate of a remaining carbon budget of 580 GtC02eq for a 50% probability of limiting the warming to 1.5°C. The objective is to limit the global warming to 1.5°C while the corresponding carbon budget is 580 GTCO2eq.

More formally, a NZE scenario can be defined by a carbon pathway that satisfies the following constraints (Barahhou et al., 2022):

\begin{equation}
CB(t_0, 2050) \leq CB^+
\end{equation}
\begin{equation}
CE(2050) \approx 0
\end{equation}

With $CE(t)$ the global carbon emissions at time $t$, $CB(t_0,t)$ the global carbon budget between $t_0$ and $t$ and $CB^+$ the maximum carbon budget to attain a given objective of global warming mitigation. If we consider the AR5 results of IPCC (2018), we can set $CB^+ = 580$.

A NZE scenario must comply with the carbon budget constraint above, with a carbon emissions level in 2050 close to 0.

The figure below, taken from Roncalli (2023), represents the IEA NZE scenario (sector scenario) and the corresponding carbon budget (global).


```{figure} scenarios.png
---
name: scenarios
---
Figure: CO2 emissions by sector in the IEA NZE scenario (in GtCO2eq) from Roncalli (2023)
```

### Decarbonization Pathway

A decarbonization pathway summarizes a NZE scenario. It is structured among the following parameters (Barahhou et al. 2022):
1. An average yearly reduction rate $\Delta \mathfrak{R}$ 
2. A minimum carbon reduction $\mathfrak{R}^-$

A decarbonization pathway is then defined as:

\begin{equation}
\mathfrak{R}(t_0,t) = 1 - (1 - \Delta \mathfrak{R})^{t-t_0}(1 - \mathfrak{R^-})
\end{equation}


Where $t_0$ is the base year, $t$ the year index and $\mathfrak{R}(t_0,t)$ is the reduction rate of the carbon emissions between $t_0$ and $t$.

Decarbonization pathway gives a forward-looking target for the economy decarbonization. This is the starting point for a dynamic portfolio decarbonization (portfolio alignment).

The figure below represents an example of decarbonization pathway, that is the expected emissions reduction compared to a base year.

```{figure} reductionrate.png
---
name: reductionrate
---
Figure: Decarbonization Pathway with $\Delta \mathfrak{R} = 0.07$ and $\mathfrak{R}^- = 0.30$
```