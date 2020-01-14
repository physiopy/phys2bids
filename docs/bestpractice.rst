.. _bestpractice:

================================================
Best Practices for Collecting Physiological Data
================================================

This document is a work in progress. Currently, an outline of important topics is presented.

.. _whycollectphysdata:

Why collect physiological data?
----------------------------------
- Physiological fluctuations can be treated as noise in fMRI data or as signals of interest to characterize different physiological states
- Add regressors in the modeling of fMRI data to explain signal variance

  - Especially cardiac and respiratory effects as they can influence in the BOLD signal
- Cardiac pulsatility and breathing related chest/abdomen movement --> RETROICOR
- Monitor subject/patient during the scan (important during first-time scans, or breathing tasks)

.. _differenttypesofphysdata:

What are the different types of physiological data that can be collected?
----------------------------------------------------------------------------

- CO2& O2: specifically end-tidal pressures of CO2 and O2, which approximate the arterial levels of these gases
- Cardiac pulsation: heart rate trace
- Respiration: change in chest volume

.. _howtocollectphysdata:

How to collect each type of physiological data?
---------------------------------------------------

- CO2 & O2: nasal cannula or face mask with gas analyzers, RespirAct (more specifically if you want to modulate end-tidal values)
- Pulse: photo-plethysmograph, pulse oximeter
- Respiration: respiratory belt, respiratory chest bellows

.. _whattodowithphysdata:

What to do with physiological data once it has been collected?
--------------------------------------------------------------------

- Use phys2bids to organize the data
- Can also plot each channel from LabChart file the quickly view which kind of physiological data each channel represents
- Use a peak detection algorithm to get end-tidal CO2 trace for breathing task BOLD fMRI and convolve with HRF
- Use a peak detection algorithm to get HR trace and convolve with CRF
- Use a peak detection algorithm to get respiratory trace and convolve with RRF

  - Perform RETROICOR on the cardiac and respiratory cycles to include in the GLM as regressors
