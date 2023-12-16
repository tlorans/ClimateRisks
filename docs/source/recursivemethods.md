# Recursive Methods for RBC Models

We will follow the same systematic approach:

1. Define the value function based on the economic environment
2. Use recursive methods to determine the Euler equations of our system

## Neoclassical Growth Model

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

The process is always the same:
1. Find the First Order Conditions (FOC) by taking the derivative of the value function with repect to the control variables
2. Find the Benveniste-Scheinkman (BS) Conditions by setting the the derivative of the value function with respect to the state variables
3. With the BS and the FOC, find an expression for the unknown derivative, that is the derivative of the value function with respect to the future state
4. Plus this expression into the the FOC to find the Euler equation.

We first need a little workaround for working with the unknown derivative of the value function with respect to future capital stock for replacement purposes:

```Python
def get_unknown_derivative(v_prime, state_variable, index_time, transition_equation):
  xi = smp.symbols('xi_1')
  unknown = smp.Subs(smp.Derivative(v_prime.subs(transition_equation.rhs, xi), xi), xi , transition_equation.rhs)
  better_printing = smp.diff(v, state_variable[index_time]) # to go to the format we would like
  better_printing = better_printing.subs(index_time, index_time + 1) # iterate forward to get the format we want
  return smp.Eq(better_printing, unknown)
```

Let's apply it:

```Python
unknown_derivative = get_unknown_derivative(v_prime, K, t, transition_equation)
```

$\frac{\partial}{\partial {K}_{t + 1}} v{\left({K}_{t + 1} \right)} = \left. \frac{d}{d \xi_{1}} v{\left(\xi_{1} \right)} \right|_{\substack{ \xi_{1}=\left(1 - \delta\right) {K}_{t} + f{\left({K}_{t} \right)} - {C}_{t} }}
$

#### First-Order Conditions

We have only one control variable here, thus only one FOC. We have the following function to help us:

```Python
def get_FOC(bellman, control_variable, index_time, utility_function, unknown_derivative):
  FOC = smp.Eq(smp.diff(bellman.rhs, control_variable[index_time]), 0)
  FOC = FOC.replace(unknown_derivative.rhs, unknown_derivative.lhs)
  return smp.Eq(smp.diff(utility_function, control_variable[t]), smp.solve(FOC, smp.diff(utility_function, control_variable[t]))[0])
```

Let's apply it:

```Python
FOC = get_FOC(bellman, C, t, u, unknown_derivative)
```
$\frac{\partial}{\partial {C}_{t}} u{\left({C}_{t} \right)} = \beta \frac{\partial}{\partial {K}_{t + 1}} v{\left({K}_{t + 1} \right)}
$

#### Benveniste-Sheinkman Conditions

We define the following function for finding the BS condition:

```Python
def get_BS(bellman, v, state_variable, index_time, unknown_derivative, FOC):
  # first need to reexpress FOC, if not we can have SymPy issue
  FOC = smp.Eq(unknown_derivative.lhs, smp.solve(FOC, unknown_derivative.lhs)[0])
  BS = smp.Eq(smp.diff(v, state_variable[index_time]), smp.diff(bellman.rhs, state_variable[index_time]))
  BS = BS.replace(unknown_derivative.rhs, unknown_derivative.lhs)
  BS = BS.subs(FOC.lhs, FOC.rhs)
  return BS.subs(index_time, index_time + 1)
```

We know can find the expression for the unknown derivative:

```Python
BS = get_BS(bellman, v, K, t, unknown_derivative, FOC)
```

$\frac{\partial}{\partial {K}_{t + 1}} v{\left({K}_{t + 1} \right)} = \left(- \delta + \frac{\partial}{\partial {K}_{t + 1}} f{\left({K}_{t + 1} \right)} + 1\right) \frac{\partial}{\partial {C}_{t + 1}} u{\left({C}_{t + 1} \right)}
$

#### Euler Equation

And we can finally plug it back to the FOC to obtain the Euler Equation:

```Python
Euler = FOC.subs(BS.lhs, BS.rhs)
```

$\frac{\partial}{\partial {C}_{t}} u{\left({C}_{t} \right)} = \beta \left(- \delta + \frac{\partial}{\partial {K}_{t + 1}} f{\left({K}_{t + 1} \right)} + 1\right) \frac{\partial}{\partial {C}_{t + 1}} u{\left({C}_{t + 1} \right)}
$

## Basic Hansen Model

