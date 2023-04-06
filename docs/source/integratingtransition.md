## Integrating the Transition Dimension

While we've addressed the decarbonization dimension in the previous part, net zero portfolio needs also to integrate the transition dimension. Indeed, one of the main objective of a net zero investor is to finance the transition to a low-carbon economy.
The PAB addresses the transition dimension by imposing a weight constraint on what is defined as climate impact sectors. However, using the green intensity measure proposed by Roncalli et al. (2022), it has been observed that the PAB constraint has no positive impact on the resulting green intensity. An observed negative relationship between the decarbonization and the transition dimensions calls for the inclusion of a green intensity constraint.

### Controlling for Climate Impact Sectors

The PAB label require the exposure to sectors highly exposed to climate change to be at least equal to the exposure in the investment universe. According to the TEG (2019a), we can distinguish two types of sectors:

1. High climate impact sectors (HCIS or $CIS_{High}$)
2. Low climate impact sectors (LCIS or $CIS_{Low}$)

The HCIS are sectors that are identified as key to the low-carbon transition. They corresponds to the following NACE classes:
- A. Agriculture, Forestry and Fishing
- B. Mining and Quarrying
- C. Manufacturing
- D. Electricity, Gas, Steam and Air Conditioning Supply
- E. Water Supply, Sewerage, Waste Management and Remediation Activities
- F. Construction
- G. Wholesale and Retail Trade, Repair of Motor Vehicles and Motorcycles
- H. Transportation and Storage
- L. Real Estate Activities

We have $CIS_{High}(x) = \sum_{i \in CIS_{High}}x_i$ the HCIS weight of the portfolio $x$. At each rebalancing date $t$, we must verify that:

\begin{equation}
CIS_{High}(x(t)) \geq \phi_{CIS} \cdot CIS_{High}(b(t))
\end{equation}

Where $\phi_{CIS} = 1$.

The PAB's optimization problem becomes:

\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2} (x(t)-b(t))^T \Sigma(t)(x(t)-b(t))\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & &  0_n \leq x \leq 1_n \\
& & & CI(x(t)) \leq (1 - \mathfrak{R}_{CI}(t_0,t))CI (b(t_0)) \\
& & & CIS_{High}(x(t)) \geq \phi_{CIS} \cdot CIS_{High}(b(t))
\end{aligned}
\end{equation*}
### Financing the Transition

If the idea behing the concept of HCIS in the PAB approach was to ensure that the resulting portfolio promotes activities contributing to the low-carbon transition, the constraint applied at the portfolio level has many drawbacks. Indeed, the constraint tends to encourages substitutions between sectors or industries and not substitutions between issuers within a same sector. The trade-off is not between green electricity and brown electricity for example, but between electricity generation and health care equipment. This approach doesn't contribute to financing the transition, which is an objective of a net zero portfolio. To assess if a portfolio is really contributing to the low-carbon transition, Roncalli et al. (2022) propose a green intensity measure. 



### Controlling for Green Intensity

As Roncalli et al. (2022) observed, there is a decreasing function between the green intensity and the reduction level. This negative correlation between decarbonization and transition dimensions calls for the introduction of a green intensity constraint. This is for preventing the aligned portfolios from having a lower green intensity.

We finally add the green intensity constraint to our previous optimization problem that includes the carbon footprint dynamics:
\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2} (x(t)-b(t))^T \Sigma(t)(x(t)-b(t))\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & &  0_n \leq x \leq 1_n \\
& & & CI(x(t)) \leq (1 - \mathfrak{R}_{CI}(t_0,t))CI(b(t_0)) \\
& & & CM(t, x) \leq CM^* \\
& & & GI(t,x) \geq (1 + G(t)) \cdot GI(t_0, b(t_0))
\end{aligned}
\end{equation*}

With $G(t)$ is a greeness multiplier. The underlying idea is to maintain a green intensity for the net zero portfolio that is higher than the green intesity of the benchmark.