################################################################################
# CLASS    : Contourx
# PURPOSE  : contour plot
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:18:04 2013
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
from builtins import zip
from builtins import range
import sys
import decida
from decida.PlotBasem import PlotBasem
from decida.SelectionDialog import SelectionDialog

class Contourx(PlotBasem) :
    """
    **synopsis**:

        Plot color-band and/or line contours.

        Contourx plots color contour bands and/or contour lines of a
        3-dimensional surface specified on points on a 2-dimensional grid.

        The color bands can be hidden, leaving only the contour lines, or
        contour lines can be hidden, leaving only the color bands.

        The Edit->Settings dialog can be used to add more (equally-spaced)
        contour values.

    **constructor arguments**:

        **parent** (tk handle, default=None)

              handle of frame or other widget to pack plot in.
              if this is not specified, top-level is created.

        **\*\*kwargs** (dict)

              keyword=value specifications:
              **options** or **configuration-options**

    **options**:

        **xvalues** (list of float)

              list of x values. [x[0], ... , x[nx]]

        **yvalues** (list of float)

              list of y values. [y[0], ... , y[ny]]

        **zvalues** (list of lists of float)

              list of z values corresponding x, y points
              [x[0],  y[0], ... , x[0],  y[ny]],
              ...           ...   ...
              [x[nx], y[0], ... , x[nx], y[ny]]

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

        **plot_width**  (str, default="10i" for MacOS, else "7i")

              Width of plot window (Tk inch or pixel specification)

        **plot_background** (str, default="GhostWhite")

              Background color of plot window.

        **legend_background** (str, default="AntiqueWhite2")

              Background color of legend.

        **grid_color** (str, default="black")

              Color of contour grid.

        **num_contours** (int, default=21)

              number of contours.

        **show_bands** (bool, default=True)

              if True, show contour color-bands.

        **colors** (list of str, default = ["blue", "red", "green",
                 "orange", "cyan", "brown",
                 "black", "blue violet", "cadet blue", "dark cyan",
                 "dark goldenrod", "dark green", "dark magenta",
                 "dark olive green", "dark orange", "dark red",
                 "dark slate blue", "dark slate gray", "dodger blue",
                 "forest green", "steel blue", "sienna"])

              list of colors for curves.
              Used to populate color menu, and to specify curve colors
              in scripted "command" option.

        **symbols** (list of str, default = ["none", "dot", "square",
                "diamond", "triangle", "itriangle",
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

        **traces** (list of str, default = ["increasing"])

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

    **example** (from test_Contourx_1): ::

        import decida, math
        from decida.Contourx import Contourx

        xmin, xmax, ymin, ymax, nx, ny, nc = -20, 20, -20, 20, 41, 41, 41
        def zfunction(x, y) :
            return math.pow(
                (math.pow((x-10.0),2.0)+math.pow(y,2.0))*
                (math.pow((x+10.0),2.0)+math.pow(y,2.0)), 0.25
            )
        xvalues = decida.range_sample(xmin, xmax, num=nx)
        yvalues = decida.range_sample(ymin, ymax, num=ny)
        zvalues = []
        for x in xvalues :
            zx = list()
            for y in yvalues :
                z = zfunction(x, y)
                zx.append(z)
            zvalues.append(zx)
        c=Contourx(None, xvalues=xvalues, yvalues=yvalues, zvalues=zvalues, num_contours=nc)

    **public methods**:

        * public methods from *PlotBasem* (2-dimensinal plot base class)

    """
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Contourx main
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
        if sys.platform == "darwin" :
            self["plot_height"] = "10i"
            self["plot_width"]  = "10i"
        else :
            self["plot_height"] = "7i"
            self["plot_width"]  = "7i"
        self["traces"]      = ["both"]
        self._add_options({
            "grid_color"      : ["black",   None],
            "num_contours"    : [21,        None],
            "show_bands"      : [True,      None],
        })
        #----------------------------------------------------------------------
        # keyword arguments are *not* all configuration options
        #----------------------------------------------------------------------
        for key, value in list(kwargs.items()) :
            if   key == "xvalues" :
                self._xvalues = value
            elif key == "yvalues" :
                self._yvalues = value
            elif key == "zvalues" :
                self._zvalues = value
            else :
                self[key] = value
        self._contour_recalc()
        #----------------------------------------------------------------------
        # build gui:
        #----------------------------------------------------------------------
        self._gui()
        self._mainloop()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Contourx configuration option callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Contourx GUI
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _contour_recalc
    # PURPOSE : re-calculate contours
    #==========================================================================
    def _contour_recalc(self) :
        curve = "contours"
        self._curves = []
        self._curves.append(curve)
        self._curve_dname[curve]  = "d"
        self._curve_xname[curve]  = "x"
        self._curve_yname[curve]  = "y"
        self._curve_color[curve]  = "blue"
        self._curve_symbol[curve] = "none"
        self._curve_ssize[curve]  = 0.01
        self._curve_wline[curve]  = 1
        self._curve_trace[curve]  = "both"
        self._curve_lstate[curve] = True
        self._curve_sstate[curve] = True
        self._curve_xdata[curve]  = []
        self._curve_ydata[curve]  = []
        #----------------------------------------------------------------------
        # find min and max of z-values:
        #----------------------------------------------------------------------
        zmin = min(self._zvalues[0])
        zmax = max(self._zvalues[0])
        for i in range(1, len(self._xvalues)) :
            zmin = min(zmin, min(self._zvalues[i]))
            zmax = max(zmax, max(self._zvalues[i]))
        #----------------------------------------------------------------------
        # generate contour values, and colors:
        #----------------------------------------------------------------------
        nc = self["num_contours"]
        contours = decida.range_sample(zmin, zmax, num=nc)
        contour_colors = []
        s, v = 0.8, 0.9
        for i in range(0, nc) :
            h = 6.0*float(i)/float(nc)
            k = int(h) % 6
            f = h - k
            r1 = 1.0
            r2 = 1.0-s
            r3 = 1.0-s*f
            r4 = 1.0+s*f-s
            if   k == 0 :
                r, g, b = (r1, r4, r2)
            elif k == 1 :
                r, g, b = (r3, r1, r2)
            elif k == 2 :
                r, g, b = (r2, r1, r4)
            elif k == 3 :
                r, g, b = (r2, r3, r1)
            elif k == 4 :
                r, g, b = (r4, r2, r1)
            elif k == 5 :
                r, g, b = (r1, r2, r3)
            color = "#%02x%02x%02x" % (int(256*v*r), int(256*v*g), int(256*v*b))
            contour_colors.append(color)
        #----------------------------------------------------------------------
        # generate contour bands for contours
        #----------------------------------------------------------------------
        self._contour_bands = True
        self._contour_data = []
        for k, co in enumerate(contours[:-1]) :
            color = contour_colors[k]
            cp  = contours[k+1]
            clo = min(co, cp)
            chi = max(co, cp)
            for i, xo in enumerate(self._xvalues[:-1]):
                xp = self._xvalues[i+1]
                dx = xp - xo
                for j, yo in enumerate(self._yvalues[:-1]):
                    yp = self._yvalues[j+1]
                    dy = yp - yo
                    z_list = (
                        self._zvalues[i][j],
                        self._zvalues[i][j+1],
                        self._zvalues[i+1][j+1],
                        self._zvalues[i+1][j],
                        self._zvalues[i][j],
                    )
                    zmin = min(z_list)
                    zmax = max(z_list)
                    if zmin == zmax :
                        continue
                    if ((clo < zmin) and (chi < zmin)) or \
                       ((clo > zmax) and (chi > zmax)) :
                        continue
                    Dlo = []
                    Dhi = []
                    Llo = []
                    Lhi = []
                    for zo, zp in zip(z_list[0:], z_list[1:]) :
                        if zp != zo :
                            dlo = (clo - zo)/(zp - zo)
                            dhi = (chi - zo)/(zp - zo)
                        else :
                            dlo = 0.5 if (clo == zo) else -1.0
                            dhi = 0.5 if (chi == zo) else -1.0
                        Dlo.append(dlo)
                        Dhi.append(dhi)
                        Llo.append( (dlo > 0.0) & (dlo <= 1.0) )
                        Lhi.append( (dhi > 0.0) & (dhi <= 1.0) )
                    Xlo = (xo, xo+Dlo[1]*dx, xp, xp-Dlo[3]*dx)
                    Ylo = (yo+Dlo[0]*dy, yp, yp-Dlo[2]*dy, yo)
                    Xhi = (xo, xo+Dhi[1]*dx, xp, xp-Dhi[3]*dx)
                    Yhi = (yo+Dhi[0]*dy, yp, yp-Dhi[2]*dy, yo)
                    Hlo = []
                    Hhi = []
                    for m in (0, 1, 2, 3) :
                        if Llo[m] and len(Hlo) < 2 :
                            Hlo.append((m, Xlo[m], Ylo[m]))
                        if Lhi[m] and len(Hhi) < 2 :
                            Hhi.append((m, Xhi[m], Yhi[m]))
                    coords = []
                    if (len(Hlo) < 2) and (len(Hhi) < 2) :
                        #-----------------------------
                        # fill entire grid section
                        #-----------------------------
                        if (clo <= zmin) and (chi >= zmax) :
                            coords = [xo, yo, xo, yp, xp, yp, xp, yo]
                    elif (len(Hlo) < 2) and (len(Hhi) == 2) :
                        #-----------------------------
                        # high band edge within segment
                        #-----------------------------
                        m1, x1, y1 = Hhi[0]
                        m2, x2, y2 = Hhi[1]
                        if (z_list[m1] == chi) :
                            coords = [xo, yo, xo, yp, xp, yp, xp, yo]
                        else :
                            coords.extend((x1, y1))
                            ccw = (z_list[m1] < chi)
                            m = m1
                            while m != m2 :
                                if ccw :
                                    x = (xo, xo, xp, xp)[m]
                                    y = (yo, yp, yp, yo)[m]
                                    m = (m-1) % 4
                                else :
                                    m = (m+1) % 4
                                    x = (xo, xo, xp, xp)[m]
                                    y = (yo, yp, yp, yo)[m]
                                coords.extend((x, y))
                            coords.extend((x2, y2))
                    elif (len(Hlo) == 2) and (len(Hhi) < 2) :
                        #-----------------------------
                        # low  band edge within segment
                        #-----------------------------
                        m1, x1, y1 = Hlo[0]
                        m2, x2, y2 = Hlo[1]
                        if (z_list[m1] == clo) :
                            coords = [xo, yo, xo, yp, xp, yp, xp, yo]
                        else :
                            coords.extend((x1, y1))
                            ccw = (z_list[m1] > clo)
                            m = m1
                            while m != m2 :
                                if ccw :
                                    x = (xo, xo, xp, xp)[m]
                                    y = (yo, yp, yp, yo)[m]
                                    m = (m-1) % 4
                                else :
                                    m = (m+1) % 4
                                    x = (xo, xo, xp, xp)[m]
                                    y = (yo, yp, yp, yo)[m]
                                coords.extend((x, y))
                            coords.extend((x2, y2))
                    elif (len(Hlo) == 2) and (len(Hhi) == 2) :
                        #-----------------------------
                        # both band edges within segment
                        #-----------------------------
                        m1, x1, y1 = Hhi[0]
                        m2, x2, y2 = Hhi[1]
                        m3, x3, y3 = Hlo[0]
                        m4, x4, y4 = Hlo[1]
                        coords.extend((x1, y1))
                        ccw = (z_list[m1] <= chi)
                        m = m1
                        while m != m3 and m != m4 :
                            if ccw :
                                x = (xo, xo, xp, xp)[m]
                                y = (yo, yp, yp, yo)[m]
                                m = (m-1) % 4
                            else :
                                m = (m+1) % 4
                                x = (xo, xo, xp, xp)[m]
                                y = (yo, yp, yp, yo)[m]
                            coords.extend((x, y))
                        if m == m3 :
                            coords.extend((x3, y3, x4, y4))
                            m = m4
                        else :
                            coords.extend((x4, y4, x3, y3))
                            m = m3
                        ccw = (z_list[m] >= clo)
                        while m != m2 :
                            if ccw :
                                x = (xo, xo, xp, xp)[m]
                                y = (yo, yp, yp, yo)[m]
                                m = (m-1) % 4
                            else :
                                m = (m+1) % 4
                                x = (xo, xo, xp, xp)[m]
                                y = (yo, yp, yp, yo)[m]
                            coords.extend((x, y))
                        coords.extend((x2, y2))
                    else :
                        print(len(Hlo), len(Hhi))
                    if coords :
                        self._contour_data.append((coords, color))
        #----------------------------------------------------------------------
        # generate line-segments for contours
        #----------------------------------------------------------------------
        for c in contours :
            for i, xo in enumerate(self._xvalues[:-1]):
                xp = self._xvalues[i+1]
                dx = xp - xo
                for j, yo in enumerate(self._yvalues[:-1]):
                    yp = self._yvalues[j+1]
                    dy = yp - yo
                    z_list = (
                        self._zvalues[i][j],
                        self._zvalues[i][j+1],
                        self._zvalues[i+1][j+1],
                        self._zvalues[i+1][j],
                        self._zvalues[i][j],
                    )
                    zmin = min(z_list)
                    zmax = max(z_list)
                    if zmin == zmax :
                        continue
                    if (c < zmin) or (c > zmax) :
                        continue
                    D = []
                    L = []
                    for zo, zp in zip(z_list[0:], z_list[1:]) :
                        if zp != zo :
                            d = (c - zo)/(zp - zo)
                        else :
                            d = -1.0
                        D.append(d)
                        L.append( (d > 0.0) & (d <= 1.0) )
                    X = (xo, xo+D[1]*dx, xp, xp-D[3]*dx)
                    Y = (yo+D[0]*dy, yp, yp-D[2]*dy, yo)
                    for m, n in zip((0, 0, 0, 1, 1, 2), (1, 2, 3, 2, 3, 3)) :
                        if L[m] and L[n] :
                            self._curve_xdata[curve].extend((X[m], X[n]))
                            self._curve_ydata[curve].extend((Y[m], Y[n]))
        #----------------------------------------------------------------------
        # sort segments (experimental)
        # map x, y to node
        #----------------------------------------------------------------------
        if False :
            Node = {}
            N_xy = {}
            n = -1
            for x, y in zip(self._curve_xdata[curve], self._curve_ydata[curve]) :
                if (x, y) not in Node :
                    n += 1
                    Node[(x, y)] = n
                    N_xy[n] = (x, y)
    #==========================================================================
    # METHOD  : _plot_curves
    # PURPOSE : plot all curves
    #==========================================================================
    def _plot_curves(self, pairwise_coordinates=False) :
        plot = self._Component["plot"]
        ctag = "contours-BAND"
        for band in self._contour_data :
            xycoords, color = band
            uvcoords = []
            for x, y in zip(xycoords[0::2], xycoords[1::2]) :
                u, v = self.plot_xy_uv(x, y)
                uvcoords.extend((u, v))
            plot.create_polygon(uvcoords, fill=color, tags=ctag)
        if self["show_bands"] :
            plot.itemconfigure(ctag, state="normal")
        else :
            plot.itemconfigure(ctag, state="hidden")
        PlotBasem._plot_curves(self, pairwise_coordinates=True)
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
          ["entry", "Contourx", [
                 ["num_contours", "Number of contours", self["num_contours"]],
              ]
          ],
          ["check", "", [
                 ["show_bands", "show contour bands", self["show_bands"]],
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
            self["num_contours"]      = int(V["num_contours"])
            self["show_bands"]        = V["show_bands"]
            self._curve_wline[curve]  = int(V["wline"])

            self._contour_recalc()
            self.autoscale(autoscale_x=False, autoscale_y=True, strict=False)
            self._plot_redraw()
