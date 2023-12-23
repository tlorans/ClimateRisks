# The Equity Premium Puzzle

A famous paper that evaluated CCAPM in terms of its ability to account for average returns on stocks and bonds in the US is Mehra and Prescott (1985).

Their results are strikingly negative, in that they show that the CCAPM has great difficulty matching even the most basic aspects of the data.

But their paper has inspired an enormous amount of additional research, which continues today, directed at modifying or extending the model to improves its empirical performance.

To compare the CCAPM' predictions to US data, Mehra and Prescott began by modifying Lucas' Tree Model to allow fluctuations in consumption growth as opposed to consumption itself, reflecting the fact that in the US consumption follows an upward trend over time.

Mehra and Prescott assumed that consumption growth $\Delta c_{t+1}$ is log-normally distributed, meaning that the natural logarithm of $\Delta c_{t+1}$ is normally distributed. They also assumed that $\Delta c_{t+1}$ is independant and identically distributed (iid) over time, meaning that $\mu_{\Delta {c_{t_+1}}}$ and $\sigma^2_{\Delta {c_{t+1}}}$ are constant over time.

EQUILIBRIUM CONDITIONS $c_t = d_t$ () 

## Value Function

Let's now assume a functional form for the utility, namely a classic Constant Relative Risk Aversion (CRRA):

\begin{equation}
u(c_t) = \frac{c_t^{1-\gamma} - 1}{1 - \gamma}
\end{equation}

USE THE NOTE CRRA-UTILIY

## Euler Equation

BASED ON CRRA, Euler Equation with gross rate of consumption within

USE ch12slides

## Method of Undetermined Coefficients and Log-Normality

From slide 75 ch12slides

In general the Euler equation has a mathematical sructure similar to that of a differential equation.

With CRRA utility and iid consumption growth, we can use method of undetermined coefficients to find a solution for $P_t$ in terms of $C_t$ and $P_{t+1}$ in terms of $C_{t+1}$

## Asset Pricing


CONCLUSION:
With CRRA utility and iid, log-normal consumption growth, the CCAPM implies an equity premium that is positive and gets larger as either:
- $\sigma^{2}_{\Delta c_{t+1}}$
increases, to that aggregate risk increase
- $\gamma$ increases, so that investors become more risk averse

## Testing