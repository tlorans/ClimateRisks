
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
With the threshold approach, the objective is to minimize the tracking error with the benchmark while imposing a reduction $\mathfrak{R}$ in terms of carbon intensity. 

In practice, implementing such approach involves the weighted-average carbon intensity (WACI) computation and the introduction of a new constraint in a portfolio optimization problem with the presence of a benchmark (Roncalli, 2013). In this part, we first define the WACI, and then introduce the threshold approach as an additional constraint to the portfolio optimization with a benchmark problem seen in the previous part.

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


