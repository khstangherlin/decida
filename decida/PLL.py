################################################################################
# CLASS    : PLL
# PURPOSE  : Phase-Locked Loop class for small-signal/z-domain model
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:22:02 2013
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
import os
import math
import time
import stat
import tkinter as tk
import tkinter.filedialog
import decida
from decida.ItclObjectx import ItclObjectx
from decida.Data        import Data
from decida.Calc        import Calc
from decida.XYplotm     import XYplotm
from decida.entry_emacs_bindings import entry_emacs_bindings

class PLL(ItclObjectx, tk.Frame) :
    """
    **synopsis**:

        Phase-Locked Loop small-signal analysis graphical user interface.

        *PLL* calculates the S-domain and Z-domain jitter transfer
        characteristics of a PLL.  Both open-loop and closed-loop
        characteristics are calculated.  The transfer function magnitude
        and phase are plotted and several characteristic PLL metrics are
        printed out, such as damping-factor, bandwidth and phase-margin.

        *PLL* has two modes of use.  The first is an interactive mode, with a
        graphical user-interface.  In the interactive mode, the user changes
        an input PLL parameter value in the entry box and presses <Return>
        to cause a new set of calculations to be performed and displayed.

        In the non-interactive mode, *PLL* can be embedded in a script involving
        one or more loops of calculations.  In this mode, use the *recalculate*
        user method.  After re-calculation, PLL metrics can be reported to a
        file.

        The DeCiDa application *pllss* simply instantiates one *PLL* object.

    **constructor arguments**:

        **parent** (tk handle, default=None)

              handle of frame or other widget to pack PLL in.
              if this is not specified, top-level is created.

        **\*\*kwargs** (dict)

              keyword=value specifications:
              configuration-options

    **configuration options**:

        **verbose** (bool, default=False)

            Enable/disable verbose mode.

        **gui** (bool, default=True)

            If gui is True, display interactive graphical-user interface.
            Otherwise, perform the calculations without any user interaction.

        **plot_width** (str, default="5in")

            Width of plot window (Tk inch or pixel specification)

        **plot_height** (str, default="5in")

            Height of plot window (Tk inch or pixel specification)

        **plot_style** (int, default=0)

            The style of the plot:

                *    0 : plot Hol(s) Hcl(s) Hcl(z)

                *    1 : plot Hol(s) Hol(z)

                *    2 : plot Hol(s) Hcl(s)

                *    3 : plot Hol(z) Hcl(z)

                *    4 : plot Htr(s) Htr(z) (dB and Phase)

                *    5 : plot Htr(s) Htr(z) (dB only)

        **plot_orient** (str, default="horizontal")

            One of "horizontal" or "vertical".  If horizontol,
            parameter selection and plot panes are side-by-side.
            If vertical, parameter selection pane is over plot pane.

        **plot_title** (str, default="")

            Main plot title

        **npts** (int, default=1000)

            Number of frequency points to sample (logarithmic sampliing).

        **fmax** (float, default=1e10)

            The maximum frequency to sample.

        **fmin** (float, default=1e2)

            The minimum frequency to sample.

        **rf** (float, default=10e3)

            Loop filter resistor value [ohm]

        **cf** (float, default=500e_12)

            Loop filter capacitor value [F]

        **cd** (float, default=5e_12)

            Loop filter ripple-bypass capacitor value [F]

        **mp** (float, default=40.0)

            Feed-back divider value.

        **icp** (float, default=100e_6)

            Charge-pump current value. [A]

        **kvco** (float, default=700e6)

            VCO total gain. [Hz/V]

        **fv2i** (float, default=100e9)

            Voltage to current converter pole. [Hz]

        **fref** (float, default=350e6)

            Reference frequency. [Hz]

        **fb_delay** (float, default=0.0)

            Feedback divider delay. [s]

        **ph_offset** (float, default=0.0)

            Excess phase-offset between reference and
            output of feedback divider. [s]

    **example** (from test_PLL): ::

        from decida.PLL import PLL
        PLL()

    **public methods**:

        * public methods from *ItclObjectx*

    """
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PLL main
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, parent=None, use_matplotlib=True, **kwargs) :
        ItclObjectx.__init__(self)
        #----------------------------------------------------------------------
        # private variables:
        #----------------------------------------------------------------------
        self.__parent = parent
        self.__use_matplotlib = use_matplotlib
        self.__Component  = {}
        self.__Parameters = {}
        self.__data_obj = Data()
        self.__dataview = None
        self.__mapped   = False
        self.__pll_root = "PLL"
        #----------------------------------------------------------------------
        # configuration options:
        #----------------------------------------------------------------------
        if sys.platform == "darwin" :
            plot_width  = "8i"
            plot_height = "8i"
        else :
            plot_width  = "5i"
            plot_height = "5i"
        self._add_options({
            "verbose"        : [False, None],
            "gui"            : [True, None],
            "plot_width"     : [plot_width, None],
            "plot_height"    : [plot_height, None],
            "plot_style"     : [0,          self._config_plot_style_callback],
            "plot_orient"    : ["horizontal", self._config_plot_orient_callback],
            "plot_title"     : ["",         self._config_plot_title_callback],
            "npts"           : [1000,       self._config_npts_callback],
            "fmax"           : [1e10,       self._config_fmax_callback],
            "fmin"           : [1e2,        self._config_fmin_callback],
            "rf"             : [10e3,       self._config_rf_callback],
            "cf"             : [500e-12,    self._config_cf_callback],
            "cd"             : [5e-12,      self._config_cd_callback],
            "mp"             : [25.0,       self._config_mp_callback],
            "icp"            : [10e-6,      self._config_icp_callback],
            "kvco"           : [700e6,      self._config_kvco_callback],
            "fv2i"           : [100e9,      self._config_fv2i_callback],
            "fref"           : [5e6,        self._config_fref_callback],
            "fb_delay"       : [0.0,        self._config_fb_delay_callback],
            "ph_offset"      : [0.0,        self._config_ph_offset_callback],
        })
        #----------------------------------------------------------------------
        # keyword arguments are all configuration options
        #----------------------------------------------------------------------
        for key, value in list(kwargs.items()) :
            self[key] = value
        #----------------------------------------------------------------------
        # build gui:
        #----------------------------------------------------------------------
        if self["gui"] :
            self._gui()
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
    # PLL configuration option callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _config_plot_style_callback
    # PURPOSE : configure plot_style
    #==========================================================================
    def _config_plot_style_callback(self) :
        if not self["plot_style"] in (0, 1, 2, 3, 4, 5) :
            self.warning("plot_style must be one of: ",
                "    0 : plot Hol(s) Hcl(s) Hcl(z)",
                "    1 : plot Hol(s) Hol(z)",
                "    2 : plot Hol(s) Hcl(s)",
                "    3 : plot Hol(z) Hcl(z)",
                "    4 : plot Htr(s) Htr(z) (dB and Phase)",
                "    5 : plot Htr(s) Htr(z) (dB only)",
            )
            self["plot_style"] = 0
        if self.__toplevel :
            self.plot(new=True)
    #==========================================================================
    # METHOD  : _config_plot_orient_callback
    # PURPOSE : configure plot_orient
    #==========================================================================
    def _config_plot_orient_callback(self) :
        if not self["plot_orient"] in ("vertical", "horizontal") :
            self.warning("plot_orient must be one of: ",
                "    \"vertical\"   : text over graph",
                "    \"horizontal\" : text beside graph",
            )
            self["plot_orient"] = "horizontal"
        if self["gui"] :
            if self.__mapped :
                self.quit()
                self.__Component["topframe"].destroy()
                self.__mapped = False
            self._gui()
    #==========================================================================
    # METHOD  : _config_plot_title_callback
    # PURPOSE : configure plot_title
    #==========================================================================
    def _config_plot_title_callback(self) :
        if self.__mapped :
            self.plot(new=True)
    #==========================================================================
    # METHOD  : _config_npts_callback
    # PURPOSE : configure npts
    #==========================================================================
    def _config_npts_callback(self) :
        self.__entry_enter("npts")
    #==========================================================================
    # METHOD  : _config_fmax_callback
    # PURPOSE : configure fmax
    #==========================================================================
    def _config_fmax_callback(self) :
        self.__entry_enter("fmax")
    #==========================================================================
    # METHOD  : _config_fmin_callback
    # PURPOSE : configure fmin
    #==========================================================================
    def _config_fmin_callback(self) :
        self.__entry_enter("fmin")
    #==========================================================================
    # METHOD  : _config_rf_callback
    # PURPOSE : configure rf
    #==========================================================================
    def _config_rf_callback(self) :
        self.__entry_enter("rf")
    #==========================================================================
    # METHOD  : _config_cf_callback
    # PURPOSE : configure cf
    #==========================================================================
    def _config_cf_callback(self) :
        self.__entry_enter("cf")
    #==========================================================================
    # METHOD  : _config_cd_callback
    # PURPOSE : configure cd
    #==========================================================================
    def _config_cd_callback(self) :
        self.__entry_enter("cd")
    #==========================================================================
    # METHOD  : _config_mp_callback
    # PURPOSE : configure mp
    #==========================================================================
    def _config_mp_callback(self) :
        self.__entry_enter("mp")
    #==========================================================================
    # METHOD  : _config_icp_callback
    # PURPOSE : configure icp
    #==========================================================================
    def _config_icp_callback(self) :
        self.__entry_enter("icp")
    #==========================================================================
    # METHOD  : _config_kvco_callback
    # PURPOSE : configure kvco
    #==========================================================================
    def _config_kvco_callback(self) :
        self.__entry_enter("kvco")
    #==========================================================================
    # METHOD  : _config_fv2i_callback
    # PURPOSE : configure fv2i
    #==========================================================================
    def _config_fv2i_callback(self) :
        self.__entry_enter("fv2i")
    #==========================================================================
    # METHOD  : _config_fref_callback
    # PURPOSE : configure fref
    #==========================================================================
    def _config_fref_callback(self) :
        self.__entry_enter("fref")
    #==========================================================================
    # METHOD  : _config_fb_delay_callback
    # PURPOSE : configure fb_delay
    #==========================================================================
    def _config_fb_delay_callback(self) :
        self.__entry_enter("fb_delay")
    #==========================================================================
    # METHOD  : _config_ph_offset_callback
    # PURPOSE : configure ph_offset
    #==========================================================================
    def _config_ph_offset_callback(self) :
        self.__entry_enter("ph_offset")
    #==========================================================================
    # METHOD  : __entry_enter
    # PURPOSE : used by config callbacks for entries
    #==========================================================================
    def __entry_enter(self, var) :
        val = self[var]
        key = "%s_entry" % (var)
        if key in self.__Component :
            entry = self.__Component[key]
            entry.delete(0, "end")
            if isinstance(val, int):
                entry.insert(0, "%s" % (val))
            else:
                entry.insert(0, "%g" % (val))
    #==========================================================================
    # METHOD  : __entry_update
    # PURPOSE : used by entry callbacks to config
    #==========================================================================
    def __entry_update(self, var) :
        val = self[var]
        key = "%s_entry" % (var)
        entry = self.__Component[key]
        newval = entry.get()
        try :
            if isinstance(val, float) :
                newval = float(newval)
            elif isinstance(val, int) :
                newval = int(newval)
            self[var] = newval
        except :
            entry.delete(0, "end")
            if isinstance(val, int) :
                entry.insert(0, "%s" % (val))
            else:
                entry.insert(0, "%g" % (val))
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # calculations
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __calculate
    # PURPOSE : calculate transfer functions:
    #==========================================================================
    def __calculate(self) :
        #----------------------------------------
        # input parameters
        #----------------------------------------
        fmin      = self["fmin"]
        fmax      = self["fmax"]
        npts      = self["npts"]
        rf        = self["rf"]
        cf        = self["cf"]
        cd        = self["cd"]
        mp        = self["mp"]
        icp       = self["icp"]
        kvco      = self["kvco"]
        fv2i      = self["fv2i"]
        fref      = self["fref"]
        fb_delay  = self["fb_delay"]
        ph_offset = self["ph_offset"]
        #----------------------------------------
        # calculated parameters
        #----------------------------------------
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # s-domain
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        lpll = float(mp)/(kvco*icp)
        zo = math.sqrt(lpll/cf)
        zeta = 0.5*rf/zo
        Q = 1.0/(2.0*zeta)
        wn = math.sqrt(1.0/(lpll*cf))
        wb = wn/Q
        wz = wn*Q
        peak = 10.0*math.log10(1.0 + math.pow(Q, 2.0))
        if cd > 0 :
            wp = 1.0/(rf*cf*cd/(cf+cd))
            wh = wn*math.sqrt(cf/cd)
            zeth = 0.25*math.sqrt(cf/cd)/zeta
        else :
            wp = 0.0
            wh = 0.0
            zeth = 0.0
        fn = wn/(2.0*math.pi)
        fz = wz/(2.0*math.pi)
        fb = wb/(2.0*math.pi)
        fp = wp/(2.0*math.pi)
        fh = wh/(2.0*math.pi)
        wv = fv2i*(2.0*math.pi)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # z-domain
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        beta = 1.0-wp/wv
        a0 = wp/fref
        b0 = wv/fref
        a0 = math.exp(-a0) if a0 < 700.0 else 0.0
        b0 = math.exp(-b0) if b0 < 700.0 else 0.0
        c0 = 1.0
        d0 = 0.0
        #----------------------------------------
        # start with new data object
        #----------------------------------------
        if  self.__data_obj is not None:
            del self.__data_obj
        d = Data()
        #----------------------------------------
        # sample freq, generate S = j*omega
        #----------------------------------------
        if self["verbose"] :
            self.message("sample frequency")
        freqs = decida.range_sample(fmin, fmax, num=npts, mode="log")
        d.read_inline("freq", freqs)
        d.cxset("S = 0")
        d.set_parsed("IMAG(S) = %g * freq" % (2.0*math.pi))
        #----------------------------------------
        # transfer functions
        #----------------------------------------
        if self["verbose"] :
            self.message("transfer functions")
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 2nd order s-domain
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        d.cxset("NUM = S/%g + 1" % (wz))
        d.cxset("DEN = S/%g"     % (wn))
        d.cxset("DEN = DEN * DEN")
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # open-loop gain
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        d.cxset("HOL = NUM/DEN")
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # feedback delay
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        d.cxset("HOL = HOL * exp(-S*%g)" % (fb_delay))
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # ripple bypass capacitor
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if cd > 0 :
            d.cxset("HOL = HOL*%g/(1+S/%g)" % (cf/(cf+cd), wp))
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # v2i pole
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if fv2i > 0 :
            d.cxset("HOL = HOL/(1+S/%g)" % (wv))
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # closed-loop and tracking
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        d.cxset("HCL = HOL/(HOL + 1)")
        d.cxset("HTR = 1.0/(HOL + 1)")
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # magnitude and phase of response functions
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        d.cxmag("HOL")
        d.cxmag("HCL")
        d.cxmag("HTR")
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # s-domain figures of merit
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #----------------------------------------
        # 3-dB bandwidth:
        #----------------------------------------
        crossings = d.crossings("freq", "DB(HCL)", level=-3)
        if crossings :
            fbs = crossings[0]
        else :
            fbs = 0.0
        #----------------------------------------
        # phase-margin (s-domain):
        #----------------------------------------
        crossings = d.crossings("freq", "DB(HOL)", level=0)
        if crossings :
            fxs = crossings[0]
            crossings = d.crossings("PH(HOL)", "freq", level=fxs)
            pm = crossings[0] + 180.0
            pos = 0.0
            while pm > 180.0 :
                pm  -= 360.0
                pos -= 360.0
            while pm <= -180.0 :
                pm  += 360.0
                pos += 360.0
        else :
            fxs = 0.0
            pm  = 0.0
            pos = 0.0
        #----------------------------------------
        # peaking (s-domain)
        #----------------------------------------
        pk = d.max("DB(HCL)")
        fk = 0.0
        x = pk
        for i in range(0, 10) :
            crossings = d.crossings("freq", "DB(HCL)", level=x)
            if crossings :
                fk = crossings[0]
                break
            else :
                x -= 1e-6
        #----------------------------------------
        # integrate |Hcl(s)|^2
        # integrate |Htr(s)|^2 = 1/(1+|Hol(s)|)^2
        #----------------------------------------
        if d.get_entry(0, "PH(HTR)") < 0.0 :
            d.set("PH(HTR)=PH(HTR)+360.0")
        dx = d.dup()
        dx.filter("freq <= %g" % (fref*0.5))
        if dx.nrows() > 0 :
            dx.set("HCL2 = MAG(HCL) * MAG(HCL)")
            dx.set_parsed("INTEG(HCL) = HCL2 integ freq")
            ihcl = dx.get_entry(-1, "INTEG(HCL)")
            ihcl = math.sqrt(ihcl*1.0/(fref*0.5))
            dx.set("HTR2 = MAG(HTR) * MAG(HTR)")
            dx.set_parsed("INTEG(HTR) = HTR2 integ freq")
            ihtr = dx.get_entry(-1, "INTEG(HTR)")
            ihtr = math.sqrt(ihtr*1.0/(fref*0.5))
        else :
            ihcl = 0.0
            ihtr = 0.0
        del dx
        #----------------------------------------
        # z-domain transfer functions:
        #----------------------------------------
        d.cxset("Z = exp(S/%g)" % (fref))
        az = 1.0*(1.0-wz/wv-wz/wp)
        bz = 1.0*wz/fref
        if abs(beta) > 1e-14 :
            # wp != wv (fpole != fv2i)
            cz = 1.0*wz/wp*(1.0-wp/wz)/(1.0-wp/wv)
            dz = 1.0*wz/wv*(1.0-wv/wz)/(1.0-wv/wp)
        else :
            # wp == wv (fpole == fv2i)
            cz = 1.0*wz/wp*(2.0-wp/wz)
            dz = 1.0*wz/wv*(1.0-wp/wz)*wp*a0/fref
        pre = 1.0*wb/(fref*(1.0+cd/cf))
        d.cxset("HOLZ = %g*(%g*Z/(Z-1) + %g*Z/((Z-1)*(Z-1)) + %g*Z/(Z-%g) + %g*Z/(Z-%g))" % (pre,az,bz,cz,a0,dz,b0))
        #----------------------------------------
        # feedback divider delay:
        #----------------------------------------
        d.cxset("HOLZ = HOLZ*exp(-S*%g)" % (fb_delay))
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # closed-loop and tracking
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        d.cxset("HCLZ = HOLZ/(HOLZ + 1)")
        d.cxset("HTRZ =  1.0/(HOLZ + 1)")
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # magnitude and phase of response functions
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        d.cxmag("HOLZ")
        d.cxmag("HCLZ")
        d.cxmag("HTRZ")
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # z-domain figures of merit
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #----------------------------------------
        # 3-dB bandwidth:
        #----------------------------------------
        crossings = d.crossings("freq", "DB(HCLZ)", level=-3)
        if crossings :
            fbz = crossings[0]
        else :
            fbz = 0.0
        #----------------------------------------
        # phase-margin (z-domain):
        #----------------------------------------
        crossings = d.crossings("freq", "DB(HOLZ)", level=0)
        if crossings :
            fxz = crossings[0]
            crossings = d.crossings("PH(HOLZ)", "freq", level=fxz)
            pmz = crossings[0] + 180.0
            poz = 0.0
            while pmz > 180.0 :
                pmz -= 360.0
                poz -= 360.0
            while pmz <= -180.0 :
                pmz += 360.0
                poz += 360.0
        else :
            fxz = 0.0
            pmz = 0.0
            poz = 0.0
        #----------------------------------------
        # peaking (z-domain)
        #----------------------------------------
        dx = d.dup()
        dx.filter("freq < %g" % (fref*0.75))
        pkz = dx.max("DB(HCLZ)")
        fkz = 0.0
        x = pkz
        for i in range(0, 10) :
            crossings = dx.crossings("freq", "DB(HCLZ)", level=x)
            if crossings :
                fkz = crossings[0]
                break
            else :
                x -= 1e-6
        del dx
        #----------------------------------------
        # rejection (z-domain)
        #----------------------------------------
        rjz = 0.0
        crossings = d.crossings("DB(HCLZ)", "freq", level=fref*0.5)
        if crossings :
            rjz = crossings[0]
        #----------------------------------------
        # integrate |Hcl(z)|^2
        # integrate |Htr(z)|^2 = 1/(1+|Hol(z)|)^2
        #----------------------------------------
        if d.get_entry(0, "PH(HTRZ)") < 0.0 :
            d.set("PH(HTR)=PH(HTRZ)+360.0")
        dx = d.dup()
        dx.filter("freq <= %g" % (fref*0.5))
        if dx.nrows() > 0 :
            dx.set("HCLZ2 = MAG(HCLZ) * MAG(HCLZ)")
            dx.set_parsed("INTEG(HCLZ) = HCLZ2 integ freq")
            ihclz = dx.get_entry(-1, "INTEG(HCLZ)")
            ihclz = math.sqrt(ihclz*1.0/(fref*0.5))
            dx.set("HTRZ2 = MAG(HTRZ) * MAG(HTRZ)")
            dx.set_parsed("INTEG(HTRZ) = HTRZ2 integ freq")
            ihtrz = dx.get_entry(-1, "INTEG(HTRZ)")
            ihtrz = math.sqrt(ihtrz*1.0/(fref*0.5))
        else :
            ihclz = 0.0
            ihtrz = 0.0
        del dx
        #----------------------------------------
        # phase-shift for viewing purposes
        #----------------------------------------
        d.set("PH(HOL)  = PH(HOL)  + %g" % (pos + ph_offset))
        d.set("PH(HOLZ) = PH(HOLZ) + %g" % (poz + ph_offset))
        #----------------------------------------
        # save parameters and figures of merit
        #----------------------------------------
        self.__data_obj = d
        self.__Parameters["lpll"] = lpll
        self.__Parameters["zo"]   = zo
        self.__Parameters["zeta"] = zeta
        self.__Parameters["Q"]    = Q
        self.__Parameters["wn"]   = wn
        self.__Parameters["wb"]   = wb
        self.__Parameters["wz"]   = wz
        self.__Parameters["peak"] = peak
        self.__Parameters["wp"]   = wp
        self.__Parameters["wh"]   = wh
        self.__Parameters["zeth"] = zeth
        self.__Parameters["fn"]   = fn
        self.__Parameters["fz"]   = fz
        self.__Parameters["fb"]   = fb
        self.__Parameters["fp"]   = fp
        self.__Parameters["fh"]   = fh
        self.__Parameters["wv"]   = wv
        self.__Parameters["beta"] = beta
        self.__Parameters["a0"]   = a0
        self.__Parameters["b0"]   = b0
        self.__Parameters["c0"]   = c0
        self.__Parameters["d0"]   = d0
        self.__Parameters["fbs"]  = fbs
        self.__Parameters["fxs"]  = fxs
        self.__Parameters["pm"]   = pm
        self.__Parameters["pos"]  = pos
        self.__Parameters["pk"]   = pk
        self.__Parameters["fk"]   = fk
        self.__Parameters["ihcl"] = ihcl
        self.__Parameters["ihtr"] = ihtr
        self.__Parameters["fbz"]  = fbz
        self.__Parameters["fxz"]  = fxz
        self.__Parameters["pmz"]  = pmz
        self.__Parameters["pkz"]  = pkz
        self.__Parameters["fkz"]  = fkz
        self.__Parameters["rjz"]  = rjz
        self.__Parameters["ihclz"]= ihclz
        self.__Parameters["ihtrz"]= ihtrz
    #==========================================================================
    # METHOD  : plot
    # PURPOSE : plot transfer functions
    #==========================================================================
    def plot(self, new=False) :
        self.__calculate()
        plot_style = self["plot_style"]
        if   plot_style == 0:
            columns = "freq DB(HOL) DB(HCL) DB(HCLZ) PH(HOL) PH(HCL) PH(HCLZ)"
            colors  = ["red", "red", "orange", "blue", "blue", "violet"]
            wlines  = [3, 1, 1, 3, 1, 1]
            title   = "|Hol| and |Hcl|"
            ytitle  = "Magnitude[dB] and Phase[deg]"
        elif plot_style == 1:
            columns = "freq DB(HOL) DB(HOLZ) PH(HOL) PH(HOLZ)"
            colors  = ["red", "orange", "blue", "violet"]
            wlines  = [3, 1, 3, 1]
            title   = "|Hol| and |Holz|"
            ytitle  = "Magnitude[dB] and Phase[deg]"
        elif plot_style == 2:
            columns = "freq DB(HOLZ) DB(HCLZ) PH(HOLZ) PH(HCLZ)"
            colors  = ["red", "orange", "blue", "violet"]
            wlines  = [3, 1, 3, 1]
            title   = "|Holz| and |Hclz|"
            ytitle  = "Magnitude[dB] and Phase[deg]"
        elif plot_style == 3:
            columns = "freq DB(HOL)  DB(HCL) PH(HOL) PH(HCL)"
            colors  = ["red", "orange", "blue", "violet"]
            wlines  = [3, 1, 3, 1]
            title   = "|Hol| and |Hcl|"
            ytitle  = "Magnitude[dB] and Phase[deg]"
        elif plot_style == 4:
            columns = "freq DB(HTR)  DB(HTRZ) PH(HTR) PH(HTRZ)"
            colors  = ["red", "orange", "blue", "violet"]
            wlines  = [3, 1, 3, 1]
            title   = "|Htr| and |Htrz|"
            ytitle  = "Magnitude[dB] and Phase[deg]"
        elif plot_style == 5:
            columns = "freq DB(HTR)           DB(HTRZ)"
            colors  = ["red", "orange"]
            wlines  = [3, 3]
            title   = "|Htr| and |Htrz|"
            ytitle  = "Magnitude[dB]"
        if new or not self.__mapped :
            if self.__dataview is not None :
                # del should have destroyed it
                self.__dataview.destroy()
                del self.__dataview
            fplt = self.__Component["plot_frame"]
            fplt.pack_forget()
            self.__dataview = XYplotm(fplt,
                use_matplotlib=self.__use_matplotlib,
                command=[self.__data_obj, columns], xaxis="log", yaxis="lin",
                ymin=-200.0, ymax=200.0, colors=colors, wlines=wlines,
                xtitle="frequency [Hz]", ytitle=ytitle, title=title
            )
            fplt.pack(side="top", expand=True, fill="both", padx=2, pady=2)
            self.update()
        else:
            xyplot = self.__dataview
            cols = columns.split()
            xcol = cols.pop(0)
            for ycol, color, wline in zip(cols, colors, wlines) :
                curve = "data_%d_:_%s_vs_%s" % (1, ycol, xcol)
                xyplot.delete_curve(curve)
                xyplot.add_curve(self.__data_obj, xcol, ycol,
                    start=False, autoscale_x=False, autoscale_y=False, strict=False,
                    color=color, wline=wline
                )
        #----------------------------------------------------------------------
        # update contents of text object
        #----------------------------------------------------------------------
        tobj = self.__Component["text"]
        tobj.delete(1.0, "end")
        tobj.insert(1.0, self.report(2))
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PLL GUI
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _gui
    # PURPOSE : build graphical user interface
    #==========================================================================
    def _gui(self) :
        #----------------------------------------------------------------------
        # top-level:
        #----------------------------------------------------------------------
        if self.__parent is None:
            if not tk._default_root :
                root = tk.Tk()
                root.wm_state("withdrawn")
                tk._default_root = root
            self.__toplevel = tk.Toplevel()
            self.__toplevel.wm_state("withdrawn")
            tk.Frame.__init__(self, self.__toplevel, class_ = "PLL",
                background = "steel blue")
            self.__Component["topframe"] = self.__toplevel
        else:
            self.__toplevel = None
            tk.Frame.__init__(self, self.__parent,   class_ = "PLL",
                background = "steel blue")
            self.__Component["topframe"] = self
        self.pack(side="top", fill="both", expand=True)
        #----------------------------------------------------------------------
        # option database:
        #----------------------------------------------------------------------
        if sys.platform == "darwin" :
            self.option_add("*PLL*Menubutton.width", 10)
            self.option_add("*PLL*Menubutton.height", 1)
            self.option_add("*PLL*Label.anchor", "e")
            self.option_add("*PLL*Label.bd", 2)
            self.option_add("*PLL*Label.relief", "sunken")
            self.option_add("*PLL*Label.font", "Courier 18 normal")
            self.option_add("*PLL*Entry.background", "Ghost White")
            self.option_add("*PLL*Entry.width", 15)
            self.option_add("*PLL*Entry.font", "Courier 18 normal")
            self.option_add("*PLL*Entry.highlightThickness", 0)
            self.option_add("*PLL*Text.background", "Ghost White")
            self.option_add("*PLL*Text.width", 30)
            self.option_add("*PLL*Text.height",18)
            self.option_add("*PLL*Text*font", "Courier 18 normal")
        else :
            self.option_add("*PLL*Menubutton.width", 10)
            self.option_add("*PLL*Menubutton.height", 1)
            self.option_add("*PLL*Label.anchor", "e")
            self.option_add("*PLL*Label.bd", 2)
            self.option_add("*PLL*Label.relief", "sunken")
            self.option_add("*PLL*Label.font", "Courier 12 normal")
            self.option_add("*PLL*Entry.background", "Ghost White")
            self.option_add("*PLL*Entry.width", 20)
            self.option_add("*PLL*Entry.font", "Courier 12 normal")
            self.option_add("*PLL*Entry.highlightThickness", 0)
            self.option_add("*PLL*Text.background", "Ghost White")
            self.option_add("*PLL*Text.width",  30)
            self.option_add("*PLL*Text.height", 18)
            self.option_add("*PLL*Text.font", "Courier 12 normal")
        #----------------------------------------------------------------------
        # main layout
        #----------------------------------------------------------------------
        mbar = tk.Frame(self, relief="sunken", bd=2, background="steel blue")
        mbar.pack(side="top", expand=False, fill="x",    padx=2, pady=2)

        fcnt = tk.Frame(self, relief="sunken", bd=2)
        fplt = tk.Frame(self, relief="sunken", bd=2)
        if self["plot_orient"] == "horizontal" :
            fcnt.pack(side="left",  expand=True,  fill="both", padx=2, pady=2)
            fplt.pack(side="right", expand=True,  fill="both", padx=2, pady=2)
        else :
            fcnt.pack(side="top",   expand=False, fill="y",    padx=2, pady=2)
            fplt.pack(side="top",   expand=True,  fill="both", padx=2, pady=2)
        cont = tk.Frame(fcnt, relief="flat", background="steel blue")
        ftxt = tk.Frame(fcnt, relief="flat", bd=2)
        cont.pack(side="left",  expand=True, fill="both", padx=2, pady=2)
        ftxt.pack(side="right", expand=True, fill="both")
        tobj = tk.Text(ftxt, relief="sunken", bd=2, height=5)
        tobj.pack(side="right", expand=True, fill="both")

        self.__Component["plot_frame"] = fplt
        self.__Component["text"] = tobj
        #----------------------------------------------------------------------
        # menu-bar
        #----------------------------------------------------------------------
        file_mb = tk.Menubutton(mbar, text="File")
        file_mb.pack(side="left", padx=5, pady=5)
        edit_mb = tk.Menubutton(mbar, text="Edit")
        edit_mb.pack(side="left", padx=5, pady=5)
        file_menu= tk.Menu(file_mb)
        edit_menu= tk.Menu(edit_mb)
        file_mb["menu"] = file_menu
        edit_mb["menu"] = edit_menu

        help_bt = tk.Button(mbar, text="Help")
        help_bt.pack(side="right", padx=5, pady=5)
        calc_bt = tk.Button(mbar, text="Calculator")
        calc_bt.pack(side="right", padx=5, pady=5)
        calc_bt["background"] = "green"
        calc_bt["foreground"] = "black"
        def calc_cmd() :
            calc_obj = Calc(wait=False)
        calc_bt["command"]    = calc_cmd
        help_bt["background"] = "powder blue"
        help_bt["foreground"] = "black"
        help_bt["command"]    = self.__help_cmd

        mblist = [file_mb, edit_mb]
        #tk_menuBar(mblist)
        #----------------------------------------------------------------------
        # file menu
        #----------------------------------------------------------------------
        file_menu.add_command(
            label="Write PLL script",
            command=self.write_script)
        file_menu.add_command(
            label="Write Data",
            command=self.write_data)
        file_menu.add_command(
            label="Write Report",
            command=self.write_report)
        file_menu.add_command(
            label="Write Plot",
            command=self.write_plot)
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit",
            command=self.__exit_cmd)
        #----------------------------------------------------------------------
        # plot_type menu
        #----------------------------------------------------------------------
        var = tk.StringVar()
        self.__Component["plot_type_var"] = var
        for item in (
            (0,  "Hol(s) Hcl(s) Hcl(z)"),
            (1,  "Hol(s) Hol(z)"),
            (2,  "Hol(s) Hcl(s)"),
            (3,  "Hol(z) Hcl(z)"),
            (4,  "Htr(s) Htr(z) (dB and Phase)"),
            (5,  "Htr(s) Htr(z) (dB only)"),
        ):
            style, label = item
            def cmd1(self=self, style=style) :
                self["plot_style"] = style
            edit_menu.add_radiobutton(
                label=label, command=cmd1,
                variable=var, value=style)
        edit_menu.add_separator()
        var = tk.StringVar()
        self.__Component["plot_orient_var"] = var
        for orient in ("horizontal", "vertical") :
            def cmd2(self=self, orient=orient) :
                self["plot_orient"] = orient
            edit_menu.add_radiobutton(
                label=orient, command=cmd2,
                variable=var, value=orient)
        #----------------------------------------------------------------------
        # plot entries
        #----------------------------------------------------------------------
        entry_list = []
        for item in (
            ["npts",  "number of samples"],
            ["fmin",  "minimum frequency [Hz]"],
            ["fmax",  "maximum frequency [Hz]"],
            ["rf",    "loop-filter resistor [ohm]"],
            ["cf",    "loop-filter capacitor [F]"],
            ["cd",    "loop-filter ripple-byp capacitor [F]"],
            ["mp",    "feed-back divider value"],
            ["icp",   "charge-pump current [A]"],
            ["kvco",  "VCO gain [Hz/V]"],
            ["fv2i",  "V to I pole [Hz]"],
            ["fref",  "reference frequency [Hz]"],
            ["fb_delay", "feedback delay [s]"],
            ["ph_offset", "phase offset [deg]"],
        ) :
            var, text = item
            val = self[var]
            f = tk.Frame(cont, relief="flat")
            f.pack(side="top", expand=False, fill="x")
            l = tk.Label(f, relief="flat", anchor="w", text=text, width=40)
            l.pack(side="left", expand=True, fill="x")
            e = tk.Entry(f, relief="sunken", bd=3)
            e.pack(side="left", expand=True, fill="x")
            self.__Component["%s_label" % (var)] = l
            self.__Component["%s_entry" % (var)] = e
            e.delete(0, "end")
            if isinstance(val, int) :
                e.insert(0, "%g" % (val))
            else:
                e.insert(0, "%s" % (val))
            new = var in ("fmin", "fmax")
            def entrybindcmd(event, self=self, new=new, var=var, entry=e):
                self.__entry_update(var)
                self.plot(new=new)
            e.bind("<Control-Key-s>", entrybindcmd)
            e.bind("<Return>",        entrybindcmd)
            entry_list.append(e)
        entry_emacs_bindings(entry_list)
        #----------------------------------------------------------------------
        # update / mainloop
        #----------------------------------------------------------------------
        self.update()
        #----------------------------------------------------------------------
        # plot transfer functions
        #----------------------------------------------------------------------
        self.plot()
        #----------------------------------------------------------------------
        # update contents of text object
        #----------------------------------------------------------------------
        tobj = self.__Component["text"]
        tobj.delete(1.0, "end")
        tobj.insert(1.0, self.report(2))
        #----------------------------------------------------------------------
        # top-level window
        #----------------------------------------------------------------------
        if  self.__toplevel :
            self.__toplevel.geometry("+20+20")
            self.__toplevel.wm_state("normal")
        self.__mapped = True
        self.wait_window()
        self.__Component["topframe"].destroy()
        self.__mapped = False
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PLL user commands
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #--------------------------------------------------------------------------
    # METHOD  : recalculate
    # PURPOSE : force re-calculation
    # NOTES :
    #    * for non-gui applications
    #--------------------------------------------------------------------------
    def recalculate(self) :
        """ recalculate transfer functions.

        **results**:

            * S-domain and Z-domain open-loop and closed loop jitter transfer
              functions are re-calculated.  For non-gui applications, several
              metrics are also calculated, such as damping-factor,
              bandwidth and phase-margin.

        """
        self.__calculate()
    #--------------------------------------------------------------------------
    # METHOD  : get
    # PURPOSE : get a parameter
    #--------------------------------------------------------------------------
    def get(self, par) :
        """ get a PLL parameter or metric.

        **arguments**:

            **par** (str)

                PLL configuration option or one of the following  metrics:

                * lpll  : PLL inductance, mp/(Kvco*Icp)
                * zo    : PLL characteristic impedance, sqrt(lpll/cf)
                * zeta  : PLL damping coefficient
                * Q     : PLL quality factor
                * wn    : PLL natural frequency [rad/s]
                * wb    : PLL bandwidth [rad/s]
                * wz    : PLL zero frequency [rad/s]
                * wp    : PLL peak frequency [rad/s]
                * wh    : PLL high zeta frequency [rad/s]
                * wv    : PLL V to I converter frequency [rad/s]
                * peak  : PLL peak closed-loop jitter transfer value [dB]
                * zeth  : PLL high-frequency damping factor
                * fn    : PLL natural frequency [Hz]
                * fb    : PLL bandwidth [Hz]
                * fz    : PLL zero frequency [Hz]
                * fp    : PLL peak frequency [Hz]
                * fh    : PLL high frequency [Hz]
                * beta  : Z-domain parameter
                * a0    : Z-domain parameter
                * b0    : Z-domain parameter
                * c0    : Z-domain parameter
                * d0    : Z-domain parameter
                * fbs   : S-domain 3db bandwidth
                * fxs   : S-domain unity-gain bandwidth
                * pm    : S-domain phase-margin
                * pos   : S-domain number of cycles to match phase-response
                * pk    : S-domain peaking
                * fk    : frequency of S-domain peaking
                * ihcl  : integration of closed-loop S-domain jitter transfer function
                * ihtr  : integration of closed-loop S-domain tracking jitter transfer function
                * fbz   : Z-domain 3-dB bandwdth
                * fxz   : Z-domain unity-gain bandwidth
                * pmz   : Z-domain phase-margin
                * pkz   : Z-domain peaking
                * fkz   : frequency of Z-domain peaking
                * rjz   : rejection: loop-gain at fref/2
                * ihclz : integration of closed-loop Z-domain jitter transfer function
                * ihtrz : integration of closed-loop Z-domain tracking transfer function

        """
        if par in self.__Parameters :
            return self.__Parameters[par]
        elif par in self.config_options() :
            return self[par]
        print("parameter \"%s\" is not available" % (par))
        return 0
    #--------------------------------------------------------------------------
    # METHOD  : report
    # PURPOSE : return formatted PLL parameters report
    #--------------------------------------------------------------------------
    def report(self, style=1) :
        """ return a formated PLL parameters report.

        **arguments**:

            **style** (int, default=1)

                The style of the report to generate:

                  1. verbose
                  2. brief

        **results**:

            * Returns a formatted PLL report with various parameters and
              metrics.

        """
        fmin      = self["fmin"]
        fmax      = self["fmax"]
        npts      = self["npts"]
        rf        = self["rf"]
        cf        = self["cf"]
        cd        = self["cd"]
        mp        = self["mp"]
        icp       = self["icp"]
        kvco      = self["kvco"]
        fv2i      = self["fv2i"]
        fref      = self["fref"]
        fb_delay  = self["fb_delay"]
        ph_offset = self["ph_offset"]
        lpll = self.__Parameters["lpll"]
        zo   = self.__Parameters["zo"]
        zeta = self.__Parameters["zeta"]
        Q    = self.__Parameters["Q"]
        wn   = self.__Parameters["wn"]
        wb   = self.__Parameters["wb"]
        wz   = self.__Parameters["wz"]
        peak = self.__Parameters["peak"]
        wp   = self.__Parameters["wp"]
        wh   = self.__Parameters["wh"]
        zeth = self.__Parameters["zeth"]
        fn   = self.__Parameters["fn"]
        fz   = self.__Parameters["fz"]
        fb   = self.__Parameters["fb"]
        fp   = self.__Parameters["fp"]
        fh   = self.__Parameters["fh"]
        wv   = self.__Parameters["wv"]
        beta = self.__Parameters["beta"]
        a0   = self.__Parameters["a0"]
        b0   = self.__Parameters["b0"]
        c0   = self.__Parameters["c0"]
        d0   = self.__Parameters["d0"]
        fbs  = self.__Parameters["fbs"]
        fxs  = self.__Parameters["fxs"]
        pm   = self.__Parameters["pm"]
        pos  = self.__Parameters["pos"]
        pk   = self.__Parameters["pk"]
        fk   = self.__Parameters["fk"]
        ihcl = self.__Parameters["ihcl"]
        ihtr = self.__Parameters["ihtr"]
        fbz  = self.__Parameters["fbz"]
        fxz  = self.__Parameters["fxz"]
        pmz  = self.__Parameters["pmz"]
        pkz  = self.__Parameters["pkz"]
        fkz  = self.__Parameters["fkz"]
        rjz  = self.__Parameters["rjz"]
        ihclz = self.__Parameters["ihclz"]
        ihtrz = self.__Parameters["ihtrz"]
        if style==1 :
            rpt = """
                :
                : ==================================================
                : PLL report: %s
                : ==================================================
                :
                : Feed-backdivider value      M+1    = %d
                : Loop-filter res.            Rf     = %-12.5g Kohm
                : Loop-filter cap.            Cf     = %-12.5g pF
                : Loop-filter ripple-byp cap. Cd     = %-12.5g pF
                : Charge-pump current         Icp    = %-12.5g uA
                : VCO gain                    Kvco   = %-12.5g MHz/V
                : V2I pole                    fv2i   = %-12.5g MHz
                : Reference frequency         fref   = %-12.5g MHz
                : feedback delay              fbdel  = %-12.5g s
                :
                : Loop-filter zero-freq.      fzero  = %-12.5g MHz
                : PLL natural freq.           fnat   = %-12.5g MHz
                : PLL bandwidth (2d-order)    fbw    = %-12.5g MHz
                : Loop-filter pole-freq.      fpole  = %-12.5g MHz
                : PLL HF natural freq.        fnatH  = %-12.5g MHz
                : LF damping factor           zetaL  = %-12.5g
                : HF damping factor           zetaH  = %-12.5g
                : Damping factor              zeta   = %-12.5g
                :
                : Bandwidth (-3dB s-domain)   fbs    = %-12.5g MHz
                : Peaking freq.  (s-domain)   fpeak  = %-12.5g MHz
                : PM freq.       (s-domain)   fxs    = %-12.5g MHz
                : Peaking        (s-domain)   peak   = %-12.5g dB
                : Phase margin   (s-domain)   pm     = %-12.5g deg
                :
                : Bandwidth (-3dB z-domain)   fbz    = %-12.5g MHz
                : Peaking freq.  (z-domain)   fpeakz = %-12.5g MHz
                : PM freq.       (z-domain)   fxz    = %-12.5g MHz
                : Peaking        (z-domain)   peakz  = %-12.5g dB
                : Rejection      (z-domain)   rejz   = %-12.5g dB
                : Phase margin   (z-domain)   pmz    = %-12.5g deg
                :
                : REF/BW ratio            fref/fbz   = %-12.5g
                :
                : VCO/REF Jitter ratio    Jvco/Jref  = %-12.5g
                : ERR/REF Jitter ratio    Jerr/Jref  = %-12.5g
            """ % (
                self.__pll_root,
                mp, rf*1e-3, cf*1e12, cd*1e12, icp*1e6,
                kvco*1e-6, fv2i*1e-6, fref*1e-6,
                fb_delay, fz*1e-6, fn*1e-6, fb*1e-6,
                fp*1e-6, fh*1e-6, zeta, zeth, min(zeta,zeth),
                fbs*1e-6, fk*1e-6, fxs*1e-6, pk, pm,
                fbz*1e-6, fkz*1e-6, fxz*1e-6, pkz, rjz, pmz,
                1.0*fref/fbz, ihclz, ihtrz
            )
        elif style==2 :
            rpt = """
                :fzero     = %-12.5g MHz
                :fnat      = %-12.5g MHz
                :fbw       = %-12.5g MHz
                :fpole     = %-12.5g MHz
                :fnatH     = %-12.5g MHz
                :zetaL     = %-12.5g
                :zetaH     = %-12.5g
                :zeta      = %-12.5g
                :
                :fbs(-3db) = %-12.5g MHz
                :fpeak     = %-12.5g MHz
                :fpm       = %-12.5g MHz
                :peak      = %-12.5g dB
                :pm        = %-12.5g deg
                :
                :fbz(-3db) = %-12.5g MHz
                :fpeakz    = %-12.5g MHz
                :fpmz      = %-12.5g MHz
                :peakz     = %-12.5g dB
                :rejz      = %-12.5g dB
                :pmz       = %-12.5g deg
                :
                :Jvco/Jref = %-12.5g
                :Jerr/Jref = %-12.5g
            """ % (
                fz*1e-6, fn*1e-6, fb*1e-6, fp*1e-6, fh*1e-6,
                zeta, zeth, min(zeta,zeth),
                fbs*1e-6, fk*1e-6,  fxs*1e-6, pk, pm,
                fbz*1e-6, fkz*1e-6, fxz*1e-6, pkz, rjz, pmz,
                ihclz, ihtrz
            )
        olines = []
        for line in rpt.split("\n") :
            tok = line.split(":")
            if len(tok) >= 2 :
                olines.append(tok[1])
        return("\n".join(olines))
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PLL GUI construction methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PLL GUI file menu callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #--------------------------------------------------------------------------
    # METHOD  : __exit_cmd
    # PURPOSE : exit file menu callback
    #--------------------------------------------------------------------------
    def __exit_cmd(self) :
        self.quit()
        self.__Component["topframe"].destroy()
        exit()
    #--------------------------------------------------------------------------
    # METHOD  : write_script
    # PURPOSE : write executable script
    #--------------------------------------------------------------------------
    def write_script(self, filename=None) :
        """ write an executable PLL script with the current parameter set.

        **arguments**:

            **filename** (str, default=None)

                Specify the file to write.  If not specified, use file dialog
                to specify the file.

        **results**:

            * Writes executable script, which when run displays the PLL
              transfer functions for the last set of PLL parameters.

        """
        if not filename :
            initialfile = "%s.pllss" % (self.__pll_root)
            if sys.platform == "darwin" :
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "PLL steady-state file name to save?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".pllss",
                )
            else :
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "PLL steady-state file name to save?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".pllss",
                    filetypes = (
                        ("PLL ss/python files", "*.pllss"),
                        ("PLL ss/python files", "*.py"),
                        ("all files", "*")
                    )
                )
        if not filename :
            return
        #-------------------------------
        # PLL parameters
        #-------------------------------
        self.__pll_root = os.path.splitext(os.path.basename(filename))[0]
        fmin      = self["fmin"]
        fmax      = self["fmax"]
        npts      = self["npts"]
        rf        = self["rf"]
        cf        = self["cf"]
        cd        = self["cd"]
        mp        = self["mp"]
        icp       = self["icp"]
        kvco      = self["kvco"]
        fv2i      = self["fv2i"]
        fref      = self["fref"]
        fb_delay  = self["fb_delay"]
        ph_offset = self["ph_offset"]
        #----------------------------------------------------------------------
        # write executable PLL script
        #----------------------------------------------------------------------
        print("writing PLL to %s" % (filename))
        timestamp = time.time()
        datetime  = time.asctime(time.localtime(timestamp))
        f = open(filename, "w")
        f.write("#! /usr/bin/env python\n")
        f.write("#" * 72 + "\n")
        f.write("# NAME : %s\n" % (filename))
        f.write("# CREATED BY : PLL\n")
        f.write("# DATE : %s\n" % (datetime))
        f.write("#" * 72 + "\n")
        f.write("import decida\n")
        f.write("from decida.PLL import PLL\n")
        f.write("PLL(\n")
        f.write("    npts=%s,\n"        % (npts))
        f.write("    fmin=%s,\n"        % (fmin))
        f.write("    fmax=%s,\n"        % (fmax))
        f.write("    rf=%s,\n"          % (rf))
        f.write("    cf=%s,\n"          % (cf))
        f.write("    cd=%s,\n"          % (cd))
        f.write("    mp=%s,\n"          % (mp))
        f.write("    icp=%s,\n"         % (icp))
        f.write("    kvco=%s,\n"        % (kvco))
        f.write("    fv2i=%s,\n"        % (fv2i))
        f.write("    fref=%s,\n"        % (fref))
        f.write("    fb_delay=%s,\n"    % (fb_delay))
        f.write("    ph_offset=%s,\n"   % (ph_offset))
        f.write(")\n")
        f.close()
        os.chmod(filename, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)
    #--------------------------------------------------------------------------
    # METHOD  : write_data
    # PURPOSE : write pll data to file
    #--------------------------------------------------------------------------
    def write_data(self, filename=None) :
        """ write the calculated data to a file.

        **arguments**:

            **filename** (str, default=None)

                Specify the file to write.  If not specified, use file dialog
                to specify the file.

        **results**:

            * Writes space-separated value format file with the calculated
              transfer functions.

        """
        if not filename :
            initialfile = "%s.col" % (self.__pll_root)
            if sys.platform == "darwin" :
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "PLL data file name to save?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".col",
                )
            else:
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "PLL data file name to save?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".col",
                    filetypes = (
                        ("space-separated data format files", "*.col"),
                        ("space-separated data format files", "*.ssv"),
                        ("all files", "*")
                    )
                )
        if not filename :
            return
        self.__pll_root = os.path.splitext(os.path.basename(filename))[0]
        self.__data_obj.write_ssv(filename)
    #--------------------------------------------------------------------------
    # METHOD  : write_plot
    # PURPOSE : write pll plot to file
    #--------------------------------------------------------------------------
    def write_plot(self, filename=None) :
        """ write a PostScript plot to a file.

        **arguments**:

            **filename** (str, default=None)

                Specify the file to write.  If not specified, use file dialog
                to specify the file.

        **results**:

            * Writes a PostScript file with the current plot.

        """
        if not filename :
            initialfile = "%s.ps" % (self.__pll_root)
            if sys.platform == "darwin" :
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "PLL plot file name to save?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".ps",
                )
            else:
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "PLL plot file name to save?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".ps",
                    filetypes = (
                        ("PostScript format files", "*.ps"),
                        ("PostScript format files", "*.eps"),
                        ("all files", "*")
                    )
                )
        if not filename :
            return
        plotwin = self.__dataview.plot_window()
        plotwin.itemconfigure("CROSSHAIRS", state="hidden")
        plotwin.postscript(file=filename, rotate=True, pagewidth="10.5i")
        plotwin.itemconfigure("CROSSHAIRS", state="normal")
    #--------------------------------------------------------------------------
    # METHOD  : write_report
    # PURPOSE : write pll report to file
    #--------------------------------------------------------------------------
    def write_report(self, filename=None) :
        """ write PLL report to a file.

        **arguments**:

            **filename** (str, default=None)

                Specify the file to write.  If not specified, use file dialog
                to specify the file.

        **results**:

            * Writes a formatted PLL report to the file.

        """
        if not filename :
            initialfile = "%s.report" % (self.__pll_root)
            if sys.platform == "darwin" :
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "PLL report file name to save?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".ps",
                )
            else :
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "PLL report file name to save?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".ps",
                    filetypes = (
                        ("Text format files", "*.txt"),
                        ("Text format files", "*.report"),
                        ("all files", "*")
                    )
                )
        if not filename :
            return
        f = open(filename, "w")
        f.write(self.report(1))
        f.close()
    #--------------------------------------------------------------------------
    # METHOD  : __help_cmd
    # PURPOSE : help
    #--------------------------------------------------------------------------
    def __help_cmd(self) :
        print("not implemented yet")
