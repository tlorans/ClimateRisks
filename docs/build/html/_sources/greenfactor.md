## Green Factor

In the previous part, we've seen how exposure to the systematic carbon risk can be measured with carbon beta, thanks to the BMG factor from Gorgen et al. (2019) and how to hedge from carbon risk by introducing carbon beta into a minimum variance portfolio. We've observed the puzzling results that green assets outperformed brown assets in the previous decade, according to the BMG negative returns.

However, as showed by the equilibrium model from Pastor et al. (2021) {cite:p}`pastor2021sustainable`, green assets should have lower expected returns than brown assets, because:
- some investors have green tastes, and then require lower returns for holding these assets (taste premium)
- greener assets are a better hedge against climate risks (risk premium)

So, how could we explain the negative returns from the BMG factor? Pastor et al. (2021) explain that green assets can have higher realized returns while agents' demand shift unexpectedly in the green direction. Investors' demand for green assets can incease unexpectedly, directly driving up green assets prices. Consumers' demand for green products can also unexpectedly strenghen, driving up green firms' profits and thus stock prices.

Then, a transitory green factor, driven by investors' attention shift, can arise. In this part, we will follow Pastor et al. (2022) {cite:p}`pastor2022dissecting` and construct a green factor portfolio. 

### Green Stocks Outperformance: Realized vs. Expected Returns

Pastor et al. (2022) explain the past green assets outperformance by the unanticipated increases in climate concerns, confirming the theoretical green factor portfolio from Pastor et al. (2021). 
The empirical framework for testing this is the following:
- Measuring the unanticipated climate concerns using the Media Climate Change Concerns Index (MCCC) from Ardia et al. (2020) {cite:p}`ardia2020climate`
- Using the new measure of the unanticipated climate concerns in a regression, and use the estimated parameters to build a counterfactual green factor returns, with climate shock equals to zero

We will follow the same approach, explaining the differences between realized and expected returns.

#### Measuring Climate Concerns

To build a measure of unanticipated climate concerns shock, Pastor et al. (2022) use the MCCC from Ardia et al. (2021). This MCCC:
- aggregates news from eight major US newspapers
- captures the number of climate news stories each day and their negativity / focus on risk

```Python
# download and look at the index https://sentometrics-research.com/download/mccc/
```

Following Pastor et al. (2022), we will measure shocks to climate concerns as prediction errors from AR(1) models applied to the MCCC index. To compute the prediction error in month $t$, the steps are the followings:
- estimate an AR(1) model using the 36 months of MCCC data ending in month $t-1$
- set the prediction error to month $t$ level of MCCC minus the AR(1) model's prediction

More formally, given a climate change concerns at time $t$, $MCCC(t)$, we want to capture the unexpected shock as:

\begin{equation}
\Delta C(t) = \Delta MCCC(t) - \mathbb{E}[\Delta MCCC(t)|I(t-1)]
\end{equation}

Where $\Delta MCCC(t)$ is the change in climate change concerns at time $t$, $I(t-1)$ is the information set available at time $t$ and $\Delta C(t)$ is the climate change concerns shock.


```Python
# AR model
```

Let's plot the cumultative shocks to climate concerns:
```Python
#plot
```
#### Counterfactual

To assess whether climate concerns shocks $\Delta C (t)$ can explains green assets outperformance, Pastor et al. (2022) propose to build a counterfactual returns. 

The approach relies on the problem of inferring an asset's expected return $\mu = \mathbb[r(t)]$ using historical observations. The most common approach is to use the asset's sample average return, $\bar{r}$, as an estimate of $\mu$.

Pastor et al. (2022) propose another approach introducing the additional information from climate shocks. We can estimate the following regression:

\begin{equation}
R_{GMB}(t) = \alpha + \beta \Delta C(t) + u(t)
\end{equation}

Where $\alpha = \mu$ because $\Delta C(t)$ has zero mean ex ante and $R(t)$ is the monthly return of the Green-Minus-Brown portfolio.

```Python
# Perform the regression
```
Once the regression is performed, we can then build the counterfactual by adding the regression intercept $\hat{\alpha}$ plus the estimated residual.

```Python
# plot cumulative counterfactual returns
```

The counterfactual, with $\Delta C(t) = 0$ is close to zero. In fact, it turns to be negative in Pastor et al. (2022) when including other proxies for attention shift. 

### Constructing the Green Factor

The green factor was theoretically defined in a two-factors models by Pastor et al. (2021). The authors show that, along with the market factor, the green factor prices assets in equilibrium. 

In this part, we will construct a green factor, using stocks' greeness measure.

#### Measuring Greeness

Pastor et al. (2022) use MSCI Environmental scores to measure stocks' greeness. In our application, we will rather use the carbon intensity. 

We measure the relative greeness of each stock compared to the market portfolio, such as:

\begin{equation}
ci_i(t) = CI_i(t) - \bar{CI(t)} 
\end{equation}

Where $\bar{CI(t)} = b(t)^TCI(t)$ with $b$ the vector of market-capitalization weights and $CI$ the vector of carbon intensities. $\bar{CI(t)}$ corresponds to the weighted-average carbon intensity (WACI) of the market-capitalization portfolio.

```Python
import numpy as np


b = np.array([0.1, 0.2, 0.3, 0.4])

CI = np.array((1.45, 7.8, 2.3, 4.8))

waci = b.T @ CI

ci = CI - waci
```

Thus, we have:

\begin{equation}
b(t)^Tci(t) = 0
\end{equation}

```Python
print(b.T @ ci)
```
```
3.885780586188048e-16
```

Which is a condition imposed in the equilibrium model from Pastor et al. (2021).

#### The Green Factor

The green factor portfolio is then constructed with the weights defined by the relative greeness measure $ci(t-1)$. The green factor portfolio is a portfolio containing long positions in green stocks ($ci(t-1)>0$) and short positions in brown stocks ($ci(t-1)<0$).

```Python
# code to get the green factor portfolio
```


### Key Takeaways






