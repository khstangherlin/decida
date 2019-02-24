################################################################################
# CLASS    : SmithChartx
# PURPOSE  : Smith Chart plot
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:25:14 2013
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
from builtins import str
from builtins import range
import sys
import math
import tkinter as tk
import six
from decida.PlotBasem import PlotBasem
from decida.Data import Data
from decida.SelectionDialog import SelectionDialog

class SmithChartx(PlotBasem) :
    """
    **synopsis**:

        Plot s-parameter data on a Smith chart.

        *SmithChartx* plots s-parameter on a Smith chart.  The Smith chart
        grid is normalized impedance and/or admittance.  The grid can be
        extended beyond the unit circle.

    **constructor arguments**:

        **parent** (tk handle, default=None)

              handle of frame or other widget to pack plot in.
              if this is not specified, top-level is created.

        **\*\*kwargs** (dict)

              keyword=value specifications:
              options or configuration-options

    **options**:

        **command** (list)

              list of pairs of data-object, string of freq, RE(s1), IM(s1),
              ?RE(s2), IM(s2), ...?  columns
              (frequency, and real, imaginary vectors)

              example: [d1, "freq RE(s11) IM(s11)", d2, "freq RE(s11) IM(s11)"]:
                 s11 curves will be plotted for each data object d1 and d2.
                 Each curve will also be plotted
                 with color, symbol, symbol-size, line-width, and
                 trace-direction selected from the successive item in
                 the respective list of specified configured options:
                 colors, symbols, ssizes, wlines, traces.  Selection
                 wraps around if the respective list is shorter than
                 the number of curves.

    **configuration options**:

        **verbose** (bool, default=False)

              enable/disable verbose mode

        **title** (str, default="")

              main title

        **xtitle** (str, default="")

              x-axis title

        **ytitle** (str, default="")

              y-axis title

        **plot_height** (str, default="10i" for MacOS, else "7i")

              Height of plot window (Tk inch  or pixelspecification)

        **plot_width** (str, default="10i" for MacOS, else "7i")

              Width of plot window (Tk inch or pixel specification)

        **plot_background** (str, default="GhostWhite")

              Background color of plot window

        **legend_background** (str, default="AntiqueWhite2")

              Background color of legend

        **grid_color** (str, default="black")

              Color of Smith Chart grid.

        **unit_color** (str, default="#eeeeff")

              Color of Smith Chart unit-circle.

        **unit_width** (int, default=4)

              Width of Smith Chart unit-circle outline.

        **resistance_list** (list of float, default=[
                  0.1, 0.2, 0.3, 0.5, 0.7, 1, 1.5, 2, 3, 5, 10])

              list of normalized resistance values to form grid of Smith Chart.

        **reactance_list** (list of float, default=[
                  0.1, 0.2, 0.3, 0.5, 0.7, 1, 1.5, 2, 3, 5, 10])

              list of normalized reactance values to form grid of Smith Chart.

        **colors** (list of str, default=[
                "blue", "red", "green", "orange", "cyan",
                "brown", "black", "blue violet", "cadet blue",
                "dark cyan", "dark goldenrod", "dark green",
                "dark magenta", "dark olive green", "dark orange",
                "dark red", "dark slate blue", "dark slate gray",
                "dodger blue", "forest green", "steel blue", "sienna"])

              list of colors for curves.
              Used to populate color menu, and to specify curve colors
              in scripted "command" option.

        **symbols** (list of str, default=[
                "none", "dot", "square", "diamond",
                "triangle", "itriangle",
                "dash", "pipe", "plus", "cross",
                "spade", "heart", "diam", "club", "shamrock",
                "fleurdelis", "circle", "star"])

              list of symbols for curves.
              Used to populate symbol menu, and to specify curve symbols
              in scripted "command" option.

        **ssizes** (list of float, default = [0.01])

              list of symbol sizes for curves.
              Used to specify curve symbol sizes
              in scripted "command" option.

        **wlines** (list of int, default = [1])

              list of line widths for curves.
              Used to specify curve line widths
              in scripted "command" option.

        **traces** (list, default = ["increasing"])

              list of traces for curves.  each trace can be one of:
              "increasing", "decreasing", or "both".
              Used to specify curve trace directions
              in scripted "command" option.

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

        **grid**  (bool, default=True)

              if True, show grid on plot

        **legend** (bool, default=True)

              if True, show legend on plot

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

    **example** (from test_SmithChartx_2): ::

        from decida.Data import Data
        from decida.SmithChartx import SmithChartx

        d = Data()
        d.read("spars.col")
        h=SmithChartx(None, command=[d, "freq REAL(Sdd11) IMAG(Sdd11) REAL(Sdd22) IMAG(Sdd22) REAL(Sdd12) IMAG(Sdd12)"], symbols=["dot"])

    **public methods**:

        * public methods from *ItclObjectx*

        * public methods from *PlotBasem* (2-dimensinal plot base class)

    """
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # SmithChartx main
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, parent=None, **kwargs) :
        PlotBasem.__init__(self, parent=parent, use_matplotlib=False)
        #----------------------------------------------------------------------
        # private variables:
        #----------------------------------------------------------------------
        #----------------------------------------------------------------------
        # configuration options
        #----------------------------------------------------------------------
        self["xmin"]        = -1
        self["xmax"]        =  1
        self["ymin"]        = -1
        self["ymax"]        =  1
        if sys.platform == "darwin" :
            self["plot_height"] = "10i"
            self["plot_width"]  = "10i"
        else :
            self["plot_height"] = "7i"
            self["plot_width"]  = "7i"
        self["traces"]      = ["both"]
        self._add_options({
            "grid_color"      : ["black",   None],
            "unit_color"      : ["#eeeeff", None],
            "unit_width"      : [4, None],
            "resistance_list" : [[0.1, 0.2, 0.3, 0.5, 0.7, 1, 1.5, 2, 3, 5, 10], None],
            "reactance_list"  : [[0.1, 0.2, 0.3, 0.5, 0.7, 1, 1.5, 2, 3, 5, 10], None],
        })
        #----------------------------------------------------------------------
        # keyword arguments are *not* all configuration options
        #----------------------------------------------------------------------
        for key, value in list(kwargs.items()) :
            if key == "command" :
                command = value
            else :
                self[key] = value
        #----------------------------------------------------------------------
        # save smithchart data
        #----------------------------------------------------------------------
        datobj = None
        idata  = 0
        self.__ssets = []
        self.__sset_dname = {}
        self.__sset_fdcol = {}
        self.__sset_rdcol = {}
        self.__sset_idcol = {}
        self.__sset_fdata = {}
        self.__sset_rdata = {}
        self.__sset_idata = {}
        for item in command :
            if isinstance(item, Data) :
                idata += 1
                datobj = item
                dname = "data_%d" % (idata)
                i     = 0
            elif isinstance(item, six.string_types) :
                cols = item.split()
                i += 1
                if i == 1:
                    fcol = cols.pop(0)
                for col in cols :
                    i += 1
                    if i % 2 == 0 :
                        rcol = col
                    else :
                        icol = col
                        sset = "%s:%s_%s_%s" % (dname, rcol, icol, fcol)
                        self.__ssets.append(sset)
                        self.__sset_dname[sset] = dname
                        self.__sset_fdcol[sset] = fcol
                        self.__sset_rdcol[sset] = rcol
                        self.__sset_idcol[sset] = icol
                        self.__sset_fdata[sset] = datobj.get(fcol)
                        self.__sset_rdata[sset] = datobj.get(rcol)
                        self.__sset_idata[sset] = datobj.get(icol)
        self._smithchart_recalc(new=True)
        #----------------------------------------------------------------------
        # build gui:
        #----------------------------------------------------------------------
        self._gui()
        self._mainloop()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # SmithChartx configuration option callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # SmithChartx GUI
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _gui
    # PURPOSE : build graphical user interface
    #==========================================================================
    def _gui(self) :
        self._Component["smithchart_extended_var"] = tk.IntVar()
        self._Component["smithchart_extended_var"].set(0)
        self._Component["smithchart_impedance_var"] = tk.IntVar()
        self._Component["smithchart_impedance_var"].set(1)
        PlotBasem._gui(self)
        func0 = self._Component["func0"]
        func1 = self._Component["func1"]
        func0.configure(text="Extended",
            command=self._grid_cmd,
            variable=self._Component["smithchart_extended_var"])
        func1.configure(text="Impedence",
            command=self._grid_cmd,
            variable=self._Component["smithchart_impedance_var"])
        edit_menu = self._Component["edit_menu"]
        end = edit_menu.index("end")
        keeps = ("Settings", "Delete current curve")
        dels = []
        for index in range(0, end+1) :
            try :
                lab = edit_menu.entryconfig(index, "label")[4]
                if isinstance(lab, tuple):
                    lab = " ".join(lab)
                if lab not in keeps :
                    dels.append(lab)
            except :
                pass
        for item in dels :
            edit_menu.delete(item)
    #==========================================================================
    # METHOD  : _smithchart_recalc
    # PURPOSE : recalculate
    #==========================================================================
    def _smithchart_recalc(self, new=False) :
        for sset in self.__ssets :
            dname = self.__sset_dname[sset]
            fcol  = self.__sset_fdcol[sset]
            rcol  = self.__sset_rdcol[sset]
            icol  = self.__sset_idcol[sset]
            fdata = self.__sset_fdata[sset]
            rdata = self.__sset_rdata[sset]
            idata = self.__sset_idata[sset]
            dsmith = Data()
            dsmith.read_inline(fcol, fdata, rcol, rdata, icol, idata)
            # if input data is admittance or impedance, convert to s-parameter
            if new :
                self.add_curve(dsmith, rcol, icol, dname=dname)
            else :
                curve = "%s_:_%s_%s_vs_%s" % (dname, rcol, icol, fcol)
                self._curve_xdata[curve] = dsmith.get(rcol)
                self._curve_ydata[curve] = dsmith.get(icol)
    #==========================================================================
    # METHOD  : _smithchart_text
    # PURPOSE : place text on smithchart
    #==========================================================================
    def _smithchart_text(self, u, v, text, tags) :
        plot = self._Component["plot"]
        sid = plot.create_text(u, v, text=text, tags=tags)
        plot.create_rectangle(plot.bbox(sid), fill="white", outline="white", tags=tags)
        plot.lift(sid)
    #==========================================================================
    # METHOD  : _smithchart_grid
    # PURPOSE : plot smithchart grid
    #==========================================================================
    def _smithchart_grid(self) :
        plot = self._Component["plot"]
        ul, uh, vl, vh = self.plot_transform_entry("uv_max_limits")
        um, vm = self.plot_xy_uv(-1, -1)
        uo, vo = self.plot_xy_uv( 0,  0)
        up, vp = self.plot_xy_uv( 1,  1)
        plot.create_oval(um, vm, up, vp, tags="UNIT")
        plot.create_line(um, vo, up, vo, tags="AXIS")
        plot.create_line(um, vo, ul, vo, tags="AXIS-EXTEND")
        plot.create_line(up, vo, uh, vo, tags="AXIS-EXTEND")
        for r in self["resistance_list"] :
            r = float(r)
            rad = 1.0/(1.0+r)
            u1, v1 = self.plot_xy_uv( 1.0-2.0*rad,  rad)
            u2, v2 = self.plot_xy_uv(-1.0+2.0*rad, -rad)
            plot.create_oval(up, v1, u1, v2, tags=("GRID", "Z-GRID"))
            self._smithchart_text(u1, vo, text=str(r), tags="Z-LABEL")
            plot.create_oval(um, v1, u2, v2, tags=("GRID", "Y-GRID"))
            self._smithchart_text(u2, vo, text=str(r), tags="Y-LABEL")
        for x in self["reactance_list"] :
            x = float(x)
            rad = 1.0/x
            rho = 2.0/(1.0+x*x)
            ud, vd = self.plot_xy_uv( 2.0*rad, -2.0*rad)
            u1, v1 = self.plot_xy_uv( 1.0+rad, -2.0*rad)
            u2, v2 = self.plot_xy_uv(-1.0+rad, -2.0*rad)
            u3, v3 = self.plot_xy_uv( 1.0-rho,  x*rho)
            u4, v4 = self.plot_xy_uv(-1.0+rho, -x*rho)
            ep = abs(90.0*math.atan(x)/math.atan(1.0))
            em = 360.0-ep
            duZ = u1 - ud
            duY = u2 - ud
            dvH = vo - vd
            dvL = v1 - vd
            plot.create_arc(uo+duZ, vo+dvH, ud+duZ, vd+dvH, start=-90, extent=-ep,
                style="arc", tags=("GRID", "Z-GRID"))
            plot.create_arc(uo+duZ, vo+dvL, ud+duZ, vd+dvL, start=90,  extent=ep,
                style="arc", tags=("GRID", "Z-GRID"))
            plot.create_arc(uo+duZ, vo+dvH, ud+duZ, vd+dvH, start=-90, extent=em,
                style="arc", tags=("GRID", "Z-GRID-EXTEND"))
            plot.create_arc(uo+duZ, vo+dvL, ud+duZ, vd+dvL, start=90,  extent=-em,
                style="arc", tags=("GRID", "Z-GRID-EXTEND"))
            self._smithchart_text(u3, v3, text=str(x),  tags="Z-LABEL")
            self._smithchart_text(u3, v4, text=str(-x), tags="Z-LABEL")
            plot.create_arc(uo+duY, vo+dvH, ud+duY, vd+dvH, start=-90, extent=ep,
                style="arc", tags=("GRID", "Y-GRID"))
            plot.create_arc(uo+duY, vo+dvL, ud+duY, vd+dvL, start=90,  extent=-ep,
                style="arc", tags=("GRID", "Y-GRID"))
            plot.create_arc(uo+duY, vo+dvH, ud+duY, vd+dvH, start=-90, extent=-em,
                style="arc", tags=("GRID", "Y-GRID-EXTEND"))
            plot.create_arc(uo+duY, vo+dvL, ud+duY, vd+dvL, start=90,  extent=em,
                style="arc", tags=("GRID", "Y-GRID-EXTEND"))
            self._smithchart_text(u4, v3, text=str(-x), tags="Y-LABEL")
            self._smithchart_text(u4, v4, text=str(x),  tags="Y-LABEL")
        self._grid_cmd()
    #==========================================================================
    # METHOD  : _plot_redraw
    # PURPOSE : (over-ride) redraw whenever plot limits, curves are changed, etc.
    #==========================================================================
    def _plot_redraw(self, redraw_reason="none") :
        plot = self._Component["plot"]
        self._plot_transform_calc()
        plot.delete("all")
        self._plot_title()
        self._smithchart_grid()
        self._grid_cmd()
        self._plot_curves()
        self._plot_annotations()
        self._update_limit_display()
        self._plot_legend()
        self._lgnd_cmd()
    #==========================================================================
    # METHOD  : _grid_cmd
    # PURPOSE : (over-ride) grid check-button call-back
    #==========================================================================
    def _grid_cmd(self) :
        plot = self._Component["plot"]
        if self._Component["grid_var"].get() :
            plot.itemconfigure("GRID", state="normal")
        else :
            plot.itemconfigure("GRID", state="hidden")
            return
        extended  = self._Component["smithchart_extended_var"].get()
        impedance = self._Component["smithchart_impedance_var"].get()
        plot.itemconfigure("UNIT", width=self["unit_width"],
            outline=self["grid_color"], fill=self["unit_color"])
        plot.itemconfigure("GRID", width=1, outline=self["grid_color"])
        plot.itemconfigure("AXIS", width=1, fill=self["grid_color"])
        plot.itemconfigure("AXIS-EXTEND", width=1, fill=self["grid_color"])
        if impedance == 1 :
            plot.itemconfigure("Z-GRID",  state="normal")
            plot.itemconfigure("Z-LABEL", state="normal")
            plot.itemconfigure("Y-GRID",  state="hidden")
            plot.itemconfigure("Y-LABEL", state="hidden")
        else :
            plot.itemconfigure("Z-GRID",  state="hidden")
            plot.itemconfigure("Z-LABEL", state="hidden")
            plot.itemconfigure("Y-GRID",  state="normal")
            plot.itemconfigure("Y-LABEL", state="normal")
        if extended == 1 :
            plot.itemconfigure("AXIS-EXTEND", state="normal")
            if impedance == 1 :
                plot.itemconfigure("Z-GRID-EXTEND", state="normal")
                plot.itemconfigure("Y-GRID-EXTEND", state="hidden")
            else :
                plot.itemconfigure("Z-GRID-EXTEND", state="hidden")
                plot.itemconfigure("Y-GRID-EXTEND", state="normal")
        else :
            plot.itemconfigure("AXIS-EXTEND",   state="hidden")
            plot.itemconfigure("Z-GRID-EXTEND", state="hidden")
            plot.itemconfigure("Y-GRID-EXTEND", state="hidden")
        plot.lower("UNIT")
        if impedance == 1 :
            plot.lift("Z-LABEL")
        else :
            plot.lift("Y-LABEL")
    #==========================================================================
    # METHOD  : _settings_cmd
    # PURPOSE : (override) settings via entrytable-select
    # NOTES   :
    #     * specs: type, blurb, items
    #     * entry: key, label, value
    #==========================================================================
    def _settings_cmd(self) :
        curve     = self.current_curve()
        wline     = self._curve_wline[curve]
        rlist     = " ".join([str(r) for r in self["resistance_list"]])
        xlist     = " ".join([str(x) for x in self["reactance_list"]])
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
              ]
          ],
          ["entry", "Colors", [
                 ["plot_bg",     "plot background",   self["plot_background"] ],
                 ["lgnd_bg",     "legend background", self["legend_background"] ],
                 ["grid_color",  "grid color",        self["grid_color"] ],
                 ["unit_color",  "unit circle color", self["unit_color"] ],
                 ["unit_width",  "unit circle width", self["unit_width"] ],
              ]
          ],
          ["entry", "Smith Chart:", [
                 ["rlist",       "resistance list",   rlist],
                 ["xlist",       "reactance list",    xlist],
              ]
          ],
          ["entry", "Current Curve: " + curve, [
                 ["wline",       "Line width",   wline],
              ]
          ],
        ]
        sd = SelectionDialog(self, title="Plot Settings", guispecs=specs)
        V = sd.go()
        if V["ACCEPT"] :
            self["title"]             = V["title"]
            self["plot_background"]   = V["plot_bg"]
            self["legend_background"] = V["lgnd_bg"]
            self["grid_color"]        = V["grid_color"]
            self["unit_color"]        = V["unit_color"]
            self["unit_width"]        = V["unit_width"]
            self._curve_wline[curve]  = int(V["wline"])
            self["resistance_list"]   = [float(r) for r in V["rlist"].split()]
            self["reactance_list"]    = [float(x) for x in V["xlist"].split()]
            # self._smithchart_recalc()
            self._plot_redraw()
