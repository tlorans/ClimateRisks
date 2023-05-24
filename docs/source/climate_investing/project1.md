## Project 1: Sector Constraints in Portfolio Decarbonization

In our first exposure to portfolio decarbonization, no other constraint than the ones related to portfolio decarbonization was imposed. 

However, portfolio decarbonization needs to take into account the industry in which the company operates. In practice, you will then need to add sector constraints in your approach. 

The question is which industrial classification needs to be used as a reference point. We will address this point.

In what follow, we use Roncalli (2023) as a reference.
### Sector Weights Constraint

In order to overcome the first issue regarding the lack of sector diversification with the static portfolio decarbonization presented in the previous part, we can extend the framework by considering a sector weight constraint (Roncalli, 2023):

\begin{equation}
s^-_j \leq \sum_{i \in Sector_j} x_i \leq s_j^+
\end{equation}

With $s_j$ a $n \times 1$ vector of sector-mapping (ie. we have here only one sector considered), with elements 0 or 1 if the stock $n$ belongs to the sector such as:

\begin{equation}
s_{i,j} = 𝟙\{i \in Sector_j\}
\end{equation}

We note that:
\begin{equation}
\sum_{i \in Sector_j} x_i = s_j^T x
\end{equation}

We can then rewrite the sector constraint $s^-_j \leq \sum_{i \in Sector_j} x_i \leq s_j^+$ as (Roncalli, 2023):

\begin{equation}
\begin{cases}
  s^-_j \leq s_j^Tx \\
  s_j^Tx \leq s^+_j
\end{cases}
\end{equation}

Which we can reorder (such that the thresholds are on the right and the sector weights on the left) as:


\begin{equation}
\begin{cases}
  - s_j^Tx \leq - s^-_j \\
  s_j^Tx \leq s^+_j
\end{cases}
\end{equation}

These last constraints can the be included into the QP inequality constraint $Gx \leq h$ as:

\begin{equation}
G = \begin{bmatrix}
-s_j^T \\
-s^T_j
\end{bmatrix}
\end{equation}

with G is a $2 \times n$ matrix,
and: 

\begin{equation}
h = \begin{bmatrix}
-s_j^- \\
s_j^+
\end{bmatrix}
\end{equation}

with h is a $2 \times 1$ vector.

You can extend this approach with many sectors.

Let's illustrate the concept by implementing an example in Python. First, let's take the scripts we've used before to define a Carbon Portfolio:

```Python
from dataclasses import dataclass
import numpy as np

@dataclass 
class CarbonPortfolio:
  """
  A class that implement supplementary information CI and new method get_waci,
  to be used in the low-carbon strategy implementation.
  """
  x: np.array # Weights
  CI: np.array # Carbon Intensities
  Sigma: np.matrix # Covariance Matrix


  def get_waci(self) -> float:
    return self.x.T @ self.CI

```
Let's make an example:

```Python
b = np.array([0.23,
              0.19,
              0.17,
              0.13,
              0.09,
              0.08,
              0.06,
              0.05])

CI = np.array([125,
               75,
               254,
               822,
               109,
               17,
               341,
               741])

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
Let's assume two sectors: $Sector_1$ and $Sector_2$.
We have:

\begin{equation}
s_1^T = 
 \begin{bmatrix}
1 & 1 & 0 & 0 & 1 & 0 & 1 & 0\\
\end{bmatrix}
\end{equation}

and:

\begin{equation}
s_2^T = 
 \begin{bmatrix}
0 & 0 & 1 & 1 & 0 & 1 & 0 & 1\\
\end{bmatrix}
\end{equation}

We can prepare the sector constraints specification in Python:

```Python
s_1 = np.array([1, 1, 0, 0, 1, 0, 1, 0])
s_2 = np.array([0, 0, 1, 1, 0, 1, 0, 1])
s_j = np.vstack([- s_1.T, - s_1.T, - s_2.T, - s_2.T]) # we stack the sectors vectors

```

To choose sectors weights constraints, let's first take a look at their relative weights in the initial benchmark:

```Python
s_1.T @ b
```
```
0.5700000000000001
```
```Python
s_2.T @ b
```
```
0.43000000000000005
```
We can choose for example $s_1^+ = 0.65$, $s_1^- = 0.5$ and $s_2^+ = 0.5$ and $s_2^- = 0.4$.

```Python
sectors_constraints = np.array([ -0.5, 0.65, -0.4, 0.5]) 
```

We can now implement a low-carbon strategy with the threshold approach, while controlling for sector weights:

```Python


from abc import ABC, abstractmethod

@dataclass
class LowCarbonStrategy:
  b: np.array # Benchmark Weights
  CI:np.array # Carbon Intensity
  Sigma: np.matrix # Covariance Matrix


  def get_portfolio(self) -> CarbonPortfolio:
    pass

from qpsolvers import solve_qp

@dataclass
class ThresholdApproach(LowCarbonStrategy):

  def get_portfolio(self, reduction_rate:float) -> CarbonPortfolio:
    """QP Formulation"""
    x_optim = solve_qp(P = self.Sigma,
              q = -(self.Sigma @ self.b), 
              A = np.ones(len(self.b)).T, 
              b = np.array([1.]),
              G = self.CI.T, # resulting WACI
              h = (1 - reduction_rate) * self.b.T @ self.CI, # reduction
              lb = np.zeros(len(self.b)),
              ub = np.ones(len(self.b)),
              solver = 'osqp')
    
    return CarbonPortfolio(x = x_optim, 
                        Sigma = self.Sigma, CI = self.CI)
    
  def get_portfolio_with_sector_constraints(self, reduction_rate:float, s_j:np.array, sector_constraints:np.array) -> CarbonPortfolio:
    """QP Formulation"""
    x_optim = solve_qp(P = self.Sigma,
              q = -(self.Sigma @ self.b), 
              A = np.ones(len(self.b)).T, 
              b = np.array([1.]),
              G = np.vstack([self.CI.T, s_j]), # nested G
              h = np.hstack([(1 - reduction_rate) * self.b.T @ self.CI, sector_constraints]), # reduction + sector constraints
              lb = np.zeros(len(self.b)),
              ub = np.ones(len(self.b)),
              solver = 'osqp')

    return CarbonPortfolio(x = x_optim, 
                           Sigma = self.Sigma, CI = self.CI)

```

```Python
low_carbon_portfolio = ThresholdApproach(b = b, 
                                         CI = CI,
                                         Sigma = Sigma)

low_carbon_portfolio.get_portfolio_with_sector_constraints(reduction_rate = 0.5,
                                                           s_j = s_j,
                                                           sector_constraints = sectors_constraints).x
```

```
array([ 2.36352155e-01,  2.53202952e-01,  1.19930045e-01,  4.29437030e-02,
        9.41669784e-02,  2.47256857e-01,  6.14731882e-03, -1.28467006e-08])
```

### Sector Neutrality

We can also impose tighter constraint regarding the sector deviation with the benchmark, by imposing sector neutrality of the portfolio. 

It means that:

\begin{equation}
\sum_{i \in Sector_j}x_i = \sum_{i \in Sector_j}b_i
\end{equation}

In the QP problem, this can be included in the $Ax = b$ equality constraint, with for example for two sectors $s_1$ and $s_2$ and 8 stocks:

\begin{equation}
A_1 = s^T_1 = \begin{bmatrix}
1 & 1 & 0 & 0 & 1 & 0 & 1 & 0 
\end{bmatrix}
\end{equation}

and 

\begin{equation}
A_2 = s^T_2 = \begin{bmatrix}
0 & 0 & 1 & 1 & 0 & 1 & 0 & 1
\end{bmatrix}
\end{equation}

Then:


\begin{equation}
A = \begin{bmatrix}
A_1 \\
A_2
\end{bmatrix}
\end{equation}


And $b_1 = s_1^Tb$, $b_2 = s_2^Tb$ such that:


\begin{equation}
b = \begin{bmatrix}
b_1 \\
b_2
\end{bmatrix}
\end{equation}

Again, we can start to implement the constraints specifications in Python:

```Python
A_sectors = np.vstack([s_1.T, s_2.T])

b_1 = s_1.T @ b
b_2 = s_2.T @ b 
b_sectors = np.hstack([b_1, b_2])
```

Then, let's create a new method integrating the sector neutrality constraint:

```Python
from qpsolvers import solve_qp

@dataclass
class ThresholdApproach(LowCarbonStrategy):

  def get_portfolio(self, reduction_rate:float) -> CarbonPortfolio:
    """QP Formulation"""
    x_optim = solve_qp(P = self.Sigma,
              q = -(self.Sigma @ self.b), 
              A = np.ones(len(self.b)).T, 
              b = np.array([1.]),
              G = self.CI.T, # resulting WACI
              h = (1 - reduction_rate) * self.b.T @ self.CI, # reduction
              lb = np.zeros(len(self.b)),
              ub = np.ones(len(self.b)),
              solver = 'osqp')
    
    return CarbonPortfolio(x = x_optim, 
                        Sigma = self.Sigma, CI = self.CI)
    
  def get_portfolio_with_sector_constraints(self, reduction_rate:float, s_j:np.array, sector_constraints:np.array) -> CarbonPortfolio:
    """QP Formulation"""
    x_optim = solve_qp(P = self.Sigma,
              q = -(self.Sigma @ self.b), 
              A = np.ones(len(self.b)).T, 
              b = np.array([1.]),
              G = np.vstack([self.CI.T, s_j]), # nested G
              h = np.hstack([(1 - reduction_rate) * self.b.T @ self.CI, sector_constraints]), # reduction + sector constraints
              lb = np.zeros(len(self.b)),
              ub = np.ones(len(self.b)),
              solver = 'osqp')

    return CarbonPortfolio(x = x_optim, 
                           Sigma = self.Sigma, CI = self.CI)
    
  def get_portfolio_with_sector_neutrality(self, reduction_rate:float, A_sectors:np.array, b_sectors:np.array):
      x_optim = solve_qp(P = self.Sigma,
            q = -(self.Sigma @ self.b), 
            A = np.vstack([np.ones(len(self.b)).T, A_sectors]), 
            b = np.hstack([1., b_sectors]),
            G = self.CI.T, 
            h = (1 - reduction_rate) * self.b.T @ self.CI, # reduction rate
            lb = np.zeros(len(self.b)),
            ub = np.ones(len(self.b)),
            solver = 'osqp')
      
      return CarbonPortfolio(x = x_optim, 
                           Sigma = self.Sigma, CI = self.CI)

```

```Python
low_carbon_portfolio = ThresholdApproach(b = b, 
                                         CI = CI,
                                         Sigma = Sigma)

low_carbon_portfolio.get_portfolio_with_sector_neutrality(reduction_rate = 0.5,
                                                           A_sectors = A_sectors,
                                                           b_sectors = b_sectors).x
```

```
array([ 2.33515514e-01,  2.41846019e-01,  1.25623128e-01,  4.43874304e-02,
        9.29058752e-02,  2.59989434e-01,  1.73260956e-03, -8.53326324e-09])
```

### Which Classification System?

To impose sectors constraints, we need to identify in which sector the stock belongs to. The question arises regarding the classification system to be used.

Assets owners and managers are familiar with the Global Industry Classification System (GICS) (Chan et al., 2007) {cite:p}`chan2007industry`.

```{figure} gics_hierarchy.png
---
name: gics_hierarchy
---
Figure: GICS Hierarchy, taken from MSCI's website
```

However, this classification system is built for stocks returns comovement clustering and not for portfolio decarbonization purposes. For example, Energy sector is dedicated to Oil & Gas companies, and doesn't includes electricity (and therefore renewable electricity) producers, classified into the Utilities sector. The Utilities sector regroups water utilities, environmental services and elecricity utilities. Applying sector constraints based on this classification will therefore leads to biased portfolio decarbonization.

| Industry   |   |
|---|---|
| 151010  | Chemicals  |
| | 150101010 Commodity chemicals | 
| | 15101020 Diversified chemicals | 
| | 150101030 Fertilizers and agricultural chemicals | 
| | 150101040 Industrial gases | 
| | 150101050 Specialty chemicals | 
| 151020| Construction Materials | 
| | 150102010 Construction materials (including cement) | 
| 151030| Containers and packaging | 
| | 15103010 Metal and glass containers | 
| | 15103020 Paper packaging | 
| 151040 | Metals and mining | 
|  | 15104010 Aluminium | 
|  | 15 104020Diversified metals and mining | 
|  | 15104025 Copper | 
| | 15104030 Gold | 
| | 15104040 Precious metals and minerals | 
| | 15104045 Silver | 
| | 15104050 Steel |  
| 151050 | Paper and forest products | 
|  | 15105010 Forest products | 
|  | 15105020 Paper products | 
| 25  | Consumer discretionary | 
|   | 25203030 Textiles | 


### Your Turn!

1. First, download the set of data we will work with for the rest of this course:
```Python
import pandas as pd
url = 'https://github.com/shokru/carbon_emissions/blob/main/data_fin.xlsx?raw=true'
data = pd.read_excel(url)
```
2. Using the data downloaded, compute the carbon intensity (emissions / market cap)
3. Retrive the sector for each stock in the data. You can easily obtain it with:
```Python
import yfinance as yf

tickerdata = yf.Ticker('TSLA') #the tickersymbol for Tesla
print (tickerdata.info['sector'])
```
4. Compute an initial capitalization-weighted benchmark weights vector $b$ using the market capitalization value
5. Implement a low-carbon strategy with the threshold approach and $\mathfrak{R} = 0.5$
6. Compare the sectors weights in $b$ and $x^*$
7. Implement the same low-carbon strategy but with a sector constraint of your choice. Did you find a solution? Compare the TE between this constrained solution and the one without sector constraints.
