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