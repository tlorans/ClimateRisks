# Part 3: ... to Asset Pricing Models

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

## Equilibrium Conditions

We can state our problem in Python as before:

```Python
import sympy as smp

t = smp.symbols('t', cls = smp.Idx)

Z = smp.IndexedBase('z') # Shares
P = smp.IndexedBase('p') # price of shares
C = smp.IndexedBase('c') # consumption
D = smp.IndexedBase('d') # dividends
E = smp.IndexedBase('E') # expectation operator

beta = smp.symbols('beta')

resource_constraint = smp.Eq(Z[t+1]*P[t] + C[t], Z[t]*D[t] + Z[t]*P[t])

u = smp.Function('u')(C[t]) # utility function

V = smp.Function('V')

bellman = smp.Eq(V(Z[t], D[t]), u + beta * E[t] * V(Z[t+1], D[t+1]))
resource_constraint = smp.Eq(C[t], smp.solve(resource_constraint, C[t])[0])
bellman = bellman.subs(resource_constraint.lhs, resource_constraint.rhs)
```

We take the first-order condition with respect to our control variable $z_{t+1}$

```Python
FOC = smp.Eq(smp.diff(bellman.rhs, Z[t+1]),0).subs(resource_constraint.rhs, resource_constraint.lhs).simplify()
```
$\beta \frac{\partial}{\partial {z}_{t + 1}} V{\left({z}_{t + 1},{d}_{t + 1} \right)} {E}_{t} - \frac{\partial}{\partial {c}_{t}} u{\left({c}_{t} \right)} {p}_{t} = 0$

As we have taken care of the choice of our control variable, the Benveniste-Scheinkman condition gives a convenient expression:

```Python
BS = smp.Eq(smp.diff(V(Z[t], D[t]), Z[t]), smp.diff(bellman.rhs, Z[t])).subs(resource_constraint.rhs, resource_constraint.lhs).simplify().subs(t, t+1)
```

$\frac{\partial}{\partial {z}_{t + 1}} V{\left({z}_{t + 1},{d}_{t + 1} \right)} = \left({d}_{t + 1} + {p}_{t + 1}\right) \frac{\partial}{\partial {c}_{t + 1}} u{\left({c}_{t + 1} \right)}$

We can plug it into the initial FOC to obtain the Euler equation:

```Python
Euler = FOC.subs(BS.lhs, BS.rhs)
```

$\beta \left({d}_{t + 1} + {p}_{t + 1}\right) \frac{\partial}{\partial {c}_{t + 1}} u{\left({c}_{t + 1} \right)} {E}_{t} - \frac{\partial}{\partial {c}_{t}} u{\left({c}_{t} \right)} {p}_{t} = 0$

Which can be reexpressed as:

\begin{equation}
p_tu'(c_t) = \beta \mathbb{E}_t[(p_{t+1}+d_{t+1})u'(c_{t+1})]
\end{equation}

The Euler equation has an intuitive interpretation. The left

## Consumption CAPM

## Equity Premium Puzzle