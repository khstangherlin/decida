################################################################################
# FUNCTION : baseconvert
# PURPOSE  : base conversion (integer only)
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:27:50 2013
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
from builtins import str
from builtins import range
def baseconvert(base_from, base_to, number, digits=None) :
    """
    **synopsis**:

        Convert number in one base to another.

        The input number to be converted by *baseconvert* is the number's string
        representation in *base_from*.  The result is the number's string
        representation in *base_to*.

    **arguments**:

        **base_from** (int)

            number is represented in this base

        **base_to** (int)

            output is to be represented in this base

        **number** (str)

            input number represented in base *base_from*

        **digits** (int, default=None)

            if specified, and output string is shorter than digits,
            fill with zeros until output string is digits long

    **result**:

            return string representation of number in base *base_to*

    **examples**:

            >>> import decida
            >>> decida.baseconvert(16, 10, "1242")
            '74562'

            >>> import decida
            >>> decida.baseconvert(10, 16, "113", 4)
            '0071'

    """
    number = number.lower()
    cmap = "0123456789abcdefghijklmnopqrstuvwxyz"
    d2i = {}
    i2d = {}
    for i, c in enumerate(cmap) :
        d2i[c] = i
        i2d[i] = c
    B = []
    for i, c in enumerate(number) :
        B.append(d2i[c])
    A = []
    while True :
        s = 0
        r = 0
        C = []
        for b in B :
            v = int(b) + r*base_from
            i = v // base_to
            r = v % base_to
            s += i
            C.append(str(i))
        B = C
        A.insert(0, i2d[r])
        if (s == 0) :
            break
    if (digits) :
        for i in range(len(A), digits) :
            A.insert(0, "0")
    result = "".join(A)
    return result
