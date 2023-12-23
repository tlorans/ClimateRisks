# Hansen's RBC Model: Equilibrium Conditions

The objective is to apply the recursive methods to characterize the equilibrium conditions of the basic Hansen's RBC model. 

This part is inspired by the McCandless (2008 {cite:p}`mccandless2008abcs`) chapter 6.

## The Value Function

In a Robinson Crusoe type economy, the one agent maximizes the discounted utility function:

\begin{equation}
\max \sum^{\infty}_{t=0}\beta^t u(c_t, l_t)
\end{equation}

where $c_t$ is time $t$ consumption, and $l_t$ is time $t$ leisure, where $l = 1 - h_t$ and $h_t$ is time $t$ labor.

The specific utility function that we use is:

\begin{equation}
u(c_t, 1 - h_t) = \ln c_t + A ln ( 1 - h_t)
\end{equation}

with $ A > 0$. The production function is Cobb-Douglas with a stochastic technology:

\begin{equation}
f(\lambda_t, k_t, h_t) = \lambda_t k_t^{\theta}h_t^{1 - \theta}
\end{equation}

where $\lambda_t$ is a random technology variable that follows the process:

\begin{equation}
\lambda_{t+1} = \gamma \lambda_t + \epsilon_{t+1}
\end{equation}

for $0 < \gamma < 1$. The $\epsilon_t$ shocks are identically and independently distributed, are positive, bounded above, and have a mean of $1 - \gamma$. These assumptions imply that the mean of $\lambda_t$ is 1 and that output cannot go ne gative. Capital accumulation follows the process:

\begin{equation}
k_{t+1} = (1 - \delta) k_t + i_t
\end{equation}

and the feasability constraint is:

\begin{equation}
f(\lambda_t, k_t, h_t) \geq c_t + i_t
\end{equation}

for every period $t$.

The model can be written as a Bellman equation of the form:

\begin{equation}
V(k_t, \lambda_t) = \max_{c_t, h_t}[\ln c_t + A \ln(1 - h_t) + \beta \mathbb{E_t}[V(k_{t+1}, \lambda_{t+1})| \lambda_t]]
\end{equation}

subject to:

\begin{equation}
\lambda_t k_t^{\theta}h_t^{1-\theta} \geq c_t + i_t
\end{equation}

\begin{equation}
\lambda_{t+1} = \gamma \lambda_t + \epsilon_{t+1}
\end{equation}

\begin{equation}
k_{t+1} = (1 - \delta)k_t + i_t
\end{equation}

The expectations operator in the value function, $\mathbb{E_t}[V(k_{t+1}, \lambda_{t+1})|\lambda_t]$ indicates that expectations are conditional on te realization of $\lambda_t$, a fact that comes from the stochastic process for technology. With substitution, the Bellman becomes:

\begin{equation}
V(k_t, \lambda_t) = \max_{k_{t+1}, h_t}[\ln(\lambda_tk_t^{\theta}h_t^{1-\theta} + (1 - \delta)k_t - k_{t+1}) + A \ln(1 - h_t) + \beta \mathbb{E_t}[V(k_{t+1}, \lambda_{t+1})|\lambda_t]]
\end{equation}

with $k_{t+1}$ and $h_t$ as the control variables.

## Equilibrium Conditions

Let's prepare the Bellman equation in Python:

```Python
import sympy as smp

t = smp.symbols('t', cls = smp.Idx)

K = smp.IndexedBase('k')
C = smp.IndexedBase('c')
L = smp.IndexedBase('l')
H = smp.IndexedBase('h')
I = smp.IndexedBase('i')
Techno = smp.IndexedBase('lambda')
epsilon = smp.IndexedBase('epsilon')
E = smp.IndexedBase('E')

A = smp.symbols('A')
beta = smp.symbols('beta')
theta = smp.symbols('theta')
gamma = smp.symbols('gamma')
delta = smp.symbols('delta')

V = smp.Function('V')
u = smp.Function('u')(C[t],1-H[t])
utility_function = smp.Eq(u, smp.log(C[t]) + A * smp.log(1 - H[t]))
f = smp.Function('f')(Techno[t], K[t], H[t])
production_function = smp.Eq(f, Techno[t] * K[t]**(theta)*H[t]**(1-theta))
techno_process = smp.Eq(Techno[t+1], gamma * Techno[t] + epsilon[t+1])
transition_equation = smp.Eq(K[t+1], (1 - delta)*K[t] + I[t])
resource_constraint = smp.Eq(f, C[t] + I[t])

# as before, we want to express C[t] in the utility function interms of our control variable Kt+1
resource_constraint = smp.Eq(I[t], smp.solve(resource_constraint, I[t])[0])
transition_equation = transition_equation.subs(resource_constraint.lhs, resource_constraint.rhs)
transition_equation = smp.Eq(C[t], smp.solve(transition_equation, C[t])[0])
transition_equation = transition_equation.subs(production_function.lhs, production_function.rhs)

bellman = smp.Eq(V(K[t], Techno[t]), utility_function.rhs.subs(transition_equation.lhs, transition_equation.rhs) + beta * E[t] * V(K[t+1], Techno[t+1]))
```

The first order conditions are:

```Python
FOC_1 = smp.Eq(smp.diff(bellman.rhs, K[t+1]), 0)
```

$\beta \frac{\partial}{\partial {k}_{t + 1}} V{\left({k}_{t + 1},{\lambda}_{t + 1} \right)} {E}_{t} - \frac{1}{- \delta {k}_{t} + {h}_{t}^{1 - \theta} {k}_{t}^{\theta} {\lambda}_{t} - {k}_{t + 1} + {k}_{t}} = 0$

and:

```Python
FOC_2 = smp.Eq(smp.diff(bellman.rhs, H[t]), 0)
```

$- \frac{A}{1 - {h}_{t}} + \frac{\left(1 - \theta\right) {h}_{t}^{1 - \theta} {k}_{t}^{\theta} {\lambda}_{t}}{\left(- \delta {k}_{t} + {h}_{t}^{1 - \theta} {k}_{t}^{\theta} {\lambda}_{t} - {k}_{t + 1} + {k}_{t}\right) {h}_{t}} = 0$

The Benveniste-Scheinkman envelope theorem condition is:

```Python
BS = smp.Eq(smp.diff(V(K[t], Techno[t]), K[t]), smp.diff(bellman.rhs, K[t])).subs(t, t+1)
```

$\frac{\partial}{\partial {k}_{t + 1}} V{\left({k}_{t + 1},{\lambda}_{t + 1} \right)} = \frac{- \delta + \frac{\theta {h}_{t + 1}^{1 - \theta} {k}_{t + 1}^{\theta} {\lambda}_{t + 1}}{{k}_{t + 1}} + 1}{- \delta {k}_{t + 1} + {h}_{t + 1}^{1 - \theta} {k}_{t + 1}^{\theta} {\lambda}_{t + 1} + {k}_{t + 1} - {k}_{t + 2}}$

The first-order conditions can thus be written as:

```Python
Euler_1 = FOC_1.subs(BS.lhs, BS.rhs)
```

$\frac{\beta \left(- \delta + \frac{\theta {h}_{t + 1}^{1 - \theta} {k}_{t + 1}^{\theta} {\lambda}_{t + 1}}{{k}_{t + 1}} + 1\right) {E}_{t}}{- \delta {k}_{t + 1} + {h}_{t + 1}^{1 - \theta} {k}_{t + 1}^{\theta} {\lambda}_{t + 1} + {k}_{t + 1} - {k}_{t + 2}} - \frac{1}{- \delta {k}_{t} + {h}_{t}^{1 - \theta} {k}_{t}^{\theta} {\lambda}_{t} - {k}_{t + 1} + {k}_{t}} = 0$

and:

```Python
Euler_2 = FOC_2
```

$- \frac{A}{1 - {h}_{t}} + \frac{\left(1 - \theta\right) {h}_{t}^{1 - \theta} {k}_{t}^{\theta} {\lambda}_{t}}{\left(- \delta {k}_{t} + {h}_{t}^{1 - \theta} {k}_{t}^{\theta} {\lambda}_{t} - {k}_{t + 1} + {k}_{t}\right) {h}_{t}} = 0
$

We can use some definition to simplify these Euler equations:

```Python
transition_equation_forward = transition_equation.subs(t, t+1)
R = smp.IndexedBase('r')
returns_capital = smp.Eq(R[t], theta * Techno[t] * K[t] **(theta)* H[t]**(1 - theta) / K[t]).subs(t, t+1)
```

${c}_{t + 1} = - \delta {k}_{t + 1} + {h}_{t + 1}^{1 - \theta} {k}_{t + 1}^{\theta} {\lambda}_{t + 1} + {k}_{t + 1} - {k}_{t + 2}$ \
${r}_{t + 1} = \frac{\theta {h}_{t + 1}^{1 - \theta} {k}_{t + 1}^{\theta} {\lambda}_{t + 1}}{{k}_{t + 1}}$

which help us to obtain:

```Python
Euler_1 = Euler_1.subs(transition_equation.rhs, transition_equation.lhs)
Euler_1 = Euler_1.subs(transition_equation_forward.rhs, transition_equation_forward.lhs)
Euler_1 = Euler_1.subs(returns_capital.rhs, returns_capital.lhs)
```

$\frac{\beta \left(- \delta + {r}_{t + 1} + 1\right) {E}_{t}}{{c}_{t + 1}} - \frac{1}{{c}_{t}} = 0$

In addition, we can use:

```Python
W = smp.IndexedBase('w')
wage_rate = smp.Eq(W[t], (1 - theta) * Techno[t] * K[t]**theta*H[t]**(1-theta)/H[t])
```

${w}_{t} = \frac{\left(1 - \theta\right) {h}_{t}^{1 - \theta} {k}_{t}^{\theta} {\lambda}_{t}}{{h}_{t}}$

In order to obtain:

```Python
Euler_2 = Euler_2.subs(transition_equation.rhs, transition_equation.lhs)
Euler_2 = Euler_2.subs(wage_rate.rhs, wage_rate.lhs)
```

$- \frac{A}{1 - {h}_{t}} + \frac{{w}_{t}}{{c}_{t}} = 0$