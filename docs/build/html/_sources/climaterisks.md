# Climate Risks Integration Strategies

Climate risks is a hot topic in Finance, from regulators requirements for climate risks stress tests to investors appetite for climate investing. As a future sustainable finance analyst, you will be asked for guidances on climate risks integration strategies. 

The purpose of this part is to give you a brief overview of the main existing strategies for climate risks integration, from the widely implemented low-carbon strategy with fundamental data (carbon intensity) to the enhanced index with market-based data (carbon beta).

Low-carbon strategy corresponds to portfolio's decarbonization, excluding the higher emitting stocks. This strategy is a tool for climate risks hedging if the assumption that carbon risk is not priced by the market holds.

An enhanced index with carbon beta recognizes that carbon risk is, at least partially, priced-in by the market. The purpose of this approach is to measure the sensibility of stocks to the carbon systematic risk and to build a portfolio that is negatively (ie. favoring stocks with positive reaction to carbon risk) loaded towards carbon risk.

## Low-Carbon Strategy

As a first climate risks integration strategy, we propose to follow Andersson et al. (2016) {cite:p}`andersson2016hedging` and Roncalli (2023), with a simple low-carbon index strategy.

The strategy consists in (i) reducing the weighted-average carbon intensity (WACI of the portoflio) while (ii) minimizing the tracking error relative to a benchmark.

The underlying assuption is that carbon risk is unpriced by the market. The financial aspect of carbon risk is then a risk of abrupt pricing by the market, once the markets participants integrate it. By reducing the portfolio's WACI, Andersson et al. (2016) suppose that the portfolio's carbon risk (here, the repricing risk associated with an abrupt carbon tax or carbon policy implementation) will be reduced. 

This carbon risk-hedging strategy is widely followed by index providers and asset managers, and can be defined as a low-carbon strategy.

In what follow, we will test two alternatives formulations for the climate objective, proposed by Andersson et al. (2016) and following the notations used in Roncalli (2023): 
- the threshold approach, which consists in reducing the portfolio's WACI by changing the weights of stocks;
- the order-statistic approach, which consists in excluding the $m$ most emitting stocks.

### Portfolio Optimization in the Presence of a Benchmark

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

We have exactly the same QP problem than with a long-only mean-variance portfolio, except that $q = -(\gamma \mu + \Sigma b)$.

Let's implement it in Python:
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

### Threshold Approach

With the threshold approach, the objective is to minimize the tracking error with the benchmark while imposing a reduction $\mathfrak{R}$ in terms of carbon intensity. In practice, implementing such approach involves the weighted-average carbon intensity (WACI) computation and the introduction of a new constraint in a portfolio optimization problem with the presence of a benchmark (Roncalli, 2023). In this part, we first define the WACI, and then introduce the threshold approach as an additional constraint to the portfolio optimization with a benchmark problem seen in the previous part.

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

Let's implement a `CarbonPortfolio` dataclass:
```Python
from dataclasses import dataclass
import numpy as np

@dataclass 
class CarbonPortfolio:
  """
  A class that implement informations and methods needed for a carbon portfolio.
  """
  x: np.array # Weights
  CI: np.array # Carbon Intensities
  Sigma: np.matrix # Covariance Matrix


  def get_waci(self) -> float:
    return self.x.T @ self.CI
```
#### Integrating Carbon Intensity Reduction as a Constraint

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

If `qpsolvers` is not installed yet:

```Python
!pip install qpsolvers 
```

We define a `LowCarbonStrategy` dataclass, because every low-carbon approaches will use the same information:
```Python
from abc import ABC, abstractmethod

@dataclass
class LowCarbonStrategy:
  b: np.array # Benchmark Weights
  CI:np.array # Carbon Intensity
  Sigma: np.matrix # Covariance Matrix


  def get_portfolio(self) -> CarbonPortfolio:
    pass
```

Now, we define a `ThresholdApproach` dataclass that inherits from `LowCarbonStrategy`:
```Python
from qpsolvers import solve_qp

@dataclass
class ThresholdApproach(LowCarbonStrategy):

  def get_portfolio(self, reduction_rate:float) -> CarbonPortfolio:
    """QP Formulation"""
    x_optim = solve_qp(P = self.Sigma,
              q = -(self.Sigma @ self.b), # we put a minus here because this QP solver consider +x^T R
              A = np.ones(len(self.b)).T, 
              b = np.array([1.]),
              G = self.CI.T, # resulting WACI
              h = (1 - reduction_rate) * self.b.T @ self.CI, # reduction
              lb = np.zeros(len(self.b)),
              ub = np.ones(len(self.b)),
              solver = 'osqp')

    return CarbonPortfolio(x = x_optim, 
                           Sigma = self.Sigma, CI = self.CI)
```

Let's work on an example (from Roncalli, 2023) with the following benchmark weights $b$ and carbon intensities $CI$:

```Python
b = np.array([0.20,
              0.19,
              0.17,
              0.13,
              0.12,
              0.08,
              0.06,
              0.05])

CI = np.array([100.5,
               97.2,
               250.4,
               352.3,
               27.1,
               54.2,
               78.6,
               426.7])
```

We can use the market one-factor model to estimate the covariance matrix, based on stocks betas $\beta$, idiosyncratic volatilities $\tilde{\sigma}$
and market volatiltiy $\sigma_m$:

\begin{equation}
\Sigma = \beta \beta^T \sigma_m^2 + D
\end{equation}

Where $D$ is a diagonal matrix with $\tilde{\sigma}^2$ on its diagonal.

```Python
betas = np.array([0.30,
                  1.80,
                  0.85,
                  0.83,
                  1.47,
                  0.94,
                  1.67,
                  1.08])

sigmas = np.array([0.10,
                   0.05,
                   0.06,
                   0.12,
                   0.15,
                   0.04,
                   0.08,
                   0.07])

Sigma = betas @ betas.T * 0.18**2 + np.diag(sigmas**2)
```

We can now instantiate our threshold construction approach:

```Python
low_carbon_portfolio = ThresholdApproach(b = b, 
                                         CI = CI,
                                         Sigma = Sigma)
```

And let's simulate it with reduction rates $\mathfrak{R}$ between 0 and 70\%:

```Python
from numpy import arange

list_R = arange(0.0,0.7, 0.05)
list_portfolios = []


for R in list_R:
  list_portfolios.append(low_carbon_portfolio.get_portfolio(reduction_rate = R))

def get_tracking_error_volatility(x:np.array, 
                                  b:np.array,
                                  Sigma:np.array) -> float:
  return np.sqrt((x - b).T @ Sigma @ (x - b))

import matplotlib.pyplot as plt


reduction_rate_threshold = [reduction * 100 for reduction in list_R]
te_threshold = [get_tracking_error_volatility(x = portfolio.x, b = b, Sigma = Sigma) * 100 for portfolio in list_portfolios]

plt.figure(figsize = (10, 10))
plt.plot(reduction_rate_threshold, te_threshold)
plt.xlabel("Carbon Intensity Reduction (in %)")
plt.ylabel("Tracking Error Volatility (in %)")
plt.title("Efficient Decarbonization Frontier with Threshold Approach")
plt.show()
```

```{figure} thresholdapproach.png
---
name: thresholdapproach
---
Figure: Efficient Decarbonization Frontier with Threshold Approach
```

Because we impose a constraint and minimize the TE risk, the resulting portfolio will have fewer stocks than the initial benchmark $b$. This imply that the portfolio $x$ is less diversified than the initial benchmark $b$. In order to explicitly control the number of removed stocks, Andersson et al. (2016) and Roncalli (2023) propose another methodology: the order-statistic approach.
### Order-Statistic Approach

Andersson et al. (2016) and Roncalli (2023) propose a second approach by eliminating the $m$ worst performing issuers in terms of carbon intensity. The choice of the parameter $m$ allows for a direct control of number of removed stocks.

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

Contrary to the threshold approach, the reduction rate $\mathfrak{R}$ is not a parameter, but an output of the order-statistic approach. We thus need to define a function computing the resulting reduction rate compated to the benchmark, such as:

\begin{equation}
\mathfrak{R}(x|b) = 1 - \frac{x^T \cdot CI}{b^T \cdot CI}
\end{equation}

```Python
def get_waci_reduction(x:np.array,
                       b:np.array,
                       CI:np.array) -> float:
    return 1 - (x.T @ CI) / (b.T @ CI)
```

#### Optimal Weights with TE Minimization

We can introduce the order-statistic approach into our optimization problem with the new constraint. The optimization problem becomes (Roncalli, 2023):


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

Where $x_i^+ = 𝟙\{CI_i < CI^{m,n}\}$, which is a vector of zeros and ones (zero if the stock is excluded, 1 otherwise).

And the following QP parameters:

\begin{equation*}
\begin{aligned}
& P = \Sigma \\
& q = - \Sigma b \\
& A = 1^T_n \\
& b = 1 \\
& lb = 0_n \\
& ub = 𝟙\{CI_i < CI^{m,n}\}
\end{aligned}
\end{equation*}

Let's implement this approach in Python:
```Python
@dataclass
class OrderStatisticTE(LowCarbonStrategy):
    def get_portfolio(self, m:int) -> CarbonPortfolio:
      """QP Formulation"""
 
      x_sup = np.zeros(len(self.b)) # the vector for exclusion 
      x_sup[np.where(CI >= np.unique(self.CI)[-m])] = 0
      x_sup[np.where(CI < np.unique(self.CI)[-m])] = 1

      x_optim = solve_qp(P = self.Sigma,
                q = -(self.Sigma @ self.b), 
                A = np.ones(len(self.b)).T, 
                b = np.array([1.]) ,
                lb = np.zeros(len(self.b)) ,
                ub = x_sup,
                solver = 'osqp')

      return CarbonPortfolio(x = x_optim, 
                            Sigma = self.Sigma, CI = self.CI)

```

Using the same example from Roncalli (2023), let's plot the relationship between reduction rate and tracking error:

```Python
low_carbon_portfolio = OrderStatisticTE(b = b, 
                                         CI = CI,
                                         Sigma = Sigma)

list_m = arange(1,6, 1)
list_portfolios = []

for m in list_m:
  list_portfolios.append(low_carbon_portfolio.get_portfolio(m = m))

reduction_rate_order_te = [get_waci_reduction(x = portfolio.x,
                   b = b,
                   CI = CI) * 100 for portfolio in list_portfolios]
te_order_te = [get_tracking_error_volatility(x = portfolio.x, b = b, Sigma = Sigma) * 100 for portfolio in list_portfolios]


plt.figure(figsize = (10, 10))
plt.plot(reduction_rate_threshold, te_threshold)
plt.plot(reduction_rate_order_te, te_order_te)
plt.legend(["Threshold Approach", "Order-Statistic with TE minimizatino"], loc=0)
plt.xlabel("Carbon Intensity Reduction (in %)")
plt.ylabel("Tracking Error Volatility (in %)")
plt.title("Efficient Decarbonization Frontier")
plt.show()
```

```{figure} orderstatisticte3.png
---
name: orderstatisticte3
---
Figure: Efficient Decarbonization Frontier
```


Because we are directly excluding high-emitters stocks rather than underweighting them, tracking error volatility increases faster with the reduction rate than with the threshold approach, as we deviate more from the initial benchmark. 

However, the resulting portfolio is more explainable than with the threshold approach. There is a trade-off between tractability and efficiency. 

Because we still rely on an optimization program in order to find the portfolio weights after exclusions, final weights between the remaning stocks can still be challenging to explain. Another approach, easier to explain, is the naive re-weighting. 

#### Naive Re-weighting

A "naive" solution consists in re-weighting the remaining stocks:

\begin{equation}
x_i = \frac{𝟙\{CI_i < CI^{m,n}\}b_i}{\sum^n_{k=1} 𝟙\{CI_k < CI^{m,n}\}b_k}
\end{equation}

This new approach doesn't rely on any optimization program. It's quite easy to implement in Python:

```Python
@dataclass
class OrderStatisticNaive(LowCarbonStrategy):
    def get_portfolio(self, m:int) -> CarbonPortfolio:
      x_sup = np.zeros(len(self.b)) # the vector for exclusion 
      x_sup[np.where(CI >= np.unique(self.CI)[-m])] = 0
      x_sup[np.where(CI < np.unique(self.CI)[-m])] = 1

      # reweighting
      x_optim = b / (x_sup.T @ b)
      x_optim[np.where(x_sup == 0)] = 0

      return CarbonPortfolio(x = x_optim, 
                            Sigma = self.Sigma, CI = self.CI)
```

Let's plot the relationship between the reduction rate and the tracking error volatility:
```Python
low_carbon_portfolio = OrderStatisticNaive(b = b, 
                                         CI = CI,
                                         Sigma = Sigma)

list_m = arange(1,6, 1)
list_portfolios = []

for m in list_m:
  list_portfolios.append(low_carbon_portfolio.get_portfolio(m = m))


reduction_rate_naive = [get_waci_reduction(x = portfolio.x,
                   b = b,
                   CI = CI) * 100 for portfolio in list_portfolios]
te_naive = [get_tracking_error_volatility(x = portfolio.x, b = b, Sigma = Sigma) * 100 for portfolio in list_portfolios]


plt.figure(figsize = (10, 10))
plt.plot(reduction_rate_threshold, te_threshold)
plt.plot(reduction_rate_order_te, te_order_te)
plt.plot(reduction_rate_naive, te_naive)

plt.legend(["Threshold Approach", "Order-Statistic with TE minimization",
            "Order-Statistic with naive reweighting"], loc=0)
plt.xlabel("Carbon Intensity Reduction (in %)")
plt.ylabel("Tracking Error Volatility (in %)")
plt.title("Efficient Decarbonization Frontier")
plt.show()
```

```{figure} orderstatisticnaive2.png
---
name: orderstatisticnaive2
---
Figure: Efficient Decarbonization Frontier
```

Again, the tracking error increases faster with the reduction rate than with the threshold approach. The increase is even higher than with the minimization of the tracking error for the weighting scheme. But the resulting weights are more easily tractable and easier to explain.

### Key Takeaways

- We've covered the most frequent carbon risk-hedging strategy with the low-carbon strategy approach. It relies on minimizing the tracking error volatiltiy relative to a benchmark while diminishing the exposure to carbon risk, measured with the carbon intensity.

- We've seen that the max-threshold approach dominates the order-statistic with TE minimization and the order-statistic with naïve reweighting in terms of decarbonization and tracking error volatility trade-off.

- The main assumption of the low-carbon strategy is the absence of carbon risk pricing. We will relax this assumption in the next part.

## Enhanced Index with Carbon Beta


While low-carbon strategy relies on the hypothesis that carbon risk is unpriced by the markets, one could ask if it is still the case, with the growth of climate investing in asset management and the rise of public concerns about global warming. In contrast with Andersson et al. (2016), Gorgen et al. (2019) {cite:p}`gorgen2020carbon` and Roncalli et al. (2020) {cite:p}`roncalli2020measuring` define carbon risk from a financial point of view, considering that the carbon risk is priced in by the market (at least partially). This relax the low-carbon strategy assumption that carbon risk is not priced in by the market.

In this part, we will introduce how Gorgen et al. (2019) show that carbon risk is a systematic risk factor, priced in by the market. Then, we will follow Roncalli et al. (2020) by introducing carbon beta into a portfolio optimization in a context of a benchmark problem.

### A Brown-Minus-Green Factor: Carbon Systematic Risk 

Gorgen et al. (2019) developed the carbon risk management project (Carima). They propose to measure the carbon risk of a stock or a portfolio by considering the dynamics of stock prices.

To do so, they developped and made public a Brown-Minus-Green Factor (BMG). The BMG factor construction is based various climate-related informations.

The Carima's BMG factor construction involves:
1. The development of a scoring system to determine if a firm is green, neutral or brown
2. The construction of a factor portfolio for carbon risk which has a long exposure to brown firms and a short exposure to green firms

The first step uses four ESG Databases (55 carbon risk proxy variables are retained) in order to determine a Brown-Green score. The higher the score, the browner the firm.

The second step corresponds to the construction of the BMG risk factor. The construction of the BMG factor follows the methodoly of Fama and French (1992, 1993) consisting in splitting the stocks into six portfolios:

|   | Green  | Neutral  | Brown  |  
|---|---|---|---|
|  Small | SG  | SN  | SB  | 
| Big  |  BG | BN  | BB  |

Where the classification is based on the terciles of the aggregating score and the median market capitalization. 

Finally, the return of the BMG factor is computed as:

\begin{equation}
F_{BMG}(t) = \frac{1}{2}(SB(t)+BB(t)) - \frac{1}{2} (SG(t) + BG(t))
\end{equation}

Let's have a look at the resulting BMG factor:

```Python
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

url = 'https://assets.uni-augsburg.de/media/filer_public/6f/36/6f36b1e7-9e03-4ca4-a4cd-c17e22a2e895/carbon_risk_factor_updated.xlsx'
carbon_risk = pd.read_excel(url, sheet_name = 'monthly')
plt.plot(carbon_risk['month'].values, np.cumprod(1 + carbon_risk['BMG'].values))
plt.title("Cumulative Returns BMG Factor")
plt.show()
```

```{figure} bmg.png
---
name: bmg
---
Figure: Cumulative Returns, BMG Factor
```

During the last decade, it seems that the BMG factor returns were constantly negative, that is brown assets underperformed green assets. If we think about carbon risk as a systematic risk, this result is puzzling. We will tackle this question in the next part (green assets outperformance).


### Carbon Beta: A Market-Based Measure

Once the BMG factor is built, Gorgen et al. (2019) propose to define the carbon financial risk of a stock by using its price sentivity to the BMG factor (carbon beta).

The authors propose to extend the Carhart Model with four factors with the additional BMG carbon risk factor:

\begin{equation}
R(t) = \alpha + \beta_{MKT}F_{MKT}(t) + \beta_{SMB}F_{SMB}(t) + \beta_{HML}F_{HML}(t) + \beta_{WML} F_{WML}(t) + \beta_{BMG} F_{BMG}(t) + u(t)
\end{equation} 

This regression is run on a stock-by-stock basis, and resulting $\beta_k$ are the sentivity of the stock to each factor.

The carbon beta interpretation is the following:

- $\beta_{BMG} >> 0$: the stock value decreases in comparison to other stocks if transition process is unexpectedly successful
- $\beta_{BMG} \approx 0$: transition process influences stock value on average
- $\beta_{BMG} << 0$: stock value increases in comparison to other stocks if transition process is unexpectedly successful

To apply the Carhart model with the new BMG factor, let's first load the data as we did in the first introducing part:
```Python
import pandas as pd
url = 'https://assets.uni-augsburg.de/media/filer_public/67/d8/67d814ce-0aa9-4156-ad25-fb2a9202769d/carima_exceltool_en.xlsx'
risk_factors = pd.read_excel(url, sheet_name = 'Risk Factors').iloc[:,4:10]
risk_factors['Month'] = pd.to_datetime(risk_factors['Month'].astype(str)).dt.strftime('%Y-%m')
carbon_risk = pd.read_excel(url, sheet_name = 'BMG').iloc[:,4:6]
carbon_risk['Month'] = pd.to_datetime(carbon_risk['Month'].astype(str)).dt.strftime('%Y-%m')

factors_df = risk_factors.merge(carbon_risk, how = "left", on = "Month")
factors_df.index = factors_df['Month']

url = 'https://assets.uni-augsburg.de/media/filer_public/67/d8/67d814ce-0aa9-4156-ad25-fb2a9202769d/carima_exceltool_en.xlsx'
returns = pd.read_excel(url, sheet_name = 'Asset Returns').iloc[:,4:14]
returns['Month'] = pd.to_datetime(returns['Month'].astype(str)).dt.strftime('%Y-%m')
returns.index = returns['Month']
```

Now that we have all the data prepared, let's make the test for British Petroleum (BP):

```Python
from statsmodels.api import OLS
import statsmodels.tools

factors_for_reg = statsmodels.tools.add_constant(factors_df, prepend = True)
factors_for_reg['erM_rf'] = factors_for_reg['erM'] - factors_for_reg['rf']

results = OLS(endog = returns['BP'] - factors_for_reg['rf'],
              exog = factors_for_reg[['const','erM_rf','SMB','HML','WML','BMG']],
              missing = 'drop').fit()

results.params['BMG']
```
And the resulting carbon beta for BP is:
```
0.9433783665287284
```

The result is consistent with the interpretation of the carbon beta: as the carbon beta for BP is highly positive, it means that the company is negatively exposed to the carbon financial risk priced by the market.

### Introducing Carbon Beta into a Portfolio Optimization in the Presence of a Benchmark

Following Roncalli et al. (2020), we can directly add a BMG's exposure constraint in a portfolio optimization in the presence of a benchmark framework:

\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2}(x-b)^T \Sigma (x-b)\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & &  0_n \leq x \leq 1_n \\
& & & \beta_{bmg}^Tx \leq \beta_{bmg}^+
\end{aligned}
\end{equation*}

With $\beta_{bmg}^+$ as the maximum tolerance of the investor with respect to the relative BMG risk. 

We have the following QP parameters:

\begin{equation*}
\begin{aligned}
& P = \Sigma \\
& q = \Sigma b \\
& A = 1^T_n \\
& b = 1 \\
& G = \beta_{bmg}^T \\
& h = \beta_{bmg}^+\\
& lb = 0_n \\
& ub = 1_n
\end{aligned}
\end{equation*}


The approach is similar to the one with the maximum threshold approach in the previous part, except that we use a market-based measure (carbon beta) rather than a fundamental-based measure (carbon intensity) in the low-carbon strategy. Thus, with this strategy, we relax the assumption that carbon risk is not priced in by the market.

We can implement this new strategy with Python.
Let's first create a `CarbonPortfolio` dataclass:

```Python
from dataclasses import dataclass
import numpy as np

@dataclass 
class CarbonPortfolio:
  
  x: np.array # Weights
  carbon_betas: np.array # Carbon Betas
  Sigma: np.matrix # Covariance Matrix
```

Then, we can implement the optimization problem:
```Python
from qpsolvers import solve_qp


@dataclass
class EnhancedIndexCarbonBeta:
  b:np.array # Benchmark weights
  carbon_betas:np.array # Carbon Betas
  Sigma: np.matrix # Covariance Matrix

  def get_portfolio(self, beta_sup:float) -> CarbonPortfolio:
    """QP Formulation"""

    x_optim = solve_qp(P = self.Sigma,
              q = - self.Sigma @ self.b, 
              A = np.ones(len(self.carbon_betas)).T, 
              b = np.array([1.]),
              G = self.carbon_betas.T,
              h = np.array([beta_sup]),
              lb = np.zeros(len(self.carbon_betas)),
              ub = np.ones(len(self.carbon_betas)) ,
              solver = 'osqp')

    return CarbonPortfolio(x = x_optim, 
                           Sigma = self.Sigma, carbon_betas = self.carbon_betas)
```

And let's test the approach with the following example (same as the previous part, we just replace the carbon intensity measure with carbon betas):
```Python
b = np.array([0.20,
              0.19,
              0.17,
              0.13,
              0.12,
              0.08,
              0.06,
              0.05])

carbon_betas = np.array([-0.3,
               0.91,
               0.01,
               0.4,
               -0.02,
               0.5,
               -0.6,
               0.80])

betas = np.array([0.30,
                  1.80,
                  0.85,
                  0.83,
                  1.47,
                  0.94,
                  1.67,
                  1.08])

sigmas = np.array([0.10,
                   0.05,
                   0.06,
                   0.12,
                   0.15,
                   0.04,
                   0.08,
                   0.07])

Sigma = betas @ betas.T * 0.18**2 + np.diag(sigmas**2)

low_betas_portfolio = EnhancedIndexCarbonBeta( b = b,
                                         carbon_betas = carbon_betas,
                                         Sigma = Sigma)
```

Let's now plot the relationship between the carbon betas and the new optimal weights deviation from the benchmark, with $\beta_{bmg}^+ = 0$:

```Python
low_betas_portfolio = EnhancedIndexCarbonBeta( b = b,
                                         carbon_betas = carbon_betas,
                                         Sigma = Sigma)

dev = (low_betas_portfolio.get_portfolio(beta_sup = 0).x - b) * 100


plt.figure(figsize = (10, 10))
plt.scatter(carbon_betas, dev)
plt.xlabel("Carbon Beta")
plt.ylabel("Weights deviation from benchmark (in %)")
plt.title("Relationship between Carbon Beta and optimal weights")
plt.show()
```

```{figure} carbonbetavsoptimalweights.png
---
name: carbonbetavsoptimalweights
---
Figure: Relationship between Carbon Beta and optimal weights with $\beta_{bmg}^+ = 0$
```

The impact of the carbon beta threshold introduction, with $\beta_{bmg}^+$ leads, as expected, to an overweighting of stocks negatively loaded into the BMG factor and the underweighting of stocks positively loaded ino the BMG factor

### Key Takeaways

- We've seen that we can relax the assumption that carbon risk is not priced in by the market. Carbon risk seems to corresponds to a systematic risk, with the existence of a Brown-Minus-Green Factor. 

- Stocks sentivities to the BMG factor can be integrated into a enhanced index, in order to hedge for carbon risk. This strategy is based on a marked-based measure of carbon risk.

- Question remains regarding the returns associated the BMG factor. Indeed, returns should reward risk. With carbon risk, brown companies are significantly exposed to the risk. Then, investors should require higher returns to bear the risk with investment in brown companies. But the Carima's BMG factor provide significant negative returns. With historic returns, it seems that investors require higher returns from green companies than for brown companies. 