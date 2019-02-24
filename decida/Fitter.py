################################################################################
# CLASS    : Fitter
# PURPOSE  : decida Fitter object
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:20:26 2013
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
import re
import decida
from decida.ItclObjectx  import ItclObjectx
from decida.LevMar       import LevMar
from decida.Parameters   import Parameters

class Fitter(ItclObjectx) :
    """
    **synopsis**:

        Fit parameterized equation set to data.

        *Fitter* is a wrapper around the Levenberg-Marquardt least-squares
        optimization class *LevMar*.  One model equation set is specified,
        and one parameter set is specified when the instance is created.

    **constructor arguments**:

        **model_eqns** (str)

           Set of equations involving data columns, and specified parameters
           equation set produces one data column, specified by the
           model_col configuration option.

        **par_specs** (str)

           Set of specifications for a set of model parameters.  The
           specifications are parameter name, initial value, the keyword
           *include* if the parameter is to be included in the optimization,
           lower_limit=value and upper_limit=value.  The last two
           specifications are optional, and if not specified the parameter
           is unbounded on the respective end.

        **\*\*kwargs** (dict)

           keyword=value specifications:
           configuration-options

    **configuration options**:

        **data** (Data object handle, default=None)

           Data object which contains data to be fitted to the model equations.
           Model and residual columns are created in the Data object.

        **meast_col** (str, default="")

           The data column which contains the data to be fitted.

        **model_col** (str, default="")

           The data column which is to be created to fit the meast_col data.

        **error_col** (str, default="")

           The relative or absolute error between the model_col
           and meast_col data

        **residual**  (str, default="relative")

           Specify whether residual is relative or absolute.  It must
           be one of these two values.

        **quiet** (bool, default=False)

           If True, do not print as much information from the LevMar class
           instance.

    **example** (from test_Fitter): ::

            d=Data()
            d.read("icp_tr_diff.report")
            ftr=Fitter(
                \"\"\"
                    dicp_mod = a0 + a1*sign(dt)*(1-(1+(abs(dt/u0))^x0)/(1+(abs(dt/u1))^x1))
                \"\"\",
                \"\"\"
                    a0 0       include lower_limit=-1   upper_limit=1
                    a1 6e-3    include lower_limit=1e-8 upper_limit=1
                    u0 2.3e-10 include lower_limit=1e-12
                    u1 2.3e-10 include lower_limit=1e-12
                    x0 1.05    include lower_limit=1
                    x1 1.05    include lower_limit=1
                \"\"\",
                meast_col="dicp",
                model_col="dicp_mod",
                error_col="residual",
                residual="relative",
                data=d
            )
            ftr.fit()
            print(ftr.par_values())
            DataViewm(data=d, command=[["dt residual"], ["dt dicp dicp_mod"]])

    **public methods**:

        * public methods from *ItclObjectx*

    """
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Fitter main
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, model_eqns, par_specs, **kwargs):
        ItclObjectx.__init__(self)
        #----------------------------------------------------------------------
        # private variables:
        #----------------------------------------------------------------------
        self.__parobj = None
        #----------------------------------------------------------------------
        # configuration options:
        #----------------------------------------------------------------------
        self._add_options({
            "data"       : [None,         None],
            "meast_col"  : ["",           None],
            "model_col"  : ["",           None],
            "error_col"  : ["",           None],
            "residual"   : ["relative",   None],
            "quiet"      : [False,        None],
        })
        #----------------------------------------------------------------------
        # keyword arguments are all configuration options
        #----------------------------------------------------------------------
        for key, value in list(kwargs.items()) :
            self[key] = value
        #----------------------------------------------------------------------
        # parameters
        #----------------------------------------------------------------------
        parobj_specs = []
        for line in decida.interpolate(par_specs, 2).split("\n") :
            line = line.strip()
            if line :
                items         = line.split()
                name          = items.pop(0)
                value         = float(items.pop(0))
                include       = False
                lower_limited = False
                lower_limit   = 0.0
                upper_limited = False
                upper_limit   = 0.0
                for item in items :
                    if item == "include" :
                        include = True
                    elif re.search("^lower_limit", item) :
                        var, val = item.split("=")
                        lower_limited=True
                        lower_limit = float(val)
                    elif re.search("^upper_limit", item) :
                        var, val = item.split("=")
                        upper_limited=True
                        upper_limit = float(val)
                parobj_specs.append([name, value, include, lower_limited, upper_limited, lower_limit, upper_limit])
        self.__parobj = Parameters(specs=parobj_specs)
        self.__model_eqns = decida.interpolate(model_eqns, 2)
        self.__optobj = None
    #----------------------------------------------------------------------
    # optimization function
    #----------------------------------------------------------------------
    def model_function(self, parobj, datobj):
        error_col = self["error_col"]
        meast_col = self["meast_col"]
        model_col = self["model_col"]
        model_eqns = self.__model_eqns
        for par in parobj.pars() :
            value = parobj[par]
            datobj.set("$par = $value")
        for eqn in model_eqns.split("\n") :
            eqn=eqn.strip()
            if eqn :
                datobj.set(eqn)
        datobj.set("$error_col = $model_col - $meast_col")
        if self["residual"] == "relative" :
            datobj.set("$error_col = $error_col / (1e-18 + abs($meast_col))")
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Fitter user commands
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD: fit
    # PURPOSE: fit data
    #==========================================================================
    def fit(self) :
        """ fit the meast_col data to model equations.

        **results**:

            * A LevMar instance is created and used to fit the meast_col
              data to the specified model equations.

        """
        self.__optobj = LevMar(
            self.model_function,
            self.__parobj,
            self["data"],
            meast_col=self["meast_col"],
            model_col=self["model_col"],
            error_col=self["error_col"],
            quiet=self["quiet"],
            debug=False
        )
        self.__optobj.fit()
    #==========================================================================
    # METHOD: par_object
    # PURPOSE: return parameter object handle
    #==========================================================================
    def par_object(self) :
        return self.__parobj
    #==========================================================================
    # METHOD: par_reset
    # PURPOSE: reset parameter values to initial values
    #==========================================================================
    def par_reset(self) :
        """ reset parameter values to initial values

        **results**:

            * parameters are set to initial values

        """
        self.__parobj.reset()
    #==========================================================================
    # METHOD: par_values
    # PURPOSE: return parameter values
    #==========================================================================
    def par_values(self) :
        """ return the current model parameter values.

        **results**:

            * A list of the values of the parameters is returned.  The
              parameter values are in the same order as they were specified.

        """
        return list(self.__parobj.values())
    #==========================================================================
    # METHOD: par_name_values
    # PURPOSE: return array of parameter name, value
    #==========================================================================
    def par_name_values(self) :
        """ return array of parameter name, value

        **results**:

            * An array of the values of the parameters is returned.

        """
        pars = self.__parobj.pars()
        vals = list(self.__parobj.values())
        return_array = {}
        for par, val in zip(pars, vals) :
            return_array[par] = val
        return return_array
