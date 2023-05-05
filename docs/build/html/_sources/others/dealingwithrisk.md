## Dealing with Risk(s) in Portfolio Construction

Before discussing the implementation of these strategies, we need to make a quick overview of some fundamentals frameworks:
- Portfolio optimization
- Factor modelling

These tools will be at the basis of the three parts we will present thereafter in this course:
- Low-Carbon Strategy (Portfolio Optimization)
- Enhanced Index with Carbon Beta (Portfolio Optimization and Factor Modelling)
- Green Stocks Outperformance (Factor Modelling)

We will discuss these basic tools with implementation in Python. In this course, we'll see how climate risks can be considered with these different approaches.

We relies on notations and frameworks from Roncalli (2013) {cite:p}`roncalli2013introduction`. 

### Portfolio's Risk and Returns

Before introducing climate risks in the portfolio construction process, a first step is to consider how to measure portfolio's risk and returns. In practice, investors build a portfolio in a context of a benchmark (the S&P 500 for example). We'll build on the definition of the portfolio's risk and returns to show that risk and returns measures in a context of a benchmark is just a slight variation. This is also a good introduction to the low-carbon strategy that we will cover in the next part.

#### Simple Portfolio's Two Moments

Our first tool, portfolio optimization, relies on the mean-variance framework. As the name of the mean-variance framework indicates, the mean (expected returns) and the variance are the two moments needed for building an efficient portfolio (efficient in the sense of the risk-rewards trade-off). 

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

A simple approach is to use the historical average for estimating $\mu$. For the covariance matrix, we can compute it with the historical volatilities and correlation matrix, such as:

\begin{equation}
\Sigma = diag(\sigma) \cdot \rho \cdot  diag(\sigma)
\end{equation}

with $\sigma$ are the volatilities of returns and $\rho$ the correlation matrix. We will see in the first project that computing the covariance matrix with the sample covariance matrix leads to significant lack of robustness in the portfolio construction.

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
```
0.0625
```
```Python
simple_portfolio.get_variance()
```
```
0.033375
```

#### Risk and Returns in the Presence of a Benchmark: Tracking Error and Excess Expected Returns

With the rise of passive investing is the rise of index replication. In the case of index replication, the portfolio's expected returns is replaced by the expected excess returns of the strategy, while the variance of the portfolio is replaced by the volatility of the tracking error (the difference between the return of the strategy and the return of the index). You may distinguish different cases of index replications (Roncalli, 2023):
- Low tracking error volatility (less than 10bps) corresponds to physical or synthetic replication;
- Moderate tracking error volatility (between 10 bps and 50 bps) corresponds to sampling (ie. less assets) replication;
- Higher tracking error volatility (larger than 50 bps) corresponds to enhanced/tilted index, such as the low-carbon strategy or ESG-enhanced indexes.

##### Tracking Error

In order to monitor the quality of the replication strategy, investors use the tracking error (TE) measure. In this part, we will define the TE and TE volatility concepts that needs to be controlled in the portfolio optimization problem in the presence of a benchmark (Roncalli, 2013).

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

##### Expected Excess Return

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

### Portfolio Construction with Optimization: Managing the Risk & Returns Trade-Off Efficiently

Now, let's see our first tool for managing risk in portfolio construction, with the optimization approach in the mean-variance framework. We'll first address the simple mean-variance portfolio, then tackle the case with portfolio construction in the context of a benchmark. We'll see that the last case is just a slight variation from the simple mean-variance portfolio.

#### Simple Mean-Variance Portfolio

In the Markowitz framework, the mean-variance investor considers maximizing the expected return of the portfolio under a volatility constraint (Roncalli, 2023):

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

For ease of computation, Markowitz transformed the two original non-linear optimization problems into a quadratic optimization problem. 
Introducing a risk-tolerance parameter ($\gamma$-problem, Roncalli 2013) and the long-only constraint, we obtain the following quadratic problem:

\begin{equation*}
\begin{aligned}
& x^* = 
& & argmin \frac{1}{2} x^T \Sigma x - \gamma x ^T \mu\\
& \text{subject to}
& & 1_n^Tx = 1 \\
& & & 0_n \leq x \leq 1_n
\end{aligned}
\end{equation*}

To solve this problem with Python, we will use the `qpsolvers` library. This library considers the following QP formulation:


\begin{equation*}
\begin{aligned}
& x^* = 
& & argmin \frac{1}{2} x^T P x + q^T x \\
& \text{subject to}
& & Ax = b, \\
&&& Gx \leq h,\\
& & & lb \leq x \leq ub
\end{aligned}
\end{equation*}

We need to find $\{P, q, A, b, G, h, lb, ub\}$. In the previous case, $P = \Sigma$, $q = \gamma \mu$, $A = 1_n^T$, $b = 1$, $lb = 0_n$ and $ub = 1_n$.

To go further, we first need to install the package `qpsolvers`:
```Python
!pip install qpsolvers 
```
We can now define a concrete dataclass with the `MeanVariance` class. This class will require two elements `mu` and `Sigma`. We also define the method `get_portfolio`, requiring a `gamma` parameter to be provided:

```Python
from qpsolvers import solve_qp

@dataclass
class MeanVariance:

  mu: np.array # Expected Returns
  Sigma: np.matrix # Covariance Matrix
  
  def get_portfolio(self, gamma:int) -> Portfolio:
    """QP Formulation"""

    x_optim = solve_qp(P = self.Sigma,
              q = -(gamma * self.mu),
              A = np.ones(len(self.mu)).T, # fully invested
              b = np.array([1.]), # fully invested
              lb = np.zeros(len(self.mu)), # long-only position
              ub = np.ones(len(self.mu)), # long-only position
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
```{figure} efficient_frontier.png
---
name: efficientfrontier
---
Figure: Efficient Frontier
```

This is the well-known efficient frontier. Every portfolios on the efficient frontier (that is, the upper side of this curve) are efficient in the Markowitz framework, depending on the risk-tolerance ($\gamma$ parameter) of the investor.

#### Portfolio Optimization in the Presence of a Benchmark

In practice, many problems consist in tracking a benchmark while improving some properties (reducing the carbon portfolio for example). To construct such a portfolio tracking a benchmark, the main tool is to control the tracking error, that is the difference between the benchmark's return and the portfolio's return.

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

We have exactly the same QP problem than with the initial long-only mean-variance portfolio, except that $q = -(\gamma \mu + \Sigma b)$.

Let's implement a new dataclass `IndexReplication`:
```Python
@dataclass
class IndexReplication:
  b: np.array # Benchmark Weights

  def get_portfolio(self, gamma:int) -> Portfolio:
    """QP Formulation"""

    x_optim = solve_qp(P = self.Sigma,
              q = -(gamma * self.mu + Sigma @ self.b), 
              A = np.ones(len(self.mu)).T, # fully invested,
              b = np.array([1.]), # fully invested
              lb = np.zeros(len(self.mu)), # long-only position
              ub = np.ones(len(self.mu)), # long-only position
              solver = 'osqp')

    return Portfolio(x = x_optim, mu = self.mu, Sigma = self.Sigma)
```
Once instantiated, an object of class `IndexReplication` will return a `Portfolio` object with the method `get_portfolio`. Because we don't have any further constraint here, this is a pure index replication strategy, and it will return a portfolio with the same weights than the benchmark.

### From CAPM to Risk Factors Models: Capturing New Risk Premia with Factor Investing

Introducing the notion of climate risks into Finance can be also made through the lens of systematic risks exposure. In this part and the following part, we refer to the [specific course from Thierry Roncalli](http://www.thierry-roncalli.com/download/AM-Lecture3.pdf) for notations and main formulas. Risks can be decomposed into a systematic (common for all stocks) and an idiosyncratic (specific to a stock) components. The expected returns can then be decomposed between an $\alpha$ (rewards for idiosyncratic risk exposure) and a $\beta$ (rewards for systematic risk exposure).

Theoretically, because idiosyncratic risk can be eliminated with diversification (with the Markowitz framework), $\alpha = 0$ and only the exposure to systematic risk should be rewarded by the markets. Factor investing treats the question of managing the exposure to systematic risks factors. But what are the systematic risks factors, and how to measure the stocks' exposure to these risks?

The capital asset pricing model (CAPM), introduced by Sharpe in 1964 {cite:p}`sharpe1964capital`, is an equilibrium model based on the Markowitz framework, and is the a first step in the quest towards risk factors identification. In the CAPM framework, the expected excess return of an asset $i$ can be defined by the sensitivity of the stock to the market portfolio $\beta_i$ times the market portfolio's return:

\begin{equation}
\mathbb{E}[R_i] - R_f = \beta^m_i(\mathbb{E}[R_m] - R_f)
\end{equation}

Where $R_i$ is the asset returns, $R_m$ are market returns, the coefficient $\beta^m_i$ is the beta of the asset $i$ with respect to the market portfolio, $R_f$ the risk-free rate and $\alpha_i$ the idiosyncratic risk premia of the asset $i$. In this framework, the excess return of an asset $i$ is then explained by its exposure to the systematic market risk. Market risk is the only systematic risk in the CAPM.

However, empirical evidences accumulated to prove the existence of a remaining idiosyncratic $\alpha$ component, that is a part of the cross-section of expected returns unexplained by the exposure to market risk:

\begin{equation}
\mathbb{E}[R_i] - R_f = \alpha_i + \beta^m_i(\mathbb{E}[R_m] - R_f)
\end{equation}

Fama and French (1992 {cite:p}`fama1992cross`, 1993 {cite:p}`fama1993common`), added two supplementary systematic risk factors to the initial Market Risk:
- Small Minus Big (SMB) that corresponds to a Size factor.
- High Minus Low (HML) that corresponds to the Value factor

\begin{equation}
\mathbb{E}[R_i] - R_f = \beta^m_i(\mathbb{E}[R_m] - R_f) + \beta^{SMB}_i \mathbb{E}[R_{SMB}] + \beta^{HML}_i \mathbb{E}[R_{HML}]
\end{equation}

But then, $\alpha$ reappeared:

\begin{equation}
\mathbb{E}[R_i] - R_f = \alpha_i + \beta^m_i(\mathbb{E}[R_m] - R_f) + \beta^{SMB}_i \mathbb{E}[R_{SMB}] + \beta^{HML}_i \mathbb{E}[R_{HML}]
\end{equation}

Carhart complemented the Fama-French 3-factors model with the Winners Minus Losers (WML) or Momentum factor (1997 {cite:p}`carhart1997persistence`):
\begin{equation}
\mathbb{E}[R_i] - R_f = \beta^m_i(\mathbb{E}[R_m] - R_f) + \beta^{smb}_i \mathbb{E}[R_{smb}] + \beta_i^{hml}{E}[R_{hml}] + \beta_i^{wml}{E}[R_{wml}]
\end{equation}

$\alpha$ reappeared again...
\begin{equation}
\mathbb{E}[R_i] - R_f = \alpha_i + \beta^m_i(\mathbb{E}[R_m] - R_f) + \beta^{smb}_i \mathbb{E}[R_{smb}] + \beta_i^{hml}{E}[R_{hml}] + \beta_i^{wml}{E}[R_{wml}]
\end{equation}

Then, Fama and French (2015) {cite:p}`fama2015five` added two new factors, profitability (RMW) and investment (CMA), leading to a five factors model without the momentum (WML) factor:
\begin{equation}
\mathbb{E}[R_i] - R_f = \beta^m_i(\mathbb{E}[R_m] - R_f) + \beta^{smb}_i \mathbb{E}[R_{smb}] + \beta_i^{hml}{E}[R_{hml}]
+ \beta_i^{rmw}{E}[R_{rmw}]
+ \beta_i^{cma}{E}[R_{cma}]
\end{equation}

And many more factors were published!

Let's have a look to the risk factors from the Carhart model:
```Python
import pandas as pd
url = 'https://assets.uni-augsburg.de/media/filer_public/67/d8/67d814ce-0aa9-4156-ad25-fb2a9202769d/carima_exceltool_en.xlsx'
risk_factors = pd.read_excel(url, sheet_name = 'Risk Factors').iloc[:,4:10]
risk_factors['Month'] = pd.to_datetime(risk_factors['Month'].astype(str)).dt.strftime('%Y-%m')
risk_factors.index = risk_factors['Month']
risk_factors.plot(subplots = True, figsize = (12, 12))
```
```{figure} riskfactors.png
---
name: riskfactors
---
Figure: Carhart 4 factors
```

With these factors returns, you can then estimate the individual stocks loading into each factors, with the following linear regression:

\begin{equation}
R_i = \alpha_i + \beta^m_i(\mathbb{E}[R_m] - R_f) + \beta^{smb}_i \mathbb{E}[R_{smb}] + \beta_i^{hml}{E}[R_{hml}] + \beta_i^{wml}{E}[R_{wml}] 
\end{equation}

Let's retrieve historical returns for a handful of stocks:
```Python
url = 'https://assets.uni-augsburg.de/media/filer_public/67/d8/67d814ce-0aa9-4156-ad25-fb2a9202769d/carima_exceltool_en.xlsx'
returns = pd.read_excel(url, sheet_name = 'Asset Returns').iloc[:,4:14]
returns['Month'] = pd.to_datetime(returns['Month'].astype(str)).dt.strftime('%Y-%m')
returns.index = returns['Month']
returns.iloc[:,1:].rolling(3).mean().plot(figsize=(12,12))
```

```{figure} returnsexample.png
---
name: returnsexamples
---
Figure: Monthly returns - 3-months rolling average
```

We can now perform the linear regression to estimate individual betas. Let's do the test with British Petroleum (BP):

```Python
from statsmodels.api import OLS
import statsmodels.tools

factors_for_reg = statsmodels.tools.add_constant(risk_factors, prepend = True) # we add a constant for the alpha component
factors_for_reg['erM_rf'] = factors_for_reg['erM'] - factors_for_reg['rf'] # The Market factor return is Market returns minus risk free rate

results = OLS(endog = returns['BP'] - factors_for_reg['rf'],
              exog = factors_for_reg[['const','erM_rf','SMB','HML','WML']],
              missing = 'drop').fit()

results.params
```
and the output is:
```
const    -0.005202
erM_rf    1.409346
SMB      -0.696120
HML       0.995068
WML       0.117735
```

What does it means? The idiosyncratic risk associated to BP is close to zero. BP is strongly exposed to the market risk and to the value factor. It is negatively loaded into the size factor (not surprising, as it is a big company) and neutral regarding the momentum factor (close to zero).

### Risk Factor Portfolio

In this part, we'll see how to construct a risk factor portfolio. As investors are compensated for taking systematic risk(s), they can look for gaining exposure to these risks with the latter. Again, for further details, the interested reader should refer to [these slides](http://www.thierry-roncalli.com/download/AM-Lecture3.pdf).

Let's begin with the first and more broadly invested risk factor: the market risk. From the CAPM framework, the only systematic risk is the market risk. Exposure to market risk can be otained by investing in market-capitalization indexes. 

We can create such a portfolio with a new dataclass `Market`, with the new `mv` (market value) data. The `get_portfolio` method is simply defined as the market-capitalization weighting:
```Python
@dataclass
class MarketCapitalizationIndex:
  mv: np.array # Market Cap
  mu: np.array # Expected Returns
  Sigma: np.matrix # Covariance Matrix

  def get_portfolio(self) -> Portfolio:
    x = self.mv / np.sum(self.mv)
    return Portfolio(x = x, mu = self.mu, Sigma = self.Sigma)

```
Despite the commercial success in passive investing with market portfolio (ie. market-cap indexes), critics arised with empirical evidences against the efficiency of market-cap investing: theory and empirical evidences introduced other systematic factors models to capture new risk premia. To generate excess returns in the long-run, investors can adopt factor investing by adding these risk factors to the existing market risk. But how can we build factor portfolio?

In the literature, factor portfolio are built with a long/short approach. It means that the weights can be negative (short positions) or positive (long positions). We can illustrate the construction of a long/short portfolio with the quintile approach:
- We define a score $S_i(t_{\tau})$ for each stock $i$ at each rebalancing date $t_{\tau}$
- We specify a weighting scheme $w_i(t_{\tau})$ (value-weighted or equally-weighted).
- Stocks with the 20\% highest scores are assigned a positive weight according to the weighting sheme ($Q1(t_{\tau})$ portfolio or the long portfolio)
- Stocks with the 20% lowest scores are assigned a negative weight according to the weighting scheme ($Q5(t_{\tau})$ portfolio, or the short portfolio)

Finally, the performance of the risk factor between two rebalancing dates corresponds to the performance of the long/short portfolio:

\begin{equation}
F(t) = F(t_{\tau}) \cdot (\sum_{i \in Q1(t_{\tau})} w_i(t_{\tau}) (1 + R_i(t)) - \sum_{i \in Q5(t_{\tau})} w_i(t_{\tau}) (1 + R_i(t)))
\end{equation}

Let's illustrate with the quintile method we've covered previously, by creating a `LongShortQuintile` dataclass. This dataclass has the method `get_portfolio` returning two `Portfolio` objects:

```Python
@dataclass
class LongShortQuintile:
  mu: np.array # Expected Returns
  Sigma: np.matrix # Covariance Matrix
  S: np.array # scores

  def get_portfolio(self) -> list[Portfolio]:
    # find the borns to define Q1 and Q5
    born_Q1 = np.quantile(self.S, 0.8)
    born_Q5 = np.quantile(self.S, 0.2)

    # define the long and short stocks
    long_stocks = np.where(self.S > born_Q1)
    short_stocks = np.where(self.S < born_Q5)

    # define the vector of weights (equally-weighted here)

    long_portfolio = np.zeros(len(self.S))
    long_portfolio[long_stocks] = 1 / len(long_stocks)
    
    short_portfolio = np.zeros(len(self.S))
    short_portfolio[short_stocks] = 1 / len(short_stocks)
    
    return [Portfolio(x = long_portfolio, mu = self.mu, Sigma = self.Sigma),
            Portfolio(x = short_portfolio, mu = self.mu, Sigma = self.Sigma)
            ]
```

We can test it with a vector of scores:
```Python
S = np.array([1.1, 
     0.5,
     2.3,
     0.3])

test_ls = LongShortQuintile(mu = mu, Sigma = Sigma, S = S)

new_port = test_ls.get_portfolio()

```

The long portfolio is:
```Python
new_port[0].x
```
```
array([0., 0., 1., 0.])
```
And the short portfolio:
```Python
new_port[1].x
```
```
array([0., 0., 0., 1.])
```
