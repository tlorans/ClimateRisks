# Long Run Risk
 
Another solution to the equity premium puzzle is, combined with the Epstein Zin preferences, the concept of stochasic volatility from Bansal and Yaron (2004):

\begin{equation}
\Delta c_{t+1} = \mu + x_t + \sigma_t \eta_{t+1}
\end{equation}
\begin{equation}
x_{t+1} = \rho x_t + \phi_x \sigma_t \epsilon_{t+1}
\end{equation}
\begin{equation}
\sigma^2_{t+1} = \sigma^2(1 - \nu) + \nu \sigma^2_t + \sigma_w w_{t+1}
\end{equation}

with $\eta_{t+1}$, $\epsilon_{t+1}$, $w_{t+1} \sim \text{iid} N(0,1)$

That is, the growth rate of consumption contains a small predictable component $x$ that determines the condiional mean of consumption growth. The autoregressive parameter $\rho$ captures the persistence of this expected growth process, and $\phi_x$ determines the amomunt of predicatble variation in realized consumption growth. $\mu$ is the unconditional mean $\Delta c$. 

Fluctuating economic uncertainty is modeled as time-varying volatility of consumption growth, $\sigma_t$. The permanence of volatility shocks depends on the parameter $\nu$. $\sigma$ represents the unconditional volatility of consumption process. We assume all shocks uncorrelated.

## Method of Undetermined Coefficients and Log-Linearization

Deriving the Elasticity Coefficients from the Euler Equation

same value function than before, therefore no changes to the initial Euler equation.

Since consumption is an exogenous process, a solution for the price-consumption ratio leads to a complete characterization of the return on the wealth portfolio. Denote the log of the valuation ratio of the consumption asset as:

\begin{equation}
z_t = \log(\frac{P_t}{C_t})
\end{equation}

The relevant state variables to derive the solutions for $z_t$ are the expected growth component $x_t$ and the stochastic volatility component $\sigma_t^2$.

We consider the equilibrium price-consumption ratio. We can conjecture, using the method of undetermined coefficients, that $z_t$ is linear in the states variables:

\begin{equation}
z_t = A_0 + A_1 x_t + A_2 \sigma^2_t
\end{equation}

LECTURES NOTES ON ASSET PRICING WITH EPSTEIN ZIN

## 