## Portfolio Alignment

We've seen in the low-carbon strategy framework how investors can conduct a portfolio decarbonization with a static approach. On the other side, net zero investing involves portfolio alignment with a decarbonization pathway, rather than a simple static decarbonization. It involves a dynamic strategy in order to comply with the given net zero scenario.

The dynamic problem is trickier since it involves rebalancing decisions and depends on the future behavior of corporate issuers. 

In this part, we are going to compare the approach for performing a portfolio alignment with the Paris-Aligned Benchmarks (PAB) and the NZE frameworks. The main difference between both approaches is that portfolio alignment is conducted at the portfolio level in the PABs, while portfolio alignment is checked at the stock level in the NZE approach.


### Net Zero Backtesting

The objective of net zero investment portfolio is to promote self-decarbonization rather than sequential decarbonization (ie. decarbonization obtained by the dynamic of the issuers' decarbonization rather than with successive or sequential decarbonization obtained by rebalancement).

Let $CI(t,x;F_t)$ be the carbon intensity of portfolio $x$ calculated at time $t$ with the information $F_t$ available at time $t$.

The portfolio $x(t)$ must satisfy:

\begin{equation}
CI(t, x(t); F_t) \leq (1 - \mathfrak{R}_{CI}(t_0,t))CI(t_0,b(t_0); F_{t_0})
\end{equation}

Where $b(t_0)$ is the benchmark at time $t_0$. The portfolio is rebalanced at time $t+1$ and we will choose a new portfolio $x(t+1)$ such that:

\begin{equation}
CI(t + 1, x(t+1); F_{t+1}) \leq (1 - \mathfrak{R}_{CI}(t_0, t+1))CI(t_0, b(t_0);F_{t_0})
\end{equation}

We don't have to rebalance (ie. add carbon reduction by new sequential decarbonization) if:

\begin{equation}
CI(t + 1, x(t); F_{t+1}) \leq (1 - \mathfrak{R}_{CI}(t_0, t+1))CI(t_0, b(t_0);F_{t_0})
\end{equation}

The variation between two rebalancing dates $CI(t+1, x(t + 1);F_{t+1}) - CI(t, x(t), F_t)$ is decomposed between two components:

1. The self-decarbonization $CI(t+1, x(t);F_{t+1}) - CI(t, x(t), F_t)$
2. The additional decarbonization with sequential decarbonization $CI(t+1, x(t + 1);F_{t+1}) - CI(t + 1, x(t), F_{t+1})$

The self-decarbonization ratio is then defined as:

\begin{equation}
SR(t+1) = \frac{CI(t, x(t);F_{t}) - CI(t + 1, x(t), F_{t+1})}{CI(t, x(t);F_{t}) - CI(t + 1, x(t + 1), F_{t+1})}
\end{equation}

The upper bound is reached when do not have to rebalance the portfolio, with the decarbonization achieved through self-decarbonization rather than sequential decarbonization. This is a first step towards the backesting of net zero portoflios. 

To maximize the self-decarbonization ratio, we need to have an idea about the dynamics of the carbon footprint, that is an estimate of $CI(t+1, x(t); F_t)$.

```Python
# Reproduces table 4 page 23 of Net Zero Investment portfolio
```

```Python
# Reproduces figure 45 and 46 page 87 in net zero investment portfoli
```

### Dynamic Decarbonization at Portfolio Level

Let's first address the PAB approach of the dynamic portfolio decarbonization. 

At date $t$, the PAB label imposes the following inequality constraint for the portfolio $x(t)$:

\begin{equation}
CI(x(t)) \leq (1 - \mathfrak{R}_{CI}(t_0,t))CI(b(t_0))
\end{equation}

The base year $t_0$ thus defines the reference level of the carbon intensity, as the reference level is $CI(b(t_0))$ and not $CI(b(t))$. This is a first important difference compared to the low-carbon strategy.

In this case, the decarbonization problem becomes dynamic:
\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2} (x(t)-b(t))^T \Sigma(t)(x(t)-b(t))\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & &  0_n \leq x \leq 1_n \\
& & & CI(x(t)) \leq (1 - \mathfrak{R}_{CI}(t_0,t))CI(b(t_0))
\end{aligned}
\end{equation*}

In this problem, finding $x^*(t)$ at time $t$ requires to know the covariance matrix $\Sigma(t)$, the carbon intensities $CI(t)$ and the investable universe $b(t)$. However, in the current year $t_1$ the observations are only available for $t_0$ and $t_1$. We can however do the exercise b assuming that the world does not change. In this case, we can assume that the covariance matrix, the carbon intensities and the investable universe remain constant, such as:

\begin{equation}
\Sigma(t) = \Sigma(t_0)
\end{equation}
\begin{equation}
CI(t) = CI(t_0)
\end{equation}
\begin{equation}
b(t) = b(t_0)
\end{equation}

```Python
# show figure of projected decarbonation
```

```Python
#show figure of projected tracking error
```

```Python
# Apply figure 45 and 46 page 87 in net zero investment portfolio with PAB strat
```

### Dynamic Decarbonization at Stock Level

In the previous section, we have performed a portfolio alignment by considering a global decarbonization path for the portfolio, as recommended by the PAB approach. In this section, we consider the decarbonization path of the issuers, as in Le Guenedal and Roncalli (2022). 

Carbon emission trends.

```Python
# reproduce figure 20 for few stocks in page 38 of portfolio construction with climate risk
```

The optimization problem is the same as the previous optimization problem except that we explicitly introduce the NZE trajectories for the individual carbon intensity trajectories.

```Python
# Reproduce Table 11 in page 40 of Portfolio Construction with Carbon Risk
```
