################################################################################
# CLASS    : ItclObjectx
# PURPOSE  : provides configure, cget, cshow (__getitem__, __setitem__, cshow)
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:21:14 2013
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
import sys
import six

class ItclObjectx(object) :
    """
    **synopsis**:

        Base class to provide configuration option capability.

        *ItclObjectx* is modeled after the [incr Tcl] configuration paradigm.
        Each derived class can add a number of configuration options.
        These options are class attributes which are treated specially.
        An instance of the derived class is configured when created, and
        can be reconfigured after creation.  The configuration/reconfiguration
        causes a call-back (if specified) to be called.  The type of the
        configuration is also checked with the established type.

        *ItclObjectx* also provides message, warning, error, and fatal
        methods, which print messages and react in different ways.

    **adding options**:

        * derived classes use the _add_options protected method to
          add configuration options.  The argument to _add_options is
          a dictionary with the option name as the index, and
          a list of default configuration option value and callback
          as the value of the dictionary index.

    **example**: (from PlotBase derived-class constructor) ::

        def __init__(self) :
            ItclObjectx.__init__(self)
            self._add_options({
                "plot_background"   : ["GhostWhite", self._config_plot_background_callback],
                "legend_background" : ["AntiqueWhite2", self._config_legend_background_callback],
                "colors"            : [colors, None],
            })

    **public methods**:

        * indexing:

            *  <instance>["<config_option>"] returns the
               value of the configuration option named <config_option>

            *  <instance>["<config_option>"]=<value> sets the
               value of the configuration option named <config_option>
               to <value>.  If the configuration option callback returns
               false, the option is set back to the previous value.

    """
    #==========================================================================
    # METHOD: __init__
    # PURPOSE: base class constructor
    #==========================================================================
    def __init__(self):
        self._ConfigOption     = {}
        self._ConfigDefault    = {}
        self._ConfigPrevious   = {}
        self._ConfigCallback   = {}
        self._ConfigConfigured = {}
    #==========================================================================
    # METHOD: _add_options
    # PURPOSE: add more configuration options
    #==========================================================================
    def _add_options(self, Options):
        for key in Options :
            default, callback = Options[key]
            self._ConfigOption[key]     = default
            self._ConfigDefault[key]    = default
            self._ConfigPrevious[key]   = default
            self._ConfigCallback[key]   = callback
            self._ConfigConfigured[key] = False
    #==========================================================================
    # METHOD: __setitem__ aka configure (with one argument)
    # PURPOSE: set configuration options, issue callback
    # NOTES:
    #   * if callback fails set back to previous value
    #==========================================================================
    def __setitem__(self, key, value) :
        if key in self._ConfigOption :
            current_value  = self._ConfigOption[key]
            tc = type(current_value)
            tv = type(value)
            set_str = isinstance(current_value, six.string_types) and isinstance(value, six.string_types)
            set_int = isinstance(current_value, six.integer_types) and isinstance(value, six.integer_types)
            set_i2f = isinstance(current_value, float) and isinstance(value, six.integer_types)
            set_f2i = isinstance(current_value, six.integer_types) and isinstance(value, float) and int(value) == value
            #......................................................
            # note: have trouble with Fitter["data"] config option
            #......................................................
            if (current_value is None) :
                self._ConfigOption[key] = value
                if self._ConfigCallback[key] is not None :
                    if self._ConfigCallback[key]() is False:
                        self._ConfigOption[key] = self._ConfigPrevious[key]
                    else :
                        self._ConfigConfigured[key] = True
                else :
                    self._ConfigConfigured[key] = True
            elif (tc is tv) or set_str or set_int or set_i2f or set_f2i :
                self._ConfigOption[key] = tc(value)
                if self._ConfigCallback[key] is not None :
                    if self._ConfigCallback[key]() is False:
                        self._ConfigOption[key] = self._ConfigPrevious[key]
                    else :
                        self._ConfigConfigured[key] = True
                else :
                    self._ConfigConfigured[key] = True
            else :
                self.warning("configuration option \"%s\" must be type : %s" % (key, str(tc)))
        else:
            self.warning("%s is not a configuration option" % (key))
    #==========================================================================
    # METHOD: __getitem__ aka cget
    # PURPOSE: get a configuration option
    # EXAMPLE: v = inst["vmem"]
    #==========================================================================
    def __getitem__(self, key) :
        if key in self._ConfigOption :
            return(self._ConfigOption[key])
        self.warning("%s is not a configuration option" % (key))
        return None
    #==========================================================================
    # METHOD: config_options
    # PURPOSE: return configuration options
    #==========================================================================
    def config_options(self) :
        """ return configuration option names.

        **results**:

            * Returns list of configuration option names, in no
              particular order.

        """
        return list(self._ConfigOption.keys())
    #==========================================================================
    # METHOD: cshow
    # PURPOSE: show configuration options
    # NOTES:
    #   show all options if option is None
    #==========================================================================
    def cshow(self, key=None) :
        """ show all configuration option values.

        **arguments**:

            **key** (str, default=None)

                configuration option key.

        **results**:

            * if key is not specified, display all configuration
              option values.  if key is specified,

            * if key is specified, display its current configuration value.

        """
        if (key is None) :
            for keyname in self._ConfigOption :
                print("  %s : %s" % (keyname, str(self._ConfigOption[keyname])))
        else :
            if key in self._ConfigOption :
                print("  %s : %s" % (key, str(self._ConfigOption[key])))
            else :
                print("  %s is not a configuration option" % (key))
    #==========================================================================
    # METHOD: was_configured
    # PURPOSE: indicate if option was ever configured
    #==========================================================================
    def was_configured(self, key) :
        """ return true if configuration option was configured.

        **arguments**:

            **key** (str)

                configuration option key

        **results**:

            * return True if configuration option was configured, or
              False if it was never configured.

        """
        if key in self._ConfigConfigured:
            return(self._ConfigConfigured[key])
        self.warning("%s is not a configuration option" % (key))
        return None
    #==========================================================================
    # PROC : message
    # PURPOSE : print message
    #==========================================================================
    def message(self, *args) :
        """ print message.

        **arguments**:

            **\*args** (tuple of str)

                message or parts of message to print.

        **results**:

            * print the class, the method, and the joined argument list.

        """
        _class  = self.__class__
        _method = sys._getframe(1).f_code.co_name
        line = "\n  ".join(args)
        print("%s::%s :\n  %s\n" % (_class, _method, line))
        sys.stdout.flush()
    #==========================================================================
    # PROC : warning
    # PURPOSE : print warning message
    #==========================================================================
    def warning(self, *args) :
        """ print warning message.

        **arguments**:

            **\*args** (tuple of str)

                message or parts of message to print.

        **results**:

            * print "warning", the class, the method, and the
              joined argument list.

        """
        _class  = self.__class__
        _method = sys._getframe(1).f_code.co_name
        line = "\n  ".join(args)
        print("%s::%s warning:\n  %s\n" % (_class, _method, line))
        sys.stdout.flush()
        #--------------------------------------
        # this gets too ugly:
        #--------------------------------------
        # raise RuntimeWarning
    #==========================================================================
    # PROC : error
    # PURPOSE : print error message, raise exception
    #==========================================================================
    def error(self, *args) :
        """ print error message, raise exception, exit.

        **arguments**:

            **\*args** (tuple of str)

                message or parts of message to print.

        **results**:

            * print "error", the class, the method, and the
              joined argument list.

            * raise a RuntimeError **taken out**

            * exit

        """
        _class  = self.__class__
        _method = sys._getframe(1).f_code.co_name
        line = "\n  ".join(args)
        print("%s::%s error:\n  %s\n" % (_class, _method, line))
        sys.stdout.flush()
        #--------------------------------------
        # this gets too ugly:
        #--------------------------------------
        # raise RuntimeError
        exit()
    #==========================================================================
    # PROC : fatal
    # PURPOSE : print error message, raise exception
    #==========================================================================
    def fatal(self, *args) :
        """ print fatal error message, raise exception, exit.

        **arguments**:

            **\*args** (tuple of str)

                message or parts of message to print.

        **results**:

            * print "error", the class, the method, and the
              joined argument list.

            * raise a RuntimeError **taken out**

            * exit

        """
        _class  = self.__class__
        _method = sys._getframe(1).f_code.co_name
        sep = "%" * 72
        line = "\n  ".join(args)
        print("\n%s\n%s::%s error:\n  %s\n%s\n" % (sep, _class, _method, line, sep))
        #--------------------------------------
        # this gets too ugly:
        #--------------------------------------
        # raise RuntimeError

        exit()
