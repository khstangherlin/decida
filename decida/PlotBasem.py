################################################################################
# CLASS    : PlotBasem
# PURPOSE  : Plot base class - using matplotlib
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:23:19 2013
# -----------------------------------------------------------------------------
# NOTES    :
#
# LICENSE  : (BSD-new)
#
# This software is provided subject to the following terms and conditions,
# which you should read carefully before using the software.  Using this
# software indicates your acceptance of these terms and conditions.  If you
# do not agree with these terms and conditions, do not use the software.
#
# Copyright (c) 2013 Richard Booth. All rights reserved.
#
# Redistribution and use in source or binary forms, with or without
# modifications, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following Disclaimer
#       in each human readable file as well as in the documentation and/or
#       other materials provided with the distribution.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following Disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Richard Booth nor the names of contributors
#       (those who make changes to the software, documentation or other
#       materials) may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# Disclaimer
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, INFRINGEMENT AND THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# ANY USE, MODIFICATION OR DISTRIBUTION OF THIS SOFTWARE IS SOLELY AT THE
# USERS OWN RISK.  IN NO EVENT SHALL RICHARD BOOTH OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, INCLUDING,
# BUT NOT LIMITED TO, CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# IN NO EVENT SHALL THE AUTHORS OR DISTRIBUTORS BE LIABLE TO ANY PARTY
# FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
# ARISING OUT OF THE USE OF THIS SOFTWARE, ITS DOCUMENTATION, OR ANY
# DERIVATIVES THEREOF, EVEN IF THE AUTHORS HAVE BEEN ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# THE AUTHORS AND DISTRIBUTORS SPECIFICALLY DISCLAIM ANY WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.  THIS SOFTWARE
# IS PROVIDED ON AN "AS IS" BASIS, AND THE AUTHORS AND DISTRIBUTORS HAVE
# NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
# MODIFICATIONS.
################################################################################
from __future__ import print_function
from builtins import str
from builtins import zip
from builtins import range
from builtins import object
import sys
import os
import os.path
import stat
import re
import math
import subprocess
import warnings
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import tkinter.colorchooser
import numpy
from decida.entry_emacs_bindings import entry_emacs_bindings
from decida.ItclObjectx import ItclObjectx
from decida.Data import Data
from decida.SelectionDialog import SelectionDialog
from decida.GetEntryDialog import GetEntryDialog
from decida.MessageDialog import MessageDialog
from decida.CanvasIdentify import CanvasIdentify
try:
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    from matplotlib.path import Path
    from matplotlib.patches import PathPatch
    from matplotlib.legend_handler import HandlerLine2D
    from matplotlib.lines import Line2D
    have_matplotlib = True
except:
    have_matplotlib = False

class PlotBasem(ItclObjectx, tk.Frame) :
    """
    **synopsis**:

        2-dimensional plot base class.

        *PlotBasem* is a base class for 2-D plotting classes. It provides
        a central canvas for displaying the plot, controls for changing aspects
        of the plot, point display boxes, and mouse commands for zooming,
        annotating, and determining line-parameters.

        *PlotBasem* provides its own vector (Hershey) fonts, which can
        be rotated, slanted, and sized.  The tk canvas does provide a
        font set, but with some limitations.

        *PlotBasem* is inherited by *XYplotm*, *Histogramx*, *Contourx*,
        and *Smithchartx*.

    **configuration options**:

        **verbose** (bool, default=False)

              enable/disable verbose mode

        **title** (str, default="")

              main title

        **xtitle** (str, default="")

              x-axis title

        **ytitle** (str, default="")

              y-axis title

        **plot_height** (str, default="10i" for MacOS, else "6i")

              Height of plot window (Tk inch or pixel specification)

        **plot_width** (str, default="10i" for MacOS, else "6i")

              Width of plot window (Tk inch or pixel specification)

        **plot_background** (str, default="GhostWhite")

              Background color of plot window

        **legend_background** (str, default="AntiqueWhite2")

              Background color of legend

        **colors** (list of str, default=[
                "blue", "red", "green", "orange", "cyan",
                "brown", "black", "blue violet", "cadet blue",
                "dark cyan", "dark goldenrod", "dark green",
                "dark magenta", "dark olive green", "dark orange",
                "dark red", "dark slate blue", "dark slate gray",
                "dodger blue", "forest green", "steel blue", "sienna"])

              list of colors for curves.
              Used to populate color menu, and to specify curve colors
              in scripted "command" option in derived classes.

        **symbols** (list of str, default = [
                "none", "dot", "square", "diamond",
                "triangle", "itriangle",
                "dash", "pipe", "plus", "cross",
                "spade", "heart", "diam", "club", "shamrock",
                "fleurdelis", "circle", "star"])

              list of symbols for curves.
              Used to populate symbol menu, and to specify curve symbols
              in scripted "command" option in derived classes.

        **ssizes** (list of float, default = [0.01])

              list of symbol sizes for curves.
              Used to specify curve symbol sizes
              in scripted "command" option in derived classes.

        **wlines** (list of int, default = [1])

              list of line widths for curves.
              Used to specify curve line widths
              in scripted "command" option in derived classes.

        **traces** (list, default = ["increasing"])

              list of traces for curves.  each trace can be one of:
              "increasing", "decreasing", or "both".
              Used to specify curve trace directions
              in scripted "command" option in derived classes.

        **xaxis** (str, default="lin")

              linear or logarithmic axis: "lin" or "log"

        **yaxis** (str, default="lin")

              linear or logarithmic axis: "lin" or "log"

        **xmin** (float, default=0.0)

              xaxis minimum

        **xmax** (float, default=0.0)

              xaxis maximum

        **ymin** (float, default=0.0)

              yaxis minimum

        **ymax** (float, default=0.0)

              yaxis maximum

        **grid** (bool, default=True)

              if true, show grid on plot

        **legend** (bool, default=True)

              if true, show legend on plot

        **postscript** (bool, default=False)

              if true, generate a PostScript file.

        **postscript_file** (str, default="plot.ps")

              name of PostScript file to plot to

        **wait** (bool, default=False)

              wait in main-loop until window is destroyed.

        **destroy** (bool, default=False)

              destroy main window after it has been displayed.
              useful for displaying, generating PostScript, then
              destroying window.

    **protected methods**:

        * _plot_curves

        * _settings_cmd

    **public methods**:

        * public methods from *ItclObjectx*

    """
    _string_data_nchar = None
    _string_data_code = {}
    _string_data_fo = []
    _string_data_fx = []
    _string_data_fy = []
    _bm_R = None
    _bm_L = None
    _bm_U = None
    _bm_D = None
    _bm_xo = None
    _bm_yo = None
    _bm_ao = None
    _bm_ai = None
    _bm_az = None
    __redraw_pending = None
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PlotBasem main
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, parent=None, use_matplotlib=True) :
        ItclObjectx.__init__(self)
        #----------------------------------------------------------------------
        # private variables:
        #----------------------------------------------------------------------
        self.__parent      = parent
        self.__use_matplotlib = use_matplotlib
        if not have_matplotlib:
            self.__use_matplotlib = False
        self._Component    = {}
        self._curves       = []
        self._curve_dname  = {}
        self._curve_xname  = {}
        self._curve_yname  = {}
        self._curve_trace  = {}
        self._curve_color  = {}
        self._curve_symbol = {}
        self._curve_ssize  = {}
        self._curve_wline  = {}
        self._curve_xdata  = {}
        self._curve_ydata  = {}
        self._curve_lstate = {}
        self._curve_sstate = {}
        self._plot_title_margin     = 0.035
        self._plot_title_height     = 0.028
        self._plot_title_font       = 2
        self._legend_label_height   = 0.015
        self._legend_box_width      = 0.250
        self._legend_box_margin     = 0.005
        self._legend_pad_margin     = 0.010
        self._legend_font           = 0
        self._xaxis_top             = False
        self._xaxis_value_angle     = 90
        self._yaxis_right           = False
        self._yaxis_value_angle     = 0
        self._axes_left_margin      = 0.15
        self._axes_right_margin     = 0.05
        self._axes_bottom_margin    = 0.15
        self._axes_top_margin       = 0.05
        self._axes_title_margin     = 0.140
        self._axes_title_height     = 0.028
        self._axes_title_font       = 2
        self._axes_value_margin     = 0.015
        self._axes_value_height     = 0.015
        self._axes_value_font       = 0
        self._axes_value_format1    = "%g"
        self._axes_value_format2    = "%8.2e"
        self._axes_tics_outside     = False
        self._axes_major_tic_size   = 0.02
        self._axes_minor_tic_size   = 0.01
        self._annotate_arrow_spread = 8
        self._annotate_arrow_length = 0.05
        #elf._annotate_text_height  = 0.015
        #elf._annotate_text_height  = 0.030
        self._annotate_text_height  = 0.020
        self._annotate_text_font    = 2
        self._postscript_landscape  = True
        self.__XYwindows            = []
        self.__XYlimits             = [0, 10, 0, 10]
        self.__Annotate             = {}
        self.__annotate_index       = 0
        self.__crosshairs_highlighted  = False
        self.__dot_toggle_state = False
        self.__square_toggle_state = False
        self._cid_curve = {}
        self._curve_id = {}
        self._curve_sym_id = {}
        self._curve_label = {}
        self._curve_lgnd_line = {}
        self.__MatPlotLibSymbols = {
            "none": "",
            "dot": ".",
            "square": "s",
            "diamond": "D",
            "triangle": "^",
            "itriangle": "v",
            "dash": "_",
            "pipe": "|",
            "plus": "+",
            "cross": "X",
            "spade": r"$\spadesuit$",
            "heart": r"$\heartsuit$",
            "diam":  r"$\diamondsuit$",
            "club":  r"$\clubsuit$",
            "shamrock": u"$\u2618$",
            "fleurdelis": u"$\u269c$",
            "circle": "o",
            "star": "*"
        }
        self.__Transform = {}
        self.__current_curve = None
        self.__stretch_colors = None
        self.__stretch_func = None
        self.__toplevel = None
        self.__stretch_mode = None
        self.__stretch_func = None
        self.__stretch_id = None
        self.__stretch_u1 = 0
        self.__stretch_v1 = 0
        self.__stretch_u2 = 0
        self.__stretch_v2 = 0
        self._curve_lgnd_id = 0
        #----------------------------------------------------------------------
        # configuration options:
        #----------------------------------------------------------------------
        symbols = [
            "narrow line", "medium line", "wide line",
            "none", "dot", "square", "diamond", "triangle", "itriangle",
            "dash", "pipe", "plus", "cross",
            "spade", "heart", "diam", "club", "shamrock",
            "fleurdelis", "circle", "star"
        ]
        colors = [
            "blue", "red", "green", "orange", "cyan", "brown", "black",
            "blue violet", "cadet blue",
            "dark cyan", "dark goldenrod", "dark green",  "dark magenta",
            "dark olive green", "dark orange", "dark red", "dark slate blue",
            "dark slate gray", "dodger blue", "forest green",
            "steel blue", "sienna"
        ]
        if sys.platform == "darwin" :
            plot_width  = "8i"
            plot_height = "8i"
        else :
            plot_width  = "6i"
            plot_height = "6i"
        self._add_options({
            "verbose"          : [False, None],
            "title"            : ["", None],
            "xtitle"           : ["", None],
            "ytitle"           : ["", None],
            "plot_width"       : [plot_width, None],
            "plot_height"      : [plot_height, None],
            "plot_background"  : ["GhostWhite", self._config_plot_background_callback],
            "legend_background": ["AntiqueWhite2", self._config_legend_background_callback],
            "colors"           : [colors, None],
            "symbols"          : [symbols, None],
            "ssizes"           : [[0.01], None],
            "wlines"           : [[1], None],
            "traces"           : [["increasing"], None],
            "xaxis"            : ["lin", None],
            "yaxis"            : ["lin", None],
            "xmin"             : [0.0,   None],
            "xmax"             : [0.0,   None],
            "ymin"             : [0.0,   None],
            "ymax"             : [0.0,   None],
            "grid"             : [True,  self._config_grid_callback],
            "legend"           : [True,  self._config_legend_callback],
            "postscript"       : [False, None],
            "postscript_file"  : ["plot.ps", None],
            "wait"             : [True, None],
            "destroy"          : [False, None],
        })
        #---------------------------------------------------------------------
        # read string data and create bitmaps
        #---------------------------------------------------------------------
        if not PlotBasem._string_data_nchar :
            PlotBasem.__plot_read_string_data()
        if not PlotBasem._bm_R :
            PlotBasem.__plot_create_bitmaps()
    #==========================================================================
    # METHOD  : __del__
    # PURPOSE : destructor
    #==========================================================================
    def __del__(self) :
        if self.__toplevel :
            self.__toplevel.destroy()
        else :
            self.destroy()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PlotBasem configuration option callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _config_plot_background_callback
    # PURPOSE : plot background
    #==========================================================================
    def _config_plot_background_callback(self) :
        plot = self._Component["plot"]
        plot_background = self["plot_background"]
        plot["background"] = plot_background
    #==========================================================================
    # METHOD  : _config_legend_background_callback
    # PURPOSE : legend background
    #==========================================================================
    def _config_legend_background_callback(self) :
        plot = self._Component["plot"]
        legend_background = self["legend_background"]
        plot.itemconfigure("LEGEND-BOX", fill=legend_background, outline="")
    #==========================================================================
    # METHOD  : _config_grid_callback
    # PURPOSE : show/hide grid
    #==========================================================================
    def _config_grid_callback(self) :
        grid = self["grid"]
        if not grid in [True, False] :
            self.warning("grid\"" + "\" not correctly specified")
            return False
        return True
    #==========================================================================
    # METHOD  : _config_legend_callback
    # PURPOSE : show/hide legend
    #==========================================================================
    def _config_legend_callback(self) :
        legend = self["legend"]
        if not legend in [True, False] :
            self.warning("legend\"" + "\" not correctly specified")
            return False
        return True
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PlotBasem GUI
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _gui
    # PURPOSE : build graphical user interface
    #==========================================================================
    def _gui(self) :
        self.__stretch_mode = None
        self.__stretch_func = None
        self.__stretch_id = None
        self.__stretch_u1 = 0
        self.__stretch_v1 = 0
        self.__stretch_u2 = 0
        self.__stretch_v2 = 0
        self.__stretch_colors = {
            "zoom": "LightSteelBlue2",
            "delete": "Red",
            "report": "Green",
            "label": "LightSteelBlue2",
        }
        #----------------------------------------------------------------------
        # top-level:
        #----------------------------------------------------------------------
        if self.__parent is None:
            self.__toplevel = tk.Toplevel()
            tk.Frame.__init__(self, self.__toplevel, class_ = "PlotBasem")
            if not self.was_configured("wait") :
                self["wait"] = True
        else:
            self.__toplevel = None
            tk.Frame.__init__(self, self.__parent,   class_ = "PlotBasem")
            if not self.was_configured("wait") :
                self["wait"] = False
        self.pack(side="top", fill="both", expand=True)
        #----------------------------------------------------------------------
        # option database:
        #----------------------------------------------------------------------
        if sys.platform == "darwin" :
            self.option_add("*PlotBasem*Menubutton.width", 12)
            self.option_add("*PlotBasem*Menubutton.relief", "raised")
            self.option_add("*PlotBasem*Menubutton.bd", 2)
            self.option_add("*PlotBasem*Label.width", 10)
            self.option_add("*PlotBasem*Label.anchor", "e")
            self.option_add("*PlotBasem*Label.relief", "sunken")
            self.option_add("*PlotBasem*Label.bd", 2)
            self.option_add("*PlotBasem*Checkbutton.width", 8)
            self.option_add("*PlotBasem*Checkbutton.anchor", "w")
            self.option_add("*PlotBasem*Checkbutton.bd", 2)
            self.option_add("*PlotBasem*Checkbutton.relief", "raised")
            self.option_add("*PlotBasem*Checkbutton.highlightThickness", 0)
            self.option_add("*PlotBasem*Button.highlightThickness", 0)
            self.option_add("*PlotBasem*Button.width", 6)
            self.option_add("*PlotBasem*Button.height", 1)
            self.option_add("*PlotBasem*Entry.width", 15)
            self.option_add("*PlotBasem*Entry.font", "Courier 16 bold")
        else :
            self.option_add("*PlotBasem*Menubutton.width", 12)
            self.option_add("*PlotBasem*Menubutton.relief", "raised")
            self.option_add("*PlotBasem*Menubutton.bd", 2)
            self.option_add("*PlotBasem*Label.width", 10)
            self.option_add("*PlotBasem*Label.anchor", "e")
            self.option_add("*PlotBasem*Label.relief", "sunken")
            self.option_add("*PlotBasem*Label.bd", 2)
            self.option_add("*PlotBasem*Checkbutton.width", 12)
            self.option_add("*PlotBasem*Checkbutton.anchor", "w")
            self.option_add("*PlotBasem*Checkbutton.bd", 2)
            self.option_add("*PlotBasem*Checkbutton.relief", "raised")
            self.option_add("*PlotBasem*Checkbutton.highlightThickness", 0)
            self.option_add("*PlotBasem*Button.highlightThickness", 0)
            self.option_add("*PlotBasem*Button.width", 4)
            self.option_add("*PlotBasem*Button.height", 1)
            self.option_add("*PlotBasem*Entry.width", 20)
            self.option_add("*PlotBasem*Entry.font", "Courier 12 bold")
        #----------------------------------------------------------------------
        # main layout
        #----------------------------------------------------------------------
        mbar = tk.Frame(self, relief="raised", bd=3)
        mbar.pack(side="top", fill="x")
        head = tk.Frame(self, relief="raised", bd=3)
        head.pack(side="top", fill="x")
        gfrm = tk.Frame(self, relief="raised", bd=3)
        gfrm.pack(side="top", expand=True, fill="both")
        main_color = "#1E90FF"
        mbar["background"] = main_color
        head["background"] = main_color
        gfrm["background"] = main_color
        #----------------------------------------------------------------------
        # menu-bar
        #----------------------------------------------------------------------
        file_mb = tk.Menubutton(mbar, text="File")
        file_mb.pack(side="left", padx=10, pady=10)
        edit_mb = tk.Menubutton(mbar, text="Edit")
        edit_mb.pack(side="left", padx=10, pady=10)
        symb_mb = tk.Menubutton(mbar, text="Symbol")
        symb_mb.pack(side="left", padx=10, pady=10)
        colr_mb = tk.Menubutton(mbar, text="Color")
        colr_mb.pack(side="left", padx=10, pady=10)
        curv_mb = tk.Menubutton(mbar, text="Curve")
        curv_mb.pack(side="left", padx=10, pady=10)
        file_menu= tk.Menu(file_mb)
        edit_menu= tk.Menu(edit_mb)
        symb_menu= tk.Menu(symb_mb)
        colr_menu= tk.Menu(colr_mb)
        curv_menu= tk.Menu(curv_mb)
        file_mb["menu"]=file_menu
        edit_mb["menu"]=edit_menu
        symb_mb["menu"]=symb_menu
        colr_mb["menu"]=colr_menu
        curv_mb["menu"]=curv_menu
        self._Component["file_menu"]=file_menu
        self._Component["edit_menu"]=edit_menu
        self._Component["symb_menu"]=symb_menu
        self._Component["colr_menu"]=colr_menu
        self._Component["curv_menu"]=curv_menu
        #----------------------------------------------------------------------
        # file menu
        #----------------------------------------------------------------------
        def write_post(self=self) :
            self.__postscript_write()
        def print_post(self=self) :
            self.__postscript_print()
        def print_spec(self=self) :
            self.__postscript_print(specify=True)
        file_menu.add_command(
            label="Write PostScript File",
            command=write_post)
        file_menu.add_command(
            label="Write and Print PostScript File",
            command=print_post)
        file_menu.add_command(
            label="Write and Print PostScript File (specify print command)",
            command=print_spec)
        file_menu.add_separator()
        file_menu.add_command(
            label="Quit",
            command=self.__quit_cmd)
        #----------------------------------------------------------------------
        # edit menu
        #----------------------------------------------------------------------
        def autox_cmd(self=self) :
            self.autoscale(autoscale_x=True,  autoscale_y=False, strict=True)
        def autoy_cmd(self=self) :
            self.autoscale(autoscale_x=False, autoscale_y=True,  strict=True)
        def autoxy_cmd(self=self) :
            self.autoscale(autoscale_x=True,  autoscale_y=True,  strict=True)
        def delete_curve_cmd(self=self) :
            curve = self.current_curve()
            self.delete_curve(curve)
        self._Component["curve_trace_var"]  = tk.StringVar()
        self._Component["curve_points_var"] = tk.StringVar()
        self._Component["curve_stack_var"]  = tk.StringVar()
        edit_menu.add_command(
            label="Settings",
            command=self._settings_cmd)
        edit_menu.add_separator()
        edit_menu.add_radiobutton(
            label="Trace increasing",
            command=self.__curve_trace_cmd,
            variable=self._Component["curve_trace_var"],
            value="increasing")
        edit_menu.add_radiobutton(
            label="Trace decreasing",
            command=self.__curve_trace_cmd,
            variable=self._Component["curve_trace_var"],
            value="decreasing")
        edit_menu.add_radiobutton(
            label="Trace both",
            command=self.__curve_trace_cmd,
            variable=self._Component["curve_trace_var"],
            value="both")
        edit_menu.add_separator()
        edit_menu.add_radiobutton(
            label="All dots and narrow lines",
            command=self.__curve_points_cmd,
            variable=self._Component["curve_points_var"],
            value="dots and narrow lines")
        edit_menu.add_radiobutton(
            label="All dots",
            command=self.__curve_points_cmd,
            variable=self._Component["curve_points_var"],
            value="dots")
        edit_menu.add_radiobutton(
            label="All small squares",
            command=self.__curve_points_cmd,
            variable=self._Component["curve_points_var"],
            value="small squares")
        edit_menu.add_radiobutton(
            label="All medium squares",
            command=self.__curve_points_cmd,
            variable=self._Component["curve_points_var"],
            value="medium squares")
        edit_menu.add_radiobutton(
            label="All large squares",
            command=self.__curve_points_cmd,
            variable=self._Component["curve_points_var"],
            value="large squares")
        edit_menu.add_radiobutton(
            label="All narrow lines",
            command=self.__curve_points_cmd,
            variable=self._Component["curve_points_var"],
            value="narrow lines")
        edit_menu.add_radiobutton(
            label="All medium lines",
            command=self.__curve_points_cmd,
            variable=self._Component["curve_points_var"],
            value="medium lines")
        edit_menu.add_radiobutton(
            label="All wide lines",
            command=self.__curve_points_cmd,
            variable=self._Component["curve_points_var"],
            value="wide lines")
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Autoscale x",
            command=autox_cmd)
        edit_menu.add_command(
            label="Autoscale y",
            command=autoy_cmd)
        edit_menu.add_command(
            label="Autoscale both",
            command=autoxy_cmd)
        edit_menu.add_separator()
        edit_menu.add_command(
            label="Delete current curve",
            command=delete_curve_cmd)
        #----------------------------------------------------------------------
        # color menu
        #----------------------------------------------------------------------
        self._Component["curve_color_var"] = tk.StringVar()
        if self["colors"] :
            self._Component["curve_color_var"].set(self["colors"][0])
        colr_menu.add_command(
            label="choose curve color",
            command=self.__curve_choose_color_cmd)
        colr_menu.add_separator()
        for color in self["colors"] :
            colr_menu.add_radiobutton(
                label=color,
                variable=self._Component["curve_color_var"],
                value=color,
                command=self.__curve_color_cmd)
        #----------------------------------------------------------------------
        # symbol menu
        #----------------------------------------------------------------------
        self._Component["curve_symbol_var"] = tk.StringVar()
        if self["symbols"] :
            self._Component["curve_symbol_var"].set(self["symbols"][0])
        for symbol in self["symbols"] :
            symb_menu.add_radiobutton(
                label=symbol,
                variable=self._Component["curve_symbol_var"],
                value=symbol,
                command=self.__curve_symbol_cmd)
        #----------------------------------------------------------------------
        # curve menu
        # moved line and symbol state variables up
        #----------------------------------------------------------------------
        self._Component["curve_sstate_var"] = tk.IntVar()
        self._Component["curve_sstate_var"].set(1)
        self._Component["curve_lstate_var"] = tk.IntVar()
        self._Component["curve_lstate_var"].set(1)
        self._Component["curve_select_var"] = tk.StringVar()
        self.__current_curve = None
        if self._curves :
            self._Component["curve_select_var"].set(self._curves[0])
            self.__curve_select_cmd()
        for curve in self._curves :
            curv_menu.add_radiobutton(
                label=curve,
                variable=self._Component["curve_select_var"],
                value=curve,
                command=self.__curve_select_cmd)
        #----------------------------------------------------------------------
        # control frames
        #----------------------------------------------------------------------
        control1 = tk.Frame(head)
        control1.pack(side="top")
        control2 = tk.Frame(head)
        control2.pack(side="top")
        control3 = tk.Frame(head)
        control3.pack(side="top")
        #----------------------------------------------------------------------
        # checkbutton controls
        #----------------------------------------------------------------------
        func0 = tk.Checkbutton(control1)
        func0.pack(side="left", anchor="w", fill="y")
        func1 = tk.Checkbutton(control1)
        func1.pack(side="left", anchor="w", fill="y")
        func2 = tk.Checkbutton(control2)
        func2.pack(side="left", anchor="w", fill="y")
        func3 = tk.Checkbutton(control2)
        func3.pack(side="left", anchor="w", fill="y")
        func4 = tk.Checkbutton(control3)
        func4.pack(side="left", anchor="w", fill="y")
        func5 = tk.Checkbutton(control3)
        func5.pack(side="left", anchor="w", fill="y")
        self._Component["xlog_var"] = tk.IntVar()
        self._Component["xlog_var"].set(0)
        self._Component["ylog_var"] = tk.IntVar()
        self._Component["ylog_var"].set(0)
        self._Component["grid_var"] = tk.IntVar()
        self._Component["grid_var"].set(1)
        self._Component["lgnd_var"] = tk.IntVar()
        self._Component["lgnd_var"].set(1)
        if self["xaxis"] == "log":
            self._Component["xlog_var"].set(1)
        if self["yaxis"] == "log":
            self._Component["ylog_var"].set(1)
        if self["grid"] is False:
            self._Component["grid_var"].set(0)
        if self["legend"] is False:
            self._Component["lgnd_var"].set(0)
        func0["text"]     = "X log"
        func0["command"]  = self.__xlog_cmd
        func0["variable"] = self._Component["xlog_var"]
        func1["text"]     = "Y log"
        func1["command"]  = self.__ylog_cmd
        func1["variable"] = self._Component["ylog_var"]
        func2["text"]     = "Symbol"
        func2["command"]  = self.__symb_cmd
        func2["variable"] = self._Component["curve_sstate_var"]
        func3["text"]     = "Line"
        func3["command"]  = self.__line_cmd
        func3["variable"] = self._Component["curve_lstate_var"]
        func4["text"]     = "Grid"
        func4["command"]  = self._grid_cmd
        func4["variable"] = self._Component["grid_var"]
        func5["text"]     = "Legend"
        func5["command"]  = self._lgnd_cmd
        func5["variable"] = self._Component["lgnd_var"]
        self._Component["func0"]=func0
        self._Component["func1"]=func1
        self._Component["func2"]=func2
        self._Component["func3"]=func3
        self._Component["func4"]=func4
        self._Component["func5"]=func5
        #----------------------------------------------------------------------
        # panning/window controls
        #----------------------------------------------------------------------
        save_button = tk.Button(control1, text="Save")
        save_button.pack(side="left", anchor="w", fill="y")
        panO_button = tk.Button(control1, image=PlotBasem._bm_ao, width=20)
        panO_button.pack(side="left", anchor="w", fill="y")
        panI_button = tk.Button(control1, image=PlotBasem._bm_ai, width=20)
        panI_button.pack(side="left", anchor="w", fill="y")
        panZ_button = tk.Button(control1, image=PlotBasem._bm_az, width=20)
        panZ_button.pack(side="left", anchor="w", fill="y")
        rest_button = tk.Button(control2, text="Rest")
        rest_button.pack(side="left", anchor="w", fill="y")
        panL_button = tk.Button(control2, image=PlotBasem._bm_L,  width=20)
        panL_button.pack(side="left", anchor="w", fill="y")
        panR_button = tk.Button(control2, image=PlotBasem._bm_R,  width=20)
        panR_button.pack(side="left", anchor="w", fill="y")
        panX_button = tk.Button(control2, image=PlotBasem._bm_xo, width=20)
        panX_button.pack(side="left", anchor="w", fill="y")
        win0_button = tk.Button(control3, text="Wind-0")
        win0_button.pack(side="left", anchor="w", fill="y")
        panU_button = tk.Button(control3, image=PlotBasem._bm_U,  width=20)
        panU_button.pack(side="left", anchor="w", fill="y")
        panD_button = tk.Button(control3, image=PlotBasem._bm_D,  width=20)
        panD_button.pack(side="left", anchor="w", fill="y")
        panY_button = tk.Button(control3, image=PlotBasem._bm_yo, width=20)
        panY_button.pack(side="left", anchor="w", fill="y")
        def cmd_panO(self=self) :
            self.__pan_zoom("out")
        def cmd_panI(self=self) :
            self.__pan_zoom("in")
        def cmd_panL(self=self) :
            self.__pan_zoom("left")
        def cmd_panR(self=self) :
            self.__pan_zoom("right")
        def cmd_panU(self=self) :
            self.__pan_zoom("up")
        def cmd_panD(self=self) :
            self.__pan_zoom("down")
        def cmd_panX(self=self) :
            self.__pan_zoom("x")
        def cmd_panY(self=self) :
            self.__pan_zoom("y")
        def cmd_panZ(self=self) :
            self.__restore_view(win0=True)
        def cmd_rest(self=self) :
            self.__restore_view()
        def cmd_save(self=self) :
            self.__save_view()
        def cmd_win0(self=self) :
            self.__save_view(win0=True)
        def cmd_panSX(self=self) :
            self.__pan_zoom("sx")
        def cmd_panSY(self=self) :
            self.__pan_zoom("sy")
        save_button["command"] = cmd_save
        panO_button["command"] = cmd_panO
        panI_button["command"] = cmd_panI
        panZ_button["command"] = cmd_panZ
        rest_button["command"] = cmd_rest
        panL_button["command"] = cmd_panL
        panR_button["command"] = cmd_panR
        panX_button["command"] = cmd_panX
        win0_button["command"] = cmd_win0
        panU_button["command"] = cmd_panU
        panD_button["command"] = cmd_panD
        panY_button["command"] = cmd_panY
        #panX_button.bind("<ButtonRelease-3>", cmd_panSX)
        #panY_button.bind("<ButtonRelease-3>", cmd_panSY)
        self._Component["save"]=save_button
        self._Component["rest"]=rest_button
        self._Component["win0"]=win0_button
        #----------------------------------------------------------------------
        # coordinate-displays
        #----------------------------------------------------------------------
        lcoo= tk.Label(control1, text="Current:")
        lcoo.pack(side="left", anchor="w", fill="y")
        xcoo= tk.Entry(control1)
        xcoo.pack(side="left", anchor="e", fill="y")
        ycoo= tk.Entry(control1)
        ycoo.pack(side="left", anchor="e", fill="y")

        lmin= tk.Label(control2, text="Minimum:")
        lmin.pack(side="left", anchor="w", fill="y")
        xmin= tk.Entry(control2)
        xmin.pack(side="left", anchor="e", fill="y")
        ymin= tk.Entry(control2)
        ymin.pack(side="left", anchor="e", fill="y")

        lmax= tk.Label(control3, text="Maximum:")
        lmax.pack(side="left", anchor="w", fill="y")
        xmax= tk.Entry(control3)
        xmax.pack(side="left", anchor="e", fill="y")
        ymax= tk.Entry(control3)
        ymax.pack(side="left", anchor="e", fill="y")
        self._Component["xcoo"]=xcoo
        self._Component["xmin"]=xmin
        self._Component["xmax"]=xmax
        self._Component["ycoo"]=ycoo
        self._Component["ymin"]=ymin
        self._Component["ymax"]=ymax
        entry_emacs_bindings([xcoo, xmin, xmax, ycoo, ymin, ymax])
        #----------------------------------------------------------------------
        # coordinate-display bindings:
        #----------------------------------------------------------------------
        def xycoocmd(event, self=self) :
            self.__coord_set()
        def xmincmd(event, self=self) :
            self.__limit_set()
        def xmaxcmd(event, self=self) :
            self.__limit_set()
        def ymincmd(event, self=self) :
            self.__limit_set()
        def ymaxcmd(event, self=self) :
            self.__limit_set()
        xcoo.bind("<Return>", xycoocmd)
        ycoo.bind("<Return>", xycoocmd)
        xmin.bind("<Return>", xmincmd)
        xmax.bind("<Return>", xmaxcmd)
        ymin.bind("<Return>", ymincmd)
        ymax.bind("<Return>", ymaxcmd)
        #----------------------------------------------------------------------
        # create and pack canvas
        #----------------------------------------------------------------------
        if not self.__use_matplotlib:
            plot = tk.Canvas(gfrm, relief="sunken", bd=2)
        else:
            plot_figure = Figure(dpi=100)
            plot_canvas = FigureCanvasTkAgg(plot_figure, master=gfrm)
            plot = plot_canvas.get_tk_widget()
            plot["relief"] = "sunken"
            plot["bd"] = 2
            self._Component["plot_canvas"] = plot_canvas
            self._Component["plot_figure"] = plot_figure
        plot.pack(side="top", padx=2, pady=2, expand=True, fill="both")
        plot["background"] = self["plot_background"]
        plot["width"]      = self["plot_width"]
        plot["height"]     = self["plot_height"]
        self._Component["plot"]=plot
        #----------------------------------------------------------------------
        # canvas identify
        #----------------------------------------------------------------------
        widen = CanvasIdentify(plot, delay=100, background="#fcf87f")
        self._Component["identify"]=widen
        #----------------------------------------------------------------------
        # pan/zoom key bindings:
        #----------------------------------------------------------------------
        def focuscmd(event, self=self):
            event.widget.focus_set()
        def unfocuscmd(event, self=self):
            tk._default_root.focus_set()
        def panleftcmd(event, self=self):
            self.__pan_zoom("left")
        def panrightcmd(event, self=self):
            self.__pan_zoom("right")
        def pandowncmd(event, self=self):
            self.__pan_zoom("down")
        def panupcmd(event, self=self):
            self.__pan_zoom("up")
        def panfleftcmd(event, self=self):
            self.__pan_zoom("fleft")
        def panfrightcmd(event, self=self):
            self.__pan_zoom("fright")
        def panfdowncmd(event, self=self):
            self.__pan_zoom("fdown")
        def panfupcmd(event, self=self):
            self.__pan_zoom("fup")
        def panoutcmd(event, self=self):
            self.__pan_zoom("out")
        def panincmd(event, self=self):
            self.__pan_zoom("in")
        def autoscalecmd(event, self=self):
            self.autoscale(autoscale_x=True, autoscale_y=True, strict=True, redraw=True)
        def dot_toggle_cmd(event, self=self):
            self.__dot_toggle_state = not self.__dot_toggle_state
            self.__square_toggle_state = False
            curve = self.__current_curve
            if  self.__dot_toggle_state :
                self._curve_symbol[curve] = "dot"
            else :
                self._curve_symbol[curve] = "none"
            self._plot_redraw("dot_toggle")
        def square_toggle_cmd(event, self=self):
            self.__square_toggle_state = not self.__square_toggle_state
            self.__dot_toggle_state = False
            curve = self.__current_curve
            if  self.__square_toggle_state :
                self._curve_symbol[curve] = "square"
            else :
                self._curve_symbol[curve] = "none"
            self._plot_redraw("square_toggle")
        plot.bind("<Enter>",     focuscmd)
        plot.bind("<Leave>",     unfocuscmd)
        plot.bind("<Key-Left>",  panfleftcmd)
        plot.bind("<Key-Right>", panfrightcmd)
        plot.bind("<Key-Down>",  panfdowncmd)
        plot.bind("<Key-Up>",    panfupcmd)
        plot.bind("<Shift-Key-Left>",   panleftcmd)
        plot.bind("<Shift-Key-Right>",  panrightcmd)
        plot.bind("<Shift-Key-Down>",   pandowncmd)
        plot.bind("<Shift-Key-Up>",     panupcmd)
        plot.bind("<Key-bracketleft>",  panoutcmd)
        plot.bind("<Key-bracketright>", panincmd)
        plot.bind("<Key-f>",     autoscalecmd)
        plot.bind("<Key-s>",     dot_toggle_cmd)
        plot.bind("<Key-S>",     square_toggle_cmd)
        #----------------------------------------------------------------------
        # mouse 1: zoom operation
        #----------------------------------------------------------------------
        def cmdz1(event, self=self):
            self.begin_stretch("zoom", self.__stretch_zoom, event.x, event.y)
        def cmdz2(event, self=self):
            self.continue_stretch(event.x, event.y)
        def cmdz3(event, self=self):
            self.end_stretch(event.x, event.y)
        plot.bind("<ButtonPress-1>",   cmdz1)
        plot.bind("<B1-Motion>",       cmdz2)
        plot.bind("<ButtonRelease-1>", cmdz3)
        #----------------------------------------------------------------------
        # shift-mouse 1: delete labels operation
        #----------------------------------------------------------------------
        def cmd0(event, self=self):
            self.begin_stretch("delete", self.__stretch_delete, event.x, event.y)
        plot.bind("<Shift-ButtonPress-1>", cmd0)
        #----------------------------------------------------------------------
        # mouse 2: zoom back to originally autoscaled window
        #----------------------------------------------------------------------
        def cmd1(event, self=self):
            self.__restore_view(win0=True)
        plot.bind("<ButtonPress-2>", cmd1)
        #----------------------------------------------------------------------
        # mouse 3: straightedge operation
        #----------------------------------------------------------------------
        def cmd2(event, self=self):
            self.begin_stretch("report", self.__stretch_report, event.x, event.y)
        def cmd3(event, self=self):
            self.continue_stretch(event.x, event.y)
        def cmd4(event, self=self):
            self.end_stretch(event.x, event.y)
        plot.bind("<ButtonPress-3>",   cmd2)
        plot.bind("<B3-Motion>",       cmd3)
        plot.bind("<ButtonRelease-3>", cmd4)
        #----------------------------------------------------------------------
        # shift-mouse 3: label operation
        #----------------------------------------------------------------------
        def cmd5(event, self=self):
            self.begin_stretch("label", self.__stretch_label, event.x, event.y)
        plot.bind("<Shift-ButtonPress-3>", cmd5)
        #----------------------------------------------------------------------
        # draw plot and curves
        # need to establish limits before axes, curves plotted
        #----------------------------------------------------------------------
        self.__plot_curve_limits()
        self._plot_redraw("orig")
        self.__save_view(win0=True)
        #----------------------------------------------------------------------
        # plot bindings:
        #----------------------------------------------------------------------
        def cmd6(event, self=self):
            if not self.__redraw_pending :
                def rdcmd(self=self) :
                    self._plot_redraw("resize")
                self.__redraw_pending = self.after_idle(rdcmd)
            self._plot_transform_calc()
        if not self.__use_matplotlib:
            plot.bind("<Configure>", cmd6)
        else :
            plot_canvas._resize_callback = cmd6
        def cmd7(event, self=self):
            self.__update_coord_display(event.x, event.y)
        plot.bind("<Motion>", cmd7)
    #==========================================================================
    # METHOD  : _mainloop
    # PURPOSE : update, mainloop
    #==========================================================================
    def _mainloop(self) :
        self.update()
        if self["postscript"] :
            self.__postscript_write(self["postscript_file"])
        if self["wait"] :
            self.wait_window()
        if self["destroy"] :
            if self.__toplevel :
                self.__toplevel.destroy()
            else :
                self.destroy()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PlotBasem user commands:
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : plot_window
    # PURPOSE : return plot window (canvas)
    #==========================================================================
    def plot_window(self) :
        """ return plot window (canvas).

        **results**:

            * Returns the handle to the current plot window.

        """
        plot = self._Component["plot"]
        return plot
    #==========================================================================
    # METHOD  : curves
    # PURPOSE : return list of curves
    # NOTES   :
    #     * must make copy of curve list
    #==========================================================================
    def curves(self) :
        """ return list of curves.

        **results**:

            * Returns the list of curve id's in the plot.

        """
        return list(self._curves)
    #==========================================================================
    # METHOD  : current_curve
    # PURPOSE : set or return current curve
    #==========================================================================
    def current_curve(self, curve=None) :
        """ return the current curve.

        **results**:

            * Returns the current curve id.

        """
        if curve is None :
            return self.__current_curve
        else :
            self._Component["curve_select_var"].set(curve)
            self.__curve_select_cmd()
            self.__symb_cmd()
            self.__line_cmd()
        return None
    #==========================================================================
    # METHOD  : limits
    # PURPOSE : return plot limits
    #==========================================================================
    def limits(self) :
        """ return plot limits.

            **results**:

                * returns a list of the current plotting limits:
                  [xmin, xmax, ymin, ymax]

        """
        return list(self.__XYlimits)
    #==========================================================================
    # METHOD  : curve_attributes
    # PURPOSE : return curve attributes
    #==========================================================================
    def curve_attributes(self, curve):
        """ return curve attributes.

        **arguments**:

            **curve** (str)

                The curve id is in the format (see add_curve):
                <data_name>\_:_<ycol>_vs_<xcol>
                If data_name is undefined, it is set to "data_1"

        **results**:

            * Returns a list of curve attributes in the Dictionary V:

                * V["dname"]  = data name (str)

                * V["xname"]  = x-column name (str)

                * V["yname"]  = y-column name (str)

                * V["color"]  = curve color (str)

                * V["symbol"] = curve symbol (str)

                * V["ssize"]  = curve symbol size (int)

                * V["wline"]  = curve line-width (int)

                * V["trace"]  = trace direction (str)
                  ("increasing", "decreasing", or "both")

                * V["lstate"] = line display state (bool)

                * V["sstate"] = symbol display state (bool)

        """
        if not curve in self._curves :
            self.warning("curve %s not in curves" % (curve))
            return None
        V = {}
        V["dname"]  = self._curve_dname[curve]
        V["xname"]  = self._curve_xname[curve]
        V["yname"]  = self._curve_yname[curve]
        V["color"]  = self._curve_color[curve]
        V["symbol"] = self._curve_symbol[curve]
        V["ssize"]  = self._curve_ssize[curve]
        V["wline"]  = self._curve_wline[curve]
        V["trace"]  = self._curve_trace[curve]
        V["lstate"] = self._curve_lstate[curve]
        V["sstate"] = self._curve_sstate[curve]
        return V
    #==========================================================================
    # METHOD  : autoscale
    # PURPOSE : find limits and autoscale plot
    #==========================================================================
    def autoscale(self, autoscale_x=False, autoscale_y=True,
        strict=False, redraw=False) :
        """ find limits and autoscale plot.

        **arguments**:

            **autoscale_x** (bool, default=False)

                widen x-axis to fit all curves. if strict, narrow x-axis to
                minimum and maximum of all curves

            **autoscale_y** (bool, default=True)

                widen y-axis to fit all curves. if strict, narrow y-axis to
                minimum and maximum of all curves

            **strict** (bool, default=False)

                if false, rescale and redraw only if current plot limits
                are smaller than minimum and maximum of all curves

            **redraw** (bool, default=False)

                if true, do redraw for any case of limit comparisons

        **results**:

            * The plot is re-drawn with the new limits.

        """
        xmin,  xmax,  ymin,  ymax  = self.__XYlimits
        if autoscale_x and autoscale_y :
            axmin, axmax, aymin, aymax = self.__plot_autoscale_limits()
        elif autoscale_x and not autoscale_y :
            axmin, axmax, aymin, aymax = \
                self.__plot_autoscale_limits(limit_y=(ymin, ymax))
        elif autoscale_y and not autoscale_x :
            axmin, axmax, aymin, aymax = \
                self.__plot_autoscale_limits(limit_x=(xmin, xmax))
        else :
            return

        do_redraw = redraw
        if autoscale_x :
            if (((axmin != xmin or axmax != xmax) and strict) or
                 (axmin <  xmin or axmax >  xmax) ) :
                xmin, xmax = axmin, axmax
                do_redraw = True
        if autoscale_y :
            if (((aymin != ymin or aymax != ymax) and strict) or
                 (aymin <  ymin or aymax >  ymax) ) :
                ymin, ymax = aymin, aymax
                do_redraw = True
        if do_redraw :
            self.__XYlimits = [xmin, xmax, ymin, ymax]
            self["xmin"] = xmin
            self["xmax"] = xmax
            self["ymin"] = ymin
            self["ymax"] = ymax
            self._plot_redraw("autoscale")
            self.__save_view(win0=True)
    #==========================================================================
    # METHOD  : delete_curve
    # PURPOSE : delete a curve
    #==========================================================================
    def delete_curve(self, curve, redraw=True) :
        """ delete a curve.

        **arguments**:

            **curve** (str)

                label of curve to delete.
                curve labels appear in the curve menu.
                the label is in the format <data_name>\_:_<ycol>_vs_<xcol>
                where data_name is the name of the data object
                and xcol and ycol are the x and y column names in the curve.

            **redraw** (bool, default=True)

                if True, redraw plot after deleting curve

        **results**:

            * The specified curve is de-registered.

            * If redraw is True, redraw the Plot.

        """
        if not curve in self._curves :
            self.warning("curve %s not in curves" % (curve))
            return
        index = self._curves.index(curve)
        self._curves.pop(index)
        del self._curve_dname[curve]
        del self._curve_xname[curve]
        del self._curve_yname[curve]
        del self._curve_color[curve]
        del self._curve_symbol[curve]
        del self._curve_ssize[curve]
        del self._curve_wline[curve]
        del self._curve_trace[curve]
        del self._curve_lstate[curve]
        del self._curve_sstate[curve]
        del self._curve_xdata[curve]
        del self._curve_ydata[curve]
        #----------------------------------------------------------------------
        # revise current curve
        #----------------------------------------------------------------------
        if self._curves :
            index = max(index-1, 0)
            current_curve = self._curves[index]
        else :
            current_curve = None
        self._Component["curve_select_var"].set(current_curve)
        self.__curve_select_cmd()
        #----------------------------------------------------------------------
        # remove from curve menu
        # note: Tk requires [] and backslash to be escaped
        #----------------------------------------------------------------------
        curv_menu = self._Component["curv_menu"]
        curvex = self.__curve_menu_scrub(curve)
        index = curv_menu.index(curvex)
        curv_menu.delete(index)
        if redraw :
            self._plot_redraw("delete_curve")
    #==========================================================================
    # METHOD  : add_curve
    # PURPOSE : add a curve
    #==========================================================================
    def add_curve(self, datobj, xcol, ycol, start=False,
        autoscale_x=False, autoscale_y=True, strict=False,
        dname=None, lstate=True, sstate=True,
        color=None, symbol=None, ssize=None, wline=None, trace=None) :
        """ add a curve.

        **arguments**:

            **datobj** (Data object handle)

                data object supplying points to add to curve.

            **xcol** (str)

                x column name.

            **ycol** (str)

                x column name.

            **start** (bool, default=False)

                modify x, y titles if this is the first and only curve.

            **autoscale_x** (bool, default=False)

                widen x-axis to fit all curves. if strict, narrow x-axis to
                minimum and maximum of all curves.

            **autoscale_y** (bool, default=True)

                widen y-axis to fit all curves. if strict, narrow y-axis to
                minimum and maximum of all curves.

            **strict** (bool, default=False)

                if false, rescale and redraw only if current plot limits
                are smaller than minimum and maximum of all curves

            **dname** (str, default=None)

                specify data name.
                if not specified, dname = data_1.

            **lstate** (bool, default=True)

                specify line-state.

            **sstate** (bool, default=true)

                specify symbol-state.

            **color** (str, default=None)

                specify curve color.
                if not specified, chooses next color in color list.

            **symbol** (str, default=None)

                specify curve symbol.
                if not specified, chooses next symbol in symbol list.
                if symbol list wasn't configured, then symbol=none.

            **ssize** (float, default=None)

                specify curve symbol size.
                if not specified, chooses next symbol size in symbol size list.

            **wline** (float, default=None)

                specify curve line width.
                if not specified, chooses next line width in line width list.

            **trace** (str, default=None)

                specify curve trace.
                if not specified, chooses next trace in trace list

        **results**:

            * Registers a new curve with a curve id in the format:
                <data_name>\_:_<ycol>_vs_<xcol>
                If data_name is undefined, it is set to "data_1"

            * Plot is re-drawn with the new curve.

            * New curve is selected as the current curve.

        """
        #----------------------------------------------------------------------
        # checking:
        #----------------------------------------------------------------------
        if not isinstance(datobj, Data):
            self.error("datobj is not a data object")
            return
        if not xcol in datobj.names() :
            self.error("xcol \"%s\" is not in data object" % (xcol))
            return
        if not ycol in datobj.names() :
            self.error("ycol \"%s\" is not in data object" % (ycol))
            return
        #----------------------------------------------------------------------
        # get curve attributes
        #----------------------------------------------------------------------
        icurve = len(self._curves)
        if  dname is None :
            dname = "data_1"
        if  color is None :
            colors   = self["colors"]
            ncolors  = len(colors)
            color    = colors[icurve % ncolors]
        if  symbol is None :
            if not self.was_configured("symbols") :
                symbol = "none"
            else :
                symbols  = self["symbols"]
                nsymbols = len(symbols)
                symbol   = symbols[icurve % nsymbols]
        if  ssize is None :
            ssizes   = self["ssizes"]
            nssizes  = len(ssizes)
            ssize    = ssizes[icurve % nssizes]
        if  wline is None :
            wlines   = self["wlines"]
            nwlines  = len(wlines)
            wline    = wlines[icurve % nwlines]
        if  trace is None :
            traces   = self["traces"]
            ntraces  = len(traces)
            trace    = traces[icurve % ntraces]
        #----------------------------------------------------------------------
        # save curve attributes
        #----------------------------------------------------------------------
        curve = dname + "_:_" + ycol + "_vs_" + xcol
        self._curves.append(curve)
        self._curve_dname[curve] = dname
        self._curve_xname[curve] = xcol
        self._curve_yname[curve] = ycol
        self._curve_color[curve] = color
        self._curve_symbol[curve] = symbol
        self._curve_ssize[curve] = ssize
        self._curve_wline[curve] = wline
        self._curve_trace[curve] = trace
        self._curve_lstate[curve] = lstate
        self._curve_sstate[curve] = sstate
        self._curve_xdata[curve] = datobj.get(xcol)
        self._curve_ydata[curve] = datobj.get(ycol)
        #----------------------------------------------------------------------
        # modify x, y titles if this is the only curve
        #----------------------------------------------------------------------
        if start and len(self._curves) == 1:
            self["xtitle"] = xcol
            self["ytitle"] = ycol
        #----------------------------------------------------------------------
        # if gui not yet built, return without trying to plot
        #----------------------------------------------------------------------
        if "curv_menu" not in self._Component :
            return
        #----------------------------------------------------------------------
        # add new curve to curve menu:
        #----------------------------------------------------------------------
        curv_menu = self._Component["curv_menu"]
        curv_menu.add_radiobutton(
            label=curve,
            variable=self._Component["curve_select_var"],
            value=curve,
            command=self.__curve_select_cmd)
        #----------------------------------------------------------------------
        # select this curve as current curve
        #----------------------------------------------------------------------
        self._Component["curve_select_var"].set(curve)
        self.__curve_select_cmd()
        #----------------------------------------------------------------------
        # redraw everything
        #----------------------------------------------------------------------
        if autoscale_x or autoscale_y :
            self.autoscale(
                autoscale_x=autoscale_x, autoscale_y=autoscale_y,
                strict=strict, redraw=True)
        else :
            self._plot_redraw("add_curve")
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PlotBasem GUI stretch: zoom, label, report callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : begin_stretch
    # PURPOSE : mouse down call-back
    #==========================================================================
    def begin_stretch(self, mode, func, u, v) :
        """ mouse down call-back.

        **arguments**:

            **mode** (str)

                mode string: one of

                    * "zoom"    : zoom in to window
                    * "delete"  : delete labels within window
                    * "report"  : report line-parameters
                    * "label"   : annotate plot

            **func** (function)

                function to call on end_stretch

            **u, v** (int)

                canvas coordinates

        **results**:

            * Registers the  stretch function, mode, and
              beginning coordinates.

            * Updates the coordinate display.

        """
        self.update()
        self.__update_coord_display(u, v)
        self.__stretch_u1, self.__stretch_v1 = u, v
        self.__stretch_mode = mode
        self.__stretch_func = func
    #==========================================================================
    # METHOD  : continue_stretch
    # PURPOSE : mouse movement call-back
    #==========================================================================
    def continue_stretch(self, u, v) :
        """ mouse movement after mouse down call-back.

        **arguments**:

            **u, v** (int)

                canvas coordinates

        **results**:

            * Redraws rectangle or line, depending on the stretch operation.

            * Updates the coordinate display.

        """
        if self.__stretch_mode is None :
            return
        self.__update_coord_display(u, v)
        self.__stretch_u2, self.__stretch_v2 = u, v
        color = self.__stretch_colors[self.__stretch_mode]
        plot = self._Component["plot"]
        u1, v1 = self.__stretch_u1, self.__stretch_v1
        u2, v2 = self.__stretch_u2, self.__stretch_v2
        plot.delete(self.__stretch_id)
        if   self.__stretch_mode in ["zoom", "delete"]:
            if sys.platform == "darwin" :
                self.__stretch_id = plot.create_rectangle(
                    u1, v1, u2, v2, outline=color, fill = "", width=1)
            else :
                self.__stretch_id = plot.create_rectangle(
                    u1, v1, u2, v2, outline="", fill=color, stipple="gray25")
        elif self.__stretch_mode == "report" :
            self.__stretch_id = plot.create_line(
                u1, v1, u2, v2, fill=color, width=1)
        elif self.__stretch_mode == "label" :
            self.__stretch_id = plot.create_rectangle(
                u1, v1, u2, v2, outline=color, fill="", width=1)
    #==========================================================================
    # METHOD  : end_stretch
    # PURPOSE : mouse up call-back
    #==========================================================================
    def end_stretch(self, u, v) :
        """ mouse up call-back.

        **arguments**:

            **u, v** (int)

                canvas coordinates

        **results**:

            * Calls the registered stretch function with the two
              canvas endpoints defined by begin_stretch and end_stretch.

            * Updates the coordinate display.

        """
        self.update()
        self.__update_coord_display(u, v)
        self.__stretch_u2, self.__stretch_v2 = u, v
        plot = self._Component["plot"]
        ### plot.delete(self.__stretch_id) # move to after function call
        u1, v1 = self.__stretch_u1, self.__stretch_v1
        u2, v2 = self.__stretch_u2, self.__stretch_v2
        if self.__stretch_func is not None :
            self.__stretch_func(u1, v1, u2, v2)
        plot.delete(self.__stretch_id)
        self.__stretch_mode = None
        self.__stretch_func = None
    #==========================================================================
    # METHOD  : __stretch_zoom
    # PURPOSE : zoom after stretch sequence
    #==========================================================================
    def __stretch_zoom(self, u1, v1, u2, v2) :
        x1, y1 = self.plot_uv_xy(u1, v1)
        x2, y2 = self.plot_uv_xy(u2, v2)
        if x2 == x1 or y2 == y1 :
            return
        if x2 < x1 :
            x2, x1 = x1, x2
        if y2 < y1 :
            y2, y1 = y1, y2
        self.__XYlimits = [x1, x2, y1, y2]
        self._plot_redraw("stretch_zoom")
        self.__save_view()
    #==========================================================================
    # METHOD  : __stretch_delete
    # PURPOSE : identify and delete annotated items overlapped by stretch box
    # NOTES   :
    #     * more restrictive selection:
    #       items = plot.find_enclosed(u1, v1, u2, v2)
    #==========================================================================
    def __stretch_delete(self, u1, v1, u2, v2) :
        plot = self._Component["plot"]
        items = plot.find_overlapping(u1, v1, u2, v2)
        tags = []
        ids  = []
        for item in items :
            for tag in plot.gettags(item):
                if re.search("^ANNOTATE-", tag) :
                    tags.append(tag)
                    ids.extend(plot.find_withtag(tag))
        tags = list(set(tags))
        ids  = list(set(ids))
        if not ids :
            return
        Fill = {}
        for item_id in ids:
            Fill[item_id] = plot.itemcget(item_id, "fill")
            plot.itemconfigure(item_id, fill="red")
        oktodelete = (tkinter.messagebox.askquestion(parent=tk.Frame(self), message="delete selected items?") == "yes")
        if oktodelete :
            for tag in tags:
                plot.delete(tag)
                del self.__Annotate[tag]
        else :
            for item_id in ids:
                fill = Fill[item_id]
                plot.itemconfigure(item_id, fill=Fill[item_id])
    #==========================================================================
    # METHOD  : __stretch_report
    # PURPOSE : line parameters report after stretch sequence
    #==========================================================================
    def __stretch_report(self, u1, v1, u2, v2) :
        x1, y1 = self.plot_uv_xy(u1, v1)
        x2, y2 = self.plot_uv_xy(u2, v2)
        self.__line_parameters(x1, y1, x2, y2)
    #==========================================================================
    # METHOD  : __stretch_label
    # PURPOSE : annotation after stretch sequence
    #==========================================================================
    def __stretch_label(self, u1, v1, u2, v2) :
        x1, y1 = self.plot_uv_xy(u1, v1)
        x2, y2 = self.plot_uv_xy(u2, v2)
        self.plot_annotate_dialog(x1, y1, x2, y2)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PlotBasem GUI plot annotation callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : plot_annotate_dialog
    # PURPOSE : add a line (or an arrowed line) to a curve with a label
    #==========================================================================
    def plot_annotate_dialog(self, x1, y1, x2, y2):
        """ add a line (or an arrowed line) to a curve with a label.

        **arguments**:

            **x1, y1, x2, y2** (float)

                x and y coordinates cooresponding to the window where
                the plot is to be annotated.

        **results**:

            * Display a dialog for the user to select text or shapes to
              annotate the plot.

        """
        plot = self._Component["plot"]
        dia = PlotBasem_annotate_dialog(plot, x1, y1)
        shape, text = dia.go()
        if shape != "NONE" or text != "" :
            self.__annotate_index += 1
            tag = "ANNOTATE-%d" % (self.__annotate_index)
            self.plot_annotate(shape, text, x1, y1, x2, y2, tag)
            cmd = "self.plot_annotate(\"%s\", \"%s\", %g, %g, %g, %g, \"%s\")" \
                % (shape, text, x1, y1, x2, y2, tag)
            compile(cmd, "string", "single")
            self.__Annotate[tag] = cmd
    #==========================================================================
    # METHOD  : plot_annotate
    # PURPOSE : add a line (or an arrowed line) to a curve with a label
    #==========================================================================
    def plot_annotate(self, shape, text, x1, y1, x2, y2, tag):
        """ add a line (or an arrowed line) to a curve with a label.

        **arguments**:

            **shape** (str)

                shape to draw on the plot. One of:

                * NONE             : no shape.
                * LINE             : line segment between two enpoints.
                * RECTANGLE        : rectangle using two endpoints.
                * FILLED-RECTANGLE : filled rectangle using two endpoints.
                * ARROW-TO         : arrow from 1st point with arrow on 2nd.
                * ARROW-FROM       : arrow from 2nd point with arrow on 1st.
                * ARROW-BOTH       : arrow to both points.

            **text** (str)

                text to draw on the plot.

            **x1, y1, x2, y2** (float)

                x and y coordinates cooresponding to the window where
                the plot is to be annotated.

            **tag** (str)

                tk canvas tag to assign to the annotation.

        **results**:

            * Display a dialog for the user to select text or shapes to
              annotate the plot.

        """
        pi = math.pi
        Anc = {
            0: "w", 1: "sw", 2: "s", 3: "se",
            4: "e", 5: "ne", 6: "n", 7: "nw",
        }
        plot = self._Component["plot"]
        s1, t1 = self.plot_xy_st(x1, y1)
        s2, t2 = self.plot_xy_st(x2, y2)
        u1, v1 = self.plot_st_uv(s1, t1)
        u2, v2 = self.plot_st_uv(s2, t2)
        ds = s2 - s1
        dt = t2 - t1
        if ds != 0.0 :
            alpha = math.atan2(dt, ds)
        else :
            alpha = 0.0
        zoct = int(4.0*alpha/pi)
        if zoct in Anc :
            anc = Anc[zoct]
        else :
            anc = "c"
        if text != "" :
            th   = self._annotate_text_height
            font = "!" + str(self._annotate_text_font)
            self.plot_texv(s2, t2, th, font + text, anchor=anc, tags=tag)
        if   shape == "NONE" :
            pass
        elif shape == "LINE" :
            plot.create_line(u1, v1, u2, v2, tags=tag)
        elif shape == "RECTANGLE" :
            coords = [u1, v1, u1, v2, u2, v2, u2, v1]
            plot.create_polygon(coords, tags=tag, fill="", outline="black")
        elif shape == "FILLED-RECTANGLE" :
            coords = [u1, v1, u1, v2, u2, v2, u2, v1]
            plot.create_polygon(coords, tags=tag, fill="black", outline="", stipple="gray12")
        elif shape == "ARROW-TO" :
            v    = self._annotate_arrow_spread # arrow spread in degrees
            r    = self._annotate_arrow_length # arrow length in st units
            beta = pi/180.0*v
            s3   = s1+r*math.cos(alpha-beta)
            t3   = t1+r*math.sin(alpha-beta)
            s4   = s1+r*math.sin(pi/2.0-alpha-beta)
            t4   = t1+r*math.cos(pi/2.0-alpha-beta)
            u3, v3 = self.plot_st_uv(s3, t3)
            u4, v4 = self.plot_st_uv(s4, t4)
            if False :
                plot.create_line(u2, v2, u1, v1, tags=tag)
                coords = [u1, v1, u3, v3, u4, v4]
                plot.create_polygon(coords, tags=tag, fill="black", outline="black")
            else :
                plot.create_line(u2, v2, u1, v1, tags=tag, arrow="last", arrowshape=(15, 20, 5))
        elif shape == "ARROW-FROM" :
            v    = self._annotate_arrow_spread # arrow spread in degrees
            r    = self._annotate_arrow_length # arrow length in st units
            beta = pi/180.0*v
            s3   = s2-r*math.cos(alpha-beta)
            t3   = t2-r*math.sin(alpha-beta)
            s4   = s2-r*math.sin(pi/2.0-alpha-beta)
            t4   = t2-r*math.cos(pi/2.0-alpha-beta)
            u3, v3 = self.plot_st_uv(s3, t3)
            u4, v4 = self.plot_st_uv(s4, t4)
            if False :
                plot.create_line(u1, v1, u2, v2, tags=tag)
                coords = [u2, v2, u3, v3, u4, v4]
                plot.create_polygon(coords, tags=tag, fill="black", outline="black")
            else :
                plot.create_line(u2, v2, u1, v1, tags=tag, arrow="first", arrowshape=(15, 20, 5))
        elif shape == "ARROW-BOTH" :
            v    = self._annotate_arrow_spread # arrow spread in degrees
            r    = self._annotate_arrow_length # arrow length in st units
            beta = pi/180.0*v
            s3   = s2-r*math.cos(alpha-beta)
            t3   = t2-r*math.sin(alpha-beta)
            s4   = s2-r*math.sin(pi/2.0-alpha-beta)
            t4   = t2-r*math.cos(pi/2.0-alpha-beta)
            u3, v3 = self.plot_st_uv(s3, t3)
            u4, v4 = self.plot_st_uv(s4, t4)
            if False :
                plot.create_line(u1, v1, u2, v2, tags=tag)
                coords = [u2, v2, u3, v3, u4, v4]
                plot.create_polygon(coords, tags=tag, fill="black", outline="black")
            else :
                plot.create_line(u2, v2, u1, v1, tags=tag, arrow="both", arrowshape=(15, 20, 5))
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PlotBasem GUI pan/zoom button callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __pan_zoom
    # PURPOSE : pan or zoom plot viewport
    #==========================================================================
    def __pan_zoom(self, detail=None) :
        Z = {
          "out"    : (-0.2,  0.2, -0.2,  0.2),
          "in"     : ( 0.2, -0.2,  0.2, -0.2),
          "left"   : (-1.0, -1.0,  0.0,  0.0),
          "right"  : ( 1.0,  1.0,  0.0,  0.0),
          "x"      : (-0.2,  0.2,  0.0,  0.0),
          "sx"     : ( 0.2, -0.2,  0.0,  0.0),
          "up"     : ( 0.0,  0.0,  1.0,  1.0),
          "down"   : ( 0.0,  0.0, -1.0, -1.0),
          "y"      : ( 0.0,  0.0, -0.2,  0.2),
          "sy"     : ( 0.0,  0.0,  0.2, -0.2),
          "fleft"  : (-0.2, -0.2,  0.0,  0.0),
          "fright" : ( 0.2,  0.2,  0.0,  0.0),
          "fup"    : ( 0.0,  0.0,  0.2,  0.2),
          "fdown"  : ( 0.0,  0.0, -0.2, -0.2),
        }
        dx1, dx2, dy1, dy2 = Z[detail]
        x1, x2, y1, y2 = self.__XYlimits
        x1p, x2p, y1p, y2p = x1, x2, y1, y2
        dx = x2 - x1
        dy = y2 - y1
        x1 += dx*dx1
        x2 += dx*dx2
        y1 += dy*dy1
        y2 += dy*dy2
        # print x1p, x2p, y1p, y2p, " -> ", x1, x2, y1, y2
        self.__XYlimits = [x1, x2, y1, y2]
        self._plot_redraw("pan_zoom")
        self.__save_view()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PlotBasem GUI save/restore window button callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __save_view
    # PURPOSE : save current viewport
    #==========================================================================
    def __save_view(self, win0=False) :
        if win0 :
            self.__XYwindows = []
        self.__XYwindows.append(self.__XYlimits)
        save_button = self._Component["save"]
        rest_button = self._Component["rest"]
        curr = len(self.__XYwindows)
        prev = curr - 1
        #ave_button["text"] = "Save-" + str(curr)
        rest_button["text"] = "Rest-" + str(prev)
    #==========================================================================
    # METHOD  : __restore_view
    # PURPOSE : restore a viewport
    #==========================================================================
    def __restore_view(self, win0=False) :
        # == 0 should not occur
        if   len(self.__XYwindows) == 1:
            return
        if win0 :
            self.__XYlimits = self.__XYwindows[0]
            self.__XYwindows = []
            self.__XYwindows.append(self.__XYlimits)
        else :
            self.__XYlimits = self.__XYwindows.pop()
        self._plot_redraw("restore_view")
        save_button = self._Component["save"]
        rest_button = self._Component["rest"]
        curr = len(self.__XYwindows)
        prev = curr - 1
        #ave_button["text"] = "Save-" + str(curr)
        rest_button["text"] = "Rest-" + str(prev)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PlotBasem GUI log/lin line/symbol grid legend button callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __xlog_cmd
    # PURPOSE : xlog check-button call-back
    #==========================================================================
    def __xlog_cmd(self) :
        self._plot_redraw("xlog")
    #==========================================================================
    # METHOD  : __ylog_cmd
    # PURPOSE : ylog check-button call-back
    #==========================================================================
    def __ylog_cmd(self) :
        self._plot_redraw("ylog")
    #==========================================================================
    # METHOD  : __line_cmd
    # PURPOSE : line check-button call-back
    #==========================================================================
    def __line_cmd(self) :
        state = self._Component["curve_lstate_var"].get()
        plot  = self._Component["plot"]
        curve = self.current_curve()
        if not self.__use_matplotlib:
            if state :
                self._curve_lstate[curve] = True
                plot.itemconfigure(curve + "-LINE",   state="normal")
            else :
                self._curve_lstate[curve] = False
                plot.itemconfigure(curve + "-LINE",   state="hidden")
        else :
            if state :
                self._curve_lstate[curve] = True
            else :
                self._curve_lstate[curve] = False
            self._plot_redraw("line")
    #==========================================================================
    # METHOD  : __symb_cmd
    # PURPOSE : symbol check-button call-back
    #==========================================================================
    def __symb_cmd(self) :
        state = self._Component["curve_sstate_var"].get()
        plot  = self._Component["plot"]
        curve = self.current_curve()
        if not self.__use_matplotlib:
            if state :
                self._curve_sstate[curve] = True
                plot.itemconfigure(curve + "-SYMBOL",   state="normal")
            else :
                self._curve_sstate[curve] = False
                plot.itemconfigure(curve + "-SYMBOL",   state="hidden")
        else:
            if state :
                self._curve_sstate[curve] = True
            else :
                self._curve_sstate[curve] = False
            self._plot_redraw("symbol")
    #==========================================================================
    # METHOD  : _grid_cmd
    # PURPOSE : grid check-button call-back
    #==========================================================================
    def _grid_cmd(self) :
        if not self.__use_matplotlib:
            plot = self._Component["plot"]
            if self._Component["grid_var"].get() :
                plot.itemconfigure("GRID", state="normal")
            else :
                plot.itemconfigure("GRID", state="hidden")
        else :
            plot_canvas  = self._Component["plot_canvas"]
            plot_subplot = self._Component["plot_subplot"]
            if self._Component["grid_var"].get() :
                plot_subplot.grid(True)
            else :
                plot_subplot.grid(False)
            plot_canvas.draw()
    #==========================================================================
    # METHOD  : _lgnd_cmd
    # PURPOSE : legend check-button call-back
    #==========================================================================
    def _lgnd_cmd(self) :
        if not self.__use_matplotlib:
            plot = self._Component["plot"]
            if self._Component["lgnd_var"].get() :
                plot.itemconfigure("LEGEND", state="normal")
            else :
                plot.itemconfigure("LEGEND", state="hidden")
        else :
            self._plot_redraw("legend")
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PlotBasem GUI focus/unfocus binding callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __curve_focus
    # PURPOSE : focus on a curve item
    #==========================================================================
    def __curve_focus(self) :
        pass
    #==========================================================================
    # METHOD  : __curve_unfocus
    # PURPOSE : unfocus from curve item
    #==========================================================================
    def __curve_unfocus(self) :
        pass
    #==========================================================================
    # METHOD  : __coord_set
    # PURPOSE : set cross-hairs to coordinate
    #==========================================================================
    def __coord_set(self) :
        pass
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PlotBasem GUI limit entry set callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __limit_set
    # PURPOSE : adjust plot to limits (limit entry call-backs)
    #==========================================================================
    def __limit_set(self) :
        xmin, xmax, ymin, ymax = self.__XYlimits
        try:
            exmin = float(self._Component["xmin"].get())
            exmax = float(self._Component["xmax"].get())
            eymin = float(self._Component["ymin"].get())
            eymax = float(self._Component["ymax"].get())
        except:
            self._update_limit_display()
            return
        if exmin == xmin and exmax == xmax and eymin == ymin and eymax == ymax:
            return
        if   exmin > exmax :
            exmin, exmax = exmax, exmin
        elif exmin == exmax :
            exmax += 1
        if   eymin > eymax :
            eymin, eymax = eymax, eymin
        elif eymin == eymax :
            eymax += 1
        self.__XYlimits = exmin, exmax, eymin, eymax
        self._update_limit_display()
        self._plot_redraw("limit_set")
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PlotBasem GUI file menu callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __quit_cmd
    # PURPOSE : exit PlotBasem
    #==========================================================================
    def __quit_cmd(self) :
        self.quit()
        if self.__toplevel :
            self.__toplevel.destroy()
        else :
            self.destroy()
    #==========================================================================
    # METHOD  : __postscript_write
    # PURPOSE : write postscript file
    #==========================================================================
    def __postscript_write(self, savefile=None):
        if not savefile :
            if sys.platform == "darwin" :
                savefile = tkinter.filedialog.asksaveasfilename(
                    parent=tk.Frame(self),
                    title = "postScript file name to save?",
                    initialfile = self["postscript_file"],
                    initialdir = os.getcwd(),
                    defaultextension = ".ps",
                )
            else:
                savefile = tkinter.filedialog.asksaveasfilename(
                    parent=tk.Frame(self),
                    title = "postScript file name to save?",
                    initialfile = self["postscript_file"],
                    initialdir = os.getcwd(),
                    defaultextension = ".ps",
                    filetypes = (
                        ("PostScript files", "*.ps"),
                        ("PostScript files", "*.eps"),
                        ("all files", "*"),
                    )
                )
            if not savefile :
                return
        self["postscript_file"] = savefile
        print("writing " + savefile)
        #----------------------------------
        # use canvas to generate postscript
        # includes annotation
        #----------------------------------
        if True or not self.__use_matplotlib:
            plot = self._Component["plot"]
            plot.itemconfigure("CROSSHAIRS", state="hidden")
            if self._postscript_landscape :
                plot.postscript(file=savefile, rotate=True, pagewidth="10.5i")
            else :
                plot.postscript(file=savefile)
            plot.itemconfigure("CROSSHAIRS", state="normal")
        else :
            plot_figure = self._Component["plot_figure"]
            if self._postscript_landscape :
                plot_figure.savefig(savefile, format="ps", orientation="landscape")
            else :
                plot_figure.savefig(savefile, format="ps", orientation="portrait")
    #==========================================================================
    # METHOD  : __postscript_print
    # PURPOSE : send plot to printer
    #==========================================================================
    def __postscript_print(self, specify=False):
        savefile = "tmp_1.ps"
        self.__postscript_write(savefile)
        os.chmod(savefile, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        printCommand = "lpr"
        if specify :
            ge = GetEntryDialog(title="print command",
                message="Print Command", initialvalue=printCommand)
            printCommand = ge.go()
            if not printCommand :
                return
        cmd = printCommand + " " + savefile
        proc = subprocess.Popen(cmd.split())
        #----------------------------------------------------------------------
        # wait for subprocess to finish before removing
        # should probably ditch the process if it takes too long
        #----------------------------------------------------------------------
        proc.wait()
        os.remove(savefile)
        print("removing " + savefile)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PlotBasem GUI edit menu callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __curve_trace_cmd
    # PURPOSE : change curve trace (increasing, decreasing, both)
    #==========================================================================
    def __curve_trace_cmd(self) :
        trace = self._Component["curve_trace_var"].get()
        curve = self.current_curve()
        self._curve_trace[curve] = trace
        self._plot_redraw("curve_trace")
    #==========================================================================
    # METHOD  : _settings_cmd
    # PURPOSE : settings via entrytable-select
    # NOTES   :
    #     * specs: type, blurb, items
    #     * entry: key, label, value
    #==========================================================================
    def _settings_cmd(self) :
        curve = self.current_curve()
        ssize = self._curve_ssize[curve]
        wline = self._curve_wline[curve]
        trace = self._curve_trace[curve]
        widen = self._Component["identify"]
        #---------------------------------------------------------------------
        # note: all keys must be unique:
        # if type == entry or check:
        #   type, blurb [ [key, label, value] ... ]
        # if type == radio:
        #   type, blurb, key, value [ [label, button_value] ... ]
        #---------------------------------------------------------------------
        specs = [
          ["entry", "Titles", [
                 ["title",  "Main title",   self["title"] ],
                 ["xtitle", "X-axis title", self["xtitle"]],
                 ["ytitle", "Y-axis title", self["ytitle"]],
              ]
          ],
          ["entry", "Colors", [
                 ["plot_bg",  "plot background",   self["plot_background"] ],
                 ["lgnd_bg",  "legend background", self["legend_background"] ],
              ]
          ],
          ["entry", "Current Curve: " + curve, [
                 ["ssize", "Symbol size", ssize],
                 ["wline", "Line width",  wline],
              ]
          ],
          ["radio", "", "trace", trace, [
                 ["Trace increasing",  "increasing"],
                 ["Trace decreasing",  "decreasing"],
                 ["Trace both",        "both"      ],
              ]
          ],
          ["check", "identify curve on plot with cross-hairs", [
                 ["identify", "identify", widen["active"]],
              ]
          ],
        ]
        sd = SelectionDialog(self, title="Plot Settings", guispecs=specs)
        V = sd.go()
        if V["ACCEPT"] :
            self["title"]             = V["title"]
            self["xtitle"]            = V["xtitle"]
            self["ytitle"]            = V["ytitle"]
            self["plot_background"]   = V["plot_bg"]
            self["legend_background"] = V["lgnd_bg"]
            self._curve_ssize[curve] = float(V["ssize"])
            self._curve_wline[curve] = int(V["wline"])
            self._curve_trace[curve] = V["trace"]
            self._Component["curve_trace_var"].set(V["trace"])
            widen["active"]=bool(V["identify"])
            self._plot_redraw("settings")
    #==========================================================================
    # METHOD  : __curve_points_cmd
    # PURPOSE : lines and squares, all squares, etc.
    #==========================================================================
    def __curve_points_cmd(self) :
        state = self._Component["curve_points_var"].get()
        plot  = self._Component["plot"]
        for curve in self._curves :
            if  state == "dots":
                self._curve_lstate[curve] = False
                self._curve_sstate[curve] = True
                self._curve_symbol[curve] = "dot"
                self._curve_ssize[curve]  = 0.01
                plot.itemconfigure(curve + "-LINE",   state="hidden")
                plot.itemconfigure(curve + "-SYMBOL", state="normal")
            elif state == "small squares":
                self._curve_lstate[curve] = False
                self._curve_sstate[curve] = True
                self._curve_symbol[curve] = "square"
                self._curve_ssize[curve]  = 0.005
                plot.itemconfigure(curve + "-LINE",   state="hidden")
                plot.itemconfigure(curve + "-SYMBOL", state="normal")
            elif state == "medium squares":
                self._curve_lstate[curve] = False
                self._curve_sstate[curve] = True
                self._curve_symbol[curve] = "square"
                self._curve_ssize[curve]  = 0.008
                plot.itemconfigure(curve + "-LINE",   state="hidden")
                plot.itemconfigure(curve + "-SYMBOL", state="normal")
            elif state == "large squares":
                self._curve_lstate[curve] = False
                self._curve_sstate[curve] = True
                self._curve_symbol[curve] = "square"
                self._curve_ssize[curve]  = 0.01
                plot.itemconfigure(curve + "-LINE",   state="hidden")
                plot.itemconfigure(curve + "-SYMBOL", state="normal")
            elif state == "narrow lines":
                self._curve_lstate[curve] = True
                self._curve_sstate[curve] = False
                self._curve_symbol[curve] = "none"
                self._curve_wline[curve]  = 1
                plot.itemconfigure(curve + "-LINE",   state="normal")
                plot.itemconfigure(curve + "-SYMBOL", state="hidden")
            elif state == "medium lines":
                self._curve_lstate[curve] = True
                self._curve_sstate[curve] = False
                self._curve_symbol[curve] = "none"
                self._curve_wline[curve]  = 3
                plot.itemconfigure(curve + "-LINE",   state="normal")
                plot.itemconfigure(curve + "-SYMBOL", state="hidden")
            elif state == "wide lines":
                self._curve_lstate[curve] = True
                self._curve_sstate[curve] = False
                self._curve_symbol[curve] = "none"
                self._curve_wline[curve]  = 6
                plot.itemconfigure(curve + "-LINE",   state="normal")
                plot.itemconfigure(curve + "-SYMBOL", state="hidden")
            elif state == "dots and narrow lines":
                self._curve_lstate[curve] = True
                self._curve_sstate[curve] = True
                self._curve_symbol[curve] = "dot"
                self._curve_ssize[curve]  = 0.01
                self._curve_wline[curve]  = 1
                plot.itemconfigure(curve + "-LINE",   state="normal")
                plot.itemconfigure(curve + "-SYMBOL", state="normal")
        self._plot_redraw("curve_points")
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PlotBasem GUI color/symbol/curve menu callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __curve_menu_scrub
    # PURPOSE : scrub curve-name for tk menu index
    #==========================================================================
    def __curve_menu_scrub(self, curve) :
        curvex = re.sub("\\\\", "\\\\\\\\", curve)
        curvex = re.sub("\[", "\\[", curvex)
        curvex = re.sub("\]", "\\]", curvex)
        return curvex
    #==========================================================================
    # METHOD  : __curve_tag_scrub
    # PURPOSE : scrub curve-name for tk canvas tags
    #==========================================================================
    def __curve_tag_scrub(self, curve) :
        curvex = re.sub("\\\\", "__", curve)
        return curvex
    #==========================================================================
    # METHOD  : __curve_choose_color_cmd
    # PURPOSE : change curve color
    #==========================================================================
    def __curve_choose_color_cmd(self) :
        color = self._Component["curve_color_var"].get()
        cx, cy = tkinter.colorchooser.askcolor(
            parent=tk.Frame(self), title="color", color=color
        )
        if cy is None :
            return
        color=str(cy)
        plot  = self._Component["plot"]
        curve = self.current_curve()
        if curve :
            self._curve_color[curve] = color
            if not self.__use_matplotlib :
                curvex = self.__curve_tag_scrub(curve)
                plot.itemconfigure(curvex + "-SYMBOL", fill=color)
                plot.itemconfigure(curvex + "-LINE",   fill=color)
                plot.itemconfigure(curvex + "-LEGEND-LINE", fill=color)
            else :
                items = color.split()
                if len(items) > 1:
                    color = "".join([item.capitalize() for item in items])
                    self._curve_color[curve] = color
                if curve in self._curve_id :
                    self._curve_id[curve].set_color(color)
                if curve in self._curve_sym_id :
                    self._curve_sym_id[curve].set_color(color)
                self._plot_redraw("choose_curve_color")
            color = self._Component["curve_color_var"].set(color)
    #==========================================================================
    # METHOD  : __curve_color_cmd
    # PURPOSE : change curve color
    #==========================================================================
    def __curve_color_cmd(self) :
        color = self._Component["curve_color_var"].get()
        plot  = self._Component["plot"]
        curve = self.current_curve()
        if curve :
            self._curve_color[curve] = color
            if not self.__use_matplotlib :
                curvex = self.__curve_tag_scrub(curve)
                plot.itemconfigure(curvex + "-SYMBOL", fill=color)
                plot.itemconfigure(curvex + "-LINE",   fill=color)
                plot.itemconfigure(curvex + "-LEGEND-LINE", fill=color)
            else :
                items = color.split()
                if len(items) > 1:
                    color = "".join([item.capitalize() for item in items])
                    self._curve_color[curve] = color
                if curve in self._curve_id :
                    self._curve_id[curve].set_color(color)
                if curve in self._curve_sym_id :
                    self._curve_sym_id[curve].set_color(color)
                self._plot_redraw("curve_color")
    #==========================================================================
    # METHOD  : __curve_symbol_cmd
    # PURPOSE : change curve symbol
    #==========================================================================
    def __curve_symbol_cmd(self) :
        symbol = self._Component["curve_symbol_var"].get()
        curve  = self.current_curve()
        if curve :
            if   symbol == "narrow line" :
                self._curve_wline[curve]  = 1
                self._curve_symbol[curve] = "none"
            elif symbol == "medium line" :
                self._curve_wline[curve]  = 3
                self._curve_symbol[curve] = "none"
            elif symbol == "wide line" :
                self._curve_wline[curve]  = 6
                self._curve_symbol[curve] = "none"
            else :
                self._curve_wline[curve]  = 1
                self._curve_symbol[curve] = symbol
        self._plot_redraw("curve_symbol")
    #==========================================================================
    # METHOD  : __curve_select_cmd
    # PURPOSE : change current curve
    #==========================================================================
    def __curve_select_cmd(self) :
        curve = self._Component["curve_select_var"].get()
        if curve != "None" :
            color  = self._curve_color[curve]
            symbol = self._curve_symbol[curve]
            trace  = self._curve_trace[curve]
            lstate = self._curve_lstate[curve]
            sstate = self._curve_sstate[curve]
        else :
            color  = None
            symbol = None
            trace  = None
            lstate = 1
            sstate = 1
        self.__current_curve = curve
        self._Component["curve_color_var"].set(color)
        self._Component["curve_symbol_var"].set(symbol)
        self._Component["curve_trace_var"].set(trace)
        self._Component["curve_lstate_var"].set(lstate)
        self._Component["curve_sstate_var"].set(sstate)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PlotBasem plot rendering
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _plot_redraw
    # PURPOSE : redraw whenever plot limits, curves are changed, etc.
    #==========================================================================
    def _plot_redraw(self, redraw_reason="none") :
        if not self.__use_matplotlib:
            plot = self._Component["plot"]
            self._plot_transform_calc()
            plot.delete("all")
            self._plot_border()
            self._plot_title()
            self._plot_xaxis()
            self._plot_yaxis()
            plot.itemconfigure("GRID", dash=".")
            self._grid_cmd()
            self._plot_curves()
            self._plot_annotations()
            self._update_limit_display()
            self._plot_legend()
            self._lgnd_cmd()
        else :
            plot = self._Component["plot"]
            self._plot_transform_calc()
            #-------------------------------
            # delete all canvas annotations:
            #-------------------------------
            items = plot.find_all()
            for item in items:
                for tag in plot.gettags(item):
                    if re.search("^ANNOTATE-", tag):
                        plot.delete(item)
            plot_figure = self._Component["plot_figure"]
            plot_canvas = self._Component["plot_canvas"]
            q1 = self._axes_left_margin
            q2 = 1.0 - self._axes_right_margin
            r1 = self._axes_bottom_margin
            r2 = 1.0 - self._axes_top_margin
            if self["title"] != "" :
                r2 = 1.0 - 2.0*self._axes_top_margin
            plot_figure.subplots_adjust(left=q1, right=q2, bottom=r1, top=r2)
            plot_figure.clear()
            #-----------------
            # plot axes, title
            #-----------------
            plot_subplot = plot_figure.add_subplot(111)
            if self["title"] != "" :
                plot_subplot.set_title(self["title"], fontsize="large", fontweight="regular")
            if self["xtitle"] != "" :
                plot_subplot.set_xlabel(self["xtitle"], labelpad=20, fontsize="large", fontweight="regular")
            if self["ytitle"] != "" :
                plot_subplot.set_ylabel(self["ytitle"], labelpad=20, fontsize="large", fontweight="regular")
            self._Component["plot_subplot"] = plot_subplot
            x1, x2, y1, y2 = self.__XYlimits
            xlog = (self._Component["xlog_var"].get() == 1)
            ylog = (self._Component["ylog_var"].get() == 1)
            if xlog :
                ax2 = abs(x2)
                ax1 = abs(x1)
                if x1*x2 <= 0.0:
                    ax2 = max(ax2, ax1)
                    ax1 = ax2*1e-6
                x1, x2 = ax1, ax2
            if   x1 == x2 :
                x2 += 1
            elif x1 >  x2 :
                x1, x2 = x2, x1
            if ylog :
                ay2 = abs(y2)
                ay1 = abs(y1)
                if y1*y2 <= 0.0:
                    ay2 = max(ay2, ay1)
                    ay1 = ay2*1e-6
                y1, y2 = ay1, ay2
            if   y1 == y2 :
                y2 += 1
            elif y1 > y2 :
                y1, y2 = y2, y1
            plot_subplot.set_xlim(x1, x2)
            plot_subplot.set_ylim(y1, y2)
            bgc = self["plot_background"]
            plot_subplot.set_facecolor(bgc)
            plot_figure.set_facecolor(bgc)
            self._grid_cmd()
            #---------------------------------
            # plot curves, legend
            #---------------------------------
            self._plot_curves()
            #-------------------------------
            # redraw all canvas annotations:
            #-------------------------------
            self._plot_annotations()
            self._update_limit_display()
            #-------------------------------
            # debug
            #-------------------------------
            if False :
                plot_canvas  = self._Component["plot_canvas"]
                plot_subplot = self._Component["plot_subplot"]
                plot_figure  = self._Component["plot_figure"]
                tk_canvas    = plot_canvas.get_tk_widget()
                fw = plot_figure.get_figwidth()
                fh = plot_figure.get_figheight()
                cw = tk_canvas["width"]
                ch = tk_canvas["height"]
                xt = self["xtitle"]
                yt = self["ytitle"]
                wext = plot_subplot.get_window_extent()
                print("redraw (%s): %s_%s, %s %s, %s %s, %s" % (redraw_reason, yt, xt, fw, fh, cw, ch, wext))
            plot_canvas.draw()
    #==========================================================================
    # METHOD  : _plot_border
    # PURPOSE : plot border around maximum limits
    #==========================================================================
    def _plot_border(self) :
        if False:
            plot = self._Component["plot"]
            u1, u2, v1, v2 = self.__Transform["uv_max_limits"]
            coords = (u1, v1, u2, v1, u2, v2, u1, v2, u1, v1)
            plot.create_line(coords, tags="BORDER")
    #==========================================================================
    # METHOD  : _plot_title
    # PURPOSE : label plot title
    #==========================================================================
    def _plot_title(self) :
        if self["title"] == "" :
            return
        title_font = "!" + str(self._plot_title_font)
        s1, s2, t1, t2 = self.__Transform["st_max_limits"]
        th = self._plot_title_height
        tm = self._plot_title_margin
        s = (s2 + s1)*0.5
        if self._xaxis_top :
            t = t1 + tm
            anchor = "s"
        else :
            t = t2 - tm
            anchor = "n"
        self.plot_texv(s, t, th, title_font + self["title"], anchor=anchor)
    #==========================================================================
    # METHOD  : _plot_legend
    # PURPOSE : label plot legend
    #==========================================================================
    def _plot_legend(self) :
        if not self._curves :
            return
        lh = self._legend_label_height
        bw = self._legend_box_width
        bm = self._legend_box_margin
        pm = self._legend_pad_margin
        font = "!" + str(self._legend_font)
        background = self["legend_background"]
        plot = self._Component["plot"]
        s1, s2 = 1.0 - bm - bw, 1.0 - bm
        t1, t2 = 1.0 - bm, 1.0 - bm - lh*(3.0*len(self._curves)+1)*0.5
        u1, v1 = self.plot_st_uv(s1,t1)
        u2, v2 = self.plot_st_uv(s2,t2)
        tagbx  = "LEGEND-BOX"
        tagsbx = "LEGEND " + tagbx
        coords = (u1, v1, u2, v1, u2, v2, u1, v2)
        plot.create_polygon(coords, tags=tagsbx, fill="", outline="blue")
        plot.itemconfigure(tagbx, fill=background, outline="")
        sc1 = s1  + pm
        sc2 = sc1 + bw*0.3
        scm = (sc1 + sc2)* 0.5
        st1 = sc2 + pm
        st2 = s2  - pm
        t   = 1.0 - bm - lh
        for curve in self._curves :
            m = re.search("^(.+)_:_(.+)_vs_(.+)$", curve)
            if m :
                curve_label = m.group(2)
            else :
                curve_label = curve
            curvex = self.__curve_tag_scrub(curve)
            tagca = curvex + "-LEGEND-LABEL"
            tagcl = curvex + "-LEGEND-LINE"
            tagcs = curvex + "-LEGEND-SYMBOL"
            tagsca = "LEGEND " + tagca
            tagscl = "LEGEND " + tagcl
            tagscs = "LEGEND " + tagcs
            color = self._curve_color[curve]
            symbol= self._curve_symbol[curve]
            ssize = self._curve_ssize[curve]
            wline = self._curve_wline[curve]
            self.plot_texv(st1, t, lh, font + curve_label, anchor="w",
                tags=tagsca)
            u1, v1 = self.plot_st_uv(sc1,t)
            u2, v2 = self.plot_st_uv(sc2,t)
            plot.create_line(u1, v1, u2, v2, tags=tagscl)
            if symbol != "none" :
                self.plot_symb(scm, t, ssize, symbol, tags=tagscs)
            plot.itemconfigure(tagcs, fill=color)
            plot.itemconfigure(tagcl, fill=color)
            plot.itemconfigure(tagcl, width=wline)
            t -= lh*1.5
    #==========================================================================
    # METHOD   : _plot_test1
    # PURPOSE  : plot axes markers
    #==========================================================================
    def _plot_test1(self):
        self.plot_texv(0.5, 0.5, 1.00, "H")
        self.plot_texv(0.5, 0.5, 0.05, "x")
        self.plot_texv(0.0, 0.0, 0.05, "x")
        self.plot_texv(0.0, 1.0, 0.05, "x")
        self.plot_texv(1.0, 0.0, 0.05, "x")
        self.plot_texv(1.0, 1.0, 0.05, "x")
    #==========================================================================
    # METHOD  : _plot_test2
    # PURPOSE : plot rotated fonts
    #==========================================================================
    def _plot_test2(self):
        Cface = ["!", "&", "$"]
        Color = [
            "red", "blue", "green", "cyan", "orange", "black",
            "cadetblue", "darkgreen"]
        stringp = "    ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        rotate = 0
        icolor = 0
        for i in range(0, 4) :
            for j in range(0, 3) :
                line_color = Color[icolor % 8]
                s = "!" + str(i) + str(Cface[j]) + stringp
                self.plot_texv(0.5, 0.5, 0.025, s, rotate=rotate, anchor="w")
                rotate += 30
            icolor += 1
    #==========================================================================
    # METHOD  : __plot_scaler
    # PURPOSE : returns major and minor axes values
    #==========================================================================
    def __plot_scaler(self, vmin, vmax, log) :
        eps = 1e-8
        dv = 1
        if not log :
            dx = vmax - vmin
            if dx == 0.0 :
                dx = 1
            while dv < dx :
                dv *= 10.0
            while dv > dx :
                dv *= 0.10
        nmin = int(vmin/dv - 0.5) + 1
        nmax = int(vmax/dv + 0.5) - 1
        while nmin*dv > vmin + abs(vmin*eps) :
            nmin -= 1
        while nmax*dv < vmax - abs(vmax*eps) :
            nmax += 1
        lo, hi = nmin*dv, nmax*dv
        div = nmax - nmin
        major = []
        minor = []
        for i in range(1, div+2) :
            if log :
                v = lo + dv*(i-1)
                collect = (v >= vmin and v <= vmax)
                v = math.pow(10.0, v)
            else :
                v = lo + dv*(i-1)
                collect = (v >= vmin and v <= vmax)
            if collect :
                major.append(v)
            if i <= div:
                for j in range (1, 10):
                    if log :
                        v = lo + dv*((i-1) + math.log10(j))
                        collect = (v >= vmin and v <= vmax)
                        v = math.pow(10.0, v)
                    else :
                        v = lo + dv*((i-1) + j*0.1)
                        collect = (v >= vmin and v <= vmax)
                    if collect :
                        minor.append(v)
        v = vmin
        if log :
            v = math.pow(10.0, v)
        if not major or v != major[0] :
            major.insert(0, v)
        v = vmax
        if log :
            v = math.pow(10.0, v)
        if not major or v != major[-1] :
            major.append(v)
        return([major, minor])
    #==========================================================================
    # METHOD  : _plot_xaxis
    # PURPOSE : plot x-axis
    # NOTES   :
    #     * log limits are log10(abs())
    #==========================================================================
    def _plot_xaxis(self) :
        plot = self._Component["plot"]
        xtitle = self["xtitle"]
        title_font = "!" + str(self._axes_title_font)
        value_font = "!" + str(self._axes_value_font)
        xlog = (self._Component["xlog_var"].get() == 1)
        x1, x2, y1, y2 = self.__Transform["xy_limits"]
        xmajor, xminor = self.__plot_scaler(x1, x2, xlog)

        if self._axes_tics_outside :
            dtm = -self._axes_major_tic_size
            dtn = -self._axes_minor_tic_size
        else :
            dtm =  self._axes_major_tic_size
            dtn =  self._axes_minor_tic_size
        if self._xaxis_top :
            to  = 1.0
            te  = 0.0
            dtt =  self._axes_title_margin
            dtv =  self._axes_value_margin
            dtm = -dtm
            dtn = -dtn
            vanchor  = "s"  if self._xaxis_value_angle == 0 else "w"
            vanchora = "se" if self._xaxis_value_angle == 0 else "nw"
            vanchorb = "sw" if self._xaxis_value_angle == 0 else "sw"
        else :
            to  = 0.0
            te  = 1.0
            dtt = -self._axes_title_margin
            dtv = -self._axes_value_margin
            vanchor  = "n"  if self._xaxis_value_angle == 0 else "e"
            vanchora = "ne" if self._xaxis_value_angle == 0 else "ne"
            vanchorb = "nw" if self._xaxis_value_angle == 0 else "se"
        #----------------------------------------------------------------------
        # axis line:
        #----------------------------------------------------------------------
        u1, v1 = self.plot_st_uv(0.0, to)
        u2, v2 = self.plot_st_uv(1.0, to)
        plot.create_line(u1, v1, u2, v2, tags="XAXIS")
        #----------------------------------------------------------------------
        # axis title:
        #----------------------------------------------------------------------
        if xtitle :
            self.plot_texv(0.5, to+dtt, self._axes_title_height,
                title_font + xtitle, tags="XAXIS")
        #----------------------------------------------------------------------
        # major tics and labels:
        #----------------------------------------------------------------------
        sa = 0.0 + self._axes_value_height*1.5
        sb = 1.0 - self._axes_value_height*1.5
        inx = len(xmajor) - 1
        for ix, xm in enumerate(xmajor) :
            s, t = self.plot_xy_st(xm, 0.0)
            if abs(xm) < 10000:
                value = self._axes_value_format1 % (xm)
            else :
                value = self._axes_value_format2 % (xm)
            if   (ix > 0   and s < sa) :
                av = vanchora
                sv = sa
            elif (ix < inx and s > sb) :
                av = vanchorb
                sv = sb
            else :
                av = vanchor
                sv = s
            self.plot_texv(sv, to+dtv, self._axes_value_height,
                value_font + value, tags="XAXIS",
                rotate=self._xaxis_value_angle, anchor=av)
            u1, v1 = self.plot_st_uv(s, to)
            u2, v2 = self.plot_st_uv(s, to+dtm)
            u3, v3 = self.plot_st_uv(s, te)
            plot.create_line(u1, v1, u2, v2, tags="XAXIS")
            plot.create_line(u2, v2, u3, v3, tags="GRID")
        #----------------------------------------------------------------------
        # minor tics:
        #----------------------------------------------------------------------
        for xn in xminor :
            s, t = self.plot_xy_st(xn, 0.0)
            u1, v1 = self.plot_st_uv(s, to)
            u2, v2 = self.plot_st_uv(s, to+dtn)
            plot.create_line(u1, v1, u2, v2, tags="XAXIS")
    #==========================================================================
    # METHOD  : _plot_yaxis
    # PURPOSE : plot y-axis
    # NOTES   :
    #     * log limits are log10(abs())
    #==========================================================================
    def _plot_yaxis(self) :
        plot = self._Component["plot"]
        ytitle = self["ytitle"]
        title_font = "!" + str(self._axes_title_font)
        value_font = "!" + str(self._axes_value_font)
        ylog = (self._Component["ylog_var"].get() == 1)
        x1, x2, y1, y2 = self.__Transform["xy_limits"]
        ymajor, yminor = self.__plot_scaler(y1, y2, ylog)

        if self._axes_tics_outside :
            dsm = -self._axes_major_tic_size
            dsn = -self._axes_minor_tic_size
        else :
            dsm =  self._axes_major_tic_size
            dsn =  self._axes_minor_tic_size
        if self._yaxis_right :
            so  = 1.0
            se  = 0.0
            dst =  self._axes_title_margin
            dsv =  self._axes_value_margin
            dsm = -dsm
            dsn = -dsn
            tanchor  = "n"
            vanchor  =  "w" if self._yaxis_value_angle == 0 else "n"
            vanchora = "sw" if self._yaxis_value_angle == 0 else "nw"
            vanchorb = "nw" if self._yaxis_value_angle == 0 else "ne"
        else :
            so  = 0.0
            se  = 1.0
            dst = -self._axes_title_margin
            dsv = -self._axes_value_margin
            tanchor  = "s"
            vanchor  =  "e" if self._yaxis_value_angle == 0 else "s"
            vanchora = "se" if self._yaxis_value_angle == 0 else "sw"
            vanchorb = "ne" if self._yaxis_value_angle == 0 else "se"
        #----------------------------------------------------------------------
        # axis line:
        #----------------------------------------------------------------------
        u1, v1 = self.plot_st_uv(so, 0.0)
        u2, v2 = self.plot_st_uv(so, 1.0)
        plot.create_line(u1, v1, u2, v2, tags="YAXIS")
        #----------------------------------------------------------------------
        # axis title:
        #----------------------------------------------------------------------
        if ytitle :
            self.plot_texv(so+dst, 0.5, self._axes_title_height,
                title_font + ytitle, tags="YAXIS", rotate=90, anchor=tanchor)
        #----------------------------------------------------------------------
        # major tics and labels:
        #----------------------------------------------------------------------
        ta = 0.0 + self._axes_value_height*1.5
        tb = 1.0 - self._axes_value_height*1.5
        iny = len(ymajor) - 1
        for iy, ym in enumerate(ymajor) :
            s, t = self.plot_xy_st(0.0, ym)
            if abs(ym) < 10000:
                value = self._axes_value_format1 % (ym)
            else :
                value = self._axes_value_format2 % (ym)
            if   (iy > 0   and t < ta) :
                av = vanchora
                tv = ta
            elif (iy < iny and t > tb) :
                av = vanchorb
                tv = tb
            else :
                av = vanchor
                tv = t
            self.plot_texv(so+dsv, tv, self._axes_value_height,
                value_font + value, tags="YAXIS",
                rotate=self._yaxis_value_angle, anchor=av)
            u1, v1 = self.plot_st_uv(so, t)
            u2, v2 = self.plot_st_uv(so + dsm, t)
            u3, v3 = self.plot_st_uv(se, t)
            plot.create_line(u1, v1, u2, v2, tags="YAXIS")
            plot.create_line(u2, v2, u3, v3, tags="GRID")
        #----------------------------------------------------------------------
        # minor tics:
        #----------------------------------------------------------------------
        for yn in yminor :
            s, t = self.plot_xy_st(0.0, yn)
            u1, v1 = self.plot_st_uv(so, t)
            u2, v2 = self.plot_st_uv(so + dsn, t)
            plot.create_line(u1, v1, u2, v2, tags="YAXIS")
    #==========================================================================
    # METHOD  : __plot_autoscale_limits
    # PURPOSE : find min, max of all curves
    # NOTES   :
    #     * if limit_x = [xmin, xmax] : find y limits between xmin and xmax
    #     * if limit_y = [ymin, ymax] : find x limits between ymin and ymax
    #==========================================================================
    def __plot_autoscale_limits(self, limit_x=None, limit_y=None) :
        xmin, xmax, ymin, ymax = self.__XYlimits
        if not limit_x and not limit_y :
            start = True
            for curve in self._curves :
                xdata = self._curve_xdata[curve]
                ydata = self._curve_ydata[curve]
                x1 = numpy.min(xdata)
                x2 = numpy.max(xdata)
                y1 = numpy.min(ydata)
                y2 = numpy.max(ydata)
                if start :
                    start = False
                    xmin, xmax = x1, x2
                    ymin, ymax = y1, y2
                else :
                    xmin, xmax = min(x1, xmin), max(x2, xmax)
                    ymin, ymax = min(y1, ymin), max(y2, ymax)
        elif limit_x :
            x1, x2 = limit_x
            if x1 <= x2 :
                xmin, xmax = limit_x
                start = True
                for curve in self._curves :
                    xdata = self._curve_xdata[curve]
                    ydata = self._curve_ydata[curve]
                    lim1 = numpy.greater_equal(xdata, xmin)
                    lim2 = numpy.less_equal(   xdata, xmax)
                    lim  = numpy.logical_and(lim1, lim2)
                    ydata = numpy.extract(lim, ydata)
                    if len(ydata) > 0 :
                        y1 = numpy.min(ydata)
                        y2 = numpy.max(ydata)
                        if start :
                            start = False
                            ymin, ymax = y1, y2
                        else :
                            ymin, ymax = min(y1, ymin), max(y2, ymax)
        elif limit_y :
            y1, y2 = limit_y
            if y1 <= y2 :
                ymin, ymax = limit_y
                start = True
                for curve in self._curves :
                    xdata = self._curve_xdata[curve]
                    ydata = self._curve_ydata[curve]
                    lim1 = numpy.greater_equal(ydata, ymin)
                    lim2 = numpy.less_equal(   ydata, ymax)
                    lim  = numpy.logical_and(lim1, lim2)
                    xdata = numpy.extract(lim, xdata)
                    if len(xdata) > 0 :
                        x1 = numpy.min(xdata)
                        x2 = numpy.max(xdata)
                        if start :
                            start = False
                            xmin, xmax = x1, x2
                        else :
                            xmin, xmax = min(x1, xmin), max(x2, xmax)
        #----------------------------------------------------------------------
        # numpy returns float64
        #----------------------------------------------------------------------
        xmin=float(xmin)
        xmax=float(xmax)
        ymin=float(ymin)
        ymax=float(ymax)
        return [xmin, xmax, ymin, ymax]
    #==========================================================================
    # METHOD  : __plot_curve_limits
    # PURPOSE : find curve limits using autoscaled, specified limits
    #==========================================================================
    def __plot_curve_limits(self) :
        xmin, xmax, ymin, ymax = self.__plot_autoscale_limits()
        #-----------------------------------------
        # specified limits over-ride curve limits:
        #-----------------------------------------
        if self.was_configured("xmin") :
            xmin = self["xmin"]
        if self.was_configured("xmax") :
            xmax = self["xmax"]
        if self.was_configured("ymin") :
            ymin = self["ymin"]
        if self.was_configured("ymax") :
            ymax = self["ymax"]
        #-----------------------------------------
        # set __XYlimits to these limits
        #-----------------------------------------
        self.__XYlimits = [xmin, xmax, ymin, ymax]
        #-----------------------------------------
        # set configuration limits to these limits
        #-----------------------------------------
        self["xmin"] = xmin
        self["xmax"] = xmax
        self["ymin"] = ymin
        self["ymax"] = ymax
    #==========================================================================
    # METHOD  : _plot_curves
    # PURPOSE : plot all curves
    # NOTES   :
    #    * pairwise_coordinates: curve data is separate segments
    #      (for contour plotting)
    #    * normally continuous curve points
    #==========================================================================
    def _plot_curves(self, pairwise_coordinates=False) :
        n_and  = numpy.logical_and
        n_or   = numpy.logical_or
        n_gt   = numpy.greater
        n_lt   = numpy.less
        n_ge   = numpy.greater_equal
        n_le   = numpy.less_equal
        n_abs  = numpy.abs
        n_add  = numpy.add
        n_mult = numpy.multiply
        n_log10= numpy.log10
        n_max  = numpy.maximum
        n_int  = numpy.rint
        if not self.__use_matplotlib:
            plot = self._Component["plot"]
            coord_step = 2 if pairwise_coordinates else 1
            realmin = 1e-300
            c0, c1, c2, c3 = self.__Transform["xy_st"]
            d0, d1, d2, d3 = self.__Transform["st_uv"]
            for curve in self._curves :
                color = self._curve_color[curve]
                symbol= self._curve_symbol[curve]
                ssize = self._curve_ssize[curve]
                wline = self._curve_wline[curve]
                trace = self._curve_trace[curve]
                lstate= self._curve_lstate[curve]
                sstate= self._curve_sstate[curve]
                curvex = self.__curve_tag_scrub(curve)
                stag = curvex + "-SYMBOL"
                ltag = curvex + "-LINE"
                xdata = self._curve_xdata[curve]
                ydata = self._curve_ydata[curve]
                if self._Component["xlog_var"].get() == 1 :
                    xdata = n_log10(n_max(n_abs(xdata), realmin))
                if self._Component["ylog_var"].get() == 1 :
                    ydata = n_log10(n_max(n_abs(ydata), realmin))
                sdata = n_add(c0, n_mult(xdata, c1))
                tdata = n_add(c2, n_mult(ydata, c3))
                udata = n_int(n_add(d0, n_mult(sdata, d1))).astype(int)
                vdata = n_int(n_add(d2, n_mult(tdata, d3))).astype(int)
                within = n_and(
                    n_and(n_ge(sdata, -1e-15), n_le(sdata, 1+1e-15)),
                    n_and(n_ge(tdata, -1e-15), n_le(tdata, 1+1e-15))
                )
                stdata = list(zip(sdata, tdata, within))
                stuvdata = list(zip(sdata, tdata, udata, vdata, within))
                tracefb = n_or(
                    n_and(n_gt(sdata[:-1], sdata[1:]), trace == "increasing"),
                    n_and(n_lt(sdata[:-1], sdata[1:]), trace == "decreasing")
                )
                nonint = n_or(
                    n_or(
                        n_and(n_lt(sdata[:-1], 0.0), n_lt(sdata[1:],  0.0)),
                        n_and(n_gt(sdata[:-1], 1.0), n_gt(sdata[1:],  1.0))
                    ),
                    n_or(
                        n_and(n_lt(tdata[:-1], 0.0), n_lt(tdata[1:],  0.0)),
                        n_and(n_gt(tdata[:-1], 1.0), n_gt(tdata[1:],  1.0))
                    )
                )

                if symbol != "none" :
                    for s, t, w in stdata :
                        if w :
                            self.plot_symb(s, t, ssize, symbol, tags=stag)
                drawn = False
                coords = []
                for (s1, t1, u1, v1, w1), (s2, t2, u2, v2, w2), tfb, non in \
                    zip(stuvdata[0::coord_step], stuvdata[1::coord_step],
                       tracefb[0::coord_step], nonint[0::coord_step]) :
                    if   pairwise_coordinates :
                        drawn = False
                    if   tfb :
                        drawn = False
                    elif w1 and w2 :
                        if not drawn :
                            if len(coords) > 2 :
                                plot.create_line(coords, tags=ltag)
                            coords = [u1, v1]
                        coords.extend([u2, v2])
                        drawn = True
                    elif non :
                        drawn = False
                    else :
                        drawn = False
                        ds, dt = s2 - s1, t2 - t1
                        pts=[]
                        if w1 :
                            pts.append((s1, t1))
                        if ds != 0:
                            r0, r1 = (0-s1)/ds, (1-s1)/ds
                            p0, p1 = t1 + r0*dt, t1 + r1*dt
                            if (r0 >= 0 and r0 <= 1) and (p0 >= 0 and p0 <= 1):
                                pts.append((0, p0))
                            if (r1 >= 0 and r1 <= 1) and (p1 >= 0 and p1 <= 1):
                                pts.append((1, p1))
                        if dt != 0:
                            r0, r1 = (0-t1)/dt, (1-t1)/dt
                            p0, p1 = s1 + r0*ds, s1 + r1*ds
                            if (r0 >= 0 and r0 <= 1) and (p0 >= 0 and p0 <= 1):
                                pts.append((p0, 0))
                            if (r1 >= 0 and r1 <= 1) and (p1 >= 0 and p1 <= 1):
                                pts.append((p1, 1))
                        if w2 :
                            pts.append((s2, t2))
                            drawn = True
                        if len(pts) == 2:
                            if len(coords) > 2 :
                                plot.create_line(coords, tags=ltag)
                            s1, t1 = pts[0]
                            s2, t2 = pts[1]
                            u1, v1 = self.plot_st_uv(s1, t1)
                            u2, v2 = self.plot_st_uv(s2, t2)
                            coords = [u1, v1, u2, v2]
                        else :
                            pass
                            # print "intersections:", pts
                if len(coords) > 2 :
                    plot.create_line(coords, tags=ltag)
                plot.itemconfigure(stag, fill=color)
                plot.itemconfigure(ltag, fill=color)
                plot.itemconfigure(ltag, width=wline)
                if wline == 0:
                    self._curve_lstate[curve] = False
                    plot.itemconfigure(ltag, state="hidden")
                else :
                    self._curve_lstate[curve] = True
                    plot.itemconfigure(ltag, state="normal")
                if ssize <= 0.0:
                    self._curve_sstate[curve] = False
                    plot.itemconfigure(stag, state="hidden")
                else :
                    self._curve_sstate[curve] = True
                    plot.itemconfigure(stag, state="normal")
        else:
            plot_figure  = self._Component["plot_figure"]
            plot_subplot = self._Component["plot_subplot"]
            plot_canvas  = self._Component["plot_canvas"]
            ph   = int(re.sub("i", "", self["plot_height"]))
            t2pt = ph*72.0 * 2
            xlog = (self._Component["xlog_var"].get() == 1)
            ylog = (self._Component["ylog_var"].get() == 1)
            xscale = "log" if xlog else "linear"
            yscale = "log" if ylog else "linear"
            plot_subplot.set_xscale(xscale)
            plot_subplot.set_yscale(yscale)
            self._cid_curve = {}
            self._curve_id = {}
            self._curve_label = {}
            self._curve_lgnd_id = {}
            lgnd_line_list = []
            lgnd_labels = []
            for curve in self._curves :
                color = self._curve_color[curve]
                symbol= self._curve_symbol[curve]
                ssize = self._curve_ssize[curve]
                wline = self._curve_wline[curve]
                if (wline <= 0.0) :
                    self._curve_lstate[curve] = False
                if (ssize <= 0.0) :
                    self._curve_sstate[curve] = False
                trace = self._curve_trace[curve]
                lstate= self._curve_lstate[curve]
                sstate= self._curve_sstate[curve]
                xdata = self._curve_xdata[curve]
                ydata = self._curve_ydata[curve]
                if symbol in self.__MatPlotLibSymbols:
                    symbol = self.__MatPlotLibSymbols[symbol]
                ssize = t2pt*ssize * 2
                items = color.split()
                if len(items) > 1:
                    color = "".join([item.capitalize() for item in items])
                    self._curve_color[curve] = color
                m = re.search("^(.+)_:_(.+)_vs_(.+)$", curve)
                if m :
                    curve_label = m.group(2)
                else :
                    curve_label = curve
                #-----------------------
                # convert to path
                #-----------------------
                coords = numpy.array(list(zip(xdata, ydata)), float)
                tracefb = n_or(
                    n_and(n_gt(xdata[:-1], xdata[1:]), trace == "increasing"),
                    n_and(n_lt(xdata[:-1], xdata[1:]), trace == "decreasing")
                )
                tracefb = numpy.insert(tracefb, 0, True)
                codes = [Path.MOVETO if t else Path.LINETO for t in tracefb]
                path = Path(coords, codes)
                path_patch = PathPatch(path, edgecolor=color, facecolor="None", label=curve_label, linewidth=wline)
                curve_id = plot_subplot.add_patch(path_patch)
                #-----------------------
                #  plot_subplot.scatter produces a user warning when
                #  x,ydata include numbers <= 0 on log axis
                #  UserWarning: Warning: converting a masked element to nan.
                #  warnings.warn("Warning: converting a masked element to nan.")
                #-----------------------
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    curve_sym_id = plot_subplot.scatter(xdata, ydata, marker=symbol, c=color, s=ssize)
                if lstate :
                    curve_id.set_visible(True)
                else :
                    curve_id.set_visible(False)
                if sstate :
                    curve_sym_id.set_visible(True)
                else :
                    curve_sym_id.set_visible(False)
                self._curve_id[curve] = curve_id
                self._curve_sym_id[curve] = curve_sym_id
                self._curve_label[curve] = curve_label
                self._cid_curve[curve_id] = curve
                # -----------
                # for legend:
                # -----------
                lgnd_labels.append(curve_label)
                lgnd_line = Line2D((0,0), (0,0), color=color, marker=symbol, markersize=ssize/ph, linewidth=wline)
                lgnd_line_list.append(lgnd_line)
            if self._Component["lgnd_var"].get() :
                lgnd=plot_subplot.legend(lgnd_line_list, lgnd_labels, loc="upper right", handler_map = {type(Line2D): HandlerLine2D}, handlelength=3, handleheight=1)
                lgnd_lines = lgnd.get_lines()
                for curve, line in zip(self._curves, lgnd_lines):
                    self._curve_lgnd_line[curve] = line
        self.__curve_select_cmd()
    #==========================================================================
    # METHOD  : _plot_annotations
    # PURPOSE : redraw plot annotations
    #==========================================================================
    def _plot_annotations(self):
        plot = self._Component["plot"]
        for tag in self.__Annotate :
            cmd = self.__Annotate[tag]
            exec(cmd)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PlotBasem refresh limit/coord displays
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _update_limit_display
    # PURPOSE : update limit display
    #==========================================================================
    def _update_limit_display(self) :
        xmin, xmax, ymin, ymax = self.__XYlimits
        sxmin = "%-15.8g" % (xmin)
        sxmax = "%-15.8g" % (xmax)
        symin = "%-15.8g" % (ymin)
        symax = "%-15.8g" % (ymax)
        sxmin = sxmin.strip()
        sxmax = sxmax.strip()
        symin = symin.strip()
        symax = symax.strip()
        exmin = self._Component["xmin"]
        exmax = self._Component["xmax"]
        eymin = self._Component["ymin"]
        eymax = self._Component["ymax"]
        exmin.delete(0, "end")
        exmax.delete(0, "end")
        eymin.delete(0, "end")
        eymax.delete(0, "end")
        exmin.insert(0, sxmin)
        exmax.insert(0, sxmax)
        eymin.insert(0, symin)
        eymax.insert(0, symax)
    #==========================================================================
    # METHOD  : __update_coord_display
    # PURPOSE : update coordinate display
    #==========================================================================
    def __update_coord_display(self, u, v) :
        self.__plot_crosshairs(u, v)
        x, y = self.plot_uv_xy(u, v)
        sx = "%-15.8g" % (x)
        sy = "%-15.8g" % (y)
        sx = sx.strip()
        sy = sy.strip()
        xcoo = self._Component["xcoo"]
        ycoo = self._Component["ycoo"]
        xcoo.delete(0, "end")
        ycoo.delete(0, "end")
        xcoo.insert(0, sx)
        ycoo.insert(0, sy)
    #==========================================================================
    # METHOD  : __plot_crosshairs
    # PURPOSE : plot crosshairs
    #==========================================================================
    def __plot_crosshairs(self, u, v):
        s, t = self.plot_uv_st(u, v)
        plot = self._Component["plot"]
        plot.delete("CROSSHAIRS")
        widen=self._Component["identify"]
        if s >= 0.0 and s <= 1.0 and t >= 0.0 and t <= 1.0:
            u1, v1 = self.plot_st_uv(0.0, t)
            u2, v2 = self.plot_st_uv(1.0, t)
            u3, v3 = self.plot_st_uv(s, 0.0)
            u4, v4 = self.plot_st_uv(s, 1.0)
            plot.create_line(u1, v1, u2, v2, tags="CROSSHAIRS")
            plot.create_line(u3, v3, u4, v4, tags="CROSSHAIRS")
            #-----------------------------------------------------------------
            # highlight curves or legend
            #-----------------------------------------------------------------
            if not self.__use_matplotlib:
                items = plot.find_overlapping(u-1, v-1, u+1, v+1)
                found_tag = None
                for item in items :
                    for tag in plot.gettags(item) :
                        if re.search("-LINE$", tag) :
                            found_tag = tag
                            break
                    if found_tag is not None :
                        break
                if self.__crosshairs_highlighted or (found_tag is not None):
                    for curve in self._curves:
                        curvex = self.__curve_tag_scrub(curve)
                        ctag = "%s-LINE" % (curvex)
                        ltag = "%s-LEGEND-LINE" % (curvex)
                        cwid = self._curve_wline[curve]
                        lwid = self._curve_wline[curve]
                        if   found_tag == ctag:
                            lwid += 2
                            widen.message_show(u, v, curve)
                        elif found_tag == ltag:
                            lwid += 2
                            cwid += 2
                        plot.itemconfigure(ctag, width=cwid)
                        plot.itemconfigure(ltag, width=lwid)
                    self.__crosshairs_highlighted = (found_tag is not None)
                else:
                    widen.message_hide()
            else :
                plot_canvas = self._Component["plot_canvas"]
                c0, c1, c2, c3 = self.__Transform["xy_st"]
                found_curve = None
                #-----------------------------------------------------
                # find curve with curve point near to crosshairs
                # should look for segment intersecting s1, t1, s2, t2
                # using clipping algorithm
                # s1, s2, t1, t2 = s-0.002, s+0.002, t-0.002, t+0.002
                #-----------------------------------------------------
                xlog = (self._Component["xlog_var"].get() == 1)
                ylog = (self._Component["ylog_var"].get() == 1)
                realmin = 1e-300
                for curve in self._curves:
                    xd = self._curve_xdata[curve]
                    yd = self._curve_ydata[curve]
                    if xlog:
                        xd = numpy.log10(numpy.maximum(numpy.abs(xd), realmin))
                    if ylog:
                        yd = numpy.log10(numpy.maximum(numpy.abs(yd), realmin))
                    sd = numpy.add(numpy.multiply(xd, c1), c0)
                    td = numpy.add(numpy.multiply(yd, c3), c2)
                    ss = numpy.subtract(sd, s)
                    ts = numpy.subtract(td, t)
                    dist = numpy.hypot(ss, ts)
                    min_dist = numpy.amin(dist)
                    if min_dist < 0.005 :
                        found_curve = curve
                        break
                if self.__crosshairs_highlighted or (found_curve is not None):
                    for curve in self._curves:
                        if found_curve == curve:
                            widen.message_show(u, v, curve)
                        if curve in self._curve_lgnd_line :
                            lgnd_line = self._curve_lgnd_line[curve]
                            lwid = self._curve_wline[curve]
                            if found_curve == curve:
                                lwid += 2
                            lgnd_line.set_linewidth(lwid)
                    self.__crosshairs_highlighted = (found_curve is not None)
                    plot_canvas.draw()
                else:
                    widen.message_hide()
    #==========================================================================
    # METHOD  : __line_parameters
    # PURPOSE : report line parameters for straightedge
    #==========================================================================
    def __line_parameters(self, x1, y1, x2, y2) :
        report = []
        report.append("")
        dx, dy = x2 - x1, y2 - y1
        if dx == 0.0 and dy == 0.0 :
            report.append("x y = %12.5g %12.5g" % (x1, y1))
        elif dx == 0.0 :
            report.append("x = %.5g" % (x1))
            report.append("y1 = %12.5g" % (y1))
            report.append("y2 = %12.5g" % (y2))
            report.append("dy = %12.5g" % (dy))
            if dy != 0.0 :
                report.append(" 1/dy = %12.5g" % (1.0/dy))
            s = y2 + y1
            if s != 0.0 :
                s = abs(100.0*(y2 - y1)/s)
                report.append("y-spread = +/- %12.5g %%" % (s))
        else :
            report.append("x1 y1 = %12.5g %12.5g" % (x1, y1))
            report.append("x2 y2 = %12.5g %12.5g" % (x2, y2))
            report.append("dx dy = %12.5g %12.5g" % (dx, dy))
            if dx != 0.0 :
                report.append(" 1/dx = %12.5g" % (1.0/dx))
            if dy != 0.0 :
                report.append(" 1/dy = %12.5g" % (1.0/dy))
            s = y2 + y1
            if s != 0.0 :
                s = abs(100.0*(y2 - y1)/s)
                report.append("y-spread = +/- %12.5g %%" % (s))
            s = x2 + x1
            if s != 0.0 :
                s = abs(100.0*(x2 - x1)/s)
                report.append("x-spread = +/- %12.5g %%" % (s))

            xlog = self._Component["xlog_var"].get() == 1
            ylog = self._Component["ylog_var"].get() == 1

            if not xlog and not ylog :
                m = 1.0*dy/dx
                b = y1 - x1*m
                report.append("len   = %12.5g" % (math.sqrt(dx*dx + dy*dy)))
                report.append("slope = %12.5g" % (m))
                if m != 0 :
                    report.append(" 1/s  = %12.5g" % (1.0/m))
                report.append("y-int = %12.5g" % (b))
                if m != 0 :
                    report.append("x-int = %12.5g" % (-1.0*b/m))
                report.append("    y = %.5g x + %.5g" % (m, b))
            elif not xlog and ylog :
                v1, v2 = math.log10(y1), math.log10(y2)
                dv = v2 - v1
                m = dv/dx
                b = v1 - x1*m
                A = pow(10.0,b)
                B = m*math.log(10.0)
                report.append("decy  = %12.5g decades"    % (dv))
                report.append("slope = %12.5g decades/dx" % (m))
                if m != 0.0 :
                    report.append(" 1/s  = %12.5g dx/decades" % (1.0/m))
                report.append("    y = %.5g exp ( %.5g x )" % (A, B))
            elif xlog and not ylog :
                u1, u2 = math.log10(x1), math.log10(x2)
                du = u2 - u1
                m = dy/du
                b = y1 - u1*m
                A = m/math.log(10.0)
                report.append("decx  = %12.5g decades"   % (du))
                report.append("slope = %12.5g dy/decade" % (m))
                if m != 0.0 :
                    report.append(" 1/s  = %12.5g decade/dy" % (1.0/m))
                report.append("    y = %.5g log ( x ) + %.5g" % (A, b))
            elif xlog and ylog :
                u1, u2 = math.log10(x1), math.log10(x2)
                v1, v2 = math.log10(y1), math.log10(y2)
                du = u2 - u1
                dv = v2 - v1
                m = dv/du
                b = v1 - u1*m
                A = math.pow(10.0, b)
                report.append("decx  = %12.5g decades" % (du))
                report.append("decy  = %12.5g decades" % (dv))
                report.append("slope = %12.5g decades/decade" % (m))
                if m != 0.0 :
                    report.append(" 1/s  = %12.5g decades/decade" % (1.0/m))
                report.append("    y = %.5g x ^ %.5g" % (A, m))
        report = "\n".join(report)
        print(report)
        MessageDialog(parent=self, message=report, title="line-parameters")
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PlotBasem plot primitives
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _plot_transform_calc
    # PURPOSE : determine transform parameters
    #==========================================================================
    def _plot_transform_calc(self) :
        self.update_idletasks()
        plot = self._Component["plot"]
        w = plot.winfo_width()
        h = plot.winfo_height()
        # margins are in fractions of width or height
        lm = self._axes_left_margin
        rm = self._axes_right_margin
        bm = self._axes_bottom_margin
        tm = self._axes_top_margin
        if self["title"] :
            tm *= 2
        if self._yaxis_right:
            lm, rm = rm, lm
        if self._xaxis_top:
            bm, tm = tm, bm
        u1 = w*(0.0+lm)
        u2 = w*(1.0-rm)
        v1 = h*(1.0-bm)
        v2 = h*(0.0+tm)
        x1, x2, y1, y2 = self.__XYlimits
        s1, s2, t1, t2 = [0.0, 1.0, 0.0, 1.0]
        if self._Component["xlog_var"].get() == 1 :
            # from scaler:
            ax2 = abs(x2)
            ax1 = abs(x1)
            if x1*x2 <= 0.0:
                ax2 = max(ax2, ax1)
                ax1 = ax2*1e-6
            x1 = math.log10(ax1)
            x2 = math.log10(ax2)
            # x1, x2 = log10 of abs scale limits
        if   x1 == x2 :
            x2 += 1
        elif x1 >  x2 :
            x1, x2 = x2, x1
        if self._Component["ylog_var"].get() == 1 :
            # from scaler:
            ay2 = abs(y2)
            ay1 = abs(y1)
            if y1*y2 <= 0.0:
                ay2 = max(ay2, ay1)
                ay1 = ay2*1e-6
            y1 = math.log10(ay1)
            y2 = math.log10(ay2)
            # y1, y2 = log10 of abs scale limits
        if   y1 == y2 :
            y2 += 1
        elif y1 >  y2 :
            y1, y2 = y2, y1
        du, dv = u2 - u1, v2 - v1
        ds, dt = s2 - s1, t2 - t1
        dx, dy = x2 - x1, y2 - y1
        us, vt = u2*s1 - u1*s2, v2*t1 - v1*t2
        ux, vy = u2*x1 - u1*x2, v2*y1 - v1*y2
        su, tv = s2*u1 - s1*u2, t2*v1 - t1*v2
        sx, ty = s2*x1 - s1*x2, t2*y1 - t1*y2
        xs, yt = x2*s1 - x1*s2, y2*t1 - y1*t2
        xu, yv = x2*u1 - x1*u2, y2*v1 - y1*v2
        self.__Transform = {
            "uv_max_limits": [0, w, h, 0],
            "st_max_limits": [us/du, us/du + w*ds/du, vt/dv + h*dt/dv, vt/dv],
            "xy_max_limits": [ux/du, ux/du + w*dx/du, vy/dv + h*dy/dv, vy/dv],
            "uv_limits":     [u1, u2, v1, v2],
            "st_limits":     [s1, s2, t1, t2],
            "xy_limits":     [x1, x2, y1, y2],
            "uv_st":         [us/du, ds/du, vt/dv, dt/dv],
            "uv_xy":         [ux/du, dx/du, vy/dv, dy/dv],
            "st_uv":         [su/ds, du/ds, tv/dt, dv/dt],
            "st_xy":         [sx/ds, dx/ds, ty/dt, dy/dt],
            "xy_st":         [xs/dx, ds/dx, yt/dy, dt/dy],
            "xy_uv":         [xu/dx, du/dx, yv/dy, dv/dy],
        }
    #==========================================================================
    # METHOD  : plot_transform_entry
    # PURPOSE : return transform list
    #==========================================================================
    def plot_transform_entry(self, entry) :
        """ return the transform dictionary entry.

        **arguments**:

            **entry** (str)

                the transform entry to return. One of:

                    * uv_max_limits:  maximum canvas limits

                    * st_max_limits:  maximum scaled limits

                    * xy_max_limits:  maximum x,y limits

                    * uv_limits:      current canvas limits

                    * st_limits:      current scaled limits

                    * xy_limits:      current x,y limits

                    * uv_st:          transform canvas to scale point

                    * uv_xy:          transform canvas to x,y point

                    * st_uv:          transform scaled to canvas point

                    * st_xy:          transform scaled to x,y point

                    * xy_st:          transform x,y to scaled point

                    * xy_uv:          transform x,y to canvas point

        """
        if entry in self.__Transform :
            return self.__Transform[entry]
        self.warning("entry \"%s\" not in transform array" % (entry))
        return None
    #==========================================================================
    # METHOD  : plot_st_uv
    # PURPOSE : convert scaled coordinates to canvas coordinates
    #==========================================================================
    def plot_st_uv(self, s, t) :
        """ convert scaled coordinates (0, 1, 0, 1) to canvas coordinates.

        **arguments**:

            **s, t** (float)

                x, y coordinates in scaled domain.  In the scaled domain,
                every point on the canvas is mapped to the window
                smin, smax = 0.0, 1.0 and tmin, tmax = 0.0, 1.0

        **results**:

            * return canvas coordinates u, v

        """
        c0, c1, c2, c3 = self.__Transform["st_uv"]
        return int(c0 + c1*s + 0.5), int(c2 + c3*t + 0.5)
    #==========================================================================
    # METHOD  : plot_uv_st
    # PURPOSE : convert canvas coordinates to scaled coordinates
    #==========================================================================
    def plot_uv_st(self, u, v) :
        """ convert canvas coordinates to scaled coordinates (0, 1, 0, 1)

        **arguments**:

            **u, v** (int)

                x, y (pixel) coordinates in canvas domain.

        **results**:

            * return scaled coordinates s, t

        """
        c0, c1, c2, c3 = self.__Transform["uv_st"]
        return c0 + c1*u, c2 + c3*v
    #==========================================================================
    # METHOD  : plot_st_xy
    # PURPOSE : convert scaled coordinates to x, y coordinates
    #==========================================================================
    def plot_st_xy(self, s, t) :
        """ convert scaled coordinates (0, 1, 0, 1) to x, y coordinates

        **arguments**:

            **s, t** (float)

                x, y coordinates in scaled domain.  In the scaled domain,
                every point on the canvas is mapped to the window
                smin, smax = 0.0, 1.0 and tmin, tmax = 0.0, 1.0

        **results**:

            * return x, y coordinates x, y

        """
        c0, c1, c2, c3 = self.__Transform["st_xy"]
        x, y = c0 + c1*s, c2 + c3*t
        if self._Component["xlog_var"].get() == 1 :
            x = math.pow(10.0, x)
        if self._Component["ylog_var"].get() == 1 :
            y = math.pow(10.0, y)
        return x, y
    #==========================================================================
    # METHOD  : plot_xy_st
    # PURPOSE : convert x, y coordinates to scaled coordinates
    #==========================================================================
    def plot_xy_st(self, x, y) :
        """ convert x, y coordinates to scaled coordinates (0, 1, 0, 1)

        **arguments**:

            **x, y** (float)

                x, y coordinates.

        **results**:

            * return scaled coordinates s, t

        """
        c0, c1, c2, c3 = self.__Transform["xy_st"]
        realmin = 1e-300
        if self._Component["xlog_var"].get() == 1 :
            x = math.log10(max(abs(x), realmin))
        if self._Component["ylog_var"].get() == 1 :
            y = math.log10(max(abs(y), realmin))
        return c0 + c1*x, c2 + c3*y
    #==========================================================================
    # METHOD  : plot_xy_uv
    # PURPOSE : convert plot coordinates to canvas coordinates
    #==========================================================================
    def plot_xy_uv(self, x, y) :
        """ convert x, y coordinates to canvas coordinates.

        **arguments**:

            **x, y** (float)

                x, y coordinates.

        **results**:

            * return canvas coordinates u, v

        """
        c0, c1, c2, c3 = self.__Transform["xy_uv"]
        realmin = 1e-300
        if self._Component["xlog_var"].get() == 1 :
            x = math.log10(max(abs(x), realmin))
        if self._Component["ylog_var"].get() == 1 :
            y = math.log10(max(abs(y), realmin))
        return int(c0 + c1*x + 0.5), int(c2 + c3*y + 0.5)
    #==========================================================================
    # METHOD  : plot_uv_xy
    # PURPOSE : convert canvas coordinates to x, y coordinates
    #==========================================================================
    def plot_uv_xy(self, u, v) :
        """ convert canvas coordinates to x, y coordinates.

        **arguments**:

            **u, v** (int)

                canvas (pixel) coordinates.

        **results**:

            * return x, y coordinates

        """
        c0, c1, c2, c3 = self.__Transform["uv_xy"]
        x, y = c0 + c1*u, c2 + c3*v
        if self._Component["xlog_var"].get() == 1 :
            x = math.pow(10.0, x)
        if self._Component["ylog_var"].get() == 1 :
            y = math.pow(10.0, y)
        return x, y
    #==========================================================================
    # STATICMETHOD : __plot_read_string_data
    # PURPOSE : read font data
    #==========================================================================
    @staticmethod
    def __plot_read_string_data() :
        offsetstring = """  '$(8=B"**&$("%"1$./%17$=7*-#$#3T&52.(&5&"*&$(&5,7.4$*$($%&("(&"%00.01'5)'*&"0)100'1')$($(&E"E6  '((($#/,,,,.((O::**MM>>*T.1#$#09&5$&(3$&">&$(&5&7,'$1&0&0&'$'0%F6<,714/1(90'2,1*:21&/85:25.35%  '8MPlD<<80JOP1%$%+$;3,,,,0->(>J-3G7B;9<D88D<J><>?E;7??5BDG','&&&56-607:;.2>1>5659..-1/6256'&'4  ,((F=N$22&$'"%"E(IK)BM:YM*,#$#=T,G>:0.C2(12*4.I8[F@,3*0..,("(&"%C<:><2V5-52(B5A><2>-5*0.1,E"E6  ,CE79;79G>:67NN****DN8JMHD88><H9,G.*0I*2(>2*4.I.Q8/,<*F8B,'$'0%FDS4I<B8<-I8373=0I<?,<EHH>=6EG%  -((E=T$22&$'"%"G+FN'BK9YK),#$#?;B`GIMJQS?@UFKB@QI[BCCBCQFI','&&&=44=59B9059.G<;9?43074?D<B'&'4  40(N=b(66>,4&.&E*>H-LW)_W<B#,#RT.FD<3/J0&20*2.F7L<I+6*2,-.("(&"%@@>@B3L5440&D5B@@1J,5*2,-.E"E6  4/:ISCc6X^c^OJG)//==;,,5,,>4rjj:,:560I*S2^D442I.28>,3G4.FI@8D0%6CL51<L*K2R?142A.0>:,1?4.AF<4?%  ,=6AB?69'?C)<A1+#(-%,-$1-MA77H=-,C@:0.F2(22*4.G6XCA,5*0..,','&&&C?7E8@G:7=</NA=E<7:/A8EFE:'&'4  <0(S=b(88>,4&.&M3Wd3P_De_<B#,#NT8]BPYPRV:DNCJ:QLe^IFB7FDA<("(&"%PG?JD?oO>AI5iOIOL@F2A5?@><E"E6  90(U=R(88>,,&)&B7GMAJP@WQ25#,#KTQx[[mjizXV|dxedYuyp]j\lThN("(&"%ME=B:API>BI3ZGAME@O7H>PPS>E"E6  <0(O=b(<<>,3&.&U/NZ+JX@wX<A#,#U;:]FQXPWV:FPAN=SMf\IDE8HDC83,3&&&LM?R>ISA=GH5TDIWN:J3D:JNK@'&'4"""
        charstring="""?VBH?CABBACBBC@VAO8VIO8\B<2\H<?OPO@IOI;ZF=7ZJ=2SMUJVFVCUASAQBOCNEMKKMJNIOGODMBJAFACBAD.VAA;VHTHRGPEOCOAQASBUDVFVHUKTNTQUSV2HMGLELCNAPARBSDSFQHOH,MUNTOSORNQLOGMDKBIAEACBBCAEAGBICJJNKOLQLSKUIVGUFSFQGNIKNDPBRATAUBUC@VAO9\FZDWBSANAJBEDAF>H<@\CZEWGSHNHJGEEAC>A<;QFE@NKH6NAH7TJB@KSK>BBAABBCCBC@B>A=@KSK?CABBACBBC.\A<:VDUBRAMAJBEDBGAIALBNEOJOMNRLUIVGV@RCSFVFA?QBRCTDUFVJVLUMTNRNPMNKKAAOA>VNVHNKNMMNLOIOGNDLBIAFACBBCAE6VAHPH6VKA4VCVBMCNFOIOLNNLOIOGNDLBIAFACBBCAE4SLUIVGVDUBRAMAHBDDBGAHAKBMDNGNHMKKMHNGNDMBKAH2VEA@VOV;VCUBSBQCOENIMLLNJOHOENCMBJAFACBBCAEAHBJDLGMKNMONQNSMUJVFV3OMLKJHIGIDJBLAOAPBSDUGVHVKUMSNONJMEKBHAFACBBD?OANBMCNBO?CABBACBBC?OANBMCNBO>BBAABBCCBC@B>A=0TAKQB@NSN@HSH@TQKAB@QARBTCUEVIVKULTMRMPLNKMGKGH:CFBGAHBGC1NOPMQJQHPGOFLFIGGIFLFNGOI7QHOGLGIHGIF1QOIOGQFSFUHVKVMUPTRRTPUMVJVGUETCRBPAMAJBGCEECGBJAMAPBRCSD0QPIPGQF8VAA8VQA=HNH@VAA@VJVMUNTOROPNNMMJL@LJLMKNJOHOENCMBJAAA1QOSMUKVGVEUCSBQANAIBFCDEBGAKAMBODPF@VAA@VHVKUMSNQONOINFMDKBHAAA@VAA@VNV@LIL@ANA@VAA@VNV@LIL1QOSMUKVGVEUCSBQANAIBFCDEBGAKAMBODPFPI6IPI@VAA2VOA@LOL@VAA6VKFJCIBGAEACBBCAFAH@VAA2VAH;MOA@VAA@AMA@VAA@VIA0VIA0VQA@VAA@VOA2VOA:VEUCSBQANAIBFCDEBGAKAMBODPFQIQNPQOSMUKVGV@VAA@VJVMUNTOROONMMLJKAK:VEUCSBQANAIBFCDEBGAKAMBODPFQIQNPQOSMUKVGV7EP?@VAA@VJVMUNTOROPNNMMJLAL9LOA2SMUJVFVCUASAQBOCNEMKKMJNIOGODMBJAFACBAD9VHA@VOV@VAGBDDBGAIALBNDOGOV@VIA0VIA@VFA6VFA6VPA,VPA@VOA2VAA@VILIA0VIL2VAA@VOV@AOA@\A<?\B<@\H\@<H<@Z]>:\G<9\H<@\H\@<H<@QIVQQ@QIUQQ@ASA;VAP;VGUAP4OMA4LKNIOFODNBLAIAGBDDBFAIAKBMD@VAA@LCNEOHOJNLLMIMGLDJBHAEACBAD4LKNIOFODNBLAIAGBDDBFAIAKBMD4VMA4LKNIOFODNBLAIAGBDDBFAIAKBMD@IMIMKLMKNIOFODNBLAIAGBDDBFAIAKBMD8VGVEUDRDA@OHO4OM?L<K;I:F:D;4LKNIOFODNBLAIAGBDDBFAIAKBMD@VAA@KDNFOIOKNLKLA@VBUCVBWAV?OBA<UFTGUFVEU;NF=E:C9A9@VAA6OAE<ILA@VAA@OAA@KDNFOIOKNLKLA5KONQOTOVNWKWA@OAA@KDNFOIOKNLKLA;ODNBLAIAGBDDBFAIAKBMDNGNIMLKNIOFO@OA:@LCNEOHOJNLLMIMGLDJBHAEACBAD4OM:4LKNIOFODNBLAIAGBDDBFAIAKBMD@OAA@IBLDNFOIO5LKNHOEOBNALBJDIIHKGLELDKBHAEABBAD=VDEEBGAIA@OHO@OAEBBDAGAIBLE5OLA@OGA4OGA@OEA8OEA8OMA0OMA@OLA5OAA?OHA3OHAF=D;B:A:5OAA@OLO@ALA;\D[CZBXBVCTDSEQEOCM=[CYCWDUETFRFPENALEJFHFFEDDCCAC?D=>KEIEGDECDBBB@C>D=F<@\A<@\C[DZEXEVDTCSBQBODM>[DYDWCUBTARAPBNFLBJAHAFBDCCDAD?C==KBIBGCEDDEBE@D>C=A<@HAJBMDNFNHMLJNIPIRJSL@JBLDMFMHLLINHPHRISLSN?VBH?CABBACBBC3VNA@VNV;LNL@ANA=MAKDI:PBKGF?KSK=EFBHE@HFCKH;TFC7ZJA@ASA.ZAASA6SJRKQLRKS?CABBACBBC-CSBTAUBTC0SJSFRDQBOALAJBGDEFDJCQC@SHSLRNQPOQLQJPGNELDHCAC@SALBHCFEDHCJCMDOFPHQLQS@CAJBNCPERHSJSMROPPNQJQC0SJSFRDQBOALAJBGDEFDJCQC@KMK1MSKPI4PRKMF@KRK=QFTHQ@NFSKN;SFB-[SZTYUZU[T\R\P[NYMWLTKPIDH@G>2ZNXMTKHJDIAH?F=D<B<A=A>B?C>B=7SGREPDMDKEHGFJELEOFQHRKRMQPORLSJS5sImFfDaC]BXAPAHB@C;D7F2I+L%8mGhEbD^CXBPBHC@D:E6G0I+@sDmGfIaJ]KXLPLHK@J;I7G2D+A%=mFhHbI^JXKPKHJ@I:H6F0D+@sALA%?sBLB%@sLs@%L%6sKLK%5sLLL%@sLs@%L%8sFqDoCmBjBfCbGZHWHTGQEN;qDnCjCfDcH[IWITHQENALEJHGIDIAH=D5C2C.D*F'<JGGHDHAG>C6B2B.C+D)F'I%@sDqFoGmHjHfGbCZBWBTCQEN=qFnGjGfFcB[AWATBQENILEJBGADAAB=F5G2G.F*D'<JCGBDBAC>G6H2H.G+F)D'A%8pFmDjBfAaA[BUCQFFGBH<H7G2F/D+;mDiCfBaB\CVDRGGHCI=I7H2F.D+A(@pDmFjHfIaI[HUGQDFCBB<B7C2D/F+=mFiGfHaH\GVFRCGBCA=A7B2D.F+I(@RHRY5:RX5;RY2 ~]ZY2)pWpVoVnWmXmYnYpXrVsTsRrPpOnNkMdLTL4K+J(*oWnXnXoWo4dM41pOmNdNDM4L-K*J(H&F%D%B&A(A*B+C+D*D)C(B(?*B)C)C*B*<aEA;aFA)aXA(aYA@a]a@AJA-A]A>aMSBA?aLS@aLR@aXaZZWa>BXB?AXAZHWA9\ALH<@\A<:\G<@\HLA<@OBLBJAG8OHLHJIG@ODNFNIO@GDHFHIG-JSHQGOGMHLIIMHNFODOBNALAJBHDGFGHHIILMMNOOQOSNTLTJ8VAA8VQA=HNH@VAA@VJVMUNTOROPNNMMJL@LJLMKNJOHOENCMBJAAA@VOA@AOV8VAA8VQA@AQA@VAA@VNV@LIL@ANA9VHA;QCPBOAMAJBHCGFFJFMGNHOJOMNOMPJQFQ@VAA@VMV@VAA2VOA@LOL@VAA-[SZTYUZU[T\R\P[NYMWLTKPIDH@G>2ZNXMTKHJDIAH?F=D<B<A=A>B?C>B=@VAA2VAH;MOA8VAA8VQA@VAA@VIA0VIA0VQA@VAA@VOA2VOA:VEUCSBQANAIBFCDEBGAKAMBODPFQIQNPQOSMUKVGV@VAA2VOA@VOV:VEUCSBQANAIBFCDEBGAKAMBODPFQIQNPQOSMUKVGV;LLL@VAA@VJVMUNTOROONMMLJKAK@VHLAA@VOV@AOA9VHA@VOV@QASBUCVEVFUGSHOHA2QOSNUMVKVJUISHO@VIA0VIA@VQV@AEABHALAPBSDUGVIVLUNSOPOLNHKAOA@VOV<LKL@AOA7VJA@PBPCODKEIFHIGKGNHOIPKQORPSP2VAA@VOV@AOA@OEOKC=OKA-ZKA@ROD2RAD@OFOOC<NOA"bOA@VBTDRGQIQLRNTOV@VBSDQGPIPLQNSOV?VGP?VAUGP@MBOBPDQFQHPLMNLPLRMSO/LPKNKLLHOFPDPBO@GBIBJDKFKHJLGNFPFRGSI/FPENELFHIFJDJBI:OENCLBJAGADBBDAFAHBKEMHOLPO:OIOJNKLMDNBOAPA6VIUGSEODLCHBBA:6VMVOTOQNOMNKMHM9MJLLJMHMELCKBIAGAEBDCCF?VDVFTLCNAPA0VPTNQDFBCAA8OFODNBLAIAFBCCBEAGAIBKDLGLJKMIOGQFSFUGVIVKUMS6MJNHOEOCNCLDJGI:ICHAFADBBDAGAIBKD;NDMBKAHAEBCCBEAHAKBNDPGQJQMOOMOKMIIGDD:@SCUEVFVHUITJQJMIH0VPSOQIHGDFA@KBMDOFOGNGLFHDA;HHLJNLONOPMPJOEL:=OBHADABBADAFCGE5GLJKMJNHOFODNBLAIAFBCCBEAGAIBKDLGMLMQLTKUIVGVEUCS<OAA2NNOMOKNGJEIDI=IFHGGIBJAKALB@VCVEUFTNA9OBA:OA:;KEFECGAIAKBMDOH0OOHNDNBOAQASCTE@ODOCIBDAA3OMLLJJGGDDBAA;ODNBLAIAFBCCBEAGAIBKDLGLJKMJNHOFO9ODA4ONIODPA@LCNFOSO@KBMDOFOGNGLFGFDGBHAJALBNEOGPJQOQRPUNVLVKTKRLONLPJSH<IEFFCGBIAKAMBODPGPJOMNNLOJOHNFLEIA:1OFODNBLAIAFBCCBEAGAIBKDLGLJKMJNHO7OGA@LCNFOQO@KBMDOFOGNGLEFECGAIALBNDPHQLQO@TBRCNCHBDAB.TRRQNQHRDSB@TCSGRMRQSST@BCCGDMDQCSB;ODNBKAHAEBBCAEAGBIE7IIEJBKAMAOBQERHRKQNPO9[FZEYEXFWIVLV8VFUDTCRCPENHMJM9MDLBKAIAGCEGCHBH@F?D?1VH:@KBMDOFOGNGLFGFDGBIAKANBPDRGTLUO9[FZEYEXFWIVLV5VHTERBOALAJBHDFGDHBH@G?E?DA6NIOFODNBLAIAFBCCBEAHAJB@HIH5VD::ODNBLAIAFBDDBGAIALBNDOGOJNLLNIOGO9VFUDRCPBMAHADBBCAEAGBIEJGKJLOLSKUJVHV?LKL?CABBACBBC?VBH?CABBACBBC:ZFXGVHXGZ:ZG>:OFLG>HLGO@SCRESCTAS@SMS8SKRMSKTIS:ZFXGVHXGZ:ZGL:PFNHJGHFJHNGP:LG>:BF@G>H@GB@SCRESCTAS@SMS8SKRMSKTIS@ECDEECFAE@EME8EKDMEKFIE8PIJ8JHA8JJA9AJA8PHSGUEV9SEV8PJSKUMV7SMV8PERCRAP:QCQAP8PMRORQP6QOQQP8PGOFNFK8PGNFK8PKOLNLK8PKNLK8TIR8OIM8JIH8DHA8DJA9AJA8VHTGS8VJTKS:SITKS8RGOENDO8RKOMNNO<NGNIOKNMN8MGJEICIBKBJCI8MKJMIOIPKPJOI<IGIIJKIMI8HGEFDDCCCBDAFADCC8HKELDNCOCPDQFQDOC=CFCIDLCNC8DHA8DJA9AJA8DLCOCQEQHPINIPKQNPPNQLPMSLUJVHVFUESFPDQBPANBKDIBIAHAECCFCID8DHA8DJA9AJA8DMEMGOHOKQLQQPTOUMUKVGVEUCUBTAQALCKCHEGEEID8UEQBMAJAHBFDEFEHFIH8UMQPMQJQHPFNELEJFIH8HHDGA8HJDKA:AKA8OHRGTEUDUBTARANBKCIEFIA8OJRKTMUNUPTQRQNPKOIMFIA7WHTDOAL7WLTPOSL@LDIHDJA.LPILDJA7ILFNEPERFSHSJRLPMNMKL6LMNNPNRMTKUIUGTFRFPGNIL8LFMDMBLAJAHBFDEFEHFJI7IIDHA7IKDLA9ALA7KJBIA7GIA7TIUGUFTFRGOJK7TKUMUNTNRMOJK7KFNDOBOANALBK7KNNPOROSNSLRK7KFHDGBGAHAJBK7KNHPGRGSHSJRK@JBJDIEGEEDC@JAKBLDLEKFIFFEDDC7VHTGQGNIHIEHCJA7VLTMQMNKHKELCJA.JSKRLPLOKNINFODPC.JRJPIOGOEPC>GQG:RDQBOALAJBGDEGDIDLENGOJOLNOLQIRGR@QAEMEMQAQ9QAEOEHQ:UAKGAMKGU8SGMAMFIDCIGNCLIQMKMIS9RHD@KOK=OBNALAJBHDGFGHHIJILHNFODO?LBJ>MCI=NDH<NEH;NFH:MGI9LHJ@OAGIGIOAO?NBH>NCH=NDH<NEH;NFH:NGH9NHH;PAGKGFP;MCH;MIH;JEH;JGH@KJFJPAK=KIH=KIN:KIJ:KIL;GKPAPFG;JIO;JCO;MGO;MEO7KAPAFJK:KBN:KBH=KBL=KBJ:QCFMMAMKFGQ:KGQ:KAM:KCF:KKF:KMM<QEMAMAIEIEEIEIIMIMMIMIQEQ2MNOLQIRGRDQBOALAJBGDEGDIDLENGOI2MMOKPIPGOFNELEJFHGGIFKFMGOI9SAGOGHS9COOAOHC7SJUKVMVNUNS@BBDDFEHFLFQGRISOSQRRQRLSHTFVDWB@BWB6BJAK@M@NAMB8WHVIUJVJWIYGZEZCYBWBUCSEQJN>SHPJNKLKJJHHF=RBPANALBJDHIE?JGGIEJCJAI?G>E>C?BABBCCDBCA=OBNALAJBHDGFGHHIJILHNFODO@ACBFEIIMPPVPAODMGKIHKFKEJEHFFHDKBNASA6TLSLPKLJIIGGDEBCABAABAEBJCMDOFRHTJUMVPVRUSSSQROQNOMLL6LLLOKPJQHQEPCOBMAJAHBGD7PJOKNMNOOPQPSOUMVJVGUESCPBNAJAFBCCBEAGAJBLDMF2VMULSKOJIIFHDFBDABAABADBEDEFDHBKANAQBSDUHVMVQUTTURVOVMTMRNOPLRJUHWG5RLQMPOPPQPSOULVHVEUDSDPENFMILFLCKBJAHAEBCCBFAIALBNDOF7PHPFQESFUIVLVPUSUUV1UNNLHJDHBFADABBADAFBGDGFF8LRL@ACBGFJKKNLRLUKVJVIUHSHPINKMOMRNSOTQTKSFRDPBMAIAFBDDCFCH:OEPDRDSEUGVHVJUKSKQJMHGFCDABAABAD:JPMRNUPWRXTXUWVVVTTRPPJOEOBPAQASBTCVF3FLHJKIMHPHSIUJVLVMUNSNPMKKFJDHBFADABBADAFBGDGFF7>HAFFELERFUHVJVKULRLOKJHAF;E8D6B5A6A8B;D>F@IBMD:OEPDRDSEUGVHVJUKSKQJMHGFCDABAABAD)SXUWVVVTURSPPNNLMJM5MMKMDNBOAPARBSCUF<JGJKKNMPOQQQTPVNVMULSKNJIIFHDFBDABAABADBEDEFDIBLANAQBSD=OBPARASBUDVEVGUHSHQGLFHDA;HIPKTLUNVOVQURSRQQLPHNA1HSPUTVUXVYV[U\S\Q[LYEYBZA[A]B^C`F=OBPARASBUDVEVGUHSHQGLFHDA;HIPKTLUNVPVRUSSSQRLPEPBQARATBUCWF7VGUESCPBNAJAFBCCBEAGAJBLDNGOIPMPQOTNULVJVHTHQINKKMIPGRF6TLSLPKLJIIGGDEBCABAABAEBJCMDOFRHTJUMVRVTUUTVRVOUMTLRKOKMLLM3PMNLMJLHLGNGPHSJUMVPVRUSSSORLPILEICGBDABAABADBEDEFDIBLAOARBTD6TLSLPKLJIIGGDEBCABAABAEBJCMDOFRHTJUMVQVSUTTURUOTMSLQKNKKLLKMIMDNBPARBSCUF@ACBEDHHJKLOMRMULVKVJUISIQJOLMOKQIRGREQCPBMAIAFBDDCFCH7PHPFQESFUIVLVPUSUUV1UNNLHJDHBFADABBADAFBGDGFF=OBPARASBUDVEVGUHSHQGMFJEFEDFBHAJALBMCOGROTV/OQKPEPBQARATBUCWF=OBPARASBUDVEVGUHSHQGMFJEFECFAHAJBMEOHQLROSSSURVQVPUOSOQPNRLTK=OBPARASBUDVEVGUHSHPGA0VGA0VOA$V[UXRUNRHOA9PFPEQESFUHVJVLUMSMPKGKDLBNAPARBSDSFRGPG*SWUVVTVRUPSNPJGHDFBDABAABAD=OBPARASBUDVEVGUHSHQGMFJEFEDFBGAIAKBMDOGPIRO-VROOEM?K:I6G5F6F8G;I>LAOCTF5PKNJMHLFLENEPFSHUKVNVPUQSQOPLNHKEGBEABAABADBEEEGDHCIAI>H;G9E6C5B6B8C;E>HAKCQF>VBUASAQBPCQBR7TISJRKSJT@KSK7DICJBKCJD?TAUBVCUCSBQAP8TIC@LQL@CQC8TIC@TQT@LQL0TCB@NSN@HSH7GIIGJEJCIBHAFADBBDAFAHBIDKJJEJBKALANBOCQF@FCIFNGPHSHUGVEUDSCOBHBBCADAFBHDIGIJJFKEMEOF9HHIGJEJCIBHAFADBBDAGAJCLF7GIIGJEJCIBHAFADBBDAFAHBIDOV6JJEJBKALANBOCQF?CDDEEFGFIEJDJBIAGADBBDAFAHBICKF;FJKLNMPNSNUMVKUJSHKEBB;A8A6B5D6E9FBGAIAKBLCNF7GIIGJEJCIBHAFADBBDAFAHBIC6JICE8D6B5A6A8B;E>H@JAMCPF@FCIFNGPHSHUGVEUDSCOBIAA@ABDCFEIGJIJJIJGIDIBJAKAMBNCPF=ODNENEODO@FCJADABBACAEBFCHF5QLPMPMQLQ8HKLE:D8B7A8A:B=E@HBJCMEPH@FCIFNGPHSHUGVEUDSCOBIAA@ABDCFEIGJIJJIJGHFEF<FGEHBIAJALBMCOF@FCIFNGPHSHUGVEUDSCOBHBBCADAFBGCIF@FCIEJFIFHEDDA<DFFHIJJLJMIMHLDKA5DMFOIQJSJTITGSDSBTAUAWBXCZF@FCIEJFIFHEDDA<DFFHIJJLJMIMGLDLBMANAPBQCSF:JEJCIBHAFADBBDAFAHBICJEJGIIGJFIFGGEIDLDNEOF<FGIHKGGA5:GHIJJLJNIOGOENCMBKA:BIALAOBQCTF7GIIGJEJCIBHAFADBBDAFAHB6JJGHBE;D8D6E5G6H9H@JAMCPF@FCIDKDIGIHHHFGCGBHAIAKBLCNF@FCIDKDIFFGDGBEA@BCAGAIBJCLF@FCIEM9VBDBBCAEAGBHCJF?NIN@FCJADABBADAFBHDJG6JIDIBJAKAMBNCPF@FCJBEBBCADAGBIDJGJJ7JKFLENEPF=JBHAEACBADAFBHD7JHDHBIAKAMBODPGPJ1JQFRETEVF@FCIEJGJHIHBIALAOCQF3IMJKJJIFBEACABB@FCJADABBADAFBHDJG6JE8D6B5A6A8B;E>H@JAMCPF@ICLEMGMIKIIHGFECDECFAF>E;D9B8A9A;B>EAHCLFOI0VAOQH@FQF@AQA@PSP@KSK@FSF@VQOAH@FQF@AQA/FPFNGLIIMHNFODOBNALAJBHDGFGHHIILMNOPPRP?VATBHCTBV?TBN?CABBACBBC?VAO>VAO7VIO6VIO8ZB>2ZH>?OPO@IOI;ZF=7ZJ=3SMRNQOROSMUJVFVCUASAQBOCNEMKKMJOH@QCOENKLMKNJOHODMBJAFACBADAEBFCEBD.VAA;VHTHRGPEOCOAQASBUDVFVHUKTNTQUSV2HMGLELCNAPARBSDSFQHOH.NRMSLTMTNSOROQNPLNGLDJBHAEABBADAGBIHMJOKQKSJUHVFUESEQFNHKMDOBRASATBTC<ACBBDBGCIEK<QFONDPBRA?VAO>VAO9\FZDWBSANAJBEDAF>H<;ZDVCSBNBJCEDBF>@\CZEWGSHNHJGEEAC>A<>ZEVFSGNGJFEEBC>;QFE@NKH6NAH7TJB@KSK?AABBCCBC@B>A=@KSK?CABBACBBC.\A<:VDUBRAMAJBEDBGAIALBNEOJOMNRLUIVGV:VEUDTCRBMBJCEDCEBGA8AKBLCMENJNMMRLTKUIV@RCSFVFA<UEA@AJA?RCQBPAQARBTCUFVJVMUNTOROPNNKLFJDIBGADAA7VLUMTNRNPMNJLFJ@CBDDDIBLBNCOD=DIAMANBODOF?RCQBPAQARBTCUFVJVMUNSNPMNJMGM7VLUMSMPLNJM7MLLNJOHOENCMBJAFACBBCAEAFBGCFBE4KNHNEMCLBJA6TKA5VLA5VAGQG9AOA>VAL@LCNFOIOLNNLOIOGNDLBIAFACBBCAEAFBGCFBE8OKNMLNINGMDKBIA>VMV>UHUMV4SLRMQNRNSMUKVHVEUCSBQAMAGBDDBGAIALBNDOGOHNKLMINHNEMCKBH9VFUDSCQBMBGCDEBGA8AKBMDNGNHMKKMIN@VAP@RBTDVFVKSMSNTOV?TDUFUKS2VOSNPJKIIHFHA3PIKHIGFGA;VCUBSBPCNFMJMMNNPNSMUJVFV;VDUCSCPDNFM7MLNMPMSLUJV;MCLBKAIAEBCCBFAJAMBNCOEOINKMLJM;MDLCKBIBECCDBFA7ALBMCNENIMKLLJM3OMLKJHIGIDJBLAOAPBSDUGVIVLUNSOPOJNFMDKBHAEACBBDBECFDECD:IEJCLBOBPCSEUGV8VKUMSNPNJMFLDJBHA?OANBMCNBO?CABBACBBC?OANBMCNBO?AABBCCBC@B>A=0TAKQB@NSN@HSH@TQKAB?RCQBPAQARBTCUEVHVKULTMRMPLNKMGKGH9VJUKTLRLPKNIL:CFBGAHBGC1NOPMQJQHPGOFLFIGGIFLFNGOI7QHOGLGIHGIF1QOIOGQFSFUHVKVMUPTRRTPUMVJVGUETCRBPAMAJBGCEECGBJAMAPBRCSD0QPIPGQF7VCA7VQA7SPA<GNG@AGA4ASA=VDA<VEA@VMVPUQTRRRPQNPMML4VOUPTQRQPPNOMML<LMLPKQJRHREQCPBMAAA4LOKPJQHQEPCOBMA2SPPPVOSMUJVHVEUCSBQANAIBFCDEBHAJAMBODPF9VFUDSCQBNBICFDDFBHA=VDA<VEA@VKVNUPSQQRNRIQFPDNBKAAA6VMUOSPQQNQIPFODMBKA=VDA<VEA6PKH@VQVQPPV<LKL@AQAQGPA=VDA<VEA6PKH@VQVQPPV<LKL@AHA2SPPPVOSMUJVHVEUCSBQANAIBFCDEBHAJAMBOD9VFUDSCQBNBICFDDFBHA2IOA1IPA5ISI=VDA<VEA0VQA/VRA@VHV3VUV<LQL@AHA3AUA=VDA<VEA@VHV@AHA8VIEHBFADABBADAFBGCFBE9VHEGBFA<VLV=VDA<VEA/VEI7MRA8MQA@VHV3VTV@AHA3ATA=VDA<VEA@VHV@APAPGOA=VDA<VKD=VKA/VKA/VRA.VSA@VEV/VVV@AGA2AVA=VDA<VQC<TQA0VQA@VEV3VTV@AGA9VEUCSBQAMAJBFCDEBHAJAMBODPFQJQMPQOSMUJVHV9VFUDSCQBMBJCFDDFBHA7ALBNDOFPJPMOQNSLUJV=VDA<VEA@VMVPUQTRRROQMPLMKEK4VOUPTQRQOPMOLMK@AHA9VEUCSBQAMAJBFCDEBHAJAMBODPFQJQMPQOSMUJVHV9VFUDSCQBMBJCFDDFBHA7ALBNDOFPJPMOQNSLUJV<CEDFFHGIGKFLDM=N<P<Q>Q?5DM@N>O=P=Q>=VDA<VEA@VMVPUQTRRRPQNPMMLEL4VOUPTQRQPPNOMML@AHA7LLKMJPCQBRBSC5KMIOBPARASCSD3SOVOPNSLUIVFVCUASAQBOCNEMKKMJOH@QCOENKLMKNJOHODMBJAGADBBDAGAABD9VHA8VIA?VAPAVPVPPOV<ALA=VDGEDGBJALAOBQDRGRV<VEGFDHBJA@VHV2VUV>VJA=VJD0VJA@VGV4VSV=VHA<VHF5VHA5VPA4VPF-VPA@VHV0VWV>VPA=VQA0VCA@VGV4VSV@AGA4ASA>VJKJA=VKKKA/VKK@VGV3VTV:ANA3VAA2VBA?VAPAVOV@AOAOGNA@\A<?\B<@\H\@<H<@Z]>:\G<9\H<@\H\@<H<@QIVQQ@QIUQQ@ASA;VAP;VGUAP>MCLBLBMCNEOIOKNLMMKMDNBOA5MLDMBOAPA5KKJEIBHAFADBBEAHAJBLD<ICHBFBDCBEA=VDA<VEA<LGNIOKONNPLQIQGPDNBKAIAGBED6OMNOLPIPGODMBKA@VEV4LLKMJNKNLLNJOGODNBLAIAGBDDBGAIALBND:OENCLBIBGCDEBGA4VMA3VNA4LKNIOGODNBLAIAGBDDBGAIAKBMD:OENCLBIBGCDEBGA7VNV4AQA?ININKMMLNJOGODNBLAIAGBDDBGAIALBND4IMLLN:OENCLBIBGCDEBGA8UHTISJTJUIVGVEUDSDA:VFUESEA@OIO@AHA:PEODNCLCJDHEGGFIFKGLHMJMLLNKOIPGP<ODMDIEG6GLILMKO5NMOOPOOMO=HCGBEBDCBFAKAN@O??DCCFBKBNAO?O>N<K;E;B<A>A?BAEB=VDA<VEA<LGNJOLOONPLPA5ONNOLOA@VEV@AHA5ASA=VCUDTEUDV=ODA<OEA@OEO@AHA;VEUFTGUFV:OG=F;D:B:A;A<B=C<B;;OF=E;D:>OGO=VDA<VEA2OEE7IPA8IOA@VEV5ORO@AHA5ARA=VDA<VEA@VEV@AHA=ODA<OEA<LGNJOLOONPLPA5ONNOLOA1LRNUOWOZN[L[A*OYNZLZA@OEO@AHA5ASA*A^A=ODA<OEA<LGNJOLOONPLPA5ONNOLOA@OEO@AHA5ASA:ODNBLAIAGBDDBGAIALBNDOGOINLLNIOGO:OENCLBIBGCDEBGA8AKBMDNGNIMLKNIO=OD:<OE:<LGNIOKONNPLQIQGPDNBKAIAGBED6OMNOLPIPGODMBKA@OEO@:H:4OM:3ON:4LKNIOGODNBLAIAGBDDBGAIAKBMD:OENCLBIBGCDEBGA7:Q:=ODA<OEA<IFLHNJOMONNNMMLLMMN@OEO@AHA6MLOLKKMJNHODOBNAMAKBJDIIGKFLE@LBKDJIHKGLFLCKBIAEACBBCAEAABC=VDEEBGAIAKBLD<VEEFBGA@OIO=ODDEBHAJAMBOD<OEDFBHA2OOA1OPA@OEO5OPO2ASA>OIA=OIC2OIA@OGO6OQO=OHA<OHD5OHA5OPA4OPD-OPA@OHO0OWO>ONA=OOA2OCA@OGO6OQO@AGA6AQA>OIA=OIC2OIAG=E;C:B:A;B<C;@OGO6OQO5OAA4OBA?OAKAOMO@AMAMELA;\D[CZBXBVCTDSEQEOCM=[CYCWDUETFRFPENALEJFHFFEDDCCAC?D=>KEIEGDECDBBB@C>D=F<@\A<@\C[DZEXEVDTCSBQBODM>[DYDWCUBTARAPBNFLBJAHAFBDCCDAD?C==KBIBGCEDDEBE@D>C=A<@HAJBMDNFNHMLJNIPIRJSL@JBLDMFMHLLINHPHRISLSN?VATBHCTBV?TBN?CABBACBBC7VGUDSBPAMAJBGDDGBJAMAPBSDUGVJVMUPSSPUMVJV6MJLJKKJLJMKMLLMKM6LKKLKLLKL=VBUCSER=VCUCS8VKUJSHR8VJUJS<RCQBPANAKBICHEGHGJHKILKLNKPJQHRER;GFA:GGA?DKD:VDUBSAPAOBLDJGIHIKJMLNONPMSKUHVGV:IGA9IHA>ELE7WGVDTBQANAJBGDDGBJANAQBTDVGWJWNVQTTQVNWJW5WLA@LWL:NDMBKAHAGBDDBGAHAKBMDNGNHMKKMHNGN-TNTRSLM-TTNSRML.SMM@SBUDVGVIUJSJPIMHKFICG:VHUISIOHLFI3VLA2VKA>GQG>VCG=VCK>KDMENGOJOMNNLNJMHKF7OLNMLMJJDJBKAMAOC@VDV:NDMBKAHAGBDDBGAHAKBMDNGNHMKKMHNGN:TCRGVGN9TLRHVHN:IFHFGGFHFIGIHHIGI:HGGHGHHGH9TIVIA6TJVJA@TBVBOCLEJHIII=TCVCNDK/TQVQOPLNJKIJI2TPVPNOK<ENE=VDA<VEA@VMVPUQTRRROQMPLMKEK4VOUPTQRQOPMOLMK@AQAQFPA2VKVGUDSBPAMAJBGDDGBKAOA2VLUISGPFMFJGGIDLBOA:KEKCJBIAGAEBCCBEAGAIBJCKEKGJIIJGK6THK/RJJ-KKH:GEHDHBGAEADBBDAEAGBHDHEGGDKCNCPDSFUIVMVPURSSPSNRKOGNENDOBQARATBUDUETGRHQHOG>PDRFTIUMUPTRRSP:PEODOBPARASBUDVEVGUHSHRGPDLCICGDDFBIAMAPBRDSGSIRLOPNRNSOUQVRVTUUSURTPROQOOP>GDEFCIBMBPCRESG3JNNOSKQGQ6QNQNN3QAD8EEEADBHBL?HBEEE?EOR?JBNAREQIQ<QBQBN?QOD:EKEODNHNL3HNEKE3EAR?OAPARBTDUFUHTISJQKL@RCTETGSHRIPJLJA.OTPTRSTQUOUMTLSKQJL-RRTPTNSMRLPKLKA@UBQCOEMHLLLOMQORQSU@UBRCPENHMLMONQPRRSU9MFLEKDIDFEDGBIAKAMBODPFPIOKNLLM9LFKEIEFFC3COFOINKLL<PED;OFE3ONE2POD@SCQEPHOLOOPQQSS@ACCEDHELEODQCSA.SDSBRAPANBLDKFKHLINIPHRSR@OBMCLEK8OHQGRES@DPDRESGSIRKPLNLLKKIKGLEAE.HRJQKOL6HLFMEOD:GEHDHBGAEADBBDAEAGBHDHEGGBLANAQBSDTGUKUOTQRRPRMQJNGMEMCNAPAQBRD<ICLBNBQCSDT6UNTPRQPQMPJNG@QDTFQFF>SEPEF;QITKQKG9SJPJG6QNTPQPA4SOPOA1QSTTRUOULTISGQENCIA/SSRTOTLSIRGPEMCIA@GEGDHCKCMDPFRISKSNRPPQMQKPHOGSG@FGFEHDKDMEPGRIS6SMROPPMPKOHMFSF>BQB>AQA@ODRGOGC>QFNFC:OJRMOMC8QLNLC4OPRSOSDUB2QRNRCTAWD0QAA0QNPHP2OLOHP0QPNPH2OOLPH9HAH:GDGAH9HHA:GGDHA@LCPHF>NHDKKPKSLTNTPSRQSPSNRMPMNNKOIPFPCNA1SORNPNNPJQGQDPBNA@MDPHN>OGMJPMN8OLMOPQN3OPMSP@GDJHH>IGGJJMH8ILGOJQH3IPGSJ?RFPHNIKIHHEFCBA?REQGPINJK7HIEGCEBBA/ROQMPKNJK7HKEMCOBRA/RNPLNKKKHLENCRA@JSJ@ISI-JSHQGOGMHLIIMHNFODOBNALAJBHDGFGHHIILMMNOOQOSNTLTJ7VCA7VQA7SPA<GNG@AGA4ASA=VDA<VEA@VMVPUQTRRRPQNPMML4VOUPTQRQPPNOMML<LMLPKQJRHREQCPBMAAA4LOKPJQHQEPCOBMA>VPA=VQA0VCA@VGV4VSV@AGA4ASA8VAA8VQA8SPA?BPB@AQA=VDA<VEA6PKH@VQVQPPV<LKL@AQAQGPA9VHA8VIA;QCPBOAMAJBHCGFFKFNGOHPJPMOONPKQFQ;QDPCOBMBJCHDGFF6FMGNHOJOMNOMPKQ<VLV<ALA=VDA<VEA@VPVPPOV@AHA=VDA<VEA0VQA/VRA@VHV3VUV<LQL@AHA3AUA=VDA<VEA@VHV@AHA-[SZTYUZU[T\R\P[NYMWLTKPIDH@G>2ZNXMTKHJDIAH?F=D<B<A=A>B?C>B==VDA<VEA/VEI7MRA8MQA@VHV3VTV@AHA3ATA7VCA7VQA7SPA@AGA4ASA=VDA<VKD=VKA/VKA/VRA.VSA@VEV/VVV@AGA2AVA=VDA<VQC<TQA0VQA@VEV3VTV@AGA9VEUCSBQAMAJBFCDEBHAJAMBODPFQJQMPQOSMUJVHV9VFUDSCQBMBJCFDDFBHA7ALBNDOFPJPMOQNSLUJV=VDA<VEA0VQA/VRA@VUV@AHA3AUA9VEUCSBQAMAJBFCDEBHAJAMBODPFQJQMPQOSMUJVHV9VFUDSCQBMBJCFDDFBHA7ALBNDOFPJPMOQNSLUJV;OFH5OLH;LLL;KLK=VDA<VEA@VMVPUQTRRROQMPLMKEK4VOUPTQRQOPMOLMK@AHA?VILAA@VHL@VPVQPOV?BOB@APAQGOA9VHA8VIA?VAPAVPVPPOV<ALA@QASBUCVEVFUGSHOHA@SCUEUGS1QPSOUNVLVKUJSIOIA1SNULUJS<ALA@VIA?VIC0VIA@VQV?UPU@DBAFADEBIALAPBSDUGVKVNUPSQPQLPINELAPAQD=ECHBLBPCSEUGV6VMUOSPPPLOHNE?BEB4BPB?VAQ0VPQ;MEH4MLH?DA?0DP??TPT?SPS;KLK;JLJ?BPB?APA7VJA6VKA@OBPDOEKFIGHIG?PCODKEIFHIGLGOHPIQKROSP5GNHOIPKQOSPTO:VNV:ANA3VAA2VBA?VAPAVOV@AOAOGNA@OEOKC=OKA-ZKA@ROD2RAD@OFOOC<NOA"bOA@VBTDRGQIQLRNTOV@VBSDQGPIPLQNSOV?VGP?VAUGP@MBOBPDQFQHPLMNLPLRMSO/LPKNKLLHOFPDPBO@GBIBJDKFKHJLGNFPFRGSI/FPENELFHIFJDJBI9OENCLBJAGADBBEAGAIBLENHPLQO9OFNDLCJBGBDCBEA9OJOLNMLODPBQA7OKNLLNDOBQARA5VIUGSEODLCHBBA:5VJUHSFOELDHCBB:5VNVPUQTQQPOONLMHM3VPTPQOONNLM9MLLNJOHOENCMBJAHAFBECDF9MKLMJNHNEMCLBJA?VDVFUGSLDMBNA=VEUFSKDLBNAPA0VPTNQDFBCAA6NIOGODNBKAHAEBCCBEAGAJBLEMHMKLMHRGTGVHWJWLVNT:OENCKBHBDCB:AIBKELHLLKNIQHSHUIVKVNT4LKNIOEOCNCLEJHI<ODNDLFJHI9ICHAFADBBEAHAJBLD9IDHBFBDCBEA;NDMBKAHAEBCCBEAHAKBNDPGQJQMOOMOKMIIGDD:@ECCEBHBKCNEPG0MONMNKLIIGCE:@SCUEVGVIUJTKQKMJIGA?TDUHUJT/VQSPQKJHEFA0VPSOQKJ@KBMDOGOHNHLGHEA;OGNGLFHDA:HILKNMOOOQNRMRJQEN:2OQMQJPEM:=OBHADABBAEAGCHE<OCHBDBBCA4JLMKNIOGODNBKAHAEBCCBEAGAJBLDMGNLNQMTLUJVGVEUDTDSESET:OENCKBHBDCB:AIBKDLGMLMQLTJV<OAA;OBA2OPNQNPONOLNHJFIDI;IHHJBKA;IGHIBJALANBPE?VDVFUGTHRNDOBPA=VFTGRMDNBPAQA8OAA8OBA:OA:9OB::LFFFCHAJALBNDPG/OODOBPASAUCVE.OPDPBQA=OBA<ODICDBA2ONKLG1OOLNJLGJEGCEBBA@OEO:ODNBKAHAEBCCBEAGAJBLEMHMKLMKNIOGO:OENCKBHBDCB:AIBKELHLLKN9NDA9NEA3NNA3NOA@LCNFOSO@LCMFNSN@KBMDOGOHNHLGGGDHBIA;OGNGLFGFDGBIAKAMBODQGRJSOSSRUPVNVLTLRMOOLQJTH4BOEPGQJRORSQUPV<FFCGBIAKANBPEQHQKPMONMOKOHNFKEHA:6AMBOEPHPLON6OINGKFHB:0OGODNBKAHAEBCCBEAGAJBLEMHMKLMKNIO:OENCKBHBDCB:AIBKELHLLKN6NQN7NGA7NHA@LCNFOQO@LCMFNQN@KBMDOGOHNHLFFFCHA;OGNGLEFECFBHAIALBNDPGQJQMPOONPMQJ1GQM@SBQNEOCOA?PND@SAQBONCOA;LBHAFADBBAA@FCB?HBFCDCBAA8INN5SLPMNONOPMQLS5SMPON?KDMGNFODNBKAHAEBBCAEAGBIEJH@EBCCBEBGCIE8HIEJBKAMAOBQERHRKQNPOONQMRK8EJCKBMBOCQE8[GZFYFXGWJVMV7VFUDTCRCPENHMKM7VGUETDRDPFNHM9MDLBKAIAGCEHCIBI@G?E?9MELCKBIBGDEHC2VI:1VH:@KBMDOGOHNHLGGGDIBLBNCQFSI;OGNGLFGFDGBIALANBPDRGSIUO8[GZFYFXGWJVOVOWLVHTERBOALAJBHEFHDIBI@H?F?E@7UFRCOBLBJCHEF5NJOGODNBLAIAFBCCBFAIAKB:OENCLBIBFCCDBFA?HJH5VF:4VE:9ODNBLAIAFBDDBGAJANBPDQGQJPLNNKOHO9OENCLBIBFCDEBGA7AMBODPGPJOLMNKO8VFUDRCPBMAHADBBDAFAIBKELGMJNONSMUKVIV8VGUERDPCMBHBDCBDA;AHBJEKGLJMOMSLUKV>LLL?CABBACBBC:VFUDI:UDI:VHUDI?CABBACBBC>VAO=VAO5VJO4VJO8ZB>2ZH>?OPO@IOI6ZC=1ZH=0RPQQPRQRRQTPUMVIVFUDSDQEOFNMJOH=QFOMKNJOHOENCMBJAFACBBCAEAFBGCFBE.VAA;VHTHRGPEOCOAQASBUDVFVHUKTNTQUSV2HMGLELCNAPARBSDSFQHOH+NUMVLWMWNVOUOSNQLLDJBHAEABBADAFBHCIEJJLLMNOOQOSNULVJUISIPJJKGMDOBQASATCTD<ACBBDBFCHDIJL8PJKKHMEOCQBSBTC>VAO=VAO4\IYFVDSBOAJAFBAC>D<8YFUDQCNBIBDC?D<7\KZLWMRMNLIJEHBE?A<7\KYLTLOKJJGHCE?;QFE@NKH6NAH7TJB@KSK>ABBCCDBDAC?A=@KSK?CABBACBBC&\A<7VGUESCPBMAIAFBCCBEAGAJBLDNGOJPNPQOTNULVJV7VHUFSDPCMBIBFCCEA:AIBKDMGNJONOQNTLV:RBA8VCA8VFSCQAP9SDQAP:RHQGPFQFRGTHUKVNVQURSRQQOOMLKHIEGCEAA3VPUQSQQPONMHI?CCDEDJBMBOCPE<DJAMAOBPE;RGQFPEQERFTGUJVMVPUQSQQPOMMJL4VOUPSPQOOMM9LJLMKNJOHOENCMBJAFACBBCAEAFBGCFBE7LLKMJNHNEMCLBJA2UIA1VJA1VAGQG9VCL9VRV9UMURV>LDMGNJNMMNLOJOGNDLBIAFACBBCAEAFBGCFBE7NLMMLNJNGMDKBIA2SNROQPRPSOUMVJVGUESCPBMAIAEBCCBEAHAKBMDNFNIMKLLJMGMELCJBH7VHUFSDPCMBIBDCB9AJBLDMFMJLL>VAP1VOSMPHJFGEEDA4PGJEGDECA?SEVGVLS>TEUGULSNSOTPV7VGUFTEREOFMHLKLOMPNQPQSPUMVJV7VHUGTFRFOGMHL6LNMONPPPSOUMV9LDKBIAGADBBEAIAMBNCOEOHNJMKKL9LEKCIBGBDCBEA8ALBMCNENIMK2ONMLKJJGJEKDLCNCQDSFUIVLVNUOTPRPNOJNGLDJBGADABBADAEBFCEBD<KDMDQESGUIV3UOSONNJMGKDIBGA<ODNEMFNEO?CABBACB;OENFMGNFO>ABBCCDBDAC?A=0TAKQB@NSN@HSH@TQKAB?RCQBPAQARBTCUFVJVMUNSNQMOLNFLDKDIEHGH7VLUMSMQLOKNIM>CBBCADBCC=OBNALAJBHDGFGHHIJILHNFODO=OALBHFGIJHNDO;OBNAJDGHHILFO,VSTQQNLLIIEFBDABAABADBECDBC,VTRRHQA,VRA0AQCPFOHMJKKIKHJHHIELBOASAUB2UNTMRKMIGHEFBDA3TMQKIJFIDGBDABAABADBECDBC8PHNGMEMDNDPERGTIULVRVTUUSUQTORNNMLM/VSUTSTQSORN3MQLRKSISFRCQBOAMALBLDMG3MPLQKRIRFQCOA?TARAPBNEMHMLNNOPQQSQUPVNVKUHRFODKCGCDDBGAIALBNDOFOHNJLJJIIG3VLUIRGOEKDGDDEBGA2UNTMRKMIGHEFBDA3TMQKIJFIDGBDABAABADBEDEFDHBJAMAOBQDSHTMTPSSQUOVJVGUESDQDOENGNHOIQ4SLRLPMOOOPQPSOUMVJVHUGTFRFPGNIM7VHTGRGOIM8MGMDLBJAHAEBCCBEAHAKBMDNFNHMJKJIIHG:MELCJBHBDCB1TORMMKGJEHBFA7PINGMEMDODQESGUJVTVQUPTOQMILFKDIBFADABBACADBECDBC5VPUQU9IIJKKOKQLSOQH?SAQAOBMDLGLJMLNOQPTPUOVNVLUJSIQHNHKIIKHMHOIQKRM2VMUKSJQINIJKH/MQIOEMCKBGADABBADAEBFCEBD0IOFMDJBGA:PFQFSGUJVMVJKHEGCFBDABAABADBECDBC4VJMIJGEFCDA<HFIHJQMSNVPXRYTYUXVWVUUSRRPPJOFOCQARATBVD*VUTSPQJPFPCQA2TMQKLIGHEFBDA0PONLMIMGNFPFRGTIUMVQVOTNRLLJFIDGBDABAABADBECDBC1VNTLQJLGCE?1ONMKLHLFMEOEQFSHULVPVNSMQJHHDGBE?D>B=A>A@BBDDFEIFMG:PFQFSHUKVMVJKHEGCFBDABAABADBECDBC4VJMIJGEFCDA,URQPONNKM)UWTXSYTYUXVWVUURPQOONKM6MNLOJPCQA6MMLNJOCQARATBVD;SEQEOFMHLKLNMPNSQTTTUSVRVPUOTMQIGHEFBDA2TMPKIJFIDGBDABAABADBEDEFDIBKANAPBRD0VMMJGHDFBDABAABADBECDBC0VOONKMFMBOA0VPROMNFNBOA'VVMQDOA'VXOWKVFVBXAYA[B]D'VYRXMWFWBXA3VMRKLIGHEFBDABAABADBECDBC3VNQOFPA3VOQPFPA%U[T\S]T]U\VZVXUVRUPSKQEPA8VGUESCPBNAJAFBCCBEAGAJBLDNGOIPMPQOTNUMUKTIRGNFIFF:UERCNBJBFCCEA2UNTMRKMIGHEFBDA3TMQKIJFIDGBDABAABADBECDBC8PHNGMEMDNDPERGTIULVPVSUTTURUOTMSLPKNKLL1VRUSTTRTOSMRLPK3RNPMNLMJLHLGNGPHSJUMVPVRUSSSORLPILEICGBDABAABADBEDEFDIBLAOAQBSD1VQURSROQLOILFHCDA2UNTMRKMIGHEFBDA3TMQKIJFIDGBDABAABADBECDBC8PHNGMEMDNDPERGTIULVQVTUUSUQTOSNPMLM0VSUTSTQSORNPM5MOLPJQCRA5MNLOJPCRASAUBWD:SFQFOGMILLLOMQNTQUTUUTVSVQUPTORNOLHKEIBGA2RNNMGLDJBGADABBADAEBFCEBD1TORMMKGJEHBFA7PINGMEMDODQESGUJVSVQUPTOQMILFKDIBFADABBACADBECDBC5VPUQU@RCUEVFVHTHQGNDFDCEA;VGTGQDICFCCEAGAIBLENHOJ.VOJNFNCPAQASBUD-VPJOFOCPA@RCUEVFVHTHQGMEFECFA;VGTGQEJDFDCFAGAJBMEOHQLROSSSURVQVPUOSOPPNRLTKVK>PBPAQASBUDVHVGTFPEGDA;PFGEA1VNTLPIGGCEA1VOTNPMGLA3PNGMA'VXUVSTPQGOCMA7QIPGPFQFSGUIVKVMUNSNPMLKGIDGBDABAABADBECDBC6VLUMSMPLLJGHDFBDA*UVTWSXTXUWVUVSUQSOPMLLGLDMBNAOAQBSD?RDUFVGVIUISGMGJHH:VHUHSFMFJHHJHMIOKQNRP-VRPOHMD,VSPQKOGMDKBHADABBADAEBFCEBD-TSRQMPJOHMEKCIBFA4PLNJMHMGOGQHSJUMVWVUUTTSQRMPGNDKBFABAABADBEDEFDIBKANAQBSD1VTUUU=VBTARAQBPCQBR7TISJRKSJT@KSK7DICJBKCJD>TBUCVDUDTCRAP8TIC@LQL@CQC8TIC@TQT@LQL0TCB@NSN@HSH7GIIGJEJCIBHAFADBBDAFAHBID<JCHBFBCDA6JIDIBKAMBNCPF5JJDJBKA@FCIEM9VBDBBDAEAGBIDJGJJKFLEMEOF8VCDCBDA9IGHHHHIGJEJCIBHAFADBBDAGAJCLF<JCHBFBCDA7GIIGJEJCIBHAFADBBDAFAHBID<JCHBFBCDA2VIDIBKAMBNCPF1VJDJBKA>CEDFEGGGIFJEJCIBHAFADBBDAGAJCLF<JCHBFBCDA9JKMMPNSNUMVKUJSA8A6B5D6E9FBGAIAKBLCNF7SINHJEAC<A87GIIGJEJCIBHAFADBBDAFAHBID<JCHBFBCDA6JE85JIAG<E8D6B5A6A8B;D=G?KANCPF@FCIEM9VAA8VBA=GFIHJIJKIKGJDJBKA8JJIJGIDIBKAMBNCPF<PDOENFOEP>JADABCAEBFCHF=JBDBBCA4RLQMPNQMR6LE:5LICG>E:D8B7A8A:B=D?GAKCNEPH@FCIEM9VAA8VBA7JJIKIJJIJGHDG=GGFHBIA=GFFGBIAJAMCOF@FCIEM9VBDBBDAFBGCIF8VCDCBDA@FCIEJGIGGEA<JFIFGDA:GIIKJLJNINGLA5JMIMGKA3GPIRJSJUIUGTDTBUA.JTITGSDSBUAWBXCZF@FCIEJGIGGEA<JFIFGDA:GIIKJLJNINGMDMBNA5JMIMGLDLBNAPBQCSF:JEJCIBHAFADBBDAFAHBICJEJGIIGJFIFGGEIDKDMENF<JCHBFBCDA<FGIIM7PA56PB59GJILJMJOIOGNDNBOA4JNINGMDMBOAQBRCTF7GIIGJEJCIBHAFADBBDAFAHB<JCHBFBCDA6JE8E6F5H6I9IAKANCPF5JIAG<E8@FCIEJGIGGEA<JFIFGDA:GIIKJLJKG6JKGLEMEOF@FCIDKDIGGHEHCGBEA=IFGGEGCEA@BCAHAKCMF@FCIEM9VBDBBDAFBGCIF8VCDCBDA>NIN>JADABCADAFBHDJG=JBDBBCA6JIDIBKAMBNCPF5JJDJBKA>JBHAEABCADAGBIDJGJJ=JCHBEBBCA7JKFLEMEOF=JBHAEABCADAFBHD<JCHBEBBCA7JHDHBJAKAMBODPGPJ6JIDIBJA1JQFRESEUF@FCIEJGJHIHGGDFBDACABBBCCCBB3IMHNHNIMJLJJIIGHDHBIALAOCQF9IIG7IHG:DHB9DFB>JADABCADAFBHDJG=JBDBBCA6JE85JIAG<E8D6B5A6A8B;D=G?KANCPF?HDKFLHLJKJHIFFDDC9LIKIHHFFD=CFBG@G=F:D8B7A8A:B=E@HBLEOH=CEBF@F=E:D80VAOQH@FQF@AQA@PSP@KSK@FSF@VQOAH@FQF@AQA/FPFNGLIIMHNFODOBNALAJBHDGFGHHIILMNOPPRP?VBHCH?VCVCH?DACABBACADBDCCDBD?CBBCBCCBC?VAUAO?UAO?VCUAO6VJUJO6UJO6VLUJO8ZB>2ZH>?OPO@IOI:ZG=H=:ZHZH=5SNSLUIVFVCUASAQBOCNKJLIMGMELCIBFBDCCD5SKTIUFUCTBSBQCOKKMINGNEMCLBIAFACBADCD4DJB.VAA;VHTHRGPEOCOAQASBUDVFVHUKTNTQUSV2HMGLELCNAPARBSDSFQHOH-OROPNOLMFLDKCIBEBCCBEBGCIDJIMKOLQLSKUIVHVFUESEQFNHKMEPBRATA-OTNRNPM0NPLNFMDKBIAEACBBCAEAGBIDKINJOKQKSJU6TIUHUFT:UFSFQGNIKNEPCRBTBTA?VAUAO?UAO?VCUAO9\FZDWBSANAJBEDAF>H<I<9\I\GZEWCSBNBJCEEAG>I<@\CZEWGSHNHJGEEAC>A<B<@\B\DZFWHSINIJHEFAD>B<;QEPGFFE;QFE;QGPEFFE@NBNJHKH@NKH@NAMKIKH6NJNBHAH6NAH6NKMAIAH8TICJC8TJTJC@LRLRK@LAKRK=BCABAABACBDCDDCD@C>A=?CBBCBCCBC>AD@=BC>@LRLRK@LAKRK?DACABBACADBDCCDBD?CBBCBCCBC.\A<B<.\T\B<:VDUBRAMAJBEDBGAIALBNEOJOMNRLUIVGV<UCRBMBJCEEB=CGBIBLC6BMENJNMMRKU5TIUGUDT@RCSFVFA@RAQCRETEAFA?QBRCTDUFVJVLUMTNRNPMNKKBA?QCQCRDTFUJULTMRMPLNJKAA?BOBOA@AOA>VNVGM>VCUMU4VFM:NINLMNKOHOGNDLBIAFACBBCAEBE;MIMLLNI7MMKNHNGMDJB3FLCIBFBCCBE<BBD6SKALA5VLA5VAFPF6SBF?GPGPF>VBM=UCN>VMVMU=UMU>NFOIOLNNLOIOGNDLBIAFACBBCAEBE?MCMENINLMNJ7NMLNINGMDJB3FLCIBFBCCBE<BBD6ULSMSLUIVGVDUBRAMAHBDDBGAHAKBMDNGNHMKKMHNGNDMBK5TIUGUDT<UCRBMBHCDFB?FDCGBHBKCMF8BLDMGMHLKIM4IKLHMGMDLBI;MCKBH@VOVEA@VAUNU3VDAEA;VCUBSBQCODNFMJLLKMJNHNEMCJBFBCCBEBHCJDKFLJMLNMONQNSMUJVFV=UCSCQDOFNJMLLNJOHOENCMBJAFACBBCAEAHBJDLFMJNLOMQMSLU4TJUFUCT?DEB6BND4LKJHIGIDJBLAOAPBSDUGVHVKUMSNONJMEKBHAFACBBDCDDB4OLLIJ4NKKHJGJDKBN;JCLBOBPCSFU?QDTGUHUKTMQ8ULSMOMJLEJB6CHBFBCC?OANAMBLCLDMDNCOBO?NBMCMCNBN?DACABBACADBDCCDBD?CBBCBCCBC?OANAMBLCLDMDNCOBO?NBMCMCNBN=BCABAABACBDCDDCD@C>A=?CBBCBCCBC>AD@=BC>0TAKQB@PRPRO@PAORO@HRHRG@HAGRG@TQKAB@QARBTCUFVIVLUMTNRNPMNLMJLGK@QBQBRCTFUIULTMRMPLNJMGL?SEU7UMS4OIL:LGHHHHL:DFCFBGAHAIBICHDGD:CGBHBHCGC1NOPMQJQHPGOFLFIGGIFLFNGOI7QHOGLGIHGIF1QOIOGQFSFUHVKVMUPTRRTPUMVJVGUETCRBPAMAJBGCEECGBJAMAPBRCSD0QPIPGQF8VAA8SBAAA8SPAQA8VQA=GNG>FOF@VAA?UBB@VIVLUMTNRNOMMLLIK?UIULTMRMOLMIL?LILLKMJNHNEMCLBIAAA?KIKLJMHMELCIBBB1QOSMUKVGVEUCSBQANAIBFCDEBGAKAMBODPF1QOQNSMTKUGUETCQBNBICFECGBKBMCNDOFPF@VAA?UBB@VHVKUMSNQONOINFMDKBHAAA?UHUKTLSMQNNNIMFLDKCHBBB@VAA?UBB@VMV?UMUMV?LHLHK?KHK?BMBMA@AMA@VAA?UBAAA@VMV?UMUMV?LHLHK?KHK1QOSMUKVGVEUCSBQANAIBFCDEBGAKAMBODPFPJKJ1QOQNSMTKUGUETDSCQBNBICFDDECGBKBMCNDOFOIKIKJ@VAA@VBVBAAA2VNVNAOA2VOA?LNL?KNK@VAABA@VBVBA7VJFICGBEBCCBFAF7VKVKFJCIBGAEACBBCAF@VAABA@VBVBA2VNVBJ2VBI<MNAOA;MOA@VAA@VBVBB?BMBMA@AMA@VAA?QBAAA?QIA@VID0VID1QIA1QPAQA0VQA@VAA?SBAAA?SOA@VND3VND3VOVOA:VEUCSBQANAIBFCDEBGAKAMBODPFQIQNPQOSMUKVGV9UETCQBNBICFECHBJBMCOFPIPNOQMTJUHU@VAA?UBAAA@VJVLUMTNRNOMMLLJKBK?UJULTMRMOLMJLBL:VEUCSBQANAIBFCDEBGAKAMBODPFQIQNPQOSMUKVGV9UETCQBNBICFECHBJBMCOFPIPNOQMTJUHU7DO?P?7DKDP?@VAA?UBAAA@VIVLUMTNRNOMMLLIKBK?UIULTMRMOLMILBL:KMANA9KNA2SMUJVFVCUASAQBOCNEMJKLJMINGNDMCJBFBDCCDAD2SMSLTJUFUCTBSBQCOENJLLKNIOGODMBJAFACBAD:UGA9UHAGA@VNVNU@VAUNU@VAGBDDBGAIALBNDOGOV@VBVBGCDDCGBIBLCMDNGNVOV@VIA@VBVID0VPVID0VIA@VGA@VBVGD5VGD5SGA5SQA5VQD*VVVQD*VQA@VNAOA@VBVOA2VNVAA2VBAAA@VHLHAIA@VBVIL1VOVHL1VILIA3VAA2VBA@VOV@VAUNU?BOBOA@AOA@\A<?\B<@\H\@<H<@Z]>:\G<9\H<@\H\@<H<@QIVQQ@QIUQQ@ASA;VAP;VGUAP4OMANA4ONONA4LKNIOFODNBLAIAGBDDBFAIAKBMD4LINFNDMCLBIBGCDDCFBIBMD@VAABA@VBVBA?LDNFOIOKNMLNINGMDKBIAFADBBD?LFNINKMLLMIMGLDKCIBFBBD4LKNIOFODNBLAIAGBDDBFAIAKBMD4LLKKMINFNDMCLBIBGCDDCFBIBKCLEMD4VMANA4VNVNA4LKNIOFODNBLAIAGBDDBFAIAKBMD4LINFNDMCLBIBGCDDCFBIBMD?HMHMKLMKNIOFODNBLAIAGBDDBFAIAKBMD?ILILKKMINFNDMCLBIBGCDDCFBIBKCLEMD8VGVEUDRDAEA8VIUGUET;UEREA@OHOHN@OANHN3OMOM@L=K<I;G;E<D=B=3ON@M=K;I:F:D;B=4LKNIOFODNBLAIAGBDDBFAIAKBMD4LINFNDMCLBIBGCDDCFBIBMD@VAABA@VBVBA?KENGOJOLNMKMA?KEMGNINKMLKLAMA?VAUATBSCSDTDUCVBV?UBTCTCUBU?OBACA?OCOCA?]A\A[BZCZD[D\C]B]?\B[C[C\B\?VBACA?VCVCA@VAABA@VBVBA4OLOBE4OBD<HKAMA;IMA@VAABA@VBVBA@OAABA@OBOBA?KENGOJOLNMKMA?KEMGNINKMLKLAMA4KPNROUOWNXKXA4KPMRNTNVMWKWAXA@OAABA@OBOBA?KENGOJOLNMKMA?KEMGNINKMLKLAMA;ODNBLAIAGBDDBFAIAKBMDNGNIMLKNIOFO;NDMCLBIBGCDDCFBIBKCLDMGMILLKMINFN@OA:B:@OBOB:?LDNFOIOKNMLNINGMDKBIAFADBBD?LFNINKMLLMIMGLDKCIBFBBD4OM:N:4ONON:4LKNIOFODNBLAIAGBDDBFAIAKBMD4LINFNDMCLBIBGCDDCFBIBMD@OAABA@OBOBA?ICLENGOJO?ICKEMGNJNJO5LKNHOEOBNALBJDIIGKF7GKEKDJB6CHBEBBC>BBDAD5LKLJN6MHNENBM>NBLCJ?KDJIHKGLELDKBHAEABBAD=VDAEA=VEVEA@OHOHN@OANHN@OAEBBDAGAIBLE@OBOBECCEBGBICLE5OLAMA5OMOMA@OGA@OBOGC4OLOGC4OGA@OFA@OBOFD7OFD7LFA7LNA7OND.OROND.ONA@OLAMA@OBOMA4OLOAA4OBAAA@OGA@OBOGC4OLOGCC:4OGAD:C:6NAA4OCB@OMO@OANKN>BMBMA@AMA;\D[CZBXBVCTDSEQEOCM=[CYCWDUETFRFPENALEJFHFFEDDCCAC?D=>KEIEGDECDBBB@C>D=F<@\A<@\C[DZEXEVDTCSBQBODM>[DYDWCUBTARAPBNFLBJAHAFBDCCDAD?C==KBIBGCEDDEBE@D>C=A<@HAJBMDNFNHMLJNIPIRJSL@JBLDMFMHLLINHPHRISLSN?VBHCH?VCVCH?DACABBACADBDCCDBD?CBBCBCCBC?AABBCCBBA6BLCMBLAKB,BVCWBVCWB?:NV2LOKNJLKMLLNJOGOENCLBIBGCDEBGAIALBND=BBDAGAIBLDN>SFUIVLVOURSTPUMUJTGRDOBLAIAFBCDAJAMBPCS2RONNQLRIRGQFPENEJFEGFIELENFOH8EGGFJFMGPIR>SFUIVLVOURSTPUMUJTGRDOBLAIAFBCDAJAMBPCS;RGRHRHQHFIEHEGEFEGFGR9RLROQPOPNOLLKHK3QOOONNLLKNJOFOEPEQF4JNF-USTTSUTUUTVSVRVPUOTMQKKIGHEFBDABAABADBEDEFDIBKANAPBRD2BIFKKMPOTPU3LHH>XBXBYCYCZE[H[JZKXJVHUFUJTKRKQJOHNENCOCPEPBQCQ8ZJXIV8TJRJQIO5LAL9JJIKGJEHDJCKAK@J>H=E=C>B@BACCEDCEBGCIEJHJ8IJGIE8CJAJ@I>=>C@CADC=ECGDI>NFNGNJN;NFZ=XFZG[GN4LAL<=G=H=J=5AAAHJH=:HG=?WBYB[?YD[F[IYJY6[JYHUFRDNENHU=ZFZIYJY5LAL9JJIKGJEHDJCKAK@J>H=E=C>B@BACCEDCEBGCIEJHJ8IJGIE8CJAJ@I>=>C@CADC=ECGDI6[C[CZBUCVEWHWJVKTKQJOHNENCOBPBQCQCP6[GZCZ8VJTJQIO5LAL9JJIKGJEHDJCKAK@J>H=E=C>B@BACCEDCEBGCIEJHJ8IJGIE8CJAJ@I>=>C@CADC=ECGDI>XBXBYCYCZE[H[JZKXJVHUFUJTKRKQJOHNENCOCPBPBQCQ8ZJXIV8TJRJQIO5LAL9JJIKGJEHDJCKAK@J>H=E=C>B@BACCEDCEBGCIEJHJ8IJGIE8CJAJ@I>=>C@CADC=ECGDI>XBXBYCYCZE[H[JZKXJVHUETCSBQBOBN?ODPGNJNJOKPKQ7OGODPBQ8ZJXIV5LAL>GBGBHCHCIEJHJJIKGJEHDFD7CKAK@J>H=E=C>C?B?B@C@8EJGII8CJAJ@I>>NFNGNJN;NFZ=XFZG[GN4LAL9JJIKGJEHDJCKAK@J>H=E=C>B@BACCEDCEBGCIEJHJ8IJGIE8CJAJ@I>=>C@CADC=ECGDI>NFNGNJN;NFZ=XFZG[GN4LAL>GBGBHCHCIEJHJJIKGJEHDFD7CKAK@J>H=E=C>C?B?B@C@8EJGII8CJAJ@I>>NFNGNJN;NFZ=XFZG[GN4LAL>GBGBICIEJHJIHKGJEHDGCCBB@B>B=>?D?G=J=J>K?K@7>G>8EJGII@LAJCJCLAL@LCJ>LAJ@VETHRJPKMKKJIIH@UGR@TDSHQJOKM6JJHHFDDAC:EAB8OJNKLKJJGHEECAA;PCOBNALAJBHCGFFJFMGNHOJOLNNMOJPFP>OBMBJCHDGFF4GNINLMNLOJP8PEOBMAKAIBGDFGFKGNIOKOMNOLPIP3OIP5PGOBM<OAK?GGF=FIGNI6GOK:PDOBMAKAIBGDFFFIGKILKLMKOIPGP>MIP?KJO@IKN?HLM>GKK=FJI>WC@8XIA@PKR@OKQ@GKI@FKH@XAF8RI@@PIR@OIQ@GII@FIH@VAA@JDLGLIKJIJGIEFCDBAA@JDKGKIJ9KIIIGHEFC@MAJ,MUJ@MUM@LUL@KUK@JUJ@MAJ6MKJ@MKM@LKL@KKK@JKJ=[IQEJEI9RDK:UGSCLEIHE7BHEFFDFBEACAAB?E=7BHDFEBEBAC?E=;FCDAA=NCPCRARAPBODNGNIOKQ?RBO@QCQ@PGN=NIO6QGD=7E7F8F9E:D:C9C7D5F4H4K5M7N9O=OHNbNiOnPpRqSqUpVnVjUgTeRbM^GZEXCUBSAOAKBGDDGBKAOASBUCWFXIXMWPVRTTQUMUJTHRGOGKHHJF=9D8E8E9D9/bN^IZFWDTCRBOBKCGDEGB2ARBTCVFWIWMVPURSTQU?TCVEWGWIVJTJRIPGOEOCPBQATAWBZD\G]K]O\RZTWUSUNTJSHQENBJ?E<A:6]N\QZSWTSTNSJRHPEMBH>E<=VHV>UIU?TJT?SJS?RJR>QIQ=PHP(YYW[W[YYY'YZW(X[X(OYM[M[OYO'OZM(N[N@`A8?`B8;`F87\L\LZJZJ]K_M`P`R_T]UZUUTRRPPONOLPKRJPHMGLHKJHKFLHNIPIRHTFUCU>T;R9P8M8K9J;J>L>L<J<6\KZ7[L[/_S]TZTUSRRP6RKPIMGLIKKHKF/HSFTCT>S;R96>K<7=L=8VIA7VJA?VAPAVMV7LQLTKUJVHVEUCTBQAFA0LSKTJUHUETCSBQA7VCA7VQA7SPA<GNG@AGA4ASA=VDA<VEA@VQVQPPV<LMLPKQJRHREQCPBMAAA4LOKPJQHQEPCOBMA=VDKEIHHKHNIPK<VEKFIHH1VPA0VQA@VHV4VTV4ATA9VHPGHFDEBDA/VRA.VSA<VVV@AVA@AA:?AA:,AV:+AV:=VDA<VEA6PKH@VQVQPPV<LKL@AQAQGPA7VJA6VKA:VNV9SDRBPAMAJBGDEHDMDQESGTJTMSPQRMSHS9SERCPBMBJCGEEHD4DPERGSJSMRPPRMS:ANA=VDA<VEA@VPVPPOV@AHA=VDA<VEA@VHV@AHA/VOUMSLQKMKJLFMDOBRATAWBYDZF[J[MZQYSWUTVRV/VPUNSMQLMLJMFNDPBRA-AVBXDYFZJZMYQXSVUTV<LKL=VDA<VEA0VQA/VRA@VHV3VUV0TEC@AHA3AUA3VNA2VOA6VRV>UDTCSBTBUCVDVEUFSGOHMJLSLUMVOWSXUYVZV[U[TZSYTZU7LHKGIFDEBDA7LIKHIGDFBEACABBAD.LUKVIWDXBYA.LTKUIVDWBXAZA[B\D6ARA=VDA<VEA@VHV<LLLNMOOPSQURVSVTUTTSSRTSU5LNKOIPDQBRA5LMKNIODPBQASATBUD@AHA:VGPFHEDDBCABAABACBDCCBB/VRA.VSA=VVV2AVA=VDA<VKD=VKA/VKA/VRA.VSA@VEV/VVV@AGA2AVA=VDA<VEA0VQA/VRA@VHV3VUV<LQL@AHA3AUA9VEUCSBQAMAJBFCDEBHAJAMBODPFQJQMPQOSMUJVHV9VFUDSCQBMBJCFDDFBHA7ALBNDOFPJPMOQNSLUJV=VDA<VEA0VQA/VRA@VUV@AHA3AUA=VDA<VEA0VQA/VRA@VHV3VUV@AUA-AU:,AU:=VDA<VEA@VMVPUQTRRROQMPLMKEK4VOUPTQRQOPMOLMK@AHA2SPPPVOSMUJVHVEUCSBQANAIBFCDEBHAJAMBODPF9VFUDSCQBNBICFDDFBHA9VHA8VIA?VAPAVPVPPOV<ALA>VJF=VKF/VKFICHBFAEADBDCEDFCEB@VGV3VTV=VDA<VEA@VMVPUQTRRRPQNPMML4VOUPTQRQPPNOMML<LMLPKQJRHREQCPBMAAA4LOKPJQHQEPCOBMA=VDA<VEA2VOA1VPA'VZA&V[A@VHV5VSV*V^V@A^A>VPA=VQA0VCA@VGV4VSV@AGA4ASA2VOA1VPA.VGVDUCTBRBPCNDMGLOL:VEUDTCRCPDNEMGL7LHKGJDCCBBBAC9KGIEBDABAACAD5ASA?SAVAPBSDUFVJVMUNSNPMNJMGM7VLUMSMPLNJM7MLLNJOHOENCMBJAEACBBCAEAFBGCFBE4KNHNEMCLBJA=VDA<VEA@VHV<LLLOKPJQHQEPCOBLAAA5LNKOJPHPEOCNBLA*VWA)VXA-V[V-A[A=VDA<VEA@VHV<LLLOKPJQHQEPCOBLAAA5LNKOJPHPEOCNBLA?SAVAPBSDUGVIVLUNSOQPNPIOFNDLBIAFACBBCAEAFBGCFBE8VKUMSNQONOINFMDKBIA;LOL@VBTDRGQIQLRNTOV@VBSDQGPIPLQNSOV?VGP?VAUGP:OGA9OHA?OAJAOKO9HLHOGPEPDOBLADA5HNGOEODNBLA>MCLBLBMCNEOIOKNLMMKMDNBOA5MLDMBOAPA5KKJEIBHAFADBBEAHAJBLD<ICHBFBDCBEA3VMUGSDQBNAKAGBDDBGAIALBNDOGOINLLNIOGODNBLAI3VMTKSGRDPBN:OENCLBIBGCDEBGA8AKBMDNGNIMLKNIO=ODHEFHEJEMFOH<OEHFFHE2OOA1OPA@OHO5OSO5ASA:OGKFEEBDA1OPA0OQA=OTO?AA<AATAT<SA?ININKMMLNJOGODNBLAIAGBDDBGAIALBND4IMLLN:OENCLBIBGCDEBGA9VH:8VI:<VIV9LGNFODOBNAKAEBBDAFAGBHD=OCNBKBECBDA4ONNOKOENBMA8LJNKOMOONPKPEOBMAKAJBID<:L:=ODA<OEA@OOOOJNO@AHA=ODA<OEA@OHO@AHA0ONNLLKIKGLDNBQASAVBXDYGYIXLVNSOQO0OONMLLILGMDOBQA.AUBWDXGXIWLUNSO<HKH=ODA<OEA2OOA1OPA@OHO5OSO@AHA5ASA2NEB5OLA4OMA8OPO=NCMBNCODOENGJHIJHOHQIRJTNUOVOWNVMUN7HHGGFEBDA7HHFFBEACABBAD2HQGRFTBUA2HQFSBTAVAWBXD8APA=ODA<OEA@OHO<HGHJIKJMNNOOOPNOMNN:HJGKFMBNA:HIGJFLBMAOAPBQD@AHA;OFKEEDBCABAABBCCB2OOA1OPA>OSO5ASA=ODA=OJA<OJC1OJA1OPA0OQA@OEO1OTO@AGA4ATA=ODA<OEA2OOA1OPA@OHO5OSO<HOH@AHA5ASA:ODNBLAIAGBDDBGAIALBNDOGOINLLNIOGO:OENCLBIBGCDEBGA8AKBMDNGNIMLKNIO=ODA<OEA2OOA1OPA@OSO@AHA5ASA=ODA<OEA2OOA1OPA@OHO5OSO@ASAS<RA=VDA<VEA<SGUIVKVNUPSQPQNPKNIKHIHGIEK6VMUOSPPPNOKMIKH@VEV@AHA4LLKMJNKNLLNJOGODNBLAIAGBDDBGAIALBND:OENCLBIBGCDEBGA:OGA9OHA?OAJAONONJMO=AKA>OIA=OIC2OIAG=E;C:B:A;B<C;@OGO6OQO=ODA<OEA@OLOONPLPKOILH5ONNOLOKNILH<HLHOGPEPDOBLAAA5HNGOEODNBLA=ODA<OEA3ONA2OOA)OXA(OYA@OHO6ORO,O\O@A\A>ONA=OOA2OCA@OGO6OQO@AGA6AQA4OMA3ONA0OFOCNBLBKCIFHMH;ODNCLCKDIFH6HHGGFEBDA6HIGHFFBEACABBAD7AQA?MAOAKBMCNEOIOLNMLMKLIIH8OKNLLLKKIIH;HIHLGMEMDLBIAEABBADAEBFCEBD8HKGLELDKBIA=ODA<OEA@OHO<HIHLGMEMDLBIAAA8HKGLELDKBIA.OSA-OTA1OWO1AWA=ODA<OEA@OHO<HIHLGMEMDLBIAAA8HKGLELDKBIA?MAOAKBMCNEOHOKNMLNINGMDKBHAEACBADAEBFCEBD9OJNLLMIMGLDJBHA:HMH?CABBACBBC?VATBHCTBV?TBN?CABBACBBC@GBICJEJFIFGEDEBFA=JEIEGDDDBFAHAJBKC4JKCKBLANAOBPD3JLCLBMA@GBICJEJFIFGEDEBFA=JEIEGDDDBFAGAIBKDLGLJKJLI@GBICJEJFIFGEDEBFA=JEIEGDDDBFAGAIBJC5JJCJBLA4JKCKBLAMAOBQDRGRJQJRI?GCIEJGJHIHG;JGIGGFDEBCABAABACBCAB4ILHMHMILJKJIIHGGDGBHA;DFBGAIAKBLD@GBICJEJFIFGEDEBFA=JEIEGDDDBFAHAJBKC4JKCJ@I>3JLCK@I>G=D=C>D>E=6JKIJHBCABAA?HCJFJIH>IFIIHJH?CCCFBIB>CFAIAJC=NBMAJAEBBDAGAIBJEJJIMGNDN=NCMBJBECBDA:AHBIEIJHMGN?KENEA=MDA@AHA?LBKAKALBMDNGNIMJKIIGHDGBFADAA:NHMIKHIGH@BBCCCFBIBJC>CFAIAJCJD?LBKAKALBMDNGNIMJKIIGH:NHMIKHIGH<HGHIGJEJDIBGADABBACADBDBC:HHGIEIDHBGA:LGA9NHA9NAELE<AJA?NAH?NIN?MFMIN@HBIDJGJIIJGJDIBGADABBACADBDBC:JHIIGIDHBGA8LIKJKJLIMGNENCMBLAIADBBDAGAIBJDJFIHGIDIAG<NCLBIBDCBDA:AHBIDIFHHGI@NAJ8LEECA7NGHDA@LCNENHL@LCMEMHLIL=JBIAGADBBDAFBGDGGFIDJ@HCJCA@ICJEJGIGGFEAAGA@ICJEJGIGGEF=FEFGEGBEACAAB;JFA;JADID?JAFCGDGFFGDFBDACAAB?JFJ;JDJBIAGADBBDAFBGDFFDGBFAD:JCA@JGJ>JAIAGCFEFGGGIEJCJ>FAEABCAEAGBGEEF:GFEDDBEAGBIDJFIGGGDFBDABA=NBMAKBIDHGHIIJKIMGNDN=NCMBKCIDH:HHIIKHMGN=HBGAEADBBDAGAIBJDJEIGGH=HCGBEBDCBDA:AHBIDIEHGGH?CBDADACBBDAFAHBICJFJKIMGNDNBMAKAIBGDFGFJH;AHCIFIKHMGN=NCMBKBICGDF;NFMGMGNFN@GBICJEJFIFGEDEBFA=JEIEGDDDBEAGAHBID9NHMIMINHN>GDIEJGJHIHGF@E>C=A=A>B=;JGIGGE@D>C=@GBICJEJFIFHDA=JEIEHCA;HGIIJKJMIMHKA6JLILHJA4HNIPJRJTITGSDSBTA/JSISGRDRBSAUAVBWD@GBICJEJFIFHDA=JEIEHCA;HGIIJKJMIMGLDLBMA6JLILGKDKBLANAOBPD=OBNALAJBHDGFGHHIJILHNFODO1VCA1VQA2TPA:GPG@AGA4ASA7VDA6VEA:VRVUUVSVQUNTMQL/VTUUSUQTNSMQL9LQLSKTITGSDQBMAAA0LRKSISGRDPBMA1TQTRVQPQRPTOUMVJVGUESCPBMAIAFBCCBFAIAKBMDNF7VHUFSDPCMBIBFCCDBFA7VDA6VEA:VPVSUTTUQUMTIREPCNBJAAA1VRUSTTQTMSIQEOCMBJA7VDA6VEA2PMH:VVVUPUV9LNL@APARFOA7VDA6VEA2PMH:VVVUPUV9LNL@AHA1TQTRVQPQRPTOUMVJVGUESCPBMAIAFBCCBFAHAKBMDOH7VHUFSDPCMBIBFCCDBFA9AJBLDNH6HRH7VDA6VEA*VQA)VRA:VNV-V[V9LTL@AHA3AUA7VDA6VEA:VNV@AHA2VJEICHBFADABBADAFBGCFBE3VIEHCFA6VRV7VDA6VEA)VGI3MRA4MQA:VNV-VZV@AHA3ATA7VDA6VEA:VNV@APARGOA7VDA7VKA6VLC)VKA)VRA(VSA:VKV)V\V@AGA2AVA7VDA7VQD7SQA*VQA:VJV-VZV@AGA7VGUESCPBMAIAFBCCBEAHAKBMDOGPJQNQQPTOUMVJV7VHUFSDPCMBIBFCCEA9AJBLDNGOJPNPQOTMV7VDA6VEA:VSVVUWSWQVNTLPKHK.VUUVSVQUNSLPK@AHA7VGUESCPBMAIAFBCCBEAHAKBMDOGPJQNQQPTOUMVJV7VHUFSDPCMBIBFCCEA9AJBLDNGOJPNPQOTMV>CCDDFFGGGIFJDJ=K<M<N>N?7DK>L=M=N>7VDA6VEA:VRVUUVSVQUNTMQLHL/VTUUSUQTNSMQL4LOKPJQBRATAUCUD1JRCSBTBUC@AHA/TSTTVSPSRRTQUNVJVGUESEQFOGNNJPH<QGONKOJPHPEOCNBKAGADBCCBEBGAABCCC7VDA6VEA=VAPCVRVQPQV@AHA<VBKAGADBBEAIALBNDOGSV;VCKBGBDCBEA?VIV1VVV>VDA=VEC0VDA@VGV4VSV=VBA<VCC5VBA5VJA4VKC-VJA@VHV0VWV8VPA7VQA*VCA:VMV.VYV@AGA4ASA>VGLDA=VHLEA/VHL@VGV3VTV@AHA-VAA,VBA9VEPGVUV@AOAQGNA>VBUASAQBPCQBR7TISJRKSJT@KSK7DICJBKCJD?TAUBVCUCSBQAP8TIC@LQL@CQC8TIC@TQT@LQL0TCB@NSN@HSH3OLHKDKBLAOAQCRE2OMHLDLBMA5HLKKNIOGODNBKAHAEBCCBEAGAIBKELH:OENCKBHBDCB<VAIAFBCCB;VBI?ICLENGOIOKNLMMKMHLEJBGAEACBBEBI6NLLLHKEIBGA?VFV5LLKMKMLLNJOGODNBKAHAEBCCBEAGAJBLE:OENCKBHBDCB1VLHKDKBLAOAQCRE0VMHLDLBMA5HLKKNIOGODNBKAHAEBCCBEAGAIBKELH:OENCKBHBDCB4VQV?FFGIHLJMLLNJOGODNBKAHAEBCCBEAGAJBLD:OENCKBHBDCB/UQTRSSTSURVPVNUMTLRKOHAG=F;1VNTMRLNJEIAH>G<F;D:B:A;A<B=C<B;:OQO0OMAL>J;G:D:B;A<A=B>C=B<1OLAK>I;G:3HNKMNKOIOFNDKCHCEDCEBGAIAKBMENH8OGNEKDHDDEB:VAA9VBA=HFLHNJOLONNOMOKMEMBNA5ONMNKLELBMAPARCSE=VHV8VHUITJUIV@KBMDOGOHNHKFEFBGA;OGNGKEEEBFAIAKCLE4VLUMTNUMV<KFMHOKOLNLKIAH>G<F;D:B:A;A<B=C<B;7OKNKKHAG>F<D::VAA9VBA2NNMOLPMPNOONOLNHJFIDI;IHHJBKA;IGHIBJALANBPE=VHV;VBHADABBAEAGCHE:VCHBDBBCA>VGV@KBMDOGOHNHLGHEA;OGNGLFHDA:HILKNMOOOQNRMRKOA2OQMQKNA0HSLUNWOYO[N\M\KZEZB[A(O[M[KYEYBZA]A_C`E@KBMDOGOHNHLGHEA;OGNGLFHDA:HILKNMOOOQNRMRKPEPBQA2OQMQKOEOBPASAUCVE:ODNBKAHAEBCCBEAGAJBLEMHMKLMKNIOGO:OENCKBHBDCB:AIBKELHLLKN>KDMFOIOJNJLIHE:9OINILHHD:8HJKLNNOPORNSMTKTHSEQBNALAJBIEIH/NSLSHREPBNA@:H:3OH:2OI:5HLKKNIOGODNBKAHAEBCCBEAGAIBKELH:OENCKBHBDCB<:L:@KBMDOGOHNHLGHEA;OGNGLFHDA:HILKNMOOOPNPMOLNMON4MMLNLNMMNJOGODNCMCKDJKFLE>LDKKGLFLCKBHAEABBACADBDBC:VCHBDBBCAFAHCIE9VDHCDCBDA@OJO@KBMDOGOHNHKFEFCHA;OGNGKEEECFBHAJALBNDPH/OPHODOBPASAUCVE.OQHPDPBQA@KBMDOGOHNHKFEFCHA;OGNGKEEECFBHAIALBNDPGQKQOPOQM@KBMDOGOHNHKFEFCHA;OGNGKEEECFBHAJALBNDOF0OOFOCPBRATAVBXDYFZJZOYOZM/OPFPCRA?KDNFOIOJMJJ9OIMIJHFGDEBCABAABACBDCCBB9FHCIALANBPE1NOMPLQMQNPOOOMNKLJJIFICJA@KBMDOGOHNHKFEFCHA;OGNGKEEECFBHAJALBNDPH.OOAN>L;I:F:D;C<C=D>E=D</ONAM>K;I:2ONMLKDEBCAA?KCMEOHOLM>MENHNLMNM?CDCHBKBMC=CHAKAMCNE0VAOQH@FQF@AQA@PSP@KSK@FSF@VQOAH@FQF@AQA/FPFNGLIIMHNFODOBNALAJBHDGFGHHIILMNOPPRP?VAUASBK?VBHCH?VCVCH>VDUDSCK?DACABBACADBDCCDBD?CBBCBCCBC?VAUAO?UAO?VCUAO6VJUJO6UJO6VLUJO8ZB>2ZH>?OPO@IOI;ZF=7ZJ=3QNRMRMPOPORNTMUJVFVCUASAPBNELKJMINGNDMB?PCNEMKKMJNH>UBSBQCOENKLNJOHOENCMBJAFACBBCAEAGCGCEBEBF.VAA;VHTHRGPEOCOAQASBUDVFVHUKTNTQUSV2HMGLELCNAPARBSDSFQHOH.MSNRNRLTLTNSOROQNPLNGLDJBHADABBADAGBIHMJOKQKSJUHVFUESEPFMHJLEOBQASATCTD>BBDBGCIDJ7OKS6QJU;UEQ;NHKLFOCQB;ADBCDCGDIHM<SFOIKMFPCRBSBTC?VAUAO?UAO?VCUAO9\FZDWBSANAJBEDAF>H<=VCSBOBICEDB;ZEXDUCOCIDCE@F>@\CZEWGSHNHJGEEAC>A<<VFSGOGIFEEB>ZDXEUFOFIECD@C>;QEPGFFE;QFE;QGPEFFE@NBNJHKH@NKH@NAMKIKH6NJNBHAH6NAH6NKMAIAH8TICJC8TJTJC@LRLRK@LAKRK=BCABAABACBDCDDCD@C>A=?CBBCBCCBC>AD@=BC>@LRLRK@LAKRK?DACABBACADBDCCDBD?CBBCBCCBC.\A<B<.\T\B<:VDUBRAMAJBEDBGAIALBNEOJOMNRLUIVGV=TCRBNBICEDC5CMENINNMRLT:VEUDSCNCIDDEBGA8AKBLDMIMNLSKUIV<TEA;TFB:VGA:VDSBR@AKA<BCA<CDA:CHA:BIA?RBQCQCRBR?SCSDRDQCPBPAQARBTCUFVJVMUNTOROPNNKLFJDIBGADAA4TNRNPMN7VLUMRMPLNJLFJ@CBDDDICMCOD=DIBMBNC=DIAMANBODOF?RBQCQCRBR?SCSDRDQCPBPAQARBTCUFVJVMUNSNPMNJM5UMSMPLN8VKULSLPKNIM:MJMLLNJOHOENCMBJAFACBBCAEAFBGCGDFDECDBD4JNHNEMC8MKLLKMHMELBJA?FBECECFBF7SJA6TKB5VLA5VAGQG:AOA7BHA7CIA5CMA5BNA>VALCNFOIOLNNLOIOGNDLBIAFACBBCAEAFBGCGDFDECDBD4LNJNFMD8OKNLMMJMFLCKBIA?FBECECFBF>VMV>UKU>TGTKUMV5SLRMRMSLS4TLTKSKRLQMQNRNSMUKVHVEUCSBQAMAGBDDBGAIALBNDOGOHNKLMINGNEMDLCJ=SCQBMBGCDDC4DNFNIMK9VFUETDRCNCGDDEBGA8AKBLCMFMILLKMIN@VAP2VOSNPJKIIHEHA8JHHGEGA3PIKGHFEFAHA@RBTDVFVKSMSNTOV>TDUFUHT@RBSDTFTKS;VCUBSBPCNFMJMMNNPNSMUJVFV=UCSCPDN5NMPMSLU;VEUDSDPENFM7MKNLPLSKUJV;MCLBKAIAEBCCBFAJAMBNCOEOINKMLJM>KBIBECC4CNENIMK;MDLCICEDBFA7ALBMEMILLJM>ECDDDDECE4MLKKJIIGIDJBLAOAPBSDUGVIVLUNSOPOJNFMDKBHAEACBBDBECFDFEEEDDCCC>LBNBQCS5TMSNPNJMFLD:IEJDKCNCQDTEUGV8VKULSMPMILEKCJBHA?OANAMBLCLDMDNCOBO?NBMCMCNBN?DACABBACADBDCCDBD?CBBCBCCBC?OANAMBLCLDMDNCOBO?NBMCMCNBN=BCABAABACBDCDDCD@C>A=?CBBCBCCBC>AD@=BC>0TAKQB@PRPRO@PAORO@HRHRG@HAGRG@TQKAB?QBRCRCPAPARBTCUEVIVLUMTNRNPMNLMHK5TMSMOLN8VKULSLOKMJL:KGHHHHKGK:DFCFBGAHAIBICHDGD:CGBHBHCGC1NOPMQJQHPGOFLFIGGIFLFNGOI7QHOGLGIHGIF1QOIOGQFSFUHVKVMUPTRRTPUMVJVGUETCRBPAMAJBGCEECGBJAMAPBRCSD0QPIPGQF7VCB8SOA7SPA7VQA<GNG@AGA5ASA>BBA>BEA2BMA2CNA1CRA=VDA<UEB;VFA@VMVPUQTRRRPQNPMML1TQRQPPN4VOUPSPOOMML;LMLPKQJRHREQCPBMAAA1JQHQEPC4LOKPIPDOBMA?VDU>VDT:VFT9VFU=BBA=CCA;CGA;BHA2SPVPPOSMUKVHVEUCSBQANAIBFCDEBHAKAMBODPF=SCQBNBICFDD9VFUDRCNCIDEFBHA=VDA<UEB;VFA@VKVNUPSQQRNRIQFPDNBKAAA2SPQQNQIPFOD6VMUORPNPIOEMBKA?VDU>VDT:VFT9VFU=BBA=CCA;CGA;BHA=VDA<UEB;VFA@VQVQP;LLL5PLH@AQAQG?VDU>VDT:VFT9VFU5VQU3VQT2VQS1VQP5PKLLH5NJLLJ5MHLLK=BBA=CCA;CGA;BHA5AQB3AQC2AQD1AQG=VDA<UEB;VFA@VQVQP;LLL5PLH@AIA?VDU>VDT:VFT9VFU5VQU3VQT2VQS1VQP5PKLLH5NJLLJ5MHLLK=BBA=CCA;CGA;BHA2SPVPPOSMUKVHVEUCSBQANAIBFCDEBHAKAMBOBPAPI=SCQBNBICFDD9VFUDRCNCIDEFBHA2HOC3INCMB6ISI5INH4ING0IPG/IPH=VDA<UEB;VFA1VPA0UQB/VRA@VIV4VUV;LPL@AIA4AUA?VDU>VDT:VFT9VFU3VPU2VPT.VRT-VRU=BBA=CCA;CGA;BHA1BNA1COA/CSA/BTA=VDA<UEB;VFA@VIV@AIA?VDU>VDT:VFT9VFU=BBA=CCA;CGA;BHA9VHEGBFA8UIEHB7VJEIBFADABBADAFBGCGDFDECDBD?FBECECFBF<VMV;VHU:VHT6VJT5VJU=VDA<UEB;VFA0UFJ8LPA7LQA7NRA@VIV3VTV@AIA4ATA?VDU>VDT:VFT9VFU1VQU.VQU=BBA=CCA;CGA;BHA1CNA1CSA=VDA<UEB;VFA@VIV@APAPG?VDU>VDT:VFT9VFU=BBA=CCA;CGA;BHA6APB4APC3APD2APG=VDB=VKA<VKD;VLD/VKA/VRA.USB-VTA@VFV/VWV@AGA2AWA?VDU,VTT+VTU=BBA=BFA/BPA/CQA-CUA-BVA=VDB=VRA<VQD;VRD/URA@VFV2VUV@AGA?VDU1VRU-VRU=BBA=BFA9VEUCSBQAMAJBFCDEBHAJAMBODPFQJQMPQOSMUJVHV=SCQBNBICFDD3DOFPIPNOQNS9VFUDRCNCIDEFBHA7ALBNEOIONNRLUJV=VDA<UEB;VFA@VMVPUQTRRROQMPLMKFK1TQRQOPM4VOUPSPNOLMK@AIA?VDU>VDT:VFT9VFU=BBA=CCA;CGA;BHA9VEUCSBQAMAJBFCDEBHAJAMBODPFQJQMPQOSMUJVHV=SCQBNBICFDD3DOFPIPNOQNS9VFUDRCNCIDEFBHA7ALBNEOIONNRLUJV<DFFHGIGKFLDM>N<P<Q>Q@4@N>O=P=5DN?O>P>Q?=VDA<UEB;VFA@VMVPUQTRRRPQNPMMLFL1TQRQPPN4VOUPSPOOMML7LLKMIOCPARASCSE2EPCQBRB5KMJPDQCRCSD@AIA?VDU>VDT:VFT9VFU=BBA=CCA;CGA;BHA3SOVOPNSLUIVFVCUASAPBNELKJMINGNDMB?PCNEMKKMJNH>UBSBQCOENKLNJOHOENCMBJAGADBBDAGAABD@VAP9VHA8UIB7VJA0VQP@VQV<AMA?VAP>VAS=VAT;VAU5VQU3VQT2VQS1VQP9BFA9CGA7CKA7BLA=VDGEDGBJALAOBQDRGRU<UEFFD;VFFGCHBJA@VIV2VUV?VDU>VDT:VFT9VFU1VRU-VRU>VJA=VJDJA<VKD0UJA@VHV4VSV?VDT;VET:VEU2VQU/VQU=VHA<VHFHA;VIF5VIFHA5VPA4VPFPA3VQF-UQFPA@VIV5VNV0VWV?VEU>VET:VFT9VFU/VTU+VTU>VOA=VPA<VQA1UDB@VHV4VSV@AGA5ASA?VET;VET:VEU3VPU/VPU=BBA=BFA2BMA2CNA2CRA>VJKJA=VKKKB<VLKLA/ULK@VHV2VUV:AOA?VDU:VEU1VRU-VRU7BHA7CIA5CMA5BNA2VAVAP4VAA3VBA2VCA@AOAOG?VAP>VAS=VAT;VAU7AOB5AOC4AOD3AOG@\A<?\B<@\H\@<H<@Z]>:\G<9\H<@\H\@<H<@QIVQQ@QIUQQ@ASA;VAP;VGUAP>LCMDMDKBKBMCNEOIOKNLMMKMDNBOA6MLKLDMB8OJNKLKDLBOAPA6JJIEHBGAEADBBEAHAJBKD>GBEBDCB7IFHDGCECDDBEA=VDAEBGB<UEC@VFVFB;LGNIOKONNPLQIQGPDNBKAIAGBFD2LPJPFOD6OMNNMOJOFNCMBKA?VDU>VDT4KMLLLLJNJNLLNJOGODNBLAIAGBDDBGAIALBND>LBJBFCD:OENDMCJCFDCEBGA5VLAQA4UMB8VNVNA5LKNIOGODNBLAIAGBDDBGAIAKBLD>LBJBFCD:OENDMCJCFDCEBGA7VLU6VLT3COA3BPA>ININKMMLNIOGODNBLAIAGBDDBGAIALBND4JMKLM>LBJBFCD5ILLKNIO:OENDMCJCFDCEBGA6TKUJUJSLSLUKVHVFUETDQDA;TEQEB9VGUFSFA@OJO@AIA=BBA=CCA;CGA;BHA3POOPPOQNQLPKO:QEPDOCMCKDIEHGGIGKHLIMKMMLOKPIQGQ<ODMDKEI6ILKLMKO:QFPENEJFHGG8GJHKJKNJPIQ=ICHBFBECCDBGAKAN@O?=CGBKBNA?ECDFCKCNBO@O?N=K<E<B=A?A@BBEC<<C=B?B@CBEC=VDA<UEB@VFVFA;KGMHNJOMOONPMQJQA2MPJPB4ONNOKOA@AIA5ATA?VDU>VDT=BBA=CCA;CGA;BHA2BMA2CNA0CRA0BSA=VDTFTFVDV<VET=UFU=ODA<NEB@OFOFA@AIA?ODN>ODM=BBA=CCA;CGA;BHA:VGTITIVGV9VHT:UIU:OG>F;E:9NH?G<=OIOI?H<G;E:B:A;A=C=C;B;B<<OGN;OGM=VDA<UEB@VFVFA2NFE7IQA7HPA8HOA5OSO@AIA5ASA?VDU>VDT4OON/OON=BBA=CCA;CGA;BHA2CMA3CRA=VDA<UEB@VFVFA@AIA?VDU>VDT=BBA=CCA;CGA;BHA=ODA<NEB@OFOFA;KGMHNJOMOONPMQJQA2MPJPB4ONNOKOA0KRMSNUOXOZN[M\J\A'M[J[B)OYNZKZA@AIA5ATA*A_A?ODN>ODM=BBA=CCA;CGA;BHA2BMA2CNA0CRA0BSA'BXA'CYA%C]A%B^A=ODA<NEB@OFOFA;KGMHNJOMOONPMQJQA2MPJPB4ONNOKOA@AIA5ATA?ODN>ODM=BBA=CCA;CGA;BHA2BMA2CNA0CRA0BSA:ODNBLAIAGBDDBGAIALBNDOGOINLLNIOGO>LBJBFCD4DNFNJML:OENDMCJCFDCEBGA8AKBLCMFMJLMKNIO=OD:<NE;@OFOF:;LGNIOKONNPLQIQGPDNBKAIAGBFD2LPJPFOD6OMNNMOJOFNCMBKA@:I:?ODN>ODM=;B:=<C:;<G:;;H:5NL:4MM;6NMNNON:5LKNIOGODNBLAIAGBDDBGAIAKBLD>LBJBFCD:OENDMCJCFDCEBGA8:Q:5;J:5<K:3<O:3;P:=ODA<NEB@OFOFA4MMNLNLLNLNNMOKOINGLFI@AIA?ODN>ODM=BBA=CCA;CGA;BHA6MLOLKKMJNHODOBNAMAKBIDHIGKFLC?NAK?JDIIHKG5FKB@MBKDJIIKHLFLCKBIAEACBBCAEAABC=TDFECFBHAJALBMD<TEEFC=TFVFEGBHA@OJO=ODFECFBHAKAMBNCOE<NEEFC@OFOFEGBHA2OOATA1NPB5OQOQA?ODN>ODM0CRA0BSA>OIA=OIC<OJC2NJCIA@OHO6OQO?OEM:OEN4OON1OON=OHA<OHD;OID5OIDHA5OPA4OPD5ONOQD-NQDPA@OIO0OWO?OEN9OFN/OTN+OTN>OMA=ONA<OOA3NDB@OHO6OQO@AGA7AQA?ODN:OEN5ONN1ONN=BBA=BFA4BKA3BPA=OJA<OJC;OKC1NKCH=F;D:B:A;A=C=C;B;B<?OIO5ORO>OFM9OFN3OPN0OPN6OAA5OBA4OCA4OAOAK@AMAME?OAK>OAL=OAM;OAN9AMB7AMC6AMD5AME;\D[CZBXBVCTDSEQEOCM=[CYCWDUETFRFPENALEJFHFFEDDCCAC?D=>KEIEGDECDBBB@C>D=F<@\A<@\C[DZEXEVDTCSBQBODM>[DYDWCUBTARAPBNFLBJAHAFBDCCDAD?C==KBIBGCEDDEBE@D>C=A<@HAJBMDNFNHMLJNIPIRJSL@JBLDMFMHLLINHPHRISLSN=VCUATCSDH=SETDUCTDSDH=VEUGTESDH=DBBDAFBDD=CCBEBDC?VAUAO?UAO?VCUAO6VJUJO6UJO6VLUJO8ZB>2ZH>?OPO@IOI;ZF=7ZJ=7VLUMSMQORNTMUJVFVCUASAPBNELKJMINGNDMB3RMT?PCNEMKKMJNH>CBE>UBSBQCOENKLNJOHOENCMBJAFACBBCAECFCDDBFA.VAA;VHTHRGPEOCOAQASBUDVFVHUKTNTQUSV2HMGLELCNAPARBSDSFQHOH/NSMTMUN0MRLTL0LRKSKTLUN/NLH6GEAAFGL9MLQHVCPIJMDOBQASATBUD<BBF6QHU=PIKMEOCQBTB;BBG6PGU=QJKNEODQCTCUD?VAUAO?UAO?VCUAO9\FZDWBSANAJBEDAF>H<=VCSBOBICEDB;ZEXDUCOCIDCE@F>@\CZEWGSHNHJGEEAC>A<<VFSGOGIFEEB>ZDXEUFOFIECD@C>;QEPGFFE;QFE;QGPEFFE@NBNJHKH@NKH@NAMKIKH6NJNBHAH6NAH6NKMAIAH8TICJC8TJTJC@LRLRK@LAKRK>?CAACCEDCDAC?A>>DBCCBCD@LRLRK@LAKRK>DABCAEBCD>CBBDBCC.\A<B<.\T\B<>TCDAC=SDDGB<TEDGCHB>TETJULV7UKTMSMC6UNSND5VMUOTQTOSOC@CCCEBFAHBMCOC@TBSCQCDAC>SBTCUDSDCFB@TDVETEDGCHC@CBCDBEAFBHC?TDTFUGVIULTNT;THU?TDSFSHTIU5TLL4SMM3TNLGLDKBIAFAA@AECIDLDPC=BGCLCOB@AFBKBNAPC?TCTEUFVHULTNT<TGU?TDSFSHU5TLM4SMN3TNMLMILGK:LIKLJNJNC4IMD5JLC@CCDEDGCHB<CGB@CCCEBFAHBLCNC6VALAGJG5GPGQFQHPG?LBH>NCG7UJDHC6RLTKUKCMB6VMTLRLDNCOC9CICKBLAMBOC?VBM?VNV>ULU?TKTMUNV5PKOINEMBM8NJNLMLC6OMNMD5PMOONPNNMNC@CCDEDGCHB<CGB@CCCEBFAHBLCNC>TCDAC=SDDGB<TEDGCHB>TETIUKVLUNTOT7ULT8UKSMSOT<LFLJMLNMO7MKMMLMC5NNLND4ONNPMQMOLOC@CCCEBFAHBMCOC@TCVFUKUPV?UETJTMU@TESHSLTPV1VOTMQIMGJFGFDGA9KGHGEHB6OILHIHFICGA>SCM=RDN<SEM>SESJTLUMV7TKTMSMM5UNTNN4VNUPTQTOSOM>MEMMJOJ2MMMEJCJ>JCDAC=IDDGB<JEDGCHB4JMC3IND2JOC@CCCEBFAHBMCOC>TCKAJ=SDJFI<TEKGJHJ>TETJULV7UKTMSMC6UNSND5VMUOTQTOSOC@JBJDIEHFIHJLKMK?CDDFDHCIB;CHB?CDCFBGAIBMCOC>OAMCLEMCO>NBMDMCN>DABCAEBCD>CBBDBCC>PANCMENCP>OBNDNCO>?CAACCEDCDAC?A>>DBCCBCD0TAKQB@PRPRO@PAORO@HRHRG@HAGRG@TQKAB@RBTCUFVHVKULTMRMPLNJLHK?RCT6TLSLOKN@RCQCSDUFV9VJUKSKOJMHK:KGHHKFKGH:DEBGAIBGD:CFBHBGC1NOPMQJQHPGOFLFIGGIFLFNGOI7QHOGLGIHGIF1QOIOGQFSFUHVKVMUPTRRTPUMVJVGUETCRBPAMAJBGCEECGBJAMAPBRCSD0QPIPGQF;SHUJVLVMUTEUDWD6ULTSDTBUCSD9UJUKTRDSBTAUAWD;OGPIQJQKP7PJO:PIPJN@ACCEDHDJC=CHCIB@ADBGBHAJC5RFD9IPI@TCVFVHUJV=UGU@TCUETHTJV;QEPDNDMBMALAJBKDKDE<OEG?LEL;QFHEFDE6SJRIPIG7QJI6SKJJHIG6SQVSUTSTQRONM0USSSQ2UQTRSRPPN1NSLTJTD/LSJSE1NQMRKRD>AFCIDMDPC<BHCMCOB>AGBLBNAPCRDTD3MND3JRJ3GRG:UETCRBPAMAIBFCDFBIALAOBQCSETG>QBNBIDEGCJBMBPC:UESDQCNCJDGGDJCMCPDRETG8RIF7RJH6SKIJGIF8RKSNVPURUSV4UOTQT5TNSPSRTSV1SPD@VOVQURSRD>UOUQSQE@VBUDTOTPSPD:QFPENEMCMBLBJCKEKEF;OFH>LFL:QGIFGEF@ADCGDKDNC>BFCKCMB@AEBJBLANCPDRD7TJD7OLNNNPO7ILJNJPI@TCVEVGUIV=UFU@TCUETGTIV;QEPDNDMBMALAJBKDKDE<OEG?LEL;QFHEFDE8OJRKTLUNVPVSU5TNUPURT7RKSMTOTQSSU8GJJKLLMNMPL5LNLOK7JKKMKNJPL>AFCJDODSC<BHCOCRB>AGBNBQASC8OID=TFVIVKUMV:UJU=TFUHTKTMV7QIPHNHMFMELEJFKHKHF8OIH;LIL7QJIIGHF4RMCLBKBGDEDCCAA3RND3LRL7BIBGCDC2SOMRM/KOKOENCJAHAFBDBAA4ROSRVTUVUWV0USTUT1TRSTSVTWV/SRE:UETCRBPAMAJBGCEECGBJANAQBSDTFTISKRLPMNM>QBNBICF:UESDQCNCIDFEDGB/DSESIRK3APBQCRERIQKPLNM8RIE7RJG6SKHJFIE8RKSNVPURUSV4UOTQT5TNSPSRTSV/TNMNA3IRI3FRF@TCVFVHUJV=UGU@TCUETHTJV;QEPDNDMBMALAJBKDKDE<OEG?LEL;QFHEFDE>AFCIDLDNC<BHCKCMB>AGBJBLANC6SJRIPIG7QJI6SKJJHIG6SMUOVQVSU1UQURT4UOUQSSU3MPNRPSOTLTHSDQA0ORNSLSGRD1NQNRLRGQA3MNC3JRJ3GRG=TFVIVLUNV:UKU=TFUITLTNV6QJPINIMGMFLFJGKIKIF7OJH:LJL6QKIJGIF0TORNONDMBKBGDEDCCAA2QOE7BIBGCDC0TPRPFODMBKAHAFBCBAA>TEVHVKUMV;UJU>TEUHTKTMV7QIPHNHMFMELEJFKHKHF8OIH;LIL7QJIIGHF1TNRMOMDLB3QNE1TOROFNDLBIAFACBADAFBGCGDFCEBE@FDF@TCVFVHUJV=UGU@TCUETHTJV;QEPDNDMBMALAJBKDKDE<OEG?LEL;QFHEFDE>AFCIDLDNC<BGCKCMB>AGBJBLANC6SJRIPIG7QJI6SKJJHIG6SMUOVQVSU1UQURT4UOUQSSU3MQPROTN1ORNTN-NRKPING1IRHSDTBUB/FSB1IQHRBSATAUB3MNC@TCVFVHUJV=UGU@TCUETHTJV;QEPDNDMBMALAJBKDKDE<OEG?LEL;QFHEFDE>AFCJDODSC<BHCOCRB>AGBNBQASC6SJRIPIG7QJI6SKJJHIG6SMUOVQVSU1UQURT4UOUQSSU2UOD9RGQFOFMDMCLCJDKFKFG:PGI=LGL9RHJGHFG@ACCEDGDICJCKD=CGCIB@ACBFBHAIAJBKD9RLVPRPEQCRC5UORODNCOBPCOD5LOL7TKTNQNMKM6KNKNDMCOARCSD1RTVXRXEYCZC-UWRWDYB-LWL/TSTVQVMSM.KVKVCXAZC6TKD.TSD@SCUEVGVIUKRPGRDSC:UISJQPESB>UEUGTIQNFPCQBSA1TRSTSVTWV0USTUT1TRVTUVUWV<MCMBLBJCKEK>LEL@ACCEDHDJC=CGCIB@ADBGBHAJC<UED.SSA5PMOONQNSO<HGIKIMH:VEUCSBQANAJBGCEECGBJALAOBQCSETGUJUNTQSSQUOVNUKSHR>RBOBICF:VETDRCOCIDFEDGB.FTITORSQT2BQDRFSISORQPTNU9RHE8RIG7RJHIFHE3UNB3OPNQNSO3IPJQJSI?VCUDSDMBMALAJBKDKDCAADBD:F<=TERE<?LEL?VDUETFRF<;QISMVQRQD4UPRPD6TLTOQOC8DLDOC7CLCNB8BKBMAOCQD8SI=8OKNMNOO8IKJMJOI:VEUCSBQANAJBGCEECGBIAMAOBQCSETGUJUNTQSSQUOVNUKSHR>RBOBICF:VETDRCOCIDFEDGB.FTITORSQT2BQDRFSISORQPTNU9RHE8RIG7RJHIFHE3UNB3OPNQNSO3IPJQJSI8AJBKBMAQ<S;T;4@O=Q;R;6BLAO;Q:S:T;@TCVFVHUJV=UGU@TCUETHTJV;QEPDNDMBMALAJBKDKDE<OEG?LEL;QFHEFDE>AFCIDKDNC<BGCKCMB>AGBJBLANC6SJRIPIG7QJI6SKJJHIG6SNUPVRUSSSPRNQMMKKJ1UQURSROQN3UPTQRQOPMMK4KOJPISDTCUC1HRDTB4KOIQCSAUC4SLTJUGV3TLU2UKVGVDUCTBRCPDOGNONQMRLRJQG>QDPGOPORNSMSKRI>TCRDQGPQPSOTMTKQGMA@MBLDKMKNJNIMG?KDJLJMI@MALBJDIKIMHMG@ADCHDKDNC>BFCJCMB@AEBJBMA2UMSKP7NHK:IEGCFBFBGCF>RBPAMAIBFDCFBIALAOBQCSETG?ICFEDGCJBMBPC>RBOBKCHEEGDJCMCPDRETG@SBUDVHVNURUTV8UMTQT@SBTDUGUMSPSRTTV5SKRIQIF7QJH6RKIJGIF1SPD@TCVEVHUJV=UGU@TCUFTHTJV=RCPBMBICFDDFBIALAOBQCSAUC>IDFGCJBMB=RCNCKDHEFGDJCNCQD3SJRIPIF7QJH6RKIJGIF3SPTRVSUUTSSSETCUC/SSTRUQTRSRDTB1TQSQD3SNC3NQN3JQJ?VCUDSDMBMALAJBKDKDDBC=TERED?LEL;CICKB?VDUETFRFDJDMC?CECHBJAMCPDRD7RMSOTQVRUTTRSRD0SRTQUPTQSQE2TPSPD7RJD7OLNNNPO7ILJNJPI?VCUDSDMBMALAJBKDKDDBC=TERED?LEL;CHCJB?VDUETFRFDIDKC?CECHBIAKCNDPCQASCVD8TLVNTNDQDSC5UMTMD8TKTLSLDKC0CRB0TTVVTVD-UUTUD0TSTTSTDSC8TID0TQD8NLN8JLJ0NTN0JTJ@SCUEVGVHUPCQBSB;UGTOCPB>UEUFTNBOAQASBUD1VRUTUUV1UQTST2TPSRSTTUV@ABCDDFDGC>CECFB@ABBDBFA1VLM7JFA<LIL5LQL?VCUDSDMBMALAJBKDKDDBC=TERED?LEL;CICKB?VDUETFRFDJDMC?CECHBJAMCPD7RMSOTQVRUTTRSR>Q<O:M;I<D<0SRTQUPTQSQC2TPSPDRA1;N<K<0<N=H=D<7RJD7OLNNNPO7ILJNJPI2UNSIMFIDEAA4QEF0VNRLNIJDDCB@TCVFULUQV?UFTJTNU@TESISMTOU>BECIDMDQC=BHCLCPB@AFBLBOAQC=LHL6LOL@\A<?\B<@\H\@<H<@Z]>:\G<9\H<@\H\@<H<@QIVQQ@QIUQQ@ASA;VAP;VGUAP=JBHAFADBBDAFCID@FBDCCEB?HBFCDECFC?LDLGMINJOLMKLKDLCMC>NBMEM9MKMJNJCKB@MCODNFMILICKAMC@MFH?TCRCDAC=RCTDUDDGB?TEVEDGCHB@CCCEBFAHBKCMC<LHMJNKOLNNMOMMLMC7NLMLD9MIMKLKC>MCDACBCDBEA=MDCFB<MEDGCHCFBEA>MGNIOJNLMMM9NIMKM<MGNILKLMM9OFNCMCDAC=MDDGB9OEMEDGCHB@CCCEBFAHBKCMC>TFVGSMMMC;SDTEUFSLMLD>TKLKC>MCDACBCDBEA=MDCFB<MEDGCHCFBEA>MGNIOLKJJEG9NKK<MGNJJ=TDDBCCCEBFA<TECGB;TFDHCICGBFA=TGUIVJULTMT9UITKT;TGUISKSMT@ODO;OJO>MCDACBCDBEAFBHCKD=LDCFB<MEDGCHC>MEMHNJOKNMMOMMLM@L=J;H:G;E<C<8NLLL@8;G<F<9NIMKLKBL?L=7;I<G=E=C<?TCRCDACBCDBEA=RCTDUDCFB?TEVEDGCEA<LHMJNKOLNNMOMMLMCKAJ?7NLMLCKA9MIMKLKCJ?J<K:L:J<=VBTDSFTDV=UCTETDU=OCNAMCLCCEAGC=LEMDNCMDLDCEB=OENGMELEDFCGC=VBTDSFTDV=UCTETDU=OCNAMCLCCEAF?=LEMDNCMDLDCEA=OENGMELECF?F<D:B:B;D:?TCRCDACBCDBEA=RCTDUDCFB?TEVEDGCEA<LHNJOLLIJEG8NKL9NJK8JJILDMCNC8IJHKCLB9IIHJCLANC?TCRCDACBCDBEA=RCTDUDCFB?TEVEDGCHCFBEA@MBMCLCDACBCDBEA>NDMDCFB@MCOEMEDGCEA<LHMJNKOMMMDOCMA7NLMLCNB9MIMKLKDJCLBMA4LPMRNSOTNVMWMULUDVCWC/NTMTCUB1MQMSLSCUAWC@MBMCLCDACBCDBEA>NDMDCFB@MCOEMEDGCEA<LHMJNKOLNNMOMMLMDNCOC7NLMLCMB9MIMKLKCMAOC>MCDAC=LDDGB<MEDGCHB@CCCEBFAHBKCMC>MEMHNJOKNMMOMMLMC8NLLLD9NIMKLKC?OCMCDACCCC:>NDMD;E<D>=CECGB?ODNEMEDGCHB<BFAHBKCMC<BE>F<C:<LHMJNKOLNNMOMMLMC7NLMLD9MIMKLKC>MCDAC=LDCFB<MEDGCHC@CBCDBEAFBHCKD>MEMHNJOKNMMOMMLM:8NLLL;K<L>9NIMKLK>J<M:@MBMCLCDACBCDBEA?NDMDCFB@MCOEMEDGCHCFBEA<MIOJNLMMM9NIMKM:NILKLMM?MBIDHJHLGLC>MCI6GKC<NDMDIFH9HJGJCIB?MENGOINKNLO;NHN<NGMIMKN5CIBGAEBCBAA9BFB8BGCDCAA5OKMIJDEAA>TDRDDBCCCEBFA<RDTEUECGB>TFVFDHCICGBFA@ODO;OIO@MBMCLCDAC?NDMDCFB@MCOEMEDGCHC@CBCDBEAFBHCKD6OLNNMOMMLMDNCOC7NLMLCMB6OIMKLKCMAOC@OBMBDEAGCJDLD?NCMCDFB@OCNDMDEEDGC7OKNMMNMLLLD8NKMKE7OHMJLJD@OBMBDEAGCJD?NCMCDFB@OCNDMDEEDGC7OHMJLJDMAOCRDTD8NKMKDNB7OKNMMLLLEMDOC/OSNUMVMTLTD0NSMSE/OPMRLRD?MCMELFKJCKBMAOC=NFMKCMB?MDOFNGMKELDNCOC8ILOMNONPO5NMMNM6MMLOMPO9GEADBBBAA<BDCCC;CDDBCAA=HGH7HMH@MBMCLCDAC?NDMDCFB@MCOEMEDGCHC@CBCDBEAFBHCKD6OLNNMOMMLM@L=J;H:G;E<C<7NLML@8;G<F<6OIMKLKBL?L=7;I<G=E=C<4OAA@MCLFLIMMO?NDMHM@MCOENINMO@AECHDKDMC;CJCLB@AEBIBKAMC>HKH;\D[CZBXBVCTDSEQEOCM=[CYCWDUETFRFPENALEJFHFFEDDCCAC?D=>KEIEGDECDBBB@C>D=F<@\A<@\C[DZEXEVDTCSBQBODM>[DYDWCUBTARAPBNFLBJAHAFBDCCDAD?C==KBIBGCEDDEBE@D>C=A<@HAJBMDNFNHMLJNIPIRJSL@JBLDMFMHLLINHPHRISLSN9VGVFUDH9UGUDH9UHTDH9VIUITDH?DACABBACADBDCCDBD?CBBCBCCBC=VCUAO=UAO=VEUAO3VMUKO3UKO3VOUKO8ZB>2ZH>?OPO@IOI6ZC=1ZH=0QQRPRPPRPRRQTPUMVIVFUDSDPENGLMINGNDMB<PFNMJNH;UESEQFOLLNJOHOENCMBJAFACBBCAEAGCGCEBEBF.VAA;VHTHRGPEOCOAQASBUDVFVHUKTNTQUSV2HMGLELCNAPARBSDSFQHOH+MVNUNULWLWNVOUOSNQLLDJBHAEABBADAFBHCIEJJLLMNOOQOSNULVJUISIPJJKGLENBPARASCSD;ABB>BBDBFCHDIFJ7LKINCPB<ADBCDCFDHEIGJLM8PJMKJMFOCQBRBSC=VCUAO=UAO=VEUAO3\L[IYFVDSBOAKAFBBC?E<:VESCOBJBB3\KZHWFTERDOCKBB?JCAD>E<7\LYMVNRNMMIKEIBF?C=A<4VMNLIJEHB7\KZLWMN4VLMKIJFIDGAD>A<;QEPGFFE;QFE;QGPEFFE@NBNJHKH@NKH@NAMKIKH6NJNBHAH6NAH6NKMAIAH8TICJC8TJTJC@LRLRK@LAKRK=ACABBBCCDDDECEAD?C>A=>CCBDBDCCC=AD@C>@LRLRK@LAKRK?DACABBACADBDCCDBD?CBBCBCCBC&\A<B<&\ \B<7VGUESCPBMAIAFBCCBEAGAJBLDNGOJPNPQOTNULVJV:TERDPCMBIBECC7CLEMGNJONORNT7VHUFREPDMCICDDBEA:AIBKELGMJNNNSMULV;RAACA8VGRBA8VCA8VFSCQAP;RDQAP:QGRHRHPFPFRGTHUKVNVQURSRQQOOMEGCEAA1UQSQQPONMKK3VOUPSPQOOMMEG?CCDEDJCOCPD<DJBOB<DJAMAOBPDPE;QFRGRGPEPERFTGUJVMVPUQSQQPOONMMJL2UPSPQOONN4VNUOSOQNOLMJL9LJLMKNJOHOENCLBIAFACBBCAEAGCGCEBEBF4JNHNEMC7LLKMIMELCKBIA3RIAKA0VORJA0VKA0VAGQG9VCL9VRV9UPU:TLTPURV>LDMGNJNMMNLOJOGNDLBHAEACBBCAEAGCGCEBEBF4LNJNGMDKB7NLMMKMGLDJBHA2ROSNSNQPQPSOUMVJVGUESCPBMAIAFBCCBEAHAKBMDNFNIMKLLJMGMELDKCI;SDPCMBIBECC5DMFMILK7VHUFREPDMCICDDBEA9AJBKCLFLJKLJM>VAP1VOSMPIKGHFEEA:IEEDA4PGJEGDECAEA?SEVGVLS=UGULS?SDTGTLSNSOTPV7VGUFTEREOFMHLKLNMPNQPQSPUNVJV5VGU:TFRFNGM;MIL7LNM2NPPPSOU1ULV7VHTGRGNHL6LMMNNOPOTNV9LDKBIAGADBBEAIAMBNCOEOHNJMKKL8LDK<KCIBGBDCB?BGAMB4CNENHMJ4KJL9LFKDICGCDDBEA8AKBLCMEMILKKL3NMLLKJJGJEKDLCNCQDSFUIVLVNUOTPQPNOJNGLDJBGADABBADAFCFCDBDBE<LDNDQES3TORONNJMGKD:JFKEMEQFTGUIV5VMUNSNNMJLGKEIBGA<ODNDMELFLGMGNFOEO<NEMFMFNEN?DACABBACADBDCCDBD?CBBCBCCBC;OENEMFLGLHMHNGOFO;NFMGMGNFN=ACABBBCCDDDECEAD?C>A=>CCBDBDCCC=AD@C>0TAKQB@PRPRO@PAORO@HRHRG@HAGRG@TQKAB?QBRCRCPAPARBTCUFVJVMUNSNQMOLNJMFLDKDIFHGH9VMU5UMSMQLOKNIM7VKULSLQKOJNFLEKEIFH>DBCBBCADAEBECDDCD>CCBDBDCCC=OBNALAJBHDGFGHHIJILHNFODO=OALBHFGIJHNDO;OBNAJDGHHILFO1VDB3ROA2TPB1VPTQCQA:GOG@AGA5ASA=BBA=BFA2BMA2CNA0CRA7VDA6VEA5VFA:VRVUUVSVQUNTMQL-UUSUQTNSM/VSUTSTQSNQL8LQLSKTITGSDQBMAAA/KSISGRDPB0LRJRGQDOBMA9VKU8VJT4VKT3VKU<BBA<CCA;CGA<BHA1TQTRVQPQRPTOUMVJVGUESCPBMAIAFBCCBFAIAKBMDNF:TERDPCMBIBECC7VHUFREPDMCICDDBFA7VDA6VEA5VFA:VPVSUTTUQUMTIREPCNBJAAA/USTTQTMSIQEOC1VRTSQSMRIPEMBJA9VKU8VJT4VKT3VKU<BBA<CCA;CGA<BHA7VDA6VEA5VFA1PNH:VVVUP8LOL@APARF9VKU8VJT4VKT3VKU/VMJMJMJUT-VUS,VUP1PNLNH2NMLNJ2MLLNK<BBA<CCA;CGA<BHA6APB4APC1CRF7VDA6VEA5VFA1PNH:VVVUP8LOL@AIA9VKU8VJT4VKT3VKU/VUU.VUT-VUS,VUP1PNLNH2NMLNJ2MLLNK<BBA<CCA;CGA<BHA1TQTRVQPQRPTOUMVJVGUESCPBMAIAFBCCBFAHAKBMDOH:TERDPCMBIBECC5DMENH7VHUFREPDMCICDDBFA9AJBLEMH7HRH6HMG5HME1HNF0HNG7VDA6VEA5VFA+VPA*VQA)VRA:VOV.V[V9LTL@AIA4AUA9VKU8VJT4VKT3VKU-VWU,VVT(VWT'VWU<BBA<CCA;CGA<BHA0BNA0COA/CSA0BTA7VDA6VEA5VFA:VOV@AIA9VKU8VJT4VKT3VKU<BBA<CCA;CGA<BHA3VIEHCFA2VKIJFID1VLIJDHBFADABBADAFBGCGDFDECDBD?FBECECFBF6VSV5VOU4VNT0VOT/VOU7VDA6VEA5VFA*UHJ5MPA4MQA3NRB:VOV-VZV@AIA4ATA9VKU8VJT4VKT3VKU,VWU(VWU<BBA<CCA;CGA<BHA1BNA1COA0CSA7VDA6VEA5VFA:VOV@APARG9VKU8VJT4VKT3VKU<BBA<CCA;CGA<BHA6APB4AQD2ARG7VDB7UKCKA6VLC5VMD)VMDKA)VRA(VSA'VTA:VLV)V]V@AGA2AWA9VJU8VJT&VYT%VYU=BBA=BFA.BPA.CQA-CUA.BVA7VDB7VQA6VQD5VRD*URDQA:VLV-VZV@AGA9VKU8VKT,VWU(VWU=BBA=BFA7VGUESCPBMAIAFBCCBEAHAKBMDOGPJQNQQPTOUMVJV;SDPCMBIBECC5DNGOJPNPROT7VHUFREPDMCICDDBEA9AJBLEMGNJONOSNUMV7VDA6VEA5VFA:VSVVUWSWQVNTLPKHK,UVSVQUNSL.VTUUSUQTNRLPK@AIA9VKU8VJT4VKT3VKU<BBA<CCA;CGA<BHA7VGUESCPBMAIAFBCCBEAHAKBMDOGPJQNQQPTOUMVJV;SDPCMBIBECC5DNGOJPNPROT7VHUFREPDMCICDDBEA9AJBLEMGNJONOSNUMV>DDFFGGGIFJDK?L>M>N?6>L=M=7DJ=K<M<N?N@7VDA6VEA5VFA:VRVUUVSVQUNTMQLIL-UUSUQTNSM/VSUTSTQSNQL4LOKPJRDSCTCUD/CSBTB1JQBRATAUDUE@AIA9VKU8VJT4VKT3VKU<BBA<CCA;CGA<BHA/TSTTVSPSRRTQUNVJVGUESEPFNHLNIOGODNB;PGNNJOH:UFSFQGOMLOJPHPEOCNBKAGADBCCBEBGAABCCC7VDA6VEA5VFA>VAP.VRP>VSV@AIA=VAP;VBS9VCU2VRU1VRT0VRS/VRP<BBA<CCA;CGA<BHA<VBKAGADBBEAIALBNDOGSU;VCKBGBCCB:VDKCGCCEA?VJV1VVV>VFU=VET9VFT8VFU0VSU,VSU>VCTDCDA=UED<VFE1UDA@VHV4VSV?VCT;VET:VDU3VPU/VPU=VDTBCBA<UCD;VDE5VDEBA5VLTJCJA4UKD3VLE-ULEJA@VIV5VNV0VWV?VEU>VDT:VES9VEU/VTU+VTU8VOA7VPA6VQA+UDB:VNV.VYV@AGA5ASA9VJT5VKT4VKU-VVU)VVU=BBA=BFA2BMA2CNA1CRA>VGLDA=VHLEA<VILFA/UIL@VHV2VUV@AIA?VDU;VET:VDU1VRU-VRU<BBA<CCA;CGA<BHA.VAA-VBA,VCA,VGVEP@AOAQG9VEP8VFS6VGU6AOB4APD3AQG<VCUBTARAPBOCODPDQCRBR>UBSBR?QBPCPCQBQ7TISJRKSJT@KSK7DICJBKCJD=SCSBTBUCVDVEUESDQCPAO>UCTDTDUCU=SDRCP8TIC@LQL@CQC8TIC@TQT@LQL0TCB@NSN@HSH3OLHLDMBNAPARCSE2OMHMB3OPONHMD5HLKKNIOGODNBKAHAFBCCBEAGAIBJCKELH<NCKBHBECC:OEMDKCHCEDBEA=VBOAIAEBCCBEAGAJBLEMHMJLMKNIOGOENDMCKBH<VCOBKBECB7CKELHLKKM@VFVDOBH:AICJEKHKKJNIO?VEU>VDT5KLLKLKJMJMLLNJOGODNBKAHAFBCCBEAGAJBLE=MCKBHBECC:OEMDKCHCEDBEA1VMKLGLDMBNAPARCSE0VNKMGMB4VRVNHMD5HLKKNIOGODNBKAHAFBCCBEAGAIBJCKELH=MCKBHBECC:OEMDKCHCEDBEA3VQU2VPT?FFGIHLJMLLNJOGODNBKAHAFBCCBEAGAJBLD=MCKBHBECC:OEMDKCHCEDBEA.TSURURSTSTUSVQVOUMSLQKNJJHAG>F<D:4RLOKJIAH>0VOTNRMOLJJBI?H=F;D:B:A;A=C=C;B;B<:ORO1OLAK>I;G:0OMAK=1ORONAL=J;G:D:B;A<A>C>C<B<B=3HNKMNKOIOFNDKCHCFDCEBGAIAKBLCMENH;MEKDHDEEC8OGMFKEHEEFBGA:VAACA9VBA=VIVCA<HGLINKOMOONPLPIND2NOJNFNB2LMGMDNBOAQASCTE<VHU;VGT9VHTJTJVHV8VIT9UJU@KBMDOFOGNHLHIFD:NGJFFFB:LEGEDFBGAIAKCLE4VMTOTOVMV3VNT4UOU<KFMHOJOKNLLLIJBI?H=F;D:B:A;A=C=C;B;B<6NKIIBH?G=6LJHHAG>F<D::VAACA9VBA=VIVCA0MQNPNPLRLRNQOOOMNIJGI<IGIIHJGLCMBOB8GKCLB:IHHJBKAMAOBQE<VHU;VGT<VBKAGADBBCAEAGCHE;VCKBGBB?VGVCHBD>VFU=VET@KBMDOFOGNHLHIFA:NGIEA:LFHDAFA9IJLLNNOPORNSLSIQA/NRIPA/LQHOAQA.IULWNYO[O]N^L^I\D$N]J\F\B$L[G[D\B]A_AaCbE@KBMDOFOGNHLHIFA:NGIEA:LFHDAFA9IJLLNNOPORNSLSIQD/NRJQFQB/LPGPDQBRATAVCWE:ODNBKAHAFBCCBFAIALBNEOHOJNMMNJOGO=MCKBHBECC5CMENHNKMM:OEMDKCHCEDBFA8AKCLEMHMKLNJO>KDMFOHOINJLJIIEF:8NIIHEE:8LHHD:7HKKLMMNOOQOSNTMUJUHTERBOAMAKBJEJH.MTKTHSERC0ORNSKSHREQCOA@:I:<;B:<<C:;<G:<;H:3OH:2OI:3OPOJ:5HLKKNIOGODNBKAHAFBCCBEAGAIBJCKELH=MCKBHBECC:OEMDKCHCEDBEA<:M:8;F:8<G:7<K:8;L:@KBMDOFOGNHLHHFA:NGHEA:LFHDAFA1MPNONOLQLQNPONOLNJLHH4LMMLMLKNKNMMNJOGODNCMCKDIFHIGKFLD=NCK=JFIIHKG5FKB>MDKFJIIKHLFLDKBHAEABBACAECECCBCBD:VDKCGCDDBEAGAICJE9VEKDGDB:VIVEHDD@OKO@KBMDOFOGNHLHIFD:NGJFFFB:LEGEDFBHAJALBNDPG/OPGPDQBRATAVCWE.OQGQB/OTORHQD@KBMDOFOGNHLHIFD:NGJFFFB:LEGEDFBHAJALBNDPGQKQOPOPNQL@KBMDOFOGNHLHIFD:NGJFFFB:LEGEDFBHAJALBNDOG0OOGODPBRATAVBXDZG[K[OZOZN[L/OPGPB0OSOQHPD>KENGOIOKNLLLJ8OJNJJIFHDFBDABAABADCDCBBBBC6MKJJFJC.MSNRNRLTLTNSOQOONMLLJKFKBLA8FIDJBLANAPBRE@KBMDOFOGNHLHIFD:NGJFFFB:LEGEDFBHAJALBNDPH/ONAM>K;I:.OOAM=/OTOPAN=L;I:F:D;C<C>E>E<D<D=2ONMLKDEBCAA3MEMCLBJ5MHNENDM5MHOEOCMBJ?CKCMDNF=CHBKBLC=CHAKAMCNF0VAOQH@FQF@AQA@PSP@KSK@FSF@VQOAH@FQF@AQA/FPFNGLIIMHNFODOBNALAJBHDGFGHHIILMNOPPRPAAAAAAAAAAAAAA"""
        Code1 = {}
        Code2 = {}
        # dummy zero'th entry
        PlotBasem._string_data_fo.append(0)
        PlotBasem._string_data_fx.append(0)
        PlotBasem._string_data_fy.append(0)
        # should map this
        for i in range(32, 127) :
            c = "%c" % (i)
            Code1[c] = i-32
            Code2[c] = i-65
            PlotBasem._string_data_code[c] = Code1[c]
        off = 1
        for c in offsetstring :
            off += Code1[c]
            PlotBasem._string_data_fo.append(off)
        for cx, cy in zip(charstring[0::2], charstring[1::2]) :
            PlotBasem._string_data_fx.append(Code2[cx])
            PlotBasem._string_data_fy.append(Code2[cy])
        PlotBasem._string_data_fy[1499] = 65
        PlotBasem._string_data_fx[25839] = 27
        PlotBasem._string_data_nchar = 1152
    #==========================================================================
    # STATICMETHOD : __plot_create_bitmaps
    # PURPOSE : make bitmaps for control buttons
    #==========================================================================
    @staticmethod
    def __plot_create_bitmaps() :
        if not tk._default_root :
            root = tk.Tk()
            root.wm_state("withdrawn")
            tk._default_root = root
        PlotBasem._bm_R = tk.Image("bitmap")   # move-right
        PlotBasem._bm_R["data"] = """
            #define bm_R_width 16
            #define bm_R_height 16
            static char bm_R_bits[] = {
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 0x00,
                0xc0, 0x01, 0x80, 0x07, 0x80, 0x1f, 0xfe, 0x7f,
                0xfe, 0x7f, 0x80, 0x1f, 0x80, 0x07, 0xc0, 0x01,
                0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            };
        """
        PlotBasem._bm_L = tk.Image("bitmap")   # move-left
        PlotBasem._bm_L["data"] = """
            #define bm_L_width 16
            #define bm_L_height 16
            static char bm_L_bits[] = {
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06,
                0x80, 0x03, 0xe0, 0x01, 0xf8, 0x01, 0xfe, 0x7f,
                0xfe, 0x7f, 0xf8, 0x01, 0xe0, 0x01, 0x80, 0x03,
                0x00, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            };
        """
        PlotBasem._bm_U = tk.Image("bitmap")   # move-up
        PlotBasem._bm_U["data"] = """
            #define bm_U_width 16
            #define bm_U_height 16
            static char bm_U_bits[] = {
                0x00, 0x00, 0x80, 0x01, 0x80, 0x01, 0xc0, 0x03,
                0xc0, 0x03, 0xe0, 0x07, 0xe0, 0x07, 0xf0, 0x0f,
                0xf0, 0x0f, 0x98, 0x19, 0x88, 0x11, 0x80, 0x01,
                0x80, 0x01, 0x80, 0x01, 0x80, 0x01, 0x00, 0x00
            };
        """
        PlotBasem._bm_D = tk.Image("bitmap")   # move-down
        PlotBasem._bm_D["data"] = """
            #define bm_D_width 16
            #define bm_D_height 16
            static char bm_D_bits[] = {
                0x00, 0x00, 0x80, 0x01, 0x80, 0x01, 0x80, 0x01,
                0x80, 0x01, 0x88, 0x11, 0x98, 0x19, 0xf0, 0x0f,
                0xf0, 0x0f, 0xe0, 0x07, 0xe0, 0x07, 0xc0, 0x03,
                0xc0, 0x03, 0x80, 0x01, 0x80, 0x01, 0x00, 0x00
            };
        """
        PlotBasem._bm_ao = tk.Image("bitmap")   # zoom out
        PlotBasem._bm_ao["data"] = """
            #define bm_ao_width 16
            #define bm_ao_height 16
            static char bm_ao_bits[] = {
                0x80, 0x01, 0xc0, 0x03, 0xe0, 0x07, 0x00, 0x00,
                0x00, 0x00, 0x04, 0x20, 0x06, 0x60, 0x07, 0xe0,
                0x07, 0xe0, 0x06, 0x60, 0x04, 0x20, 0x00, 0x00,
                0x00, 0x00, 0xe0, 0x07, 0xc0, 0x03, 0x80, 0x01
            };
        """
        PlotBasem._bm_ai = tk.Image("bitmap")   # zoom in
        PlotBasem._bm_ai["data"] = """
            #define bm_ai_width 16
            #define bm_ai_height 16
            static char bm_ai_bits[] = {
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xe0, 0x07,
                0xc0, 0x03, 0x88, 0x11, 0x18, 0x18, 0x38, 0x1c,
                0x38, 0x1c, 0x18, 0x18, 0x88, 0x11, 0xc0, 0x03,
                0xe0, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            };
        """
        PlotBasem._bm_az = tk.Image("bitmap")   # zoom start
        PlotBasem._bm_az["data"] = """
            #define bm_az_width 16
            #define bm_az_height 16
            static char bm_az_bits[] = {
                0x00, 0x00, 0x00, 0x00, 0xfc, 0x3f, 0xfc, 0x3f,
                0x0c, 0x30, 0x0c, 0x30, 0x0c, 0x30, 0x0c, 0x30,
                0x0c, 0x30, 0x0c, 0x30, 0x0c, 0x30, 0x0c, 0x30,
                0xfc, 0x3f, 0xfc, 0x3f, 0x00, 0x00, 0x00, 0x00
            };
        """
        PlotBasem._bm_xo = tk.Image("bitmap")   # x-out
        PlotBasem._bm_xo["data"] = """
            #define bm_xo_width 16
            #define bm_xo_height 16
            static char bm_xo_bits[] = {
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x08,
                0x18, 0x18, 0x0c, 0x30, 0x0e, 0x70, 0xff, 0xff,
                0xff, 0xff, 0x0e, 0x70, 0x0c, 0x30, 0x18, 0x18,
                0x10, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            };
        """
        PlotBasem._bm_yo = tk.Image("bitmap")   # y-out
        PlotBasem._bm_yo["data"] = """
            #define bm_yo_width 16
            #define bm_yo_height 16
            static char bm_yo_bits[] = {
                0x80, 0x01, 0xc0, 0x03, 0xe0, 0x07, 0xf0, 0x0f,
                0x98, 0x19, 0x80, 0x01, 0x80, 0x01, 0x80, 0x01,
                0x80, 0x01, 0x80, 0x01, 0x80, 0x01, 0x98, 0x19,
                0xf0, 0x0f, 0xe0, 0x07, 0xc0, 0x03, 0x80, 0x01
            };
        """
        PlotBasem._bm_ann_arrow_left = tk.Image("bitmap")
        PlotBasem._bm_ann_arrow_left["data"] = """
            #define bm_ann_arrow_left_width 32
            #define bm_ann_arrow_left_height 16
            static char bm_ann_arrow_left_bits[] = {
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00,
                0x00, 0x03, 0x00, 0x00, 0xc0, 0x01, 0x00, 0x00,
                0xf0, 0x01, 0x00, 0x00, 0xfc, 0xff, 0xff, 0x3f,
                0xf0, 0x01, 0x00, 0x00, 0xc0, 0x01, 0x00, 0x00,
                0x00, 0x03, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            };
        """
        PlotBasem._bm_ann_arrow_right = tk.Image("bitmap")
        PlotBasem._bm_ann_arrow_right["data"] = """
            #define bm_ann_arrow_right_width 32
            #define bm_ann_arrow_right_height 16
            static char bm_ann_arrow_right_bits[] = {
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00,
                0x00, 0x00, 0xc0, 0x00, 0x00, 0x00, 0x80, 0x03,
                0x00, 0x00, 0x80, 0x0f, 0xfc, 0xff, 0xff, 0x3f,
                0x00, 0x00, 0x80, 0x0f, 0x00, 0x00, 0x80, 0x03,
                0x00, 0x00, 0xc0, 0x00, 0x00, 0x00, 0x40, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            };
        """
        PlotBasem._bm_ann_arrow_both = tk.Image("bitmap")
        PlotBasem._bm_ann_arrow_both["data"] = """
            #define bm_ann_arrow_both_width 32
            #define bm_ann_arrow_both_height 16
            static char bm_ann_arrow_both_bits[] = {
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x40, 0x00,
                0x00, 0x03, 0xc0, 0x00, 0xc0, 0x01, 0x80, 0x03,
                0xf0, 0x01, 0x80, 0x0f, 0xfc, 0xff, 0xff, 0x3f,
                0xf0, 0x01, 0x80, 0x0f, 0xc0, 0x01, 0x80, 0x03,
                0x00, 0x03, 0xc0, 0x00, 0x00, 0x02, 0x40, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            };
        """
        PlotBasem._bm_ann_line = tk.Image("bitmap")
        PlotBasem._bm_ann_line["data"] = """
            #define bm_ann_line_width 32
            #define bm_ann_line_height 16
            static char bm_ann_line_bits[] = {
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0xfc, 0xff, 0xff, 0x3f,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            };
        """
        PlotBasem._bm_ann_none = tk.Image("bitmap")
        PlotBasem._bm_ann_none["data"] = """
            #define bm_ann_none_width 32
            #define bm_ann_none_height 16
            static char bm_ann_none_bits[] = {
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            };
        """
        PlotBasem._bm_ann_rect = tk.Image("bitmap")
        PlotBasem._bm_ann_rect["data"] = """
            #define bm_ann_rect_width 32
            #define bm_ann_rect_height 16
            static char bm_ann_rect_bits[] = {
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x80, 0xff, 0xff, 0x01, 0x80, 0x00, 0x00, 0x01,
                0x80, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x01,
                0x80, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x01,
                0x80, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x01,
                0x80, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x01,
                0x80, 0x00, 0x00, 0x01, 0x80, 0xff, 0xff, 0x01,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            };
        """
        PlotBasem._bm_ann_frect = tk.Image("bitmap")
        PlotBasem._bm_ann_frect["data"] = """
            #define bm_ann_frect_width 32
            #define bm_ann_frect_height 16
            static char bm_ann_frect_bits[] = {
                0x00, 0x00, 0x00, 0x00, 0x40, 0x92, 0x24, 0x01,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x40, 0x92, 0x24, 0x01, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x40, 0x92, 0x24, 0x01,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x40, 0x92, 0x24, 0x01, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x40, 0x92, 0x24, 0x01,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            };
        """
    #==========================================================================
    # METHOD  : plot_symb
    # PURPOSE : plot a symbol
    # NOTES   :
    #     * xp, yp, hp in st units
    #==========================================================================
    def plot_symb(self, sp, tp, hp, symbol, tags=None) :
        """ plot a symbol.

        **arguments**:

            **sp, tp** (float)

                plot location in scaled coordinates.
                In the scaled domain,
                every point on the canvas is mapped to the window
                smin, smax = 0.0, 1.0 and tmin, tmax = 0.0, 1.0

            **hp** (float)

                size of the symbol to be drawn in scaled units.

            **symbol** (str)

                the name of the symbol to be drawn. One of:

                    * spade      : (Hershey) spade

                    * heart      : (Hershey) heart

                    * diam       : (Hershey) diamond

                    * club       : (Hershey) club

                    * shamrock   : (Hershey) shamrock

                    * fleurdelis : (Hershey) Fleur-de-lis

                    * circle     : (Hershey) circle

                    * star       : (Hershey) star

                    * dot        : dot

                    * square     : square

                    * diamond    : diamond

                    * triangle   : triangle

                    * itriangle  : inverted triangle

                    * dash       : dash

                    * pipe       : pipe

                    * plus       : plus

                    * cross      : cross

            **tags** (str)

                tk canvas tags to apply to the symbol.

        """
        Symb = {
            "spade"      : 201,
            "heart"      : 202,
            "diam"       : 203,
            "club"       : 204,
            "shamrock"   : 205,
            "fleurdelis" : 206,
            "circle"     : 207,
            "star"       : 211,
        }
        plot = self._Component["plot"]
        if symbol in Symb :
            sp += hp*0.15
            hp *= 1.5
            self.plot_texv(sp, tp, hp, "X", single_char=Symb[symbol], tags=tags)
        else :
            s1 = sp - hp*0.5
            s2 = sp + hp*0.5
            t1 = tp - hp*0.5
            t2 = tp + hp*0.5
            up, vp = self.plot_st_uv(sp, tp)
            u1, v1 = self.plot_st_uv(s1, t1)
            u2, v2 = self.plot_st_uv(s2, t2)
            if symbol == "dot" :
                u1, v1 = up-1, vp-1
                u2, v2 = up+1, vp+1
                coords = [u1, v1, u2, v1, u2, v2, u1, v2, u1, v1]
            elif symbol == "square" :
                coords = [u1, v1, u2, v1, u2, v2, u1, v2, u1, v1]
            elif symbol == "diamond" :
                coords = [u1, vp, up, v1, u2, vp, up, v2, u1, vp]
            elif symbol == "triangle" :
                coords = [u1, v1, u2, v1, up, v2, u1, v1]
            elif symbol == "itriangle" :
                coords = [u1, v2, u2, v2, up, v1, u1, v2]
            elif symbol == "dash" :
                coords = [u1, vp, u2, vp]
            elif symbol == "pipe" :
                coords = [up, v1, up, v2]
            elif symbol == "plus" :
                coords = [u1, vp, u2, vp]
                plot.create_line(coords, tags=tags)
                coords = [up, v1, up, v2]
            elif symbol == "cross" :
                coords = [u1, v1, u2, v2]
                plot.create_line(coords, tags=tags)
                coords = [u2, v1, u1, v2]
            else :
                print("symbol %s not supported" % (symbol))
                return
            plot.create_line(coords, tags=tags)
    #==========================================================================
    # METHOD  : plot_texv
    # PURPOSE : plot text vector
    # NOTES   :
    #     * sp, tp, hp in st units
    #     * single-character control sequences:
    #        &  greek characters follow
    #        $  script characters follow
    #        ^  super-script
    #        ~  subscript
    #        @  increase character size
    #        #  decrease character size
    #        %  toggle overstrike mode
    #        \  back-space
    #        !  begin two-letter control sequence
    #     * two-letter control sequences:
    #        !0  font family 0
    #        !1  font family 1
    #        !2  font family 2
    #        !3  font family 3
    #        !=  toggle constant spacing mode
    #        !-  toggle connected mode
    #        !|  stretch by 1.2
    #        !~  shrink by 1.2
    #        !.  ignore any following control sequences
    #==========================================================================
    def plot_texv(self, sp, tp, hp, stringp, **kwargs) :
        """ plot a text string.

        **arguments**:

            **sp, tp** (float)

                plot location in scaled coordinates.
                In the scaled domain,
                every point on the canvas is mapped to the window
                smin, smax = 0.0, 1.0 and tmin, tmax = 0.0, 1.0

            **hp** (float)

                size of the text to be drawn in scaled units.

            **stringp** (str)

                the string to label.

                If control_mode is True, the following control sequences are
                respected:

                 * single-character control sequences:

                    * &  greek characters follow

                    * $  script characters follow

                    * ^  super-script

                    * ~  subscript

                    * @  increase character size

                    * #  decrease character size

                    * %  toggle overstrike mode

                    * \  back-space

                    * !  begin two-letter control sequence

                 * two-letter control sequences:

                    * !0  font family 0

                    * !1  font family 1

                    * !2  font family 2

                    * !3  font family 3

                    * !=  toggle constant spacing mode

                    * !-  toggle connected mode

                    * !|  stretch by 1.2

                    * !~  shrink by 1.2

                    * !.  ignore any following control sequences

            **\*\*kwargs** (dict)

               options.

        **options**:

            **tags** (str, default="STRING")

                tk canvas tags to apply to the symbol.

            **rotate** (float, default=0.0)

               The rotation angle in degrees of the string label.

            **slant** (float, default=0.0)

               The slant angle in degrees of the string label.

            **anchor** (str, default="c")

                The alignment of text with respect to sp, tp.  One of:

                "c" : x:centered y: centered

                "n" : x:centered y: north of sp, tp

                "s" : x:centered y: south of sp, tp

                "e" : x:east of sp, tp  y: centered

                "w" : x:west of sp, tp  y: centered

                "ne" : x:east of sp, tp  y: north of sp, tp

                "nw" : x:west of sp, tp  y: north of sp, tp

                "se" : x:east of sp, tp  y: south of sp, tp

                "sw" : x:west of sp, tp  y: south of sp, tp

            **control_mode** (bool, default=True)

                if True, respect control sequences,
                listed in stringp option description

            **single_char** (int, default=-1)

                specify one character in the Hershey font set to be printed,
                an integer between 0 and 1535.

        """
        nschar = PlotBasem._string_data_nchar
        nchar = len(stringp)
        control_chars = ["&", "%", "$", "^", "~", "!", "#", "\"", "@"]
        Anchor = {
            "sw": 0, "w": 1, "nw": 2, "s": 3, "c": 4,
            "n": 5, "se": 6, "e": 7, "ne": 8
        }
        rotate = 0
        slant  = 0
        anchor = "c"
        single_char = -1
        single_mode = False
        control_mode = True
        tags = "STRING"
        for key, value in list(kwargs.items()) :
            if   key == "tags" :
                tags = value
            elif key == "rotate" :
                rotate = value
            elif key == "slant" :
                slant = value
            elif key == "anchor" :
                anchor = value
            elif key == "control_mode" :
                control_mode = value
            elif key == "single_char" :
                single_char = value
                single_mode = True
        #----------------------------------------------------------------------
        # slant:
        #----------------------------------------------------------------------
        slant = slant-180.0*int(slant/180.0)
        if slant >  89.0 and slant <  91.0 :
            slant =  89.0
        if slant < -89.0 and slant > -91.0 :
            slant = -89.0
        #----------------------------------------------------------------------
        # single character mode:
        #----------------------------------------------------------------------
        if single_mode :
            if single_char > nschar or single_char < 1:
                self.fatal("single character index is out of range")
                return
            nchar = 1
            stringp = "x"
        #----------------------------------------------------------------------
        # anchor
        #----------------------------------------------------------------------
        if anchor in Anchor:
            lorg = Anchor[anchor]
        else :
            self.fatal("incorrect anchor specification")
            return
        #----------------------------------------------------------------------
        # fiddler vector string plotting routine
        #----------------------------------------------------------------------
        vstrch = 1.0
        m1 = 21
        m4 = m1/4
        h1 = 1.0*hp/m1
        fa = 4.0*math.atan(1)/180.0
        cr = math.cos(fa*rotate)
        sr = math.sin(fa*rotate)
        ts = math.tan(fa*slant)
        isx = 0
        isy = -(m1/2)*(lorg%3)
        plot = self._Component["plot"]
        coords = []
        for xpass in [1, 2] :
            isx     = -(isx/2)*(lorg/3)
            fcont   = control_mode
            fxpt    = False
            fscript = False
            fover   = False
            fgreek  = False
            fconst  = False
            fconne  = False
            nfont   = 0
            nsups   = 0
            nsize   = m4
            h2      = h1
            for c in stringp :
                fskip = False
                if fcont and (fxpt or (c in control_chars)) :
                    fskip = True
                    if fxpt :
                        fxpt = False
                        if c in ["0", "1", "2", "3"] :
                            nfont = int(c)
                        elif c == "=" :
                            fconst = not fconst
                        elif c == "-" :
                            fconne = not fconne
                        elif c == "|" :
                            vstrch *= 1.2
                        elif c == "~" :
                            vstrch *= 0.8
                        elif c == "." :
                            fcont = False
                        else :
                            fskip = False
                    else :
                        if   c == "&" :
                            fgreek = not fgreek
                        elif c == "$" :
                            fscript = not fscript
                        elif c == "%" :
                            fover = not fover
                            if fover is False :
                                c = " "
                                fskip = False
                        elif c == "!" :
                            fxpt = True
                        elif c == "^" :
                            nsups += 1
                        elif c == "~" :
                            nsups -= 1
                        elif c == "\"" :
                            isx -= nsize
                        elif c == "@" :
                            nsize += 1
                            h2 = h1*1.0*nsize/m4
                        elif c == "#" :
                            nsize -= 1
                            h2 = h1*1.0*nsize/m4
                if fskip :
                    continue
                ic = PlotBasem._string_data_code[c] + 1 + nfont*(96*3)
                if fgreek :
                    ic += 96
                elif fscript :
                    ic += 192
                if ic > nschar or ic < 1 :
                    ic = 11
                if single_mode :
                    ic = single_char

                j1 = PlotBasem._string_data_fo[ic]
                j2 = j1
                if ic < nschar :
                    j2 = PlotBasem._string_data_fo[ic+1]
                ixhi = 0
                for j in range(j1, j2) :
                    idx = PlotBasem._string_data_fx[j]
                    if idx < 0 :
                        idx = -(idx + 1)
                    ixhi = max(ixhi, idx)
                if j2 == j1 :
                    ixhi = m1

                if xpass == 2 :
                    x0 = h1*isx
                    y0 = h1*(isy+nsups*nsize*3)
                    for j in range(j1, j2) :
                        idx = PlotBasem._string_data_fx[j]
                        idy = PlotBasem._string_data_fy[j]
                        fdraw = True
                        if idx < 0 :
                            fdraw = False
                            idx = -(idx + 1)
                        if fconst :
                            idx += (m1-ixhi)/2
                        ys = y0 + h2*idy*vstrch
                        xs = x0 + h2*idx + ts*ys
                        s  = sp + xs*cr - ys*sr
                        t  = tp + ys*cr + xs*sr
                        u, v = self.plot_st_uv(s, t)
                        if fdraw :
                            coords.extend([u, v])
                        else :
                            if coords :
                                plot.create_line(coords, tags=tags)
                            coords = [u, v]
                if fover:
                    continue
                if fconst:
                    isx += (m1*nsize)/m4
                    if not fconne :
                        isx += nsize
                else :
                    isx += (ixhi*nsize)/m4
                    if not fconne :
                        isx += nsize
        if coords :
            plot.create_line(coords, tags=tags)
###############################################################################
# CLASS   : PlotBasem_annotate_dialog
# PURPOSE : dialog for adding plot annotation
###############################################################################
class PlotBasem_annotate_dialog(object):
    #==========================================================================
    # METHOD  : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, parent, x1, y1):
        self._parent = parent
        self._shape = None
        self._text  = ""
        self._Component = {}
        self._Component["shape_var"] = tk.StringVar()
        self._Component["shape_var"].set("NONE")
        #----------------------------------------------------------------------
        # toplevel
        #----------------------------------------------------------------------
        top = tk.Toplevel(parent)
        top.protocol('WM_DELETE_WINDOW', self.__wm_delete_window)
        top.option_add("*Dialog*Entry.width", 40)
        self._Component["top"] = top
        #----------------------------------------------------------------------
        # top text
        #----------------------------------------------------------------------
        tf = tk.Frame(top, bd=2, relief="raised")
        tf.pack(side="top", fill="both")
        tm = tk.Message(tf, justify="left", aspect=400, text="Annotate Plot:")
        tm.pack(side="right", expand=True, fill="both", padx=10, pady=10)
        tb = tk.Label(tf, bitmap="question")
        tb.pack(side="left", padx=3, pady=3)
        #----------------------------------------------------------------------
        # middle value frame, entry
        #----------------------------------------------------------------------
        mvf = tk.Frame(top, bd=2, relief="raised")
        mvf.pack(side="top", fill="both")
        mvf_e = tk.Entry(mvf, relief="sunken")
        mvf_e.pack(side="top", fill="x", expand=True, padx=10, pady=10)
        self._Component["value"] = mvf_e
        #----------------------------------------------------------------------
        # middle format frame, buttons
        #----------------------------------------------------------------------
        mff= tk.Frame(top, bd=2, relief="raised")
        mff.pack(side="top", fill="both", expand=True)
        mff_clr= tk.Button(mff, text="clear", highlightthickness=0, anchor="w")
        mff_clr.pack(side="left", fill=None, expand=False)
        mff_x= tk.Button(mff, text="x", highlightthickness=0, anchor="w")
        mff_x.pack(side="left", fill=None, expand=False)
        mff_y= tk.Button(mff, text="y", highlightthickness=0, anchor="w")
        mff_y.pack(side="left", fill=None, expand=False)
        mff_xy= tk.Button(mff, text="(x,y)", highlightthickness=0, anchor="w")
        mff_xy.pack(side="left", fill=None, expand=False)
        #----------------------------------------------------------------------
        # middle format entry
        #----------------------------------------------------------------------
        mff_e= tk.Entry(mff, relief="sunken", width=5)
        mff_e.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        mff_e.delete(0, "end")
        mff_e.insert(0, "%.5g")
        self._Component["format"] = mff_e

        def clr_cmd(self=self):
            self._Component["value"].delete(0, "end")
        def ann_x_cmd(self=self) :
            self._annotate_dialog_pt(x1)
        def ann_y_cmd(self=self) :
            self._annotate_dialog_pt(y1)
        def ann_xy_cmd(self=self) :
            self._annotate_dialog_pt(x1, y1)

        mff_clr["command"] = clr_cmd
        mff_x["command"]   = ann_x_cmd
        mff_y["command"]   = ann_y_cmd
        mff_xy["command"]  = ann_xy_cmd
        #----------------------------------------------------------------------
        # middle shape frame, radio-buttons
        #----------------------------------------------------------------------
        msf = tk.Frame(top, bd=2, relief="raised")
        msf.pack(side="top", fill="both", expand=True)
        msf_none = tk.Radiobutton(msf, text="none",
            compound="left", image=PlotBasem._bm_ann_none,
            variable=self._Component["shape_var"], value="NONE",
            highlightthickness=0, anchor="w")
        msf_none.pack(side="top", fill="x", expand=True)
        msf_line = tk.Radiobutton(msf, text="line-segment",
            compound="left", image=PlotBasem._bm_ann_line,
            variable=self._Component["shape_var"], value="LINE",
            highlightthickness=0, anchor="w")
        msf_line.pack(side="top", fill="x", expand=True)
        msf_arrow_to = tk.Radiobutton(msf, text="arrow to first point",
            compound="left", image=PlotBasem._bm_ann_arrow_left,
            variable=self._Component["shape_var"], value="ARROW-TO",
            highlightthickness=0, anchor="w")
        msf_arrow_to.pack(side="top", fill="x", expand=True)
        msf_arrow_from = tk.Radiobutton(msf, text="arrow from first point",
            compound="left", image=PlotBasem._bm_ann_arrow_right,
            variable=self._Component["shape_var"], value="ARROW-FROM",
            highlightthickness=0, anchor="w")
        msf_arrow_from.pack(side="top", fill="x", expand=True)
        msf_arrow_both = tk.Radiobutton(msf, text="arrow to both points",
            compound="left", image=PlotBasem._bm_ann_arrow_both,
            variable=self._Component["shape_var"], value="ARROW-BOTH",
            highlightthickness=0, anchor="w")
        msf_arrow_both.pack(side="top", fill="x", expand=True)
        msf_rectangle = tk.Radiobutton(msf, text="rectangle",
            compound="left", image=PlotBasem._bm_ann_rect,
            variable=self._Component["shape_var"], value="RECTANGLE",
            highlightthickness=0, anchor="w")
        msf_rectangle.pack(side="top", fill="x", expand=True)
        msf_filled_rectangle = tk.Radiobutton(msf, text="filled rectangle",
            compound="left", image=PlotBasem._bm_ann_frect,
            variable=self._Component["shape_var"], value="FILLED-RECTANGLE",
            highlightthickness=0, anchor="w")
        msf_filled_rectangle.pack(side="top", fill="x", expand=True)
        #----------------------------------------------------------------------
        # accept and cancel buttons
        #----------------------------------------------------------------------
        def accept_cmd(self=self) :
            self.__done(cancel=False)
        def cancel_cmd(self=self):
            self.__done(cancel=True)
        def accept_bind_cmd(event, self=self) :
            self.__done(cancel=False)
        def cancel_bind_cmd(event, self=self):
            self.__done(cancel=True)
        bf = tk.Frame(top, bd=2, relief="raised")
        bf.pack(side="top", fill="both")
        bf_cancel = tk.Frame(bf, bd=2, relief="sunken")
        bf_cancel.pack(side="left", expand=True, padx=3, pady=2)
        bf_cancel_button = tk.Button(bf_cancel, text="cancel", command=cancel_cmd)
        bf_cancel_button.pack(anchor="c", expand=True, padx=3, pady=2)
        bf_accept = tk.Frame(bf, bd=2, relief="sunken")
        bf_accept.pack(side="left", expand=True, padx=3, pady=2)
        bf_accept_button = tk.Button(bf_accept, text="accept", command=accept_cmd)
        bf_accept_button.pack(anchor="c", expand=True, padx=3, pady=2)
        self._Component["cancel"] = bf_cancel_button
        self._Component["accept"] = bf_accept_button
        #----------------------------------------------------------------------
        # key bindings
        #----------------------------------------------------------------------
        self._Component["value"].bind("<Control-Key-q>", cancel_bind_cmd)
        self._Component["value"].bind("<Control-Key-s>", accept_bind_cmd)
        self._Component["value"].bind("<Return>",        accept_bind_cmd)

        self._set_transient()
    #==========================================================================
    # METHOD  : _set_transient
    # PURPOSE : determine window placement
    #==========================================================================
    def _set_transient(self, relx=0.5, rely=0.3):
        parent = self._parent
        widget = self._Component["top"]
        widget.withdraw() # Remain invisible while we figure out the geometry
        widget.transient(parent)
        widget.update_idletasks() # Actualize geometry information
        if parent.winfo_ismapped():
            m_width = parent.winfo_width()
            m_height = parent.winfo_height()
            m_x = parent.winfo_rootx()
            m_y = parent.winfo_rooty()
        else:
            m_width = parent.winfo_screenwidth()
            m_height = parent.winfo_screenheight()
            m_x = m_y = 0
        w_width = widget.winfo_reqwidth()
        w_height = widget.winfo_reqheight()
        x = m_x + (m_width - w_width) * relx
        y = m_y + (m_height - w_height) * rely
        if x+w_width > parent.winfo_screenwidth():
            x = parent.winfo_screenwidth() - w_width
        elif x < 0:
            x = 0
        if y+w_height > parent.winfo_screenheight():
            y = parent.winfo_screenheight() - w_height
        elif y < 0:
            y = 0
        widget.geometry("+%d+%d" % (x, y))
        widget.deiconify() # Become visible at the desired location
    #==========================================================================
    # METHOD  : go
    # PURPOSE : post dialog, return results
    #==========================================================================
    def go(self):
        top = self._Component["top"]
        top.wait_visibility()
        top.grab_set()
        top.mainloop()
        top.grab_release()
        top.destroy()
        return [self._shape, self._text]
    #==========================================================================
    # METHOD  : __done
    # PURPOSE : cancel or accept call-back
    #==========================================================================
    def __done(self, cancel=False):
        if cancel :
            self._text  = ""
            self._shape = None
        else :
            self._text  = self._Component["value"].get()
            self._shape = self._Component["shape_var"].get()
        self._Component["top"].quit()
        self._Component["top"].destroy()
    #==========================================================================
    # METHOD  : __wm_delete_window
    # PURPOSE : call-back for when window is deleted
    #==========================================================================
    def __wm_delete_window(self):
        self.__done(cancel=True)
    #==========================================================================
    # METHOD  : _annotate_dialog_pt
    # PURPOSE : annotate dialog box update entry box with x, y
    #==========================================================================
    def _annotate_dialog_pt(self, a, b="") :
        value_entry  = self._Component["value"]
        format_entry = self._Component["format"]
        x   = value_entry.get()
        fmt = format_entry.get()
        try :
            s = fmt % (-1.0e-2)
        except :
            fmt = "%.5g"
            format_entry.delete(0, "end")
            format_entry.insert(0, fmt)
        if x :
            value_entry.insert("end", " ")
        if b == "" :
            value_entry.insert("end", fmt % (a))
        else :
            a = fmt % (a)
            b = fmt % (b)
            value_entry.insert("end", "(" + a + ", " + b + ")")
