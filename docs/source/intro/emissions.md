# Cross-Sector Reponsibility for Emissions


## Sources of Emissions

From the previous part, we know that anthopogenic emissions $CE_{Industry}(t)$ are the drivers of global warming. To mitigate global warming, $\sigma(t)$, the carbon intensity of industrial activities must be reduced.

But, questions arise about the ultime sources of carbon emissions. The chart below represents the relative share of sources of emissions.

```{figure} sectors.png
---
name: sectors
---
Figure: Emissions by Sector, from Our World in Data, based on World Resources Institute data
```

Thus, we have:

\begin{equation}
CE_{Industry}(t) = CE_{Industry-Related}(t) + CE_{Waste-Related}(t) + CE_{Agriculture-Related}(t) + CE_{Energy-Related}(t)
\end{equation}

Emissions due to the use of fossil fuels $CE_{Energy-Related}(t)$ is by far the most important contributor to global warming.

As presented by Teske et al. (2022), emissions due to energy production and consumption can be represented as an energy-system (with GICS sectors), with:
\begin{equation}
CE_{Energy-Related}(t) = CE_{Energy}(t) + CE_{Utilities}(t) + CE_{End-Use}(t)
\end{equation}

Where $CE_{Energy}(t)$ represents the carbon emissions from the (primary) energy sector, $CE_{Utilities}(t)$ represents the secondary energy emissions and $CE_{End-Use}(t)$ the end-use activities emissions.

The end-use activities can be further decomposed into the main end-use sources of energy-related emissions (Teske et al., 2022):

\begin{equation}
CE_{End-Use}(t) = CE_{Cement}(t) + CE_{Steel}(t) + CE_{Chemicals}(t) + CE_{Texxtile \; \& \; Leather}(t) + CE_{Aluminium}(t) + CE_{Buildings}(t) + CE_{Food \; Processing}(t) + CE_{Transport}(t)
\end{equation}


## Energy System and Cross-Sector Responsibility

Analyzing carbon emissions through the lens of the energy-system as Teske et al. (2022) allows for further comprehesions of interlinkages and cross-sector responsibility for emissions.

Indeed, one can account for both direct and indirect emissions occuring in each stage (primary and secondary energy production and end-use activities), with indirect emissions representing the amount of emissions produced by using the energy / product produced in the previous stage.
### Primary Energy
For the primary energy (Energy sector), we have:

- Scope 1 ($SC_1^{Energy}$): emissions defined as the direct emissions related to extraction, mining and burning of fossils fuels
- Scope 2 ($SC_2^{Energy}$): indirect emissions from the electricity used for the operation of mining equipment, oil and gas rigs, refineries and other equipment
- Scope 3 ($SC_3^{Energy}$): emissions embedded, which occur when the fossil fuel produced by the primary energy industry is burnt by end users

### Secondary Energy

For the secondary energy (Utilities sector) we have:
- Scope 1 ($SC_1^{Utilities}$): direct emissions from fuels related to the generation and transmission of electricity and the distribution of fossil fuels / renewable gas
- Scope 2 ($SC_2^{Utilities}$): indirect emissions from the electricity used for the production of a sector's core product. It includes electricity consumption of power plants, losses by power grids etc.
- Scope 3 ($SC_3^{Utilities}$): emissions embedded, that occur with the use of electricity or gaseous fuels by end users.

### End-Use Activities

And for the end-use activities, we generally have:
- Scope 1 ($SC_1^{End-Use}$): emissions related to fuel used in the activities
- Scope 2 ($SC_2^{End-Use}$): indirect emissions from the electricity used across the steps of the value chain of the activity
- Scope 3 ($SC_3^{End-Use}$): in Teske et al. (2022), $SC_3^{Transport}$ is the main energy-related source, corresponding to the emissions from the use of transports.

### Cross-Sector Responsibility 

Analyzing carbon emissions sources through the lens of the energy-system highlights the cross-sector responsibility for carbon emissions, as:

\begin{equation}
CE_{Energy-Related}(t) =
SC^{Energy}_1(t) + SC^{Energy}_2(t) + SC^{Energy}_3(t)
\end{equation}

\begin{equation}
= SC^{Utilities}_1(t) + SC^{Utilities}_2(t) + SC^{Utilities}_3(t)
\end{equation}

\begin{equation}
=
SC^{End-Use}_1(t) + SC^{End-Use}_2(t) + SC^{End-Use}_3(t) = 35 \text{ GtCO2}
\end{equation}

The chart below represents this cross-sector responsibility along the energy system:

```{figure} interconnected.png
---
name: interconnected
---
Figure: Global Energy Related CO2 Emissions - Scope 1, 2 and 3, from Teske et al. (2022)
```

That is, demand for fossil fuels from the end-use activities and supply of electricity produced with fossil fuels from the Utilities are cross-responsibles for the energy-related emissions.


