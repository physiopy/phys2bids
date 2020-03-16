.. _bestpractice:

================================================
Best Practices for Collecting Physiological Data
================================================
This document is a work in progress.

**Best Practices for Collecting Physiological Data**

**Why collect physiological data?**

- Physiological fluctuations can be treated as noise in fMRI data or as signals of interest to characterize different physiological states
- Add regressors in the modeling of fMRI data to explain signal variance
- Especially cardiac and respiratory effects as they can influence the BOLD signal
- Cardiac pulsatility and breathing-related chest/abdomen movement → RETROICOR
- Monitor subject/patient during the scan (important during first-time scans, or breathing tasks)

**What are the different types of physiological data that can be collected?**

- CO2 & O2 - specifically end-tidal pressures of CO2 and O2, which approximate the arterial levels of these gases
- Cardiac pulsation - heart rate trace
- Respiration - change in chest volume

**How to collect each type of physiological data?**

- CO2 & O2 - Nasal cannula or face mask with gas analyzers, RespirAct (more specifically if you want to modulate end-tidal values)
- Pulse - Photo-plethysmograph, pulse oximeter
- Respiration - Respiration belt, respiratory chest bellows

**What to do with physiological data once it has been collected?**

- Use Phys2bids to organize the data
- Can also plot each channel from LabChart file to quickly view which kind of physiological data each channel represents
- Use a peak detection algorithm to get end-tidal CO2 trace for breathing task BOLD fMRI and convolve with HRF
- Use peak detection algorithm to get HR trace and convolve with CRF
- Perform RETROICOR on the cardiac and respiratory cycles to include in GLM as regressors
