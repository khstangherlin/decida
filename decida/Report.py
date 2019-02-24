################################################################################
# CLASS    : Report
# PURPOSE  : report package
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:24:24 2013
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
from builtins import object
import os
import os.path
import shutil
import time

class Report(object) :
    """

    **synopsis**:

        Format and report data to file.

        *Report* manages a reporting scheme where data is to be written to a
        file in column-oriented format.

        The output format is space-separated values, but an additional
        comma-separated values format file can also be written.

        The *Report* *header* method specifies the names of the data columns.
        After each set of values (one value for each data column) is written
        to the file, the file is flushed.

    **constructor arguments**:

        **filename** (str)

            name of report file to generate.

        **format** (str) (optional, default=None)

            format string for report values.  If None, then report items
            are formatted as float.

        **comment_char** (str) (optional, default="#")

            character(s) to prepend to comments.

        **verbose** (bool, default=False)

            if true, print each report line to stdout.

        **csv** (bool, default=False)

            if true, report to a csv file.

    **results**:

        * if file already exists, move to file.bak

        * reports header, followed by reported lines, formated
          by the report format

    **example**:

        >>> from decida.Report import Report
        >>> rpt = Report("example1.txt", verbose=True)
        >>> rpt.header("time vscl")
        >>> for i in range(0, 20):
        >>>    t = i*1e-3/20
        >>>    v = 1.2 + 2.4*t + 840.0*t*t
        >>>    rpt.report(t, v)

    **public methods**:

    """
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Report main
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, filename, format=None, comment_char="#", verbose=False, csv=False) :
        self.format       = format
        self.verbose      = verbose
        self.comment_char = comment_char
        #-----------------------------------------
        # if file already exists, move it to *.bak
        #-----------------------------------------
        if os.path.isfile(filename) :
            shutil.move(filename, filename + ".bak")
        self.rpt = open(filename, "w")
        self.csv = None
        if csv :
            csvfilename = filename + ".csv"
            self.csv = open(csvfilename, "w")
    #==========================================================================
    # METHOD  : __del__
    # PURPOSE : destructor
    #==========================================================================
    def __del__(self) :
        self.rpt.close()
        if self.csv :
            self.csv.close()
    #==========================================================================
    # METHOD  : __output__
    # PURPOSE : output report line and flush to file
    #==========================================================================
    def __output__(self, s) :
        if (self.verbose) :
            print(s)
        self.rpt.write(s + "\n")
        self.rpt.flush()
        if self.csv :
            scsv = ",".join(s.split())
            self.csv.write(scsv + "\n")
            self.csv.flush()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Report user commands
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : comment
    # PURPOSE : generate a comment in the report file
    #==========================================================================
    def comment(self, comment) :
        """ generate a comment in the report file.
            no comments are placed in csv files.

            **comment** (str)

                comment string to put in report file, prepended with
                a comment-character (comment_char)
        """
        savecsv = self.csv
        self.csv = False
        self.__output__(self.comment_char + comment)
        self.csv = savecsv
    #==========================================================================
    # METHOD  : date
    # PURPOSE : generate a date/time comment in the report file
    #==========================================================================
    def date(self) :
        """ generate a date/time comment in the report file.
            no comments are placed in csv files.
        """
        date = time.asctime(time.localtime(time.time()))
        self.comment(" DATE: %s" % (date))
    #==========================================================================
    # METHOD  : user
    # PURPOSE : generate a user comment in the report file
    #==========================================================================
    def user(self) :
        """ generate a user comment in the report file.
            no comments are placed in csv files.
        """
        try :
            user = os.environ["USERNAME"]
        except :
            user = os.environ["USER"]
        self.comment(" USER: %s" % (user))
    #==========================================================================
    # METHOD  : header
    # PURPOSE : generate a header in the report file
    #==========================================================================
    def header(self, *args) :
        """ generate a header in the report file.
            if format is not specified, header is used to generate the format.

            **\*args** (str or lists of str)

                separate or combined header column names
                the column names can be separate list items, specified
                in a string with space separated fields, or specified in
                a list of strings
        """
        items = []
        for arg in args :
            if isinstance(arg, (list, tuple)) :
                for item in arg :
                    items.append(item)
            else :
                items.append(arg)
        #-----------------------------------------
        # join args and then split to get items:
        # args = "a b c" or "a", "b", "c"
        #-----------------------------------------
        head  = " ".join(items)
        items = head.split()
        if (self.format is None) :
            fmtlst = []
            for  item in items :
                fmtlst.append("%s")
            self.format = " ".join(fmtlst)
        self.__output__(" ".join(items))
    #==========================================================================
    # METHOD  : report
    # PURPOSE : generate a report line in the report file
    #==========================================================================
    def report(self, *args) :
        """ generate a report line in the report file.

            **\*args** (items or lists of items)

                items to report to the report file
                each argument can be a separate report item, or a list
                of report items.  The combined list of report items
                is formatted by the specified Report format.
        """
        items = []
        for arg in args :
            if isinstance(arg, (list, tuple)):
                for item in arg :
                    items.append(item)
            else :
                items.append(arg)

        if self.format is not None :
            try :
                self.__output__(self.format % tuple(items))
            except :
                strlst = [str(item) for item in items]
                self.__output__(" ".join(strlst))
        else :
            strlst = [str(item) for item in items]
            self.__output__(" ".join(strlst))
