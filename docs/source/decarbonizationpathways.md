## Net Zero Emissions Scenario

To be able to implement a net zero investing policy, investors have to define a net zero emissions (NZE) scenario, which is summarized by a decarbonization pathway. In this part, we will see how to check if a given decarbonization pathway or an emissions scenario is net zero compliant.

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

### Net Zero Objective Compliance

To check if a given decarbonization pathway or an emissions scenario fulfill the Net Zero objective, investors need to assess if the resulting carbon budget $CB(t_0, 2050)$ and the final carbon emissions level $CE(2050)$ comply with the carbon budget constraint stated above.

#### Decarbonization Pathway

A decarbonization pathway summarized an emissions scenario. It is structured among the following principles:
1. An average yearly reduction rate $\Delta \mathfrak{R}$ 
2. A minimum carbon reduction $\mathfrak{R}^-$

A decarbonization pathway is then defined as:

\begin{equation}
\mathfrak{R}(t_0,t) = 1 - (1 - \Delta \mathfrak{R})^{t-t_0}(1 - \mathfrak{R^-})
\end{equation}


Where $t_0$ is the base year, $t$ the year index and $\mathfrak{R}(t_0,t)$ is the reduction rate of the carbon footprint between $t_0$ and $t$.


```Python
# Reproduce figure 1 page 6 in Net Zero Investment Portfolios Part 1
```


Considering the definition of the decarbonization pathway, we have the following emissions scenario (Roncalli et al., 2022):

\begin{equation}
CE(t) = (1 - \Delta \mathfrak{R})^{t - t_0}(1 - \mathfrak{R}^-) CE(t_0)
\end{equation}

#### From Decarbonization Pathway to Carbon Budget

From Le Guenedal et al. (2022), we find the carbon budget with a given value for $\mathfrak{R}^-$, $\Delta \mathfrak{R}$ and $CE(t_0)$ with:

\begin{equation}
CB(t_0,t) = (\frac{(1 - \Delta \mathfrak{R})^{t-t_0} - 1}{ln(1 - \Delta \mathfrak{R})})(1 - \mathfrak{R}^-)CE(t_0)
\end{equation}

```Python
# reproduce results in Table 1 p7 in Net Zero Portfolio, an integrated approach
```

From a given decarbonization pathway, we can then estimate $CB(t_0,2050)$ and $CE(2050)$, the variables we need to check net zero compliance.

#### The IEA Scenario as a Net Zero Emissions Scenario

Let's now take the International Energy Agency (IEA) net zero scenario. Wa can compute the carbon budget $CB(2019, 2050)$ by considering the carbon pathway as a piecewise linear function. We assume that $CE(s)$ is known for $s \in \{t_0,...,t_m = t\}$ and $CE(s)$ 

Using the IEA scneario, we obtain $CB(2019, 2050) = 512.35$. Since $CB(2019, 2050) \leq CB^+$ and $CE(2050) = 1.94$, we can consider the IEA scenario as a 2050 net zero emissions scenario.

```Python
# Reproduce Figure 9.18 p355 of the handbook
#done by setting CE 2019 = 36 Gt and assuming a constant compound reduction rate R
```

### Decarbonization Pathway for Portfolio

If a decarbonization pathway is generally valid for an economy or a country, we must have in mind that it is defined in terms of absolute carbon emissions in this case. However, portfolio decarbonization uses carbon intensity, and not absolute carbon emissions.

#### Carbon Emissions and Carbon Intensity Pathway Relationship

The carbon intensity $CI(t)$ is defined as the ratio between the carbon emissions $CE(t)$ and a normalization variable $Y(t)$ (a physical or monetary value):

\begin{equation}
CI(t) = \frac{CE(t)}{Y(t)}
\end{equation}

If $\mathfrak{R}_{CI}(t_0)$ and $\mathfrak{R}_{CE}(t,t_0)$ are the reduction rates of carbon intensity and emissions between the base date $t_0$ and $t$, we have the following relationship:

\begin{equation}
\mathfrak{R}_{CI}(t_0,t) = \frac{g_Y(t_0,t) + \mathfrak{R}_{CE}(t_0,t)}{1 + g_Y(t_0,t)}
\end{equation}

Where $g_Y(t_0,t)$ is the growth rate of the normalization variable. As we assume that $g_Y(t_0,t) \geq 0$ and $0 \leq \mathfrak{R}_{CE}(t_0,t) \leq 1$, we have the property that the reduction rate of the carbon intensity is always greater than the reduction rate of the carbon emissions:

\begin{equation}
\mathfrak{R}_{CI}(t_0,t) \geq \mathfrak{R}_{CE}(t_0,t)
\end{equation}


The emissions decarbonization pathway $\mathfrak{R}_{CE}(t_0,t)$ is called the economic decarbonization pathway, while the intensity decarbonization pathway $\mathfrak{R}_{CI}(t_0,t)$ is called the financial decarbonization pathway.

We generally simplify the financial / economic pathway relationship by considering both the annual growth rate of normalization variable $g_{Y}$ and the annual reduction rate of carbon emissions $\Delta \mathfrak{R}_{CE}$ as constant. We then have the compound growth rate of the normalization variable:

\begin{equation}
g_Y(t_0,t) = (1 + g_Y)^{t-t_0} - 1
\end{equation}

And the carbon reduction rate as:

\begin{equation}
\mathfrak{R}_{CE}(t_0,t) = 1 - (1 - \Delta \mathfrak{R}_{CE})^{t - t_0}
\end{equation}

Then, the relationship between the financial and the economic decarbonization pathway becomes:

\begin{equation}
\mathfrak{R}_{CI}(t_0,t) = 1 - (1 - \frac{(g_Y + \Delta \mathfrak{R}_{CE})}{1 + g_Y})^{t - t_0}
\end{equation}


```Python
# reproduce figure 3 page 9 Net Zero Integrated approach about the impact of the growth rate g_Y on the intensity decarbonization pathway and Delta R_CE set to 7% -> on y-axis the R_CI
```

#### From Economic to Financial Decarbonization Pathway

With a given economic decarbonization pathway $\mathfrak{R}_CE(t_0,t)$ and given normalization variable growth $g_Y(t_0,t)$, we can try to approximate the relationship between the economic and the financial decarbonization pathway in order to estimate the parameters $\mathfrak{R}^-_{CI}$ and $\Delta \mathfrak{R}_{CI}$ with the following regression model estimated by least squares:

\begin{equation}
\mathfrak{R}_{CI}(t_0,t) = f_1(t; \mathfrak{R^-}_{CI}, \Delta \mathfrak{R}_{CI}) + \epsilon(t)
\end{equation}

```Python
# reproduce Table 2 Intensity decarbonization pathway
# page 10 in NZE integrated approach
```
PAB financial decarbonization very aggressive pathway compared to the IEA deduced pathway for the next ten years.

### Key Takeaways

- Net Zero Emissions Scenario is a carbon pathway with a resulting carbon budget compliant with global warming mitigation objective

- The investor can use the carbon budget constraint to check if a given decarbonization pathway corresponds to a NZE

- Portfolio decarbonization pathway use carbon intensity decarbonization pathway rather than carbon emissions pathway

- The investor can deduce an intensity decarbonization pathway from a decarbonization pathway

- PAB and CAB are ad-hoc portfolio intensity decarbonization pathways that doesn't rely on a global emissions scenario

- PAB and CAB resulting intensity decarbonization pathways are far more aggressive than the intensity decarbonization pathway deduced from the IEA Scenario