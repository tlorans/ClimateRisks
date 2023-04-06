## Portfolio Alignment

We've seen in the low-carbon strategy framework how investors can conduct a portfolio decarbonization with a static approach. On the other side, net zero investing involves portfolio alignment with a decarbonization pathway, rather than a simple static decarbonization. It involves a dynamic strategy in order to comply with the given net zero scenario.

The dynamic problem is trickier since it involves rebalancing decisions and depends on the future behavior of corporate issuers. 

In this part, we are going to compare the approach for performing a portfolio alignment with the Paris-Aligned Benchmarks (PAB) and the NZE frameworks. Introducing the concept of Net Zero Backtesting, we'll see that the dynamic decarbonization in the PAB relies on sequential decarbonization rather than self-decarbonization, because the issuers' carbon footprint dynamic is not taken into account. We will introduce carbon footprint dynamics measure, following Roncalli et al. (2022), in order to maximize the self-decarbonization ratio of the net zero portfolio. 

### Dynamic Portfolio's Decarbonization

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
# Reproduces figure 45 and 46 page 87 in net zero investment portfolio
```

By definition, and because the PAB approach doesn't integrate any information about carbon footprint dynamics, the PAB's decarbonization is almost entirely due to sequential decarbonization.

### Integrating Carbon Footprint Dynamics

In the previous section, we have performed a portfolio alignment by considering a global decarbonization path for the portfolio, as recommended by the PAB approach. In this section, we consider the decarbonization path of the issuers, as in Le Guenedal and Roncalli (2022) and Roncalli et al. (2022). This approach allows to improve the self-decarbonization ratio of the portfolio.

#### Carbon Momentum

In order to have an idea of the potential issuers carbon footprint dynamics, we can exploit the historical trajectory of the past carbon emissions. We can therefore, as Roncalli et al. (2022), estimate the associated linear trend model and project the future carbon emissions by assuming that the issuer will do the same efforts in the future than in the past.

Le Guenedal et al. (2022) define the carbon trend by considering the following linear constant trend model:

\begin{equation}
CE(t) = \beta_0 + \beta_1 \cdot t + u(t)
\end{equation}

We can estimate $\beta_0$ and $\beta_1$ using the least squares approach. Then, we can build the carbon trajectory iplied by the trend by applying the projection:

\begin{equation}
\hat{CE}(t) = CE(t_0) + \hat{\beta_1} \cdot (t - t_0)
\end{equation}

Le Guenedal et al. (2022) then define a long-term carbon momentum $CM(t)$ as the ratio between the slope estimated at time $t$, $\hat{\beta_1}(t)$, and the current carbon emissions:

\begin{equation}
CM(t) = \frac{\hat{\beta_1}(t)}{CE(t)}
\end{equation}

```Python
# reproduce figure 20 for few stocks in page 38 of portfolio construction with climate risk
```

#### Managing the Carbon Footprint Dynamic

The optimization problem is the same as the previous optimization problem except that we explicitly introduce the issuers carbon footprint dynamics with the carbon momentum:

\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2} (x(t)-b(t))^T \Sigma(t)(x(t)-b(t))\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & &  0_n \leq x \leq 1_n \\
& & & CI(x(t)) \leq (1 - \mathfrak{R}_{CI}(t_0,t))CI(b(t_0)) \\
& & & CM(t, x) \leq CM^*
\end{aligned}
\end{equation*}

With $CM^*$ a global threshold. For example, setting $CM^* = -7\%$, we expect the aligned portfolio to decarbonize itself by 7\%, improving the self-decarbonization ratio.

```Python
# Reproduce Table 11 in page 40 of Portfolio Construction with Carbon Risk
```

### Key Takeaways 

- Net zero portfolios introduce the notion of portfolio alignment, with a dynamic decarbonization compared to a reference base year. This contrasts with the low-carbon strategy

- Roncalli et al. (2022) intoduced the notion of net zero backtesting: as net zero investment portfolio promote self-decarbonization rather than sequential decarbonization, investors need to be able to verify where does the portfolio's decarbonization comes from, with the self-decarbonization ratio for example

- Improving the self-decarbonization ratio calls for the integration of issuers' carbon footprint dynamics. It constrats with the PAB's approach, that doesn't include any forward-looking information. PAB's decarbonization comes almost entirely from sequential decarbonization.

- We introduce a measure of carbon footprint dynamics in our optimization problem, improving the resulting self-decarbonization ratio.