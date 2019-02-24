################################################################################
# FUNCTION : vtb
# PURPOSE  : extract verilog files to run ncsim
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:26:29 2013
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
import os
import os.path
import shutil
import stat

#==========================================================================
# FUNCTION : vtb
# PURPOSE  : extract verilog testbench files
#==========================================================================
def vtb(netlistdir, testbench, check=False, mod_dir=None):
    """
    **synopsis**:

        Extract verilog testbench files from Cadence NCsim netlister.

    **arguments**:

        **netlistdir** (str)

            directory where netlists have been produced

        **testbench** (str)

            testbench name

        **check** (bool, default=False)

            if True, produce check files for debugging (NOT USED)

        **mod_dir** (str, default=None)

            directory to place modified modules

    """
    if not os.path.isdir(netlistdir) :
        print("netlist directory \"%s\" doesn't exist" % (netlistdir))
        return
    tb_dir = "ncsim_%s"  % (testbench)
    tb_lib = "%s/lib_%s" % (tb_dir, testbench)
    DoneCells = {}
    os.mkdir(tb_dir)
    os.mkdir(tb_lib)
    vin = "%s/verilog.inpfiles"   % (netlistdir)
    f = open(vin, "r")
    for line in f :
        line = line.strip()
        if len(line) < 1 :
            continue
        m = re.search("^//", line)
        if m :
            libcel   = ""
            vtype    = ""
            library  = ""
            cellname = ""
            cellview = ""
            m1 = re.search("// timscale", line)
            if m1 :
                vtype = "TIM"
                continue
            m1 = re.search("// HDL file - (\w+), (\w+), (\w+)\.", line)
            if m1 :
                vtype = "HDL"
                library  = m1.group(1)
                cellname = m1.group(2)
                cellview = m1.group(3)
                libcel= "%s:%s" % (library, cellname)
                continue
            m1 = re.search("// HDL file for (\w+), (\w+), (\w+)\.", line)
            if m1 :
                vtype = "HDL"
                library  = m1.group(1)
                cellname = m1.group(2)
                cellview = m1.group(3)
                libcel= "%s:%s" % (library, cellname)
                continue
            m1 = re.search("// netlist file - (\w+), (\w+), (\w+)\.", line)
            if m1 :
                vtype = "NET"
                library  = m1.group(1)
                cellname = m1.group(2)
                cellview = m1.group(3)
                libcel= "%s:%s" % (library, cellname)
                continue
            m1 = re.search("// globals file", line)
            if m1 :
                vtype = "GLO"
                library  = ""
                cellname = "cds_globals"
                cellview = "functional"
                libcel= "%s:%s" % (library, cellname)
                continue
            continue
        if (libcel in DoneCells) :
            print("cell \"%s\" already done" % (libcel))
        elif vtype in ("HDL", "NET", "GLO") :
            DoneCells[libcel] = 1
            vfile = line
            if vtype == "NET" or vtype == "GLO" :
                vfile = "%s/%s" % (netlistdir, vfile)
            if cellname == testbench :
                shutil.copy(vfile, "%s/%s.v" % (tb_dir, cellname))
            else :
                shutil.copy(vfile, "%s/%s.v" % (tb_lib, cellname))
                os.chmod("%s/%s.v" % (tb_lib, cellname), stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)
            print(library, cellname, cellview, vfile)
    #----------------------------------------------------------------------
    # write modifications into library
    #----------------------------------------------------------------------
    if mod_dir :
        if not os.path.isdir(mod_dir) :
            print("modification directory \"%s\" does not exist" % (mod_dir))
        else :
            mod_files = os.listdir(mod_dir)
            lib_files = os.listdir(tb_lib)
            for file_name in mod_files:
                if file_name in lib_files :
                    shutil.move("%s/%s" % (tb_lib, file_name),
                                "%s/%s.orig" % (tb_lib, file_name))
                shutil.copy("%s/%s" % (mod_dir, file_name),
                            "%s/%s" % (tb_lib, file_name))
