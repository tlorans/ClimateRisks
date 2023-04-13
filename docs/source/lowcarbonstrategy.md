## Low-Carbon Strategy

As a first climate risks hedging strategy, we propose to follow Andersson et al. (2016) {cite:p}`andersson2016hedging` and Roncalli (2023), with a simple low-carbon index strategy.

The strategy consists in (i) reducing the weighted-average carbon intensity (WACI of the portoflio) while (ii) minimizing the tracking error relative to a benchmark.

The underlying assuption is that carbon risk is unpriced by the market. The financial aspect of carbon risk is then a risk of abrupt pricing by the market, once the markets participants integrate it. By reducing the portfolio's WACI, Andersson et al. (2016) suppose that the portfolio's carbon risk (here, the repricing risk associated with an abrupt carbon tax or carbon policy implementation) will be reduced. 

This carbon risk-hedging strategy is widely followed by index providers and asset managers, and can be defined as a low-carbon strategy.

In what follow, we will test two alternatives formulations for the climate objective: 
- the threshold approach, which consists in reducing the portfolio's WACI by changing the weights of stocks;
- the order-statistic approach, which consists in excluding the $m$ most emitting stocks.

### Threshold Approach

With the threshold approach, the objective is to minimize the tracking error with the benchmark while imposing a reduction $\mathfrak{R}$ in terms of carbon intensity. In practice, implementing such approach involves the weighted-average carbon intensity (WACI) computation and the introduction of a new constraint in a portfolio optimization problem with the presence of a benchmark (Roncalli, 2023).

#### Weighted-Average Carbon Intensity

The weighted-average carbon intensity (WACI) of the benchmark is:

\begin{equation}
CI(b) = b^T CI
\end{equation}

With $CI = (CI_1, ..., CI_n)$ the vector of carbon intensities.

The same is for the WACI of the portfolio:

\begin{equation}
CI(x) = x^T CI
\end{equation}

Let's implement a `CarbonPortfolio` dataclass that is a child of the `Portfolio` class. This new class inherits from the `Portfolio` methods and data elements, adding a vector of carbon intensities and the `get_waci` method:
```Python
from dataclasses import dataclass

@dataclass 
class CarbonPortfolio(Portfolio):
  """
  A class that implement supplementary information CI and new method get_waci,
  to be used in the low-carbon strategy implementation.
  """
  CI: np.array # Carbon Intensities

  def get_waci(self) -> float:
    return self.x.T @ self.CI
```

#### Integrating Carbon Intensity Reduction as a Constraint

The low-carbon strategy involves the reduction $\mathfrak{R}$ of the portfolio's carbon intensity $CI(x)$ compared to the benchmark's carbon intensity $CI(b)$. It can be viewed as the following constraint:

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
& Q = \Sigma \\
& R = \Sigma b \\
& A = 1^T_n \\
& B = 1 \\
& C = CI^T \\
& D = CI^{+} = (1 - ℜ)CI(b) \\
& x^- = 0_n \\
& x^+ = 1_n
\end{aligned}
\end{equation*}

```Python
@dataclass
class LowCarbonStrategy(PortfolioConstruction):
  b: np.array # Benchmark Weights
  CI:np.array # Carbon Intensity

  def threshold_approach():
    pass

  def get_portfolio(self) -> CarbonPortfolio:
    pass
```

Because we impose a constraint and minimize the TE risk, the resulting portfolio will have fewer stocks than the initial benchmark $b$. This imply that the portfolio $x$ is less diversified than the initial benchmark $b$. In order to explicitly control the number of removed stocks, Andersson et al. (2016) and Roncalli (2023) propose another methodology: the order-statistic approach.
### Order-Statistic Approach

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

#### Optimal Weights with TE Minimization

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

#### Naive Re-weighting

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

### Key Takeaways

We've covered the most frequent carbon risk-hedging strategy with the low-carbon strategy approach. It relies on minimizing the tracking error volatiltiy relative to a CW benchmark while diminishing the exposure to carbon risk, measured with the carbon intensity. This is a fundamental-based approach (carbon intensity is the fundamental data of the carbon risk).

We've seen that the max-threshold approach dominates the order-statistic with TE minimization and the order-statistic with naïve reweighting in terms of decarbonization and tracking error volatility trade-off.

The main assumption of the low-carbon strategy is the absence of carbon risk pricing. We will relax this assumption in the next part.
