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

Here we change a bit from what you have seen in the previous part, the state variable being denoted as the previous capital stock $K_{t-1}$ rather than current capital stock as in the previous part $K_t$. We follow the approach from Uhlig that seems more logical to us: $K_{t-1}$ is the state variable that is inherited. 

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

As explained in the basics, we first need to apply our little workaround function in order to find a better representation of the unknown derivative:

```Python
unknown_derivative = get_unknown_derivative(v, v_prime, K, t - 1, transition_equation)
```

$\frac{\partial}{\partial {K}_{t}} v{\left({K}_{t},{Z}_{t + 1} \right)} = \left. \frac{\partial}{\partial \xi_{1}} v{\left(\xi_{1},{Z}_{t + 1} \right)} \right|_{\substack{ \xi_{1}=\left(1 - \delta\right) {K}_{t - 1} - {C}_{t} + {K}_{t - 1}^{\alpha} {Z}_{t} }}
$

### First-Order Conditions

We have only one control variable here, thus only one FOC. We have the function defined in the previous part to help us:

```Python
FOC = get_FOC(bellman, C, t, utility_function.rhs, unknown_derivative)
```
$\frac{1}{{C}_{t}} = \beta \frac{\partial}{\partial {K}_{t}} v{\left({K}_{t},{Z}_{t + 1} \right)}
$

### Benveniste-Sheinkman Conditions

We have the previously defined function to help us to find the expression for the unknown derivative:

```Python
BS = get_BS(bellman, v, K, t - 1, unknown_derivative, FOC)
```

$\frac{\partial}{\partial {K}_{t}} v{\left({K}_{t},{Z}_{t + 1} \right)} = \frac{\frac{\alpha {K}_{t}^{\alpha} {Z}_{t + 1}}{{K}_{t}} - \delta + 1}{{C}_{t + 1}}
$

### Euler Equation

And we can finally plug it back to the FOC to obtain the Euler Equation:

```Python
euler_equation = FOC.subs(BS.lhs, BS.rhs)
```

$\frac{1}{{C}_{t}} = \frac{\beta \left(\frac{\alpha {K}_{t}^{\alpha} {Z}_{t + 1}}{{K}_{t}} - \delta + 1\right)}{{C}_{t + 1}}
$

Again, please note that we should have an expectation operator in our Euler Equation.

## Equilibrium Conditions

The Equilibrium Conditions of your model are composed by the Euler Equation and the time series macro dynamics of your system. As we have reexpressed the resource constraint and the production function into a transition equation, the transition equation and the total factor productivity equation will represents the time series macro dynamics:

$\frac{1}{{C}_{t}} = \mathbb{E}[\frac{\beta \left(\frac{\alpha {K}_{t}^{\alpha} {Z}_{t + 1}}{{K}_{t}} - \delta + 1\right)}{{C}_{t + 1}}] \\$

${K}_{t} = \left(1 - \delta\right) {K}_{t - 1} - {C}_{t} + {K}_{t - 1}^{\alpha} {Z}_{t} \\$

${Z}_{t} = e^{{\epsilon}_{t}}$

This is a Non-Linear Rational Expectation Model.