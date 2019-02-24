################################################################################
# CLASS    : SimulatorNetlist
# PURPOSE  : circuit-simulator netlist parsing, etc.
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:24:59 2013
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
import re
import os.path
import decida
from decida.ItclObjectx import ItclObjectx

class SimulatorNetlist(ItclObjectx) :
    """
    **synopsis**:

        Circuit simulator netlist parsing.

        *SimulatorNetlist* reads a circuit-simulator netlist and extracts
        some limited information about the circuit, such as lists or devices,
        and total capacitance on each node.

    **constructor arguments**:

        **netlist_file** (str)

            simulator netlist file

        **\*\*kwargs** (dict)

           configuration-options

    **configuration options**:

        **verbose** (bool) (optional, default=False)

           enable/disable verbose mode

        **simulator** (str) (optional, default="sspice")

           circuit simulator associated with the netlist file, one of :

           +------------+----------------+
           | simulator: |  format:       |
           +============+================+
           | spice      |   spice        |
           +------------+----------------+
           | hspice     |   spice        |
           +------------+----------------+
           | sspice     |   spice        |
           +------------+----------------+
           | eldo       |   spice        |
           +------------+----------------+
           | adit       |   spice        |
           +------------+----------------+
           | nanosim    |   spice        |
           +------------+----------------+
           | finesim    |   spice        |
           +------------+----------------+
           | ngspice    |   spice        |
           +------------+----------------+
           | spectre    |   spectre      |
           +------------+----------------+
           | spectrerf  |   spectre      |
           +------------+----------------+
           | ncverilog  |   verilog      |
           +------------+----------------+
           | ncsim      |   verilog      |
           +------------+----------------+
           | vsim       |   verilog      |
           +------------+----------------+
           | vcs        |   verilog      |
           +------------+----------------+

    **example** (from test_SimulatorNetlist): ::

        from decida.SimulatorNetlist import SimulatorNetlist

        s = SimulatorNetlist("sar_seq_dig.net", simulator="ngspice")
        print("subcircuits :")
        print(s.get("subckts"))
        print("instances :")
        print(s.get("insts"))
        print("capacitors:")
        print(s.get("caps"))
        print("resistors:")
        print(s.get("ress"))

    **public methods**:

        * public methods from *ItclObjectx*

    """
    _SimulatorDB ={
        "spice"     : ["spice"],
        "hspice"    : ["spice"],
        "sspice"    : ["spice"],
        "eldo"      : ["spice"],
        "adit"      : ["spice"],
        "nanosim"   : ["spice"],
        "finesim"   : ["spice"],
        "ngspice"   : ["spice"],
        "spectre"   : ["spectre"],
        "spectrerf" : ["spectre"],
        "ncverilog" : ["verilog"],
        "ncsim"     : ["verilog"],
        "vsim"      : ["verilog"],
        "vcs"       : ["verilog"],
    }
    #==========================================================================
    # METHOD: SimulatorNetlist::constructor
    #==========================================================================
    def __init__(self, netlist_file, **kwargs) :
        ItclObjectx.__init__(self)
        #----------------------------------------------------------------------
        # private variables:
        #----------------------------------------------------------------------
        self._Netlist_info       = {}      # information array
        self._netlist_info_done  = False   # flag for getting netlist info
        self._netlist_file       = None    # netlist file
        self._netlist_lines      = []      # save verbatim input
        self._netlist_title_line = None    # 1st line in the file
        self._netlist_line_list  = []      # uncontinued, uncommented list
        self._netlist_format     = "spice" # spice or spectre or verilog
        #----------------------------------------------------------------------
        # configuration options:
        #----------------------------------------------------------------------
        self._add_options({
            "verbose"   : [False,    None],
            "simulator" : ["sspice", self._config_simulator_callback],
        })
        #----------------------------------------------------------------------
        # all keyword arguments are configuration options:
        #----------------------------------------------------------------------
        for key, value in list(kwargs.items()) :
            self[key] = value
        self._read_netlist(netlist_file)
    #==========================================================================
    # METHOD : SimulatorNetlist::_config_simulator_callback
    # PURPOSE : simulator configuration callback
    #==========================================================================
    def _config_simulator_callback(self) :
        simulator = self["simulator"]
        if simulator in SimulatorNetlist._SimulatorDB :
            self._netlist_format = SimulatorNetlist._SimulatorDB[simulator][0]
        else :
            self.fatal("simulator \"" + simulator + "\" not supported")
    #==========================================================================
    # METHOD : SimulatorNetlist::get
    # PURPOSE : access
    #==========================================================================
    def get(self, what, **kwargs) :
        """ access method for several parameters.

        **arguments**:

            **what** (string)

                 specify what to retrieve:

                     * netlist-file: return netlist file path

                     * netlist-format: netlist format (circuit simulator)

                     * original-netlist: unmodified netlist text

                     * filtered-netlist: netlist after line-continuations and other
                       preprocessing has been done

                     * subckts: list of subcircuits defined in the netlist

                     * insts: list of subcircuit instances in the netlist

                     * caps: list of capacitors in the netlist

                     * ress: list of resistors in the netlist

            **\*\*kwargs** (dict)

                unused

        """
        if   what == "netlist-file" :
            return self._netlist_file
        elif what == "netlist-format" :
            return self._netlist_format
        elif what == "original-netlist" :
            return self._netlist_lines
        elif what == "filtered-netlist" :
            return "\n".join(self._netlist_line_list)
        elif what == "subckts" :
            self._netlist_info()
            return self._Netlist_info["subckts"]
        elif what == "insts" :
            self._netlist_info()
            return self._Netlist_info["insts"]
        elif what == "caps" :
            self._netlist_info()
            return self._Netlist_info["caps"]
        elif what == "ress" :
            self._netlist_info()
            return self._Netlist_info["ress"]
        self.warning("unsupported argument: \"" + what + "\"")
        return None
    #==========================================================================
    # METHOD : SimulatorNetlist::get_subckt
    # PURPOSE : access
    #==========================================================================
    def get_subckt(self, subckt, detail) :
        """ get subcircuit information.

        **arguments**:

            **subckt** (str)

                name of subcircuit

            **detail** (str)

                one of:

                   * ports: return list of subcircuit ports

        """
        self._netlist_info()
        if detail in ("ports") :
            key = "subckt-" + subckt + "-" + detail
            if key in self._Netlist_info :
                return self._Netlist_info[key]
            else :
                self.warning("no information for subckt " + subckt)
        else :
            this = __name__
            self.warning("usage: " + this + ".get_subckt(<subckt>, \"ports\")")
        return None
    #==========================================================================
    # METHOD : SimulatorNetlist::get_inst
    # PURPOSE : access
    #==========================================================================
    def get_inst(self, inst, detail) :
        """ get subcircuit instance information.

        **arguments**:

            **inst** (str)

                name of subcircuit instance

            **detail** (str)

                one of:

                   * ports: return list of instance ports

                   * params: return list of instance parameters

                   * subckt: return subcircuit name

        """
        self._netlist_info()
        if detail in ("ports", "params", "subckt") :
            key = "inst-" + inst + "-" + detail
            if key in self._Netlist_info :
                return self._Netlist_info[key]
            else :
                self.warning("no information for instance " + inst)
        else :
            this = __name__
            self.warning("usage: " + this + ".get_inst(<inst>, \"(ports|params|subckt)\")")
        return None
    #==========================================================================
    # METHOD : SimulatorNetlist::get_cap
    # PURPOSE : access
    #==========================================================================
    def get_cap(self, cap, detail) :
        """ get capacitor information.

        **arguments**:

            **cap** (str)

                name of capacitor instance

            **detail** (str)

                one of:

                   * ports: return list of capacitor ports

                   * value: return capacitance value

        """
        self._netlist_info()
        if detail in ("ports", "value") :
            key = "cap-" + cap + "-" + detail
            if key in self._Netlist_info :
                return self._Netlist_info[key]
            else :
                self.warning("no information for capacitor " + cap)
        else :
            this = __name__
            self.warning("usage: " + this + ".get_cap(<cap>, \"(ports|value)\")")
        return None
    #==========================================================================
    # METHOD : SimulatorNetlist::get_res
    # PURPOSE : access
    #==========================================================================
    def get_res(self, res, detail) :
        """ get resistor information.

        **arguments**:

            **res** (str)

                name of resistor instance

            **detail** (str)

                one of:

                   * ports: return list of resistor ports

                   * value: return resistor value

        """
        self._netlist_info()
        if detail in ("ports", "value") :
            key = "res-" + res + "-" + detail
            if key in self._Netlist_info :
                return self._Netlist_info[key]
            else :
                self.warning("no information for resistor " + res)
        else :
            this = __name__
            self.warning("usage: " + this + ".get_res(<res>, \"(ports|value)\")")
        return None
    #==========================================================================
    # METHOD: SimulatorNetlist::_read_netlist (private)
    # PURPOSE: read netlist file
    # NOTES :
    #   * spice continued lines:
    #     + at beginning of line
    #   * spice comments:
    #     * at beginning of line
    #     $ inline
    #==========================================================================
    def _read_netlist(self, netlist_file) :
        if not os.path.isfile(netlist_file) :
            self.warning("netlist \"" + netlist_file + "\" is not readable")
            return
        if self["verbose"] :
            self.message("reading \"" + netlist_file + "\"")
        self._netlist_file = netlist_file
        f = open(netlist_file, "r")
        self._netlist_lines = f.read()
        f.close()
        if self._netlist_format == "spice" :
            lines = re.sub("\r", " ", self._netlist_lines)
            lines = re.sub("\n *\\+", " ", lines)
            lines = lines.lower()
            llines = lines.split("\n")
            # for line in llines:
            #   print line
            # sys.exit()

            self._netlist_line_list =[]
            self._netlist_title_line = llines.pop(0)
            self._netlist_line_list.append(self._netlist_title_line)
            for line in llines :
                m = re.search("^ *\*", line)
                if m :
                    continue
                line = re.sub("\$.*$", "", line)
                line = line.strip()
                if line :
                    self._netlist_line_list.append(line)
    #==========================================================================
    # METHOD : SimulatorNetlist::_netlist_info (private)
    # PURPOSE : subcircuit information, (to be extended)
    #==========================================================================
    def _netlist_info(self) :
        if self._netlist_info_done :
            return
        if self["verbose"] :
            self.message("gathering netlist information")
        self._Netlist_info["ress"]    = []
        self._Netlist_info["caps"]    = []
        self._Netlist_info["subckts"] = []
        self._Netlist_info["insts"]   = []
        for line in self._netlist_line_list :
            m = re.search("^r", line)
            if m :
                lline = line.split()
                if len(lline) == 4 :
                    res, node1, node2, value = lline
                else :
                    self.warning("resistor line doesn't have 4 items:", "  " + line)
                    continue
                value = decida.spice_value(value)
                self._Netlist_info["ress"].append(res)
                self._Netlist_info["res-" + res + "-ports"] = (node1, node2)
                self._Netlist_info["res-" + res + "-value"] = value
                continue
            m = re.search("^c", line)
            if m :
                lline = line.split()
                if len(lline) == 4 :
                    cap, node1, node2, value = lline
                else :
                    self.warning("capacitor line doesn't have 4 items:", "  " + line)
                    continue
                value = decida.spice_value(value)
                self._Netlist_info["caps"].append(cap)
                self._Netlist_info["cap-" + cap + "-ports"] = (node1, node2)
                self._Netlist_info["cap-" + cap + "-value"] = value
                continue
            m = re.search("^.subckt", line)
            if m :
                lline = line.split()
                lline.pop(0)
                subckt = lline.pop(0)
                self._Netlist_info["subckts"].append(subckt)
                self._Netlist_info["subckt-" + subckt + "-ports"] = lline
                continue
            m = re.search("^x", line)
            if m :
                line   = re.sub(" *= *", "=", line)
                lline  = line.split()
                inst   = lline.pop(0)
                ports  = []
                params = []
                isport = True
                for item in lline :
                    if isport :
                        m = re.search("=", item)
                        if m :
                            isport = False
                            params.append(item)
                        else :
                            ports.append(item)
                    else :
                        m = re.search("=", item)
                        if m :
                            params.append(item)
                        else :
                            self.warning("ports follow params:", "  " + line)
                subckt = ports.pop(-1)
                self._Netlist_info["insts"].append(inst)
                self._Netlist_info["inst-" + inst + "-subckt"] = subckt
                self._Netlist_info["inst-" + inst + "-ports"]  = ports
                self._Netlist_info["inst-" + inst + "-params"] = params
        self._netlist_info_done = True
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # original methods not yet translated:
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : SimulatorNetlist::capacitance_report
    # PURPOSE : total parasitic capacitance to each node
    #==========================================================================
    def capacitance_report(self, report_format="column") :
        Cap = {}
        for cap in self.get("caps") :
            ports = self.get_cap(cap, "ports")
            value = float(self.get_cap(cap, "value"))
            if len(ports) == 2 :
                node1, node2 = ports
            else :
                self.warning("capacitor \"%s\" doesn't have 2 ports!" % (cap))
                continue
            if not node1 in Cap :
                Cap[node1] = 0.0
            if not node2 in Cap :
                Cap[node2] = 0.0
            Cap[node1] += value
            Cap[node2] += value
        report = []
        icap = -1
        nodes = list(Cap.keys())
        nodes.sort()
        for node in nodes :
            capff = Cap[node]*1e15
            if   report_format == "column" :
                report.append("%-20s %8.3f fF" % (node, capff))
            elif report_format == "spice" :
                icap += 1
                cname  = "c_%d" % (icap)
                report.append("%-8s %-20s vss %8.3ff" % (cname, node, capff))
        return "\n".join(report)
    #==========================================================================
    # METHOD  : SimulatorNetlist::time_constants
    # PURPOSE : total capacitance/conductance/time-constants for each node
    # NOTES :
    #   * for R-C/CC extractions
    #==========================================================================
    def _time_constants(self, **kwargs) :
        pass
    #==========================================================================
    # METHOD:  flatten
    # PURPOSE: flatten a hierarchical netlist
    # OPTIONS:
    #   % -subckt
    #     specify main_subckt (default = last subckt in file)
    #   % -main
    #     main_subckt lines to main circuit, otherwise to subcircuit (default)
    # NOTES:
    #   * there must be a main subckt: if not, surround main circuit lines
    #     with .subckt .ends lines.  Or generate netlist embedded in a testbench
    #==========================================================================
    def _flatten(self, **kwargs) :
        pass
