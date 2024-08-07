# U-120M proton beam model in PHITS
These are a simulation input parameters for Monte Carlo program [PHITS](https://phits.jaea.go.jp/). Model is used in my Bachelor thesis **Model description of proton beams** for comparation with the experiment done on [cyclotron U-120M](https://www.ujf.cas.cz/en/departments/department-of-accelerators/cyclotron/) in Řež, Czechia. 

File `bp_model_v1.inp` is the old version of experiment conducted by C. Granja and his PhD student D. Poklop described in article *Directional-Sensitive Wide Field-of-View Monitoring of High-Intensity Proton Beams by Spectral Tracking of Scattered Particles with Scattering Foil and Miniaturized Radiation Camera* (this article is **not** yet published).  File `bp_model_v2.inp` is the current version of the experiment described in the next chapter. 

File `scatter_model.inp` is for manual output of differential effective cross section to solid angle for proton collision with tantalum. 

## Experimental setup
- proton beam with average energy of $E=33$ MeV ($FWHM = 0.5$ MeV) on the $Ta$ foil,
- beam divergence of $\pm1.2339\degree$,
- nozzle has a exit window $0.055$ mm thick $Al$ foil, 
- $0.1$ mm thick $Ta$ scatter foil $56$ cm from the nozzle, 
- $Si$ detection element of [MiniPix TPX3](https://advacam.com/camera/minipix-tpx3/) detector $141$ cm perpendicularly to the beam, $141$ cm parallel to the foil ($200$ cm from scatter foil), perpendicularly to scattered paticles and angled at $60$ degrees to the ceiling. 

## Simulation
`$OMP=0` is a command for turning on parallel computing using *OpenMP* with all available processing cores (if you aren't using parallelization then just delete the line). 

Variables `cXX` can be used to quickly change detection element position, size, resolution and Ta-foil thickness. 

Aluminium walls around the detector element simulate detector cover. Above the detector element is $0.001$ mm thick $Al$ entrance window and bellow is $0.85$ thick $Si$ ASIC chip with $0.025$ mm air gap. Detector has agle of $60$ degrees to ceiling so that, based on the agles of trajectories, origin of scatter events can be determined. 

`[T-Track]` (Overview) tally is for visualization of the setup and beam geometry. `[T-Track]` (TPX3) tally is to check flux on the detector (there are two addition `[T-Track]` tallies to determine flux between the detector and scatter foil). `[T-Cross]` (Energy spectrum) tally is for determinig energy specrum of the beam in front of the $Ta$ foil and the detector. Main output of the simulation is `[T-Deposit]` and `[T-LET]`, they are for displaying deposited energy $Dose$ and linear energy trasnfer $LET$ in $Si$ detection element of TPX3. 

`[Forced Collisions]` are to improve chances of deflected particles interactions. Geometry is designed in a way, that particles that leave the experiment space and are no longer useful enter into the void where they no longer interact. This saves on computation time. 

## Simulation output

These are the simulation outputs for $10^{8}$ particles and $100$ batches.  

- Particle flux in $xz$ plane, at position $(0;0)$ is $Ta$ scatter foil, primary beam behind scatter foil is ignored.
<img src="simulation_output/track_all.png" width=75% height=75%>

- Proton energy spectrum $1$ cm in front of the scatter foil. 
<img src="simulation_output/foil_spectrum_1.png" width=75% height=75%>

- Proton energy spectrum $1$ cm behind the scatter foil. 
<img src="simulation_output/foil_spectrum_2.png" width=75% height=75%>

- Deposited energy in detector element. 
<img src="simulation_output/deposit_det.png" width=75% height=75%>

- Proton energy spectrum on the detector. 
<img src="simulation_output/det_spectrum.png" width=75% height=75%>

