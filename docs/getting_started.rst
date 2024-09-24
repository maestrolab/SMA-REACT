.. SMA-REACT documentation getting started file, created by
   sphinx-quickstart on Wed Sep  4 13:23:33 2024.
Overview
========
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

Installation
============
SMA-REACT is available under the GNU general public license
on GitHub_

.. _GitHub: https://github.com/maestrolab/SMAREACTcleaned

Currently, we do not support pip installation.
Please download or clone the repository and type::
   python setup.py install

Requirements
------------
SMA-REACT is compatible with Python 3.9 and is built
with pyqt5, version 5.15.10. 
Here is a complete list of dependencies:
   * deap_ (requires pip install)
   * matplotlib_
   * numpy_
   * pandas_
   * pyqt5_
   * scikit-learn_
   * scipy_
   * Spyder_

.. _deap: https://deap.readthedocs.io/en/master/
.. _numpy: https://numpy.org/
.. _matplotlib: https://matplotlib.org/
.. _pandas: https://pandas.pydata.org/
.. _pyqt5: https://www.riverbankcomputing.com/static/Docs/PyQt5/
.. _scikit-learn: https://scikit-learn.org/stable/
.. _scipy: https://scipy.org/
.. _spyder: https://www.spyder-ide.org/


We recommend creating an anaconda virtual environment with the aforementioned
packages installed and running the code in Spyder.
A packaged executable for SMA-REACT is in development.





