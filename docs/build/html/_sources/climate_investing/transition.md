
## Integrating the Transition Dimension

While we've addressed the decarbonization dimension in the previous part, climate risk integration strategy also calls for integrating the transition dimension (Barahhou et al., 2022).

Indeed, one of the main objective of potential mitigation policies will be to shift the economy towards green activities.

The PAB addresses the transition dimension by imposing a weight constraint on what is defined as climate impact sectors. However, using the green intensity measure proposed by Barahhou et al. (2022), it has been observed that the PAB constraint has no positive impact on the resulting green intensity. 

Furthermore, Barahhou et al. (2022) observed a negative relationship between the decarbonization and the transition dimensions. This negative relationship calls for the inclusion of a green intensity constraint.

In what follows, we will cover the transition dimension integration by the PAB label with the Climate Impact sectors, before introducing the green intensity measure from Barahhou et al. (2022).
### Climate Impact Sectors

The PAB label requires the portfolio's exposure to sectors highly exposed to climate change to be at least equal to the exposure in the investment universe. According to the TEG (2018 {cite:p}`hoepner2018teg`, 2019 {cite:p}`hoepner2019handbook`), we can distinguish two types of sectors:

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
CIS_{High}(x(t)) \geq  CIS_{High}(b(t))
\end{equation}

The PAB's optimization problem becomes (Le Guenedal and Roncalli, 2022):

\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2} (x(t)-b(t))^T \Sigma(t)(x(t)-b(t))\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & &  0_n \leq x \leq 1_n \\
& & & CI(x(t)) \leq (1 - \mathfrak{R}_{CI}(t_0,t))CI (b(t_0)) \\
& & & CIS_{High}(x(t)) \geq CIS_{High}(b(t))
\end{aligned}
\end{equation*}

Regarding the QP parameters, the last two constraints can be casted into $Gx \leq h$ with:

\begin{equation}
G = \begin{bmatrix}
CI^T \\
- CIS_{High}^T
\end{bmatrix}
\end{equation}

and 

\begin{equation}
h = \begin{bmatrix}
(1 - \mathfrak{R}_{CI}(t_0,t))CI (b(t_0)) \\
- CIS_{High}(b(t))
\end{bmatrix}
\end{equation}


If the idea behing the concept of HCIS in the PAB approach was to ensure that the resulting portfolio promotes activities contributing to the low-carbon transition, the constraint applied at the portfolio level has many drawbacks. Indeed, the constraint tends to encourages substitutions between sectors or industries and not substitutions between issuers within a same sector. As stated by Barahhou et al. (2022), the trade-off is not between green electricity and brown electricity for example, but between electricity generation and health care equipment. To assess if a portfolio is really shifting to the low-carbon economy, Barahhou et al. (2022) propose a green intensity measure. 

### Green Intensity


A green intensity measure starts with a green taxonomy. The most famous example is the European green taxonomy. Developed by the TEG (2020 {cite:p}`eutaxo2020`), the EU green taxonomy defines economic activities which make a contribution to environmental objectives while do no significant harm to the other environmental objectives (DNSH constraint) and comply with minimum social safeguards (MS constraint). Other taxonomies exist, such as the climate solutions listed by the Project Drawdown (2017 {cite:p}`hawken2017drawdown`) for each important sectors. Proprietary taxonomies from data vendors can also be used.

A bottom-up approach to measure the green intensity of a portfolio starts with the green revenue share at the issuer level:

\begin{equation}
GI_i = \frac{GR_i}{TR_i}
\end{equation}

Where $GR_i$ and $TR_i$ are respectively the green revenues and the total turnover of the issuer $i$.

The green intensity of the portfolio is then:

\begin{equation}
GI(x) = \sum^n_{i=1}x_i \cdot GI_i
\end{equation}

As Barahhou et al. (2022) observed, there is a decreasing function between the green intensity and the reduction level. This negative correlation between decarbonization and transition dimensions calls for the introduction of a green intensity constraint. This is for preventing the aligned portfolios from having a lower green intensity.

We finally add the green intensity constraint to our previous optimization problem that includes the carbon footprint dynamics (Barahhou et al., 2022):
\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \frac{1}{2} (x(t)-b(t))^T \Sigma(t)(x(t)-b(t))\\
& \text{subject to}
& & 1_n^Tx = 1\\
& & &  0_n \leq x \leq 1_n \\
& & & CI^{Trend}(x(t)) \leq (1 - \mathfrak{R}_{CI}(t_0,t))CI(b(t_0)) \\
& & & GI(t,x) \geq (1 + G(t)) \cdot GI(t_0, b(t_0))
\end{aligned}
\end{equation*}

With $G(t)$ is a greeness multiplier. The underlying idea is to maintain a green intensity for the portfolio that is higher than the green intensity of the benchmark.

### Key Takeaways

- Transition dimension needs to be taken into account in a climate risk integration strategy, as mitigation policies objective is to shift the economy towards green activities

- PAB approach to integrate the transition dimension relies on the HCIS constraint

- A measure to assess the portfolio's transition to a low-carbon economy has been proposed by Barahhou et al. (2022): the green intensity

- The HCIS constraint from the PAB falls short in improving the green intensity of the portoflio compared to the benchmark, and then underlies failures in the PAB's integration of the transition dimension

- In fact, the decarbonization and the transition dimensions seems to be negatively correlated

- This negative correlation calls for the direct inclusion of a green intensity constraint for climate risk integration strategy