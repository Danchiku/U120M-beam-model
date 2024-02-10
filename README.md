# U-120M proton beam model in PHITS
Monte Carlo model (PHITS) of proton beam output of cyclotron U-120M in Řež, Czechia. Experimental setup: 
- 33 MeV proton beam
- beam divergence of +/- 1.2339 degrees
- 0.86 mm thick Ta foil 40 cm from nozzle
- Si detection element of minipix TPX3 detector 10 cm perpendicularly to the beam, 10 cm parallel to the foil and angled at 45 degrees.

[T-Track] (Overview) tally is used to visualized the setup and beam geometry. [T-Track] (TPX3) tally is used to check flux on detector. [T-Deposit] (TPX3) is used to calculate deposited energy in Si detection element of TPX3. 

Variables "cXX" can be used to quickly change detector position, size and Ta-foil thickness. 

[Forced Collisions] are used to improve chances of deflected particles interactions. 
