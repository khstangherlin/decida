################################################################################
# CLASS    : Itemizer
# PURPOSE  : cross-product iterator package
# AUTHOR   : Richard Booth
# DATE     : Wed Jul 20 13:38:52 EDT 2016
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
from builtins import object
import itertools
class Itemizer(object):
    """
    **synopsis**:

        Cross-product iterator with tag.

        Each *Itemizer* iteration produces a list of elements, one from each
        contributing list of iterators.

        At each iteration, the tag() method produces a string for
        naming or reporting.

    **constructor arguments**:

        **\*iterators** (iterables)

            variable arguments are each an iterator

        **tag** (str, default=None)

            format string for the tag.  If None, then tag is
            "%s. ... %s" (number of iterators)

    **results**:

        * the Itemizer instance iterates over the cross-product of
          all of the specified iterators.

        * each iteration produces a list of elements, one from each iterator.

        * the tag() method produces a string for naming or reporting.

    **example** (from test_Itemizer):

        >>> from decida.Itemizer import Itemizer
        >>> procs = ["TT", "SS", "FF"]
        >>> vdds  = [0.9, 1.0, 1.1]
        >>> temps = [0, 25, 100]
        >>> ix = Itemizer(procs, vdds, temps, tag="%s.V_%s.T_%s")
        >>> for proc, vdd, temp in ix :
        >>>    tag = ix.tag()
        >>>    print tag, proc, vdd, temp
        TT.V_0.9.T_0 TT 0.9 0
        TT.V_0.9.T_25 TT 0.9 25
        TT.V_0.9.T_100 TT 0.9 100
        TT.V_1.0.T_0 TT 1.0 0
        TT.V_1.0.T_25 TT 1.0 25
        TT.V_1.0.T_100 TT 1.0 100
        TT.V_1.1.T_0 TT 1.1 0
        TT.V_1.1.T_25 TT 1.1 25
        TT.V_1.1.T_100 TT 1.1 100
        SS.V_0.9.T_0 SS 0.9 0
        SS.V_0.9.T_25 SS 0.9 25
        SS.V_0.9.T_100 SS 0.9 100
        SS.V_1.0.T_0 SS 1.0 0
        SS.V_1.0.T_25 SS 1.0 25
        SS.V_1.0.T_100 SS 1.0 100
        SS.V_1.1.T_0 SS 1.1 0
        SS.V_1.1.T_25 SS 1.1 25
        SS.V_1.1.T_100 SS 1.1 100
        FF.V_0.9.T_0 FF 0.9 0
        FF.V_0.9.T_25 FF 0.9 25
        FF.V_0.9.T_100 FF 0.9 100
        FF.V_1.0.T_0 FF 1.0 0
        FF.V_1.0.T_25 FF 1.0 25
        FF.V_1.0.T_100 FF 1.0 100
        FF.V_1.1.T_0 FF 1.1 0
        FF.V_1.1.T_25 FF 1.1 25
        FF.V_1.1.T_100 FF 1.1 100

    **public methods**:

    """
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Itemizer main
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #========================================================================== 
    # METHOD  : __init__
    # PURPOSE : constructor
    #==========================================================================
    def  __init__(self, *iterables, **kwargs) :
        self.__iterx = itertools.product(*iterables)
        self.__tag = None
        for k, v in list(kwargs.items()):
            if k == "tag" :
                self.__tag = v
        if self.__tag is None :
            self.__tag = ".".join(["%s"] * len(iterables))
        self.__length = 1
        for q in iterables :
            self.__length *= len(q)
        #----------------------------------------------------------------------
        # class variables
        #----------------------------------------------------------------------
        self.__value = None
    #==========================================================================
    # METHOD  : __len__
    # PURPOSE : number of experiments
    #==========================================================================
    def __len__(self) :
        return self.__length
    #==========================================================================
    # METHOD  : __iter__
    # PURPOSE : iterator method (private)
    #==========================================================================
    def __iter__(self) :
        return self
    #==========================================================================
    # METHOD  : tag
    # PURPOSE : generate string based on specified tag format and element values
    #==========================================================================
    def tag(self) :
        """ generate string based on specified tag format and element values

        """
        return self.__tag % (self.__value)
    #==========================================================================
    # METHOD  : next
    # PURPOSE : produce next iteration
    #==========================================================================
    def __next__(self) :
        """ produce next iteration
        """
        self.__value = next(self.__iterx)
        return self.__value
