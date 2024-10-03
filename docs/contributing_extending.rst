Contributing to or extending SMA-REACT
======================================

The current version of SMA-REACT begs for many more enhancements. 
Different loading conditions (i.e., superelasticity), different model formulations (i.e., the Brinson or extended Lagoudas models), and alternative optimization routines all could provide benefits for the SMA community. 
If you are interested in contributing to SMA-REACT, please raise an issue on GitHub, and the developers will coordinate the best way to incorporate your feature. 
This section will describe the skeleton of how to add functionality to the GUI and the sections of code for the possible enhancements listed above.

Preliminaries
-------------

SMA-REACT is built on the pyqt5_ graphical user interface package.
PyQt functions as the software front-end (i.e., all interactive elements), while the Lagoudas model and optimization codes form the back-end.
Any new feature must be reflected in both the front- and back-ends, and hence requires knowledge of both. 
Thankfully, PyQt is an intuitive object-oriented package, so adding front-end elements is not too arduous.
Here are a few helpful tutorials and articles on various components:

    * Dropdown_ boxes, or combo boxes, are good to allow the user to pick between multiple discrete options.
    * lineEdits_ enable the user to input a value or string.
    * Labels_ are, as the name suggest, non-editable labels for various entities.
    * Layouts_ are important to properly organize all of your GUI entities.

.. _pyqt5: https://www.riverbankcomputing.com/static/Docs/PyQt5/
.. _Dropdown: https://www.tutorialspoint.com/pyqt/pyqt_qcombobox_widget.htm
.. _lineEdits: https://www.tutorialspoint.com/pyqt/pyqt_qlineedit_widget.htm
.. _Labels: https://www.tutorialspoint.com/pyqt/pyqt_qlabel_widget.htm
.. _Layouts: https://www.tutorialspoint.com/pyqt/pyqt_layout_management.htm


Accepting different input file types
------------------------------------

Currently, SMA-REACT uses the ``pandas.read_csv()`` function with ``sep=None`` to load experimental data.
As such, the tool can only load tab-delimited text files robustly. 
To accomodate other file formats, the following modifications could be performed:

    * Add a Dropdown_ on the  :mod:`~data_input.create_data_input`  tab to add an input option.
    * Modify the :func:`~data_input.create_data_input.DataInputWidget.open_files` and :func:`~data_input.create_data_input.DataInputWidget.load_files` functions to accept different inputs (via if-else or otherwise).
  

Reformulating for different loading conditions (i.e., superelasticity)
----------------------------------------------------------------------

The current model formulation calibrates isobaric experimental cycles by predicting strain as a function of applied temperature and stress.
It also assumes the material starts in Martensite; :func:`~data_input.create_data_input.DataInputWidget.load_files` performs the reorganization of experimental data to arrange the thermal cycles to run from cold to hot.
For superelastic characterization cycles, the material stress should be predicted as a function of temperature and strain. 
This requires a few distinct modifications:

    * Add a Dropdown_ on the :mod:`~data_input.create_data_input` tab to delineate between isobaric and isothermal experimental data.
    * Modify the :func:`~data_input.create_data_input.DataInputWidget.load_files` function to re-organize the experimental data with respect to strain, or to pass the raw data to the model.
    * Add a new model function to calculate the material stress as a function of temperature and strain. This may seem involved, but the model formulation is much simpler.
    * Change the :mod:`~calibration_progress.create_calibration_progress_widget` figures to reflect superelastic behavior (i.e., change the temperature-strain plot to a temperature-stress plot).

Adding another model formulation
--------------------------------

The Lagoudas one-dimensional constitutive model is one of many different options popular in the SMA community.
Alternative modeling approaches include the Brinson model :cite:p:`brinson_one-dimensional_1993`, the Aurrichio model :cite:p:`auricchio_sma_2009`, and various extensions for plasticity :cite:p:`scalet_three-dimensional_2019`, finite deformation :cite:p:`xu_finite_2021`, and other phenomena.
No matter the particular model you wish to include, the process we will detail below will be the same (if you have access to the model source code in python).

    * Add a Dropdown_ on the :mod:`~data_input.create_data_input` tab to allow the user pick between different model formulations.
    * Modify the :class:`~calibration.create_calibration_parameters.CalibrationParametersWidget` function (associated with the calibration parameters tab) to include the model parameters required for your chosen formulation. This would probably be best implemented in an if-else format.
    * Change :func:`~calibration.model_funcs.optimizer.main` to accomodate these different model parameters.
    * Include another if-else statement in :func:`~calibration.model_funcs.optimizer.evaluate` to call your chosen model formulation. If your model formulation returns a strain history given temperature and stress histories, this involves adding an if-else statement at the location where the current source code calls :func:`~calibration.model_funcs.Full_Model_stress`.
    * Be sure to modify the :mod:`~calibration_progress.create_calibration_progress_widget` figures to include any unique model parameters.

Including other optimization schemes
------------------------------------

The current tool uses the Non-Sorting Genetic Algorithm (II) and Sequential-Least-Squares Quadratic Programming Algorithms to optimize the calibration.
However, these algorithms are not "optimal" in any sense; rather, they were selected out of developer laziness for being "good enough."
If you are interested in implementing alternative optimization schemes that you feel would be better for calibration, follow these steps:

    * Add a Dropdown_ on the :class:`~calibration.create_calibration_parameters.CalibrationParametersWidget` tab to allow the user to select algorithms.
    * Add extra lineEdits_ on the :class:`~calibration.create_calibration_parameters.CalibrationParametersWidget` tab if there are other optimization parameters that need specified.
    * Add the necessary code to :mod:`~calibration.model_funcs.optimizer` to call your optimization of choice.

Adding more result export options
---------------------------------

SMA-REACT currently can export all relevant optimization results to a JSON. 
See the :func:`~launch_GUI.App.export_solution` for more information about the particular export quantities. 
If you would like to tailor the GUI to export a particular file format, follow these steps:

    * Add a Dropdown_ on the :mod:`~calibration_progress.create_calibration_progress_widget` tab to accomodate different export options.
    * Modify the :func:`~launch_GUI.App.export_solution` function to export different quantities depending on the aforementioned dropdown.





