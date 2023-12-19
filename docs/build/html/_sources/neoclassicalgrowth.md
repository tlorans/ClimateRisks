# Neoclassical Growth Model: Equilibrium Conditions

We will follow the same systematic approach:

1. Define the value function based on the economic environment
2. Use recursive methods to determine the Euler equations of our system


## The Value Function

### Economic Environment

We start with the definition of the variables and parameters.

#### Time Series Macro Dynamics

We work in discrete time, with $t$ the unit of time: 

```Python
import sympy as smp
t = smp.symbols('t', cls = smp.Idx)
```

We have the following variables:
```

Y = smp.IndexedBase('Y') # output
C = smp.IndexedBase('C') # consumption
K = smp.IndexedBase('K') # Capital
Z = smp.IndexedBase('Z') # total factor productivity
I = smp.IndexedBase('I') # Investment
epsilon = smp.IndexedBase('epsilon') # TFP shock
```

${Y}_{t}$,
${C}_{t}$,
${K}_{t}$,
${I}_{t}$,
${Z}_{t}$,
${\epsilon}_{t}$

And the following parameters:
```
alpha = smp.symbols('alpha') # capital share
beta = smp.symbols('beta') # discount factor
delta = smp.symbols('delta') # capital depreciation rate
```
$\alpha$,
$\beta$,
$\delta$

The production function is the following:

```
production_function = smp.Eq(Y[t], Z[t] * K[t-1]**alpha + (1 - delta)*K[t-1])
```
${Y}_{t} = \left(1 - \delta\right) {K}_{t - 1} + {K}_{t - 1}^{\alpha} {Z}_{t}$

The resource constraint is:
```Python
resource_constraint = smp.Eq(C[t] + K[t], Y[t])
```

${C}_{t} + {K}_{t} = {Y}_{t}$


And we have a technology shock describing the evolution of the total factor productivity (TFP):

```Python
TFP_equation = smp.Eq(Z[t], smp.exp(epsilon[t]))
```

${Z}_{t} = e^{{\epsilon}_{t}}$

#### Representative Consumer Preferences

The representative consumer / producer derives utility from consumption:

```
u = smp.Function('u')(C[t]) # utility function
```

$u{\left({C}_{t} \right)}$

Here we will give a functional form to the utility function: a logarithmic utility function:

```Python
utility_function = smp.Eq(u, smp.log(C[t]))
```

$u{\left({C}_{t} \right)} = \log{\left({C}_{t} \right)}$

### States and Controls

The consumer gives some value to the initial capital stock $K_{t-1}$, conditional on the stochastic TFP process $Z_t$:

```
v = smp.Function('v')(K[t-1], Z[t])
```

$v{\left({K}_{t - 1},{Z}_{t} \right)}$

Here we denote a bit from what you have seen in the previous part, naming the state variable being denoted as the current capital stock $K_t$ (and you will see this approach in other places). We follow the approach from Uhlig that seems more logical to us: $K_{t-1}$ is the state variable that is inherited. 

At each period $t$, the consumer can choose to adjust the consumption level $C_t$. Having the choice about the consumption level implies that it can also control the current level of capital stock $K_{t}$. So theoretically, the control variable could either be the consumption level or the capital stock. Here, we will focus on choosing as control variables the ones that directly appear in the utility function.

The future value of capital stock is thus:

```Python
v_prime = smp.Function('v')(K[t], Z[t+1])
```

$v{\left({K}_{t},{Z}_{t + 1} \right)}$

However, we want to make appears our control variable $C_t$ as much as possible in our value function. We can therefore use the time series macro dynamic definitions for reexpressing the state variable $K_{t}$ with the control variable $C_{t}$, by finding the transition equation (the equation expressing the dynamic of the capital stock):

```Python
transition_equation = smp.Eq(K[t], smp.solve(resource_constraint, K[t])[0])
transition_equation = transition_equation.subs(production_function.lhs, production_function.rhs)
```

${K}_{t} = - {C}_{t} + {Y}_{t} \\$ 

${K}_{t} = \left(1 - \delta\right) {K}_{t - 1} - {C}_{t} + {K}_{t - 1}^{\alpha} {Z}_{t}$

So we can reexpress:

```Python
v_prime = v_prime.subs(transition_equation.lhs, transition_equation.rhs)
```

$v{\left(\left(1 - \delta\right) {K}_{t - 1} - {C}_{t} + {K}_{t - 1}^{\alpha} {Z}_{t},{Z}_{t + 1} \right)}$

We therefore can state our final version of the Bellman equation:

```Python
bellman = smp.Eq(v, utility_function.rhs + beta * v_prime)
```

$v{\left({K}_{t - 1},{Z}_{t} \right)} = \beta v{\left(\left(1 - \delta\right) {K}_{t - 1} - {C}_{t} + {K}_{t - 1}^{\alpha} {Z}_{t},{Z}_{t + 1} \right)} + \log{\left({C}_{t} \right)}$

Please note that we should have an expectation operator associated with the value of future state variables, as we have a stochastic shock on total factor productivity. Our Bellman Equation should be:

$v{\left({K}_{t - 1},{Z}_{t} \right)} = \beta \mathbb{E} [v{\left(\left(1 - \delta\right) {K}_{t - 1} - {C}_{t} + {K}_{t - 1}^{\alpha} {Z}_{t},{Z}_{t + 1} \right)}] + \log{\left({C}_{t} \right)}$

For ease of programming (I didn't managed yet to work properly with the expectation operator in SymPy), we will program without the expectation operator. But please add it mentally into the results.

## Euler Equation

The process is always the same:
1. Find the First Order Conditions (FOC) by taking the derivative of the value function with repect to the control variables
2. Find the Benveniste-Scheinkman (BS) Conditions by setting the the derivative of the value function with respect to the state variables
3. With the BS and the FOC, find an expression for the unknown derivatives, that is the derivative of the value function with respect to the future state variables
4. Plug the resulting expressions into the initial FOCs in order to find the proper forms of the FOCs, namely the Euler Equations.

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

### First-Order Conditions

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

### Benveniste-Sheinkman Conditions

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

### Euler Equation

And we can finally plug it back to the FOC to obtain the Euler Equation:

```Python
Euler = FOC.subs(BS.lhs, BS.rhs)
```

$\frac{\partial}{\partial {C}_{t}} u{\left({C}_{t} \right)} = \beta \left(- \delta + \frac{\partial}{\partial {K}_{t + 1}} f{\left({K}_{t + 1} \right)} + 1\right) \frac{\partial}{\partial {C}_{t + 1}} u{\left({C}_{t + 1} \right)}
$

## Equilibrium Conditions

## Steady-State