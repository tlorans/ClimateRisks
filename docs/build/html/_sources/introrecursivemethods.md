# Characterizing the Equilibrium Conditions

The objective of this part is to give you the basics ideas behind the the process of finding equilibrium conditions of your model.

I advise you to take a look at [this excellent note from G.Fonseca](https://www.hetwebsite.net/het/fonseca/notes/fonseca_bellman.pdf).

This is a short version of McCandless (2008 {cite:p}`mccandless2008abcs`) examples for Recursive Deterministic and Stochastic Models Chapters. 

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

## The Art of Choosing the Control Variables

Our Robinson Crusoe economy could have been written with a different choice for the control variable. Let's keep in the state variabe to be the stock of capital $k_t$. But now let's try to choose the time $t$ consumption to be the control variable. In that case, we need to redefine the objective function and the budget constraints.

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

# we now want to express budget constraint with our control variable inside
resource_constraint = smp.Eq(I[t], smp.solve(resource_constraint, I[t])[0])
transition_equation = transition_equation.subs(resource_constraint.lhs, resource_constraint.rhs)
```

${k}_{t + 1} = \left(1 - \delta\right) {k}_{t} + f{\left({k}_{t} \right)} - {c}_{t}$

Writing out the model, we have the Bellman equation:

```Python
bellman = smp.Eq(V(K[t]), u + beta * V(transition_equation.rhs))
```

$V{\left({k}_{t} \right)} = \beta V{\left(\left(1 - \delta\right) {k}_{t} + f{\left({k}_{t} \right)} - {c}_{t} \right)} + u{\left({c}_{t} \right)}$

This version is less convenient than the previous version when we try to write out the condition from the Benveniste-Scheinkman envelope theorem. Indeed, if we write out the envelope theorem condition we get:

```Python
BS = smp.Eq(smp.diff(V(K[t]), K[t]), smp.diff(bellman.rhs, K[t]))
```

$\frac{\partial}{\partial {k}_{t}} V{\left({k}_{t} \right)} = \beta \left(- \delta + \frac{\partial}{\partial {k}_{t}} f{\left({k}_{t} \right)} + 1\right) \left. \frac{d}{d \xi_{1}} V{\left(\xi_{1} \right)} \right|_{\substack{ \xi_{1}=\left(1 - \delta\right) {k}_{t} + f{\left({k}_{t} \right)} - {c}_{t} }}$

And we have the derivative of the value function in terms of the derivative of the value function and some other terms, which is no improvement.

One of the important tricks of working with the Bellman equation is to write out the objective function and the budget constraint so one gets a convenient version of the envelope theorem, that is a version that is not expressed in terms of the derivative of the value function. 

In the previous example, the envelope theorem was convenient because the derivative of the value function $V(k_{t+1})$ with respect to the state variable $k_t$ was equal to $0$, such that we ended up with an envelope theorem condition that gave us an expression to be plugged in the initial first-order condition.

## Robinson Crusoe with Variable Labor

It might be useful to show that recursive methods can be applied to the Robison Crusoe economy, where labor is variable input.

The utility function of Robinson is now:

\begin{equation}
\sum^{\infty}_{t=0}\beta^iu(c_{t+i}, h_{t+i})
\end{equation}

which is maximized subject to the constraint:

\begin{equation}
k_{t+1} = (1 - \delta)k_t + i_t
\end{equation}

\begin{equation}
y_t = f(k_t, h_t) \geq c_t + i_t
\end{equation}

\begin{equation}
h_t \leq 1
\end{equation}

### The Value Function

We choose $h_t$ and $k_{t+1}$ as our control variables. The problem can be written as the Bellman equation:

\begin{equation}
V(k_t) = \max_{h_t, k_{t+1}}[u(f(k_t, h_t) + (1 - \delta)k_t - k_{t+1}, h_t) + \beta V(k_{t+1})]
\end{equation}

Here we know that the envelope theorem condition has a simple representation because the derivative of $V(k_{t+1})$ with respect to the state variable $k_t$ will be equal to zero.

### Equilibrium Conditions

There are now two first-order conditions since there are two controls, $h_t$ and $k_{t+1}$:

```Python
import sympy as smp

t = smp.symbols('t', cls = smp.Idx)

K = smp.IndexedBase('k')
C = smp.IndexedBase('c')
H = smp.IndexedBase('h')
I = smp.IndexedBase('i')

delta = smp.symbols('delta')
beta = smp.symbols('beta')

f = smp.Function('f')(K[t], H[t])
u = smp.Function('u')(C[t], H[t])
resource_constraint = smp.Eq(f, I[t] + C[t])
transition_equation = smp.Eq(K[t+1], (1 - delta) * K[t] + I[t])

V = smp.Function('V')

# reexpress C_t to make appear the control variable Kt+1
resource_constraint = smp.Eq(C[t], smp.solve(resource_constraint, C[t])[0])
transition_equation = smp.Eq(I[t], smp.solve(transition_equation, I[t])[0])
resource_constraint = resource_constraint.subs(transition_equation.lhs, transition_equation.rhs)
bellman = smp.Eq(V(K[t]), u.subs(resource_constraint.lhs, resource_constraint.rhs) + beta * V(K[t+1]))


FOC_1 = smp.Eq(smp.diff(bellman.rhs, K[t+1]),0).subs(resource_constraint.rhs, resource_constraint.lhs).simplify()
FOC_2 = smp.Eq(smp.diff(bellman.rhs, H[t]), 0).subs(resource_constraint.rhs, resource_constraint.lhs).simplify()
```
The FOC for $k_{t+1}$:

$\beta \frac{\partial}{\partial {k}_{t + 1}} V{\left({k}_{t + 1} \right)} - \frac{\partial}{\partial {c}_{t}} u{\left({c}_{t},{h}_{t} \right)} = 0
$ 

The FOC for $h_t$:

$\frac{\partial}{\partial {h}_{t}} f{\left({k}_{t},{h}_{t} \right)} \frac{\partial}{\partial {c}_{t}} u{\left({c}_{t},{h}_{t} \right)} + \frac{\partial}{\partial {h}_{t}} u{\left({c}_{t},{h}_{t} \right)} = 0
$

The derivative of the value function only appear in the FOC for $k_{t+1}$. Thus we will only need the envelope condition in order to find the Euler Equation for $k_{t+1}$. The Euler Equation for $h_t$ has directly been found with the FOC, which can be reexpressed as:

\begin{equation}
\frac{u_h(c_t, h_t)}{u_c(c_t, h_t)} = - f_h(k_t, h_t)
\end{equation}

We find the envelope condition:

```Python
BS_K = smp.Eq(smp.diff(V(K[t]), K[t]), smp.diff(bellman.rhs, K[t])).subs(resource_constraint.rhs, resource_constraint.lhs).subs(t, t+1).simplify()
```

$\frac{\partial}{\partial {k}_{t + 1}} V{\left({k}_{t + 1} \right)} = \left(- \delta + \frac{\partial}{\partial {k}_{t + 1}} f{\left({k}_{t + 1},{h}_{t + 1} \right)} + 1\right) \frac{\partial}{\partial {c}_{t + 1}} u{\left({c}_{t + 1},{h}_{t + 1} \right)}$

We can plug it into the FOC for $k_{t+1}$ in order to get the Euler Equation:

```Python
Euler_1 = FOC_1.subs(BS_K.lhs, BS_K.rhs)
```

$\beta \left(- \delta + \frac{\partial}{\partial {k}_{t + 1}} f{\left({k}_{t + 1},{h}_{t + 1} \right)} + 1\right) \frac{\partial}{\partial {c}_{t + 1}} u{\left({c}_{t + 1},{h}_{t + 1} \right)} - \frac{\partial}{\partial {c}_{t}} u{\left({c}_{t},{h}_{t} \right)} = 0$

Which can be reexpressed:

\begin{equation}
\frac{u_c(c_t, h_t)}{u_c(c_{t+1}, h_{t+1})} = \beta (f_k(k_{t+1}, h_{t+1})+ (1 - \delta))
\end{equation}


The equilibrium conditions of the Robinson Crusoe Economy are thus these Euler equations and the budget constraints:


\begin{equation}
\frac{u_h(c_t, h_t)}{u_c(c_t, h_t)} = - f_h(k_t, h_t)
\end{equation}

\begin{equation}
\frac{u_c(c_t, h_t)}{u_c(c_{t+1}, h_{t+1})} = \beta (f_k(k_{t+1}, h_{t+1})+ (1 - \delta))
\end{equation}

\begin{equation}
k_{t+1} = (1 - \delta) k_t + i_t
\end{equation}

\begin{equation}
y_t = f(k_t, h_t) = c_t + i_t
\end{equation}

## Stochastic Case

Up to this point, our models have been deterministic. The values of all of the parameters of the models and the form of the functions are known with certinty. Given some initial condition, these economies follow a prescribed path.

Models are approximations of reality and being approximations are at least partially false. The predictions that a model makes, even a very good and very complete model, will not coincide with what occurs. This failure of models to predict perfectly comes from two potential sources.

One source of this failure to predict perfectly is that these are variables that are not included in the model but that impact on the values of the variables included. Our simple model of a deterministic Robison Crusoe economy tells us how the decisions about how much to save and how much to work affect the amount of output in the economy but does not account for how the economy responds to external shocks. Under this logic, if a model were sufficiently rich, it would be able to predict future outcomes with very great accuracy. However, our capacity to collect information and to construct, to test and to solve models is limited.

Since we know we can't include everything in a model, one way to handle that which we cannot include is to allow the model to be stochastic. We simply let some part of the model, the value of some parameters in each period, for example, be determined by "nature", where nature embodies everything that is not in our model.

A second source may be that the universe is simply naturally stochastic and there are things that we cannot predic with absolute certainty even if we have full information about the current state of the universe.

Whatever its source, for an economist it is convenient to assume that the world is stochastic and that the way the randomness intrudes in our models can be described by probabilities. Adding a little randomness goes a long way in helping the predictions of our models better match the data that we observe.

### Probability 

Before discussing models with stochastic shocks, it is worth taking some time to briefly define exactly what is meant by probability and by a probability space. A probability space $(\Omega, \mathcal{F}, P)$ is comprised of three elements:
- $\Omega$ a set that contains all the states of nature that might occur;
- $\mathcal{F}$ a collection of subset of $\Omega$, where each subset is called an event;
- $P$ a probability measure over $\mathcal{F}$

First, consider what this means when $\Omega$ is a finite set of possible states of nature. For example, it might contain just two possible values for technology, $A_1$ and $A_2$. Then a natural way to define $\mathcal{F}$ is with four elements:
- the empty set $[]$
- $A_1$
- $A_2$
- the set $[A_1, A_2]$

A probability measure for these four sets is:
- $0$ for the empty set
- some value $0 \leq p_1 \leq 1$ for $A_1$
- $p_2 = 1 - p_1$ for $A_2$
- $1$ for the set $[A_1, A_2]$

This says that either $A_1$ or $A_2$ will occur and, for a large enough sample, $A_1$ will occur with frequency $p_1$. For larger finite sets of possible states of nature, the structure is the same, but there are simply more elements to $\mathcal{F}$.

If $\Omega$ were comprised of three elements, $A_1 = 0.9$, $A_2 = 1.05$ and $A_3 = 1.10$, then, in addition to the sets given above, $\mathcal{F}$ would include:
- $A_3$
- $[A_1, A_3]$
- $[A_2, A_3]$
- $[A_1, A_2, A_3]$

The event $[A_2, A_3]$ contains all possible technology levels greater than 1 and occurs with probability $p_2 + p_3$.

It may seem like one goes to too much trouble with defining $\mathcal{F}$, the set of subsets of $\Omega$, and then probabilities over this subset. In the finite case, with independent underlying events, one can frequently simply define the probability measure over the elements of $\Omega$. Each underlying event has its probability, and the probability of any subset of these events is found by summing the probabilities of the events that make up the subsets.

When the set of possible states of nature is continuous, then the definition is more useful. Consider a growth model where technology, $A_t$, can take on any value in the set $[0.9, 1.2]$, the closed continuous set of values between $0.9$ and $1.2$, that includes the end points. Suppose that the probability distribution is uniform, so that, in some sense, any value is equally as likely as any other inside the set. In this case, the probability that ins some given period $t$, $A_t = 1.15565$ for example, is zero. With a uniform distribution, or any continuous distribution, for that matter, the probability that technology has any specific value in any specific period is always zero.

It is in this case that defining subsets of $[0.9, 1.2]$ becomes useful. Imagine that we want to know the probability that technology will have a value in period $t$ between $0.97$ and $1.03$. Since this is a uniform distribution, this probability can be calculated as $(1.03 - 0.97)/(1.2 - 0.9) = 0.2$ or 20%. Although the probability of any one value occuring for $A_t$ is always zero in this example, for any positive range of values, one can usually find a positive probability. Therefore, by defining probabilities over subsets of the states of nature, the definition encompasses situations with a continuous range of possible states of nature.

### A Simple Stochastic Growth Model

### The Value Function

### Equilibrium Conditions