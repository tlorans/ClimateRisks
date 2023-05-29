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

```{figure} temp_increase2.png
---
name: temp_increase
---
Figure: Global Warming Without Mitigation Policies ($\mu(t)=0$) (Roncalli, 2023)
```

We have a sense of the tragedy of the horizon with this figure. Indeed, if no mitigation policy is taken, global temperature is expected to attain level resulting in important economic losses by the end of this century, while economic losses due to more stringent mitigation policies are expected to be immediate.