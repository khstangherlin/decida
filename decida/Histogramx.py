################################################################################
# CLASS    : Histogramx
# PURPOSE  : histogram
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:20:58 2013
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
from builtins import zip
from builtins import range
import six
import numpy
from decida.PlotBasem import PlotBasem
from decida.Data import Data
from decida.SelectionDialog import SelectionDialog

class Histogramx(PlotBasem) :
    """
    **synopsis**:

        Plot histogram of vector values.

        *Histogramx* plots a histogram of counts of a 1-dimensional array
        of values.  For each data value, if it is within the range of a
        particular histogram bin, that bin's count is incremented.

        The set of histogram bins are specified by configuration options,
        but can be changed by using the Edit->Settings dialog.

    **constructor arguments**:

        **parent** (tk handle, default=None)

              handle of frame or other widget to pack plot in.
              if this is not specified, top-level is created.

        **\*\*kwargs** (dict)

              keyword=value specifications:
              options or configuration-options

    **options**:

        **command** (list)

              list of pairs of data-object, string of x, ?x1, x2, ...? columns

              example: [d1, "x x1 x2", d2, "x x1 x2"]:
                 x, x1, and x2 histograms will be plotted for each
                 data object d1 and d2.  Each histogram will also be
                 plotted with color selected from the successive item in
                 the list of specified colors configuration option.
                 Selection wraps around if the respective list is shorter
                 than the number of curves.

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

              Height of plot window (Tk inch  or pixelspecification)

        **plot_width**  (str, default="10i" for MacOS, else "6i")

              Width of plot window (Tk inch or pixel specification)

        **plot_background** (str, default="GhostWhite")

              Background color of plot window

        **legend_background** (str, default="AntiqueWhite2")

              Background color of legend

        **nbins** (int, default=21)

              number of histogram bins between binorigin and nbins*binsize.

        **binsize** (float, default=1.0)

              size of each histogram bin.

        **binorigin** (float, default=0.0)

              minimum of histogram bins.

        **bar_width** (float, default=1.0)

              width of each histogram bar.

        **bar_outline** (str, default="black")

              color or each histogram bar.

        **colors** (list of str, default = [
                "blue", "red", "green", "orange", "cyan",
                "brown", "black", "blue violet", "cadet blue",
                "dark cyan", "dark goldenrod", "dark green",
                "dark magenta", "dark olive green", "dark orange",
                "dark red", "dark slate blue", "dark slate gray",
                "dodger blue", "forest green", "steel blue", "sienna"])

              list of colors for curves.
              Used to populate color menu, and to specify curve colors
              in scripted "command" option.

        **symbols** (list of str, default = [
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

        **xmin**  (float, default=0.0)

              xaxis minimum

        **xmax**  (float, default=0.0)

              xaxis maximum

        **ymin**  (float, default=0.0)

              yaxis minimum

        **ymax**  (float, default=0.0)

              yaxis maximum

        **grid**  (bool, default=True)

              if true, show grid on plot

        **legend**  (bool, default=True)

              if true, show legend on plot

        **postscript**  (bool, default=False)

              if true, generate a PostScript file.

        **postscript_file** (str, default="plot.ps")

              name of PostScript file to plot to

        **wait** (bool, default=False)

              wait in main-loop until window is destroyed.

        **destroy** (bool, default=False)

              destroy main window after it has been displayed.
              useful for displaying, generating PostScript, then
              destroying window.

    **example** (from test_Histogramx_1): ::

        from decida.Data import Data
        from decida.Histogramx import Histogramx
        d = Data()
        d.read("smartspice_tr_binary.raw")
        h=Histogramx(None, command=[d, "v(cint)"], nbins=51)

    **public methods**:

        * public methods from *PlotBasem* (2-dimensinal plot base class)

    """
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Histogramx main
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
        self._add_options({
            "nbins"          : [21, self._config_nbins_callback],
            "binsize"        : [1.0, self._config_binsize_callback],
            "binorigin"      : [0.0, None],
            "bar_width"      : [1.0, None],
            "bar_outline"    : ["black", None],
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
        # save histogram data
        #----------------------------------------------------------------------
        datobj = None
        idata  = 0
        self.__hsets = []
        self.__hset_dname = {}
        self.__hset_dcol  = {}
        self.__hset_data  = {}
        for item in command :
            if isinstance(item, Data) :
                idata += 1
                datobj = item
                dname = "data_%d" % (idata)
            elif isinstance(item, six.string_types):
                cols = item.split()
                for col in cols:
                    hset = "%s:%s" % (dname, col)
                    self.__hsets.append(hset)
                    self.__hset_dname[hset] = dname
                    self.__hset_dcol[hset]  = col
                    self.__hset_data[hset]  = datobj.get(col)
        self._histogram_rebin(new=True)
        #----------------------------------------------------------------------
        # build gui:
        #----------------------------------------------------------------------
        self._gui()
        self._mainloop()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Histogramx configuration option callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _config_nbins_callback
    # PURPOSE : number of histogram bins
    #==========================================================================
    def _config_nbins_callback(self) :
        nbins = self["nbins"]
        if nbins <= 0:
            self.warning("number of bins must be > 0")
            return False
        return True
    #==========================================================================
    # METHOD  : _config_binsize_callback
    # PURPOSE : size of histogram bins
    #==========================================================================
    def _config_binsize_callback(self) :
        binsize = self["binsize"]
        if binsize <= 0.0:
            self.warning("bin size must be > 0")
            return False
        return True
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Histogramx GUI
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _gui
    # PURPOSE : build graphical user interface
    #==========================================================================
    def _gui(self) :
        PlotBasem._gui(self)
        func0 = self._Component["func0"]
        func1 = self._Component["func1"]
        func0.configure(text="", command="", variable="")
        func1.configure(text="", command="", variable="")
        symb_menu = self._Component["symb_menu"]
        edit_menu = self._Component["edit_menu"]
        for symbol in self["symbols"] :
            symb_menu.delete(symbol)
        end = edit_menu.index("end")
        keeps = ("Settings", "Autoscale y", "Autoscale x", "Autoscale both",
            "Delete current curve")
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
    # METHOD  : _histogram_rebin
    # PURPOSE : recalculate bins
    #==========================================================================
    def _histogram_rebin(self, new=False) :
        #----------------------------------------------------------------------
        # find minimum, maximum of all histogram data
        #----------------------------------------------------------------------
        hmin = None
        hmax = None
        start = True
        for hset in self.__hsets:
            hmin1 = numpy.min(self.__hset_data[hset])
            hmax1 = numpy.max(self.__hset_data[hset])
            if start :
                hmin = hmin1
                hmax = hmax1
                start = False
            else :
                hmin = min(hmin, hmin1)
                hmax = max(hmax, hmax1)
        hmin = float(hmin)
        hmax = float(hmax)
        if hmax == hmin :
            hmax = hmin + 1e-3
        self.__Hlimits = (hmin, hmax)
        #----------------------------------------------------------------------
        # revise bin info
        #----------------------------------------------------------------------
        nbins  = int(self["nbins"])
        if not self.was_configured("binsize") :
            self["binsize"] = 1.001*abs(hmax - hmin) / float(nbins)
        binsize = float(self["binsize"])
        if not self.was_configured("binorigin") :
            self["binorigin"] = hmin
        binorigin = float(self["binorigin"])
        if not self.was_configured("bar_width") :
            self["bar_width"] = self["binsize"]
        bar_width = float(self["bar_width"])

        if not self.was_configured("xmin") :
            self["xmin"] = binorigin - bar_width * 0.5
        if not self.was_configured("xmax") :
            self["xmax"] = binorigin + nbins*binsize + bar_width * 0.5
        if not self.was_configured("ymin") :
            self["ymin"] = 0
        #----------------------------------------------------------------------
        # get histogram counts
        #----------------------------------------------------------------------
        dhist = Data()
        bin_values = []
        for i in range(0, nbins) :
            bin_values.append(binorigin + i*binsize)
        dhist.read_inline("hbin", bin_values)

        for hset in self.__hsets :
            dname = self.__hset_dname[hset]
            col   = self.__hset_dcol[hset]
            hdata = self.__hset_data[hset]
            if not self.was_configured("xtitle") :
                self["xtitle"] = col
            if not self.was_configured("ytitle") :
                self["ytitle"] = "counts"
            hcol = "%s_counts" % col
            dhist.set("%s = 0" % (hcol))
            for col_value in hdata :
                k = int((col_value - binorigin)/binsize)
                if k >= nbins :
                    continue
                count = dhist.get_entry(k, hcol)
                dhist.set_entry(k, hcol, count + 1)
            if new :
                self.add_curve(dhist, "hbin", hcol, dname=dname)
            else :
                curve = "%s_:_%s_vs_%s" % (dname, hcol, "hbin")
                self._curve_xdata[curve] = dhist.get("hbin")
                self._curve_ydata[curve] = dhist.get(hcol)
    #==========================================================================
    # METHOD  : _plot_curves
    # PURPOSE : plot all curves
    #==========================================================================
    def _plot_curves(self, pairwise_coordinates=False) :
        plot = self._Component["plot"]
        hbar_width = 0.5*self["bar_width"]
        s1, t = self.plot_xy_st(0,0)
        s2, t = self.plot_xy_st(self["bar_width"],0)
        ds = s2-s1
        if self.was_configured("bar_outline") :
            outline = self["bar_outline"]
        else :
            outline = "black"

        for curve in self.curves() :
            color = self._curve_color[curve]
            wline = self._curve_wline[curve]
            xydata = list(zip(self._curve_xdata[curve], self._curve_ydata[curve]))
            ltag = curve + "-LINE"
            for x, y in xydata :
                sh, th = self.plot_xy_st(x, y)
                sz, tz = self.plot_xy_st(x, 0)
                s1 = max(min(sh,    1.0), 0.0)
                s2 = max(min(sh+ds, 1.0), 0.0)
                t1 = max(min(tz,    1.0), 0.0)
                t2 = max(min(th,    1.0), 0.0)
                u1, v1 = self.plot_st_uv(s1, t1)
                u2, v2 = self.plot_st_uv(s2, t1)
                u3, v3 = self.plot_st_uv(s2, t2)
                u4, v4 = self.plot_st_uv(s1, t2)
                coords = (u1, v1, u2, v2, u3, v3, u4, v4)
                plot.create_polygon(coords, tags=ltag)
            plot.itemconfigure(ltag, fill=color)
            plot.itemconfigure(ltag, outline=outline)
            plot.itemconfigure(ltag, width=wline)
    #==========================================================================
    # METHOD  : _settings_cmd
    # PURPOSE : settings via entrytable-select
    # NOTES   :
    #     * specs: type, blurb, items
    #     * entry: key, label, value
    #==========================================================================
    def _settings_cmd(self) :
        curve     = self.current_curve()
        wline     = self._curve_wline[curve]
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
          ["entry", "Histogramx", [
                 ["nbins",       "Number of bins", self["nbins"]],
                 ["binorigin",   "Bin origin",     self["binorigin"]],
                 ["binsize",     "Bin size",       self["binsize"]],
                 ["bar_width",   "Bar width",      self["bar_width"]],
                 ["bar_outline", "Bar outline",    self["bar_outline"]],
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
            self["xtitle"]            = V["xtitle"]
            self["ytitle"]            = V["ytitle"]
            self["plot_background"]   = V["plot_bg"]
            self["legend_background"] = V["lgnd_bg"]
            self["nbins"]             = int(V["nbins"])
            self["binorigin"]         = float(V["binorigin"])
            #-----------------------------------------
            # if binsize wasn't changed, revise
            #-----------------------------------------
            if self["binsize"]   == float(V["binsize"]) :
                nbins                 = self["nbins"]
                hmin, hmax            = self.__Hlimits
                self["binsize"]       = 1.001*abs(hmax - hmin) / float(nbins)
            else :
                self["binsize"]       = float(V["binsize"])
            if self["bar_width"] == float(V["bar_width"]) :
                self["bar_width"]     = self["binsize"]
            else :
                self["bar_width"]     = float(V["bar_width"])
            self["bar_outline"]       = V["bar_outline"]
            self._curve_wline[curve]  = int(V["wline"])

            self._histogram_rebin()
            self.autoscale(autoscale_x=False, autoscale_y=True, strict=False)
            self._plot_redraw()
