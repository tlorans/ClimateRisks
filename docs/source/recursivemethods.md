# Recursive Methods

We will follow the same systematic approach:

1. Define the value function based on the economic environment
2. Use recursive methods to determine the Euler equations of our system

## Deterministic Case

### The Value Function

#### Economic Environment

We start with the definition of the variables and parameters.

##### Time Series Macro Dynamics

We work in discrete time, with $t$ the unit of time: 

```Python
import sympy as smp
t = smp.symbols('t', cls = smp.Idx)
```

We have the following variables:
```
K = smp.IndexedBase('K') # capital
Y = smp.IndexedBase('Y') # output
C = smp.IndexedBase('C') # consumption
I = smp.IndexedBase('I') # investment
```
${K}_{t}$,
${Y}_{t}$,
${C}_{t}$,
${I}_{t}$

And the following parameters:
```
delta = smp.symbols('delta')
beta = smp.symbols('beta')
```
$\delta$,
$\beta$

The dynamic of the capital stock is defined by the following transition equation:

```
transition_equation = smp.Eq(K[t+1], (1 - delta) * K[t] + I[t])
```
${K}_{t + 1} = \left(1 - \delta\right) {K}_{t} + {I}_{t}$

The resource constraint is:
```Python
resource_constraint = smp.Eq(Y[t], C[t] + I[t])
```
${Y}_{t} = {C}_{t} + {I}_{t}$

And we have the production function:

```Python
f = smp.Function('f')(K[t]) # Prod
production_function = smp.Eq(Y[t], f)
```

${Y}_{t} = f{\left({K}_{t} \right)}$

##### Representative Consumer Preferences

The representative consumer / producer derives utility from consumption:

```
u = smp.Function('u')(C[t]) # utility function
```

$u{\left({C}_{t} \right)}$

#### States and Controls

The consumer gives some value to the initial capital stock $K_t$:

```
v = smp.Function('v')(K[t]) # value function
```

$v{\left({K}_{t} \right)}$

It is a state variable as it is inherited from the previous period (refer to the transition equation). 

At each period $t$, the consumer can choose to adjust the consumption level $C_t$. Having the choice about the consumption level implies that it can also control the future level of capital stock $K_{t+1}$. So theoretically, the control variable could either be the consumption level or the future capital stock. Here, we will focus on choosing as control variables the ones that directly appear in the utility function.

The future value of capital stock is thus:

```Python
v_prime = smp.Function('v')(K[t+1])
```
$v{\left({K}_{t + 1} \right)}$

However, we want to make appears our control variable $C_t$ as much as possible in our value function. We can therefore use the time series macro dynamic definitions for reexpressing the state variable $K_{t+1}$ with the control variable $C_{t}$:

```Python
investment_equation = smp.Eq(I[t], smp.solve(resource_constraint, I[t])[0])
investment_equation = investment_equation.subs(production_function.lhs, production_function.rhs)
transition_equation = transition_equation.subs(investment_equation.lhs, investment_equation.rhs)

v_prime = v_prime.subs(transition_equation.lhs, transition_equation.rhs)
```

$v{\left(\left(1 - \delta\right) {K}_{t} + f{\left({K}_{t} \right)} - {C}_{t} \right)}$

We therefore can state our final version of the Bellman equation:

```Python
bellman = smp.Eq(v, u + beta * v_prime)
```

$v{\left({K}_{t} \right)} = \beta v{\left(\left(1 - \delta\right) {K}_{t} + f{\left({K}_{t} \right)} - {C}_{t} \right)} + u{\left({C}_{t} \right)}$



### Euler Equation

## Stochastic Case

## Lucas Tree