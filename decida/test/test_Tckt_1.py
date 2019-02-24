#! /usr/bin/env python
###############################################################################
# NAME    : test_Tckt_1.py
# PURPOSE : sequence file for simulation of crrc
# DATE    : Wed Apr 29 13:38:04 2015
# AUTHOR  : gen
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
#     vin sin 0.6 0.2 $freq
#     vbg netlist
#     vdd $vdd
#     vsd<3:0> 5'b0011 v0=0.0 v1=$vdd
#     vdac_in<9:0> counter v0=0.0 v1=$vdd edge=$edge hold=$hold
#   * example Data commands:
#     d.set("z = v(out) * 2")
#     d.a2d("z", "v(sd<3:0>)", slice=1.5)
#     x = d.crossings("time", "v(xcp.cint)", level=1.5, edge="rising")
#     period = x[3] - x[2]
#   * stability analysis:
#     1. insert a voltage source in feedback path with + - in dir of feedback
#     2. in elements section, define the voltage source with stability spec.
#        a. example:
#            vstb stability xreg.xstb fmin=0.01 fmax=100G \
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
from __future__ import print_function
import decida
import decida.test
from decida.Report  import Report
from decida.Data    import Data
from decida.Tckt    import Tckt
from decida.XYplotm import XYplotm
#==============================================================================
# test-circuit init
#==============================================================================
tckt = Tckt(project="trane", simulator="ngspice", verbose=True)
tckt["testdir"] = "/home/gen/.DeCiDa/projects/trane"
test_dir = decida.test.test_dir()
tckt["path"] = [".", test_dir]
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
    tckt["circuit"]     = "crrc"
    tckt["netlistfile"] = "data/crrc.sp"
    #--------------------------------------------------------------------------
    # signals to monitor
    #--------------------------------------------------------------------------
    tckt.monitor("""
        qp cm 0 ip n p in qn
    """)
    #--------------------------------------------------------------------------
    # loop through experiments
    #--------------------------------------------------------------------------
    poststart = True
    cases = ['tt', 'ss', 'ff', 'fs', 'sf']
    if True :
        cases = ["tt"]
    for case in cases :
        tckt["case"] = case
        ckey    = tckt.get_case_key()
        process = tckt.get_process()
        vdd     = tckt.get_vdd()
        temp    = tckt.get_temp()
        prefix  = "%s.%s.%s" % \
            (test, tckt["circuit"], case)
        print(prefix)
        tckt["title"]  = prefix
        tckt["prefix"] = prefix
        tstop = 500e-12
        tstep = 1e-12
        tckt.elements("""
            vp netlist
            vn netlist
        """)
        tckt.control("""
            .options rawpts=150 nomod brief=1 probe
            .options itl1=50000 itl2=50000 gmin=0 dcpath=0
            .options conv=-1 accurate=1 gmin=0 dcpath=0
            .prot
            .lib '$modelfile' $process
            .unprot
            .temp $temp
            .tran $tstep $tstop
            .parameter fosc=14G res=50 cap=220f
        """)
        if   detail == "simulate" :
            if False and tckt.is_already_done() :
                continue
            tckt.generate_inputfile()
            tckt.simulate(clean=False)
        elif detail == "view" :
            if poststart :
                poststart = False
            if tckt.no_data() :
                continue
            d = Data()
            d.read_nutmeg(tckt.get_datafile())
            xy = XYplotm(command=[d, "time v(ip) v(qn) v(in) v(qp)"])
        elif detail == "report" :
            if poststart :
                poststart = False
                point = 0
                rpt = Report(test + ".report", verbose=True, csv=True)
                header  = "point case temp vdd"
                rpt.header(header)
            if tckt.no_data() :
                continue
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
all_tests = """
    tr simulate view report
"""
# instead of command-line test-spec, do two default tests
#tests = tckt.test_select(all_tests, sys.argv[1:])
tests = tckt.test_select(all_tests, ("tr", "tr:view"))
for test in tests :
    eval(test)
exit()
