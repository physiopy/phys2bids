.. _bestpractice:

================================================
Best Practices for Collecting Physiological Data
================================================
This document is a work in progress. Currently, an outline of important topics is presented.
NOTE: This information is presented within the context of fMRI data collection.

**Best Practices for Collecting Physiological Data**

**Why collect physiological data?**

Physiological monitoring is a key component of imaging analysis. In fMRI, physiological fluctuations can be identified as noise or as signals of interest, depending on the research question. These data can aid in characterizing different physiological states of the subject during a scan and account for noise components of the overall signal. CO2 is a known vasodilator and creating variability in blood flow can enhance the BOLD signal. Having this data allows one to more accurately model fMRI data by using physiological traces collected during the scan, and adding them as regressors. Each component of physiological data can add motion and variation to the signal of interest and can be accounted for in this way. More specifically, cardiac and respiratory effects are especially important as they can influence the BOLD signal.

An important aspect of accounting for physiological fluctuations is RETROICOR, a method that retrospectively uses information about the cardiac and respiratory cycles to identify which phase of these cycles is represented in each time point of the fMRI time series. This can be particularly useful when imaging regions that are more susceptible to cardiac and respiratory noise, such as the spinal cord and brainstem.

Another benefit of collecting physiological data is that it provides a method to monitor the subject and/or patient during the scan, in real-time. Any sudden changes in the different aspects being monitored can help those in the control room identify if the subject and/or patient is under duress. Looking out for these changes is emphasized during first time MRI scans, and ensuring values stay within safe and IRB approved limits, especially during breathing tasks.


**What are the different types of physiological data that can be collected?**

The most common types of physiological data acquired in fMRI analysis are arterial gas concentrations (particularly CO2 and O2), cardiac pulsation, and respiration.

The concentrations of CO2 and O2 in arterial blood can be approximated by the partial pressure of each gas at the end of an exhalation, or the end-tidal partial pressure (commonly abbreviated as PETCO2 and PETO2). This physiological data is important to characterize changes in the BOLD signal that are due to vascular, rather than neural, processes.

Cardiac pulsation can be collected to determine heart rate and to detect motion associated with the cardiac cycle.

A respiratory trace can be used to detect changes in chest volume throughout the respiratory cycle as well as the respiratory rate.


**How to collect each type of physiological data?**

End-tidal gas pressures can be collected by sampling exhaled air with a nasal cannula or face mask and measuring the gas concentration with a gas analyzer. Computerized gas delivery systems such as the RespirActTM can also be used for precise modulation and measurement of end-tidal values. Typically with these systems, the partial pressures of CO2 and O2 are collected in real-time. In post-processing, an algorithm is necessary to identify the end-tidal values from the recorded traces.

Cardiac cycle information can be collected with a photo-plethysmograph or pulse oximeter that is worn on the fingers or toes. Intervals between peaks in the cardiac trace can be used to determine heart rate.

The respiratory cycle is recorded with a respiratory belt or respiratory chest bellows. Both devices are worn around the level of the diaphragm and detect changes in chest volume during inspiration and expiration. An algorithm is then used to identify the peaks and troughs of the resulting trace and to determine the respiration rate.

Most physiological recording devices require accessory electronics such as an analog-to-digital converter, data acquisition device (DAQ), specialized recording software, and appropriate circuitry to shield noise from the MR environment.


**What to do with physiological data once it has been collected?**

Phys2bids can be used to organize the various physiological data traces that you have collected. With this program, your data will have the appropriate BIDS labels to describe physiological information. As a sanity check, you should plot each trace to quickly view each trace and ensure that it matches the type of information you think you collected.

A peak detection algorithm can be used on the stored traces to identify end-tidal values for O2 and CO2, and phases of the cardiac and respiratory cycles. The selected peaks traces can then be used as regressors in a general linear model to explain portions of your signal attributed to physiological effects.
