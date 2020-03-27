.. _bestpractice:

================================================
Best Practices for Collecting Physiological Data
================================================
*This document is a work in progress. Currently, an outline of important topics is presented.
NOTE: This information is presented within the context of fMRI data collection.*

**Best Practices for Collecting Physiological Data During fMRI**

This document provides a succinct introduction to what physiological data are typically recorded during an fMRI experiment, how these signals are recorded, and how these signals can improve our modeling of fMRI timeseries data. This is an active field of research, and we encourage all users to get the latest recommendations prior to initiating a new study. For a more in-depth article on similar subject matter, please see `Bulte and Wartolowska (2017) Neuroimage 154:81-91 <https://www.sciencedirect.com/science/article/pii/S1053811916306929>`_.


Why collect physiological data?
###############################

Physiological monitoring is a key component of understanding physiological sources of signal variance in fMRI data. Monitoring physiology during scanning is critical to enable the characterization of a given subject's physiologic state at the time of the scan, and to track variations in physiology throughout the scan. With these data, we can more accurately model how these factors manifest in the fMRI signal timeseries.

Physiological fluctuations can be identified as "noise" or as "signals of interest", depending on the research question of the imaging experiment. For most fMRI experiments, the goal is to isolate signal fluctuations that are associated with a neural stimulus and the resulting hemodynamic response. In these data, it is important to model and remove signals with a non-neural origin, such as breathing or cardiac related signal variance. Removing these confounds will improve the sensitivity and confidence of the fMRI analysis. In some fMRI experiments, the goal is to characterize a physiologic effect (for example, studies that map cerebrovascular reactivity aim to quantify the dilation of blood vessels during certain non-neural stimuli). In these studies it is essential that the relevant physiologic parameters are recorded so that the analysis produces robust, quantitative physiological parameter maps.

Another benefit of collecting physiological data is that it provides a method to monitor the subject and/or patient during the scan in real-time. Any sudden changes in the different aspects being monitored can help those in the control room identify if the person is under duress or complying with the scan protocol. Looking out for these changes is particularly helpful during an individual's first MRI scan, when they may react poorly to the scan environment. In some protocols, tracking physiology in real-time can ensure that values stay within safe, IRB-approved limits.

Although current modeling of physiology is imperfect, and fMRI signal processing techniques do not yet accurately factor in all physiologic signals, the field continues to develop and our modeling continues to improve. We encourage all fMRI researchers to collect these data to more fully capture the variable human physiology inherent to imaging experiments.


How are typical physiological data collected?
#############################################

The most common types of physiological data acquired in fMRI analysis are cardiac pulsation (pulse), breathing (chest position), and expired gas concentrations (particularly CO2 and O2).

**Cardiac pulsation** can be collected via a sensor on the fingertip (or ear lobe, toe, or other pulse point). These devices are often known as a photoplethysmograph, and typically are included in the MRI scanner infrastructure. The data can thus be collected by the scanner, or recorded by a separate device. Typically the peaks of the cardiac pulsation trace are identified (e.g., the timing of each heart beat). Cardiac pulsation causes local movement artifacts, particularly around large arterial vessels, the edges of the ventricles, and in brainstem areas. RETROICOR (Glover et al. 2000) is one cardiac denoising example, where the timing of each fMRI acquisition relative to the nearest cardiac peak is used to model and remove these local pulsation artifacts. Low frequency changes in heart rate have also been modeled and shown to influence the fMRI timeseries.

**Breathing** is typically monitored using a "respiratory belt" around the participant's chest/diaphragm. The belt may be rigid or elastic, using MR compatible force or pressure transducers to generate a signal proportional to the chest diameter. The optimal positioning of the belt depends on the device being used, however it is best to be fairly consistent in how the belt is worn throughout a study. In some labs, multiple belts are used to better capture different types of breathing styles (e.g., "chest breathing" versus "belly breathing"). Often a belt is incorporated into the MRI scanner infrastructure, and these data can be collected by the scanner or recorded by a separate device. The peaks and troughs of the breathing trace are identified, which can provide information about breathing rate as well as breathing depth. There are three primary ways by which breathing can influence the fMRI signals. First, breathing often leads to bulk motion of the body and head. These effects are typically modeled using volume registration and motion correction algorithms. Second, breathing changes the chest position which can influence the success of the shim, continuously changing B0 homogeneity throughout the scan and in turn affecting signal amplitude. These effects are also modeled using techniques like RETROICOR. Thirdly, changing breathing rate and depth can influence blood gases, which can drive vasodilation or vasoconstriction, and thus substantially influence the fMRI signal amplitude. RVT correction (Birn et al. 2008) estimates the change in breathing rate/depth to model these effects.

**Blood gases:** It is also possible (and recommended!) to directly record changes in blood gas levels, rather than infer them from a chest position measurement. Most commonly we measure carbon dioxide levels (CO2), which is a known vasodilator and can drive large variability in blood flow and the BOLD signal. We can also measure oxygen (O2) levels; O2 only has a mild vasoconstictive effect on the cerebrovasculature, but oxygen levels can directly influence BOLD signal contrast. These two blood gases are typically strongly anticorrelated with eachother in most scans, but can also be manipulated independently and influence the fMRI signals through distinct mechanisms. best practice would be to record both. Although the most accurate recordings of blood gas levels would be achieved through arterial sampling, this is not recommended for most imaging experiments. Instead, the concentrations of CO2 and O2 in arterial blood can be approximated by the partial pressure of each gas at the end of an exhalation, or the end-tidal partial pressure (commonly abbreviated as PETCO2 and PETO2). The person being scanned wears a nasal cannula (soft plastic tube that rests just below the nostrils) or face mask that is connected to a gas analyzer in the control room. The resulting data shows the fluctuations in CO2 and O2 across every breath; an algorithm must extract the "end-tidal" values.


What equipment is needed?
#########################

Peripheral devices:
* finger photoplethysmograph (pulse-oximeter)
* respiratory belt
* disposable nasal cannula (or face mask) and long sample line to connect to control room

Some peripherals can be passed through a void in the penetration panel from the control room to the scan room (e.g., gas sampling line); others must be plugged into the penetration panel for noise filtering (e.g., some pulse sensors). Devices native to the MRI scanner may communicate wirelessly with the scanner. When adding non-native peripheral devices to the scanner environment, we recommend that you check that you are not bringing any outside noise into the scan room or bringing too much scanner noise into the physiological recordings. It may be necessary to develop additional devices or mechanisms to shield these connections.

Recording devices:
* CO2 and O2 analyzer
* analog-to-digital converter (ADC) or other data acquisition (DAQ) device
* associated signal recording/analysis software
For example, ADInstruments sells the Powerlab and uses LabChart software; Biopac sells the MP160 and uses AcqKnowledge software.

It is also important to sync the physiological recordings with the fMRI scan triggers. To do this, it will be necessary to extract the trigger pulses from your MRI scanner, typically inputting these analog signals via BNC into the same ADC recording all of the physiological information.


What to do with physiological data once it has been collected?
##############################################################

Ideally you have recorded physiological data throughout the entire scan session, and have trigger data to identify when scanning occurred. Phys2bids can be used to organize the various physiological data traces that you have collected. With this program, your data will have the appropriate BIDS labels to describe physiological information. As a sanity check, you should plot each trace to quickly view each trace and ensure that it matches the type of information you think you collected.

After this restructuring of the data, there are numerous tools available to process each type of physiological trace, identifying end-tidal values for O2 and CO2, and phases of the cardiac and respiratory cycles. These data are then further processed via smoothing or convolution to create physiological regressors, which can be incorporated into a generalized linear model framework to explain portions of your fMRI signal attributed to physiological effects.
