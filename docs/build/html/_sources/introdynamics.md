# Solving for Dynamics

## Log Linearization Techniques

Handling and solving models with substantial nonlinearity is often difficult. If the model is relatively simple, one can find an approximation to the policy function by recursively solving for the value function.

Linear models are often much easier to solve, and there exist well-developed methods for solving linear models. The problem is to convert a nonlinear model into a sufficiently good linear approximation so that the solutions to the linear approximation are helpful in understanding the behavior of the underlying nonlinear system. 

A now standard method for a linear approximation is to log-linearize a model around its stationary state. The assumption is that, if the model is not too far from the stationary state, the linear version that results closely approximate the original model.

### Basics of Log Linearization

Consider a nonlinear model that can be represented by a set of equations of the general form:

\begin{equation}
F(x_t) = \frac{G(x_t)}{H(x_t)}
\end{equation}

where $x_t$ is a vector of the variables of the model that can include expectational variables and lagged variables in addition to contemporaneous variables.

The process of log linearization is to first take the logarithms of te function $F()$, $G()$ and $H()$ and then take a first-order Taylor series approximation. Taking the logarithms gives:

\begin{equation}
\ln(F(x_t)) = \ln(G(x_t)) - \ln(H(x_t))
\end{equation}

and taking the first-order Taylor series expansion around the stationary state values, $\bar{x}$, gives:

\begin{equation}
\ln(F(\bar{x})) + \frac{F'(\bar{x})}{F(\bar{x})}(x_t - \bar{x}) \approx \ln(G(\bar{x})) + \frac{G'(\bar{x})}{G(\bar{x})}(x_t - \bar{x}) - \ln(H(\bar{x})) - \frac{H'(\bar{x})}{H(\bar{x})}(x_t - \bar{x})
\end{equation}

where the notation $X'(\bar{x})$ is used to indicate the gradient at the stationary state. Notice that the model is now linear in $x_t$, since $\frac{F'(\bar{x})}{F(\bar{x})}$, $\frac{G'(\bar{x})}{G(\bar{x})}$, $\frac{H'(\bar{x})}{H(\bar{x})}$, $\ln(G(\bar{x}))$, $\ln(G(\bar{x}))$ and $\ln(H(\bar{x}))$ are constants. 

Given that the log version of the model holds at the stationary state:

\begin{equation}
\ln(F(\bar{x})) = \ln(G(\bar{x})) - \ln(H(\bar{x}))
\end{equation}

We can eliminate the three $\ln()$ components, and the equation simplifies to:

\begin{equation}

\end{equation}

### Uhlig's Method of Log Linearization

## The Method of Undetermined Coefficients


### Conjecturing a Linear Recursive Law of Motion

What is given in our system is the state variables at time $t$. We need to find the value of the endogeneous variables in our model.

We can conjecture a linear recursive law of motion.

### Solving for the Undetermined Coefficients of the Linear Recursive Law of Motion

