## Portfolio Alignment

We've seen in the low-carbon strategy framework how investors can conduct a portfolio decarbonization with a static approach. On the other side, net zero investing involves portfolio alignment with a decarbonization pathway, rather than a simple static decarbonization. It involves a dynamic strategy in order to comply with the given net zero scenario.

The dynamic problem is trickier since it involves rebalancing decisions and depends on the future behavior of corporate issuers. 

In this part, we are going to compare the approach for performing a portfolio alignment with the Paris-Aligned Benchmarks (PAB) and the NZE frameworks. The main difference between both approaches is that portfolio alignment is conducted at the portfolio level in the PABs, while portfolio alignment is checked at the stock level in the NZE approach.

### Sequential Decarbonization at Portfolio Level

Let's first address the PAB approach of sequential portfolio decarbonization. 

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

In this problem, finding $x^*(t)$ at time $t$ requires to know the covariance matrix $\Sigma(t)$, the carbon intensities $CI(t)$ and the investable universe $b(t)$. However, in the current year $t_1$ the observations are only available for $t_0$ and $t_1$. We can however do the exercise b assuming that the world does not change. In this case, we can assume that the covariance matrix, the carbon intensities and the investable universe remain constat, such as:

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

### Sequential Decarbonization at Stock Level

In the previous section, we have performed a portfolio alignment by considering a global decarbonization path for the portfolio, as recommended by the PAB approach. In this section, we consider the decarbonization path of the issuers, as in Le Guenedal and Roncalli (2022). 
#### Net Zero Metric

Carbon emission trends.

```Python
# reproduce figure 20 for few stocks in page 38 of portfolio construction with climate risk
```

#### NZE Optimization Problem

The optimization problem is the same as the sequential optimization problem except that we explicitly introduce the NZE trajectories for the individual carbon intensity trajectories.

```Python
# Reproduce Table 11 in page 40 of Portfolio Construction with Carbon Risk
```
