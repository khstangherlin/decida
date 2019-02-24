################################################################################
# FUNCTION : range_sample
# PURPOSE  : lin or log sample a range of values
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:29:37 2013
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
from builtins import range
from decimal import Decimal
import random

def range_sample(beg, end, num=0, step=0.0, mode="lin") :
    """
    **synopsis**:

        lin or log sample a range of values.

    **arguments**:

        **beg** (float)

            begin value of the range to sample

        **end** (float)

            end value of the range to sample

        **num** (int, default=0)

            number of points to sample

        **step** (float, default=0.0)

            step size (lin mode only)

            if first step is greater than last step, step down

        **mode** (str, default="lin")

            sweep mode

            * "lin" linear sampling mode

            * "log" logarithmic sampling mode

            * "uniform" uniform random sampling mode

        **results**:

            * return a list of sampled values

        **examples**:

                >>> import decida
                >>> vmin = 0 ; vmax  = 2
                >>> values = decida.range_sample(vmin, vmax, num=11, mode=\"lin\")
                >>> print values
                [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]

                >>> import decida
                >>> vmin, vmax = 0, 2
                >>> values = decida.range_sample(vmin, vmax, step=0.5)
                >>> print values
                [0.0, 0.5, 1.0, 1.5, 2.0]
    """
    beg_d  = Decimal(str(beg))
    end_d  = Decimal(str(end))
    step_d = Decimal(str(step))
    rng_d  = end_d - beg_d
    values = []
    if step != 0 :
        if rng_d == 0.0 :
            values.append(beg)
        elif mode == "lin" :
            if step_d*rng_d < 0 :
                step_d = -step_d
            npts  = int(rng_d/step_d) + 1
            val_d = beg_d
            #---------------------------------------
            # reject val beyond end
            # to accept 1 beyond, append before test
            #---------------------------------------
            for i in range(0, npts) :
                if ((rng_d > 0) and (val_d > end_d)) or ((rng_d < 0) and (val_d < end_d)) :
                    break
                values.append(float(val_d))
                val_d += step_d
        else :
            print("range_sample: step != 0 only for lin mode")
    else :
        if   num < 1 :
            pass
        elif num == 1 :
            values.append(beg)
        elif mode == "uniform" :
            for i in range(0, num) :
                values.append(beg + float(rng_d)*random.random())
        elif mode == "lin" :
            del_d = rng_d/(num-1)
            values = [float(beg_d + i*del_d) for i in range(0, num)]
        elif mode == "log" :
            if   beg == 0 :
                print("range_sample: beg=0 in log mode")
            elif end == 0 :
                print("range-sample: end=0 in log mode")
            elif beg*end < 0 :
                print("range_sample: beg, end have opposite signs in -log mode")
            else :
                base = 1.0*end/beg
                norm = 1.0/(num-1)
                values = [beg*pow(base, i*norm) for i in range(0, num)]
    return(values)
