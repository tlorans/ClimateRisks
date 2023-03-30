# Low-Carbon Strategy

As a first climate risks hedging strategy, we propose to follow Andersson et al. (2016) and Roncalli et al. (2021), with a simple **low-carbon index strategy**.

The underlying main assuption is that climate risks is unpriced by the market. The financial aspect of climate risks is then a risk of abrupt pricing by the market, once the markets participants integrate it. 

In that context, Andersson et al. (2016) propose a climate risk-hedging strategy by:
1. Reducing the weighted-average carbon intensity (WACI) of the portfolio
2. Minimizing the tracking error relative to a capitalization-weighted benchmark

By reducing the portfolio's WACI, Andersson et al. (2016) suppose that the portfolio's carbon risk (here, the repricing risk associated with an abrupt carbon tax or carbon policy implementation) will be reduced. 

This climate risks strategy is widely followed by index providers and asset managers, and can be defined as a low-carbon strategy.

In what follow, we will implement a simple low-carbon strategy, following Andersson et al. (2016) and Roncalli et al. (2021). We will test two alternatives approach for the climate objective: 
- the threshold approach, which consists in reducing the portfolio's WACI by changing the weights of stocks;
- the order-statistic approach, which consists in excluding the $m$ most emitting stocks.

In order to implement this low-carbon strategy, we follow Roncalli (2013) formulation of the problem as a portfolio optimization in the presence of a benchmark. We have seen in the previous part how the TE component helps in tracking the benchmark. In this part, we will address the carbon risk exposure reduction, as exposed by Andersson et al. (2016) and Roncalli et al. (2021). 

More precisely, we will integrate the carbon risk exposure reduction into the portfolio optimization in the presence of a benchmark problem. This is equivalent to adding a new constraint to our initial optimization problem.

## Threshold Approach

With the threshold approach, the objective is to minimize the tracking error with the benchmark while imposing a reduction $\Re$ in terms of carbon intensity.

The weighted-average carbon intensity (WACI) of the benchmark is:

\begin{equation}
CI(b) = b^T CI
\end{equation}

With $CI = (CI_1, ..., CI_n)$ the vector of carbon intensities.

The same is for the WACI of the portfolio:

\begin{equation}
CI(x) = x^T CI
\end{equation}

```Python
from dataclasses import dataclass

@dataclass 
class CarbonPortfolio(Portfolio):
  """xx
  """
  CI: np.array # Carbon Intensities

  def get_waci(self) -> float:
    pass
```

The optimization problem becomes:


\begin{equation*}
\begin{aligned}
& x(ℜ) = 
& & argmin \frac{1}{2}(x-b)^T \Sigma (x - b)\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & & x \geq 0_n \\
&&&  CI^T x \leq (1 - ℜ) CI(b)
\end{aligned}
\end{equation*}

And the QP formulation is:


\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2}x^T \Sigma x - x^T \Sigma b\\
& \text{subject to}
& & 1_n^Tx = 1\\
&&&  CI^T x \leq (1 - ℜ) (b^T CI) \\
&&& 0_n \leq x \leq 1
\end{aligned}
\end{equation*}

with the following QP parameters:

\begin{equation*}
\begin{aligned}
& Q = \Sigma \\
& R = \Sigma b \\
& A = 1^T_n \\
& B = 1 \\
& C = CI^T \\
& D = CI^{+} = (1 - ℜ) (b^T CI) \\
& x^- = 0_n \\
& x^+ = 1_n
\end{aligned}
\end{equation*}

```Python
# implement the first method: threshold appraoch

@dataclass
class LowCarbonStrategy(PortfolioConstruction):
  b: np.array # Benchmark Weights
  CI:np.array # Carbon Intensity

  def threshold_approach():
    pass

  def get_portfolio(self) -> CarbonPortfolio:
    pass
```
## Order-Statistic Approach

Andersson et al. (2016) and Roncalli et al. (2021) propose a second approach by eliminating the $m$ worst performing issuers in terms of carbon intensity.

We note $CI_{i:n}$ the order statistics of $[CI_1, ..., CI_n]$:

\begin{equation}
minCI_i = CI_{1:n} \leq ... \leq CI_{n:n} = max CI_i
\end{equation}

The carbon intensity bound $CI^{m,n}$ is defined as:

\begin{equation}
CI^{m,n} = CI_{n-m+1:n}
\end{equation}

Where $CI_{n-m+1:n}$ is the $(n-m+1)$-th order statistic of $[CI_1, ..., CI_n]$

Eliminating the $m$ worst performing assets is then equivalent to imposing the following constraint:

\begin{equation}
CI_i \geq CI^{m,n} → x_i = 0
\end{equation}

To implement this decarbonization strategy, the resulting weightings can be determined by:
- finding the optimal weightings that minimize the TE volatility
- reweighting the remaining stocks with a naïve approach

### Optimal Weights with TE Minimization

We can introduce the order-statistic approach into our optimization problem with the new constraint. 

The optimization problem becomes:

\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2}x^T \Sigma x - x^T \Sigma b\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & & 0_n \leq x \leq x^+
\end{aligned}
\end{equation*}

Where $x_i^+ = 𝟙\{CI_i < CI^{m,n}\}$

Which is again a QP Problem.

Thus we have the following QP problem:

\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2}x^T \Sigma x - x^T \Sigma b\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & & 0_n \leq x \leq x^+ \\
& & & x+ =  𝟙\{CI_i < CI^{m,n}\}
\end{aligned}
\end{equation*}

And the following QP parameters:

\begin{equation*}
\begin{aligned}
& Q = \Sigma \\
& R = \Sigma b \\
& A = 1^T_n \\
& B = 1 \\
& x^- = 0_n \\
& x^+ = 𝟙\{CI_i < CI^{m,n}\}
\end{aligned}
\end{equation*}

```Python
# implement the second method: order-statistic approach

@dataclass
class LowCarbonStrategy(PortfolioConstruction):
  b: np.array # Benchmark Weights
  CI:np.array # Carbon Intensity
  
  def threshold_approach():
    pass

  def order_statistic_approach():
      if reweighting = "te_minimization"
    pass 

  def get_portfolio(self) -> CarbonPortfolio:
    pass
```

### Naive Re-weighting

A "naive" solution consists in re-weighting the remaining stocks:

\begin{equation}
x_i = \frac{𝟙\{CI_i < CI^{m,n}\}b_i}{\sum^n_{k=1} 𝟙\{CI_k < CI^{m,n}\}b_k}
\end{equation}

```Python
# implement the second method: order-statistic approach

@dataclass
class LowCarbonStrategy(PortfolioConstruction):
  b: np.array # Benchmark Weights
  CI:np.array # Carbon Intensity
  
  def threshold_approach():
    pass

  def order_statistic_approach():
      if reweighting = "te_minimization":
        pass
      elif reweighting = "naive":
        pass

    pass 

  def get_portfolio(self) -> CarbonPortfolio:
    pass
```

## Conclusion

We've covered the most frequent climate risks hedging strategy with the low-carbon strategy approach. It relies on minimizing the tracking error relative to a CW benchmark while diminishing the exposure to carbon risk, measured with the carbon intensity.

We've seen that the max-threshold approach dominates the order-statistic with TE minimization and the order-statistic with naïve reweighting in terms of decarbonization and tracking error volatility trade-off.

The main assumption of the low-carbon strategy is the absence of carbon risk pricing. We will relax this assumption in the next part.
