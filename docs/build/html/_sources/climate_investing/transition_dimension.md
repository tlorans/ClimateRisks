# Starting from the Transition Dimension


## Promoting Climate Solutions

Because Climate Solutions stocks tend to be less mature than other stocks, a lot of them can be not included in the initial benchmark. To increase the potential climate solutions stocks to be included in the net zero benchmark, you may want to increase the list of eligible securities, such as:

\begin{equation}
b^{augmented} = \begin{bmatrix}
b \\
0_k \\
0_l \\
0_m
\end{bmatrix}
\end{equation}

with $k$ the universe of clean energy stocks, $l$ the universe of clean transportation and $m$ the universe of building efficiency stocks among an extended securities universe.

We now have a universe of eligible securities $u = n + k + l + m$, with $n$ the initial benchmark universe.

### Clean Energy

| Climate Solution | Example Stock | Stock Description |
|---|---|---|
| Geothermal | AAON | AAON sells geothermal/water-source heat pumps a key technology for making buildings electrified and more energy efficient. |
| Grid Expansion | ABB | ABB makes 65.5% of its revenue from grid flexibility and EV infrastructure by selling substation packages and charging infrastructure. |
| Hydrogen | Advent Technologies Holdings | Advent sells components that improve the performance of hydrogen fuel cells for the aviation, automotive, and other markets. |
| Methane Capture | Archaea Energy Inc | Archea Energy is a pure play in methane capture. They capture landfill gas and convert it into low-carbon renewable natural gas and electricity. |
| Solar PVs | Array Technologies | Array sells solar tracking systems that use machine learning to identify the best positioning for a solar array to increase energy production. |
| Nuclear Power | Cameco | Cameco mines and sells uranium for the purposes of nuclear fuel production. |
| Energy Storage | CBAK Energy Technology | CBAK is a pure play that makes lithium batteries used in EVs, electric tools, and energy storage applications. |
| Waste to Energy | Covanta | Covanta makes most of its revenue from waste-to-energy operations and metal recycling, both Climate Solutions. |
| Biofuels | FutureFuel | Future Fuels makes 79% of revenue from biofuels made mostly from cooking oils, other plant oils and animal fats. |
| Wind Turbines | Broadwind | Broadwind makes 70% of its revenue by selling steel towers and adapters to wind turbine manufacturers. |

### Clean Transportation 

| Climate Solution | Example Stock | Stock Description |
| --- | --- | --- |
| Telepresence | 8x8, Inc. | 8x8, Inc. provides voice, video, chat, contact center, business phones and cloud-based contact center solutions that enable people and businesses to avoid traveling for meetings. |
| EV Infrastructure | ADS-TEC Energy PLC | ADS-TEC Energy is an EV infrastructure pure play. ADS-TEC Energy's ChargeBox is a fast charging solution for EVs with up to 320 KW charging power. |
| Electric Aviation | Archer Aviation Inc. | Archer Aviation is an electric aviation pure play that is designing an electric aircraft for use in future urban air mobility networks and reduce the need for fossil-fuel powered air transport. |
| Electric Cars | Arcimoto | Arcimoto is known for making 3-wheeled EVs, such as an all-electric rapid response vehicle for emergency services and an EV for last-mile delivery. |
| Electric Cars | Faraday Future Intelligent Electric Inc. | Faraday is a pure play that intends to start building electric cars. |
| E-bikes | EZGO Technologies | EZ is a pure play that makes e-bicycles, e-tricycles, and lithium batteries for the Chinese market. |

### Building Efficiency

| Climate Solution | Example Stock | Stock Description |
| --- | --- | --- |
| LED | Acuity Brands | Acuity makes LED lights for commercial, architectural, and specialty applications. Acuity also makes building efficiency and building automation products. |
| Retrofit | Ameresco | Ameresco makes buildings more energy efficient, builds renewable power plants, sells solar PV products, and owns a wind power project. |
| High Performance Glass | Apogee Enterprises | Apogee makes high-performance glass and related products that enhance the energy efficiency of buildings. |
| Water Distribution | Badger Meter | Badger makes >50% of its revenue from selling water meters that can help water utilities detect leaks, an important climate solution. |
| Insulation | Beacon Roofing Supply | Beacon sells and distributes insulation products, solar paneling, solar inverters and solar panels mounting hardware. |
| Heat Pumps | Carrier Global | Carrier sells HVAC products including high-efficiency heat pumps, a technology necessary for electrifying and energy retrofitting buildings. |
| Building Automation | Comfort Systems USA | Comfort Systems makes 84.5% of its revenue from replacing old HVAC systems with more efficient ones. |
| Dynamic Glass | Crown ElectroKinetics | Crown makes dynamic glass that changes its opacity and reflectiveness in response to outside conditions. Dynamic glass enhances the energy efficiency of buildings. |




### Integrating Climate Solutions Promotion into the Decarbonized Portfolio Problem

We have $cs_{Clean \; Energy}$, $cs_{Clean \; Transportation}$ and $cs_{Buildings \; Efficiency}$ vectors of 0 and 1 is a climate solution or not, of size $u$. 

We have:
\begin{equation}b_{Clean \; Energy} = cs_{Clean \; Energy}^T b^{augmented}
\end{equation}

\begin{equation}
b_{Clean \; Transportation} = cs_{Clean \; Transportation}^T b^{augmented}
\end{equation} 

and

\begin{equation} 
b_{Buildings \; Efficiency} = cs_{Buildings \; Efficiency}^T b^{augmented}
\end{equation}

The vector of optimal weights $x^*$ is of size $u$.

The optimization problem becomes:

\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \; \frac{1}{2} (x-b^{augmented})^T \Sigma(x-b^{augmented})\\
& \text{subject to}
& & 1_u^Tx = 1 \\
& & &  0_u \leq x \leq 1_u \\
& & & - \begin{bmatrix}
cs_{Clean \; Energy} \\
cs_{Clean \; Transportation} \\
cs_{Buildings \; Efficiency}
\end{bmatrix}^T x \leq  - (1 + G) \cdot \begin{bmatrix}
b_{Clean \; Energy} \\
b_{Clean \; Transportation} \\
b_{Buildings \; Efficiency}
\end{bmatrix}
\end{aligned}
\end{equation*}

With $G$ a transition multiplier.


## Excluding Companies Fueling Climate Change

We have $\mathbb{1}\{i \notin \text{Oil or Coal}\}$ a vector with 0 and 1.

The optimization problem becomes:

\begin{equation*}
\begin{aligned}
& x* = 
& & argmin \; \frac{1}{2} (x-b^{augmented})^T \Sigma(x-b^{augmented})\\
& \text{subject to}
& & 1_u^Tx = 1 \\
& & &  0_u \leq x \leq \mathbb{1}\{i \notin \text{Oil or Coal}\} \\
& & & - \begin{bmatrix}
cs_{Clean \; Energy} \\
cs_{Clean \; Transportation} \\
cs_{Buildings \; Efficiency}
\end{bmatrix}^T x \leq  - (1 + G) \cdot \begin{bmatrix}
b_{Clean \; Energy} \\
b_{Clean \; Transportation} \\
b_{Buildings \; Efficiency}
\end{bmatrix}
\end{aligned}
\end{equation*}