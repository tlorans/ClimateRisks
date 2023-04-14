## Enhanced Index with Carbon Beta

While low-carbon strategy relies on the hypothesis that carbon risk is unpriced by the markets, one could ask if it is still the case, with the growth of climate investing in asset management and the rise of public concerns about global warming. In contrast with Andersson et al. (2016), Gorgen et al. (2019) {cite:p}`gorgen2020carbon` and Roncalli et al. (2020) define carbon risk from a financial point of view, and consider that the carbon risk of equities corresponds to the market risk is priced in by the market (at least partially). This relax the low-carbon strategy assumption that carbon risk is not priced in by the market.

In this part, we will introduce how Gorgen et al. (2019) show that carbon risk is a systematic risk factor, priced in by the market. Then, we will follow Roncalli et al. (2020) by introducing carbon beta into a portfolio optimization in a context of a benchmark problem in order to hedge for carbon risk.

### A Brown-Minus-Green Factor: Carbon Systematic Risk

Gorgen et al. (2019) developed the carbon risk management project (Carima). They propose to measure the carbon risk of a firm or a portfolio by considering the dynamics of stock prices, partly determined by climate policies and transition process towards a green economy.

To do so, they developped and made public a Brown-Minus-Green Factor. This BMG factor is based on large amount of climate information from different dathabases.

The Carima's BMG factor construction involves:
1. The development of a scoring system to determine if a firm is green, neutral or brown
2. The construction of a mimicking factor portfolio for carbon risk which has a long exposure to brown firms and a short exposure to green firms

The first step uses four ESG Databases (55 carbon risk proxy variables are retained). based on the scoring of three dimensions that may affect the stock value of a firm in the event of unexpected shifts towards a low carbon economy: (i) value chain; (ii) public perception and (iii) adaptability.

The scores on each three dimensions are then aggregated with a weighted average, resulting in a Brown-Green score. The higher the BGS value, the browner the firm.

The second step corresponds to the construction of the BMG risk factor. 

The construction of the BMG factor follows the methodoly of Fama and French (1992, 1993) consisting in splitting the stocks into six portfolios:

|   | Green  | Neutral  | Brown  |  
|---|---|---|---|
|  Small | SG  | SN  | SB  | 
| Big  |  BG | BN  | BB  |

Where the classification is based on the terciles of the aggregating BGS and the median market capitalization. 

Finally, the return of the BMG factor is computed as:

\begin{equation}
f_{BMG}(t) = \frac{1}{2}(SB(t)+BB(t)) - \frac{1}{2} (SG(t) + BG(t))
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


### Carbon Beta: A Market-Based Measure

Once the BMG factor is built, Gorgen et al. (2019) propose to define the carbon financial risk of a stock by using its price sentivity to the BMG factor (carbon beta).

The authors propose to extend the Carhart Model with four factors with the additional BMG carbon risk factor:

\begin{equation}
r(t) = \alpha + \beta_{MKT}f_{MKT}(t) + \beta_{SMB}f_{SMB}(t) + \beta_{HML}f_{HML}(t) + \beta_{WML} f_{WML}(t) + \beta_{BMG} f_{BMG}(t) + u(t)
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
And the resultign carbon beta for BP is:
```
0.9433783665287284
```

The result is consistent with the interpretation of the carbon beta: as the carbon beta for BP is highly positive, it means that the company is negatively exposed to the carbon financial risk priced by the market.

### Introducing Carbon Beta into a Portfolio Optimization in the Presence of a Benchmark

Following Roncalli et al. (2020), we can directly add a BMG's exposure constraint in a portfolio optimization in the presence of a benchmark framework:

\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2}x^T \Sigma x\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & &  0_n \leq x \leq 1_n \\
& & & \beta_{bmg}^Tx \leq \beta_{bmg}^+
\end{aligned}
\end{equation*}

With $\beta_{bmg}^+$ as the maximum tolerance of the investor with respect to the relative BMG risk. 

```Python
#### Use the example in table 6 in page 26 of Roncalli et al. 2021

@dataclass
class MinimumVarianceCarbonBeta(PortfolioConstruction):
  CI:np.array # Carbon Intensity

  def get_portfolio(self) -> CarbonPortfolio:
    pass
```

### Key Takeaways

We've seen that we can relax the assumption that carbon risk is not priced in by the market. Carbon risk seems to corresponds to a systematic risk, with the existence of a Brown-Minus-Green Factor. 

Stocks sentivities to the BMG factor can be integrated into a minimum variance framework, in order to hedge for carbon risk. This strategy is based on a marked-based measure of carbon risk.

Question remains regarding the returns associated the BMG factor. Indeed, returns should reward risk. With carbon risk, brown companies are significantly exposed to the risk. Then, investors should require higher returns to bear the risk with investment in brown companies. 

The thing is that the Carima's BMG factor provide significant negative returns. With historic returns, it seems that investors require higher returns from green companies than for brown companies. This doesn't make sense in a theoretical (and common sense) point of view. 

We will question the BMG factor puzzling result in the next part.