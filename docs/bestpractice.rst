.. _bestpractice:

================================================
Best Practices for Collecting Physiological Data
================================================
This document is a work in progress. Currently, an outline of important topics is presented.
NOTE: This information is presented within the context of fMRI data collection.

**Best Practices for Collecting Physiological Data**

**Why collect physiological data?**

Physiological monitoring is a key component of imaging analysis. In fMRI, physiological fluctuations can be identified as noise or as signals of interest, depending on the research question. These data can aid in characterizing different physiological states of the subject during a scan and account for noise components of the overall signal . CO2 is a known vasodilator and creating variability in blood flow can enhance the BOLD signal. Having this data allows one to more accurately model fMRI data by using physiological traces collected during the scan, and adding them as regressors. Each component of physiological data can add motion and variation to the signal of interest and can be accounted for in this way. More specifically, cardiac and respiratory effects are especially important as they can influence the BOLD signal.

An important aspect of accounting for physiological fluctuations is RETROICOR, a method that retrospectively uses information about the cardiac and respiratory cycles to identify which phase of these cycles is represented in each time point of the fMRI time series. This can be particularly useful when imaging regions that are more susceptible to cardiac and respiratory noise, such as spinal cord or brainstem.

Another benefit of collecting physiological data is that it provides a method to monitor the subject and/or patient during the scan, in real-time. Any sudden changes in the different aspects being monitored can help those in the control room identify if the subject and/or patient is under duress. Looking out for these changes is emphasized during first time MRI scans, and ensuring values stay within safe and IRB approved limits, especially during breathing tasks.

**What are the different types of physiological data that can be collected?**

- CO2 & O2 - specifically end-tidal pressures of CO2 and O2, which approximate the arterial levels of these gases
- Cardiac pulsation - heart rate trace
- Respiration - change in chest volume

**How to collect each type of physiological data?**

- CO2 & O2 - Nasal cannula or face mask with gas analyzers, RespirAct (more specifically if you want to modulate end-tidal values)
- Pulse - Photo-plethysmograph, pulse oximeter
- Respiration - Respiration belt, respiratory chest bellows

**What to do with physiological data once it has been collected?**

Phys2bids can be used to organize the various physiological data traces that you have collected. With this program, your data will have the appropriate BIDS labels to describe physiological information. As a sanity check, you should plot each trace to quickly view each trace and ensure that it matches the type of information you think you collected.

A peak detection algorithm can be used on the stored traces to identify end-tidal values for O2 and CO2, and phases of the cardiac and respiratory cycles. The selected peaks traces can then be used as regressors in a general linear model to explain portions of your signal attributed to physiological effects.
