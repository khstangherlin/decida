################################################################################
# CLASS    : FormulaCalculator
# PURPOSE  : GUI for calculating simple formula
# AUTHOR   : Richard Booth
# DATE     : Sat Jun  2 11:55:18 EDT 2012
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
from builtins import object
import math
import tkinter as tk
from decida.entry_emacs_bindings import entry_emacs_bindings

class FormulaCalculator(object) :
    """
    **synopsis**:

        Simple formula calculator.

        A small calculator can be useful to evaluate a single formula involving
        a few parameters/variables. This formula calculator class constructs
        a small calculator which evaluates the formula or its inverse with
        respect to a particular parameter, according to specified code
        for each result.

        (originally posted as a Tcl/Tk application on wiki.tcl.tk)

    **constructor arguments**:

        **parent** (tk handle, default=None)

              handle of frame or other widget to pack plot in.
              if this is not specified, top-level is created.

        **par_specs** (list of lists of parameter specifications)

              each list of parameter specifications is: parameter name,
              text to be displayed for the parameter label in the GUI,
              units, initial value, key of equation recalculation formula.

        **recalc_specs** (list of lists of formula specifications)

              each list of recalculation specifications is: recalculation key,
              formula.

    **results**:

        * Sets up GUI for formula recalculation.

        * Changing and typing return in a parameter entry box re-evaluates
          the respective formula.

        * Emacs-style bindings switch between entry boxes:
          ^n and ^p  focus on next or previous entry windows, respectively

    **example** (from test_FormulaCalculator_1): ::

        from decida.FormulaCalculator import FormulaCalculator
        fc = FormulaCalculator(None,
            title="L-C oscillator",
            par_specs = [
                ["L",    "Inductance",  "pH", 1000.0, "f"],
                ["C",    "Capacitance", "pF",  25.00, "f"],
                ["freq", "Frequency",   "GHz",  1.00, "L"],
            ],
            recalc_specs = [
                ["f", "freq = 1e3/(2*pi*sqrt(L*C))"],
                ["L", "L    = 1e6/(C*pow(2*pi*freq, 2))"],
                ["C", "C    = 1e6/(L*pow(2*pi*freq, 2))"],
            ]
        )
    """
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # FormulaCalculator main
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD: __init__
    # PURPOSE: constructor
    #==========================================================================
    def __init__(self, parent=None, par_specs=None, recalc_specs=None,
        title=""
    ) :
        self.title = title
        self.__parent = parent
        self.__Component = {}
        self.__pars = []
        self.__ParInfo = {}
        self.__Recalc  = {}
        for item in par_specs :
            par, text, unit, value, rkey = item
            self.__pars.append(par)
            self.__ParInfo[par] = (text, unit, value, rkey)
        for item in recalc_specs :
            rkey, code = item
            self.__Recalc[rkey] = code
        self.__gui()
    #==========================================================================
    # METHOD: __quit
    # PURPOSE: destroy window
    #==========================================================================
    def __quit(self):
        top = self.__Component["top"]
        top.quit()
        top.destroy()
    #==========================================================================
    # METHOD  : __gui
    # PURPOSE : build graphical user interface
    #==========================================================================
    def __gui(self) :
        #---------------------------------------------------------------------
        # toplevel
        #---------------------------------------------------------------------
        if self.__parent is None:
            if not tk._default_root :
                root = tk.Tk()
                root.wm_state("withdrawn")
                tk._default_root = root
            top = tk.Toplevel()
        else :
            top = tk.Toplevel()
        top.protocol('WM_DELETE_WINDOW', self.__quit)
        self.__Component["top"] = top
        #---------------------------------------------------------------------
        # basic frames
        #---------------------------------------------------------------------
        ftext = tk.Frame(top, bd=2, relief="raised")
        ftext.pack(side="top", fill="both", expand=True)
        fpars = tk.Frame(top, bd=2, relief="raised")
        fpars.pack(side="top", fill="both", expand=True)
        mtext = tk.Message(ftext, justify="center", text=self.title, aspect=800)
        mtext.pack(side="left", fill="both", expand=True)
        bquit = tk.Button(ftext, text="Quit", command=self.__quit)
        bquit.pack(side="left", padx=3, pady=3, expand=True, fill="x")
        self.__Component["text"] = mtext
        self.__Component["quit"] = bquit
        ftext["background"]="cadet blue"
        bquit["width"]=12
        bquit["relief"]="raised"
        bquit["background"]="dark khaki"
        bquit["foreground"]="black"
        #---------------------------------------------------------------------
        # parameter entry
        #---------------------------------------------------------------------
        entries = []
        for par in self.__pars :
            text, unit, value, rkey = self.__ParInfo[par]
            fpar = tk.Frame(fpars)
            fpar.pack(side="top", expand=True, fill="x")
            lpar = tk.Label(fpar, text=text, width=30, anchor="w")
            lpar.pack(side="left", expand=True, fill="x")
            epar = tk.Entry(fpar, relief="sunken", bd=2)
            epar.pack(side="left", expand=True, fill="x")
            upar = tk.Label(fpar, text=unit, width=15, anchor="center")
            upar.pack(side="left", expand=True, fill="x")
            self.__Component["%s-entry" % (par)] = epar
            epar.insert(0, value)
            def par_recalc(event, self=self, par=par) :
                self.recalculate(par)
            epar.bind("<Return>", par_recalc)
            lpar["background"] = "cadet blue"
            lpar["foreground"] = "white"
            upar["background"] = "cadet blue"
            upar["foreground"] = "white"
            epar["background"] = "GhostWhite"
            epar["foreground"] = "black"
            entries.append(epar)
        entry_emacs_bindings(entries)
        self.recalculate(self.__pars[0])
        top.mainloop()
    #==========================================================================
    # METHOD  : recalculate
    # PURPOSE : revise calculations based on one parameter change
    #==========================================================================
    def recalculate(self, par_changed) :
        rkey = self.__ParInfo[par_changed][3]
        #---------------------------------------------
        # gather local and global variables for eval()
        #---------------------------------------------
        cos   = math.cos
        sin   = math.sin
        tan   = math.tan
        cosh  = math.cosh
        sinh  = math.sinh
        tanh  = math.tanh
        acos  = math.acos
        asin  = math.asin
        atan  = math.atan
        atan2 = math.atan2
        acosh = math.acosh
        asinh = math.asinh
        atanh = math.atanh
        ceil  = math.ceil
        floor = math.floor
        trunc = math.trunc
        fabs  = math.fabs
        fmod  = math.fmod
        sqrt  = math.sqrt
        pi    = math.pi
        exp   = math.exp
        log   = math.log
        log10 = math.log10
        erf   = math.erf
        erfc  = math.erfc
        dvars = dict(locals())
        dvars.update(globals())
        if rkey in self.__Recalc :
            for par in self.__pars :
                value = self.__Component["%s-entry" % (par)].get()
                dvars[par] = eval(value)
            code = self.__Recalc[rkey]
            lines = code.split("\n")
            for line in lines:
                line = line.strip()
                if not line :
                    continue
                # need to catch possible error
                var, val = line.split("=")
                var = var.strip()
                dvars[var] = eval(val, dvars)
        for par in self.__pars :
            par_value = eval(par, dvars)
            epar = self.__Component["%s-entry" % (par)]
            epar.delete(0, "end")
            epar.insert(0, par_value)
