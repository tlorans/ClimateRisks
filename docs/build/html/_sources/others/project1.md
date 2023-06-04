## Project 1: Consistent Portfolio Decarbonization

In our first exposure to portfolio decarbonization, no other constraint than the one related to portfolio decarbonization was imposed. 

## OECM Sectors

### Primary and Secondary Energy Sectors

|  | GICS | Sector Name OECM |
|---|---|---|
| 101010   | Energy Equipment & Services  | Energy |
|   | 10101010 Oil & Gas Drilling  | Energy |
|   | 10101020 Oil & Gas Equipment & Services | Energy |
|  101020 | Oil, Gas & Consumable Fuels  | Energy |
|   | 10102010 Integrated Oil & Gas  | Energy |
|   | 10102020 Oil & Gas Exploration & Production  | Energy |
|   | 10102030 Oil & Gas Refining & Marketing  | Energy |
|   | 10102040 Oil & Gas Storage & Transportation  | Energy |
|   | 10102050 Coal & Consumable Fuels  | Energy |
| 5510 Electric Utilities  |  | Utilities (Power & Gas only) |
| 5520 Gas Utilities|  | Utilities (Power & Gas only) |
| 5530 Multi Utilities | | Utilities (Power & Gas only) |
| 5550 Independent Power and Renewable Electricity Producers | | Utilities (Power & Gas only) |
### End-Use Activities Sectors

|  | GICS | Sector Name OECM |
|---|---|---|
| 601010  Equity Real Estate Investment Trusts (REITs) |  | Buildings |
|  | 60101010 Diversified REITs | Buildings |
|  | 60101020 Industrial REITs | Buildings |
|  | 60101030 Hotel & Resort REITs | Buildings |
|  | 60101040 Office REITs | Buildings |
|  | 60101050 Health Care REITs | Buildings |
|  | 60101060 Residential REITs | Buildings |
|  | 60101070 Retail REITs | Buildings |
|  | 60101080 Specialized REITs | Buildings |
| 601020 Real Estate Management & Development |  | Buildings |
|  | 60102010 Diversified Real Estate Activities | Buildings |
|  | 60102020 Real Estate Operating Companies | Buildings |
|  | 60102030 Real Estate Development | Buildings |
|  | 60102040 Real Estate Services | Buildings |
| 2030 Transportation |  | Transport |
| 203010 Air Freight & Logistics |  | Aviation |
|  | 20301010 Air Freight & Logistics | Aviation |
| 203020 Airlines |  | Aviation |
|  | 20302010 Airlines | Aviation |
| 203030 Marine | | Shipping |
| | 20303010 Marine| Shipping |


## Energy-System Consistent Decarbonization 

For a consistent portfolio decarbonization, you thus need to make sure that decarbonization takes place both in the energy-supply system (primary and secondary energy activities) and in the end-use activities. In particular, portfolio decarbonization shouldn't lead to a portfolio weights deviation towards end-use activities for example. Decarbonization should respect the energy-system constraint.


In what follow, we will first see how to control potential weights deviation for the three stages of the energy-system with portfolio decarbonization. Then we will address full neutrality. 
We use Roncalli (2023) as a reference for implementing the constraints.
### Weights Constraint

In order to limit the weights deviation for the energy-system, and limiting the responsibility bias, we can extend the framework by considering a weights constraint, similar to the sector constraint presented by Roncalli (2023):

\begin{equation}
c^-_j \leq \sum_{i \in Class_j} x_i \leq c_j^+
\end{equation}

With $c_j$ a $n \times 1$ vector of energy-system class-mapping (ie. we have here only one class considered), with elements 0 or 1 if the stock $n$ belongs to the class such as:

\begin{equation}
c_{i,j} = 𝟙\{i \in Class_j\}
\end{equation}

We note that:
\begin{equation}
\sum_{i \in Sector_j} x_i = c_j^T x
\end{equation}

We can then rewrite the class constraint constraint $c^-_j \leq \sum_{i \in Class_j} x_i \leq c_j^+$ as (Roncalli, 2023):

\begin{equation}
\begin{cases}
  c^-_j \leq c_j^Tx \\
  c_j^Tx \leq c^+_j
\end{cases}
\end{equation}

Which we can reorder (such that the thresholds are on the right and the sector weights on the left) as:

\begin{equation}
\begin{cases}
  - c_j^Tx \leq - c^-_j \\
  c_j^Tx \leq c^+_j
\end{cases}
\end{equation}

These last constraints can the be included into the QP inequality constraint $Gx \leq h$ as:

\begin{equation}
G = \begin{bmatrix}
-c_j^T \\
-c^T_j
\end{bmatrix}
\end{equation}

with G is a $2 \times n$ matrix,
and: 

\begin{equation}
h = \begin{bmatrix}
-c_j^- \\
c_j^+
\end{bmatrix}
\end{equation}

with h is a $2 \times 1$ vector.

You can extend this approach with the three classes describing the energy-system.

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

We have three classes in our energy-system: $Class_{PE}$ the primary energy class, $Class_{SE}$ the secondary energy and $Class_{EU}$ the end-use activities.

We have:

\begin{equation}
c_{PE}^T = 
 \begin{bmatrix}
1 & 0 & 0 & 0 & 0 & 0 & 1 & 0\\
\end{bmatrix}
\end{equation}

\begin{equation}
c_{SE}^T = 
 \begin{bmatrix}
0 & 0 & 1 & 1 & 0 & 1 & 0 & 0\\
\end{bmatrix}
\end{equation}

\begin{equation}
c_{EU}^T = 
 \begin{bmatrix}
0 & 1 & 0 & 0 & 1 & 0 & 0 & 1\\
\end{bmatrix}
\end{equation}

We can prepare the sector constraints specification in Python:

```Python
s_1 = np.array([1, 1, 0, 0, 1, 0, 1, 0])
s_2 = np.array([0, 0, 1, 1, 0, 1, 0, 1])
s_j = np.vstack([- s_1.T, - s_1.T, - s_2.T, - s_2.T]) # we stack the sectors vectors

```

To choose classes weights constraints, let's first take a look at their relative weights in the initial benchmark:

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

We can now implement a low-carbon strategy with the threshold approach, while controlling for energy-system and responsibility consistency:

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

### Neutrality

We can also impose tighter constraint regarding energy-system consistency and the responsibility, by imposing class neutrality of the portfolio. 

It means that:

\begin{equation}
\sum_{i \in Class_j}x_i = \sum_{i \in Class_j}b_i
\end{equation}

In the QP problem, this can be included in the $Ax = b$ equality constraint. With 8 stocks and our three energy-system classes we have $c_{PE}$, $c_{SE}$ and $c_{EU}$:

\begin{equation}
A_{PE} = c_{PE}^T = 
 \begin{bmatrix}
1 & 0 & 0 & 0 & 0 & 0 & 1 & 0\\
\end{bmatrix}
\end{equation}

\begin{equation}
A_{SE} = c_{SE}^T = 
 \begin{bmatrix}
0 & 0 & 1 & 1 & 0 & 1 & 0 & 0\\
\end{bmatrix}
\end{equation}

\begin{equation}
A_{EU} = c_{EU}^T = 
 \begin{bmatrix}
0 & 1 & 0 & 0 & 1 & 0 & 0 & 1\\
\end{bmatrix}
\end{equation}

Then:


\begin{equation}
A = \begin{bmatrix}
A_{PE} \\
A_{SE} \\
A_{EU}
\end{bmatrix}
\end{equation}


And $b_{PE} = c_{PE}^Tb$, $b_{SE} = c_{SE}^Tb$ and $b_{EU} = c_{EU}^Tb$ such that:


\begin{equation}
b = \begin{bmatrix}
b_{PE} \\
b_{SE} \\
b_{EU}
\end{bmatrix}
\end{equation}

Again, we can start to implement the constraints specifications in Python:

```Python
A_sectors = np.vstack([s_1.T, s_2.T])

b_1 = s_1.T @ b
b_2 = s_2.T @ b 
b_sectors = np.hstack([b_1, b_2])
```

Then, let's create a new method integrating the energy-system neutrality constraint:

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
