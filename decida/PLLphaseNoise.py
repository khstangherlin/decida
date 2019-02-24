################################################################################
# CLASS    : PLLphaseNoise
# PURPOSE  : calculate phase-noise characteristics
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:22:17 2013
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
import sys
import os
import os.path
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

class PLLphaseNoise(ItclObjectx, tk.Frame) :
    """
    **synopsis**:

        Phase-Locked Loop phase noise analysis.

        *PLLphaseNoise* calculates the frequency-domain noise power spectra
        of a PLL.  The different noise components within
        the PLL are specified by different models for the noise, and each
        component's effect on the output of the PLL is calculated by the
        respective transfer-function from the place within the PLL to the
        output.

        *PLLphaseNoise* has two modes of use.  The first is an interactive
        mode, with a graphical user-interface.  In the interactive mode,
        the user changes an input PLL parameter value, or noise model
        parameter in the entry box and presses <Return> to cause a new set
        of calculations to be performed and displayed.

        In the non-interactive mode, *PLLphaseNoise* can be embedded in a
        script involving one or more loops of calculations.  In this mode,
        use the *recalculate* user method.  After re-calculation, PLL and
        phase-noise metrics can be reported to a file.

        The DeCiDa application *pll_phase_noise* simply instantiates
        one *PLLphaseNoise* object.

    **constructor arguments**:

        **parent** (tk handle, default=None)

              handle of frame or other widget to pack PLLphaseNoise in.
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

                * 0 : plot Output Noise Power

                * 1 : plot Noise Sources

                * 2 : plot Transfer Functions

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

        **temp_c** (float, default=25.0)

            Circuit temperature. [C]

        **ref_af2** (float, default=1e_5)

            REF (1/freq^2) noise power. [rad^2*Hz]

        **ref_af3** (float, default=1)

            REF (1/freq^3) noise power. [rad^2*Hz^2]

        **ref_af0** (float, default=1e_16)

            REF noise power floor. [rad^2/Hz]

        **pfd_trst** (float, default=300e_12)

            Phase-Frequency Detector reset time. [s]

        **icp_beta** (float, default=900e_6)

            Charge-pump output transistor transconductance parameter. [A/V^2]

        **icp_af1** (float, default=1e_14)

            Charge-pump current 1/f coefficient. [A^2]

        **vco_af2** (float, default=100.0)

            VCO (1/freq^2) noise power. [rad^2*Hz]

        **vco_af3** (float, default=1e7)

            VCO (1/freq^3) noise power. [rad^2*Hz^2]

        **vco_af0** (float, default=1e_16)

            VCO noise power floor. [rad^2/Hz]

        **snddb** (float, default=_150.0)

            Feedback divider noise power. [rad^2/Hz]

        **snxdb** (float, default=_400.0)

            Excess VCO noise power. [rad^2/Hz]

        **fspurx** (float, default=1.0e6)

            Noise spur 1 (at VCO output) frequency. [Hz]

        **pspurx** (float, default=_400.0)

            Noise spur 1 (at VCO output) power. [rad^2/Hz]

        **aspurx** (float, default=32)

            Noise spur 1 (at VCO output) exponent.

        **fspurv** (float, default=1.5e6)

            Noise spur 2 (at VCO input) frequency. [Hz]

        **pspurv** (float, default=_400.0)

            Noise spur 2 (at VCO input) power. [V^2/Hz]

        **aspurv** (float, default=32)

            Noise spur 2 (at VCO input) exponent.

        **fspurd** (float, default=1.5e6)

            Noise spur 3 (at divider output) frequency. [Hz]

        **pspurd** (float, default=_400.0)

            Noise spur 3 (at divider output) power. [rad^2/Hz]

        **aspurd** (float, default=32)

            Noise spur 3 (at divider output) exponent.

    **example** (from test_PLLphaseNoise): ::

        from decida.PLLphaseNoise import PLLphaseNoise
        PLLphaseNoise()

    **public methods**:

        * public methods from *ItclObjectx*

    """
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
        self.__pll_root = "PLLphaseNoise"
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
            "plot_style"     : [0,            self._config_plot_style_callback],
            "plot_orient"    : ["horizontal", self._config_plot_orient_callback],
            "plot_title"     : ["",         self._config_plot_title_callback],
            "npts"           : [1000,       self._config_npts_callback],
            "fmax"           : [1e10,       self._config_fmax_callback],
            "fmin"           : [1e2,        self._config_fmin_callback],
            "rf"             : [10e3,       self._config_rf_callback],
            "cf"             : [500e-12,    self._config_cf_callback],
            "cd"             : [5e-12,      self._config_cd_callback],
            "mp"             : [40.0,       self._config_mp_callback],
            "icp"            : [100e-6,     self._config_icp_callback],
            "kvco"           : [700e6,      self._config_kvco_callback],
            "fv2i"           : [100e9,      self._config_fv2i_callback],
            "fref"           : [350e6,      self._config_fref_callback],
            "temp_c"         : [25.0,       self._config_temp_c_callback],
            "ref_af2"        : [1e-5,       self._config_ref_af2_callback],
            "ref_af3"        : [1,          self._config_ref_af3_callback],
            "ref_af0"        : [1e-16,      self._config_ref_af0_callback],
            "pfd_trst"       : [300e-12,    self._config_pfd_trst_callback],
            "icp_beta"       : [900e-6,     self._config_icp_beta_callback],
            "icp_af1"        : [1e-14,      self._config_icp_af1_callback],
            "vco_af2"        : [100.0,      self._config_vco_af2_callback],
            "vco_af3"        : [1e7,        self._config_vco_af3_callback],
            "vco_af0"        : [1e-16,      self._config_vco_af0_callback],
            "snddb"          : [-150.0,     self._config_snddb_callback],
            "snxdb"          : [-400.0,     self._config_snxdb_callback],
            "fspurx"         : [1.0e6,      self._config_fspurx_callback],
            "pspurx"         : [-400.0,     self._config_pspurx_callback],
            "aspurx"         : [32,         self._config_aspurx_callback],
            "fspurv"         : [1.5e6,      self._config_fspurv_callback],
            "pspurv"         : [-400.0,     self._config_pspurv_callback],
            "aspurv"         : [32,         self._config_aspurv_callback],
            "fspurd"         : [1.5e6,      self._config_fspurd_callback],
            "pspurd"         : [-400.0,     self._config_pspurd_callback],
            "aspurd"         : [32,         self._config_aspurd_callback],
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
    # PLLphaseNoise configuration option callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _config_plot_style_callback
    # PURPOSE : configure plot_style
    #==========================================================================
    def _config_plot_style_callback(self) :
        if not self["plot_style"] in (0, 1, 2) :
            self.warning("plot_style must be one of: ",
                "    0 : plot Output Noise Power",
                "    1 : plot Noise Sources",
                "    2 : plot Transfer Functions",
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
    # METHOD  : _config_temp_c_callback
    # PURPOSE : configure temp_c
    #==========================================================================
    def _config_temp_c_callback(self) :
        self.__entry_enter("temp_c")
    #==========================================================================
    # METHOD  : _config_pfd_trst_callback
    # PURPOSE : configure pfd_trst
    #==========================================================================
    def _config_pfd_trst_callback(self) :
        self.__entry_enter("pfd_trst")
    #==========================================================================
    # METHOD  : _config_icp_beta_callback
    # PURPOSE : configure icp_beta
    #==========================================================================
    def _config_icp_beta_callback(self) :
        self.__entry_enter("icp_beta")
    #==========================================================================
    # METHOD  : _config_icp_af1_callback
    # PURPOSE : configure icp_af1
    #==========================================================================
    def _config_icp_af1_callback(self) :
        self.__entry_enter("icp_af1")
    #==========================================================================
    # METHOD  : _config_ref_af2_callback
    # PURPOSE : configure ref_af2
    #==========================================================================
    def _config_ref_af2_callback(self) :
        self.__entry_enter("ref_af2")
    #==========================================================================
    # METHOD  : _config_ref_af3_callback
    # PURPOSE : configure ref_af3
    #==========================================================================
    def _config_ref_af3_callback(self) :
        self.__entry_enter("ref_af3")
    #==========================================================================
    # METHOD  : _config_ref_af0_callback
    # PURPOSE : configure ref_af0
    #==========================================================================
    def _config_ref_af0_callback(self) :
        self.__entry_enter("ref_af0")
    #==========================================================================
    # METHOD  : _config_vco_af2_callback
    # PURPOSE : configure vco_af2
    #==========================================================================
    def _config_vco_af2_callback(self) :
        self.__entry_enter("vco_af2")
    #==========================================================================
    # METHOD  : _config_vco_af3_callback
    # PURPOSE : configure vco_af3
    #==========================================================================
    def _config_vco_af3_callback(self) :
        self.__entry_enter("vco_af3")
    #==========================================================================
    # METHOD  : _config_vco_af0_callback
    # PURPOSE : configure vco_af0
    #==========================================================================
    def _config_vco_af0_callback(self) :
        self.__entry_enter("vco_af0")
    #==========================================================================
    # METHOD  : _config_snddb_callback
    # PURPOSE : configure snddb
    #==========================================================================
    def _config_snddb_callback(self) :
        self.__entry_enter("snddb")
    #==========================================================================
    # METHOD  : _config_snxdb_callback
    # PURPOSE : configure snxdb
    #==========================================================================
    def _config_snxdb_callback(self) :
        self.__entry_enter("snxdb")
    #==========================================================================
    # METHOD  : _config_fspurx_callback
    # PURPOSE : configure fspurx
    #==========================================================================
    def _config_fspurx_callback(self) :
        self.__entry_enter("fspurx")
    #==========================================================================
    # METHOD  : _config_pspurx_callback
    # PURPOSE : configure pspurx
    #==========================================================================
    def _config_pspurx_callback(self) :
        self.__entry_enter("pspurx")
    #==========================================================================
    # METHOD  : _config_aspurx_callback
    # PURPOSE : configure aspurx
    #==========================================================================
    def _config_aspurx_callback(self) :
        self.__entry_enter("aspurx")
    #==========================================================================
    # METHOD  : _config_fspurv_callback
    # PURPOSE : configure fspurv
    #==========================================================================
    def _config_fspurv_callback(self) :
        self.__entry_enter("fspurv")
    #==========================================================================
    # METHOD  : _config_pspurv_callback
    # PURPOSE : configure pspurv
    #==========================================================================
    def _config_pspurv_callback(self) :
        self.__entry_enter("pspurv")
    #==========================================================================
    # METHOD  : _config_aspurv_callback
    # PURPOSE : configure aspurv
    #==========================================================================
    def _config_aspurv_callback(self) :
        self.__entry_enter("aspurv")
    #==========================================================================
    # METHOD  : _config_fspurd_callback
    # PURPOSE : configure fspurd
    #==========================================================================
    def _config_fspurd_callback(self) :
        self.__entry_enter("fspurd")
    #==========================================================================
    # METHOD  : _config_pspurd_callback
    # PURPOSE : configure pspurd
    #==========================================================================
    def _config_pspurd_callback(self) :
        self.__entry_enter("pspurd")
    #==========================================================================
    # METHOD  : _config_aspurd_callback
    # PURPOSE : configure aspurd
    #==========================================================================
    def _config_aspurd_callback(self) :
        self.__entry_enter("aspurd")
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
            if isinstance(val, int) :
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
        temp_c    = self["temp_c"]
        ref_af2   = self["ref_af2"]
        ref_af3   = self["ref_af3"]
        ref_af0   = self["ref_af0"]
        pfd_trst  = self["pfd_trst"]
        icp_beta  = self["icp_beta"]
        icp_af1   = self["icp_af1"]
        vco_af2   = self["vco_af2"]
        vco_af3   = self["vco_af3"]
        vco_af0   = self["vco_af0"]
        snddb     = self["snddb"]
        snxdb     = self["snxdb"]
        fspurx    = self["fspurx"]
        pspurx    = self["pspurx"]
        aspurx    = self["aspurx"]
        fspurv    = self["fspurv"]
        pspurv    = self["pspurv"]
        aspurv    = self["aspurv"]
        fspurd    = self["fspurd"]
        pspurd    = self["pspurd"]
        aspurd    = self["aspurd"]
        #----------------------------------------
        # calculated parameters
        #----------------------------------------
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
        #--------------------------------------------------------------------
        # 2nd order loop-filter:
        #--------------------------------------------------------------------
        d.cxset("Z = %g + 1.0/(S*%g)" % (rf, cf))
        #--------------------------------------------------------------------
        # 3rd order loop-filter:
        #--------------------------------------------------------------------
        if cd > 0.0 :
            d.cxset("Z = 1.0/(1.0/Z + S*%g)" % (cd))
        #--------------------------------------------------------------------
        # transfer functions for different noise sources:
        #--------------------------------------------------------------------
        Ko = kvco * (2.0*math.pi)
        Kd = icp  / (2.0*math.pi)
        K  = Ko * Kd

        d.cxset("pre = %g/(S*%g + Z*%g)" % (mp, mp, K))
        d.cxset("Hr  = pre * Z*%g" % (K))   # NTF_IN
        d.cxset("Hd  = -Hr")                # NTF_DIV
        d.cxset("Hi  = pre * %g*Z" % (Ko))  # NTF_CP
        d.cxset("Hv  = pre * %g"   % (Ko))  # NTF_R
        d.cxset("Hx  = pre * S")            # NTF_VCO

        d.cxmag("Hr")
        d.cxmag("Hd")
        d.cxmag("Hv")
        d.cxmag("Hi")
        d.cxmag("Hx")
        d.set("Hr2 = MAG(Hr) * MAG(Hr)")
        d.set("Hd2 = MAG(Hd) * MAG(Hd)")
        d.set("Hi2 = MAG(Hi) * MAG(Hi)")
        d.set("Hv2 = MAG(Hv) * MAG(Hv)")
        d.set("Hx2 = MAG(Hx) * MAG(Hx)")
        #--------------------------------------------------------------------
        # different noise sources:
        #--------------------------------------------------------------------
        ssndiv = math.pow(10.0, snddb*0.1)   # excess divider noise
        ssnexc = math.pow(10.0, snxdb*0.1)   # excess noise at VCO output
        kb     = 1.380622e-23
        T      = temp_c + 273.16
        pfd_ru = pfd_trst*fref               # ratio of pfd reset to update
        icp_gm = math.sqrt(2.0*icp*icp_beta) # gm of charge-pump output dev
        icp_in = 2.0*kb*T*(8.0/3.0)*icp_gm   # charge-pump noise (nmos/pmos)
        lpf_vn = 4.0*kb*T*rf                 # loop-filter resistor noise
        if False :
            print("gm=%s in=%s vn=%s" % (icp_gm, icp_in, lpf_vn))
        # resistor noise to LPF output
        if cd > 0:
            cdf = cd*cf/(cd+cf)
            d.cxset("Hrlpf = %g/(1.0+S*%g)" % (cdf/cd, rf*cdf))
            d.cxmag("Hrlpf")
            d.set("Hrlpf2 = MAG(Hrlpf) * MAG(Hrlpf)")
        else :
            d.set("Hrlpf2 = 1")
        # charge-pump, lpf, excess, reference, vco:
        # Snicp = [2*(4*kb*T*2/3)*gm + KF*Id^AF/(f*Cox*L^2)]*pfd_rst/period
        d.set("Snicp = (%g + %g*%g/freq)*%g"  % (icp_in, icp_af1, icp, pfd_ru))
        d.set("Snlpf = %g*Hrlpf2)"                 % (lpf_vn))
        d.set("Sndiv = %g"                         % (ssndiv))
        d.set("Snexc = %g"                         % (ssnexc))
        d.set("Snref = %g/(freq^2)+%g/(freq^3)+%g" % (ref_af2, ref_af3, ref_af0))
        d.set("Snvco = %g/(freq^2)+%g/(freq^3)+%g" % (vco_af2, vco_af3, vco_af0))
        d.set("Soicp = Snicp * Hi2")
        d.set("Solpf = Snlpf * Hv2")
        d.set("Sodiv = Sndiv * Hd2")
        d.set("Soexc = Snexc * Hx2")
        d.set("Soref = Snref * Hr2")
        d.set("Sovco = Snvco * Hx2")

        # spurs:
        sspurx = math.pow(10.0, pspurx*0.1) * 2.0/math.pi
        sspurv = math.pow(10.0, pspurv*0.1) * 2.0/math.pi
        sspurd = math.pow(10.0, pspurd*0.1) * 2.0/math.pi

        if True :
            d.set("fan = (freq/%g)^%g"                     % (fspurx, aspurx))
            d.set("Spurx = max(1e-80, 2*%g*fan/(1+fan^2))" % (sspurx))
            d.set("fan = (freq/%g)^%g"                     % (fspurv, aspurv))
            d.set("Spurv = max(1e-80, 2*%g*fan/(1+fan^2))" % (sspurv))
            d.set("fan = (freq/%g)^%g"                     % (fspurd, aspurd))
            d.set("Spurd = max(1e-80, 2*%g*fan/(1+fan^2))" % (sspurd))
        else :
            d.set("Spurx = 1e-80")
            d.set("Spurv = 1e-80")
            d.set("Spurd = 1e-80")

        d.set("Sospurx = Spurx * Hx2")
        d.set("Sospurv = Spurv * Hv2")
        d.set("Sospurd = Spurd * Hd2")

        # total noise power
        d.set("So = Soref + Sodiv + Soicp + Solpf + Sovco + Soexc + Sospurx + Sospurv + Sospurd")

        # integrate reference for jitter
        d.set("Ja_inp = integ(Snref, freq)")
        ja_inp  = d.get_entry(-1, "Ja_inp")
        ja_inp  = math.sqrt(ja_inp)/(2.0*math.pi*fref)

        # integrate outputs for jitter
        fvco = mp*fref
        d.set("Ja = integ(So, freq)")
        ja  = d.get_entry(-1, "Ja")
        ja  = math.sqrt(ja)/(2.0*math.pi*fvco)

        d.set("Ja_ref = integ(Soref, freq)")
        ja_ref  = d.get_entry(-1, "Ja_ref")
        ja_ref  = math.sqrt(ja_ref)/(2.0*math.pi*fvco)

        d.set("Ja_div = integ(Sodiv, freq)")
        ja_div  = d.get_entry(-1, "Ja_div")
        ja_div  = math.sqrt(ja_div)/(2.0*math.pi*fvco)

        d.set("Ja_icp = integ(Soicp, freq)")
        ja_icp  = d.get_entry(-1, "Ja_icp")
        ja_icp  = math.sqrt(ja_icp)/(2.0*math.pi*fvco)

        d.set("Ja_lpf = integ(Solpf, freq)")
        ja_lpf  = d.get_entry(-1, "Ja_lpf")
        ja_lpf  = math.sqrt(ja_lpf)/(2.0*math.pi*fvco)

        d.set("Ja_vco = integ(Sovco, freq)")
        ja_vco  = d.get_entry(-1, "Ja_vco")
        ja_vco  = math.sqrt(ja_vco)/(2.0*math.pi*fvco)

        # convert to power in dB for plots
        for col in ["So",
            "Soref", "Sodiv", "Soicp", "Solpf", "Sovco", "Soexc",
            "Snref", "Sndiv", "Snicp", "Snlpf", "Snvco", "Snexc",
            "Spurx", "Spurv", "Spurd"
        ] :
            d.set("%s = 10.0*log10(max(%s, 1e-200))" % (col, col))
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
        self.__Parameters["fvco"] = fvco
        self.__Parameters["ja"]     = ja
        self.__Parameters["ja_inp"] = ja_inp
        self.__Parameters["ja_ref"] = ja_ref
        self.__Parameters["ja_div"] = ja_div
        self.__Parameters["ja_icp"] = ja_icp
        self.__Parameters["ja_lpf"] = ja_lpf
        self.__Parameters["ja_vco"] = ja_vco
    #==========================================================================
    # METHOD  : plot
    # PURPOSE : plot transfer functions
    #==========================================================================
    def plot(self, new=False) :
        self.__calculate()
        plot_style = self["plot_style"]
        if   plot_style == 0:
            title   = "Output Phase Noise Power"
            columns = "freq Soref Sodiv Soicp Solpf Sovco Soexc So"
            colors  = ["red", "orange", "green", "blue", "violet", "cyan", "black"]
            wlines  = [2, 2, 2, 2, 2, 2, 4]
            ytitle  = "Output Phase Noise Power [dBc/Hz]"
            ymin    = -200
            ymax    =   50
            yaxis   = "lin"
        elif plot_style == 1:
            title   = "Noise Sources"
            columns = "freq Snref Sndiv Snicp Snlpf Snvco Snexc Spurx Spurv Spurd"
            colors  = ["red", "orange", "green", "blue", "violet", "cyan", "gray", "gray", "gray"]
            wlines  = [2, 2, 2, 2, 2, 2, 2, 2, 2]
            ytitle  = "Noise Sources"
            ymin    =  -200
            ymax    =  200
            yaxis   = "lin"
        elif plot_style == 2:
            title   = "Transfer Functions"
            columns = "freq DB(Hr) DB(Hd) DB(Hi) DB(Hv) DB(Hx)"
            colors  = ["red", "orange", "green", "blue", "violet"]
            wlines  = [2, 2, 2, 2, 2]
            ytitle  = "Transfer Functions"
            ymin    = -200
            ymax    =  200
            yaxis   = "lin"
        if new or not self.__mapped :
            if self.__dataview is not None :
                self.__dataview.destroy()
                del self.__dataview
            fplt = self.__Component["plot_frame"]
            fplt.pack_forget()
            self.__dataview = XYplotm(fplt,
                use_matplotlib=self.__use_matplotlib,
                plot_height=self["plot_height"],
                plot_width=self["plot_width"],
                command=[self.__data_obj, columns], xaxis="log",
                ymin=ymin, ymax=ymax, yaxis=yaxis,
                colors=colors, wlines=wlines,
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
    # PLLphaseNoise GUI
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
            self.option_add("*PLLphaseNoise*Menubutton.width", 10)
            self.option_add("*PLLphaseNoise*Menubutton.height", 1)
            self.option_add("*PLLphaseNoise*Label.anchor", "e")
            self.option_add("*PLLphaseNoise*Label.bd", 2)
            self.option_add("*PLLphaseNoise*Label.relief", "sunken")
            self.option_add("*PLLphaseNoise*Label.font", "Courier 18 normal")
            self.option_add("*PLLphaseNoise*Entry.background", "Ghost White")
            self.option_add("*PLLphaseNoise*Entry.width", 10)
            self.option_add("*PLLphaseNoise*Entry.font", "Courier 18 normal")
            self.option_add("*PLLphaseNoise*Entry.highlightThickness", 0)
            self.option_add("*PLLphaseNoise*Text.background", "Ghost White")
            self.option_add("*PLLphaseNoise*Text.width", 20)
            self.option_add("*PLLphaseNoise*Text.height",18)
            self.option_add("*PLLphaseNoise*Text*font", "Courier 18 normal")
        else :
            self.option_add("*PLLphaseNoise*Menubutton.width", 10)
            self.option_add("*PLLphaseNoise*Menubutton.height", 1)
            self.option_add("*PLLphaseNoise*Label.anchor", "e")
            self.option_add("*PLLphaseNoise*Label.bd", 2)
            self.option_add("*PLLphaseNoise*Label.relief", "sunken")
            self.option_add("*PLLphaseNoise*Label.font", "Courier 12 normal")
            self.option_add("*PLLphaseNoise*Entry.background", "Ghost White")
            self.option_add("*PLLphaseNoise*Entry.width", 15)
            self.option_add("*PLLphaseNoise*Entry.font", "Courier 12 normal")
            self.option_add("*PLLphaseNoise*Entry.highlightThickness", 0)
            self.option_add("*PLLphaseNoise*Text.background", "Ghost White")
            self.option_add("*PLLphaseNoise*Text.width",  20)
            self.option_add("*PLLphaseNoise*Text.height", 18)
            self.option_add("*PLLphaseNoise*Text.font", "Courier 12 normal")
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
        tobj = tk.Text(ftxt, relief="sunken", bd=2, height=5, width=30)
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
            label="Write PLLphaseNoise script",
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
            (0,  "plot Output Noise Power"),
            (1,  "plot Noise Sources"),
            (2,  "plot Transfer Functions"),
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
            ["npts",    "number of samples"],
            ["fmin",    "minimum frequency [Hz]"],
            ["fmax",    "maximum frequency [Hz]"],
            ["rf",      "LPF resistor [ohm]"],
            ["cf",      "LPF capacitor [F]"],
            ["cd",      "LPF ripple-bypass capacitor [F]"],
            ["mp",      "DIV feed-back divider value"],
            ["icp",     "ICP current [A]"],
            ["kvco",    "VCO gain [Hz/V]"],
            ["fv2i",    "V2I pole [Hz]"],
            ["fref",    "REF frequency [Hz]"],
            ["temp_c",  "temperature [C]"],
            ["ref_af2", "REF noise power (1/f^2) (phase)"],
            ["ref_af3", "REF noise power (1/f^3) (phase)"],
            ["ref_af0", "REF noise power (floor) (phase)"],
            ["pfd_trst","PFD reset time [s]"],
            ["icp_beta","ICP output transistor beta [A/V^2]"],
            ["icp_af1", "ICP current (1/f) coefficient"],
            ["vco_af2", "VCO noise power (1/f^2)"],
            ["vco_af3", "VCO noise power (1/f^3)"],
            ["vco_af0", "VCO noise power (floor)"],
            ["snddb",     "DIV feedback divider noise power  (phase)"],
            ["snxdb",   "Excess VCO noise power (phase)"],
            ["fspurx",  "spur #1 (@ VCO output) frequency"],
            ["pspurx",  "spur #1 power"],
            ["aspurx",  "spur #1 exponent"],
            ["fspurv",  "spur #2 (@ VCO input)  frequency"],
            ["pspurv",  "spur #2 power"],
            ["aspurv",  "spur #2 exponent"],
            ["fspurd",  "spur #3 (@ DIV output) frequency"],
            ["pspurd",  "spur #3 power"],
            ["aspurd",  "spur #3 exponent"],
        ) :
            var, text = item
            val = self[var]
            f = tk.Frame(cont, relief="flat")
            f.pack(side="top", expand=False, fill="x")
            l = tk.Label(f, relief="flat", anchor="w", text=text, width=35)
            l.pack(side="left", expand=True, fill="x")
            l = tk.Label(f, relief="flat", anchor="w", text=var,  width=10)
            l.pack(side="left", expand=True, fill="x")
            e = tk.Entry(f, relief="sunken", bd=3)
            e.pack(side="left", expand=True, fill="x")
            self.__Component["%s_label" % (var)] = l
            self.__Component["%s_entry" % (var)] = e
            e.delete(0, "end")
            if isinstance(val, int) :
                e.insert(0, "%s" % (val))
            else:
                e.insert(0, "%g" % (val))
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
    # PLLphaseNoise user commands
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #--------------------------------------------------------------------------
    # METHOD  : recalculate
    # PURPOSE : force re-calculation
    #--------------------------------------------------------------------------
    def recalculate(self) :
        """ recalculate transfer functions, and output phase-noise.

        **results**:

            * Frequency domain transfer functions are re-calculated,
              noise models are updated, and output phase-noise per component
              is calculated and displayed.   For non-gui applications, several
              metrics are also calculated.

        """
        self.__calculate()
    #--------------------------------------------------------------------------
    # METHOD  : get
    # PURPOSE : get a parameter
    # NOTES :
    #    * for non-gui applications
    #--------------------------------------------------------------------------
    def get(self, par) :
        """ get a PLLphaseNoise parameter or metric.

        **arguments**:

            **par** (str)

                PLLphaseNoise configuration option or one of the following metrics:

                * lpll   : PLL inductance, mp/(Kvco*Icp)
                * zo     : PLL characteristic impedance, sqrt(lpll/cf)
                * zeta   : PLL damping coefficient
                * Q      : PLL quality factor
                * wn     : PLL natural frequency [rad/s]
                * wb     : PLL bandwidth [rad/s]
                * wz     : PLL zero frequency [rad/s]
                * wp     : PLL peak frequency [rad/s]
                * wh     : PLL high zeta frequency [rad/s]
                * wv     : PLL V to I converter frequency [rad/s]
                * peak   : PLL peak closed-loop jitter transfer value [dB]
                * zeth   : PLL high-frequency damping factor
                * fn     : PLL natural frequency [Hz]
                * fb     : PLL bandwidth [Hz]
                * fz     : PLL zero frequency [Hz]
                * fp     : PLL peak frequency [Hz]
                * fh     : PLL high frequency [Hz]
                * fvco   : VCO frequency [Hz]
                * ja     : Total absolute jitter at PLL output [s]
                * ja_inp : Absolute jitter at PLL input reference noise [s]
                * ja_ref : Absolute jitter at PLL output from reference noise [s]
                * ja_div : Absolute jitter at PLL output from divider noise [s]
                * ja_icp : Absolute jitter at PLL output from charge-pump noise [s]
                * ja_lpf : Absolute jitter at PLL output from loop-filter noise [s]
                * ja_vco : Absolute jitter at PLL output from VCO noise [s]

        """
        if par in self.__Parameters :
            return self.__Parameters[par]
        elif par in self.config_options() :
            return self[par]
        print("parameter \"%s\" is not available" % (par))
        return 0
    #--------------------------------------------------------------------------
    # METHOD  : report
    # PURPOSE : return formatted PLLphaseNoise parameters report
    #--------------------------------------------------------------------------
    def report(self, style=1) :
        """ return a formated PLLphaseNoise parameters report.

        **arguments**:

            **style** (int, default=1)

                The style of the report to generate:

                  1. verbose
                  2. brief

        **results**:

            * Returns a formatted PLLphaseNoise report with various parameters
              and metrics.

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
        fvco = self.__Parameters["fvco"]
        ja     = self.__Parameters["ja"]
        ja_inp = self.__Parameters["ja_inp"]
        ja_ref = self.__Parameters["ja_ref"]
        ja_div = self.__Parameters["ja_div"]
        ja_icp = self.__Parameters["ja_icp"]
        ja_lpf = self.__Parameters["ja_lpf"]
        ja_vco = self.__Parameters["ja_vco"]
        if style==1 :
            rpt = """
                :
                : ==================================================
                : PLLphaseNoise report: %s
                : ==================================================
                :
                : Feed-backdivider value     M+1    = %d
                : Loop-filter res.           Rf     = %-12.5g Kohm
                : Loop-filter cap.           Cf     = %-12.5g pF
                : Loop-filter ripple-byp cap Cd     = %-12.5g pF
                : Charge-pump current        Icp    = %-12.5g uA
                : VCO gain                   Kvco   = %-12.5g MHz/V
                : V2I pole                   fv2i   = %-12.5g MHz
                : Reference frequency        fref   = %-12.5g MHz
                : VCO frequency              fvco   = %-12.5g MHz
                :
                : Loop-filter zero-freq.     fzero  = %-12.5g MHz
                : PLL natural freq.          fnat   = %-12.5g MHz
                : PLL bandwidth (2d-order)   fbw    = %-12.5g MHz
                : Loop-filter pole-freq.     fpole  = %-12.5g MHz
                : PLL HF natural freq.       fnatH  = %-12.5g MHz
                : LF damping factor          zetaL  = %-12.5g
                : HF damping factor          zetaH  = %-12.5g
                : Damping factor             zeta   = %-12.5g
                :
                : INP abs  jitter (RMS)      ja_inp = %-12.5g ps
                : REF abs  jitter (RMS)      ja_ref = %-12.5g ps
                : DIV abs  jitter (RMS)      ja_div = %-12.5g ps
                : ICP abs  jitter (RMS)      ja_icp = %-12.5g ps
                : LPF abs  jitter (RMS)      ja_lpf = %-12.5g ps
                : VCO abs  jitter (RMS)      ja_vco = %-12.5g ps
                : ______________________________________________
                : TOT abs  jitter (RMS)      ja     = %-12.5g ps
                :
            """ % (
                self.__pll_root,
                mp, rf*1e-3, cf*1e12, cd*1e12, icp*1e6,
                kvco*1e-6, fv2i*1e-6, fref*1e-6, fvco*1e-6,
                fz*1e-6, fn*1e-6, fb*1e-6,
                fp*1e-6, fh*1e-6, zeta, zeth, min(zeta,zeth),
                ja_inp*1e12,
                ja_ref*1e12, ja_div*1e12,
                ja_icp*1e12, ja_lpf*1e12, ja_vco*1e12,
                ja*1e12,
            )
        elif style==2 :
            rpt = """
                :fvco  = %-12.5g MHz
                :fzero = %-12.5g MHz
                :fnat  = %-12.5g MHz
                :fbw   = %-12.5g MHz
                :fpole = %-12.5g MHz
                :fnatH = %-12.5g MHz
                :zetaL = %-12.5g
                :zetaH = %-12.5g
                :zeta  = %-12.5g
                :
                :ja_rms_inp = %-12.5g ps
                :ja_rms_ref = %-12.5g ps
                :ja_rms_div = %-12.5g ps
                :ja_rms_icp = %-12.5g ps
                :ja_rms_lpf = %-12.5g ps
                :ja_rms_vco = %-12.5g ps
                :_______________________
                :ja_rms_tot = %-12.5g ps
                :
            """ % (
                fvco*1e-6, fz*1e-6, fn*1e-6, fb*1e-6, fp*1e-6, fh*1e-6,
                zeta, zeth, min(zeta,zeth),
                ja_inp*1e12,
                ja_ref*1e12, ja_div*1e12,
                ja_icp*1e12, ja_lpf*1e12, ja_vco*1e12,
                ja*1e12,
            )
        olines = []
        for line in rpt.split("\n") :
            tok = line.split(":")
            if len(tok) >= 2 :
                olines.append(tok[1])
        return("\n".join(olines))
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PLLphaseNoise GUI construction methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # PLLphaseNoise GUI file menu callback methods
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
        """ write an executable PLLphaseNoise script with the current parameter set.

        **arguments**:

            **filename** (str, default=None)

                Specify the file to write.  If not specified, use file dialog
                to specify the file.

        **results**:

            * Writes executable script, which when run displays the
              PLLphaseNoise output noise and
              transfer functions for the last set of PLLphaseNoise parameters.

        """
        if not filename :
            initialfile = "%s.pllpn" % (self.__pll_root)
            if sys.platform == "darwin" :
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "PLLphaseNoise file name to save?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".pllpn",
                )
            else:
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "PLLphaseNoise file name to save?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".pllpn",
                    filetypes = (
                        ("PLL pn/python files", "*.pllpn"),
                        ("PLL pn/python files", "*.py"),
                        ("all files", "*")
                    )
                )
        if not filename:
            return
        #-------------------------------
        # PLLphaseNoise parameters
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
        temp_c    = self["temp_c"]
        ref_af2   = self["ref_af2"]
        ref_af3   = self["ref_af3"]
        ref_af0   = self["ref_af0"]
        pfd_trst  = self["pfd_trst"]
        icp_beta  = self["icp_beta"]
        icp_af1   = self["icp_af1"]
        vco_af2   = self["vco_af2"]
        vco_af3   = self["vco_af3"]
        vco_af0   = self["vco_af0"]
        snddb     = self["snddb"]
        snxdb     = self["snxdb"]
        fspurx    = self["fspurx"]
        pspurx    = self["pspurx"]
        aspurx    = self["aspurx"]
        fspurv    = self["fspurv"]
        pspurv    = self["pspurv"]
        aspurv    = self["aspurv"]
        fspurd    = self["fspurd"]
        pspurd    = self["pspurd"]
        aspurd    = self["aspurd"]
        #----------------------------------------------------------------------
        # write executable PLLphasNoise script
        #----------------------------------------------------------------------
        print("writing PLLphaseNoise to %s" % (filename))
        timestamp = time.time()
        datetime  = time.asctime(time.localtime(timestamp))
        f = open(filename, "w")
        f.write("#! /usr/bin/env python\n")
        f.write("#" * 72 + "\n")
        f.write("# NAME : %s\n" % (filename))
        f.write("# CREATED BY : PLLphaseNoise\n")
        f.write("# DATE : %s\n" % (datetime))
        f.write("#" * 72 + "\n")
        f.write("import decida\n")
        f.write("from decida.PLLphaseNoise import PLLphaseNoise\n")
        f.write("PLLphaseNoise(\n")
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
        f.write("    temp_c=%s,\n"      % (temp_c))
        f.write("    ref_af2=%s,\n"     % (ref_af2))
        f.write("    ref_af3=%s,\n"     % (ref_af3))
        f.write("    ref_af0=%s,\n"     % (ref_af0))
        f.write("    pfd_trst=%s,\n"    % (pfd_trst))
        f.write("    icp_beta=%s,\n"    % (icp_beta))
        f.write("    icp_af1=%s,\n"     % (icp_af1))
        f.write("    vco_af2=%s,\n"     % (vco_af2))
        f.write("    vco_af3=%s,\n"     % (vco_af3))
        f.write("    vco_af0=%s,\n"     % (vco_af0))
        f.write("    snddb=%s,\n"       % (snddb))
        f.write("    snxdb=%s,\n"       % (snxdb))
        f.write("    fspurx=%s,\n"      % (fspurx))
        f.write("    pspurx=%s,\n"      % (pspurx))
        f.write("    aspurx=%s,\n"      % (aspurx))
        f.write("    fspurv=%s,\n"      % (fspurv))
        f.write("    pspurv=%s,\n"      % (pspurv))
        f.write("    aspurv=%s,\n"      % (aspurv))
        f.write("    fspurd=%s,\n"      % (fspurd))
        f.write("    pspurd=%s,\n"      % (pspurd))
        f.write("    aspurd=%s,\n"      % (aspurd))
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
              input and output noise and transfer functions.

        """
        if not filename :
            initialfile = "%s.col" % (self.__pll_root)
            if sys.platform == "darwin" :
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "PLLphaseNoise data file name to save?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".col",
                )
            else:
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "PLLphaseNoise data file name to save?",
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
                    title = "PLLphaseNoise plot file name to save?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".ps",
                )
            else:
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "PLLphaseNoise plot file name to save?",
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
        """ write PLLphaseNoise report to a file.

        **arguments**:

            **filename** (str, default=None)

                Specify the file to write.  If not specified, use file dialog
                to specify the file.

        **results**:

            * Writes a formatted PLLphaseNoise report to the file.

        """
        if not filename :
            initialfile = "%s.report" % (self.__pll_root)
            if sys.platform == "darwin" :
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "PLLphaseNoise report file name to save?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".ps",
                )
            else:
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "PLLphaseNoise report file name to save?",
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
