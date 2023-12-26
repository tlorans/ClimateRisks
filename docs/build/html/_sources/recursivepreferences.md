# Recursive Preferences

The observed level of risk premia and return volatility require a volatile SDF. In CCAPM model, we have seen something of the form:

\begin{equation}
e^{\gamma \sigma^2_g} 
\end{equation}

That requires high volatility of consumption growth ($\sigma^2_g$) or high risk aversion $\gamma$.

Another approach, to give more degree of freedoms with more parameters, is to relax assumption of time-separability utility, such that the marginal utility $u'(c_t)$ would depends on things besides current consumption. It allow to make $u'(c_t)$ much more volatilite than consumption growth. 

We are going to focus on the solution with Recursive Preferences. In that case, the marginal utility depends on expected future consumption, and not current consumption only.

## Drawbacks of Time-Additive Preferences

The assumption of time-additive preferences that we've used until now has no compelling theoretical justification. Its widespread use is based solely on mathematical convenience.

Unfortunately, this convenience comes at a cost. Indeed, time-additive / expected utility preferences impose several restrictions.

### Elasticity of Intertemporal Substition and Coefficient of Relative Risk Aversion

First, it implies that the Elasticity of Intertemporal Substitution (EIS) is the reciprocal of the Coefficient of Relative Risk Aversion (RRA). This is unsurprising as $\gamma$ is the only parameters describing preferences.


---
**NOTE**

We have already used the basic Constant Relative Risk Aversion form of utility function in our previous time-additive preferences model (CCAPM):

\begin{equation}
u(c) = \frac{c^{1-\gamma}}{1 - \gamma}
\end{equation}

The parameter $\gamma$ represents the relative risk aversion.

To see this, note that:

\begin{equation}
u'(c) = c^{-\gamma}
\end{equation}

\begin{equation}
u''(c) = -\gamma c^{-\gamma - 1}
\end{equation}

Using the definition of measure of relative risk aversion RRA and our particular utility function, we have:

\begin{equation}
RRA = -\frac{c u''(c)}{u'(c)} = \frac{-\gamma c^{-\gamma - 1}}{c^{-\gamma}} = \gamma
\end{equation}
---

It can be shown by starting with the Euler condition from household optimisation:

\begin{equation}
u'(c_t) = \beta (1 + r)u'(c_{t+1})
\end{equation}

which, with CRRA utility becomes:

\begin{equation}
c_t^{-\gamma} = \beta(1+r)c_{t+1}^{-\gamma}
\end{equation}

Rearranging:

\begin{equation}
(\frac{c_{t+1}}{c_t})^{\gamma} = \beta(1 + r)
\end{equation}

Taking the logs:

\begin{equation}
\ln(c_{t+1}/c_t) = \frac{1}{\gamma} \ln \beta + \frac{1}{\gamma} \ln (1 + r)
\end{equation}

And the approximation with $\ln(1 + r) \approx r$:

\begin{equation}
\ln(c_{t+1}/c_t) = \frac{1}{\gamma} \ln \beta + \frac{1}{\gamma} r
\end{equation}

Finally, applying the definition of the Elasticity of Intertemporal Substitution gives:

\begin{equation}
EIS = \frac{\partial \ln (c_{t+1}/c_t)}{\partial r} = \frac{1}{\gamma}
\end{equation}

This is an arbitrary restriction. Why should the willingness to substitue across dates (or smoothing the consumption across time measured by the EIS) be related to the willingness to substitue across states (risk aversion, measured with the RRA)?

This restriction is the fundamental cause of the Equity Premium Puzzle: we need a high $\gamma$ to explain the mean return on risky assets, but then this implies a very low EIS, which generates a very high risk-free rate.

### Timing of Resolution of Uncertainty

Time-additive / expected utility preferences imply an indifference to the timing of resolution of uncertainty. Consider the following 2 lotteries:

1. At time 0, a single coin is tossed. If it's Heads, then $c_t = H$ for all $t$. If it's Tails, then $c_t = T$ for all $t$.
2. At each date $t$, a coin will be tossed. If it's Heads, then $c_t = H$. If Tails, then $C_t = T$.

An agent with time-additive / expected utility preferences will be indifferent to these 2 lotteries, since the expectured utiltiy of both is:

\begin{equation}
\sum^{\infty}_{t=1} \beta^t[\frac{1}{2}u(H) + \frac{1}{2}u(T)]
\end{equation}

In the first lottery, uncertainty is resolved earlier... 

## Value Function with Recursive Preferences

Kreps and Porteus proposed to relax time-additivity by defining current utility recursively, using two distinct functions:

Epstein and Zin (1989, 1991 {cite:p}`epstein1991substitution`) 

## Euler Equation and Stochastic Discount Factor

## Pricing

Ec2021_Lecture9 slide 10

## Eliminating the Value Function from the Pricing Rules Altogether

A key advantage of the CCAPM is that it is based on observable data. In constrat, the ICAPM of Merton (1973) required observable proxies for the marginal value of wealth. 

In a sense, the EZ model combines the CCAPM and ICAPM. We must find observable proxies for the value function.

A first approach consists in relating the value function to the return on the market portfolio, defined as an asset that pays aggregate consumption as its dividend.



