# Basics Intuition for Characterizing the Equilibrium Conditions

The objective of this part is to give you the basics ideas behind the the process of finding equilibrium conditions of your model.

I advise you to take a look at [this excellent note from G.Fonseca](https://www.hetwebsite.net/het/fonseca/notes/fonseca_bellman.pdf).

This is a short version of McCandless (2008 {cite:p}`mccandless2008abcs`) examples for Recursive Deterministic Models. 

## Robison Crusoe Economy

In recursive approach, we separate teh set of variables that we are using into state variables and control variables. 

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
