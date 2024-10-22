# SMA REACT
SMA-REACT is an open-source, (hopefully) easy-to-use
tool for processing shape memory alloy experimental data and calibrating a constitutive model for use in other analyses(e.g., Abaqus).
Data processing and model calibration are presented in the form of a python GUI, allowing those unfamiliar with the intricate details of SMA constitutive modeling to easily calibrate appropriate models without writing their own custom subroutines. 

## Downloads

SMA REACT is released on [PyPi](https://pypi.org/project/SMA-REACT/). You can also build the package from source.

## Documentation

See the [SMA REACT User's Guide](smareact.readthedocs.io) for the full documentation. You can also build the documentation locally by navigating to the ``docs`` subfolder and running the command ``.\make.bat html``.
The documentation will be located under ``docs\_build\html``.

## Requirements

SMA-REACT is compatible with Python 3.9 and is built
with pyqt5, version 5.15.10. 
Here is a complete list of dependencies:

   * [deap](https://deap.readthedocs.io/en/master/)
   * [matplotlib](https://matplotlib.org/)
   * [numpy](https://numpy.org/)
   * [pandas](https://pandas.pydata.org/)
   * [pyqt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
   * [scikit-learn](https://scikit-learn.org/stable/)
   * [scipy](https://scipy.org/)

## How to cite SMA REACT
Authors of scientific papers including results generated using SMA-REACT are encouraged to cite the following paper.

```xml
@article{walgren_pre-print_2024,
	title = {[{PRE}-{PRINT}] {The} {Shape} {Memory} {Alloy} {Rendering} and {Calibration} {Tool} ({SMA}-{REACT})},
	journal = {Shape Memory and Superelasticity},
	author = {Walgren, Patrick and Mingear, Jacob},
	year = {2024},
}
```


