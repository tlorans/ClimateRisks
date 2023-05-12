

## Participation, Ambition and Credibility

In this part, we discuss the participation, ambition and credibility (PAC) framework proposed by Le Guenedal et al. (2022) to assess a company's NZE alignment strategy, based on the quantitative metrics discussed previously. It can forms the basis for a sound stocks selection for net zero investing in part 3.

This framework depends on the carbon trajectories $CE_i(t)$, $CE_i^{Trend}(t)$, $CE^{Target}_i(t)$ and $CE^{NZE}_i(t)$, where $CE_i(t)$ are the historical carbon emissions, $CE_i^{Trend}$ are the estimated carbon emissions forecasted with the trend model, $CE_i^{Target}(t)$ are the deduced carbon emissions form the targets and $CE^{NZE}_i(t)$ is the NZE scenario.

In what follows, we will note $t_{Base}$ the base date, $t_{Last}$ the last reporting date and $t_{NZE}$ the target date of the NZE scenario.
### Participation

The participation dimension generally depends on the past observations and corresponds to the track record analysis of historical carbon emissions.
This dimension helps to answer the question: is the trend of the issuer in line with the net zero emissions scenario? 

Below is a table with indicators that can be used to assess the participation dimension. We can for example use metrics related to the carbon trend such as the slope $\hat{\beta}_{i,1}$ or the estimated carbon emissions $CE_i^{Trend}(t)$. We can also use current gap with the NZE scenario $Gap^{Trend}_i(t_{Last})$ or the time contribution $TC_i(t_{Last}+1 \| t_{Last}, t_{NZE})$.

| Metric | Condition |  
|---|---|
| Gap  | $Gap^{Trend}_i(t_{Last}) \leq 0 $  | 
| Reduction  | $\mathfrak{R}_i(t_{Base},t_{Last}) < 0$  |  
| Time contribution  | $TC_i(t_{Last}+1 \| t_{Last}, t_{NZE}) < 0 $  | 
| Trend  | $\hat{\beta}_{i,1} < 0$ and $R^2_i > 50\%$  |
| Trend  | $CE^{Trend}_i(t)$ for $t > t_{Last}$  |
| Velocity  | $v_i^{(1)}(t_{Last}) \leq 0 $  |

```Python
# Figure 9 page 27, participation
```

### Ambition 


The ambition dimension compares the target trajectory on one side and the NZE scenario or the trend on the other side. It measures to what extent companies are willing to reverse their current carbon emissions and have objectives that match the NZE scenario. This dimension relies on the existence of targets published by the issuer.

This dimension answers to the question: is the commitment of the issuer to fight climate change ambitious? In particular, it helps to understand if the target trajector is above, below or in line with the NZE consensus scenario.

Below is a table with the metrics that can be used to assess the ambition dimension. Among them are the gap based on the target $Gap_i^{Target}$ or the duration computed with the target $\tau^{Target}_i$. An other measure can be the comparison between the normalized carbon budget $\bar{CB}_i^{Target}(t_{Last}, t_{NZE})$ of the company and the normalized carbon budget (normalized wit the current carbon emissions or the carbon emissions of the base year) of the corresponding sector $\bar{CB}^{Target}_{Sector}(t_{Last},t_{NZE})$.

| Metric | Condition |  
|---|---|
| Budget  | $\bar{CB}^{Target}_i(t_{Last}, t_{NZE}) \leq \bar{CB}^{Target}_{Sector}(t_{Last},t_{NZE})$  | 
| Budget  | $CB^{Target}_i(t_{Last}, t_{NZE}) \leq CB^{Trend}_i(t_{Last},t_{NZE})$  | 
| Duration  | $\tau_i^{Target} \leq t_{NZE}$  | 
| Gap  | $Gap^{Target}_i(t_{NZE}) \leq 0$  | 

```Python
# Figure 9 page 27 ambition
```

### Credibility 

Finally, this last dimension address the most important issue: is the target setting of the issuer relevant and robust? 

Indeed, we may wonder if the target trajectory is a too ambitious promise and a form of greenwashing or a plausible scenario.

We can measure the credibility of the targets by comparing the current trend of carbon emissions and the reduction targets or by analyzing the recent dynamics of the track record.

```Python
# Figure 9 page 27, credibility
```