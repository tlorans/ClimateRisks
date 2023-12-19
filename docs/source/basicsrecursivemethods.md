# Basics Intuition for Characterizing the Equilibrium Conditions

The objective of this part is to give you the basics ideas behind the the process of finding equilibrium conditions of your model.

I advise you to take a look at [this excellent note from G.Fonseca](https://www.hetwebsite.net/het/fonseca/notes/fonseca_bellman.pdf).

We start with a brief overview of what is a value function and the recursive formulation of a social planner.

## The Value Function

Let's say our consumer begin with a capital stock $K_t$:

```Python
import sympy as smp

K = smp.IndexedBase('K') # capital stock

t = smp.symbols('t', cls = smp.Idx)
```
And we give some value to current capital stock $v(K_t)$ but also future capital stock:

```Python
v_prime = smp.Function('v')(K[t+1]) # future
```

In $v(K_t)$ and $v(K_{t+1})$, you notice that the function itself is not time-subscripted. Because we work in infinite time periods, in both cases we are facing the same remaining "future", so both functions are in fact a unique time-invariant function $v(.)$.

Now comes the question how to put some "value" to capital stock? The consumer doesn't directly derived utility from capital stock, but from consumption of the output produced using capital stock:

```Python
C = smp.IndexedBase('C') # consumption
print(smp.latex(C[t]))
u = smp.Function('u')(C[t]) # utility function
print(smp.latex(u))
```
${C}_{t}$,
$u{\left({C}_{t} \right)}$

And the production function is:

```Python
f = smp.Function('f')(K[t]) # production function
```
$f{\left({K}_{t} \right)}$


Before writing the value function, let's create a discounting factor $\beta$ to make value of current capital stock and future capital stock comparable:

```Python
beta = smp.symbols('beta') # discount factor
```

All right. Now, we can state our value function of current capital stock as a function of utility derived from consumption and discounted value of future capital stock:

```
value_function = smp.Eq(v, u + beta * v_prime)
print(smp.latex(value_function))
```
$v{\left({K}_{t} \right)} = \beta v{\left({K}_{t + 1} \right)} + u{\left({C}_{t} \right)}$

## State vs. Control Variables

Future capital stock $K_{t+1}$ must be constructed (or saved) from output today ($f(K_t)$). We have the following difference equation or transition function:

```Python
transition_equation = smp.Eq(K[t+1], f - C[t])
```
${K}_{t + 1} = f{\left({K}_{t} \right)} - {C}_{t}$

So, let's recall that $K_t$ is given, this is our state variable to which we attribute some value $v(K_t)$. What is the variable the consumer controls in this problem? 

Well, the consumer can define the level of consumption $C_t$. Due to the transition equation defined before, we know that $K_{t+1}$ depends on the level of consumption choosen today $C_t$. 

We can therefore rewrite our value function to replace $K_{t+1}$ by the transition equation with our control variable:

```Python
v_prime = v_prime.subs(transition_equation.lhs, transition_equation.rhs)
value_function = smp.Eq(v, u + beta * v_prime)
```

$v{\left({K}_{t} \right)} = \beta v{\left(f{\left({K}_{t} \right)} - {C}_{t} \right)} + u{\left({C}_{t} \right)}$

The main point here is that once you've defined your control variable (you could have choosen $K_{t+1}$ instead of $C_t$ as your control variable), you must try to make it appear in most places of your value function.

The value function we have defined is not the objective by itself: we want to find a policy function $K_t = h(C_t)$.

## First Order Conditions

Let's take the first derivative of our value function with respect to our control variable $C_t$ and set it to zero:

```Python
FOC = smp.Eq(smp.diff(value_function.rhs, C[t]), 0)
```

$ -\beta \left. \frac{d}{d \xi_{1}} v{\left(\xi_{1} \right)} \right|_{\substack{ \xi_{1}=f{\left({K}_{t} \right)} - {C}_{t} }} + \frac{\partial}{\partial {C}_{t}} u{\left({C}_{t} \right)} = 0$

The problem we face here is that we don't know what the derivative of the value for future capital stock with respect to future capital stock is, because we don't know what our value function is!  

Indeed, the chain rule gives $\frac{\partial}{\partial K_{t+1}} v{\left({K}_{t+1} \right)}\frac{\partial}{\partial C_{t}} {K}_{t+1}$.

We know what $\frac{\partial}{\partial C_{t}} {K}_{t+1}$ gives thanks to the transition equation:

```Python
smp.diff(transition_equation.rhs, C[t])
```
$-1$

But we don't know what $\frac{\partial}{\partial K_{t+1}} v{\left({K}_{t+1} \right)}$ is. 

Let's define two functions to deal with this first step:

```Python

def get_unknown_derivative(value_function, value_function_next_period, state_variable, index_time, transition_equation):
  xi = smp.symbols('xi_1')
  # we have v'(K[t+1]()) in the deriv dV/dC, we have generally dV/dC = dU/dC (we know) + dV'/dK[t+1] * dKt+1/dC
  # We generally know dKt+1/dC (at least we have refomulated Kt+1 such as C appear)
  # we don't know dV'/dK[+1]
  unknown = smp.Subs(smp.Derivative(value_function_next_period.subs(transition_equation.rhs, xi), xi), xi , transition_equation.rhs)
  better_printing = smp.diff(value_function, state_variable[index_time]) # to go to the format we would like
  # format better what we don't know: dV/dKt+1 in the chain rule
  better_printing = better_printing.subs(index_time, index_time + 1) # iterate forward to get the format we want
  return smp.Eq(better_printing, unknown)

def get_FOC(bellman, control_variable, index_time, utility_function, unknown_derivative):
  # take the first derivative of the bellman for the control variable and set it to 0
  FOC = smp.Eq(smp.diff(bellman.rhs, control_variable[index_time]), 0)
  # replace the format for the unknown derivative for a better one
  FOC = FOC.replace(unknown_derivative.rhs, unknown_derivative.lhs)
  return smp.Eq(smp.diff(utility_function, control_variable[t]), smp.solve(FOC, smp.diff(utility_function, control_variable[t]))[0])

```

We use the first function as a workaround to get a better expression for manipulation purposes:

```Python
unknown_derivative = get_unknown_derivative(v, v_prime, K, t, transition_equation)
```

$\frac{\partial}{\partial {K}_{t + 1}} v{\left({K}_{t + 1} \right)} = \left. \frac{d}{d \xi_{1}} v{\left(\xi_{1} \right)} \right|_{\substack{ \xi_{1}=f{\left({K}_{t} \right)} - {C}_{t} }}$

And the second to get the FOC:

```Python
FOC = get_FOC(value_function, C, t, u, unknown_derivative)
```

$\frac{\partial}{\partial {C}_{t}} u{\left({C}_{t} \right)} = \beta \frac{\partial}{\partial {K}_{t + 1}} v{\left({K}_{t + 1} \right)}$

Please note that in case of multiple control variables, you will end up with as much first order conditions.

## Benveniste-Scheinkman Conditions

Hopefully, we can find an expression for the unknown derivative thanks to the Benveniste-Scheinkman (BS) Condition, such that we can have a final equilibrium condition that doesn't refer to the value function itself.

The process is the following:

1. Take the derivative of the value function with respect to your state variable $K_t$

```Python
BS = smp.Eq(smp.diff(v, K[t]), smp.diff(value_function.rhs, K[t]))
BS = BS.replace(unknown_derivative.rhs, unknown_derivative.lhs)
```
$\frac{\partial}{\partial {K}_{t}} v{\left({K}_{t} \right)} = \beta \frac{\partial}{\partial {K}_{t}} f{\left({K}_{t} \right)} \frac{\partial}{\partial {K}_{t + 1}} v{\left({K}_{t + 1} \right)}$

2. Use the previous result of the FOC in order to get an expression for the unknown derivative:

```Python
re_express_FOC = smp.Eq(unknown_derivative.lhs, smp.solve(FOC, unknown_derivative.lhs)[0])
```
$\frac{\partial}{\partial {K}_{t + 1}} v{\left({K}_{t + 1} \right)} = \frac{\frac{\partial}{\partial {C}_{t}} u{\left({C}_{t} \right)}}{\beta}$

3. Plug it into the BS condition:

```Python
BS = BS.subs(re_express_FOC.lhs, re_express_FOC.rhs)
```

$\frac{\partial}{\partial {K}_{t}} v{\left({K}_{t} \right)} = \frac{\partial}{\partial {K}_{t}} f{\left({K}_{t} \right)} \frac{\partial}{\partial {C}_{t}} u{\left({C}_{t} \right)}$

4. Iterate forward:

```Python
BS = BS.subs(t, t+1)
```

$\frac{\partial}{\partial {K}_{t + 1}} v{\left({K}_{t + 1} \right)} = \frac{\partial}{\partial {K}_{t + 1}} f{\left({K}_{t + 1} \right)} \frac{\partial}{\partial {C}_{t + 1}} u{\left({C}_{t + 1} \right)}$

Now we have an expression to replace the derivative of the value function into the FOC. 

Let's define a function to produce all theses preceding steps:

```Python

def get_BS(bellman, v, state_variable, index_time, unknown_derivative, FOC):
  # first need to reexpress FOC, if not we can have SymPy issue
  FOC = smp.Eq(unknown_derivative.lhs, smp.solve(FOC, unknown_derivative.lhs)[0])
  # we want to find an expression for dV/dKt+1
  BS = smp.Eq(smp.diff(v, state_variable[index_time]), smp.diff(bellman.rhs, state_variable[index_time]))
  BS = BS.replace(unknown_derivative.rhs, unknown_derivative.lhs)
  BS = BS.subs(FOC.lhs, FOC.rhs)
  return BS.subs(index_time, index_time + 1)
```

And use it to get the expression we want in one line:

```Python
BS = get_BS(value_function, v, K, t, unknown_derivative, FOC)
```

$\frac{\partial}{\partial {K}_{t + 1}} v{\left({K}_{t + 1} \right)} = \frac{\partial}{\partial {K}_{t + 1}} f{\left({K}_{t + 1} \right)} \frac{\partial}{\partial {C}_{t + 1}} u{\left({C}_{t + 1} \right)}$

In case of multiple non-stochastic state variables, you will end up with multiple BS conditions (ie. one expression per unknown derivative of the value function with each state variable).

## Euler Equations

The final stage is to find the Euler Equation (the name of the final form for our FOCs). We find it by plugging the expression we've obtained from the BS condition into the initial FOC:

```Python
euler_equation = FOC.subs(BS.lhs, BS.rhs)
```

$\frac{\partial}{\partial {C}_{t}} u{\left({C}_{t} \right)} = \beta \frac{\partial}{\partial {K}_{t + 1}} f{\left({K}_{t + 1} \right)} \frac{\partial}{\partial {C}_{t + 1}} u{\left({C}_{t + 1} \right)}$

And we're done! The Euler Equation and the transition equation gives you the equilibrium conditions of this model.

In case of multiple control variables, you will end up with multiple Euler equations (one equation per control variable).