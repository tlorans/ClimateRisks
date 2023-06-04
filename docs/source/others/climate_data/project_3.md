## Project 3: Greeness Weighting

As an alternative to the portfolio weighting scheme proposed in most of this course, following Roncalli (2023), we can use a greeness weighting scheme, as proposed by Pastor et al. (2022).

### Greeness Weighting

#### Scoring

The scoring approach is such as:

\begin{equation}
g_{i,j}(t) = G_{i,j}(t) - \bar{G}_j(t)
\end{equation}

with $\bar{G}(t)$ the market capitalization weighted average of $G_i(t)$ accross all issuers $i$ for the metric $j$. Because we substract $\bar{G}_{i,j}(t)$, $g_{i,j}(t)$ measures the issuer's greeness relative to the market portfolio, as in Pastor et al. (2021).

### Finding the Optimal Combination of Metrics

We are interested in long-only portfolio, so we need to keep only positive weights and rescale it such that the sum is equal to one:

\begin{equation}
v_i(t) = \frac{g_i(t)}{\sum_{i=1}^n g_i(t)}
\end{equation}

Finally, the weight of the portfolio will be defined as:

\begin{equation}
x_i(t) = \Pi_{j = 1}^kv_{i,j}^{\theta_j}(t)
\end{equation}

The parameters to determine are $\theta_j$, the relative importance of each metric we are using to define issuer's greeness.






