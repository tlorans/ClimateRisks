## Project 2: Portfolio Alignment with Energy-System Consistent Decarbonization Pathways

While we've seen in the previous part how to ensure portfolio alignment with an intensity decarbonization pathway based on a NZE scenario, one should question the idea to use the same decarbonization pathways for all stocks in the portfolio.
### Energy-System NZE Scenarios

Primary Energy and Secondary Energy: Shifting to Renewables

```{figure} primary_energy.png
---
name: primary_energy
---
Figure: Primary energy sector-energy production under the OECM 1.5°C pathway, from Teske et al. (2022)
```

### Portfolio Alignment with Energy-System Decarbonization

We now assume that we want to reduce the carbon footprint at the sector level. In this case, we can denote by $CI(x; Sector_j)$ the carbon intensity of the $j^{th}$ sector, with (Roncalli, 2023):

\begin{equation}
CI(x;Sector_j) = \sum_{i \in Sector_j} \tilde{x_i} CI_i
\end{equation}

With $\tilde{x}_i$ the normalized weight in the sector bucket, such as:

\begin{equation}
\tilde{x}_i = \frac{x_i}{\sum_{k \in Sector_j}x_k}
\end{equation}

Equivalently:

\begin{equation}
CI(x;Sector_j) = \frac{(s_j \circ CI)^T x}{s^T_j x}
\end{equation}

With $a \circ b$ is the Hadamard product (element-wise product): $(a \circ b)_i = a_ib_i$.



Imposing a portfolio alignment at the sector level is equivalent to modify the constraint to become:

\begin{equation}
CI(x(t); Sector_j) \leq (1 - \mathfrak{R}_{CI}(t_0,t;Sector_j))CI(b(t_0;Sector_j))
\end{equation}

In order to find the QP form to integrate into our problem, we need a few transformations (because we need to find the form $G^Tx \leq h$):

\begin{equation}
(*) ↔ CI(x(t); Sector_j) \leq (1 - \mathfrak{R}_{CI}(t_0,t;Sector_j))CI(b(t_0;Sector_j))
\end{equation}

\begin{equation}
↔ (s_j \circ CI)^T x \leq (1 - \mathfrak{R}_{CI}(t_0,t;Sector_j))CI(b(t_0;Sector_j))(s_j^T x)
\end{equation}

\begin{equation}
↔ ((s_j \circ CI) - (1 - \mathfrak{R}_{CI}(t_0,t;Sector_j))CI(b(t_0;Sector_j)) s_j)^T x \leq 0
\end{equation}

\begin{equation}
↔ (s_j \circ (CI - (1 - \mathfrak{R}_{CI}(t_0,t;Sector_j))CI(b(t_0;Sector_j))^T x \leq 0
\end{equation}

We thus have our QP form $G = (s_j \circ (CI - (1 - \mathfrak{R}_{CI}(t_0,t;Sector_j))CI(b(t_0;Sector_j))^T$ and $h = 0$.


### Your Turn!

The IEA NZE scenario consider four main sectors:
1. Buildings
2. Industry
3. Transport 
4. Electricity and heating
5. Other

The IEA NZE scenario is the following (in GtCO2eq):

| Year  |  2020 | 2025 | 2030 | 2035 | 2040 | 2045 | 2050 |
|---|---|---|---|---|---|---|---|
|$CE_{Buildings}(t)$|  2.9   | 2.4  | 1.8  | 1.2 | 0.7 | 0.3 | 0.1 |
|$CE_{Industry}(t)$|  8.5   | 8.1  | 6.9  | 5.2 | 3.5 | 1.8 | 0.5 |
|$CE_{Transport}(t)$|  7.2   | 7.2  | 5.7  | 4.1 | 2.7 | 1.5 | 0.7 |
|$CE_{Electricity}(t)$|  13.5   | 10.8  | 5.8  | 2.1 | -0.1 | -0.3 | -0.4 |
|$CE_{Other}(t)$|  1.9   | 1.7  | 0.9  | 0.1 | -0.5 | -0.8 | -1 |

1. With the data used in the previous project, and using the global IEA-derived intensity decarbonization pathway, build a net zero portfolio, without integrating the carbon dynamics.
2. Compute the carbon trends and emissions forecasts.
3. Implement a climate risk integration strategy, taking into account the carbon trend.
4. Based on the sectors NZE, determine an intensity decarbonization pathway per sector
5. Map the IEA sectors to the stocks' sectors in the data we've used in the previous projects.
6. Using the sector-based intensity decarbonization pathway, build a new portfolio. You can integrate the carbon trend or not.