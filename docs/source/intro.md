# Introduction: Climate Risk & Equity Investing

## Economics and Physics of Climate Risk

### Economics and Climate Risk

We start with the economics settings of the DICE 2013 model (Nordhaus and Sztorc, 2013). The gross production $Y(t)$ is given by a standard Cobb-Douglas function:

\begin{equation}
Y(t) = A(t)K(t)^{\gamma}L(t)^{1 - \gamma}
\end{equation}

with $A(t)$ the total productivity factor (or technological progress), $K(t)$ the capital input, $L(t)$ the labor input and $\gamma \in ]0,1[$ measures the elasticity of the capital factor:

\begin{equation}
\gamma = \frac{\partial ln Y(t)}{\partial ln K (t)} = \frac{\partial Y(t)}{\partial K(t)} \frac{K(t)}{Y(t)}
\end{equation}

In the Integrated Assessment Model (IAM), we have a distinction between the production $Y(t)$ and net output $Q(t)$ because climate risk generate losses:

\begin{equation}
Q(t) = \Omega_{climate}(t)Y(t) \leq Y(t)
\end{equation}

where $\Omega_{climate}(t) \in ]0,1[$ is the loss percentage of the production. 

$Q(t)$ is thus the net output when taking into account damages from climate change. 


### Physical Risk and Transition Risk

We've seen that the net output is reduced because of climate change. We have:

\begin{equation}
\Omega_{climate}(t) = \Omega_D(t)\Omega_{\Lambda}(t) = \frac{1}{1 + D(t)}(1 - \Lambda(t))
\end{equation}

with $D(t) \geq 0$ corresponds to the damage function (physical risk) and $\Lambda(t) \geq 0$ is the mitigation or abatement cost (transition risk).

The costs $D(t)$ or physical risk result from natural disasters and climatic events (wildfires, floods, storms, etc.). The costs $\Lambda(t)$ come from reducing GHG emissions and policiy for financing the transition to a low-carbon economy.

Nordhaus and Sztorc (2013) assume that $D(t)$ is a function of the atmospheric temperature $T_{AT}(t)$:

\begin{equation}
D(t) = \psi_1 T_{AT}(t) + \psi_2 T_{AT}(t)^2
\end{equation}

with $\psi_1 \geq 0$ and $\psi_2 \geq 0$ are two exogenous parameters. $T_{AT}(t)$ corresponds to the global mean surface tempature increase in °C from 1900.
We then have the fraction of net output lost because of global warming defined as:

\begin{equation}
\mathfrak{L}_D(t) = 1 - \Omega_D(t) = 1 - (1 + D(t))^{-1} 
\end{equation}

Various implementations of the damage function have been proposed in the literature. 


```{figure} damage_function.png
---
name: damage_function
---
Figure: Loss Function due to Climate Damage Costs (Roncalli, 2023)
```

The abatement cost function depends on the control variable $\mu(t)$:

\begin{equation}
\Lambda(t) = \theta_1(t)\mu(t)^{\theta_2}
\end{equation}

with $\theta_1 \geq 0$ and $\theta_2 \geq 0$ are two parameters, and $\mu(t) \in ]0,1[$ the emission-control rate.


```{figure} abatement_function.png
---
name: abatement_function
---
Figure: Abatement Cost Function (Roncalli, 2023)
```

We finally have the global impact of climate change as:

\begin{equation}
\Omega_{climate}(t) = \frac{1 - \theta_1(t)\mu(t)^{\theta_2}}{1 + \psi_1 T_{AT}(t) + \psi_2 T_{AT}(t)^2}
\end{equation}

### Global Warming

## Climate Risk Pricing in Equity Markets

### The Brown-Minus-Green Factor or an Unconventional Risk Pricing

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

During the last decade, it seems that the BMG factor returns were constantly negative, that is brown assets underperformed green assets. If we think about carbon risk as a systematic risk, this result is puzzling. We will tackle this question in the next sub-section (green assets outperformance).

### Green Assets Outperformance with Attention Shift

In the previous part, we've observed the puzzling results that green assets outperformed brown assets in the previous decade, according to the BMG negative returns.

However, as showed by the equilibrium model from Pastor et al. (2021) {cite:p}`pastor2021sustainable`, green assets should have lower expected returns than brown assets, because:
- some investors have green tastes, and then require lower returns for holding these assets (taste premium)
- greener assets are a better hedge against climate risks (risk premium)

So, how could we explain the negative returns from the BMG factor? Pastor et al. (2021) explain that green assets can have higher realized returns while agents' demand shift unexpectedly in the green direction. Investors' demand for green assets can incease unexpectedly, directly driving up green assets prices. Consumers' demand for green products can also unexpectedly strenghen, driving up green firms' profits and thus stock prices. Then, a transitory green factor, driven by investors' attention shift, can arise. 

Pastor et al. (2022) {cite:p}`pastor2022dissecting` explain the past green assets outperformance by the unanticipated increases in climate concerns, confirming the theoretical green factor portfolio from Pastor et al. (2021). 
The empirical framework for testing this is the following:
- Measuring the unanticipated climate concerns using the Media Climate Change Concerns Index (MCCC) from Ardia et al. (2020) {cite:p}`ardia2020climate`
- Using the new measure of the unanticipated climate concerns in a regression, and use the estimated parameters to build a counterfactual green factor returns, with climate shock equals to zero

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

## Key Takeaways

- Physical risk is expected to occur by the end of the century, while transition risk can occur during the next decade: this is the consequence of the tragedy of horizons. 

- Climate risk pricing is noisy, with a mixed between risk pricing and attention shift, resulting in differences between expected and realized returns in the past decade.