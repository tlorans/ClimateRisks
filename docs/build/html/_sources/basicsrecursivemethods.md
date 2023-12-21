# Basics Intuition for Characterizing the Equilibrium Conditions

The objective of this part is to give you the basics ideas behind the the process of finding equilibrium conditions of your model.

I advise you to take a look at [this excellent note from G.Fonseca](https://www.hetwebsite.net/het/fonseca/notes/fonseca_bellman.pdf).

This is a short version of McCandless (2008 {cite:p}`mccandless2008abcs`) examples for Recursive Deterministic Models. 

## Robison Crusoe Economy

In recursive approach, we separate the set of variables that we are using into state variables and control variables. 

In period $t$, the state variables are those whose values are already determined, either by our actions in the past or by some other process such as nature. 

Usually, for a growth model, the capital stock that we inherit from the past is considered a state variable. 

The control variables in period $t$ are those variables whose values individuals explicitly choose in that period with the goal of maximizing some objective function. We generally have the choice about which variables will be states and control variables.

Let's consider the simple version of a Robinson Crusoe Economy (that is a representative agent that is both the producer and the consumer). The objective function of Robison Crusoei is to maximize the discounted lifetime utility of consumption:

\begin{equation}
\begin{aligned}
\max & \sum^{\infty}_{i=0}\beta^i u(c_{t+i})\\
\end{aligned}
\end{equation}

where $\beta$ is a discount factor, $u(.)$ is the utility function and $c_{t}$ is the consumption level.

Robinson is subject to the budget constraints:

\begin{equation}
k_{t+1} = (1 - \delta) k_t + i_t
\end{equation}

And: 

\begin{equation}
y_t = f(k_t) = c_t + i_t
\end{equation}


where $k_{t}$ is the stock of capital, $i_t$ the amount of investment, $delta$ the capital depreciation rate, $y_t$ the output, $f()$ a production function.

In this model, the capital stock inherited from period $t-1$, $k_t$, is a state variable. It is predetermined and known. 

However, there is a number of options of choosing a control variable. One option could be for Robinson Crusoe to choose the consumption $c_t$, that appears directly in the objective function. Once consumption in period $t$ is determined, the second budget constraint determines the investment $i_t$, and the first budget constraint then determines the capital stock that will be available in the next period $t_{t+1}$. In this case, consumption is the control variable.

An alternative is for Robinson Crusoe to choose the amount of capital that will be available in next period, $k_{t+1}$. In that case, we could combine both budget constraints as:

\begin{equation}
c_t = f(k_t) + (1 - \delta)k_t - k_{t-1}
\end{equation}

After substitution, the objective function is:


\begin{equation}
\begin{aligned}
\max & \sum^{\infty}_{i=0}\beta^i u(f(k_{t+i}) + (1 - \delta)k_{t+i} - k_{t + i-1})\\
\end{aligned}
\end{equation}

### The Value Function

Assume we can calculate the value of the discounted value of utility that an agent receive when that agent is maximizing the infinite horizon objective function subject to the budget constraints. In our case with fixed labor supply, this value is clearly a function of the initial per worker capital stock $k_t$. As shown previously, we can write out a version of this problem where Robinson is using the capital stock to be carried over to the next period $k_{t+1}$, as the control variable. For that example, the value of utility is equal to:

\begin{equation}
V(k_t) = \max_{\{k_s\}^{\infty}_{s = t+1}} \sum^{\infty}_{i=0} \beta^i u(f(k_{t+i})-k_{t+1+i} + (1 - \delta)k_{t+i})
\end{equation}

where we denote the value of the discounted utility by $V(k_t)$, to stress that it is a function of the value of the initial capital stock $k_t$. For any value of $k_t$, limited to the approapriate domain, the value of the value function $V(k_t)$, is the discounted value of utility when the maximization problem has been solved and when $k_t$ was the initial capital stock.

Since $V(k_t)$ is a function, its value can be found for any permitted value of $k_t$. In particular, the value of the function can be found for the value of $k_{t+1}$ that was chosen in period $t$. This is possible because the economy is recursive: in period $t+1$, the value of $k_{t+1}$ is given (it is a state variable) and the problem to be solved is simply the maximization of utility beginning in period $t+1$. The maximization problem can be written as:

\begin{equation}
V(k_{t+1}) = \max_{\{k_s\}^{\infty}_{s = t+2}} \sum^{\infty}_{i=0} \beta^i u(f(k_{t+1+i})-k_{t+2+i} + (1 - \delta)k_{t+1+i})
\end{equation}

and its value, $V(k_{t+1})$, is a function of the stock of capital per worker at time $t+1$.

By separating the period $t$ problem from that of future periods, we can rewrite the value function $V(k_t)$ as:

\begin{equation}
V(k_t) = \max_{k_{t+1}}[u(f(k_t) - k_{t+1} + (1 - \delta)k_t) + \max_{\{k_s\}^{\infty}_{s = t+2}} \sum^{\infty}_{i=0} \beta^i u(f(k_{t+1+i})-k_{t+2+i} + (1 - \delta)k_{t+1+i})]
\end{equation}

The summation in the last part of this equation is simply the value function $V(k_{t+1})$. We can thus make the substition and write:

\begin{equation}
V(k_t) = \max_{k_{t+1}}[u(f(k_t) - k_{t+1} + (1 - \delta)k_t) + \beta V(k_{t+1})]
\end{equation}

An equation of this form is known as a Bellman equation. Writing out the problem recursively makes it conceptually simpler. The value of the choice variable $k_{t+1}$ is being chosen to maximize an objective function of only a single period. The problem is reduced from one of infinite dimension to one of only one dimension.

However, this simplification comes at a cost. The problem is now one where both the time $t$ one-period problem $u(f(k_t) - k_{t+1} + (1 - \delta)k_t)$ and the discounted value function evaluated at $k_{t+1}$, $\beta V(k_{t+1})$ are included. The complication is that the value of the function $V(k_{t+1})$ evaluated at $k_{t+1}$ is not known. If it where known, then the value of the function $V(k_t)$ would also be known as it is the same function. We will illustrate this issue and how to overcome it in the next subsection.

### Equilibrium Conditions

We assume that the value function $V(.)$ exists and has a first derivative. We can then proceed by taking the derivative of $V(k_t)$ with respect to our control variable $k_{t+1}$.

Let's do it with SymPy:

```Python
import sympy as smp

t = smp.symbols('t', cls = smp.Idx)

K = smp.IndexedBase('k')
C = smp.IndexedBase('c')
I = smp.IndexedBase('i')

delta  =smp.symbols('delta')
beta = smp.symbols('beta')

f = smp.Function('f')(K[t])

# budget constraint
resource_constraint = smp.Eq(f, C[t] + I[t])
transition_equation = smp.Eq(K[t+1], (1 - delta)*K[t] + I[t])

u = smp.Function('u')(C[t])

V = smp.Function('V')

# reexpress consumption in function of your control variable
resource_constraint = smp.Eq(I[t], smp.solve(resource_constraint, I[t])[0])
transition_equation = transition_equation.subs(resource_constraint.lhs, resource_constraint.rhs)
transition_equation = smp.Eq(C[t], smp.solve(transition_equation, C[t])[0])
utility_function = u.subs(transition_equation.lhs, transition_equation.rhs)

bellman = smp.Eq(V(K[t]), utility_function + beta * V(K[t+1]))

FOC = smp.Eq(smp.diff(bellman.rhs, K[t+1]), 0)
```
$\beta \frac{\partial}{\partial {k}_{t + 1}} V{\left({k}_{t + 1} \right)} - \left. \frac{d}{d \xi_{1}} u{\left(\xi_{1} \right)} \right|_{\substack{ \xi_{1}=- \delta {k}_{t} + f{\left({k}_{t} \right)} - {k}_{t + 1} + {k}_{t} }} = 0$

It seems we do not have progressed very far. The first-orer condition contains $V'(k_{t+1})$, the derivative of the function $V()$ evaluated at $k_{t+1}$. This is inconvenient since we need to know the derivative of $V()$ to be able to determine the same function $V()$. We do not know that derivative.

Under certain conditions, one can find the derivative of $V()$ simply by taking the partial derivative of the value function with respect to the state variable $k_t$. Theorems that provide the sufficient conditions for getting a derivative and that tell us how to find it are called envelope theorems (Benveniste and Scheinkman, 1979 {cite:p}`benveniste1979differentiability`, Milgrom and Segal, 2002 {cite:p}`milgrom2002envelope`).

Let's take this partial derivative, evaluated at $k_{t+1}$:

```Python
BS = smp.Eq(smp.diff(V(K[t]), K[t]), smp.diff(bellman.rhs, K[t])).subs(t, t+1)
```

$\frac{\partial}{\partial {k}_{t + 1}} V{\left({k}_{t + 1} \right)} = \left(- \delta + \frac{\partial}{\partial {k}_{t + 1}} f{\left({k}_{t + 1} \right)} + 1\right) \left. \frac{d}{d \xi_{1}} u{\left(\xi_{1} \right)} \right|_{\substack{ \xi_{1}=- \delta {k}_{t + 1} + f{\left({k}_{t + 1} \right)} + {k}_{t + 1} - {k}_{t + 2} }}$

We can now plug this definition of the derivative evaluated at $k_{t+1}$ into the first-order condition to get an Euler equation of:

```Python
Euler = FOC.subs(BS.lhs, BS.rhs)
Euler = Euler.subs(transition_equation.rhs, transition_equation.lhs)
Euler = Euler.subs(transition_equation.rhs.subs(t, t+1), transition_equation.lhs.subs(t, t+1))
print(smp.latex(Euler.simplify()))
```

$\beta \left(- \delta + \frac{\partial}{\partial {k}_{t + 1}} f{\left({k}_{t + 1} \right)} + 1\right) \frac{\partial}{\partial {c}_{t + 1}} u{\left({c}_{t + 1} \right)} - \frac{\partial}{\partial {c}_{t}} u{\left({c}_{t} \right)} = 0$

which can be reexpressed as:

\begin{equation}
\frac{u'(c_t)}{u'(c_{t+1})} = \beta (f'(k_{t+1})+ (1 - \delta))
\end{equation}

The equilibrium conditions of the Robinson Crusoe Economy are thus this Euler equation and the budget constraints:

\begin{equation}
\frac{u'(c_t)}{u'(c_{t+1})} = \beta (f'(k_{t+1})+ (1 - \delta))
\end{equation}

\begin{equation}
k_{t+1} = (1 - \delta) k_t + i_t
\end{equation}

\begin{equation}
y_t = f(k_t) = c_t + i_t
\end{equation}


## Robinson Crusoe with Variable Labor

### The Value Function

### Optimizing

### Equilibrium Conditions