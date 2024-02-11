# U-120M proton beam model in PHITS
This are a simulation input parameters for Monte Carlo program [PHITS](https://phits.jaea.go.jp/). Model is used in my Bachelor thesis **Model description of proton beams** for comparation with the experiment done on [cyclotron U-120M](https://www.ujf.cas.cz/en/departments/department-of-accelerators/cyclotron/) in Řež, Czechia. 

## Experimental setup
- proton beam with average energy of $E=33$ MeV ($FWHM = 0.5$ MeV),
- beam divergence of $\pm1.2339\degree$, 
- $0.86$ mm thick Ta foil $40$ cm from the nozzle, 
- Si detection element of [MiniPix TPX3](https://advacam.com/camera/minipix-tpx3/) detector $10$ cm perpendicularly to the beam, $10$ cm parallel to the foil and angled at $45\degree$.

## Simulation
Variables `cXX` can be used to quickly change detection element position, size, resolution and Ta-foil thickness. 

`[T-Track]` (Overview) tally is for visualization of the setup and beam geometry. `[T-Track]` (TPX3) tally is to check flux on the detector. Main output of the simulation is `[T-Deposit]` and `[T-LET]`, they are for displaying deposited energy $Dose$ and linear energy trasnfer $LET$ in Si detection element of TPX3. 

`[Forced Collisions]` are to improve chances of deflected particles interactions. `[Importance]` is for neglect of residual beam behind the Ta-foil that will no longer be useful, also it is for run time optimalization. 
