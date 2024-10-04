.. SMA-REACT documentation master file, created by
   sphinx-quickstart on Wed Sep  4 13:23:33 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Shape Memory Alloy Rendering and Calibration Tool (SMA-REACT) Documentation
===========================================================================

.. image:: _static/sample_flowchart.png
   :width: 600 px
   :align: center


SMA-REACT is an open-source, (hopefully) easy-to-use
tool for processing shape memory alloy experimental data 
and calibrating a constitutive model for use in other analyses
(e.g., Abaqus). Data processing and model calibration are 
presented in the form of a python GUI, allowing those unfamiliar
with the intricate details of SMA constitutive modeling to
easily calibrate appropriate models without writing their own
custom subroutines. 

Why should you use SMA-REACT? Have you ever spent hours collecting 
SMA characterization data, only to have to spend even more time 
processing, filtering, and cleaning that data to present? Have you
ever spent countless hours fine-tuning model calibrations, with 
little tracability? If you answered yes to either of these questions,
try it out, and let us know what you think. 


.. toctree::
   :maxdepth: 1
   
   getting_started
   example_calibration
   citation_information
   further_reading
   contributing_extending
   license
   Source Code <modules>

**Indices and tables**
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
