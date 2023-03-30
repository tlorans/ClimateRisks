# Dealing with Risk(s) in Portfolio Construction

Before discussing the implementation of these strategies, we need to make a quick overview of some fundamentals frameworks:
- Portfolio optimization, relying on the modern portfolio theory
- Factor investing, relying on the arbitrage pricing theory

These tools will be at the basis of the three strategies we will present thereafter in this course:
- Low-Carbon Strategy (Portfolio Optimization)
- Minimum Variance with Carbon Beta (Portfolio Optimization and Factor Investing)
- Green Factor (Factor Investing)

We will discuss these basic tools with implementation in Python.

Along this course, we'll see how climate risks can be considered with these different approaches.

## Portfolio's Risk and Returns

Before introducing climate risks in the portfolio construction process, a first step is to consider how to measure portfolio's risk and returns. In practice, investors build a portfolio in a context of a benchmark (the S&P 500 for example). We'll build on the previous definition of the portfolio's risk and returns to show that risk and returns measures in a context of a benchmark is just a slight variation. This is also a good introduction to the low-carbon strategy that we will cover in the next part.

### Simple Portfolio's Two Moments

As the name of the mean-variance framework indicates, the mean (expected returns) and the variance are the two moments needed for building an efficient portfolio (efficient in the sense of the risk-rewards trade-off). 

Let's consider a universe of $n$ assets. We have a vector of assets' weights in the portfolio: $x = (x_1, ..., x_n)$.

The portfolio is fully invested:

\begin{equation}
\sum^n_{i=1}x_i = 1^T_n x = 1
\end{equation}

We have a vector of assets' returns $R = (R_1, ..., R_n)$. 


The return of the portfolio is equal to:

\begin{equation}
R(x) = \sum^n_{i=1}x_iR_i = x^T R
\end{equation}

The expected return of the portfolio is:
\begin{equation}
\mu(x) = \mathbb{E}[R(x)] = \mathbb{E}[x^TR] = x^T \mathbb{E}[R] = x^T \mu
\end{equation}

The expected return of the portfolio is then simply the weighted average of the assets' returns in the portfolio (weighted by their relative weight).

```Python
import numpy as np

x = np.array([0.25, 0.25, 0.25, 0.25])
mu = np.array([0.05, 0.06, 0.08, 0.06])
```
```Python
mu_portfolio = x.T @ mu
print(mu_portfolio)
```

```
0.0625
```

The thing is slightly more complicated with the portfolio's variance. Indeed, you need to take into account the covariance matrix between the assets in the portfolio in order to obtain a proper measure of the variance of the portfolio:

\begin{equation}
\sigma^2(x) = \mathbb{E}[(R(x) - \mu(x))(R(x) - \mu(x))^T]
\end{equation}

\begin{equation}
= \mathbb{E}[(x^TR - x^T\mu) (x^TR - x^T\mu)^T]
\end{equation}

\begin{equation}
= \mathbb{E}[x^T(R-\mu)(R - \mu)^T x]
\end{equation}

\begin{equation}
x^T \mathbb{E}[(R-\mu)(R-\mu)^T]x
\end{equation}

\begin{equation}
= x^T \Sigma x
\end{equation}

In practice, we use the historical average for estimating $\mu$. For the covariance matrix, we can compute it with historical observations with the historical volatilities and correlation matrix, such as:

\begin{equation}
\Sigma = diag(\sigma) \cdot \rho \cdot  diag(\sigma)
\end{equation}

with $\sigma$ are the volatilities of returns and $\rho$ the correlation matrix.

```Python
sigma = np.array([0.15, 0.20, 0.25, 0.30])
rho = np.array([[1., 0.1, 0.4, 0.5],
               [0.1, 1, 0.7 , 0.4 ],
               [0.4, 0.7, 1., 0.8],
               [0.5, 0.4, 0.8, 1]])

Sigma = np.diag(sigma) @ rho @ np.diag(sigma)               
```

```Python
variance_portfolio = x.T @ Sigma @ x
print(variance_portfolio)
```

```
0.033375
```

Rather than writing again and again the same formula, let's create a simple dataclass with the data we need for computing the portfolio's two moments and the corresponding methods:
```Python
from dataclasses import dataclass 

@dataclass 
class Portfolio:
  """A simple dataclass storing the basics information of a porfolio and 
  implementing the methods for the two moments computation.
  """
  x: np.array # Weights
  mu: np.array # Expected Returns
  Sigma: np.matrix # Covariance Matrix

  def get_expected_returns(self) -> float:
    return self.x.T @ self.mu

  def get_variance(self) -> float:
    return self.x.T @ self.Sigma @ self.x

```

```Python
simple_portfolio = Portfolio(x = x,
                 mu = mu,
                 Sigma = Sigma)
```
```Python
simple_portfolio.get_expected_returns()
```
```Python
simple_portfolio.get_variance()
```

### Risk and Returns in the Presence of a Benchmark: Tracking Error and Excess Expected Returns

With the rise of passive investing is the rise of index replication. The purpose of index replication is to build a hedging strategy by investing in stocks. In this case of index replication, the portfolio's expected returns is replaced by the expected excess returns of the strategy, while the variance of the portfolio is replaced by the volatility of the tracking error (the difference between the return of the strategy and the return of the index). You may distinguish different cases of index replications:
- Low tracking error volatility (less than 10bps) corresponds to physical or synthetic replication;
- Moderate tracking error volatility (between 10 bps and 50 bps) corresponds to sampling (ie. less assets) replication;
- Higher tracking error volatility (larger than 50 bps) corresponds to enhanced/tilted index, such as the low-carbon strategy or ESG-enhanced indexes.

#### Tracking Error

In order to monitor the quality of the hedging strategy, investors use the tracking error (TE) measure. In this part, we will define the TE and TE volatility concepts that needs to be controlled in the portfolio optimization problem in the presence of a benchmark (Roncalli, 2013 {cite:p}`roncalli2013introduction`).

Let's define $b = (b_1, ..., b_n)$ and $x = (x_1, ..., x_n)$ the stocks weights in the benchmark and the portfolio. 

The tracking error between a portfolio $x$ and its benchmark $b$ is the difference between the return of the portfolio and the return of the benchmark:

\begin{equation}
e = R(x) - R(b) = (x - b)^{T}R
\end{equation}

The volatility of the tracking error is:

\begin{equation}
\sigma(x|b) = \sigma(e) = \sqrt{(x-b)^T \Sigma (x-b)}
\end{equation}

With $\Sigma$ the covariance matrix.

Let's implement it in Python:
```Python
def get_tracking_error_volatility(x:np.array, 
                                  b:np.array,
                                  Sigma:np.array) -> float:
  return np.sqrt((x - b).T @ Sigma @ (x - b))
```

#### Expected Excess Return

The expected excess return is:

\begin{equation}
\mu(x|b) = E[e] = (x - b)^T\mu 
\end{equation}

Where $\mu$ is the vector of expected returns $(\mu_1,...,\mu_n)$.

```Python
def get_excess_expected_returns(x:np.array, 
                                b:np.array,
                                mu:np.array) -> float:
  return (x - b).T @ mu
```

## Portfolio Construction with Optimization: Managing the Risk & Returns Trade-Off Efficiently

Let's go now on the first approach for managing risk in portfolio construction, with the optimization approach in the mean-variance framework. We'll first address the simple mean-variance portfolio, then tackle the case with portfolio construction in the context of a benchmark. We'll see that the last case is just a slight variation from the simple mean-variance portfolio.

### Simple Mean-Variance Portfolio

In the Markowitz framework, the mean-variance investor considers maximizing the expected return of the portfolio under a volatility constraint:

\begin{equation*}
\begin{aligned}
& x^* = 
& & argmax & \mu(x) \\
& \text{subject to}
& & 1_n^Tx = 1, \\
&&& \sigma(x) \leq \sigma^*
\end{aligned}
\end{equation*}

Or, equivalently, minimizing the volatility of the portfolio under a return constraint:

\begin{equation*}
\begin{aligned}
& x^* = 
& & argmin & \sigma(x) \\
& \text{subject to}
& & 1_n^Tx = 1, \\
&&& \mu* \leq \mu(x)
\end{aligned}
\end{equation*}

This is the optimization problem of finding the most efficient risk-returns couple mentioned previously, with the portfolio's two moments.

For ease of computation, Markowitz transformed the two original non-linear optimization problems into a quadratic optimization problem. Introducing a risk-tolerance parameter ($\gamma$-problem) and the long-only constraint, we obtain the following quadratic problem:

\begin{equation*}
\begin{aligned}
& x^* = 
& & argmin & \frac{1}{2} x^T \Sigma x - \gamma x ^T \mu\\
& \text{subject to}
& & 1_n^Tx = 1 \\
& & & 0_n \leq x \leq 1_n
\end{aligned}
\end{equation*}

Solvers consider the following QP formulation:

\begin{equation*}
\begin{aligned}
& x^* = 
& & argmin & \frac{1}{2} x^T Q x - x^T R \\
& \text{subject to}
& & Ax = B, \\
&&& Cx \leq D,\\
& & & x^- \leq x \leq x^+
\end{aligned}
\end{equation*}

We need to find the parameters $\{Q, R, A, B, C, D, x^-, x^+\}$. In the previous case, $Q = \Sigma$, $R = \gamma \mu$, $A = 1_n^T$, $B = 1$, $x^- = 0_n$ and $x^+ = 1_n$.

We begin the implementation in Python by defining a `PortfolioConstruction` dataclass, with `mu` and `Sigma` as the two elements requested and an abstract method `get_portfolio` without any specific definition:
```Python
from abc import ABC, abstractmethod

@dataclass 
class PortfolioConstruction(ABC):
  """The parent class of portfolio construction approaches"""
    mu: np.array # Expected Returns
    Sigma: np.matrix # Covariance Matrix

    @abstractmethod
    def get_portfolio(self) -> Portfolio:
      pass
```
Some would say that such a definition of a portfolio construction overarching class wasn't needed. They are right. The only purpose here is to highlight the fact that every approaches that we will cover are different ways to build a portfolio. All the children classes will be related, because they all are frameworks for building a portfolio. Noteworthy, all children classes will inherit the `mu` and `Sigma` elements needed for instantiating an object inheriting from this class.

Let's then define a child for this class with the `PortfolioOptimization` dataclass:
```Python
@dataclass 
class PortfolioOptimization(PortfolioConstruction):
"""Portfolio Construction with Optimization approaches"""

    @abstractmethod
    def get_portfolio(self) -> Portfolio:
      pass

```
Here we are. We have defined our first family of portfolio construction with the portfolio optimization.

To go further, we first need to install the package `qpsolvers`:
```Python
!pip install qpsolvers 
```
We can now define a concrete dataclass with the `MeanVariance` class. This class will inherits from the `PortfolioConstruction` and `PortfolioOptimization` classes the two required elements `mu` and `Sigma`. We also define the first concrete implementation of the method `get_portfolio`, requiring a `gamma` parameter to be provided:
```Python
from qpsolvers import solve_qp

@dataclass
class MeanVariance(PortfolioOptimization):
  
  def get_portfolio(self, gamma:int) -> Portfolio:
    """QP Formulation"""
    Q = self.Sigma
    R = gamma * self.mu
    A = np.ones(len(self.mu)).T # fully invested
    B = np.array([1.]) # fully invested
    x_inf = np.zeros(len(self.mu)) # long-only position
    x_sup = np.ones(len(self.mu)) # long-only position

    x_optim = solve_qp(P = Q,
              q = -R, # we put a minus here because this QP solver consider +x^T R
              A = A, 
              b = B,
              lb = x_inf,
              ub = x_sup,
              solver = 'osqp')

    return Portfolio(x = x_optim, mu = self.mu, Sigma = self.Sigma)
```
This new class will return a `Portfolio` object if we call the `get_portfolio` method with an instantiated object. Let's find several optimum portfolios with various value of $\gamma$, and plot the result:
```Python
test = MeanVariance(mu = mu, Sigma = Sigma)
```

```Python
from numpy import arange

list_gammas = arange(-1,1.2, 0.01)
list_portfolios = []


for gamma in list_gammas:
  list_portfolios.append(test.get_portfolio(gamma = gamma))
```

```Python
import matplotlib.pyplot as plt

returns = [portfolio.get_expected_returns() * 100 for portfolio in list_portfolios]
variances = [portfolio.get_variance() * 100 for portfolio in list_portfolios]

plt.figure(figsize = (10, 10))
plt.plot(variances, returns)
plt.xlabel("Volatility (in %)")
plt.ylabel("Expected Return (in %)")
plt.title("Efficient Frontier")
plt.show()
```
This is the well-known efficient frontier. Every portfolios on the efficient frontier (that is, the upper side of this curve) are efficient in the Markowitz framework, depending on the risk-tolerance of the investor.

### Portfolio Optimization in the Presence of a Benchmark

In practice, many problems consist in tracking a benchmark while improving some properties (reducing the carbon portfolio for example). 

To construct such a portfolio tracking a benchmark, the main tool is to control the tracking error, that is the difference between the benchmark's return and the portfolio's return.

In the presence of a benchmark, the expected return of the portfolio $\mu(x)$ is replaced by the expected excess return $\mu(x|b)$. The volatility of the portfolio $\sigma(x)$is replaced by the volatility of the tracking error $\sigma(x|b)$:

\begin{equation*}
\begin{aligned}
& x^* = 
& & argmin & \frac{1}{2} \sigma^2 (x|b) - \gamma \mu(x|b)\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & & 0_n \leq x \leq 1_n
\end{aligned}
\end{equation*}

Without any further constraint, the optimal solution $x^*$ will be equal to the benchmark weights $b$. This is the case aiming to perfect replication strategy. An enhanced or tilted version will add further constraints, depending on the objective of the strategy (decarbonization for example).

We have a few more steps to consider before finding our QP formulation parameters.

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

We have exactly the same QP problem than with the initial long-only mean-variance portfolio, except that $R = \gamma \mu + \Sigma b$

Let's implement a new dataclass `IndexReplication`:
```Python
@dataclass
class IndexReplication(PortfolioOptimization):
  b: np.array # Benchmark Weights

  def get_portfolio(self, gamma:int) -> Portfolio:
    """QP Formulation"""
    Q = self.Sigma
    R = gamma * self.mu + Sigma @ self.b
    A = np.ones(len(self.mu)).T # fully invested
    B = np.array([1.]) # fully invested
    x_inf = np.zeros(len(self.mu)) # long-only position
    x_sup = np.ones(len(self.mu)) # long-only position

    x_optim = solve_qp(P = Q,
              q = -R, # we put a minus here because this QP solver consider +x^T R
              A = A, 
              b = B,
              lb = x_inf,
              ub = x_sup,
              solver = 'osqp')

    return Portfolio(x = x_optim, mu = self.mu, Sigma = self.Sigma)
```
Once instantiated, an object of class `IndexReplication` will return a `Portfolio` object with the method `get_portfolio`. Because we don't have any further constraint here, this is a pure index replication strategy, and it will return a portfolio with the same weights than the benchmark.

## From CAPM to Risk Factors Models: Capturing New Risk Premia with Factor Investing

Introducing the notion of climate risks into Finance can be also made through the lens of systematic risks exposure. Risks can be decomposed into a systematic (common for all stocks) and an idiosyncratic ($\alpha$, specific to a stock) components. Theoretically, because idiosyncratic risk can be eliminated with diversification, $\alpha = 0$ and only the exposure to systematic risk should be rewarded by the markets. Factor investing treats the question of managing the exposure to systematic risks factors. 

The capital asset pricing model (CAPM), introduced by Sharpe in 1964, is an equilibrium model based on the Markowitz framework. Before Sharpe, and in the absence of an equilibrium model, expected excess return of an asset $i$ was only explained by the idiosyncratic component:

\begin{equation}
E[R_i] - R_f = \alpha_i
\end{equation}

Where $R_i$ is the asset returns, $R_f$ the risk-free rate and $\alpha_i$ the idiosyncratic risk premia of the asset $i$.
In the CAPM framework, the expected excess return of an asset $i$ can be defined by the sensitivity of the stock to the market portfolio $\beta_i$ times the market portfolio's return:

\begin{equation}
\mathbb{E}[R_i] - R_f = \beta^m_i(\mathbb{E}[R_m] - R_f)
\end{equation}

Where $R_m$ are market returns and the coefficient $\beta^m_i$ is the beta of the asset $i$ with respect to the market portfolio. In that framework, the excess return of an asset $i$ is then explained by its exposure to the systematic market risk.

However, empirical evidences accumulated to prove the existence of a remaining idiosyncratic $\alpha$ component, that is a part of the cross-section of expected returns unexplained by the exposure to market risk:

\begin{equation}
\mathbb{E}[R_i] - R_f = \alpha_i + \beta^m_i(\mathbb{E}[R_m] - R_f)
\end{equation}

A revolution with risk factors took place with Fama and French (1992), adding two supplementary systematic risk factors to the initial Market Risk (SMB and HML):

\begin{equation}
\mathbb{E}[R_i] - R_f = \beta^m_i(\mathbb{E}[R_m] - R_f) + \beta^{SMB}_i \mathbb{E}[R_{SMB}] + \beta^{HML}_i \mathbb{E}[R_{HML}]
\end{equation}

Then $\alpha$ reappeared:

\begin{equation}
\mathbb{E}[R_i] - R_f = \alpha_i + \beta^m_i(\mathbb{E}[R_m] - R_f) + \beta^{SMB}_i \mathbb{E}[R_{SMB}] + \beta^{HML}_i \mathbb{E}[R_{HML}]
\end{equation}

Carhart complemented the Fama-French 3-factors model with the WML risk factor (1997):
\begin{equation}
\mathbb{E}[R_i] - R_f = \beta^m_i(\mathbb{E}[R_m] - R_f) + \beta^{smb}_i \mathbb{E}[R_{smb}] + \beta_i^{hml}{E}[R_{hml}] + \beta_i^{wml}{E}[R_{wml}]
\end{equation}

And $\alpha$ reappeared again...
\begin{equation}
\mathbb{E}[R_i] - R_f = \alpha_i + \beta^m_i(\mathbb{E}[R_m] - R_f) + \beta^{smb}_i \mathbb{E}[R_{smb}] + \beta_i^{hml}{E}[R_{hml}] + \beta_i^{wml}{E}[R_{wml}]
\end{equation}

```Python
# to be done: download the FF factors and estimate betas for a handful of stocks
```
## Risk Factor Portfolio

As investors are compensated for taking systematic risk(s), they can look for gaining exposure to these risks with a Risk Factor Portfolio. We'll see how long/short risk factor portfolio can be built.

In the CAPM framework, there is a single market risk premium, which can be otained by investing in market-capitalization indexes. 

```Python
@dataclass
class MarketCapIndex(PortfolioConstruction):
  mv: np.array # Market Cap

  def get_portfolio(self) -> Portfolio:
    x = self.mv / np.sum(self.mv)
    return Portfolio(x = x, mu = self.mu, Sigma = self.Sigma)

```
But critics against market-cap indexation arised with empirical evidences against the efficiency of market-cap investing: as we've seen in the previous part, theory and empirical evidences introduced other systematic factors models to capture new risk premia. To generate excess returns in the long-run, investors can adopt factor investing by adding these risk factors to the existing market risk one, and invest in the corresponding factor portfolio.

We can illustrate the construction of a long/short portfolio with the quintile approach:
- We define a score $S_i(t_{\tau})$ for each stock $i$ at each rebalancing date $t_{\tau}$
- We specify a weighting scheme $w_i(t_{\tau})$ (value-weighted or equally-weighted).
- Stocks with the 20\% highest scores are assigned a positive weight according to the weighting sheme ($Q1(t_{\tau})$ portfolio or the long portfolio)
- Stocks with the 20% lowest scores are assigned a negative weight according to the weighting scheme ($Q5(t_{\tau})$ portfolio, or the short portfolio)


```Python
# We define a new way to build a portfolio: the Long-Short Portfolio Construction

@dataclass 
class LongShortConstruction(PortfolioConstruction):
    S: np.array # Score

    @abstractmethod
    def get_portfolio(self) -> Portfolio:
      pass

@dataclass
class QuintileConstruction(LongShortConstruction):

  def get_portfolio(self) -> Portfolio:
    # find the borns to define Q1 and Q5
    born_Q1 = np.quantile(self.S, 0.8)
    born_Q5 = np.quantile(self.S, 0.2)

    # define the long and short stocks
    long_stocks = self.S[np.where(self.S > born_Q1)]
    short_stocks = self.S[np.where(self.S < born_Q5)]

    # define the vector of weights (equally-weighted here)
    x = np.zeros(len(self.S))
    x[np.where(self.S > born_Q1)] = 1 / len(long_stocks)
    x[np.where(self.S < born_Q5)] = - 1 / len(short_stocks)
    
    return Portfolio(x = x, mu = self.mu, Sigma = self.Sigma)
    
```

```Python
S = np.array([1.1, 
     0.5,
     -1.3,
     1.5,
     -2.8,
     0.3,
     0.1,
     2.3,
     -0.7,
     -0.3])
```