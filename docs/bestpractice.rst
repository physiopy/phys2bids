.. _bestpractice:

================================================
Best Practices for Collecting Physiological Data
================================================

This document provides a succinct introduction to what physiological data are typically recorded during an fMRI experiment, how these signals are recorded, and how these signals can improve our modeling of fMRI time series data. This is an active field of research, and we encourage all users to get the latest recommendations prior to initiating a new study. For a more in-depth article on similar subject matter, please see `Bulte and Wartolowska (2017) Neuroimage 154:81-91 <https://www.sciencedirect.com/science/article/pii/S1053811916306929>`_.

.. _whycollectphysdata:

Why collect physiological data?
----------------------------------
Physiological monitoring is a key component of understanding physiological sources of signal variance in fMRI data. Monitoring physiology during scanning is critical to enable the characterization of a given subject's physiologic state at the time of the scan, and to track variations in physiology throughout the scan. With these data, we can more accurately model how these factors manifest in the fMRI signal time series.

Physiological fluctuations can be identified as "noise" or as "signals of interest", depending on the research question of the imaging experiment. For most fMRI experiments, the goal is to isolate signal fluctuations that are associated with a neural stimulus and the resulting hemodynamic response (Caballero-Gaudes et. al 2016). In these data, it is important to model and remove signals with a non-neural origin, such as breathing or cardiac related signal variance. Removing these confounds will improve the sensitivity and confidence of the fMRI analysis. In some fMRI experiments, the goal is to characterize a physiologic effect (for example, studies that map cerebrovascular reactivity aim to quantify the dilation of blood vessels during certain non-neural stimuli) (Caballero-Gaudes et. al 2016). In these studies it is essential that the relevant physiologic parameters are recorded so that the analysis produces robust, quantitative physiological parameter maps.

Another benefit of collecting physiological data is that it provides a method to monitor the subject and/or patient during the scan in real-time. Any sudden changes in the different aspects being monitored can help those in the control room identify if the person is under duress or complying with the scan protocol. Looking out for these changes is particularly helpful during an individual's first MRI scan, when they may react poorly to the scan environment. In some protocols, tracking physiology in real-time can ensure that values stay within safe, IRB-approved limits.

Although current modeling of physiology is imperfect, and fMRI signal processing techniques do not yet accurately factor in all physiologic signals, the field continues to develop and our modeling continues to improve. We encourage all fMRI researchers to collect these data to more fully capture the variable human physiology inherent to imaging experiments.

.. _differenttypesofphysdata:

How are typical physiological data collected?
----------------------------------------------------------------------------
The most common types of physiological data acquired in fMRI analysis are cardiac pulsation (pulse), breathing (chest position), and expired gas concentrations (particularly CO2 and O2).

**Cardiac pulsation** can be collected via a sensor on the fingertip (or ear lobe, toe, or other pulse point). These devices are often known as a photoplethysmograph, and typically are included in the MRI scanner infrastructure. The data can thus be collected by the scanner, or recorded by a separate device. Typically the peaks of the cardiac pulsation trace are identified (e.g., the timing of each heart beat). Cardiac pulsation causes local movement artifacts, particularly around large arterial vessels, the edges of the ventricles, and in brainstem areas (Dagli et al. 1999). RETROICOR (Glover et al. 2000) is one cardiac denoising example, where the timing of each fMRI acquisition relative to the nearest cardiac peak is used to model and remove these local pulsation artifacts. Low frequency changes in heart rate have also been modeled and shown to influence the fMRI time series (Shmueli et al. 2007, Chang et al. 2009).

**Breathing** is typically monitored using a "respiratory belt" around the participant's chest/diaphragm. The belt may be rigid or elastic, using MR compatible force or pressure transducers to generate a signal proportional to the chest diameter. The optimal positioning of the belt depends on the device being used, however it is best to be fairly consistent in how the belt is worn throughout a study. In some labs, multiple belts are used to better capture different types of breathing styles (e.g., "chest breathing" versus "belly breathing"). Often a belt is incorporated into the MRI scanner infrastructure, and these data can be collected by the scanner or recorded by a separate device. The peaks and troughs of the breathing trace are identified, which can provide information about breathing rate as well as breathing depth. There are three primary ways by which breathing can influence the fMRI signals. First, breathing often leads to bulk motion of the body and head (Brosch et al. 2002). These effects are typically modeled using volume registration and motion correction algorithms. Second, breathing changes the chest position which can influence the success of the shim, continuously changing B0 homogeneity throughout the scan and in turn affecting signal amplitude (Brosch et al. 2002, Raj et al. 2001). These effects are also modeled using techniques like RETROICOR. Thirdly, changing breathing rate and depth can influence blood gases, which can drive vasodilation or vasoconstriction, and thus substantially influence the fMRI signal amplitude (Chang and Glover 2009). RVT correction (Birn et al. 2008) estimates the change in breathing rate/depth to model these effects.

**Blood gases** It is also possible (and recommended!) to directly record changes in blood gas levels, rather than infer them from a chest position measurement. Most commonly we measure carbon dioxide levels (CO2), which is a known vasodilator and can drive large variability in blood flow and the BOLD signal (Birn et al. 2006, Wise et al. 2004). We can also measure oxygen (O2) levels; O2 only has a mild vasoconstrictive effect on the cerebrovasculature, but O2 levels can directly influence BOLD signal contrast (Bulte et al. 2007). These two blood gases are typically strongly anti correlated with each other in most scans, but can also be manipulated independently and influence the fMRI signals through distinct mechanisms (Floyd 2003). Best practice would be to record both. Although the most accurate recordings of blood gas levels would be achieved through arterial sampling, this is not recommended for most imaging experiments. Instead, the concentrations of CO2 and O2 in arterial blood can be approximated by the partial pressure of each gas at the end of an exhalation, or the end-tidal partial pressure (commonly abbreviated as PETCO2 and PETO2) (Bengtsson et al. 2001, McSwain et al. 2010?). The person being scanned wears a nasal cannula (soft plastic tube that rests just below the nostrils) or face mask that is connected to a gas analyzer in the control room. The resulting data shows the fluctuations in CO2 and O2 across every breath; an algorithm must extract the "end-tidal" values.

.. _howtocollectphysdata:

What equipment is needed?
---------------------------------------------------
Peripheral devices:

- finger photoplethysmograph (pulse-oximeter)
- respiratory belt
- disposable nasal cannula (or face mask)
- long sample line to connect from the scan room to the control room

Some peripheral devices can be passed through a void in the penetration panel from the control room to the scan room (e.g., gas sampling line); others must be plugged into the penetration panel for noise filtering (e.g., some pulse sensors). Devices native to the MRI scanner may communicate wirelessly with the scanner. When adding non-native peripheral devices to the scanner environment, we recommend that you check that you are not bringing any outside noise into the scan room or bringing too much scanner noise into the physiological recordings. It may be necessary to develop additional devices or mechanisms to shield these connections.

Recording devices:

- CO2 and O2 analyzer
- analog-to-digital converter (ADC) or other data acquisition (DAQ) device
- associated signal recording/analysis software

For example, ADInstruments sells the Powerlab and uses LabChart software; Biopac sells the MP160 and uses AcqKnowledge software.
It is also important to sync the physiological recordings with the fMRI scan triggers. To do this, it will be necessary to extract the trigger pulses from your MRI scanner, typically inputting these analog signals via BNC into the same ADC recording all of the physiological information.

.. _whattodowithphysdata:

What to do with physiological data once it has been collected?
--------------------------------------------------------------------

Ideally you have recorded physiological data throughout the entire scan session, and have trigger data to identify when scanning occurred. Phys2bids can be used to organize the various physiological data traces that you have collected. With this program, your data will have the appropriate BIDS labels to describe physiological information. As a sanity check, you should quickly plot each trace to ensure that it matches the type of information you think you collected.

After this restructuring of the data, there are numerous tools available to process each type of physiological trace, identifying end-tidal values for O2 and CO2, and phases of the cardiac and respiratory cycles. These data are then further processed via smoothing or convolution to create physiological regressors, which can be incorporated into a generalized linear model framework to explain portions of your fMRI signal attributed to physiological effects.

.. _references:

References
--------------------------------
Bengtsson, J., Bake, B., Johansson, A., & Bengtson, J. P. (2001). End-tidal to arterial oxygen tension difference as an oxygenation index. Acta Anaesthesiologica Scandinavica, 45(3), 357–363. https://doi.org/10.1034/j.1399-6576.2001.045003357.x

Birn, R. M., Diamond, J. B., Smith, M. A., & Bandettini, P. A. (2006). Separating respiratory-variation-related fluctuations from neuronal-activity-related fluctuations in fMRI. NeuroImage, 31(4), 1536–1548. https://doi.org/10.1016/j.neuroimage.2006.02.048

Birn, R. M., Smith, M. A., Jones, T. B., & Bandettini, P. A. (2008). The respiration response function: The temporal dynamics of fMRI signal fluctuations related to changes in respiration. NeuroImage, 40(2), 644–654. https://doi.org/10.1016/j.neuroimage.2007.11.059

Brosch, J. R., Talavage, T. M., Ulmer, J. L., & Nyenhuis, J. A. (2002). Simulation of human respiration in fMRI with a mechanical model. IEEE Transactions on Biomedical Engineering, 49(7), 700–707. https://doi.org/10.1109/TBME.2002.1010854

Bulte, D. P., Chiarelli, P. A., Wise, R. G., & Jezzard, P. (2007). Cerebral perfusion response to hyperoxia. Journal of Cerebral Blood Flow and Metabolism : Official Journal of the International Society of Cerebral Blood Flow and Metabolism, 27(1), 69–75. https://doi.org/10.1038/sj.jcbfm.9600319

Bulte, D., & Wartolowska, K. (2017). Monitoring cardiac and respiratory physiology during FMRI. NeuroImage, 154, 81–91. https://doi.org/10.1016/j.neuroimage.2016.12.001

Caballero-Gaudes, C., & Reynolds, R. C. (2017). Methods for cleaning the BOLD fMRI signal. NeuroImage, 154(December 2016), 128–149. https://doi.org/10.1016/j.neuroimage.2016.12.018

Chang, C., Cunningham, J. P., & Glover, G. H. (2009). Influence of heart rate on the BOLD signal: The cardiac response function. NeuroImage, 44(3), 857–869. https://doi.org/10.1016/j.neuroimage.2008.09.029

Chang, C., & Glover, G. H. (2009). Relationship between respiration, end-tidal CO2, and BOLD signals in resting-state fMRI. NeuroImage, 47(4), 1381–1393. https://doi.org/10.1016/j.neuroimage.2009.04.048

Dagli, M. S., Ingeholm, J. E., & Haxby, J. V. (1999). Localization of cardiac-induced signal change in fMRI. NeuroImage, 9(4), 407–415. https://doi.org/10.1006/nimg.1998.0424

Floyd, T. F., Clark, J. M., Gelfand, R., Detre, J. A., Ratcliffe, S., Guvakov, D., … Eckenhoff, R. G. (2003). Independent cerebral vasoconstrictive effects of hyperoxia and accompanying arterial hypocapnia at 1 ATA. Journal of Applied Physiology, 95(6), 2453–2461. https://doi.org/10.1152/japplphysiol.00303.2003

Glover, G. H., Li, T., & Ress, D. (2000). Image‐based method for retrospective correction of physiological motion effects in fMRI: RETROICOR. Magnetic Resonance in Medicine, 44(1), 162–167. https://doi.org/10.1002/1522-2594(200007)44:1<162::AID-MRM23>3.0.CO;2-E

McSwain, S. D., Hamel, D. S., Smith, P. B., Gentile, M. A., Srinivasan, S., Meliones, J. N., & Cheifetz, I. M. (2010). End-tidal and arterial carbon dioxide measurements correlate across all levels of physiologic dead space. Respiratory Care, 55(3), 288–293.

Raj, D., Anderson, A. W., & Gore, J. C. (2001). Respiratory effects in human functional magnetic resonance imaging due to bulk susceptibility changes. Phys. Med. Biol, 46, 3340.

Shmueli, K., van Gelderen, P., de Zwart, J. A., Horovitz, S. G., Fukunaga, M., Jansma, J. M., & Duyn, J. H. (2007). Low-frequency fluctuations in the cardiac rate as a source of variance in the resting-state fMRI BOLD signal. NeuroImage, 38(2), 306–320. https://doi.org/10.1016/j.neuroimage.2007.07.037

Wise, R. G., Ide, K., Poulin, M. J., & Tracey, I. (2004). Resting fluctuations in arterial carbon dioxide induce significant low frequency variations in BOLD signal. NeuroImage, 21(4), 1652–1664. https://doi.org/10.1016/j.neuroimage.2003.11.025
