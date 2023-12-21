# Long-Run Risk Model: Equilibrium Conditions

The Long-Run Risk Model (LLRM) introduced by Bansal and Yaron (2004 {cite:p}`bansal2004risks`) is one of the main theoretical pillars in financial macroeconomics. In its original version, the LRRM reconciles several key asset pricing phenomena in a unified framework by combining recursive preferences à la Epstein and Zin (1989 {cite:p}`epstein1991substitution`) with a model of aggregate consumption growth that exhibits predictable low-frequency movements and time-varying volatility. 

## The Value Function

The previous models were based on time-separable utility. An alternative approach is to assume time-nonseparable utility. 

The representative agent in LRRM has Epstein and Zin (1989) type preferences, which allow for a separation of risk aversion and the elastricity of intertemporal substitution. Specifically, the agent maximizes her life-time utility, defined as:

\begin{equation}
V_t = [(1 - \delta)C_t^{\frac{1 - \gamma}{\theta}} + \delta(\mathbb{E}_t[V_{t+1}^{1 - \gamma}])^{\frac{1}{\theta}}]^{\frac{\theta}{1 - \gamma}}
\end{equation}

where $C_t$ is consumption at time $t$, $0 < \delta < 1$ reflects the agent's time preferences, $\gamma$ is the coefficient of risk aversion, $\theta = \frac{1 - \gamma}{1 - \frac{1}{\psi}}$ and $\psi$ is the elastici of intertemporal substitution (IES). Utility maximization is subject to the budget constraint:

\begin{equation}
W_{t+1} = (W_t - C_t)R_{c,t+1}
\end{equation}

where $W_t$ is the wealth of the agent and $R_{c,t}$ is the return on all invested wealth.

Consumption growth has the following dynamics:

\begin{equation}
\Delta c_{t+1} = \mu_c + x_t + \sigma_t \eta_{t+1}
\end{equation}

\begin{equation}
x_{t+1} = \rho x_t + \phi_e \sigma_t e_{t+1}
\end{equation}

\begin{equation}
\sigma^2_{t+1} = \bar{\sigma}^2 + \nu(\sigma^2_t - \bar{\sigma}^2) + \sigma_w w_{t+1}
\end{equation}

Where $\Delta c_{t+1}$ is the growth rate of log consumption. The conditional expectation of consumption growth is given by $\mu_c + x_t$ where $x_t$ is a small but persistent component that captures long-run risks in consumption growth. The parameter $\rho$ determines the persistence in the condtional mean of consumption growth. There is a common time-varying volatility in consumption, which leads to time-varying risk premia. The unconditional variance of consumption is $\bar{\sigma}^2$ and $\nu$ governs the persistence of the volatility process.

With $W_{t+1}$ as our control variable and $W_t$ and $\sigma_t$ the state variables:

\begin{equation}
V(W_t, \sigma_t) = \max_{W_{t+1}} [(1 - \delta)C_t^{\frac{1 - \gamma}{\theta}} + \delta(\mathbb{E}_t[V(W_{t+1}, \sigma_{t+1})^{1 - \gamma}])^{\frac{1}{\theta}}]^{\frac{\theta}{1 - \gamma}}
\end{equation}

## Equilibrium Conditions