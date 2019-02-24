################################################################################
# CLASS    : Parameters
# PURPOSE  : parameter database
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:22:47 2013
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
import math
from decida.Parameter   import Parameter
from decida.ItclObjectx import ItclObjectx

class Parameters(ItclObjectx) :
    """
    **synopsis**:

        Parameter set manager class.

        *Parameters* manages a set of instances of the *Parameter* class.
        Each *Parameter* instance has associated current value and ranges.

        *LevMar* and *Fitter* use the *Parameters* instance to manage
        the optimization.

    **constructor arguments**:

        **\*\*kwargs** (dict)

              keyword=value specifications:
              configuration-options

    **configuration options**:

        **verbose** (bool, default=False)

            If verbose is True, print more information if available.

        **gui** (bool, default=True)

            flag to indicate that a *Parameters* graphical user-interface
            should be displayed. **Not currently implemented**

    **example** (from test_Parameters): ::

        from decida.Parameters import Parameters
        #-----------------------------------------------------------------
        # specs:
        # name, initial_value, include,
        #     lower_limited, upper_limited, lower_limit, upper_limit
        #-----------------------------------------------------------------
        parobj = Parameters(specs=(
           ("L" , 150e-12, True, True, False, 0.0, 0.0),
           ("Co", 250e-15, True, True, False, 0.0, 0.0),
           ("Cu", 120e-15, True, True, False, 0.0, 0.0),
           ("C1",  25e-15, True, True, False, 0.0, 0.0),
           ("C2",  30e-15, True, True, False, 0.0, 0.0),
        ))
        parobj.show("L")
        parobj.modify("L", tied="1.0/(math.pow(2*math.pi*10e9,2)*Co)")
        parobj.values([L,Co,Cu,C1,C2])
        parobj.show("L")

    **public methods**:

        * public methods from *ItclObjectx*

        * indexing:

          * <parameters_object>["<parameter_name>"] returns the
             current value of the parameter named <parameter_name>

          * <parameters_object>["<config_option>"] returns the
             value of the configuration option named <config_option>

          * <parameters_object>["<parameter_name>"]=<value> sets the
             current value of the parameter named <parameter_name> to <value>

          * <parameters_object>["<config_option>"]=<value> sets the
             value of the configuration option named <config_option> to <value>

        * length:

          * len(<parameters_object>) returns the number of parameters
            in the parameter set.

        * parameter-attributes :

          * each parameter instance has the following attributes, many which
            pertain only to Levenberg-Marquardt optimization:

            +----------------+----------+---------------------------------+
            | attribute:     | default  | description:                    |
            |                | value:   |                                 |
            +================+==========+=================================+
            | initial_value  | 0.0      | first value of parameter        |
            +----------------+----------+---------------------------------+
            | current_value  | 0.0      | current value of parameter      |
            +----------------+----------+---------------------------------+
            | include        | True     | parameter is not fixed          |
            +----------------+----------+---------------------------------+
            | lower_limited  | True     | parameter has a lower-limit     |
            +----------------+----------+---------------------------------+
            | lower_limit    | 0.0      | the lower-limit                 |
            +----------------+----------+---------------------------------+
            | upper_limited  | False    | parameter has an upper-limit    |
            +----------------+----------+---------------------------------+
            | upper_limit    | 0.0      | the upper-limit                 |
            +----------------+----------+---------------------------------+
            | step           | 0.0      | absolute step for derivatives   |
            +----------------+----------+---------------------------------+
            | relative_step  | 0.0      | relative step for derivatives   |
            +----------------+----------+---------------------------------+
            | side           | 1        | side to take derivatives:       |
            |                |          | 1=forward, -1=reverse           |
            |                |          | 2=two-sided                     |
            +----------------+----------+---------------------------------+
            | minstep        | 0.0      | minimum iteration step          |
            |                |          | (not used)                      |
            +----------------+----------+---------------------------------+
            | maxstep        | 0.0      | maximum iteration step          |
            +----------------+----------+---------------------------------+
            | tied           | ""       | expression to tie parameter     |
            |                |          | with other parameters           |
            +----------------+----------+---------------------------------+
            | print          | True     | print parameter value at        |
            |                |          | each iteration                  |
            +----------------+----------+---------------------------------+

        * parameter-conditions:

          * parameters can be checked for the following conditions:

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
    #==========================================================================
    # METHOD  : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, parent=None, specs=None, **kwargs) :
        ItclObjectx.__init__(self)
        #----------------------------------------------------------------------
        # private variables:
        #----------------------------------------------------------------------
        self.__parent = parent
        self.__Component  = {}
        self.__parameters = []
        self.__ParHandle  = {}
        self.__mapped = False
        #----------------------------------------------------------------------
        # configuration options:
        #----------------------------------------------------------------------
        self._add_options({
            "verbose"        : [False, None],
            "gui"            : [True,  None],
        })
        #----------------------------------------------------------------------
        # keyword arguments are all configuration options
        #----------------------------------------------------------------------
        for key, value in list(kwargs.items()) :
            self[key] = value
        #----------------------------------------------------------------------
        # add any parameters from specs
        # specs should be in less restrictive form
        #----------------------------------------------------------------------
        for spec in specs :
            par, init, incl, fllim, fulim, llim, ulim  = spec
            self.add(par, initial_value=init, include=incl,
                lower_limited=fllim, lower_limit=llim,
                upper_limited=fulim, upper_limit=ulim,
            )
        #----------------------------------------------------------------------
        # build gui:
        #----------------------------------------------------------------------
        if self["gui"] :
            self._gui()
    #==========================================================================
    # METHOD  : __len__
    # PURPOSE : return number of parameters
    #==========================================================================
    def __len__(self):
        return len(self.__parameters)
    #==========================================================================
    # METHOD  : __getitem__
    # PURPOSE : return config option or parameter value
    #==========================================================================
    def __getitem__(self, item):
        if   item in self.config_options() :
            return ItclObjectx.__getitem__(self, item)
        elif item in self.__parameters :
            return self.__ParHandle[item]["current_value"]
        self.warning("config option or parameter \"%s\" not present" % (item))
        return None
    #==========================================================================
    # METHOD  : __setitem__
    # PURPOSE : return config option or parameter value
    #==========================================================================
    def __setitem__(self, item, value):
        if item in self.config_options() :
            self[item] = value
        elif item in self.__parameters :
            self.__ParHandle[item]["current_value"] = value
        else :
            self.warning("config option or parameter \"%s\" not present" % (item))
            return
    #==========================================================================
    # METHOD  : show
    # PURPOSE : show parameters and attributes
    #==========================================================================
    def show(self, par=None):
        """ show parameters and attributes.

        **arguments**:

            **par** (str, default=None)

                parameter name to show.  If not specified, all parameters are
                shown.

        **results**:

            * parameter name and attributes of the specified parameter, or
              all parameters if par is not specified, are displayed.

        """
        if par is None:
            pars = self.pars()
        else :
            pars = list(par)
        for parname in pars:
            print("%" * 72)
            print("parameter: ", parname)
            print("%" * 72)
            self.__ParHandle[parname].show()
    #==========================================================================
    # METHOD  : pars
    # PURPOSE : return parameter names
    #==========================================================================
    def pars(self):
        """ return parameter names.

        **results**:

            * list of parameter names in the parameter set is returned.

        """
        return self.__parameters
    #==========================================================================
    # METHOD  : reset
    # PURPOSE : reset all parameters to initial values
    #==========================================================================
    def reset(self):
        """ reset all parameters to initial values

        **results**:

            * parameters are reset to initial values.

        """
        for par in self.pars() :
            self.__ParHandle[par].reset()
    #==========================================================================
    # METHOD  : check
    # PURPOSE : return attr of parameter
    #==========================================================================
    def check(self, par, condition, verbose=False):
        """ check a parameter condition.

        **arguments**:

            **par** (str)

                 parameter to check

            **condition** (str)

                 parameter condition to check

            **verbose** (bool, default=False)

                 enable or disable verbose mode.

        **results**:

            * if condition is True for parameter *par*, return True, else False.

        """
        return self.__ParHandle[par].check(condition, verbose=verbose)
    #==========================================================================
    # METHOD  : list_of_pars
    # PURPOSE : return list of pars with attributes
    #==========================================================================
    def list_of_pars(self, condition) :
        """ return list of parameters with condition.

        **arguments**:

            **condition** (str)

                 condition string for filtering parameter set.

        **results**:

            * parameter list is returned with pars with condition True.

        """
        return [par for par in self.pars() if self.check(par, condition)]
    #==========================================================================
    # METHOD  : list_of_attr
    # PURPOSE : return list of parameter attributes
    #==========================================================================
    def list_of_attr(self, condition) :
        """ return bool list of checked condition for each parameter.

        **arguments**:

            **condition** (str)

                 condition string for checking parameter set.

        **results**:

            * Returns list of boolean values for whether or not the condition
              is met by each parameter.

        """
        return [self.check(par, condition) for par in self.pars()]
    #==========================================================================
    # METHOD  : add
    # PURPOSE : add a parameter and attributes
    # NOTES : parameter itself checks attribute
    #==========================================================================
    def add(self, par, **kwargs) :
        """ add a parameter and specifications to the parameter set.

        **arguments**:

            **par** (str)

                 parameter name to add.

            **\*\*kwargs** (dict):

                 <attribute>=<value> specifications for the parameter

        **results**:

            * The parameter set is appended with par.

            * The attributes of the parameter are set to specified values.

        """
        if par in self.pars() :
            self.warning("parameter \"%s\" already present" % (par))
            return
        self.__parameters.append(par)
        self.__ParHandle[par] = Parameter(par, **kwargs)
    #==========================================================================
    # METHOD  : modify
    # PURPOSE : modify a parameter's attributes
    #==========================================================================
    def modify(self, par, **kwargs) :
        """ modify a parameter's attributes

        **arguments**:

            **par** (str)

                 parameter name to modify.

            **\*\*kwargs** (dict)

                 <attribute>=<value> specifications for the parameter

        **results**:

            * The attributes of the parameter are modified.

        """
        if not (par in self.pars()) :
            self.warning("parameter \"%s\" not present" % (par))
            return
        #self.__ParHandle[par] = Parameter(par, **kwargs)
        for key, value in list(kwargs.items()) :
            self.__ParHandle[par][key] = value
    #==========================================================================
    # METHOD  : free_pars
    # PURPOSE : return free parameters
    #==========================================================================
    def free_pars(self):
        """ return list of parameters that are free to vary.

        **results**:

            * Returns a list of parameters that have the attribute "free".

        """
        return self.list_of_pars("free")
    #==========================================================================
    # METHOD  : free_indices
    # PURPOSE : return indices of free parameters
    #==========================================================================
    def free_indices(self):
        """ return list of parameter indices for paramteres that
            are free to vary.

        **results**:

            * Returns a list of indices (within the parameter set) of
              parameters that have the attribute "free".

        """
        return [i for i, par in enumerate(self.pars()) if self.check(par, "free")]
    #==========================================================================
    # METHOD  : values
    # PURPOSE : set or return parameter values
    # NOTES :
    #    * fixed-parameters aren't changed
    #    * if par is tied, wait to set it and then use the tied value
    #    * tied expressions can only include parameters that aren't tied
    #==========================================================================
    def values(self, values=None):
        """ set or return parameter values.

        **arguments**:

            **values** (list or tuple, default=None)

                 list of values to set parameters current value attribute.
                 if values is not specified, return a list of parameter
                 current values.

        **results**:

            * Every parameter current value is set to a value in the value
              list, if values is specified.

            * If values is not specified, return the list of parameter
              current values.

        """
        if values is not None :
            if len(values) != len(self.pars()) :
                self.error("number of values != number of parameters")
                return None
            free_pars   = self.free_pars()
            tied_pars   = self.list_of_pars("tied")
            untied_pars = self.list_of_pars("untied")
            for par, value in zip(self.pars(), values) :
                if par in free_pars :
                    self[par] = float(value)
            if tied_pars :
                dvars = dict(locals())
                dvars.update(globals())
                for par in untied_pars :
                    dvars[par] = float(self[par])
                for par in tied_pars :
                    tied_expr = self.__ParHandle[par]["tied"]
                    value = eval(tied_expr, dvars)
                    self[par] = float(value)
                    dvars[par] = self[par]
        return [self[par] for par in self.pars()]
    #==========================================================================
    # METHOD  : free_values
    # PURPOSE : set or return free parameter values
    # NOTES :
    #    * same as self.values, but only free parameters set/returned
    #==========================================================================
    def free_values(self, values=None):
        """ set or return free parameter values.

        **arguments**:

            **values** (list or tuple, default=None)

                 list of values to set free parameters current value attribute.
                 if values is not specified, return a list of free parameter
                 current values.

        **results**:

            * Every free parameter current value is set to a value in the value
              list, if values is specified.

            * If values is not specified, return the list of free parameter
              current values.

        """
        free_pars = self.free_pars()
        if values is not None :
            if len(values) != len(free_pars) :
                self.error("number of values != number of free parameters")
                return None
            tied_pars   = self.list_of_pars("tied")
            untied_pars = self.list_of_pars("untied")
            for par, value in zip(free_pars, values) :
                self[par] = float(value)
            if tied_pars :
                dvars = dict(locals())
                dvars.update(globals())
                for par in untied_pars :
                    dvars[par] = float(self[par])
                for par in tied_pars :
                    tied_expr = self.__ParHandle[par]["tied"]
                    value = eval(tied_expr, dvars)
                    self[par] = float(value)
                    dvars[par] = self[par]
        return [self[par] for par in free_pars]
    #==========================================================================
    # METHOD  : check_correct_step_limits
    # PURPOSE : return True if step limits are consistent
    #           (minstep < maxstep)
    #==========================================================================
    def check_correct_step_limits(self) :
        """ check whether parameter step limits are consistent.

        **results**:

            * Check to see if all parameters have attributes
              minstep < maxstep.

        """
        ok = True
        for par in self.pars() :
            ok &= self.check(par, "correct_step_limits", verbose=True)
        return ok
    #==========================================================================
    # METHOD  : check_correct_limits
    # PURPOSE : return True if limits are consistent (lower_limit < upper_limit)
    #==========================================================================
    def check_correct_limits(self) :
        """ check whether parameter limits are consistent.

        **results**:

            * Check to see if all parameters have attributes
              lower_limit < upper_limit.

        """
        ok = True
        for par in self.pars() :
            ok &= self.check(par, "correct_limits", verbose=True)
        return ok
    #==========================================================================
    # METHOD  : check_within_limits
    # PURPOSE : return True if current_value within [lower_limit, upper_limit]
    #==========================================================================
    def check_within_limits(self) :
        """ check whether parameter current value is within limits.

        **results**:

            * Check to see if all parameters have current value within
              the range lower_limit, upper_limit, if the parameter is limited.

        """
        ok = True
        for par in self.pars() :
            ok &= self.check(par, "within_limits", verbose=True)
        return ok
    #==========================================================================
    # METHOD  : check_any_free_limited
    # PURPOSE : return True if any free parameter is limited
    #==========================================================================
    def check_any_free_limited(self) :
        """ check whether any free parameters are limited.

        **results**:

            * Check to see if any free parameters are limited.

        """
        flag = False
        for par in self.free_pars() :
            flag |= self.check(par, "limited")
        return flag
    #==========================================================================
    # METHOD  : check_any_step_limited
    # PURPOSE : return True if any free parameter is step-limited
    #==========================================================================
    def check_any_free_step_limited(self) :
        """ check whether any free parameters are step limited.

        **results**:

            * Check to see if any free parameters are step limited.

        """
        flag = False
        for par in self.free_pars() :
            flag |= self.check(par, "step_limited")
        return flag
    #==========================================================================
    # METHOD  : _gui
    # PURPOSE : gui
    #==========================================================================
    def _gui(self) :
        pass
