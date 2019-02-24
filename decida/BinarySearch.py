################################################################################
# CLASS    : BinarySearch
# PURPOSE  : binary search
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:17:19 2013
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
from builtins import object
class BinarySearch(object) :
    """
    **synopsis**:

        Binary Search iterator class.

        BinarySearch organizes a binary search for a parameter value based on
        some external evaluation which gives a success or failure using
        trial parameter values presented by the BinarySearch instance.

        The binary search proceeds as follows:

            * Set the parameter to the low configuration value.

            * Bracket1 mode: stay or move the parameter value lower until the
              external evaluation produces success (if find_max is False,
              look for failure).

            * Set the parameter value to the high configuration value.

            * Bracket2 mode: stay or move the parameter value higher until the
              external evaluation producess failure (if find_max is False,
              look for success).

            * With the upper and lower brackets determined, search within their
              interval for the maximum value of the parameter which produces
              success (if find_max is False, look for the minimum value of the
              parameter which produces success).

            * Bracket trial values are changed according to the configuration
              options bracket_step (increase or decrease by a specific step),
              or bracket_mult (increase or decrease by multiplying or dividing
              by a specific factor).  Also the initial brackets are limited by
              min and max configuration options.

            * Convergence is reported when the absolute change in trial
              parameter values is less than the min_delta configuration option.


    **constructor arguments**:

        **low** (float)

             first parameter value to try in binary-search
             bracket lower-bound (bracket1) mode.
             If the evaluation produces a success,
             the  mode proceeds to bracket upper-bound (bracket2) mode.
             Otherwise, the parameter is decremented by bracket_step,
             if specified, or divided by bracket_mult if specified.

        **high** (float)

             first parameter value to try in binary-search
             bracket upper-bound (bracket2) mode.
             If the evaluation produces a success,
             the  mode proceeds to binary search (bisection) mode.
             Otherwise, the parameter is incremented by bracket_step,
             if specified, or multiplied by bracket_mult if specified.

        **min_value** (float)

             minimum value of the parameter.
             If searching in bracket1 mode goes below min, the binary
             search stops.

        **max_value** (float)

             maximum value of the parameter.
             If searching in bracket2 mode goes above max, the binary
             search stops.

        **min_delta** (float, default=None)

             Convergence is achieved if the absolute change between parameter
             steps is less than min_delta.

        **bracket_step** (float, default=None)

             If specified, the parameter is revised by one bracket_step
             in bracket1 or bracket2 modes.

        **bracket_mult** (float, default=None)

             If specified, the parameter is revised by scaling by bracket_mult
             in bracket1 or bracket2 modes.

        **find_max** (bool, default=True)

             If True, maximum value of the parameter is found which gives
             a successful result.
             If False, bracket modes and searching goes in the opposite
             sense.

    **example** (from test_BinarySearch_2): ::

        def funct(x) :
            a, b, c = 1.0, -4.0, 2.0
            y = a*x*x + b*x + c
            return y

        bin = BinarySearch(
             low=1.0, high=2.0, min=-10, max=3,
             min_delta=1e-6, bracket_step=0.1
        )

        bin.start()
        while not bin.is_done() :
            x=bin.value()
            f=funct(x)
            success = (f >= 0)
            print("%-10s: x=%-18s y=%-18s %-5s" % (bin.mode(), x, f, success))
            bin.update(success)

        print
        print("x = ", bin.last_success())

    **public methods**:

    """
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # BinarySearch main
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, low, high, min_value, max_value, min_delta=None, bracket_step=None, bracket_mult=None, find_max=True):
        self.__low   = low
        self.__high  = high
        self.__min   = min_value
        self.__max   = max_value
        self.__delta = min_delta
        self.__step  = bracket_step
        self.__mult  = bracket_mult
        self.__find_max     = find_max
        if self.__high == self.__low :
            print("error: high == low")
            exit()
        if self.__mult is not None and self.__mult < 1.0 :
            print("error: mult < 1")
            exit()
        if self.__step is not None and self.__step < 0.0 :
            print("error: step < 0")
            exit()
        if self.__delta is None :
            self.__delta = (self.__high - self.__low) *0.0001
        if self.__step is None and self.__mult is None :
            self.__mult = 2.0
        #----------------------------
        # define other attributes
        #----------------------------
        self.__last_success = None
        self.__par1  = self.__low
        self.__par2  = self.__high
        self.__par   = self.__par1
        self.__mode  = "start"
        self.start()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # BinarySearch user commands
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : mode
    # PURPOSE : return the current binary search mode
    #==========================================================================
    def mode(self) :
        """ return the binary search mode.

        **results**:

            * The binary search mode is returned.  The modes are:

                * start : initial mode.

                * bracket1 : search for the lowest value of the parameter that
                  produces a successful result.

                * bracket2 : search for the highest value of the parameter that
                  produces an unsuccessful result.

                * bisection : binary search mode.

                * done : convergence.

        """
        return(self.__mode)
    #==========================================================================
    # METHOD  : is_done
    # PURPOSE : return true if convergence is achieved
    #==========================================================================
    def is_done(self) :
        """ return True if convergence is achieved.

        **results**:

            * Return True if bisection has converged.

        """
        return(self.__mode == "done")
    #==========================================================================
    # METHOD  : value
    # PURPOSE : return current value of the parameter
    #==========================================================================
    def value(self) :
        """ return the updated parameter value.

        **results**:

            * Returns the updated parameter value which is to be
              tried for success.

        """
        return(self.__par)
    #==========================================================================
    # METHOD  : last_success
    # PURPOSE : return the last successful parameter value
    #==========================================================================
    def last_success(self) :
        """ return the last successful parameter value.

        **results**:

            * Returns the parameter value which last achieved success.

        """
        return(self.__last_success)
    #==========================================================================
    # METHOD  : start
    # PURPOSE : reset parameter value, brackets, and binary search mode
    #==========================================================================
    def start(self) :
        """ reset parameter value, brackets and binary search mode.

        **results**:

            * Resets the binary search object to its starting state.

            * The parameter is set to the first trial value.

            * Initial bracket values are reset.

            * The bisection mode is set to "start"

        """
        self.__last_success = None
        self.__par1  = self.__low
        self.__par2  = self.__high
        self.__par   = self.__par1
        self.__mode  = "start"
    #==========================================================================
    # METHOD  : update
    # PURPOSE : return new value of parameter based on success
    #==========================================================================
    def update(self, success) :
        """ update the trial parameter value.

        **results**:

            * Revise the parameter value based on the two last bracketed
              binary search values and success or failure of the current
              parameter value.

            * Binary search brackets are revised.

        """
        proceed = success if self.__find_max else (not success)
        if success :
            self.__last_success = self.__par
        if   self.__mode == "start" :
            if proceed :
                self.__par1 = self.__par
                self.__par  = self.__par2
                self.__mode = "bracket2"
            else :
                self.__mode = "bracket1"
        elif self.__mode == "bracket1" :
            if proceed :
                self.__par1 = self.__par
                self.__par  = self.__par2
                self.__mode = "bracket2"
            else :
                if self.__par <= self.__min :
                    self.__mode = "done"
                else :
                    if   self.__step is not None :
                        self.__par -= self.__step
                    elif self.__mult is not None:
                        self.__par /= self.__mult
                    self.__par = max(self.__par, self.__min)
        elif self.__mode == "bracket2" :
            if not proceed :
                self.__par2 = self.__par
                self.__par  = (self.__par2 + self.__par1)*0.5
                self.__mode = "bisection"
            else :
                if self.__par >= self.__max :
                    self.__mode = "done"
                else :
                    self.__par1 = self.__par
                    if   self.__step is not None :
                        self.__par += self.__step
                    elif self.__mult is not None:
                        self.__par *= self.__mult
                    self.__par = min(self.__par, self.__max)
        elif self.__mode == "bisection" :
            if proceed :
                self.__par1 = self.__par
            else :
                self.__par2 = self.__par
            self.__par  = (self.__par2 + self.__par1)*0.5
            if abs(self.__par2 - self.__par1) < self.__delta :
                self.__mode = "done"
