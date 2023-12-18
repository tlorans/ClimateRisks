# Basics Intuition for the Recursive Methods

The objective of this part is to give you the basics ideas behind the Recursive methods we will use in the next parts.

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

## The Problem with the First Order Condition: the Unknown Derivative

Let's take the first derivative of our value function with respect to our control variable $C_t$ and set it to zero:

```Python
FOC = smp.Eq(smp.diff(value_function.rhs, C[t]), 0)
```

$ -\beta \left. \frac{d}{d \xi_{1}} v{\left(\xi_{1} \right)} \right|_{\substack{ \xi_{1}=f{\left({K}_{t} \right)} - {C}_{t} }} + \frac{\partial}{\partial {C}_{t}} u{\left({C}_{t} \right)} = 0$


## Finding an Expression for the Unknown Derivative with the Benveniste-Scheinkman Condition

