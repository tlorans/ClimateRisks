## Integrating the Transition Dimension

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

### Controlling for Green Intensity