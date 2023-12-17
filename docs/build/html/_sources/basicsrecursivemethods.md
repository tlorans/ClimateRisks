# Basics Intuition for the Recursive Methods

The objective of this part is to give you the basics ideas behind the Recursive methods we will use in the next parts.

We start with a brief overview of what is a value function and the recursive formulation of a social planner.

## The Value Function

Let's say our consumer begin with some value for capital stock $K_t$:

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

Before stating the final form of the value function, let's create a discounting factor $\beta$ to make value of current capital stock and future capital stock comparable:

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

## The Problem with the First Order Condition: the Unknown Derivative

## Finding an Expression for the Unknown Derivative with the Benveniste-Scheinkman Condition

