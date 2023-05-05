## Green Stocks Outperformance: Realized vs. Expected Returns

In the previous part, we've seen how exposure to the systematic carbon risk can be measured with carbon beta, thanks to the BMG factor from Gorgen et al. (2019) and how to hedge from carbon risk with an enhanced-index with carbon beta (Roncalli et al., 2020). We've observed the puzzling results that green assets outperformed brown assets in the previous decade, according to the BMG negative returns.

However, as showed by the equilibrium model from Pastor et al. (2021) {cite:p}`pastor2021sustainable`, green assets should have lower expected returns than brown assets, because:
- some investors have green tastes, and then require lower returns for holding these assets (taste premium)
- greener assets are a better hedge against climate risks (risk premium)

So, how could we explain the negative returns from the BMG factor? Pastor et al. (2021) explain that green assets can have higher realized returns while agents' demand shift unexpectedly in the green direction. Investors' demand for green assets can incease unexpectedly, directly driving up green assets prices. Consumers' demand for green products can also unexpectedly strenghen, driving up green firms' profits and thus stock prices.

Then, a transitory green factor, driven by investors' attention shift, can arise. In this part, we will follow Pastor et al. (2022) {cite:p}`pastor2022dissecting` to understand the outperformance of green assets in the 2010s. 

Pastor et al. (2022) explain the past green assets outperformance by the unanticipated increases in climate concerns, confirming the theoretical green factor portfolio from Pastor et al. (2021). 
The empirical framework for testing this is the following:
- Measuring the unanticipated climate concerns using the Media Climate Change Concerns Index (MCCC) from Ardia et al. (2020) {cite:p}`ardia2020climate`
- Using the new measure of the unanticipated climate concerns in a regression, and use the estimated parameters to build a counterfactual green factor returns, with climate shock equals to zero

### Measuring Climate Concerns

To build a measure of unanticipated climate concerns shock, Pastor et al. (2022) use the MCCC from Ardia et al. (2020). This MCCC:
- aggregates news from eight major US newspapers
- captures the number of climate news stories each day and their negativity / focus on risk

Let's have a look to the latest version of the MCCC from Ardia et al. (2022) {cite:p}`ardia2022climate`:
```Python
import pandas as pd
url = 'https://www.dropbox.com/scl/fi/uucc6401uje293ofc3ahq/Sentometrics_US_Media_Climate_Change_Index.xlsx?dl=1&rlkey=jvgb6xg9w4ctdz5cdl6qun5md'
mccc = pd.read_excel(url, sheet_name = "SSRN 2022 version (monthly)", header = 5)[['Date','Aggregate']]
mccc['Date'] = pd.to_datetime(mccc['Date'].astype(str)).dt.strftime('%Y-%m')
mccc.index = mccc['Date']
mccc.plot(figsize = (12, 12), ylabel = "MCCC")
```

```{figure} mcc.png
---
name: mcc
---
Figure: MCCC (2022 version)
```

If the resulting index seems quite volatile, we can see an increasing trend in the 2010s.

Following Pastor et al. (2022), we will now measure shocks to climate concerns as prediction errors from AR(1) models applied to this MCCC index. To compute the prediction error in month $t$, the steps are the followings:
- we estimate an AR(1) model using the 36 months of MCCC data ending in month $t-1$
- we set the prediction error to month $t$ level of MCCC minus the AR(1) model's prediction

More formally, given a climate change concerns at time $t$, $MCCC(t)$, we want to capture the unexpected shock as:

\begin{equation}
CC(t) = MCCC(t) - \mathbb{E}[MCCC(t)|I(t-1)]
\end{equation}

Where $MCCC(t)$ is the climate change concerns at time $t$, $I(t-1)$ is the information set available at time $t$ and $CC(t)$ is the climate change concerns shock.

Let's compute the AR(1) model in Python and produce the predictions $\mathbb{E}[MCCC(t)|I(t-1)]$:
```Python
from statsmodels.tsa.ar_model import AutoReg

model = AutoReg(mccc['Aggregate'], lags=1)
model_fit = model.fit()
print('Coefficients: %s' % model_fit.params)

import numpy as np

preds = []
for t in range(0, len(mccc['Aggregate'])):
    if t < 36:
      pred = np.nan
    else:
      pred = model_fit.params[0] + np.sum(model_fit.params[1:]*mccc['Aggregate'][t-1:t].values[::-1])
    preds.append(pred)

mccc['Preds'] = preds
```

Let's now compute and plot the cumultative shocks to climate concerns:
```Python
mccc['Climate_Shock'] = mccc['Aggregate'] - mccc['Preds']
```

```{figure} climateshocks.png
---
name: climateshocks
---
Figure: Cumulative Climate Concern Shocks
```
### Counterfactual

To assess whether climate concerns shocks $CC(t)$ can explain green assets outperformance, Pastor et al. (2022) propose to build a counterfactual returns. 

The approach relies on the problem of inferring an asset's expected return $\mu = \mathbb{E}[r(t)]$. The most common approach is to use the asset's sample average return, $\bar{r}$, as an estimate of $\mu$.

Pastor et al. (2022) propose another approach, introducing the additional information from climate shocks. We can estimate the following regression:

\begin{equation}
R_{GMB}(t) = \alpha + \beta CC(t) + u(t)
\end{equation}

Where $\alpha = \mu$ because $CC(t)$ has zero mean ex ante and $R(t)$ is the monthly return of the Green-Minus-Brown portfolio.

Once the regression is performed, we can then build the counterfactual by adding the regression intercept $\hat{\alpha}$ plus the estimated residual.

The counterfactual, with $CC(t) = 0$ is close to zero according to Pastor et al. (2022) results:

```{figure} counterfactualreturns.png
---
name: counterfactualreturns
---
Figure: Cumulative counterfactual vs. realized GMB returns (Pastor et al., 2022)
```

### Key Takeaways

- We've seen in this part that realized returns for green assets have been higher than expected ones in 2010s, due to unanticipated increases in climate concerns.

- It is an illustration of the fact that measuring $\mathbb{E}[R]$ with recent average realized returns can be dangerous, especially with a sample period with a lot of shocks.




