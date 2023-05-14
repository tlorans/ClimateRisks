
## Portfolio Self-Decarbonization

The objective of net zero investment portfolio, according to the framework proposed by Barahhou et al. (2022), is to promote self-decarbonization rather than sequential decarbonization (ie. decarbonization obtained by the dynamic of the issuers' decarbonization rather than with successive or sequential decarbonization obtained by rebalancement). Indeed, as stated by Barahhou et al. (2022), net zero investing must include a mechanism that respects the endogenous aspect of the decarbonization pathway. If the time-varying decarbonization is only due to rebalancing process, it is clear that the portfolio cannot be claim to be net zero.

### Decarbonization Backtesting

Let $CI(t,x;I_t)$ be the carbon intensity of portfolio $x$ calculated at time $t$ with the information $I_t$ available at time $t$. The portfolio $x(t)$'s WACI must satisfy the following constraint (Barahhou et al., 2022):

\begin{equation}
CI(t, x(t); I_t) \leq (1 - \mathfrak{R}_{CI}(t_0,t))CI(t_0,b(t_0); I_{t_0})
\end{equation}

Where $b(t_0)$ is the benchmark at time $t_0$. 

Let's know formulate this same constraint, but taking into account the fact that the portfolio is rebalanced at time $t+1$ and we will choose a new portfolio $x(t+1)$. The new constraint is then:

\begin{equation}
CI(t + 1, x(t+1); I_{t+1}) \leq (1 - \mathfrak{R}_{CI}(t_0, t+1))CI(t_0, b(t_0);I_{t_0})
\end{equation}

The information on the right hand scale are known (because we only need information from the starting date $I_{t_0}$). The information on the left hand scale depends on the information available in the future rebalance date $I_{t+1}$. We don't have to rebalance (ie. adding carbon reduction by new sequential decarbonization in order to respect the constraint) if:

\begin{equation}
CI(t + 1, x(t); I_{t+1}) \leq (1 - \mathfrak{R}_{CI}(t_0, t+1))CI(t_0, b(t_0);I_{t_0})
\end{equation}

That is if the portfolio $x(t)$ (before the rebalance in $t+1$) has a WACI in $t+1$ that respect the constraint. If not, we need to rebalance in $t+1$ in order to obtain a new set of weights and a new portfolio $x(t+1)$.

The variation between two rebalancing dates $CI(t+1, x(t + 1);I_{t+1}) - CI(t, x(t), I_t)$ is decomposed between two components:

1. The self-decarbonization $CI(t+1, x(t);I_{t+1}) - CI(t, x(t), I_t)$ (the decarbonization due to issuers' self-decarbonization)
2. The additional decarbonization with sequential decarbonization $CI(t+1, x(t + 1);I_{t+1}) - CI(t + 1, x(t), I_{t+1})$ (the decarbonization achieved by rebalancing the portfolio from $x(t)$ to $x(t+1)$)

The self-decarbonization ratio is finally defined as (Barahhou et al., 2022):

\begin{equation}
SR(t+1) = \frac{CI(t, x(t);I_{t}) - CI(t + 1, x(t), I_{t+1})}{CI(t, x(t);I_{t}) - CI(t + 1, x(t + 1), I_{t+1})}
\end{equation}

The higher value for the self-decarbonization ratio $SR(t+1)$ is reached when we do not have to rebalance the portfolio, with the decarbonization achieved through self-decarbonization rather than sequential decarbonization. This is a first step towards the backesting of net zero portoflios. 

To maximize the self-decarbonization ratio, we need to have an idea about the dynamics of the carbon footprint, that is an estimate of $CI(t+1, x(t); I_t)$.

To illustrate this concept of net zero backtesting with the use of the self-decarbonization ratio, let's take this example from Barahhou et al. (2022):

| $s$  | $(1 - \mathfrak{R}_{CI}(t_0, s))CI(t_0, b(t_0);I_{t_0})$ | $CI(s, x(s); I_s)$ | $CI(s + 1, x(s); I_{s+1})$ |   
|---|---|---|---|
|t| 100.0  | 100.0  | 99.0  |  
|t + 1| 93.0  | 93.0  | 91.2  | 
|t + 2| 86.5  | 86.5  | 91.3  | 
|t + 3| 80.4  | 80.4  | 78.1  | 
|t + 4| 74.8  | 74.8  | 74.2  | 
|t + 5| 69.6  | 69.6  | 70.7  | 
|t + 6| 64.7  | 64.7  | 62.0  | 
|t + 7| 60.2  | 60.2  | 60.0  | 
|t + 8| 55.9  | 55.9  | 58.3  | 
|t + 9| 52.0  | 52.0  | 53.5  | 
|t + 10| 48.4  | 48.4  | 50.5  | 

Let's apply this example in Python. First, we create a `NetZeroBacktesting` with the methods we need:
```Python

@dataclass 
class NetZeroBacktesting:

  CI_s_star: np.array # Targets
  CI_s_x: np.array # Carbon Intensity of the portfolio x at s
  CI_s_plus_one_x: np.array # Carbon intensity of the portfolio x at s+1

  def get_self_decarbonization_ratio(self):
    sr_s = []

    for t in range(len(self.CI_s_star)-1):
      sr = (self.CI_s_x[t] - self.CI_s_plus_one_x[t]) / (self.CI_s_x[t] - self.CI_s_x[t+1])
      sr_s.append(sr)
    
    return sr_s

  def get_self_decarbonization(self):
    return [self.CI_s_plus_one_x[t] - self.CI_s_x[t] for t in range(0, len(self.CI_s_x) - 1)]
    
  def get_sequential_decarbonization(self):
    return [self.CI_s_x[t+1] - self.CI_s_plus_one_x[t] for t in range(0, len(self.CI_s_x)-1)]
```

Then we can implement our example:
```Python
CI_s_star = [100.0, 93.0, 86.5, 80.4, 74.8, 69.6, 64.7, 60.2, 55.9, 52.0, 48.4]
CI_s_x =  [100.0, 93.0, 86.5, 80.4, 74.8, 69.6, 64.7, 60.2, 55.9, 52.0, 48.4]
CI_s_plus_one_x = [99.0, 91.2, 91.3, 78.1, 74.2, 70.7, 62.0, 60.0, 58.3, 53.5, 50.5]

test = NetZeroBacktesting(CI_s_star = CI_s_star,
                          CI_s_x = CI_s_x,
                          CI_s_plus_one_x = CI_s_plus_one_x)
```

And let's plot the results:

```Python
self_decarbonization = np.array(test.get_self_decarbonization())
negative_decarbonization = np.zeros(len(self_decarbonization))
negative_decarbonization[np.where(self_decarbonization > 0)] = self_decarbonization[np.where(self_decarbonization > 0)]
self_decarbonization[np.where(self_decarbonization > 0)] = 0
sequential_decarbonization = np.array(test.get_sequential_decarbonization())

import matplotlib.pyplot as plt 

s = ["t+1","t+2", "t+3","t+4","t+5","t+6","t+7","t+8","t+9","t+10"]

fig, ax = plt.subplots()
fig.set_size_inches(10, 10)

ax.bar(s, sequential_decarbonization, label='Sequential decarbonization', color ='b')
ax.bar(s, self_decarbonization,
       label='Self-decarbonization', color = 'g')
ax.bar(s, negative_decarbonization,
       label='Negative decarbonization', color = 'r')
ax.legend()
```

```{figure} nzebacktestingsequential.png
---
name: nzebacktestingsequential
---
Figure: Sequential versus self-decarbonization
```

In this example, we can see that almost all yearly portfolio decarbonization comes from the rebalancement process (sequential decarbonization). This is typically what we can expect by applying the PAB methodology. Indeed, because the PAB approach doesn't integrate any information about carbon footprint dynamics, the PAB's decarbonization is almost entirely due to sequential decarbonization.

### Integrating Carbon Footprint Dynamics

In the previous section, we have performed a portfolio alignment by considering a global decarbonization path for the portfolio, as recommended by the PAB approach. In this section, we consider the decarbonization path of the issuers, as in Le Guenedal and Roncalli (2022 {cite:p}`le2022portfolio`) and Barahhou et al. (2022). This approach should help in improving the self-decarbonization ratio of the portfolio.

In order to have an idea of the potential issuers carbon footprint dynamics, we can exploit the historical trajectory of the past carbon emissions. We can therefore, as Roncalli et al. (2022), estimate the associated linear trend model and project the future carbon emissions by assuming that the issuer will do the same efforts in the future than in the past.

Le Guenedal et and Roncalli (2022) define the carbon trend by considering the following linear constant trend model:

\begin{equation}
CE(t) = \beta_0 + \beta_1 \cdot t + u(t)
\end{equation}

The parameters $\beta_0$ and $\beta_1$ can be estimated with the least squares methods on a sample of observations. 

The projected carbon trajectory is then given by:

\begin{equation}
CE^{Trend}(t) = \hat{CE}(t) = \hat{\beta_0} + \hat{\beta_1}t
\end{equation}

The underlying idea heare is to extrapolate the past trajectory. However, we need to reformulate our previous model. Indeed, it is not easy to interpret as $\hat{\beta_0} = \hat{CE(0)}$ when $t = 0$. We can add a base year $t_0$, that converts our model to:

\begin{equation}
CE(t) = \beta'_0 + \beta'_1(t - t_0) + u(t)
\end{equation}

And the carbon trajectory is now given by:

\begin{equation}
CE^{Trend}(t) = \hat{\beta'_0} + \hat{\beta'_1}(t - t_0)
\end{equation}

This change is just a matter of facilitating the interpretration. Indeed, the two models are equivalent and give the same value $\hat{CE}(t)$ with:

\begin{equation}
\beta'_0 = \beta_° + \beta_1 t_0
\end{equation}

and 

\begin{equation}
\beta'_1 = \beta_1
\end{equation}

The only change resulting from the new formulation is that now $\hat{\beta}'_0 = \hat{CE}(t_0)$

Let's implement this with an example in Python:
```Python
years = [i for i in range(2007, 2021)]
emissions = [57.8, 58.4, 57.9, 55.1,
            51.6, 48.3, 47.1, 46.1,
            44.4, 42.7, 41.4, 40.2, 41.9, 45.0]

import pandas as pd
import statsmodels.api as sm

X = pd.Series([years[t] - years[-1] for t in range(len(years))])
X = sm.add_constant(X)
Y = pd.Series(emissions)
model = sm.OLS(Y, X)
results = model.fit()
results.params
```
Our estimates for $\hat{\beta_0}'$ and $\hat{\beta_1}'$ are:

```
const    38.988571
0        -1.451209
dtype: float64
```

And now we can define a function `forecast_carbon_emissions` for determining $CE^{Trend}(t)$:

```Python
beta_0 = results.params["const"]
beta_1 = results.params[0]

def forecast_carbon_emissions(beta_0:float, beta_1:float, t:int) -> float:
  carbon_trend = beta_0 + beta_1 * (t - 2020)
  return carbon_trend

forecast_carbon_emissions(beta_0 = beta_0,
                          beta_1 = beta_1,
                          t = 2025)
```

And the result is:

```
31.73252747252748
```

We can apply the same process on the carbon intensity $CI^{Trend}(t)$, rather than the carbon emissions level.
The optimization problem is the same as the previous optimization problem except that we include projected trends (of carbon intensity) in place of current intensities for the portfolio's WACI:

\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2} (x(t)-b(t))^T \Sigma(t)(x(t)-b(t))\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & &  0_n \leq x \leq 1_n \\
& & & CI^{trend}(x(t)) \leq (1 - \mathfrak{R}_{CI}(t_0,t))CI(b(t_0)) \\
\end{aligned}
\end{equation*}


### Key Takeaways 

- Barahhou et al. (2022) introduced the concept of net zero backtesting: as net zero investing promotes self-decarbonization rather than sequential decarbonization, investors need to be able to verify where does the portfolio's decarbonization comes from, with the self-decarbonization ratio for example.

- Improving the self-decarbonization ratio calls for the integration of issuers' carbon footprint dynamics. It constrats with the PAB's approach, that doesn't include any forward-looking information. PAB's decarbonization comes almost entirely from sequential decarbonization.

- We introduce a measure of carbon footprint dynamics in our optimization problem, that could help in improving the self-decarbonization ratio.