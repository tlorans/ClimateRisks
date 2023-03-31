## Green Factor

In the previous part, we've seen how exposure to the systematic carbon risk can be measured with carbon beta, thanks to the BMG factor from Gorgen et al. (2019) and how to hedge from carbon risk by introducing carbon beta into a minimum variance portfolio. We've observed the puzzling results that green assets outperformed brown assets in the previous decade, according to the BMG negative returns.

However, as showed by the equilibrium model from Pastor et al. (2021) {cite:p}`pastor2021sustainable`, green assets should have lower expected returns than brown assets, because:
- some investors have green tastes, and then require lower returns for holding these assets (taste premium)
- greener assets are a better hedge against climate risks (risk premium)

So, how could we explain the negative returns from the BMG factor? Pastor et al. (2021) explain that green assets can have higher realized returns while agents' demand shift unexpectedly in the green direction. Investors' demand for green assets can incease unexpectedly, directly driving up green assets prices. Consumers' demand for green products can also unexpectedly strenghen, driving up green firms' profits and thus stock prices.

Then, a transitory green factor, driven by attention shift, can arise. In this part, we will follow Pastor et al. (2022) {cite:p}`pastor2022dissecting` and construct a green factor portfolio. This green factor portolio potentially benefits from the investors' attention shift.

### Green Stocks Outperformance: Realized vs. Expected Returns

Pastor et al. (2022) explain the past green assets outperformance by the unanticipated increases in climate concerns, confirming the theoretical green factor portfolio from Pastor et al. (2021). 
The empirical framework for testing this is the following:
- Measure the unanticipated climate concerns using the Media Climate Change Concerns Index (MCCC) from Ardia et al. (2020) {cite:p}`ardia2020climate`
- Use the new measure of the unanticipated climate concerns in a regression, and use the estimated parameters to build a counterfactual green factor returns, with climate shock equals to zero

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

```Python
# AR model
```

Let's plot the cumultative shocks to climate concerns:
```Python
#plot
```
#### Counterfactual


### A Green Factor Portfolio


## Key Takeaways






