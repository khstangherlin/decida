################################################################################
# CLASS    : NGspice
# PURPOSE  : spice with plotting
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:21:47 2013
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
import sys
import os
import os.path
import re
import time
import stat
import subprocess
import tkinter as tk
import tkinter.filedialog
import decida
from decida.entry_emacs_bindings import entry_emacs_bindings
from decida.grep             import grep
from decida.ItclObjectx      import ItclObjectx
from decida.Data             import Data
from decida.DataViewm        import DataViewm
from decida.Tckt             import Tckt

template = """#! /usr/bin/env python
from __future__ import print_function
###############################################################################
# NAME    : $SCRIPT
# PURPOSE : sequence file for simulation of $CIRCUIT
# DATE    : $DATE
# AUTHOR  : $AUTHOR
# -----------------------------------------------------------------------------
# NOTES:
#   * example tckt.monitor() specifications:
#     REF       : monitor voltage of node REF
#     VCD<3:0>  : monitor voltage of nodes VCD_3, ... , VCD_0
#     I(vsc)    : monitor current in voltage source vsc
#     IDN(mn1)  : monitor drain current in mosfet xmn1 (5V),    also IDN(xmn1)
#     IDNH(nmn1): monitor drain current in mosfet xmn1 (LDMOS), also IDNH(xnmn1)
#     IR(res)   : monitor current in resistor res, also IR(xres)
#     IX(xa1.p) : monitor current in subcircuit xa1, node p
#     PN(mn1-vdsat)  : monitor mosfet xmn1 vdsat parameter (5V)
#     PNH(mn1-vdsat) : monitor mosfet xmn1 vdsat parameter (LDMOS)
#     @Xgmc:    : following specs are for subcircuit Xgmc
#     @Xgmc.Xq: : following specs are for subcircuit Xgmc.Xq
#     @:        : following specs are for top-level circuit
#   * example tckt.element() definitions:
#     vin sin 0.6 0.2 $$freq
#     vbg netlist
#     vdd $$vdd
#     vsd<3:0> 5'b0011 v0=0.0 v1=$$vdd
#     vdac_in<9:0> counter v0=0.0 v1=$$vdd edge=$$edge hold=$$hold
#   * example Data commands:
#     d.set("z = v(out) * 2")
#     d.a2d("z", "v(sd<3:0>)", slice=1.5)
#     x = d.crossings("time", "v(xcp.cint)", level=1.5, edge="rising")
#     period = x[3] - x[2]
#   * stability analysis:
#     1. insert a voltage source in feedback path with + - in dir of feedback
#     2. in elements section, define the voltage source with stability spec.
#        a. example:
#            vstb stability xreg.xstb fmin=0.01 fmax=100G \\
#                method=middlebrook vblock=2 iblock=5
#        b. parameters:
#            xreg.xstb = full path of the stability source which is
#                to replace the voltage source
#            fmin, fmax = min, max frequency sweeps for ac analysis
#            method = middlebrook or vbreak
#            vblock, iblock = voltage and current simulation block numbers
#     3. no analysis card is required since stability analysis is signaled
#        by the voltage source element specification.  But doing an .op
#        analysis before the stability analysis seems to ensure dc conv.
#     4. in (post-process) report detail section, do stability_analysis
#           V = tckt.stability_analysis(plot=True, save=True)
#           phase_margin = V["pm"], etc.
###############################################################################
import sys
import re
import decida
from decida.Report  import Report
from decida.Data    import Data
from decida.Tckt    import Tckt
from decida.XYplotm import XYplotm
from decida.FrameNotebook import FrameNotebook
#==============================================================================
# test-circuit init
#==============================================================================
tckt = Tckt(project="$PROJECT", simulator="$SIMULATOR", verbose=True)
tckt["testdir"] = "$TESTDIR"
tckt["path"] = [".", "$PATH1", "$PATH2"]
tckt["temp_high"] = 125
postlayout = False
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# tests
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#==============================================================================
# tr: transient analysis
#==============================================================================
def tr(detail="simulate") :
    global tckt
    test      = tckt.get_test()
    modelfile = tckt.get_modelfile()
    tckt["circuit"]     = "$CIRCUIT"
    tckt["netlistfile"] = "$NETLIST"
    #--------------------------------------------------------------------------
    # signals to monitor
    #--------------------------------------------------------------------------
    tckt.monitor(\"\"\"
        $MONITOR
    \"\"\")
    #--------------------------------------------------------------------------
    # loop through experiments
    #--------------------------------------------------------------------------
    poststart = True
    cases = $CASES
    if True :
        cases = ["$CASE0"]
    for case in cases :
        tckt["case"] = case
        ckey    = tckt.get_case_key()
        process = tckt.get_process()
        vdd     = tckt.get_vdd()
        temp    = tckt.get_temp()
        prefix  = "%s.%s.%s" % \\
            (test, tckt["circuit"], case)
        print(prefix)
        tckt["title"]  = prefix
        tckt["prefix"] = prefix
        tstop = $TSTOP
        tstep = $TSTEP
        tckt.elements(\"\"\"
            $ELEMENTS
        \"\"\")
        tckt.control(\"\"\"
            .options rawpts=150 nomod brief=1 probe
            .options itl1=50000 itl2=50000 gmin=0 dcpath=0
            .options conv=-1 accurate=1 gmin=0 dcpath=0
            .prot
            .lib '$$modelfile' $$process
            .unprot
            .temp $$temp
            .tran $$tstep $$tstop
            * control lines:
            $CONTROL
        \"\"\")
        if   detail == "simulate" :
            if False and tckt.is_already_done() :
                continue
            tckt.generate_inputfile()
            tckt.simulate(clean=False)
        elif detail == "view" :
            if poststart :
                poststart = False
            if True :
                tckt.wait_for_data(2)
                tckt.view()
            else :
                if tckt.no_data() : continue
                d = Data()
                d.read_nutmeg(tckt.get_datafile())
                xy = XYplotm(command=[d, "time v(out)"])
        elif detail == "report" :
            if poststart :
                poststart = False
                point = 0
                rpt = Report(test + ".report", verbose=True, csv=True)
                header  = "point case temp vdd"
                rpt.header(header)
            if tckt.no_data() : continue
            d = Data()
            d.read_nutmeg(tckt.get_datafile())
            rpt.report(point, ckey, temp, vdd)
            point += 1
            del d
        else :
            print("detail " + detail + " not supported")
#==============================================================================
# run specified tests
# all_test format:  test, details
# command-line argument format: test:detail or test (if no details)
#==============================================================================
all_tests = \"\"\"
    tr simulate view report
\"\"\"
tests = tckt.test_select(all_tests, sys.argv[1:])
for test in tests :
    eval(test)
exit()
"""

class NGspice(ItclObjectx, tk.Frame) :
    """
    **synopsis**:

        Simulate using *NGspice* and plot results.

        *NGspice* is a graphical user-interface to run *NGspice*.  There is a
        netlist pane to directly enter a netlist and a plotting pane for
        displaying results.  The plotting pane is a full *DataViewm* window,
        which has all of the features of that class.

        The DeCiDa application *ngsp* simply instantiates one *NGspice* object.

    **constructor arguments**:

        **parent** (tk handle, default=None)

              handle of frame or other widget to pack plot in.
              if this is not specified, top-level is created.

        **\*\*kwargs** (dict)

              keyword=value specifications:
              options or configuration-options

    **options**:

        **netlist** (str, default=None)

            netlist lines.

        **cktfile** (str, default=None)

            circuit file to read.

    **configuration options**:

        **verbose** (bool, default=False)

              enable/disable verbose mode

        **plot_height** (str, default="10i" for MacOS, else "6i")

              Height of plot window (Tk inch  or pixelspecification)

        **plot_width** (str, default="10i" for MacOS, else "6i")

              Width of plot window (Tk inch or pixel specification)

        **xcol** (str, default="time")

              X-column of plot to generate after simulation.

        **ycol** (str, default="v(1)")

              Y-columns of plot to generate after simulation.

    **example** (from test_NGspice_1): ::

        from decida.NGspice import NGspice
        NGspice(cktfile="hartley.ckt", xcol="time", ycols="v(c)")

    **public methods**:

        * public methods from *ItclObjectx*

    """
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # NGspice main
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
        self.__parent    = parent
        self.__use_matplotlib = use_matplotlib
        self.__Component = {}
        self.__data_obj  = None
        self.__dataview  = None
        self.__netlist   = None
        self.__cktfile   = None
        self.__ngspice_root = "ngspice"
        self.__ngspice_ext  = ""
        self.__ngspice_dir  = ""
        self.__datfile  = ""
        self.__analysis = ""
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
            "plot_width"     : [plot_width, None],
            "plot_height"    : [plot_height, None],
            "xcol"           : ["time", self._config_xcol_callback],
            "ycols"          : ["v(1)", self._config_ycols_callback],
            "simulator"      : ["ngspice", self._config_simulator_callback],
        })
        #----------------------------------------------------------------------
        # keyword arguments are *not* all configuration options
        #----------------------------------------------------------------------
        for key, value in list(kwargs.items()) :
            if   key == "netlist" :
                self.__netlist = value
            elif key == "cktfile" :
                self.__cktfile = value
            else :
                self[key] = value
        #----------------------------------------------------------------------
        # build gui:
        #----------------------------------------------------------------------
        self.__gui()
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
    # NGspice configuration option callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _config_xcol_callback
    # PURPOSE : configure xcol
    #==========================================================================
    def _config_xcol_callback(self) :
        self.__entry_enter("xcol")
    #==========================================================================
    # METHOD  : _config_ycols_callback
    # PURPOSE : configure ycols
    #==========================================================================
    def _config_ycols_callback(self) :
        self.__entry_enter("ycols")
    #==========================================================================
    # METHOD  : _config_simulator_callback
    # PURPOSE : configure simulator
    #==========================================================================
    def _config_simulator_callback(self) :
        valid_simulators = ("ngspice", "hspice")
        if not self["simulator"] in valid_simulators :
            self.__warning("simulator must be in \"%s\"", (valid_simulators))
            return False
        if "simulator" in self.__Component :
            self.__Component["simulator"].set(self["simulator"])
        return True
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
            entry.insert(0, str(val))
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # NGspice GUI
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __gui
    # PURPOSE : build graphical user interface
    #==========================================================================
    def __gui(self) :
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
            tk.Frame.__init__(self, self.__toplevel, class_ = "NGspice")
        else:
            self.__toplevel = None
            tk.Frame.__init__(self, self.__parent,   class_ = "NGspice")
        self.pack(side="top", fill="both", expand=True)
        #----------------------------------------------------------------------
        # option database:
        #----------------------------------------------------------------------
        if sys.platform == "darwin" :
            self.option_add("*NGspice*Menubutton.width", 10)
            self.option_add("*NGspice*Menubutton.height", 1)
            self.option_add("*NGspice*Label.width", 10)
            self.option_add("*NGspice*Label.anchor", "e")
            self.option_add("*NGspice*Label.relief", "sunken")
            self.option_add("*NGspice*Label.bd", 2)
            self.option_add("*NGspice*Entry.width", 15)
            self.option_add("*NGspice*Entry.font", "Courier 20 normal")
            self.option_add("*NGspice*Entry.background", "Ghost White")
            self.option_add("*NGspice*Checkbutton.width", 12)
            self.option_add("*NGspice*Checkbutton.anchor", "w")
            self.option_add("*NGspice*Checkbutton.bd", 2)
            self.option_add("*NGspice*Checkbutton.relief", "raised")
            self.option_add("*NGspice*Checkbutton.highlightThickness", 0)
            self.option_add("*NGspice*Radiobutton.anchor", "w")
            self.option_add("*NGspice*Radiobutton.highlightThickness", 0)
            self.option_add("*NGspice*Button.highlightThickness", 0)
            self.option_add("*NGspice*Button.width", 10)
            self.option_add("*NGspice*Button.height", 1)
            self.option_add("*NGspice*Text.width", 20)
            self.option_add("*NGspice*Text.height", 8)
            self.option_add("*NGspice*Text.font", "Courier 20 normal")
            self.option_add("*NGspice*Text.background", "Ghost White")
        else :
            self.option_add("*NGspice*Menubutton.width", 10)
            self.option_add("*NGspice*Menubutton.height", 1)
            self.option_add("*NGspice*Label.width", 10)
            self.option_add("*NGspice*Label.anchor", "e")
            self.option_add("*NGspice*Label.relief", "sunken")
            self.option_add("*NGspice*Label.bd", 2)
            self.option_add("*NGspice*Entry.width", 20)
            self.option_add("*NGspice*Entry.font", "Courier 12 normal")
            self.option_add("*NGspice*Entry.background", "Ghost White")
            self.option_add("*NGspice*Checkbutton.width", 12)
            self.option_add("*NGspice*Checkbutton.anchor", "w")
            self.option_add("*NGspice*Checkbutton.bd", 2)
            self.option_add("*NGspice*Checkbutton.relief", "raised")
            self.option_add("*NGspice*Checkbutton.highlightThickness", 0)
            self.option_add("*NGspice*Radiobutton.anchor", "w")
            self.option_add("*NGspice*Radiobutton.highlightThickness", 0)
            self.option_add("*NGspice*Button.highlightThickness", 0)
            self.option_add("*NGspice*Button.width", 10)
            self.option_add("*NGspice*Button.height", 1)
            self.option_add("*NGspice*Text.width", 20)
            self.option_add("*NGspice*Text.height", 8)
            self.option_add("*NGspice*Text.font", "Courier 12 normal")
            self.option_add("*NGspice*Text.background", "Ghost White")
        #----------------------------------------------------------------------
        # main layout
        #----------------------------------------------------------------------
        mbar = tk.Frame(self, relief="sunken", bd=2)
        mbar.pack(side="top", expand=False, fill="x",    padx=2, pady=2)
        fcnt = tk.Frame(self, relief="sunken", bd=2)
        fcnt.pack(side="top", expand=False, fill="x",    padx=2, pady=2)
        fplt = tk.Frame(self, relief="sunken", bd=2, background="blue")
        fplt.pack(side="top", expand=True, fill="both", padx=2, pady=2)

        cont = tk.Frame(fcnt, relief="flat")
        cont.pack(side="left", expand=True, fill="both", padx=2, pady=2)
        ftxt = tk.Frame(fcnt, relief="flat", bd=2)
        ftxt.pack(side="right", expand=True, fill="both")
        tobj = tk.Text(ftxt, relief="sunken", bd=2, height=15, width=40)
        tobj.pack(side="right", expand=True, fill="both")
        self.__Component["plot_frame"] = fplt
        self.__Component["text"] = tobj
        if self.__netlist is not None:
            tobj.delete(1.0, "end")
            tobj.insert(1.0, self.__netlist)
        elif self.__cktfile is not None:
            self.__read_netlist(self.__cktfile)
        #----------------------------------------------------------------------
        # menu-bar
        #----------------------------------------------------------------------
        file_mb = tk.Menubutton(mbar, text="File")
        file_mb.pack(side="left", padx=5, pady=5)
        edit_mb = tk.Menubutton(mbar, text="Edit")
        edit_mb.pack(side="left", padx=5, pady=5)

        file_menu= tk.Menu(file_mb)
        file_mb["menu"] = file_menu
        edit_menu= tk.Menu(edit_mb)
        edit_mb["menu"] = edit_menu

        simu_bt = tk.Button(mbar, text="Simulate/Plot")
        simu_bt.pack(side="left", padx=5, pady=5)
        simu_bt["background"] = "red"
        simu_bt["foreground"] = "white"
        simu_bt["command"] = self.__simulate_plot

        mblist = [file_mb, simu_bt]
        #tk_menuBar(mblist)
        #----------------------------------------------------------------------
        # file menu
        #----------------------------------------------------------------------
        file_menu.add_command(
            label="Read NGspice circuit file",
            command=self.__read_netlist)
        file_menu.add_command(
            label="Write NGspice circuit file",
            command=self.__write_netlist)
        file_menu.add_command(
            label="Write NGspice DeCiDa script",
            command=self.__write_script)
        file_menu.add_command(
            label="Write executable NGspice file",
            command=self.__write_ngspice)
        file_menu.add_command(
            label="Write Data",
            command=self.__write_ssv)
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit",
            command=self.__exit_cmd)
        #----------------------------------------------------------------------
        # edit menu
        #----------------------------------------------------------------------
        self.__Component["simulator"] = tk.StringVar()
        self.__Component["simulator"].set(self["simulator"])
        def cmd1(self=self):
            self["simulator"] = "ngspice"
        edit_menu.add_radiobutton(
            label="Simulator = NGspice",
            variable=self.__Component["simulator"],
            value="ngspice",
            command=cmd1
        )
        def cmd2(self=self):
            self["simulator"] = "hspice"
        edit_menu.add_radiobutton(
            label="Simulator = HSpice",
            variable=self.__Component["simulator"],
            value="hspice",
            command=cmd2
        )
        #----------------------------------------------------------------------
        # plot entries
        #----------------------------------------------------------------------
        def entrybindcmd(event, self=self):
            self.__simulate_plot(new=False, simulate=False)
        def textbindcmd(event, self=self):
            self.__simulate_plot(new=False, simulate=True)
        entry_list = []
        for item in (
            ["xcol",  "x column"],
            ["ycols", "y columns"],
        ) :
            var, text = item
            val = self[var]
            f = tk.Frame(cont, relief="flat")
            f.pack(side="top", fill="x")
            l = tk.Label(f, relief="flat", anchor="w", text=text, width=12)
            l.pack(side="left", expand=True, fill="x")
            e = tk.Entry(f, relief="sunken", bd=2)
            e.pack(side="left", expand=True, fill="x")
            self.__Component["%s_label" % (var)] = l
            self.__Component["%s_entry" % (var)] = e
            e.delete(0, "end")
            e.insert(0, str(val))
            e.bind("<Control-Key-s>", entrybindcmd)
            e.bind("<Return>", entrybindcmd)
            entry_list.append(e)
        if False :
            self.__Component["analysis"] = tk.StringVar()
            self.__Component["analysis"].set("tr")
            for item in (
                ["tr", "transient analysis", ".tr 1n 100n"],
                ["ac", "ac analysis", ".ac dec 10 1e2 1e8"],
                ["dc", "dc analysis", ".dc temp 0 100 10"],
            ) :
                var, text, analysis = item
                f = tk.Frame(cont, relief="flat")
                f.pack(side="top", fill="x")
                rb = tk.Radiobutton(f, relief="flat", anchor="w", text=text, width=10,
                   variable = self.__Component["analysis"], value=var
                )
                rb.pack(side="left", expand=True, fill="x")
                e = tk.Entry(f, relief="sunken", bd=2)
                e.pack(side="left", expand=True, fill="x")
                self.__Component["%s_entry" % (var)] = e
                e.delete(0, "end")
                e.insert(0, ".%s %s" % (var, analysis))
                e.bind("<Control-Key-s>", entrybindcmd)
                e.bind("<Return>", entrybindcmd)
                entry_list.append(e)
        #----------------------------------------------------------------------
        # bindings
        #----------------------------------------------------------------------
        text = self.__Component["text"]
        text.bind("<Control-Key-s>", textbindcmd)
        entry_emacs_bindings(entry_list)
        #----------------------------------------------------------------------
        # update / mainloop
        #----------------------------------------------------------------------
        self.update()
        if False :
            if self.__netlist is not None:
                self.__simulate_plot()
        if  self.__toplevel :
            self.__toplevel.geometry("+20+20")
            self.__toplevel.wm_state("normal")
        self.wait_window()
        if  self.__toplevel :
            self.__toplevel.destroy()
        else :
            self.destroy()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # NGspice GUI construction methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # NGspice GUI file menu callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #--------------------------------------------------------------------------
    # METHOD  : __exit_cmd
    # PURPOSE : exit file menu callback
    #--------------------------------------------------------------------------
    def __exit_cmd(self) :
        self.quit()
        if self.__toplevel :
            self.__toplevel.destroy()
        else :
            self.destroy()
        exit()
    #--------------------------------------------------------------------------
    # METHOD  : __read_netlist
    # PURPOSE : read netlist file
    #--------------------------------------------------------------------------
    def __read_netlist(self, filename=None) :
        if not filename :
            if sys.platform == "darwin" :
                filename = tkinter.filedialog.askopenfilename(
                    parent = tk.Frame(self),
                    title = "circuit file name to read?",
                    initialdir = os.getcwd(),
                )
            else:
                filename = tkinter.filedialog.askopenfilename(
                    parent = tk.Frame(self),
                    title = "circuit file name to read?",
                    initialdir = os.getcwd(),
                    filetypes = (
                        ("circuit files", "*.ckt"),
                        ("circuit files", "*.sp"),
                        ("circuit files", "*.cir"),
                        ("all files", "*")
                    )
                )
        if not filename :
            return
        if not os.path.isfile(filename) :
            print("circuit file \"" + filename + "\" doesn't exist")
        self.__ngspice_root = os.path.splitext(os.path.basename(filename))[0]
        f = open(filename, "r")
        netlist = f.read()
        tobj = self.__Component["text"]
        tobj.delete(1.0, "end")
        tobj.insert(1.0, netlist)
    #--------------------------------------------------------------------------
    # METHOD  : __write_netlist
    # PURPOSE : write ngspice circuit file
    #--------------------------------------------------------------------------
    def __write_netlist(self, filename=None) :
        if not filename :
            initialfile = "%s.ckt" % (self.__ngspice_root)
            if sys.platform == "darwin" :
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "ngspice circuit file name to save?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".ckt",
                )
            else:
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "ngspice circuit file name to save?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".ckt",
                    filetypes = (
                        ("circuit files", "*.ckt"),
                        ("circuit files", "*.sp"),
                        ("circuit files", "*.cir"),
                        ("all files", "*")
                    )
                )
        if not filename :
            return
        #----------------------------------------------------------------------
        # NGspice parameters
        #----------------------------------------------------------------------
        filename = os.path.abspath(filename)
        root, ext = os.path.splitext(os.path.basename(filename))
        self.__ngspice_root = root
        self.__ngspice_ext  = ext
        self.__ngspice_dir  = os.path.dirname(filename)
        tobj  = self.__Component["text"]
        netlist = tobj.get(1.0, "end")
        netlist = str(netlist)
        #----------------------------------------------------------------------
        # write ngspice circuit file
        #----------------------------------------------------------------------
        print("writing ngspice circuit file to %s" % (filename))
        timestamp = time.time()
        datetime  = time.asctime(time.localtime(timestamp))
        f = open(filename, "w")
        f.write("* DATE : %s\n" % (datetime))
        for line in netlist.split("\n") :
            line=line.strip()
            if line :
                f.write("%s\n" % (line))
        f.close()
    #--------------------------------------------------------------------------
    # METHOD  : __write_ssv
    # PURPOSE : write data file
    #--------------------------------------------------------------------------
    def __write_ssv(self, filename=None) :
        if not filename :
            initialfile = "%s.ssv" % (self.__ngspice_root)
            if sys.platform == "darwin" :
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "data file name to save?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".col",
                )
            else:
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "data file name to save?",
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
        self.__ngspice_root = os.path.splitext(os.path.basename(filename))[0]
        # file/format dialog?
        self.__data_obj.write_ssv(filename)
    #--------------------------------------------------------------------------
    # METHOD  : __write_script
    # PURPOSE : write ngspice DeCiDa script
    #--------------------------------------------------------------------------
    def __write_script(self, filename=None) :
        if not filename :
            initialfile = "%s.py" % (self.__ngspice_root)
            if sys.platform == "darwin" :
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "ngspice DeCiDa script name?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".py",
                )
            else :
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "ngspice DeCiDa script name?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".py",
                    filetypes = (
                        ("ngspice/python files", "*.py"),
                        ("all files", "*")
                    )
                )
        if not filename :
            return
        #----------------------------------------------------------------------
        # NGspice parameters
        #----------------------------------------------------------------------
        filename = os.path.abspath(filename)
        root, ext = os.path.splitext(os.path.basename(filename))
        self.__ngspice_root = root
        self.__ngspice_ext  = ext
        self.__ngspice_dir  = os.path.dirname(filename)
        xcol  = self.__Component["xcol_entry"].get()
        ycols = self.__Component["ycols_entry"].get()
        tobj  = self.__Component["text"]
        netlist = tobj.get(1.0, "end")
        netlist = str(netlist)
        #----------------------------------------------------------------------
        # need to do line-continuation here
        #----------------------------------------------------------------------
        #----------------------------------------------------------------------
        # extract element, control, monitor lines
        #----------------------------------------------------------------------
        element_lines = []
        control_lines = []
        monitor_vars  = []
        monitor_lines = []
        netlist_lines = []
        tstep = "0.1e-9"
        tstop = "10e-9"
        lines = netlist.split("\n")
        for line in lines :
            uline = line.lower()
            uline = uline.strip()
            if re.search("^(v|i)", uline) :
                toks = line.split()
                src  = toks[0]
                monitor_vars.append(toks[1])
                monitor_vars.append(toks[2])
                eline = "%s netlist" % (src)
                netlist_lines.append(line)
                element_lines.append(eline)
            elif re.search("^\.end", uline) :
                pass
            elif re.search("^\.(save|print|plot|probe)", uline) :
                toks = line.split()
                for var in toks[1:] :
                    m=re.search("v\(([^\)]+)\)", var)
                    if m:
                        node = m.group(1)
                        monitor_vars.append(var)
                    m=re.search("i\(([^\)]+)\)", var)
                    if m:
                        src  = m.group(1)
                        monitor_vars.append("I(%s)" % (src))
            elif re.search("^\.tr", uline) :
                analysis = "tr"
                toks = uline.split()
                tstep = decida.spice_value(toks[1])
                tstop = decida.spice_value(toks[2])
            elif re.search("^\.ac", uline) :
                analysis = "ac"
            elif re.search("^\.dc", uline) :
                analysis = "dc"
            elif re.search("^\.", uline) :
                control_lines.append(line)
            else :
                toks = uline.split()
                if re.search("^(r|c|d|l)", uline) :
                    monitor_vars.append(toks[1])
                    monitor_vars.append(toks[2])
                netlist_lines.append(line)
        monitor_vars = list(set(monitor_vars))
        monitor_lines.append(" ".join(monitor_vars))
        #----------------------------------------------------------------------
        # TBD: dialog to get project:
        #----------------------------------------------------------------------
        project = "trane"
        #----------------------------------------------------------------------
        # parameters for ckt template
        #----------------------------------------------------------------------
        if project is None or project not in Tckt.projects():
            print()
            print("@" * 72)
            print("%s is not in supported projects changing project to GENERIC" % (project))
            print()
            print("the list of supported projects is:")
            ps = Tckt.projects()
            ps.sort()
            for p in ps:
                print(p)
            print("@" * 72)
            PROJECT = "GENERIC"
        else :
            PROJECT = project
        timestamp = time.time()
        datetime  = time.asctime(time.localtime(timestamp))
        TECH      = Tckt.project_tech(PROJECT)
        CASES     = str(Tckt.project_cases(PROJECT))
        CASE0     = Tckt.project_cases(PROJECT)[0]
        MODELFILE = Tckt.project_modelfile(PROJECT)
        try :
            USER = os.environ["USERNAME"]
        except :
            USER = os.environ["USER"]
        AUTHOR    = USER
        DATE      = time.asctime(time.localtime(time.time()))
        TESTDIR   = os.path.expanduser("~/.DeCiDa/projects/%s" % (project))
        PATH1     = self.__ngspice_dir
        PATH2     = os.path.expanduser("~/.DeCiDa/projects/%s" % (project))
        SCRIPT    = self.__ngspice_root + self.__ngspice_ext
        testbench = self.__ngspice_root
        NETLIST   = testbench + ".sp"
        CIRCUIT   = testbench
        SIMULATOR = self["simulator"]
        TSTOP     = tstop
        TSTEP     = tstep
        m = re.search("^(TEST_|TB_TEST|TB_|test_|tb_test|tb_)(.+)$", testbench)
        if m :
            CIRCUIT = m.group(2)
        ELEMENTS  = "\n            ".join(element_lines)
        CONTROL   = "\n            ".join(control_lines)
        MONITOR   = "\n        ".join(monitor_lines)
        #----------------------------------------------------------------------
        # fill template
        #----------------------------------------------------------------------
        filled_template = decida.interpolate(template)
        #----------------------------------------------------------------------
        # write output file (script)
        #----------------------------------------------------------------------
        if os.path.isfile(filename) :
            print("over-writing ", filename)
        print("writing ngspice DeCiDa script to %s" % (filename))
        f = open(filename, "w")
        for line in filled_template.split("\n") :
            f.write(line + "\n")
        f.close()
        os.chmod(filename, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)
        #----------------------------------------------------------------------
        # write output file (template)
        #----------------------------------------------------------------------
        netlist_template = "%s/%s" % (self.__ngspice_dir, NETLIST)
        if os.path.isfile(netlist_template) :
            print("over-writing ", netlist_template)
        f = open(netlist_template, "w")
        for line in netlist_lines :
            f.write(line + "\n")
        f.close()
    #--------------------------------------------------------------------------
    # METHOD  : __write_ngspice
    # PURPOSE : write executable ngspice file
    #--------------------------------------------------------------------------
    def __write_ngspice(self, filename=None) :
        if not filename :
            initialfile = "%s.py" % (self.__ngspice_root)
            if sys.platform == "darwin" :
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "ngspice file name to save?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".py",
                )
            else :
                filename = tkinter.filedialog.asksaveasfilename(
                    parent = tk.Frame(self),
                    title = "ngspice file name to save?",
                    initialfile=initialfile,
                    initialdir = os.getcwd(),
                    defaultextension = ".py",
                    filetypes = (
                        ("ngspice/python files", "*.py"),
                        ("all files", "*")
                    )
                )
        if not filename :
            return
        #----------------------------------------------------------------------
        # NGspice parameters
        #----------------------------------------------------------------------
        filename = os.path.abspath(filename)
        root, ext = os.path.splitext(os.path.basename(filename))
        self.__ngspice_root = root
        self.__ngspice_ext  = ext
        self.__ngspice_dir  = os.path.dirname(filename)
        xcol  = self.__Component["xcol_entry"].get()
        ycols = self.__Component["ycols_entry"].get()
        simulator = self.__Component["simulator"].get()
        tobj  = self.__Component["text"]
        netlist = tobj.get(1.0, "end")
        netlist = str(netlist)
        #----------------------------------------------------------------------
        # write executable ngspice file
        #----------------------------------------------------------------------
        print("writing ngspice file to %s" % (filename))
        timestamp = time.time()
        datetime  = time.asctime(time.localtime(timestamp))
        f = open(filename, "w")
        f.write("#! /usr/bin/env python\n")
        f.write("#" * 72 + "\n")
        f.write("# NAME : %s\n" % (filename))
        f.write("# CREATED BY : NGspice\n")
        f.write("# DATE : %s\n" % (datetime))
        f.write("#" * 72 + "\n")
        f.write("import decida\n")
        f.write("from decida.NGspice import NGspice\n")
        f.write("NGspice(\n")
        f.write("    xcol=\"%s\",\n"      % (xcol))
        f.write("    ycols=\"%s\",\n"     % (ycols))
        f.write("    simulator=\"%s\",\n" % (simulator))
        f.write("    netlist=\"\"\"\n")
        for line in netlist.split("\n") :
            line=line.strip()
            if line :
                f.write("        %s\n" % (line))
        f.write("    \"\"\"\n")
        f.write(")\n")
        f.close()
        os.chmod(filename, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # NGspice GUI plot callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #--------------------------------------------------------------------------
    # METHOD  : __simulate
    # PURPOSE : do NGspice simulation
    # NOTES :
    #     * tobj comes out as unicode
    #--------------------------------------------------------------------------
    def __simulate(self) :
        inpfile = "%s_tmp.inp" % (self.__ngspice_root)
        outfile = "%s.lis" % (self.__ngspice_root)
        #-------------------------------------------
        # generate netlist from text-window contents
        #-------------------------------------------
        tobj   = self.__Component["text"]
        netlist= tobj.get(1.0, "end")
        netlist= str(netlist)
        netlist_lines = []
        analysis = ""
        for line in netlist.split("\n") :
            line = line.strip()
            det = line.lower()
            if   re.search("^.tr", det) :
                analysis = "tr"
            elif re.search("^.ac", det) :
                analysis = "ac"
            elif re.search("^.dc", det) :
                analysis = "dc"
            if line :
                netlist_lines.append(line)
        if netlist_lines[-1].lower() != ".end" :
            netlist_lines.append(".end")
        f = open(inpfile, "w")
        for line in netlist_lines :
            f.write(line + "\n")
        f.close()
        #---------------------------------
        # generate simulation command line
        #---------------------------------
        if self["simulator"] == "ngspice" :
            datfile = "%s.raw" % (self.__ngspice_root)
            sim = os.path.expanduser("~/.DeCiDa/bin/") + "run_ngspice"
            args = ""
            simargs = ""
            cmd = "%s -quiet -project %s -b %s -o %s -r %s %s %s" % (
                sim, "generic", inpfile, outfile, datfile, args, simargs
            )
        elif self["simulator"] == "hspice" :
            datfile = "%s.%s0" % (self.__ngspice_root, analysis)
            sim = os.path.expanduser("~/.DeCiDa/bin/") + "run_hspice"
            args = ""
            simargs = ""
            cmd = "%s -quiet -project %s %s -o %s %s %s" % (
                sim, "generic", inpfile, outfile, args, simargs
            )
        #---------------
        # run simulation
        #---------------
        try:
            subprocess.check_call(cmd.split())
        except subprocess.CalledProcessError as err :
            pass
        if grep("Error", outfile) :
            print("error detected.  examine \"%s\"" % (outfile))
            return False
        self.__datfile  = datfile
        self.__analysis = analysis
        return True
    #--------------------------------------------------------------------------
    # METHOD  : __simulate_plot
    # PURPOSE : simulate and plot
    #--------------------------------------------------------------------------
    def __simulate_plot(self, new=True, simulate=True) :
        if simulate or self.__data_obj is None :
            if not self.__simulate() :
                return
            self.__data_obj = Data()
            if self["simulator"] == "ngspice" :
                self.__data_obj.read_nutmeg(self.__datfile)
            elif self["simulator"] == "hspice" :
                self.__data_obj.read_hspice(self.__datfile)
        #------------------
        # get x, y columns
        #------------------
        xcol  = self.__Component["xcol_entry"].get()
        ycols = self.__Component["ycols_entry"].get()
        data_cols = self.__data_obj.names()
        ok = True
        if not xcol in data_cols :
            ok = False
            print("xcol \"%s\" not in data" % (xcol))
        if not ok :
            xcol  = data_cols[0]
            self.__Component["xcol_entry"].delete(0, "end")
            self.__Component["xcol_entry"].insert(0, xcol)
        ok = True
        for ycol in ycols.split() :
            if not ycol in data_cols :
                ok = False
                print("ycol \"%s\" not in data" % (ycol))
        if not ok :
            ycols = data_cols[1]
            self.__Component["ycols_entry"].delete(0, "end")
            self.__Component["ycols_entry"].insert(0, ycols)
        #------------------
        # plot x, y columns
        #------------------
        if new or self.__dataview is None :
            if self.__dataview is not None :
                # del should have destroyed it
                self.__dataview.destroy()
                del self.__dataview
            fplt = self.__Component["plot_frame"]
            fplt.pack_forget()
            plt = xcol + "  " + ycols
            if   self.__analysis == "tr" :
                xaxis = "lin"
            if   self.__analysis == "dc" :
                xaxis = "lin"
            elif self.__analysis == "ac" :
                xaxis = "log"
            self.__dataview = DataViewm(fplt,
                use_matplotlib=self.__use_matplotlib,
                data=self.__data_obj, command=[[plt, "xaxis=\"%s\"" % (xaxis)]],
                plot_height=self["plot_height"]
            )
            fplt.pack(side="top", expand=True, fill="both", padx=2, pady=2)
            self.update()
        else :
            xyplot = self.__dataview.current_plot()
            curves = xyplot.curves()
            for ycol in ycols.split():
                curve = "data_%d_:_%s_vs_%s" % (1, ycol, xcol)
                if curve in curves:
                    V = xyplot.curve_attributes(curve)
                    color = V["color"]
                    symbol= V["symbol"]
                    wline = V["wline"]
                    ssize = V["ssize"]
                    trace = V["trace"]
                    lstate= V["lstate"]
                    sstate= V["sstate"]
                    xyplot.delete_curve(curve)
                    xyplot.add_curve(self.__data_obj, xcol, ycol,
                        color=color, symbol=symbol,
                        wline=wline, ssize=ssize,
                        trace=trace, lstate=lstate, sstate=sstate,
                        start=True,
                        autoscale_x=False, autoscale_y=True, strict=False)
                else :
                    xyplot.add_curve(self.__data_obj, xcol, ycol,
                        start=True,
                        autoscale_x=False, autoscale_y=True, strict=False)
