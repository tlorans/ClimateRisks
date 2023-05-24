# Introduction
## Economics and Physics of Climate Risk: The Tragedy of the Horizon

As climate risk is a hot topic in Finance, a step back into the economics and physics of climate change is needed in order to understand it. In particular, we want to highlight the sources of the tragedy of the horizon as explained by Mark Carney in his famous speech (2015) {cite:p}`carney2015breaking`.

In what follows, we dig into the DICE 2013 model (Nordhaus and Sztorc, 2013 {cite:p}`nordhaus2013dice`), following the notations and presentation by Roncalli (2023). 
### Economics and Climate Risk

We start with the economics settings of the DICE 2013 model (Nordhaus and Sztorc, 2013). The gross production $Y(t)$ is given by a standard Cobb-Douglas function:

\begin{equation}
Y(t) = A(t)K(t)^{\gamma}L(t)^{1 - \gamma}
\end{equation}

with $A(t)$ the total productivity factor (or technological progress), $K(t)$ the capital input, $L(t)$ the labor input and $\gamma \in ]0,1[$ measures the elasticity of the capital factor:

\begin{equation}
\gamma = \frac{\partial ln Y(t)}{\partial ln K (t)} = \frac{\partial Y(t)}{\partial K(t)} \frac{K(t)}{Y(t)}
\end{equation}

In the Integrated Assessment Models (IAMs), we have a distinction between the production $Y(t)$ and net output $Q(t)$ because climate risk generate losses:

\begin{equation}
Q(t) = \Omega_{climate}(t)Y(t) \leq Y(t)
\end{equation}

where $\Omega_{climate}(t) \in ]0,1[$ is the loss percentage of the production. 

$Q(t)$ is thus the net output when taking into account damages from climate change. 

### Physical Risk and Transition Risk

We've seen that the net output is reduced because of climate change. We have:

\begin{equation}
\Omega_{climate}(t) = \Omega_D(t)\Omega_{\Lambda}(t) = \frac{1}{1 + D(t)}(1 - \Lambda(t))
\end{equation}

with $D(t) \geq 0$ corresponds to the damage function (physical risk) and $\Lambda(t) \geq 0$ is the mitigation or abatement cost (transition risk).

The costs $D(t)$ or physical risk result from natural disasters and climatic events (wildfires, floods, storms, etc.). The costs $\Lambda(t)$ come from reducing GHG emissions and policiy for financing the transition to a low-carbon economy.

Nordhaus and Sztorc (2013) assume that $D(t)$ is a function of the atmospheric temperature $T_{AT}(t)$:

\begin{equation}
D(t) = \psi_1 T_{AT}(t) + \psi_2 T_{AT}(t)^2
\end{equation}

with $\psi_1 \geq 0$ and $\psi_2 \geq 0$ are two exogenous parameters. $T_{AT}(t)$ corresponds to the global mean surface tempature increase in °C from 1900.
We then have the fraction of net output lost because of global warming defined as:

\begin{equation}
\mathfrak{L}_D(t) = 1 - \Omega_D(t) = 1 - (1 + D(t))^{-1} 
\end{equation}

Various implementations of the damage function have been proposed in the literature, such as:
- Weitzman (2009 {cite:p}`weitzman2009modeling`, 2010 {cite:p}`weitzman2010damages`, 2012 {cite:p}`weitzman2012ghg`)
- Hanemann (2008 {cite:p}`hanemann2008economic`)
- Pindyck (2012 {cite:p}`pindyck2012uncertain`)
- Newbold-Marten (2014 {cite:p}`newbold2014value`)


```{figure} damage_function.png
---
name: damage_function
---
Figure: Loss Function due to Climate Damage Costs (Roncalli, 2023)
```

The abatement cost function depends on the control variable $\mu(t)$:

\begin{equation}
\Lambda(t) = \theta_1(t)\mu(t)^{\theta_2}
\end{equation}

with $\theta_1 \geq 0$ and $\theta_2 \geq 0$ are two parameters, and $\mu(t) \in ]0,1[$ the emission-control rate.

Below is a figure taken from Roncalli (2023) and showing the immediate and long-lasting economic losses due to the implementation of a stringent transition policy (higher $\mu(t)$).

```{figure} abatement_function.png
---
name: abatement_function
---
Figure: Abatement Cost Function (Roncalli, 2023)
```

We finally have the global impact of climate change as:

\begin{equation}
\Omega_{climate}(t) = \frac{1 - \theta_1(t)\mu(t)^{\theta_2}}{1 + \psi_1 T_{AT}(t) + \psi_2 T_{AT}(t)^2}
\end{equation}

### Global Warming

Let's now have a basic view of the physics of the DICE model, in order to have a sense of mechanisms behind the global warming. 

The GHG emissions $CE(t)$ depends on the production $Y(t)$ and the land use emissions $CE_{Land}(t)$:

\begin{equation}
CE(t) = CE_{Industry}(t) + CE_{Land}(t)
\end{equation}

\begin{equation}
= (1 - \mu(t))\sigma(t)Y(t) + CE_{Land}(t)
\end{equation}

where $\sigma(t)$ is the impact of the production on GHG emissions, $CE_{Industry}(t)$ corresponds to the anthropogeneic emissions due to industrial activities, and the dynamic of $CE_{Land}(t)$ is described as:

\begin{equation}
CE_{Land}(t) = (1 - \delta_{Land})CE_{Land}(t-1)
\end{equation}

with $\delta_{Land}$ a parameter.

The control variable $\mu(t)$ introduced previously measures the impact of climate change mitigation policies.

We have two extreme cases:

1. If $\mu(t) = 1$, mitigation policies have eliminated the anthropogenic emissions and then $CE(t) = CE_{Land}(t)$
2. If $\mu(t) = 0$, no specific policy has been put in place and we have $CE(t) = \sigma(t)Y(t) + CE_{Land}(t)$

In the DICE model, $\mu(t)$ is an endogenous variable and can be viewed as an effort rate that the economy must bear to limit global warming.

$\sigma(t)$ measures the relationshp between the carbon emissions due to anthropogenic activities and the gross output in the absence of mitigation policies ($\mu(t) = 0$):

\begin{equation}
\sigma(t) = \frac{CE_{Industry}(t)}{Y(t)}
\end{equation}

It can be interpreted as the carbon intensity of the economy.

The relationship between the carbon emissions $CE(t)$ and the atmospheric temperature $T_{AT}(t)$ uses a reduced for of a global circulation model in the DICE 2013 model, describing the evolution of GHG concentratins in three carbon-sink reservoirs:

- the atmosphere $AT$
- the upper ocean $UP$
- the deep (or lower) ocean $LO$

Nordhaus and Sztorc (2013) assume the following dynamics of carbon concentrations:

\begin{equation}
CC_{AT}(t) = \phi_{1,1}CC_{AT}(t-1) + \phi_{1,2}CC_{UP}(t-1) + \phi_1CE(t)
\end{equation}
\begin{equation}
CC_{UP}(t) = \phi_{2,1}CC_{AT}(t-1)+\phi_{2,2}CC_{UP}(t-1) + \phi_{2,3}CC_{LO}(t-1)
\end{equation}
\begin{equation}
CC_{LO}(t) = \phi_{3,2}CC_{UP}(t-1) + \phi_{3,3}CC_{LO}(t-1)
\end{equation}

with $\phi_{i,j}$ the flow parameters between carbon-sink reservoirs, and $\phi_1$ the mass percentage of carbon in CO2.

Let's define $CC$ as the vector of the three-reservoir layers:

\begin{equation}
CC = \begin{bmatrix}
CC_{AT} \\
CC_{UP} \\
CC_{LO}
\end{bmatrix}
\end{equation}

We then have the dynamics of $CC$ as a vector autoregressive process:

\begin{equation}
CC(t) = \Phi_{CC}CC(t-1) + B_{CC}CE(t)
\end{equation}

with:

\begin{equation}
B_{CC} = \begin{bmatrix}
\phi_1 \\
0 \\
0
\end{bmatrix}
\end{equation}

and:

\begin{equation}
\Phi_{CC} = \begin{bmatrix}
\phi_{1,1} & \phi_{1,2} & 0 \\
\phi_{2,1} & \phi_{2,2} & \phi_{3,2} \\
0 & \phi_{3,2} & \phi_{3,3}
\end{bmatrix}
\end{equation}

We can now link accumulated carbon emissions in the atmosphere and global warming at the earth's surface through increases in radiative forcing:

\begin{equation}
F_{RAD}(t) = \frac{\eta}{ln2}ln(\frac{CC_{AT}(t)}{CC_{AT}(1750)}) + F_{EX}(t)
\end{equation}

with $F_{RAD}(t)$ the change in total radiative forcing of GHG emissions since 1750, $\eta$ the temperature forcing parameter and $F_{EX}(t)$ an exogenous forcing.

We finally achieve to obtain the climate system for temperatures from the DICE 2013 model as:

\begin{equation}
T_{AT}(t) = T_{AT}(t-1) + \xi_1(F_{RAD}(t) - \xi_2 T_{AT}(t-1) - \xi_3(T_{AT}(t-1) - T_{LO}(t-1)))
\end{equation}
\begin{equation}
T_{LO}(t) = T_{LO}(t-1) + \xi_4(T_{AT}(t-1) - T_{LO}(t-1))
\end{equation}

with $T_{AT}(t)$ the mean surface temperature, $T_{LO}(t)$ the temperature of the deep ocean, $\xi_1$ the speed of adjustment parameter for the atmospheric temperature, $\xi_2$ the ratio of increased forcing from CO2 doubling to the climate sensitivity, $\xi_3$ the heat loss coefficient from atmosphere to oceans and $\xi_4$ the heat gain coefficient by deep oceans.

Therefore, to limite global warming $T_{AT}(t)$, we need to reduce the radiative forcing $F_{RAD}(t)$ that is a function of the carbon concentration $CC_{AT}(t)$ in the atmosphere.


Carbon concentration in the atmosphere is reduced by emitting lower carbon emissions. To achieve carbon emissions reduction, we have three choices:

1. Reducing the production $Y(t)$
2. Reducing the carbon intensity $\sigma(t)$ of industrial activities
3. Increasing the mitiation effort $\mu(t)$ and accelerating the transition to a low-carbon economy

Below is a figure taken from Roncalli (2013) and showing the expected temperature increase if no mitigation policies is undertaken.

```{figure} temp_increase.png
---
name: temp_increase
---
Figure: Global Warming Without Mitigation Policies ($\mu(t)=0$) (Roncalli, 2023)
```

We have a sense of the tragedy of the horizon with this figure. Indeed, if no mitigation policy is taken, global temperature is expected to attain level resulting in important economic losses by the end of this century, while economic losses due to more stringent mitigation policies are expected to be immediate.

## Portfolio Decarbonization

While perspectives regarding climate physical risk impacts are uncertain and expected to mostly occur in a very long-term horizon, potential transition risk is a sword of Damocles for investors. Indeed, the prospect of policy interventions has increased significantly following the Paris Climate Chance Conference. Therefore, there is a risk with respect to the magnitude and the timing of climate mitigation policies. 
In such an increasing climate risk awaraness, climate investing grew up as a specific field in Finance, proposing "green" portfolio strategies.

One of the main approach so far is portfolio decarbonization or low-carbon strategy, starting from a standard benchmark and removing or underweighting the companies with high carbon footprints.

Decarbonized portfolios are structured to maintain a low tracking error with respect to the benchmark index.

The main point underlying the climate risk-hedging strategy using decarbonization is to keep an aggregate risk exposure similar to that of the standard initial benchmark by minimizing tracking error, while diminishing carbon intensity, seen as a fundamental proxy for carbon risk exposure. 

Minimizing the TE leads to a strategy that obtain similar returns to the benchmark index as long as mitigation policies are postponed. But once significant mitigation policies are introduced, the decarbonized portfolio should outperform the benchmark, as high-emitters stocks should face an abrupt repricing.

In what follows, we will cover the low-carbon strategy proposed by Andersson et al. (2016), following Roncalli (2023) presentation and notations.

We begin by introducing the concept of portfolio optimization in the context of a benchmark, highlighting the minimization of the tracking error (Roncalli, 2013, 2023) concept.

### Portfolio Optimization in the Context of a Benchmark

As noted by Roncalli (2013), in practice, many problems consist in tracking a benchmark while improving some properties (reducing the carbon portfolio for example). To construct such a portfolio tracking a benchmark, the main tool is to control the tracking error, that is the difference between the benchmark's return and the portfolio's return.

In the presence of a benchmark, the expected return of the portfolio $\mu(x)$ is replaced by the expected excess return $\mu(x|b)$. The volatility of the portfolio $\sigma(x)$is replaced by the volatility of the tracking error $\sigma(x|b)$ (Roncalli, 2013):

\begin{equation*}
\begin{aligned}
& x^* = 
& & argmin \frac{1}{2} \sigma^2 (x|b) - \gamma \mu(x|b)\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & & 0_n \leq x \leq 1_n
\end{aligned}
\end{equation*}

Without any further constraint, the optimal solution $x^*$ will be equal to the benchmark weights $b$. This is the case of a perfect replication strategy. An enhanced or tilted version will add further constraints, depending on the objective of the strategy (decarbonization for example). We have a few more steps to consider before finding our QP formulation parameters.

First, let's recall that:
\begin{equation}
\sigma^2(x|b) = (x - b)^T \Sigma (x -b)
\end{equation}

and
\begin{equation}
\mu(x|b) = (x -b)^T \mu
\end{equation}

If we replace $\sigma^2(x|b)$ and $\mu(x|b)$ in our objective function, we get:

\begin{equation}
* = \frac{1}{2}(x-b)^T \Sigma (x -b) - \gamma (x -b)^T \mu
\end{equation}

With further developments, you end up with the following QP objective function formulation:
\begin{equation}
* = \frac{1}{2} x^T \Sigma x - x^T(\gamma \mu + \Sigma b)
\end{equation}

We have exactly the same QP problem than with a long-only mean-variance portfolio, except that $q = -(\gamma \mu + \Sigma b)$.

### The Decarbonization Optimization Problem

We present the decarbonization optimization problem following the threshold approach (Roncalli, 2023).
With the threshold approach, the objective is to minimize the tracking error with the benchmark while imposing a reduction $\mathfrak{R}$ in terms of carbon intensity. In practice, implementing such approach involves the weighted-average carbon intensity (WACI) computation and the introduction of a new constraint in a portfolio optimization problem with the presence of a benchmark (Roncalli, 2013). In this part, we first define the WACI, and then introduce the threshold approach as an additional constraint to the portfolio optimization with a benchmark problem seen in the previous part.

The weighted-average carbon intensity (WACI) of the benchmark is:

\begin{equation}
CI(b) = b^T CI
\end{equation}

With $CI = (CI_1, ..., CI_n)$ the vector of carbon intensities.

The same is for the WACI of the portfolio:

\begin{equation}
CI(x) = x^T CI
\end{equation}

The low-carbon strategy involves the reduction $\mathfrak{R}$ of the portfolio's carbon intensity $CI(x)$ compared to the benchmark's carbon intensity $CI(b)$. It can be viewed as the following constraint (Roncalli, 2023):

\begin{equation}
CI(x) \leq (1 - \mathfrak{R})CI(b)
\end{equation}

The optimization problem becomes:

\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2}(x-b)^T \Sigma (x - b)\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & & 0_n \leq x \leq 1_n \\
&&&  CI(x) \leq (1 - ℜ) CI(b)
\end{aligned}
\end{equation*}

with the following QP parameters:

\begin{equation*}
\begin{aligned}
& P = \Sigma \\
& q = - \Sigma b \\
& A = 1^T_n \\
& b = 1 \\
& G = CI^T \\
& h = CI^{+} = (1 - ℜ)CI(b) \\
& lb = 0_n \\
& ub = 1_n
\end{aligned}
\end{equation*}

Below is a figure illustrating the efficient decarbonization frontier achieved with this approach. We underlines the trade-off between portfolio decarbonization and the TE.

```{figure} thresholdapproach.png
---
name: thresholdapproach
---
Figure: Efficient Decarbonization Frontier with Threshold Approach
```

Because we impose a constraint and minimize the TE risk, the resulting portfolio will have fewer stocks than the initial benchmark $b$. This imply that the portfolio $x$ is less diversified than the initial benchmark $b$. In order to explicitly control the number of removed stocks, Andersson et al. (2016) and Roncalli (2023) propose alternative approaches such as the order-statistic. In this course, we will focus on this threshold approach.

Below is a figure taken from Andersson et al. (2016) and illustrating his low-carbon strategy property of providing similar returns than the benchmark while reducing the portolio's WACI.

```{figure} andersson_example.png
---
name: andersson_example
---
Figure: S&P 500 and S&P US Carbon Efficient Indexes, from Andersson et al. (2016)
```

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
## Key Takeaways

- Physical risk is expected to occur by the end of the century, while transition risk can occur during the next decade: this is the consequence of the tragedy of horizons, coming from the economics and physics of climate change. Therefore, studies (and this course) focus on transition risk (in fact, carbon risk)

- Portfolio decarbonization has been proposed as a climate risk integration strategy by Andersson et al. (2016). It consists in minimizing the tracking error with the benchmark while reducing the carbon footprint of the portfolio. 

- We know that the objective of potential climate mitigations policies will be to track a NZE scenario. A robust portfolio decarbonization should target portfolio alignment with this NZE scenario, and thus adopt a dynamic approach.