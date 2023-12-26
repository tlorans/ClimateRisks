# The Consumption CAPM

REWRITE IT USING NOTATIONS AND EXPLANATIONS from Ch12 slides

While the previous part aim was to solve a consumption - physical assets allocation optimal path problem, one can use the same dynamic stochastic general equilibrium problem to focus on consumption - financial assets allocation optimal path. A special case is the Lucas Tree Model (Lucas, 1978 {cite:p}`lucas1978asset`).

## Lucas Tree Model

This is a special case of the infinite horizon, pure exchange economy with stochastic endowments. The model economy is given as follows:

- There is a large number of identical, infinitely lived agents each of whom maximizes lifetime expected utility

- There is an equal number of trees, $i = 1, ..., N$. Each agent starts life at time zero with one three. These trees are the only assets in the economy.

- At the beginning of period $t$, each tree $i$ yields a stochastic divident (or fruit) in the amount $d_{i,t}$ to its owner. The distribution of $d_{i,t}$ is identical for all trees. The process is known by the agents and the fruit is not storable.
- The market in the ownership of trees is perfectly competitive. In the equilibrium, asset prices clear the market. That is, total stock positions of all agents are equal to the aggregate number of shares.

## Value Function

Due to the assumption that all agents are identical with respecto to both preferences and enowments, we can work with a representative agent. The agents' economic activity in each period consists of trading shares, where a share represents a claim to the future stream of dividends.

We let $p_{i,t}$ be the price of tree $i$ in period $t$ (i.e., of a claim to the entire income stream $\{d_{i,t+\tau}\}^{\infty}_{\tau = 0}$), measured in terms of the consumption commodity, and $z_{i,t}$ the quantity of tree $i$ that the agent holds between $t$ and $t+1$. 

Our aim is to find $p_{i,t}$ as a function of the stochastic payofss, $\{d_{i,t+\tau}\}^{\infty}_{\tau = 0}$. Stated formally, the representative consume chooses $\{z_{1,t}, z_{2,t},...,z_{N,t};c_t\}^{\infty}_{t=0}$ to maximize:

\begin{equation}
E_t \sum^{\infty}_{s = t} \beta^{s-t}u(c_s)
\end{equation}

subjet to the budget constraint:

\begin{equation}
\sum^{N}_{i=0}z_{i,t+1}p_{i,t} + c_t \leq \sum^{N}_{i=0}z_{i,t}d_{i,t}+\sum^{N}_{i=0}z_{i,t}p_{i,t}
\end{equation}

The budget constraint has the following interpretation: the ownership of share $i$ at the beginning of period $t$, $z_{i,t}$, entitles the owner to receive dividend $d_{i,t}$ in period $t$ and to have the right to sell the ree at price $p_{i,t}$ in period $t$. Thus, the agent's source of funds in period $t$ are given by the sum of shares that the agent holds times their respective dividents $\sum^{N}_{i=0}z_{i,t}d_{i,t}$, plus the revenue of the sale of the shares at the prevailing prices $\sum^{N}_{i=0}z_{i,t}p_{i,t}$.
On the left hand side of the inequality we have got the agent's use of funds, saying that the proceedings are either consumed or spent for the number of shares the agent wants to hold in period $t+1$. 

For a market equilibrium, the quantities of each tree demanded must equal to the given supply, that is, the number of shares for each tree must sump up to one. Since there is only one agent, equilibrium implies that $z_{i,t} = 1$ for all $i,t$. In other words, there is no other agent in the economy with whom to trade. From the budget constraint, this implies that consumption of the representative agent must equal to output, which is the sum of dividends.

\begin{equation}
c_t \leq \sum^N_{i=0}d_{i,t}
\end{equation}

We can assume that there is only one tree. Thus, the representative agent maximizes:

\begin{equation}
E_t \sum^{\infty}_{s=t}\beta^{s-t}u(c_s)
\end{equation}

subject to the budget constraint:

\begin{equation}
z_{t+1}p_t + c_t \leq z_td_t +z_tp_t
\end{equation}

and market clearing conditions:

\begin{equation}
c_t = d_t
\end{equation}

This representative agent's problem can again being treated as a problem of dynamic optimization. 

With $z_{t+1}$ as our control variables and $z_t$ and $d_t$ as our states variables, the Bellman equatoin can be written as:

\begin{equation}
V(z_{t},d_{t}) = \max_{z_{t+1}}[u(c_t) + \beta \mathbb{E}[V(z_{t+1}, d_{t+1})]]
\end{equation}

Reexpressing the budget constraint and making the substitution we have:

\begin{equation}
V(z_{t},d_{t}) = \max_{z_{t+1}}[u(d_tz_t - p_tz_{t+1}+p_tz_t) + \beta \mathbb{E}[V(z_{t+1}, d_{t+1})]]
\end{equation}

## Euler Equation

We can state our problem in Python as before:

```Python
import sympy as smp

t = smp.symbols('t', cls = smp.Idx)

Z = smp.IndexedBase('z') # Shares
P = smp.IndexedBase('p') # price of shares
C = smp.IndexedBase('c') # consumption
D = smp.IndexedBase('d') # dividends

beta = smp.symbols('beta')

resource_constraint = smp.Eq(Z[t+1]*P[t] + C[t], Z[t]*D[t] + Z[t]*P[t])

u = smp.Function('u')(C[t]) # utility function

V = smp.Function('V')

bellman = smp.Eq(V(Z[t], D[t]), u + beta * V(Z[t+1], D[t+1]))
```

We take the first-order condition with respect to our control variable $z_{t+1}$

```Python
FOC = smp.Eq(smp.diff(bellman.rhs, Z[t+1]),0).subs(resource_constraint.rhs, resource_constraint.lhs).simplify()
```
$\beta \frac{\partial}{\partial {z}_{t + 1}} V{\left({z}_{t + 1},{d}_{t + 1} \right)} - \frac{\partial}{\partial {c}_{t}} u{\left({c}_{t} \right)} {p}_{t} = 0$

As we have taken care of the choice of our control variable, the Benveniste-Scheinkman condition gives a convenient expression:

```Python
BS = smp.Eq(smp.diff(V(Z[t], D[t]), Z[t]), smp.diff(bellman.rhs, Z[t])).subs(resource_constraint.rhs, resource_constraint.lhs).simplify().subs(t, t+1)
```

$\frac{\partial}{\partial {z}_{t + 1}} V{\left({z}_{t + 1},{d}_{t + 1} \right)} = \left({d}_{t + 1} + {p}_{t + 1}\right) \frac{\partial}{\partial {c}_{t + 1}} u{\left({c}_{t + 1} \right)}$

We can plug it into the initial FOC to obtain the Euler equation:

```Python
Euler = FOC.subs(BS.lhs, BS.rhs)

```

$\beta \left({d}_{t + 1} + {p}_{t + 1}\right) \frac{\partial}{\partial {c}_{t + 1}} u{\left({c}_{t + 1} \right)} - \frac{\partial}{\partial {c}_{t}} u{\left({c}_{t} \right)} {p}_{t} = 0
$

Again, please note that we should have an expectation operator:

\begin{equation}
p_tu'(c_t) = \beta \mathbb{E}_t[(p_{t+1}+d_{t+1})u'(c_{t+1})]
\end{equation}

The Euler equation has an intuitive interpretation. The left-hand side gives the marginal utility (loss) to giving up a small amount of consumption, and using it to buy some of the asset at price $p_t$. The right-hand side gives the discounted expected marginal utility (gain) at date $t+1$ from having an increased amount of the asset: part of the utility gain comes from the expected resale value of the additional amount of the asset and part of it comes from the dividend which this additional amount of the asset brings. Thus, the Euler equation is simply saying that given prices $p_t$ and dividends $d_t$, agents will find it optimal to increase their demand of the asset if the expected future gains to doing so (ie. the RHS) are greater than the costs (ie. the LHS).
The Euler equation is also saying that the agents will find it optimal to decrease their demand of the assets whenever the costs in utility terms to buying an additional amount of the asset (i.e. the LHS) are greater than the expected future gains (the RHS). Taken together, that means that if agents are just indifferent between increasing and decreasing the amount of the asset which they demand, then they are already demanding the optimal amount of the asset.

## Deriving the CCAPM

HOW TO PRICE RISK FREE, RISKY RETURNS
EULER EQUATION TO SDF

Although the Tree Model assumes there is only one asset, we can turn it into a more general model by introducing additional assets.

Let $R_{j,t+1}$ denote the gross return on asset $j$ between $t$ and $t+1$ and let $r_{j,t+1}$ be the associated net return, so that:

\begin{equation}
1 + r_{j,t+1} = R_{j,t+1}
\end{equation}

For shares in the tree, the gross return is:

\begin{equation}
R_{t+1} = \frac{d_{t+1} + p_{t+1}}{p_t}
\end{equation}

and the net return:

\begin{equation}
r_{t+1} = \frac{d_{t+1} + p_{t+1} - p_t}{p_t}
\end{equation}

More generally, our previously derived Euler equation implies that the return on any asset $j$ must satisfy:

\begin{equation}
u'(c_t) = \beta \mathbb{E}_t[u'(c_{t+1})R_{j,t+1}] = \beta \mathbb{E}_t[u'(c_{t+1})(1 + r_{j,t+1})]
\end{equation}

### Pricing the Risk-Free Asset

Consider first a riskless asset, like a bank account or a short-term Government bond, with return $r_{f,t+1}$ that is known at $t$. For this asset, the Euler equation:

\begin{equation}
u'(c_t) = \beta \mathbb{E}_t[u'(c_{t+1})R_{j,t+1}] = \beta \mathbb{E}_t[u'(c_{t+1})(1 + r_{f,t+1})]
\end{equation}

implies:

\begin{equation}
\frac{1}{1 + r_{f,t+1}} = \mathbb{E}_t[\frac{\beta u'(c_{t+1})}{u'(c_t)}]
\end{equation}

### Pricing a Risky Asset

Next, consider a risky asset. The Euler equation can be rewritten:

\begin{equation}
1 = \mathbb{E}_t[(\frac{\beta u'(c_{t+1})}{u'(c_t)})(1 + r_{j,t+1})]
\end{equation}

But what does this equation imply about $\mathbb{E}_t(r_{j,t+1}))$, the expected return on the risky asset?

---
**NOTE**

Recall that for any two random variables X and Y with $\mathbb{E}[X] = \mu_X$ and $\mathbb{E}[Y] = \mu_Y$, the covariance between $X$ and $Y$ is defined as:

\begin{equation}
Cov(X,Y) = \mathbb{E}[(X - \mu_x)(Y - \mu_Y)]
\end{equation}

This definition implies:

\begin{equation}
Cov(X,Y) = \mathbb{E}[XY] - \mathbb{E}[X]\mathbb{E}[Y]
\end{equation}

Or, equivalently:

\begin{equation}
\mathbb{E}[XY] = \mathbb{E}[X]\mathbb{E}[Y] + Cov(X,Y)
\end{equation}

---

With the simple definition of the expression of the expectation of a product of two random variables, the Euler equation can be rewritten as:

\begin{equation}
1 = \mathbb{E}[\frac{\beta u'(c_{t+1})}{u'(c_t)}] \mathbb{E}_t[1 + r_{j,t+1}] + Cov_t[\frac{\beta u'(c_{t+1})}{u'(c_t)}, r_{j,t+1}]
\end{equation}

Combining this equation with the price of a risk-free asset $\frac{1}{1 + r_{f,t+1}} = \mathbb{E}_t[\frac{\beta u'(c_{t+1})}{u'(c_t)}]$ we obtain:

\begin{equation}
1 = \frac{E_t(1 + r_{j,t+1})}{1 + r_{f,t+1}} + Cov_t[\frac{\beta u'(c_{t+1})}{u'(c_t)}, r_{j,t+1}]
\end{equation}

which implies:

\begin{equation}
1 + r_{f,t+1} = 1 + \mathbb{E}_t[r_{j,t+1}] + ( 1 + r_{f,t+1})Cov_t[\frac{\beta u'(c_{t+1})}{u'(c_t)}, r_{j,t+1}]
\end{equation}

and then:

\begin{equation}
\mathbb{E}_t(r_{j,t+1})-r_{f,t+1} = -(1 + r_{f,t+1})Cov_t[\frac{\beta u'(c_{t+1})}{u'(c_t)}, r_{j,t+1}]
\end{equation}

This equation look a lot like the equations from the CAPM. In fact, is has similar implications: The expected return on asset $j$ will be above the risk-free rate if the covariance between the actual return on asset $j$ and the repreentative investor's IMRS (or SDF) is negative.

If the utility function is concave, the investor's IMRS (or the SDF):

\begin{equation}
\frac{\beta u'(c_{t+1})}{u'(c_t)}
\end{equation}

will be high if $c_{t+1}$ is low relative to $c_t$ and low if $c_{t+1}$ is high relative to $c_t$.

Hene, the IMRS (or SDF) is inversely related to the business cycle: it is high during recessions and low during booms.

Then, our previous equation:

\begin{equation}
\mathbb{E}_t(r_{j,t+1})-r_{f,t+1} = -(1 + r_{f,t+1})Cov_t[\frac{\beta u'(c_{t+1})}{u'(c_t)}, r_{j,t+1}]
\end{equation}

Means that the risky asset, as the covariance between its return and the IMRS (or SDF) is negative (that is, the asset return is high during booms and low during recessions), it exposes investors to additional aggregate risk. In equilibrium, it must offer a higher expected return to compensate.

Conversely, the expected return on aset $j$ will be below the risk-free rate if the covariance between the actual return on asset $j$ and the investor's IMRS is positive: that is, if the asset return is high during recessions and low during booms.

This asset insures investors against aggregate risk. Its low expected return reflects the premium that investors are willing to pay to obtain this insurance.

Like the traditional CAPM, the CCAPM implies that assets offer higher expected returns only when they expose investors to additional aggregate risk. The CCAPM goes further, by explicitly linking aggregate risk to business cycle.


## Testing the CCAPM

A famous paper that evaluated CCAPM in terms of its ability to account for averager returns on stocks and bonds in the US is Rajnish Mehra and Edward Prescott: "The Equity Premium: A Puzzle" (1985). 

Mehra and Prescott's results are strikingly negative, in that they show that the CCAPM has great difficulty in matching even the most basic aspects of the data.

But their paper has inspired an enormous amount of additional research, which continues today, directed at modifying or extending the model to improves its empirical performance.

To compare the CCAPM's predictions to US data, Mehra and Prescott began by modifying Lucas' Tree model to allow for fluctuations in consumption growth as opposed to consumption itself, reflecting the fact in the US, consumption follows an upward trend over time.

They continued to assume that there is a single representative investor, with an infinite horizon and CRRA utility:

\begin{equation}
u(c) = \frac{c^{1-\gamma}- 1}{1 - \gamma}
\end{equation}


---
**NOTE**

We have previously worked without assuming a specific form to the utility function. 

Let's implement the corresponding Bellman's equation:

```Python
import sympy as smp

t = smp.symbols('t', cls = smp.Idx)

Z = smp.IndexedBase('z') # Shares
P = smp.IndexedBase('p') # price of shares
C = smp.IndexedBase('c') # consumption
D = smp.IndexedBase('d') # dividends

beta = smp.symbols('beta')
gamma = smp.symbols('gamma') # relative risk aversion

resource_constraint = smp.Eq(Z[t+1]*P[t] + C[t], Z[t]*D[t] + Z[t]*P[t])

u = smp.Function('u')(C[t]) # utility function

CRRA = smp.Eq(u,(C[t]**(1 - gamma)-1)/(1 - gamma))

V = smp.Function('V')

bellman = smp.Eq(V(Z[t], D[t]), CRRA.rhs + beta * V(Z[t+1], D[t+1]))
resource_constraint = smp.Eq(C[t], smp.solve(resource_constraint, C[t])[0])
bellman = bellman.subs(resource_constraint.lhs, resource_constraint.rhs)
```
$V{\left({z}_{t},{d}_{t} \right)} = \beta V{\left({z}_{t + 1},{d}_{t + 1} \right)} + \frac{\left({d}_{t} {z}_{t} - {p}_{t} {z}_{t + 1} + {p}_{t} {z}_{t}\right)^{1 - \gamma} - 1}{1 - \gamma}
$

We have the following first-order condition with respect to $z_{t+1}$:

```Python
FOC = smp.Eq(smp.diff(bellman.rhs, Z[t+1]),0).subs(resource_constraint.rhs, resource_constraint.lhs).simplify()
```
$\beta \frac{\partial}{\partial {z}_{t + 1}} V{\left({z}_{t + 1},{d}_{t + 1} \right)} - \frac{{c}_{t}^{1 - \gamma} {p}_{t}}{{c}_{t}} = 0$

The envelope condition is:

```Python
BS = smp.Eq(smp.diff(V(Z[t],D[t]), Z[t]), smp.diff(bellman.rhs, Z[t])).subs(resource_constraint.rhs, resource_constraint.lhs).simplify()
BS = BS.subs(t, t+1)
```
$\frac{\partial}{\partial {z}_{t + 1}} V{\left({z}_{t + 1},{d}_{t + 1} \right)} = \left({d}_{t + 1} + {p}_{t + 1}\right) {c}_{t + 1}^{- \gamma}$

Plugging it into the initial FOC and rearranging:

```Python
Euler = FOC.subs(BS.lhs, BS.rhs).simplify()
Euler = smp.Eq(P[t], smp.solve(Euler, P[t])[0])
```
${p}_{t} = \beta \left({d}_{t + 1} + {p}_{t + 1}\right) {c}_{t + 1}^{- \gamma} {c}_{t}^{\gamma}$

---

Which can be expressed, with the expectation operator:

\begin{equation}
p_t = \beta \mathbb{E}_t[(\frac{c_{t+1}}{c_t})^{-\gamma}(d_{t+1}+p_{t+1})]
\end{equation}

and rewritting with $G_{t+1} = \frac{c_{t+1}}{c_{t}}$, the gross rate of consumption growth between $t$ and $t+1$:

\begin{equation}
p_t = \beta \mathbb{E}_t[G_{t+1}^{-\gamma}(d_{t+1}+p_{t+1})]
\end{equation}

### Log-Normality Assumption

Mehras and Prescott assumed that consumption growth $G_{t+1}$ is log-normally distributed, meaning that the natural logarithm of $G_{t+1}$ is normally distributed, with:

\begin{equation}
\ln(G_{t+1}) \sim N(\mu_g, \sigma^2g)
\end{equation}

They also assumed that $G_{t+1}$ is idependent and identically distributed (iid) over time, so that the mean $\mu_g$ and variance $\sigma^2_g$ of the log of $G_{t+1}$ are constant over time.

Let denote $g_{t+1} = G_{t+1} -1$ the net rate of consumption growth.

The approximation:

\begin{equation}
\ln(G_{t+1}) = \ln(1 + g_{t+1}) \approx g_{t+1}
\end{equation}

show that, since $G_{t+1}$ is log-normally distributed, $\ln(G_{t+1})$ is normally distributed, and therefore $g_{t+1}$ is approximately normally distributed.

Since, by definition:

\begin{equation}
G_{t+1} = e^{\ln(G_{t+1})}
\end{equation}

Jensen's inequality implies that the mean and variance of $G_{t+1}$ can't be found simply by calculating $e^{\mu_g}$ and $e^{\sigma^2_g}$.

In particular, since the exponential function is convex:

\begin{equation}
\mathbb{E}[G_{t+1}] > e^{\mathbb{E}[ln(G_{t+1})]} = e^{\mu_g}
\end{equation}

In particular, if $G_{t+1}$ is log-normally distributed, with:

\begin{equation}
\ln{G_{t+1}} \sim N(\mu_g, \sigma^2_g)
\end{equation}

then

\begin{equation}
\mathbb{E}[G_{t+1}] = e^{\mu_g + \frac{1}{2} \sigma^2_g}
\end{equation}

where the $\frac{1}{2}\sigma^2_g$ is the "Jensen's inequality term". In addition:

\begin{equation}
\mathbb{E}[G_{t+1}^{\alpha}] = e^{\alpha\mu_g + \frac{1}{2} \sigma^2_g}
\end{equation}

for any value of $\alpha$.

### The Method of Undetermined Coefficients

In general the Euler equation has a mathematical structure similar to that of a differential equation. With CRRA utility and iid consumption growth, a guess-and-verify procedure (the method of undetermined coefficients) can be used to find the solution of $p_t$ in terms of $c_t$ and $p_{t+1}$ in terms of $c_{t+1}$.

In particular, you can conjecture that:

\begin{equation}
p_t = vc_t
\end{equation}

and 

\begin{equation}
p_{t+1} = vc_{t+1}
\end{equation}

Recall that in equilibrium, $c_t = d_t$, thus we can also write:

\begin{equation}
p_t = vd_t
\end{equation}

\begin{equation}
p_{t+1} = vd_{t+1}
\end{equation}


where $v$ is a constant to be determined.

Substitute these guesses into the Euler equation:

\begin{equation}
p_t = \beta \mathbb{E}_t[G_{t+1}^{-\gamma}(d_{t+1}-p_{t+1})]
\end{equation}

to obtain:

\begin{equation}
vc_t = \beta \mathbb{E}_t[G_{t+1}^{-\gamma}(c_{t+1} + v c_{t+1})]
\end{equation}

implies:

\begin{equation}
v = \beta \mathbb{E}_t[G_{t+1}^{-\gamma}(1 + v)(\frac{c_{t+1}}{c_t})]
\end{equation}

\begin{equation}
v = (1 + v) \beta * E_t (G_{t+1}^{1 - \gamma})
\end{equation}

and hence:

\begin{equation}
v = \frac{\beta \mathbb{E}_t(G_{t+1}^{1 - \gamma})}{1 - \beta  \mathbb{E}_t(G_{t+1}^{1 - \gamma})}
\end{equation}

which is constant since $\mathbb{E}_t(G_{t+1}^{1-\gamma})$ is constant over time when $G_{t+1}$ is iid.

### Pricing the Risk-Free Asset 

Now we are ready to address the question of how well the CCAPM fits the facts. 

Consider, first, the risk-free rate of return $r_{f,t+1}$, which satisfies:

\begin{equation}
1 = \beta \mathbb{E}_t[G_{t+1}^{-\gamma}(1 + r_{f,t+1})]
\end{equation}

or 

\begin{equation}
1 + r_{f,t+1} = \frac{1}{\beta \mathbb{E}_t(G_{t+1}^{-\gamma})}
\end{equation}

Since $\ln(G_{t+1}) \sim N(\mu_g, \sigma^2_g)$:

\begin{equation}
\mathbb{E}[G_{t+1}^{\alpha}] = e^{\alpha \mu_g + \frac{1}{2}\alpha^2\sigma^2_g}
\end{equation}

for any value of $\alpha$. In particular:

\begin{equation}
\mathbb{E}[G_{t+1}^{-\gamma}] = e^{-\gamma \mu_g + \frac{1}{2} \gamma^2 \sigma^2_g}
\end{equation}

Now we use the fact that:

\begin{equation}
\frac{1}{e^x} = e^{-x}
\end{equation}

To rewrite this last equation as:

\begin{equation}
\frac{1}{\mathbb{E}[G_{t+1}^{-\gamma}]} = e^{\gamma \mu_g - \frac{1}{2}\gamma^2\sigma^2_g}
\end{equation}

We substitute this last equation into our previous $1 + r_{f,t+1} = \frac{1}{\beta \mathbb{E}_t[G_{t+1}^{-\gamma}]}$ to obtain:

\begin{equation}
1 + r_{f,t+1} = (\frac{1}{\beta})e^{\gamma \mu_g - \frac{1}{2}\gamma^2 \sigma^2_g}
\end{equation}

This equation shows specifically how, according to the model, the risk-free rate depends on the preference parameters $\beta$ and $\gamma$ and the mean and variance $\mu_g$ and $\sigma^2_g$ of log consumption growth.

### Pricing a Risky Asset

We now consider the return $r_{e,t+1}$ on stocks (equities) which the CCAPM associates with the retunr on trees as:

\begin{equation}
1 + r_{e,t+1} = \frac{d_{t+1}+p_{t+1}}{p_t} = \frac{c_{t+1}+v c_{t+1}}{vc_{t+1}} = (\frac{1}{v} + 1)G_{t+1}
\end{equation}

implies:

\begin{equation}
\mathbb{E}_t(r_{e,t+1}) = (\frac{1}{v} +1) \mathbb{E}_t(G_{t+1}) - 1
\end{equation}

Using $v = \frac{\beta \mathbb{E}_t[G_{t+1}^{1-\gamma}]}{1 - \beta \mathbb{E}_t[G_{t+1}^{1-\gamma}]}$, we have:

\begin{equation}
\frac{1}{v} + 1 = \frac{1 - \beta \mathbb{E}_t[G_{t+1}^{1-\gamma}]}{\beta \mathbb{E}_t[G_{t+1}^{1-\gamma}]} + 1 = \frac{1}{\beta \mathbb{E}_t[G_{t+1}^{1 - \gamma}]}
\end{equation}

and hence:

\begin{equation}
\mathbb{E}_t[r_{e,t+1}] = (\frac{1}{v} + 1) \mathbb{E}_t[G_{t+1}] - 1
\end{equation}

implies:

\begin{equation}
1 + \mathbb{E}_t[r_{e,t+1}] = \frac{\mathbb{E}_t[G_{t+1}]}{\beta \mathbb{E}_t[G_{t+1}^{1-\gamma}]}
\end{equation}

Since $\ln(G_{t+1}) \sim N(\mu_g, \sigma^2_g)$, then we transform the numerator as:

\begin{equation}
\mathbb{E}_t[G_{t+1}] = e^{\mu_g + \frac{1}{2}\sigma^2_g}
\end{equation}

and in the denominator we have:

\begin{equation}
\mathbb{E}_t[G_{t+1}^{1 - \gamma}] = e^{(1 - \gamma) \mu_g + \frac{1}{2}(1 - \gamma)^2 \sigma^2_g}
\end{equation}

Therefore we have:

\begin{equation}
1 + \mathbb{E}_t[r_{e,t+1}] = \frac{e^{\mu_g + \frac{1}{2}\sigma^2_g}}{\beta e^{(1 - \gamma) \mu_g + \frac{1}{2}(1 - \gamma)^2 \sigma^2_g}}
\end{equation}

\begin{equation}
= (\frac{1}{\beta})e^{\mu_g + \frac{1}{2}\sigma^2_g}e^{-(1 - \gamma)\mu_g - \frac{1}{2}(1 - \gamma)^2 \sigma^2_g}
\end{equation}

Using $e^x e^y = e^{x+y}$, it simplifies to:

\begin{equation}
1 + \mathbb{E}_t[r_{e,t+1}] = (\frac{1}{\beta})e^{\gamma \mu_g + \frac{1}{2}\gamma^2\sigma^2_g}e^{\gamma \sigma^2_g}
\end{equation}

To interpret this result, recall that:

\begin{equation}
1 + r_{f,t+1} = (\frac{1}{\beta})e^{\gamma \mu_g - \frac{1}{2}\gamma^2\sigma^2_g}
\end{equation}

So we can combine both solutions to obtain something simpler:

\begin{equation}
1 + \mathbb{E}_t[r_{e,t+1}] = (1 + r_{f,t+1})e^{\gamma \sigma^2_g}
\end{equation}

implying:

\begin{equation}
\frac{1 + \mathbb{E}_t[r_{e,t+1}]}{1 + r_{f,t+1}} = e^{\gamma \sigma^2_g} > 1
\end{equation}

Thus, with CRRA utility and iid, log-normal consumption growth, the CCAPM implies an equity premium that is positive and gets larger as either:
1. $\sigma^2_g$ increases, so that aggregate risk increases
2. $\gamma$ increases, so that investors become more risk averse

