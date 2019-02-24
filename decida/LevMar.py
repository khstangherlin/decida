################################################################################
# CLASS    : LevMar
# PURPOSE  : Levenberg-Marquardt linear least-squares
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:21:32 2013
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
from builtins import str
from builtins import range
from builtins import object
import math
import numpy
import six
from decida.ItclObjectx import ItclObjectx

class LevMar(ItclObjectx) :
    """
    **synopsis**:

        Levenberg-Marquardt linear least-squares minimization.

        *LevMar* performs linear least-squares minimization.
        It is used to fit a specified model equation set to data, by adjusting
        parameter values in the equation set.  *LevMar* uses the *Parameters*
        class to manage the parameter set.

        *LevMar* is adapted from the *mpfit* module, which is based on
        MINPACK-1.  The document strings from *mpfit*, and the MINPACK-1
        source-code are referenced at the bottom of this page.
        These are more detailed than the documentation shown here.

        *LevMar* is still under development.

        The *Fitter* class is a wrapper around *LevMar*, which makes its use
        somewhat easier.

    **constructor arguments**:

        **function** (function)

            A function which includes the model to fit.
            The required arguments to function are a *Parameters* object
            and a *Data* object.  Each used parameter current value
            is available by indexing the *Parameters* object by the parameter
            name.  The *Data* object must contain a column with the
            data points to be fit: the data column is specified by the
            "meast_col" configuration option to *LevMar*.  The function
            generates a model column and an error column.

        **parobj** (Parameters object handle)

            The *Parameters* object which manages the parameter values.

        **dataobj** (Data object handle)

            The *Data* object which manages the measurement, model, and error
            values.

        **\*\*kwargs** (dict)

            keyword=value specifications:
            configuration-options

    **configuration options**:

        **debug** (bool, default=False)

           enable debug mode, which prints out more information
           during minimization.

        **quiet** (bool, default=False)

           disable printing of information during minimization.

        **meast_col** (str, default="")

           The data column which contains the data to be fitted.

        **model_col** (str, default="")

           The data column which is to be created to fit the meast_col data.

        **error_col** (str, default="")

           The relative or absolute error between the model_col
           and meast_col data.

        **ftol** (float, default=1e_10)

           Relative sum-of-squares error tolerance for convergence.

        **xtol** (float, default=1e_10)

           Relative approximate solution error tolerance for convergence.

        **gtol** (float, default=1e_10)

           Minimum value of the gradient norm:
           measure of the orthogonality between parameter
           Jacobian and function for convergence.

        **maxiter** (int, default=200)

           Maximum number of Levenberg-Marquardt iterations.

        **factor** (float, default=100.0)

           Parameter-step scaling factor.

        **damp** (float, default=0.0)

           Parameter-step damping factor.

        **nprint** (int, default=1)

           Number of iterations to skip before printing information.

        **iterfunct** (function, default=None)

           Specify a different iteration function to print values of the
           parameters at each Levenberg-Marquart iteration.
           The required parameters of the iteration function are:

               **parobj**

                   The *Parameters* object handle.

               **iter**

                   The iteration number.

               **fnorm2**

                   The current sum-of-squares norm.

           Other parameters are passed as keyword=value pairs, specified in
           the iterkw configuration option.

        **iterkw** (dict, default={})

           Keyword options for the user-defined iteration function.

        **nocovar** (bool, default=False)

           Disable covarianace calculation (if performed in user function).

        **fastnorm** (bool, default=False)

           Use a faster calculation of error norma.

        **rescale** (bool, default=False)

           Use the tuple specified in the diag configuration option
           to rescale.

        **autoderiv** (bool, default=True)

           If True, compute Jacobian numerically.

        **diag** (tuple, default=None)

           Set of values to rescale error.

        **epsfcn** (float, default=None)

           Used to determine numerical derivative step.

    **example** (from test_LevMar): ::

        from decida.LevMar import LevMar
        from decida.Parameters import Parameters
        from decida.Data import Data

        def lcfunc(parobj, dataobj):
            L  = parobj["L"]
            Co = parobj["Co"]
            Cu = parobj["Cu"]
            C1 = parobj["C1"]
            C2 = parobj["C2"]
            a2 = C2*16.0
            c2 = (C2-C1)*8.0
            b2 = (C2-C1)*24.0
            dataobj.set("Cc = (floor(vc/4.0)+fmod(vc,4)*0.25)*$Cu")
            dataobj.set("Cf = $a2 - $b2*vf + $c2*vf^2")
            dataobj.set("Ct = $Co + Cc + Cf")
            dataobj.set("fhat = 1.0/(2*pi*sqrt($L*Ct))")
            dataobj.set("residual = fhat - freq")

        parobj = Parameters(specs=(
           ("L" , 2400e-12, False,  True, False, 0.0, 0.0),
           ("Co",  250e-15,  True,  True, False, 0.0, 0.0),
           ("Cu",   60e-15,  True,  True, False, 0.0, 0.0),
           ("C1",   23e-15,  True,  True, False, 0.0, 0.0),
           ("C2",   27e-15,  True,  True, False, 0.0, 0.0),
        ))

        dataobj = Data()
        dataobj.read("lcdata.col")

        optobj = LevMar(lcfunc, parobj, dataobj,
            meast_col="freq", model_col="fhat", error_col="residual",
            quiet=False, debug=False
        )
        optobj.fit()
        print(optobj.status())
        print("parameters = ", parobj.values())

    **public methods**:

        * public methods from *ItclObjectx*

    """
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # LevMar main
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, function, parobj, dataobj, **kwargs) :
        ItclObjectx.__init__(self)
        #---------------------------------------------------------------------
        # private variables:
        #---------------------------------------------------------------------
        self.__function   = function         # a user-supplied function
        self.__parobj     = parobj           # a Parameters object
        self.__dataobj    = dataobj          # a Data object
        self.__diag       = None             # diag keyword
        self.__iterfunct  = self._defiter    # printout at each iteration
        self.__machar     = Machar(double=1) # machine characteristic numbers
        self.__status     = 0                # negative values = error
        self.__covar      = None             #
        self.__perror     = None             #
        self.__nfev       = 0                # number of function evaluations
        #---------------------------------------------------------------------
        # configuration options:
        # meast, model, error columns checked in call
        #---------------------------------------------------------------------
        self._add_options({
            "debug"      : [False, None],
            "quiet"      : [False, None],
            "meast_col"  : ["",      self._config_meast_col_callback],
            "model_col"  : ["",      self._config_model_col_callback],
            "error_col"  : ["",      self._config_error_col_callback],
            "ftol"       : [1.0e-10, self._config_ftol_callback],
            "xtol"       : [1.0e-10, self._config_xtol_callback],
            "gtol"       : [1.0e-10, self._config_gtol_callback],
            "maxiter"    : [200,     self._config_maxiter_callback],
            "factor"     : [100.0,   self._config_factor_callback],
            "damp"       : [0.0,   None],
            "nprint"     : [1,     None],
            "iterfunct"  : [None,    self._config_iterfunct_callback],
            "iterkw"     : [{},    None],
            "nocovar"    : [False, None],
            "fastnorm"   : [False, None],
            "rescale"    : [False, None],
            "autoderiv"  : [True,  None],
            "diag"       : [None,    self._config_diag_callback],
            "epsfcn"     : [None,  None],
        })
        #----------------------------------------------------------------------
        # keyword arguments are all configuration options
        #----------------------------------------------------------------------
        for key, value in list(kwargs.items()) :
            self[key] = value
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # LevMar configuration option callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _config_meast_col_callback
    # PURPOSE : configure meast_col
    #==========================================================================
    def _config_meast_col_callback(self) :
        meast_col = self["meast_col"]
    #==========================================================================
    # METHOD  : _config_model_col_callback
    # PURPOSE : configure model_col
    #==========================================================================
    def _config_model_col_callback(self) :
        model_col = self["model_col"]
    #==========================================================================
    # METHOD  : _config_error_col_callback
    # PURPOSE : configure error_col
    #==========================================================================
    def _config_error_col_callback(self) :
        error_col = self["error_col"]
    #==========================================================================
    # METHOD  : _config_ftol_callback
    # PURPOSE : configure ftol
    #==========================================================================
    def _config_ftol_callback(self) :
        ftol = self["ftol"]
        if ftol <= 0.0 :
            self.__status = -1
            self.error("ftol must be > 0.0")
            return False
        return True
    #==========================================================================
    # METHOD  : _config_xtol_callback
    # PURPOSE : configure xtol
    #==========================================================================
    def _config_xtol_callback(self) :
        xtol = self["xtol"]
        if xtol <= 0.0 :
            self.__status = -1
            self.error("xtol must be > 0.0")
            return False
        return True
    #==========================================================================
    # METHOD  : _config_gtol_callback
    # PURPOSE : configure gtol
    #==========================================================================
    def _config_gtol_callback(self) :
        gtol = self["gtol"]
        if gtol <= 0.0 :
            self.__status = -1
            self.error("gtol must be > 0.0")
            return False
        return True
    #==========================================================================
    # METHOD  : _config_maxiter_callback
    # PURPOSE : configure maxiter
    #==========================================================================
    def _config_maxiter_callback(self) :
        maxiter = self["maxiter"]
        if maxiter <= 0.0 :
            self.__status = -1
            self.error("maxiter must be > 0")
            return False
        return True
    #==========================================================================
    # METHOD  : _config_factor_callback
    # PURPOSE : configure factor
    #==========================================================================
    def _config_factor_callback(self) :
        factor = self["factor"]
        if factor <= 0.0 :
            self.__status = -1
            self.error("factor must be > 0.0")
            return False
        return True
    #==========================================================================
    # METHOD  : _config_diag_callback
    # PURPOSE : configure diag
    #==========================================================================
    def _config_diag_callback(self) :
        diag = self["diag"]
        self.__diag = diag
    #==========================================================================
    # METHOD  : _config_iterfunct_callback
    # PURPOSE : configure iterfunct
    #==========================================================================
    def _config_iterfunct_callback(self) :
        func = self["iterfunct"]
        if isinstance(func, six.string_types) and func == "default" :
            self.__iterfunct = self._defiter
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # LevMar user commands
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : status
    # PURPOSE : return optimizer status
    #==========================================================================
    def status(self) :
        """ return optimizer status.

        **results**:

            * Returns the optimizer status message.

        """
        return self.__status
    #==========================================================================
    # METHOD  : fit
    # PURPOSE : fit model to data
    #==========================================================================
    def fit(self) :
        """ fit model to data.

        **results**:

            * Fits model to specified data.

        """
        #----------------------------------------------------------------------
        # init fit
        #----------------------------------------------------------------------
        machep = self.__machar.machep  # machine precision
        self.__covar  = None           #
        self.__perror = None           #
        self.__nfev   = 0              # number of function evaluations
        #----------------------------------------------------------------------
        # check parameter limits
        #----------------------------------------------------------------------
        if not self.__parobj.check_within_limits() :
            self.__status = -1
            self.error("parameters are not within specified limits")
        if not self.__parobj.check_correct_limits() :
            self.__status = -1
            self.error("specified parameter limits are not consistent")
        #----------------------------
        # free/fixed/tied
        # NOTES:
        #   * all_par_vals = xall
        #   * free_par_vals = x
        #----------------------------
        all_par_vals  = numpy.asarray(list(self.__parobj.values()), float)
        free_par_vals = numpy.asarray(self.__parobj.free_values(), float)
        free_par_inds = numpy.asarray(self.__parobj.free_indices(), int)
        free_pars     = self.__parobj.free_pars()

        if len(free_pars) == 0:
            self.__status = -1
            self.error("no free parameters")
        #----------------------------------------------------------------------
        # (rescale) diag check
        #----------------------------------------------------------------------
        if self["rescale"]:
            if (len(self.__diag) < len(free_pars)):
                self.__status = -1
                self.error("diag length is less than number of free parameters")
            wh = (numpy.nonzero(self.__diag <= 0))[0]
            if (len(wh) > 0):
                self.__status = -1
                self.error("some diag values are <= 0.0")
        #---------------------------------------------------------------
        # first call to user function
        # parobj.values(*) only to force tied parameters to get tied
        # probably should have parobj.reset() instead
        #---------------------------------------------------------------
        all_par_vals = numpy.asarray(self.__parobj.values(all_par_vals), float)
        fvec = self._call()
        if (self.__status < 0):
            self.error("first call to user function failed")

        n   = len(free_pars)  # number of free parameters
        m   = len(fvec)       # number of data points
        dof = m - n           # degrees of freedom (0 ok?)

        if (m < n):
            if self["debug"]:
                print("number of parameters = ", n)
                print("number of datapoints = ", m)
            self.__status = -1
            self.error("number of parameters must not exceed data")

        fnorm = self._enorm(fvec)
        #---------------------------------------------------------------
        # Initialize Levenberg-Marquardt parameter and iteration counter
        #---------------------------------------------------------------
        if self["debug"] :
            print("initializing Levenberg-Marquardt")
        self.__status  = 0
        lmpar          = 0.
        niter          = 1
        qtf            = free_par_vals * 0.
        fnorm1         = -1.0
        #======================================================================
        # outer loop
        #======================================================================
        while(True):
            #------------------------------------------------------------------
            # put free par values back into pars
            # setting parobj also deals with tied parameters
            #------------------------------------------------------------------
            free_par_vals = numpy.asarray(self.__parobj.free_values(free_par_vals))
            all_par_vals  = numpy.asarray(list(self.__parobj.values()), float)
            #------------------------------------------------------------------
            # call iteration function
            #------------------------------------------------------------------
            if ((self["nprint"] > 0) and (self.__iterfunct is not None) and
                ((niter-1) % self["nprint"]) == 0
            ) :
                mperr = 0
                status = self.__iterfunct(
                    self.__parobj,
                    niter,
                    fnorm**2,
                    quiet=self["quiet"],
                    dof=dof,
                    **self["iterkw"]
                )
                if (status is not None):
                    self.__status = status
                #-----------------------------------
                # Check for user termination
                #-----------------------------------
                if (self.__status < 0):
                    self.error("premature termination by user function")
            #-----------------------------------
            # Calculate the jacobian matrix
            #-----------------------------------
            self.__status = 2
            fjac = self._fdjac2(fvec)
            if (fjac is None):
                self.warning("premature termination by FDJAC2")
                return
            #------------------------------------------------------------------
            # Determine if any of the parameters are pegged at the limits
            # See if any "pegged" values should keep their derivatives
            #------------------------------------------------------------------
            if self["debug"] :
                print("zeroing derivatives of pegged parameters")
            for i, _par in enumerate(free_pars):
                if self.__parobj.check(_par, "at_lower_limit"):
                    sum0 = sum(fvec * fjac[:,i])
                    if (sum0 > 0) :
                        fjac[:,i] = 0.0
                if self.__parobj.check(_par, "at_upper_limit"):
                    sum0 = sum(fvec * fjac[:,i])
                    if (sum0 < 0) :
                        fjac[:,i] = 0.0
            #------------------------------------------------------------------
            # Compute the QR factorization of the jacobian
            #------------------------------------------------------------------
            [fjac, ipvt, wa1, wa2] = self._qrfac(fjac, pivot=1)
            #------------------------------------------------------------------
            # On the first iteration if "diag" is unspecified, scale
            # according to the norms of the columns of the initial jacobian
            # if not rescaling by user-supplied diag:
            #   diag = wa2 copy
            # wa3 = scaled parameters diag*free_par_vals
            #------------------------------------------------------------------
            if self["debug"] :
                print("rescaling diagonal elements")
            if (niter == 1):
                if ((not self["rescale"]) or (len(self.__diag) < n)):
                    self.__diag = wa2.copy()
                    wh = (numpy.nonzero(self.__diag == 0))[0]
                    numpy.put(self.__diag, wh, 1.)
                ## On first iteration, calculate the norm of the scaled free_pars
                ## and initialize the step bound delta
                wa3 = self.__diag * free_par_vals
                xnorm = self._enorm(wa3)
                delta = self["factor"]*xnorm
                if (delta == 0.0) :
                    delta = self["factor"]
            #------------------------------------------------------------------
            # Form (q transpose)*fvec and store the first n components in qtf
            #------------------------------------------------------------------
            if self["debug"] :
                print("forming (q transpose)*fvec")
            wa4 = fvec.copy()
            for j in range(n):
                lj = ipvt[j]
                temp3 = fjac[j,lj]
                if (temp3 != 0):
                    fj = fjac[j:,lj]
                    wj = wa4[j:]
                    ## *** optimization wa4(j:*)
                    wa4[j:] = wj - fj * sum(fj*wj) / temp3
                fjac[j,lj] = wa1[j]
                qtf[j] = wa4[j]
            #------------------------------------------------------------------
            # From this point on, only the square matrix, consisting of the
            # triangle of R, is needed.
            #------------------------------------------------------------------
            fjac = fjac[0:n, 0:n]
            fjac.shape = [n, n]
            temp = fjac.copy()
            for i in range(n):
                temp[:,i] = fjac[:, ipvt[i]]
            fjac = temp.copy()
            #------------------------------------------------------------------
            # Check for overflow.  This should be a cheap test here since FJAC
            # has been reduced to a (small) square matrix, and the test is
            # O(N^2).
            # wh = where(finite(fjac) EQ 0, ct)
            # if ct GT 0 then goto, FAIL_OVERFLOW
            #   Compute the norm of the scaled gradient
            #------------------------------------------------------------------
            if self["debug"] :
                print("computing the scaled gradient")
            gnorm = 0.
            if (fnorm != 0):
                for j in range(n):
                    l = ipvt[j]
                    if (wa2[l] != 0):
                        sum0 = sum(fjac[0:j+1,j]*qtf[0:j+1])/fnorm
                        gnorm = numpy.max([gnorm,abs(sum0/wa2[l])])
            #------------------------------------------------------------------
            # Test for convergence of the gradient norm
            #------------------------------------------------------------------
            if (gnorm <= self["gtol"]):
                self.__status = 4
                if self["debug"] :
                    print("gradient norm convergence")
                break
            if self["maxiter"] == 0:
                if self["debug"] :
                    print("maxiter = zero, stopping")
                break
            #------------------------------------------------------------------
            # Rescale if necessary
            #------------------------------------------------------------------
            if (not self["rescale"] == 0):
                self.__diag = numpy.choose(self.__diag>wa2, (wa2, self.__diag))
            #------------------------------------------------------------------
            # inner loop
            #------------------------------------------------------------------
            while(True):
                if self["debug"] :
                    print("Inner loop")
                #--------------------------------------------------------------
                # Determine the levenberg-marquardt parameter
                #--------------------------------------------------------------
                if self["debug"] :
                    print("calculating LM parameter (MPFIT_)")
                [fjac, lmpar, wa1, wa2] = self._lmpar(
                    fjac, ipvt, self.__diag, qtf,
                    delta, wa1, wa2, par=lmpar
                )
                #--------------------------------------------------------------
                # Store the direction p and x+p. Calculate the norm of p
                #--------------------------------------------------------------
                wa1 = -wa1
                alpha = 1.0
                if ((not self.__parobj.check_any_free_limited()) and
                    (not self.__parobj.check_any_free_step_limited())
                ) :
                    wa2 = free_par_vals + wa1
                else:
                    #----------------------------------------------------------
                    # Respect the limits.  If a step were to go out of bounds,
                    # then we should take a step in the same direction but
                    # shorter distance. The step should take us right to the
                    # limit in that case.
                    #----------------------------------------------------------
                    if self["debug"] :
                        print("checking for a step out of bounds")
                    steps = []
                    for step, _par in zip(wa1, free_pars):
                        if   self.__parobj.check(_par, "at_lower_limit"):
                            steps.append(max(0.0, step))
                        elif self.__parobj.check(_par, "at_upper_limit"):
                            steps.append(min(0.0, step))
                        else :
                            steps.append(step)
                    for step, _par in zip(steps, free_pars):
                        if self.__parobj.check(_par, "lower_limited"):
                            val = self.__parobj[_par]
                            lim = self.__parobj.check(_par, "lower_limit")
                            if step < -machep :
                                alpha = min(alpha, (lim-val)/step)
                        elif self.__parobj.check(_par, "upper_limited"):
                            val = self.__parobj[_par]
                            lim = self.__parobj.check(_par, "upper_limit")
                            if step > machep :
                                alpha = min(alpha, (lim-val)/step)
                    for step, _par in zip(steps, free_pars):
                        _maxstep = self.__parobj.check(_par, "maxstep")
                        if _maxstep > 0.0 and abs(step) > machep :
                            alpha = min(alpha, _maxstep/abs(step))
                    wa1 = numpy.asarray(steps, float) * alpha
                    wa2 = free_par_vals + wa1
                    #----------------------------------------------------------
                    ## Adjust the final output values.
                    ## If the step put us exactly on a boundary,
                    ## make sure it is exact.
                    #----------------------------------------------------------
                    vals = []
                    for val, _par in zip(wa2, free_pars):
                        _llimited = self.__parobj.check(_par, "lower_limited")
                        _llimit   = self.__parobj.check(_par, "lower_limit")
                        _ulimited = self.__parobj.check(_par, "upper_limited")
                        _ulimit   = self.__parobj.check(_par, "upper_limit")
                        if   _llimited and val <= _llimit*(1+machep) :
                            vals.append(_llimit)
                        elif _ulimited and val >= _ulimit*(1-machep) :
                            vals.append(_ulimit)
                        else :
                            vals.append(val)
                    wa2 = numpy.asarray(vals)
                #--------------------------------------------------------------
                # endelse (limits)
                #--------------------------------------------------------------
                wa3 = self.__diag * wa1
                pnorm = self._enorm(wa3)
                #--------------------------------------------------------------
                # On the first iteration, adjust the initial step bound
                #--------------------------------------------------------------
                if (niter == 1):
                    delta = numpy.min([delta,pnorm])
                #--------------------------------------------------------------
                # put updated free parameters back in params
                #--------------------------------------------------------------
                numpy.put(all_par_vals, free_par_inds, wa2)
                #--------------------------------------------------------------
                # Evaluate the function at x+p and calculate its norm
                #--------------------------------------------------------------
                mperr = 0
                if self["debug"] :
                    print("calling ", str(self.__function))
                #--------------------------------------------------------------
                # put parameters back into parobj
                #--------------------------------------------------------------
                all_par_vals = numpy.asarray(self.__parobj.values(all_par_vals), float)
                wa4 = self._call()
                if (self.__status < 0):
                    self.error("premature termination by user function")
                fnorm1 = self._enorm(wa4)
                #--------------------------------------------------------------
                # Compute the scaled actual reduction
                #--------------------------------------------------------------
                if self["debug"] :
                    print("computing convergence criteria")
                actred = -1.
                if ((0.1 * fnorm1) < fnorm) :
                    actred = - (fnorm1/fnorm)**2 + 1.
                #--------------------------------------------------------------
                # Compute the scaled predicted reduction and the scaled
                # directional derivative
                #--------------------------------------------------------------
                for j in range(n):
                    wa3[j] = 0
                    wa3[0:j+1] = wa3[0:j+1] + fjac[0:j+1,j]*wa1[ipvt[j]]
                #--------------------------------------------------------------
                # Remember, alpha is the fraction of the full LM step actually
                # taken
                #--------------------------------------------------------------
                temp1 = self._enorm(alpha*wa3)/fnorm
                temp2 = (math.sqrt(alpha*lmpar)*pnorm)/fnorm
                prered = temp1*temp1 + (temp2*temp2)/0.5
                dirder = -(temp1*temp1 + temp2*temp2)
                #--------------------------------------------------------------
                # Compute the ratio of the actual to the predicted reduction.
                #--------------------------------------------------------------
                ratio = 0.
                if (prered != 0) :
                    ratio = actred/prered
                #--------------------------------------------------------------
                # Update the step bound
                #--------------------------------------------------------------
                if (ratio <= 0.25):
                    if (actred >= 0) :
                        temp = .5
                    else :
                        temp = .5*dirder/(dirder + .5*actred)
                    if ((0.1*fnorm1) >= fnorm) or (temp < 0.1) :
                        temp = 0.1
                    delta = temp*numpy.min([delta,pnorm/0.1])
                    lmpar = lmpar/temp
                else:
                    if (lmpar == 0) or (ratio >= 0.75):
                        delta = pnorm/.5
                        lmpar = .5*lmpar
                #--------------------------------------------------------------
                # Test for successful iteration
                #--------------------------------------------------------------
                if (ratio >= 0.0001):
                    if self["debug"] :
                        print("Successful iteration.  Update free_pars, fvec, and their norms")
                    free_par_vals = wa2
                    wa2 = self.__diag * free_par_vals

                    fvec = wa4
                    xnorm = self._enorm(wa2)
                    fnorm = fnorm1
                    niter = niter + 1
                #--------------------------------------------------------------
                # Tests for convergence
                #--------------------------------------------------------------
                if ((abs(actred) <= self["ftol"]) and (prered <= self["ftol"])
                     and (0.5 * ratio <= 1)):
                    self.__status = 1
                    if self["debug"] :
                        print("Convergence test 1")
                if delta <= self["xtol"]*xnorm:
                    self.__status = 2
                    if self["debug"] :
                        print("Convergence test 2")
                if ((abs(actred) <= self["ftol"]) and (prered <= self["ftol"])
                    and (0.5 * ratio <= 1) and (self.__status == 2)):
                    self.__status = 3
                    if self["debug"] :
                        print("Convergence test 3")
                if (self.__status != 0):
                    break
                #--------------------------------------------------------------
                # Tests for termination and stringent tolerances
                #--------------------------------------------------------------
                if (niter >= self["maxiter"]):
                    self.__status = 5
                    if self["debug"] :
                        print("Termination test 5")
                if ((abs(actred) <= machep) and (prered <= machep)
                    and (0.5*ratio <= 1)):
                    self.__status = 6
                    if self["debug"] :
                        print("Termination test 6")
                if delta <= machep*xnorm:
                    self.__status = 7
                    if self["debug"] :
                        print("Termination test 7")
                if gnorm <= machep:
                    self.__status = 8
                    if self["debug"] :
                        print("Termination test 8")
                if (self.__status != 0):
                    break
                #--------------------------------------------------------------
                # End of inner loop. Repeat if iteration unsuccessful
                #--------------------------------------------------------------
                if (ratio >= 0.0001):
                    if self["debug"] :
                        print("ratio > 1e-4, breaking inner loop")
                    break
                #--------------------------------------------------------------
                # Check for over/underflow
                #--------------------------------------------------------------
                if ~numpy.all(numpy.isfinite(wa1) & numpy.isfinite(wa2) &
                            numpy.isfinite(free_par_vals)) or ~numpy.isfinite(ratio):
                    self.__status = -16
                    self.error(
                        "parameter or function value(s) have become infinite.",
                        " check model function for over- or under-flow"
                    )
                    break
            #--------------------------------------------------------------
            # End of inner loop
            #--------------------------------------------------------------
            if (self.__status != 0):
                if not self["quiet"]:
                    self.message("END OF INNER LOOP, status = %s" % (self.__status))
                break
        #--------------------------------------------------------------
        # End of outer loop.
        #--------------------------------------------------------------
        if self["debug"] :
            print("in the termination phase")
        #--------------------------------------------------------------
        # Termination, either normal or user imposed.
        #--------------------------------------------------------------
        if (len(all_par_vals) == 0):
            return
        if (len(free_par_inds)  == 0):
            all_par_vals = self.__parobj.copy()
        else:
            numpy.put(all_par_vals, free_par_inds, free_par_vals)
        if (self["nprint"] > 0) and (self.__status > 0):
            if self["debug"] :
                print("calling ", str(self.__function))
            all_par_vals = numpy.asarray(self.__parobj.values(all_par_vals), float)
            fvec = self._call()
            if self["debug"] :
                print("in the termination phase")
            fnorm = self._enorm(fvec)

        if ((fnorm is not None) and (fnorm1 is not None)):
            fnorm = numpy.max([fnorm, fnorm1])
            fnorm = fnorm**2.

        self.__covar = None
        self.__perror = None
        #--------------------------------------------------------------
        # (very carefully) set the covariance matrix COVAR
        #--------------------------------------------------------------
        if ((self.__status > 0) and (self["nocovar"]==0) and (n is not None)
                       and (fjac is not None) and (ipvt is not None)):
            sz = numpy.shape(fjac)
            if ((n > 0) and (sz[0] >= n) and (sz[1] >= n)
                and (len(ipvt) >= n)):

                if self["debug"] :
                    print("computing the covariance matrix")
                cv = self._calc_covar(fjac[0:n,0:n], ipvt[0:n])
                cv.shape = [n, n]
                nn = len(self.__parobj)

                ## Fill in actual covariance matrix, accounting for fixed
                ## parameters.
                self.__covar = numpy.zeros([nn, nn], dtype=float)
                for i in range(n):
                    self.__covar[free_par_inds, free_par_inds[i]] = cv[:,i]

                ## Compute errors in parameters
                if self["debug"] :
                    print("computing parameter errors")
                self.__perror = numpy.zeros(nn, dtype=float)
                d = numpy.diagonal(self.__covar)
                wh = (numpy.nonzero(d >= 0))[0]
                if len(wh) > 0:
                    numpy.put(self.__perror, wh, numpy.sqrt(numpy.take(d, wh)))
            if not self["quiet"]:
                print("END OF OUTER LOOP, status = %s" % (self.__status))
            all_par_vals = numpy.asarray(self.__parobj.values(all_par_vals), float)
        return
    #==========================================================================
    # METHOD  : _defiter
    # PURPOSE : default procedure to be called every iteration.
    #     It simply prints the parameter values.
    #==========================================================================
    def _defiter(self, parobj, iiter,
        fnorm2, quiet=False, pformat="%.10g", dof=1
    ) :
        if self["debug"] :
            print('Entering _defiter...')
        if (quiet):
            return None
        print("iter %6i   chi-square = %.10g  dof = %d" % (iiter, fnorm2, dof))
        fmt = "    %%-10s : P[%%d] = %s"  % (pformat)
        for i, par in enumerate(parobj.pars()) :
            if parobj.check(par, "print") and parobj.check(par, "free") :
                print(fmt % (par, i, parobj[par]))
        status = 0
        return status
    #==========================================================================
    # METHOD  : _call
    # PURPOSE : Call user function or procedure, with _EXTRA or not,
    #     with derivatives or not.
    # NOTES :
    #   * Apply damping if requested.  This replaces the residuals
    #     with their hyperbolic tangent.  Thus residuals larger than
    #     DAMP are essentially clipped.
    #==========================================================================
    def _call(self, fjac=None):
        self.__nfev += 1
        self.__function(self.__parobj, self.__dataobj)
        meast_col = self["meast_col"]
        model_col = self["model_col"]
        error_col = self["error_col"]
        if not meast_col in self.__dataobj.names() :
            self.error("meast_col \"%s\" is not in data object" % (meast_col))
            self.__status = -1
            return None
        if not model_col in self.__dataobj.names() :
            self.error("model_col \"%s\" is not in data object" % (model_col))
            self.__status = -1
            return None
        meast_array = numpy.asarray(self.__dataobj.get(meast_col), float)
        model_array = numpy.asarray(self.__dataobj.get(model_col), float)
        error_array = meast_array - model_array
        status = 0
        if (fjac is None) and (self["damp"] > 0) :
            error_array = numpy.tanh(error_array/self["damp"])
        # tbd:
        # self.__dataobj.col_set(self["error_col"], error_array)
        self.__dataobj.set("%s = 0.0" % (error_col))
        for i in range(len(error_array)) :
            self.__dataobj.set_entry(i, error_col, error_array[i])
        self.__status = 0
        return error_array
    #==========================================================================
    # METHOD  : _enorm
    # PURPOSE : normalization
    # NOTES :
    #   *  It turns out that, for systems that have a lot of data
    #      points, this routine is a big computing bottleneck.  The extended
    #      computations that need to be done cannot be effectively
    #      vectorized.  The introduction of the FASTNORM configuration
    #      parameter allows the user to select a faster routine, which is
    #      based on TOTAL() alone.
    #==========================================================================
    def _enorm(self, vec):
        if self["debug"] :
            print('Entering _enorm...')
        #----------------------------------
        # Very simple-minded sum-of-squares
        #----------------------------------
        if (self["fastnorm"]):
            ans = math.sqrt(sum(vec*vec))
        else:
            agiant = self.__machar.rgiant / len(vec)
            adwarf = self.__machar.rdwarf * len(vec)
            #-------------------------------------------------------------------
            # This is hopefully a compromise between speed and robustness.
            # Need to do this because of the possibility of over- or underflow.
            #-------------------------------------------------------------------
            mx = numpy.max(vec)
            mn = numpy.min(vec)
            mx = max([abs(mx), abs(mn)])
            if mx == 0:
                return(vec[0]*0.)
            if mx > agiant or mx < adwarf:
                ans = mx * math.sqrt(sum((vec/mx)*(vec/mx)))
            else:
                ans = math.sqrt(sum(vec*vec))
        if self["debug"] :
            print("norm = ", ans)
        return(ans)
    #==========================================================================
    # METHOD  : _fdjac2
    # PURPOSE :
    #==========================================================================
    def _fdjac2(self, fvec):
        if self["debug"] :
            print('Entering _fdjac2...')
        m    = len(fvec)
        #&&&&&&&&&&&&&&&&&&&&&&&&&&
        # tbd get these from parobj
        #&&&&&&&&&&&&&&&&&&&&&&&&&&
        all_par_vals  = numpy.asarray(list(self.__parobj.values()), float)
        free_par_vals = numpy.asarray(self.__parobj.free_values(), float)
        free_par_inds = numpy.asarray(self.__parobj.free_indices(), int)

        nall = len(all_par_vals)
        n    = len(free_par_vals)
        machep = self.__machar.machep  # machine precision
        #------------------------------
        # Compute analytical derivative
        # probably needs work
        #------------------------------
        if (not self["autoderiv"]):
            #------------------------------------------
            # specify parameters which need derivatives
            #------------------------------------------
            fjac = numpy.zeros(nall, dtype=float)
            numpy.put(fjac, free_par_inds, 1.0)
            fp = self._call(fjac=fjac)
            if len(fp) != m*nall:
                print('ERROR: Derivative matrix was not computed properly.')
                return(None)
            fp.shape = [m, nall]
            fp = -fp
            #------------------------------------------
            # select only the free parameters
            #------------------------------------------
            if len(free_par_inds) < nall:
                fp = fp[:,free_par_inds]
                fp.shape = [m, n]
                return(fp)
        #-------------------------------------
        # Compute finite-difference derivative
        #-------------------------------------
        ####eps = math.sqrt(numpy.max([self["epsfcn"], machep]))
        eps = math.sqrt(machep)
        fjac = numpy.zeros([m, n], dtype=float)
        h = eps * abs(free_par_vals)
        #-------------------------------------
        # use absolute steps specified > 0
        #-------------------------------------
        a_step  = numpy.asarray(self.__parobj.list_of_attr("step"), float)
        a_stepi = numpy.take(a_step, free_par_inds)
        wh      = (numpy.nonzero(a_stepi > 0.0))[0]
        a_eps   = numpy.take(a_stepi, wh)
        numpy.put(h, wh, a_eps)
        #-------------------------------------
        # use relative steps specified > 0
        #-------------------------------------
        r_step  = numpy.asarray(self.__parobj.list_of_attr("relative_step"), float)
        r_stepi = numpy.take(r_step, free_par_inds)
        wh      = (numpy.nonzero(r_stepi > 0.0))[0]
        r_eps   = abs(numpy.take(r_stepi, wh) * numpy.take(free_par_vals,wh))
        numpy.put(h, wh, r_eps)
        #-------------------------------------
        # in case any of the step values are zero
        #-------------------------------------
        wh = (numpy.nonzero(h == 0.0))[0]
        numpy.put(h, wh, eps)
        #-------------------------------------
        # Loop through parameters, computing the derivative for each
        # use appropriate difference if at a parameter limit
        #        0 - one-sided derivative computed automatically
        #        1 - one-sided derivative (f(x+h) - f(x)  )/h
        #       -1 - one-sided derivative (f(x)   - f(x-h))/h
        #        2 - two-sided derivative (f(x+h) - f(x-h))/(2*h)
        #----------------------------------------------------------------------
        lower_limited = numpy.asarray(self.__parobj.list_of_attr("lower_limited"), bool)
        upper_limited = numpy.asarray(self.__parobj.list_of_attr("upper_limited"), bool)
        lower_limit   = numpy.asarray(self.__parobj.list_of_attr("lower_limit"), float)
        upper_limit   = numpy.asarray(self.__parobj.list_of_attr("upper_limit"), float)
        side          = numpy.asarray(self.__parobj.list_of_attr("side"), int)
        paro = all_par_vals.copy()
        for j, k in enumerate(free_par_inds) :
            ho = h[j]
            po = all_par_vals[k]
            sidek = side[k]
            if upper_limited[k] and (po + ho) > upper_limit[k] :
                sidek = -1
            if lower_limited[k] and (po - ho) < lower_limit[k] :
                sidek =  1
            if   (sidek == 1) or (sidek == 0) :
                paro[k] = po + ho
                paro = numpy.asarray(self.__parobj.values(paro), float)
                fp = self._call()
                if (self.__status < 0):
                    return(None)
                fjac[:,j] = (fp - fvec) / ho
            elif (sidek == -1) :
                paro[k] = po - ho
                paro = numpy.asarray(self.__parobj.values(paro), float)
                fm = self._call()
                if (self.__status < 0):
                    return(None)
                fjac[:,j] = (fvec - fm) / ho
            elif (sidek == 2) :
                paro[k] = po + ho
                paro = numpy.asarray(self.__parobj.values(paro), float)
                fp = self._call()
                if (self.__status < 0):
                    return(None)
                paro[k] = po - ho
                paro = numpy.asarray(self.__parobj.values(paro), float)
                fm = self._call()
                if (self.__status < 0):
                    return(None)
                fjac[:,j] = (fp - fm)/(2*ho)
            paro[k] = po
        return(fjac)
    #==========================================================================
    # METHOD  : _qrfac
    # PURPOSE : QR factorization of A(mxn)
    # ARGUMENTS :
    #   * a      : mxn matrix  (m datapoints, n parameters)
    #   * pivot  : pivot flag
    # RETURNS :
    #   * a      : R (right triangular matrix)
    #   * ipvt   :
    #   * rdiag  :
    #   * acnorm :
    #==========================================================================
    def _qrfac(self, a, pivot=0):
        if self["debug"] :
            print('Entering _qrfac...')
        machep = self.__machar.machep
        sz = numpy.shape(a)
        m = sz[0]
        n = sz[1]

        ## Compute the initial column norms and initialize arrays
        acnorm = numpy.zeros(n, dtype=float)
        for j in range(n):
            acnorm[j] = self._enorm(a[:,j])
        rdiag = acnorm.copy()
        wa = rdiag.copy()
        ipvt = numpy.arange(n)

        ## Reduce a to r with householder transformations
        minmn = numpy.min([m,n])
        for j in range(minmn):
            if (pivot != 0):
                ## Bring the column of largest norm into the pivot position
                rmax = numpy.max(rdiag[j:])
                kmax = (numpy.nonzero(rdiag[j:] == rmax))[0]
                ct = len(kmax)
                kmax = kmax + j
                if ct > 0:
                    kmax = kmax[0]

                    ## Exchange rows via the pivot only.  Avoid actually exchanging
                    ## the rows, in case there is lots of memory transfer.  The
                    ## exchange occurs later, within the body of MPFIT, after the
                    ## extraneous columns of the matrix have been shed.
                    if kmax != j:
                        temp = ipvt[j]
                        ipvt[j] = ipvt[kmax]
                        ipvt[kmax] = temp
                        rdiag[kmax] = rdiag[j]
                        wa[kmax] = wa[j]

            ## Compute the householder transformation to reduce the jth
            ## column of A to a multiple of the jth unit vector
            lj = ipvt[j]
            ajj = a[j:,lj]
            ajnorm = self._enorm(ajj)
            if ajnorm == 0 :
                break
            if a[j,j] < 0 :
                ajnorm = -ajnorm

            ajj = ajj / ajnorm
            ajj[0] = ajj[0] + 1
            ## *** Note optimization a(j:*,j)
            a[j:,lj] = ajj

            ## Apply the transformation to the remaining columns
            ## and update the norms

            ## NOTE to SELF: tried to optimize this by removing the loop,
            ## but it actually got slower.  Reverted to "for" loop to keep
            ## it simple.
            if (j+1 < n):
                for k in range(j+1, n):
                    lk = ipvt[k]
                    ajk = a[j:,lk]
                    ## *** Note optimization a(j:*,lk)
                    ## (corrected 20 Jul 2000)
                    if a[j,lj] != 0:
                        a[j:,lk] = ajk - ajj * sum(ajk*ajj)/a[j,lj]
                        if ((pivot != 0) and (rdiag[k] != 0)):
                            temp = a[j,lk]/rdiag[k]
                            rdiag[k] = rdiag[k] * math.sqrt(numpy.max([(1.-temp**2), 0.]))
                            temp = rdiag[k]/wa[k]
                            if ((0.05*temp*temp) <= machep):
                                rdiag[k] = self._enorm(a[j+1:,lk])
                                wa[k] = rdiag[k]
            rdiag[j] = -ajnorm
        return([a, ipvt, rdiag, acnorm])
    #==========================================================================
    # METHOD : _qrsolv
    # PURPOSE :
    # NOTES :
    #   * A = QR = [Q1 Q2] [R1]
    #                      [0 ]
    #     A  (mxn)
    #     Q  (mxm, unitary)
    #     R  (mxn)
    #     Q1 (mxn)
    #     Q2 (mx(m-n))
    #     R1 (nxn)
    #     0  ((m-n)xn)
    #   * r   : R1
    #   * qtb : Q1^T * b
    #   * x^ = R1^-1*(Q1^T*b)
    #==========================================================================
    def _qrsolv(self, r, ipvt, diag, qtb, sdiag):
        if self["debug"] :
            print('Entering _qrsolv...')
        sz = numpy.shape(r)
        m = sz[0]
        n = sz[1]

        ## copy r and (q transpose)*b to preserve input and initialize s.
        ## in particular, save the diagonal elements of r in x.

        for j in range(n):
            r[j:n,j] = r[j,j:n]
        x = numpy.diagonal(r)
        wa = qtb.copy()

        ## Eliminate the diagonal matrix d using a givens rotation
        for j in range(n):
            l = ipvt[j]
            if (diag[l] == 0) :
                break
            sdiag[j:] = 0
            sdiag[j] = diag[l]

            ## The transformations to eliminate the row of d modify only a
            ## single element of (q transpose)*b beyond the first n, which
            ## is initially zero.

            qtbpj = 0.
            for k in range(j,n):
                if (sdiag[k] == 0) :
                    break
                if (abs(r[k,k]) < abs(sdiag[k])):
                    cotan  = r[k,k]/sdiag[k]
                    sine   = 0.5/math.sqrt(.25 + .25*cotan*cotan)
                    cosine = sine*cotan
                else:
                    tang   = sdiag[k]/r[k,k]
                    cosine = 0.5/math.sqrt(.25 + .25*tang*tang)
                    sine   = cosine*tang

                ## Compute the modified diagonal element of r and the
                ## modified element of ((q transpose)*b,0).
                r[k,k] = cosine*r[k,k] + sine*sdiag[k]
                temp = cosine*wa[k] + sine*qtbpj
                qtbpj = -sine*wa[k] + cosine*qtbpj
                wa[k] = temp

                ## Accumulate the transformation in the row of s
                if (n > k+1):
                    temp = cosine*r[k+1:n,k] + sine*sdiag[k+1:n]
                    sdiag[k+1:n] = -sine*r[k+1:n,k] + cosine*sdiag[k+1:n]
                    r[k+1:n,k] = temp
            sdiag[j] = r[j,j]
            r[j,j] = x[j]

        ## Solve the triangular system for z.  If the system is singular
        ## then obtain a least squares solution
        nsing = n
        wh = (numpy.nonzero(sdiag == 0))[0]
        if (len(wh) > 0):
            nsing = wh[0]
            wa[nsing:] = 0

        if (nsing >= 1):
            wa[nsing-1] = wa[nsing-1]/sdiag[nsing-1] ## Degenerate case
            ## *** Reverse loop ***
            for j in range(nsing-2,-1,-1):
                sum0 = sum(r[j+1:nsing,j]*wa[j+1:nsing])
                wa[j] = (wa[j]-sum0)/sdiag[j]

        ## Permute the components of z back to components of x
        x.setflags(write=True)
        numpy.put(x, ipvt, wa)
        return(r, x, sdiag)
    #==========================================================================
    # METHOD : _lmpar
    # PURPOSE :
    #==========================================================================
    def _lmpar(self, r, ipvt, diag, qtb, delta, x, sdiag, par=None):
        if self["debug"] :
            print('Entering _lmpar...')
        dwarf = self.__machar.minnum
        sz = numpy.shape(r)
        m = sz[0]
        n = sz[1]

        ## Compute and store in x the gauss-newton direction.  If the
        ## jacobian is rank-deficient, obtain a least-squares solution
        nsing = n
        wa1 = qtb.copy()
        wh = (numpy.nonzero(numpy.diagonal(r) == 0))[0]
        if len(wh) > 0:
            nsing = wh[0]
            wa1[wh[0]:] = 0
        if nsing >= 1:
            ## *** Reverse loop ***
            for j in range(nsing-1,-1,-1):
                wa1[j] = wa1[j]/r[j,j]
                if (j-1 >= 0):
                    wa1[0:j] = wa1[0:j] - r[0:j,j]*wa1[j]

        ## Note: ipvt here is a permutation array
        numpy.put(x, ipvt, wa1)

        ## Initialize the iteration counter.  Evaluate the function at the
        ## origin, and test for acceptance of the gauss-newton direction
        iiter = 0
        wa2 = diag * x
        dxnorm = self._enorm(wa2)
        fp = dxnorm - delta
        if (fp <= 0.1*delta):
            return[r, 0., x, sdiag]

        ## If the jacobian is not rank deficient, the newton step provides a
        ## lower bound, parl, for the zero of the function.  Otherwise set
        ## this bound to zero.

        parl = 0.
        if nsing >= n:
            wa1 = numpy.take(diag, ipvt)*numpy.take(wa2, ipvt)/dxnorm
            wa1[0] = wa1[0] / r[0,0] ## Degenerate case
            for j in range(1,n):   ## Note "1" here, not zero
                sum0 = sum(r[0:j,j]*wa1[0:j])
                wa1[j] = (wa1[j] - sum0)/r[j,j]

            temp = self._enorm(wa1)
            parl = ((fp/delta)/temp)/temp

        ## Calculate an upper bound, paru, for the zero of the function
        for j in range(n):
            sum0 = sum(r[0:j+1,j]*qtb[0:j+1])
            wa1[j] = sum0/diag[ipvt[j]]
        gnorm = self._enorm(wa1)
        paru = gnorm/delta
        if paru == 0 :
            paru = dwarf/numpy.min([delta,0.1])

        ## If the input par lies outside of the interval (parl,paru), set
        ## par to the closer endpoint

        par = numpy.max([par,parl])
        par = numpy.min([par,paru])
        if par == 0 :
            par = gnorm/dxnorm

        ## Beginning of an interation
        while(1):
            iiter = iiter + 1

            ## Evaluate the function at the current value of par
            if par == 0 :
                par = numpy.max([dwarf, paru*0.001])
            temp = math.sqrt(par)
            wa1 = temp * diag
            [r, x, sdiag] = self._qrsolv(r, ipvt, wa1, qtb, sdiag)
            wa2 = diag*x
            dxnorm = self._enorm(wa2)
            temp = fp
            fp = dxnorm - delta

            if ((abs(fp) <= 0.1*delta) or
               ((parl == 0) and (fp <= temp) and (temp < 0)) or
               (iiter == 10)): break

            ## Compute the newton correction
            wa1 = numpy.take(diag, ipvt)*numpy.take(wa2, ipvt)/dxnorm

            for j in range(n-1):
                wa1[j] = wa1[j]/sdiag[j]
                wa1[j+1:n] = wa1[j+1:n] - r[j+1:n,j]*wa1[j]
            wa1[n-1] = wa1[n-1]/sdiag[n-1] ## Degenerate case

            temp = self._enorm(wa1)
            parc = ((fp/delta)/temp)/temp

            ## Depending on the sign of the function, update parl or paru
            if fp > 0 :
                parl = numpy.max([parl,par])
            if fp < 0 :
                paru = numpy.min([paru,par])

            ## Compute an improved estimate for par
            par = numpy.max([parl, par+parc])

            ## End of an iteration

        ## Termination
        return[r, par, x, sdiag]
    #==========================================================================
    # METHOD : _calc_covar
    # PURPOSE :
    #==========================================================================
    def _calc_covar(self, rr, ipvt=None, tol=1.e-14):
        if self["debug"] :
            print('Entering _calc_covar...')
        if numpy.rank(rr) != 2:
            print('ERROR: r must be a two-dimensional matrix')
            return(-1)
        s = numpy.shape(rr)
        n = s[0]
        if s[0] != s[1]:
            print('ERROR: r must be a square matrix')
            return(-1)

        if (ipvt is None) :
            ipvt = numpy.arange(n)
        r = rr.copy()
        r.shape = [n,n]

        ## For the inverse of r in the full upper triangle of r
        l = -1
        tolr = tol * abs(r[0,0])
        for k in range(n):
            if (abs(r[k,k]) <= tolr) :
                break
            r[k,k] = 1./r[k,k]
            for j in range(k):
                temp = r[k,k] * r[j,k]
                r[j,k] = 0.
                r[0:j+1,k] = r[0:j+1,k] - temp*r[0:j+1,j]
            l = k

        ## Form the full upper triangle of the inverse of (r transpose)*r
        ## in the full upper triangle of r
        if l >= 0:
            for k in range(l+1):
                for j in range(k):
                    temp = r[j,k]
                    r[0:j+1,j] = r[0:j+1,j] + temp*r[0:j+1,k]
                temp = r[k,k]
                r[0:k+1,k] = temp * r[0:k+1,k]

        ## For the full lower triangle of the covariance matrix
        ## in the strict lower triangle or and in wa
        wa = numpy.repeat([r[0,0]], n)
        for j in range(n):
            jj = ipvt[j]
            sing = j > l
            for i in range(j+1):
                if sing :
                    r[i,j] = 0.
                ii = ipvt[i]
                if ii > jj :
                    r[ii,jj] = r[i,j]
                if ii < jj :
                    r[jj,ii] = r[i,j]
            wa[jj] = r[j,j]

        ## Symmetrize the covariance matrix in r
        for j in range(n):
            r[0:j+1,j] = r[j,0:j+1]
            r[j,j] = wa[j]

        return(r)
#==============================================================================
# CLASS : Machar
# PURPOSE : machine characteristic numbers
#==============================================================================
class Machar(object):
    def __init__(self, double=1):
        if (double == 0):
            self.machep = 1.19209e-007
            self.maxnum = 3.40282e+038
            self.minnum = 1.17549e-038
            self.maxgam = 171.624376956302725
        else:
            self.machep = 2.2204460e-016
            self.maxnum = 1.7976931e+308
            self.minnum = 2.2250739e-308
            self.maxgam = 171.624376956302725

        self.maxlog = math.log(self.maxnum)
        self.minlog = math.log(self.minnum)
        self.rdwarf = math.sqrt(self.minnum*1.5) * 10
        self.rgiant = math.sqrt(self.maxnum) * 0.1
