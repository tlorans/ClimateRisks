# Net Zero Backtesting

While we've seen that the adoption of portfolio alignment to a decarbonization pathway leads to a dynamic strategy, questions arise about the status of the portfolio time-varying decarbonization.

Indeed, the time-varying portfolio decarbonization can comes from (Barahhou et al., 2022):
- sequential decarbonization with successive rebalancements ie. an exogenous decarbonization
- self-decarbonization ie. an endogenous decarbonization

In our sense, a time-proofed portfolio alignment strategy should mostly relies on self-decarbonization rather than decarbonization coming from successive rebalancements (ie. we must ensure that resulting portfolio has endogenized the decarbonization pathway and is on track with the NZE scenario).

In this part, we cover the concept of net zero backtesting and the self-decarbonization ratio, introduced by Barahhou et al. (2022). 

## Sequential vs. Self-Decarbonization

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


## The Self-Decarbonization Ratio

The self-decarbonization ratio is finally defined as (Barahhou et al., 2022):

\begin{equation}
SR(t+1) = \frac{CI(t, x(t);I_{t}) - CI(t + 1, x(t), I_{t+1})}{CI(t, x(t);I_{t}) - CI(t + 1, x(t + 1), I_{t+1})}
\end{equation}

The higher value for the self-decarbonization ratio $SR(t+1)$ is reached when we do not have to rebalance the portfolio, with the decarbonization achieved through self-decarbonization rather than sequential decarbonization. This is a first step towards net zero backtesting. 

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

In this example, we can see that almost all yearly portfolio decarbonization comes from the rebalancement process (sequential decarbonization). This is typically what we can expect if we use backward-looking data for such a forward-looking exercice.
