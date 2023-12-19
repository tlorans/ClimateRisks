# Consumption-Based Capital Asset Pricing Model: Equilibrium Conditions

## The Genesis with the Lucas Tree Model

### The Value Function

#### Economic Environment

##### Time Series Macro Dynamics

We start with the following variables:

```Python
C = smp.IndexedBase('C') # conso, control variable
Z = smp.IndexedBase('Z') # assets
D = smp.IndexedBase('D') # Dividends
P = smp.IndexedBase('P') # Price

t = smp.symbols('t', cls = smp.Idx)
```

And the discounting factor:
```
beta = smp.symbols('beta')
```

We have the following resource constraint and transition function:

```Python

resource_constraint = smp.Eq(Z[t+1] * P[t] + C[t], Z[t] * D[t] + Z[t] * P[t])
transition_function = smp.Eq(Z[t+1], smp.solve(resource_constraint, Z[t+1])[0])
```

##### Representative Consumer Preferences

We have the following utility function:

```Python
u = smp.Function('u')(C[t])
```

##### States and Controls

We choose $C_t$ as our control variable. Thus $Z_t$ and $Z_{t+1}$ are our states variables. 

```Python
v = smp.Function('v')(Z[t])
v_prime = smp.Function('v')(Z[t+1])
```

We want to reexpress $Z_{t+1}$ to make our control variable appear:

```
v_prime = v_prime.subs(transition_function.lhs, transition_function.rhs)
```

We can finally state our Bellman equation:

```Python
bellman = smp.Eq(v, u + beta * v_prime)
```

### Euler Equation

Before starting, we find our unknown derivative:

```Python
unknown = get_unknown_derivative(v_prime, Z, t, transition_function)
```

#### First Order Conditions

We get our FOC:

```Python
FOC = get_FOC(bellman, C, t, u, unknown)
```

#### Benveniste-Scheinkman Conditions

We get the BS:

```Python
BS = get_BS(bellman, v, Z, t, unknown, FOC)
```

#### Euler Equation

And finally the Euler:

```Python
Euler = FOC.subs(BS.lhs, BS.rhs)
Euler.simplify()
```

## Returns As Equilibrium Conditions

## The Value Function

## Euler Equation

## Equilibrium Conditions

## Steady-State