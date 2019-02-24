==========
Change Log
==========

v1.0.0, 11-10-2013
------------------

- Initial release.

v1.0.1,  4-20-2014
------------------

- changes to DataViewx.

- changes to Fitter.

v1.0.2, 12-14-2014
------------------

- some changes to skill code

- added new basic modules:

  o pattern_alignment: compare two bit-patterns

  o syscall: simplified system call

- added new classes:
  
  o DialogBase: dialog base class with fixed font

  o MessageDialog: message dialog for analysis reports

  o FormulaCalculator: formula gui calculator class

- Calc:

  o fix binding problem

- Data:

  o read_hspice : read binary, other fixes
 
  o read_nutmeg : partially written data-file read-in

  o added new methods: delays, skews, period_time_average

  o modified jitter analysis

- DataViewx:

  o add analyses: INL/DNL, period-time-average

  o added MessageDialog to DataViewx analysis reports

- PlotBase:

  o add new windowing bindings

  o other minor fixes

- Tckt:

  o architectural changes

  o fixed several issues

- interpolate:

  o fix dictionary issue

- range_sample:

  o fix random issue

v1.0.3,  4-14-2015
------------------

- added new classes:

  o StatusDialog

  o Balloonhelp

- Data.py

  o fix csv file detector

  o cxmag method: don't use set method which might have trouble with
    names which are numbers

  o add write_vcsv method: Cadence VCSV-format

  o revise/fix read_psf method

- DataViewx.py

  o add file->write VCSV-format

  o add file->rename columns

  o revise command parameter to include -x directive 

  o add y-target and x-target specifications for linear regression

  o add hex report of analog to digital parameters

- DialogBase.py

  o revise windows, resizable height only

- NGspice.py

  o add simulator configuration option (HSpice, NGspice)

  o file menu options: add write NGspice circuit file

  o edit menu: add simulator radiobuttons

  o fix xcol, ycols plotting 

- Pattern.py

  o revise/correct PRBS pattern generator

- PlotBase.py

  o add x- and y-spread to line-parameters report

  o add more information for vertical lines

- Report.py

  o add date and user methods

- SelectionDialog.py

  o add entry_emacs_bindings to entry windows

- Tckt.py

  o Fix spectre instance regular expression

  o Fix spectre sine source 

v1.0.4,  3-12-2017
------------------

- added new classes:

  o Itemizer

  o CanvasIdentify

- Data.py and Dataviewx.py

  o Add interpolation of other columns to periods

  o added read_touchstone method

  o added THD analysis

  o fix low-pass filter

  o add rescale/overlay operation

  o add advance/delay operation

  o dY/dX binary method -> deriv

- Tckt.py

  o Add case2ckey method

- StatusDialog.py

  o Fix update option

- MessageDialog.py

  o add write button/function

- PlotBase.py

  o Add/Change annotation bitmaps

  o Add CanvasIdentify curve identifier, and turn-on/turn-off in settings

- PlotBasem.py, DataViewm.py, XYplotm.py, and Plotterm.py

  o Plots using matplotlib

v1.0.5,  6-19-2017
------------------

- re-release, since doc directory and CHANGES.txt didn't get uploaded

v1.0.6,  5-28-2018
------------------

- matplotlib is default: added flyback removal

- Data.py

  o Add append_numpy_array method

  o Revise read_touchstone method

  o Revise moving-average filter method

  o add "no window" for FFT

  o add header_lines_to_skip argument to read_ssv method

- DataViewm.py

  o Add matplotlib flyback line removal

  o For resize binding, add pending to prevent multiple calls while resizing

  o Add "dots and narrow lines" to settings window

  o Add "S" and "s" key-bindings for toggling squares and dots

- Itemizer.py

  o Add __len__ method for number of experiments

v1.1.0,  1-01-2019
------------------

- add support for both Python 3 and Python 2.7

- clean up code

- added new class:

  o GetEntryDialog - replaces tkinter.simpledialog

- Data.py

  o add find_rows_where_equal method

  o add samples method

  o add read_vcsv method

  o jitter method: average frequency calculation - use average of steps

  o read_csv: set values to zero if not present

- DataViewm.py

  o minor fixes

- FrameNotebook.py

  o tabs set to fixed size, long names on balloon windows

- PlotBasem.py

  o minor changes

- SmithChart.py

  o fix extra parameter required for _plot_curves method

- Tckt.py

  o put back simulate_ngspice

  o op report changes for different versions of spectre

v1.1.1,  1-03-2019
------------------

- re-release, minor correction to setup.py and test_all

v1.1.2,  1-03-2019
------------------

- re-release, minor correction to setup.py and Tckt.py

v1.1.3,  1-03-2019
------------------

- re-release, doc correction to setup.py
