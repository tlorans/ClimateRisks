# Part 2: Dynamic Asset Pricing

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

$\frac{\partial}{\partial {c}_{t}} u{\left({c}_{t} \right)} {p}_{t} = \beta \left({d}_{t + 1} + {p}_{t + 1}\right) \frac{\partial}{\partial {c}_{t + 1}} u{\left({c}_{t + 1} \right)}
$

Again, please note that we should have an expectation operator:

\begin{equation}
p_tu'(c_t) = \beta \mathbb{E}_t[(p_{t+1}+d_{t+1})u'(c_{t+1})]
\end{equation}

The Euler equation has an intuitive interpretation. The left-hand side gives the marginal utility (loss) to giving up a small amount of consumption, and using it to buy some of the asset at price $p_t$. The right-hand side gives the discounted expected marginal utility (gain) at date $t+1$ from having an increased amount of the asset: part of the utility gain comes from the expected resale value of the additional amount of the asset and part of it comes from the dividend which this additional amount of the asset brings. Thus, the Euler equation is simply saying that given prices $p_t$ and dividends $d_t$, agents will find it optimal to increase their demand of the asset if the expected future gains to doing so (ie. the RHS) are greater than the costs (ie. the LHS).
The Euler equation is also saying that the agents will find it optimal to decrease their demand of the assets whenever the costs in utility terms to buying an additional amount of the asset (i.e. the LHS) are greater than the expected future gains (the RHS). Taken together, that means that if agents are just indifferent between increasing and decreasing the amount of the asset which they demand, then they are already demanding the optimal amount of the asset.

## Asset Pricing

We can use the resulting Euler equation of our model to determines the amount by which the risky asset's expected return exceeds that of risk-free asset.

We can again reexpress the Euler:

```Python
Euler = smp.Eq(1, smp.solve(Euler, 1)[0])
```
$1 = \frac{\beta \left({d}_{t + 1} + {p}_{t + 1}\right) \frac{\partial}{\partial {c}_{t + 1}} u{\left({c}_{t + 1} \right)}}{\frac{\partial}{\partial {c}_{t}} u{\left({c}_{t} \right)} {p}_{t}}$

Let's define for secturity $j$:

\begin{equation}
r_{j,t+1} = \frac{p_{j,t+1} +d_{j,t+1}}{p_{j,t}}
\end{equation}

And the stochastic discount factor (SDF):

\begin{equation}
M_t = \beta \frac{u'(c_{t+1})}{u'(c_t)}
\end{equation}

We finally recall the formula:

\begin{equation}
Cov[A,B] = \mathbb{E}[AB] - \mathbb{E}[A]\mathbb{E}[B]
\end{equation}


We reformulate our Euler equation accordingly in Python:
```Python
import sympy as smp
from sympy import stats as stats

#Create variables as random symbols:
M = stats.rv.RandomSymbol('M') # SDF
R = stats.rv.RandomSymbol('R') # risky assets
R_0 = smp.symbols('R_f') # risk free

identity = smp.Eq(stats.Covariance(M,R),stats.Covariance(M,R).rewrite(stats.Expectation))

SDF = smp.Eq(M, beta * (smp.diff(u, C[t]).subs(t, t+1) / smp.diff(u,C[t])))
risk_price = smp.Eq(R, (P[t+1] + D[t+1]) / P[t])
Euler = Euler.subs(SDF.rhs, SDF.lhs).subs(risk_price.rhs, risk_price.lhs)
# we need a trick to introduce Expectation operator
Euler = Euler.subs(M*R, stats.Expectation(M*R))
```
$1 = \operatorname{E}\left[M R\right]$

Future price of risk-free asset is defined as:

\begin{equation}
r_{f,t} = \frac{1}{p_{0,t}}
\end{equation}

Then:

```Python
risk_free_euler = Euler.subs(R, R_0)
risk_free_euler = risk_free_euler.expand()
risk_free_euler = smp.Eq(R_0, smp.solve(risk_free_euler, R_0)[0])
```

$R_{f} = \operatorname{E}\left[M\right]^{-1}$

And for the risky assets we have:

```Python
identity = smp.Eq(Euler.rhs, smp.solve(identity, Euler.rhs)[0])
risky_euler = Euler.subs(identity.lhs, identity.rhs)
risky_euler = smp.Eq(risky_euler.lhs * risk_free_euler.rhs, risky_euler.rhs * risk_free_euler.rhs)

risky_euler = smp.Eq(stats.Expectation(R) - risk_free_euler.rhs, smp.solve(risky_euler, stats.Expectation(R))[0] - risk_free_euler.rhs)

risky_euler = risky_euler.subs(risk_free_euler.rhs, risk_free_euler.lhs)
```

$- R_{f} + \operatorname{E}\left[R\right] = - R_{f} \operatorname{Cov}\left(M, R\right)
$

Assets which have high returns when consumption is already high and marginal utility is low (and which have comparatively low returns when consumption is low and marginal utility is high) also have a high overall expected return: investors need to be compensated extra for holding an assets which doe not pay that much when they really need it.