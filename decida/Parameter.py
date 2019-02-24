################################################################################
# CLASS    : Parameter
# PURPOSE  : optimization parameter
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:22:31 2013
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
from decida.ItclObjectx import ItclObjectx

class Parameter(ItclObjectx) :
    """
    **synopsis**:

        Parameter attribute manager class.

        *Parameter* manages one parameter with a number of attributes.

        A set of *Parameter* instances is managed by the *Parameters* class.

    **constructor arguments**:

        **par** (str)

            parameter name

        **\*\*kwargs** (dict)

              keyword=value specifications:
              configuration-options (parameter attributes)

    **configuration options (parameter attributes)**:

        **initial_value** (float, default=0.0)

            first value of parameter

        **current_value** (float, default=0.0)

            current value of parameter

        **include** (bool, default=True)

            if include is True, parameter is not fixed

        **lower_limited** (bool, default=True)

            parameter has a lower-limit

        **lower_limit** (float, default=0.0)

            the lower-limit

        **upper_limited** (bool, default=False)

            parameter has an upper-limit

        **upper_limit** (float, default=0.0)

            the upper-limit

        **step** (float, default=0.0)

            absolute step for derivatives

        **relative_step** (float, default=0.0)

            relative step for derivatives

        **side** (int, default=1)

            side to take derivatives:

              *  1: forward

              * -1: reverse

              *  2: two-sided

        **minstep** (float, default=0.0)

            minimum iteration step (not used)

        **maxstep** (float, default=0.0)

            maximum iteration step

        **tied** (str, default="")

            expression to tie parameter with other parameters

        **print** (bool, default=True)

            if True, print parameter value at each iteration

    **public methods**:

        * public methods from *ItclObjectx*

    """
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Parameter main
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, par, **kwargs) :
        ItclObjectx.__init__(self)
        #----------------------------------------------------------------------
        # private variables:
        #----------------------------------------------------------------------
        self.__par = par
        #----------------------------------------------------------------------
        # configuration options:
        #----------------------------------------------------------------------
        self._add_options({
            "initial_value"  : [0.0,   None],
            "current_value"  : [0.0,   None],
            "include"        : [True,  None],
            "lower_limited"  : [True,  None],
            "lower_limit"    : [0.0,   None],
            "upper_limited"  : [False, None],
            "upper_limit"    : [0.0,   None],
            "step"           : [0.0,   None],
            "relative_step"  : [0.0,   None],
            "side"           : [1,     None],
            "minstep"        : [0.0,   None],
            "maxstep"        : [0.0,   None],
            "tied"           : ["",    self._config_tied_callback],
            "print"          : [True,  None],
        })
        #----------------------------------------------------------------------
        # keyword arguments are all configuration options
        #----------------------------------------------------------------------
        for key, value in list(kwargs.items()) :
            self[key] = value
        self.reset()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Parameter configuration option callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _config_tied_callback
    # PURPOSE : configure tied
    #==========================================================================
    def _config_tied_callback(self) :
        tied = self["tied"]
        tied = tied.strip()
        self._ConfigOption["tied"] = tied
    #==========================================================================
    # METHOD  : reset
    # PURPOSE : reset current value to initial value
    #==========================================================================
    def reset(self) :
        """ reset current value to initial value.

        **results**:

            * current_value attribute is set to initial value_attribute.

        """
        self["current_value"] = self["initial_value"]
    #==========================================================================
    # METHOD  : show
    # PURPOSE : show config options
    #==========================================================================
    def show(self) :
        """ show parameter attributes.

        **results**:

            * print out parameter attributes.

        """
        options  = ["initial_value", "current_value", "include"]
        options += ["lower_limit"]
        options += ["upper_limit"]
        options += ["tied"]
        for option in options:
            self.cshow(option)
    #==========================================================================
    # METHOD  : check
    # PURPOSE : return values based on condition
    # NOTES :
    #   * return True, False if "fixed", "free", "included", "limited", "tied"
    #   * "within" within limits (current value within max, min)
    #   * if condition is a config option return it
    #==========================================================================
    def check(self, condition, verbose=False) :
        """ check parameter conditions.

        **arguments**:

            **condition** (str)

                Specify one of the conditions: "fixed", "included", "tied",
                "untied", "free", "limited", "step_limited", "at_upper_limit",
                "at_lower_limit", "within_limits", "correct_limits",
                "correct_step_limits"

            **verbose** (bool, default=False)

                If verbose is True, print more information if available.

        **results**:

           * Return True or False, depending on condition.

           +----------------------+--------------------------------------------+
           | condition:           | description:                               |
           +======================+============================================+
           | fixed                | parameter is not allowed to vary           |
           +----------------------+--------------------------------------------+
           | included             | parameter is allowed to vary (free or tied)|
           +----------------------+--------------------------------------------+
           | tied                 | parameter is tied others by an expression  |
           +----------------------+--------------------------------------------+
           | untied               | not tied                                   |
           +----------------------+--------------------------------------------+
           | free                 | parameter is allowed to vary               |
           +----------------------+--------------------------------------------+
           | limited              | parameter is limited (upper or lower)      |
           +----------------------+--------------------------------------------+
           | step_limited         | value of parameter change for one          |
           |                      | iteration is limited                       |
           +----------------------+--------------------------------------------+
           | at_upper_limit       | parameter current value is at upper-limit  |
           +----------------------+--------------------------------------------+
           | at_lower_limit       | parameter current value is at lower-limit  |
           +----------------------+--------------------------------------------+
           | within_limits        | parameter current value is within limits   |
           +----------------------+--------------------------------------------+
           | correct_limits       | parameter upper_limit > lower_limit        |
           +----------------------+--------------------------------------------+
           | correct_step_limits  | parameter maxstep > minstep                |
           +----------------------+--------------------------------------------+

        """
        if   condition == "fixed" :
            return (not self["include"])
        elif condition == "included" :
            return self["include"]
        elif condition == "tied" :
            return (self.check("included") and self["tied"] != "" )
        elif condition == "untied" :
            return (self["tied"] == "" )
        elif condition == "free" :
            return (self.check("included") and not self.check("tied"))
        elif condition == "limited" :
            return (self["lower_limited"] or self["upper_limited"])
        elif condition == "step_limited" :
            return (self["minstep"] > 0 or self["maxstep"] > 0)
        elif condition == "at_upper_limit" :
            return (self["upper_limited"] and (
                self["current_value"] == self["upper_limit"]
            ))
        elif condition == "at_lower_limit" :
            return (self["lower_limited"] and (
                self["current_value"] == self["lower_limit"]
            ))
        elif condition == "within_limits" :
            if self.check("fixed") :
                return True
            if   self["upper_limited"] and (
                self["current_value"] > self["upper_limit"]
            ) :
                if verbose :
                    self.message("parameter %s is > upper_limit (%g)" %
                        (self.__par, self["upper_limit"])
                    )
                return False
            elif self["lower_limited"] and (
                self["current_value"] < self["lower_limit"]
            ) :
                if verbose :
                    self.message("parameter %s is < lower_limit (%g)" %
                        (self.__par, self["lower_limit"])
                    )
                return False
            else :
                return True
        elif condition == "correct_limits" :
            if self.check("fixed") :
                return True
            if not (self["upper_limited"] and self["lower_limited"]) :
                return True
            if self["lower_limit"] >= self["upper_limit"] :
                if verbose :
                    self.message("parameter %s lower_limit (%g) is >= upper_limit (%g)" %
                        (self.__par, self["lower_limit"], self["upper_limit"])
                    )
                return False
            else :
                return True
        elif condition == "correct_step_limits" :
            if self.check("fixed") :
                return True
            if ((self["minstep"] > 0.0) and
                (self["maxstep"] > 0.0) and
                (self["minstep"] > self["maxstep"])
            ) :
                if verbose :
                    self.message("parameter %s minstep (%g) is > maxstep (%g)" %
                        (self.__par, self["minstep"], self["maxstep"])
                    )
                return False
            else :
                return True
        elif condition in self.config_options() :
            return self[condition]
        return None
