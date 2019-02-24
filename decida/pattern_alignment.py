################################################################################
# FUNCTION : pattern_alignment
# PURPOSE  : align several bit patterns for maximum correlation
# AUTHOR   : Richard Booth
# DATE     : Wed Aug  1 16:33:59 2012
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
from builtins import range
def pattern_alignment(patterns):
    """
    **synopsis**:

        Align several bit patterns for maximum correlation.

    **arguments**:

        **patterns** (list)

            list of bit patterns (strings of "1", "0")

    **results**:

        * returns list of lists of aligned patterns and pair bit-errors

    **example**:

        >>> from decida.pattern_alignment import pattern_alignment
        >>> pats = ["1000001000010101110110101110",
            "1000001000010101110110101110010111",
            "01000010101110110101110010111000111000"
        >>> ]
        for ab in pattern_alignment(pats) :
            print(ab[1], ab[0])

    """
    #--------------------------------------------------------
    # find maximum correlation between each pair of patterns
    #--------------------------------------------------------
    alignpairs = []
    for pat1, pat2 in zip(patterns[0:], patterns[1:]) :
        if len(pat1) < len(pat2) :
            p1, p2 = pat2, pat1
            flag = True
        else :
            p1, p2 = pat1, pat2
            flag = False
        np1 = len(p1)
        np2 = len(p2)
        nalign = np1 + np2 - 1
        maxcorr  = 0
        imaxcorr = 0
        for ialign in range(nalign) :
            corr = 0
            for ib2 in range(np2) :
                ib1 = ialign + ib2 - np2 - 1
                if ib1 > 0 and ib1 < np1 :
                    bit2 = p2[ib2]
                    bit1 = p1[ib1]
                    if bit2 == bit1 :
                        corr += 1
                    elif bit1 != " ":
                        corr -= 1
            if corr > maxcorr :
                maxcorr = corr
                imaxcorr = ialign - np2 - 1
        if imaxcorr < 0:
            align1 = -imaxcorr
            align2 = 0
        else :
            align1 = 0
            align2 = imaxcorr
        if flag :
            align1, align2 = align2, align1
        alignpairs.append((align1, align2))
    #----------------
    # align patterns
    #----------------
    Pats = []
    pair = alignpairs[0]
    a = pair[1]
    for pair in alignpairs :
        a += pair[0]
    Pats.append(" " * a + patterns[0])
    for pair, pattern in zip(alignpairs, patterns[1:]) :
        a += pair[1] - pair[0]
        Pats.append(" " * a + pattern)
    #------------------------------------------
    # find bit errors between aligned patterns
    #------------------------------------------
    Bers = []
    Bers.append(0)
    for pat1, pat2 in zip(Pats[0:], Pats[1:]) :
        ber = 0
        for b1, b2 in zip(pat1, pat2):
            if not (b1 == " ") and not (b2 == " ") and not(b1 == b2) :
                ber += 1
        Bers.append(ber)
    #---------------------------------------------------------
    # return list of list of aligned pattern, pair bit-errors
    #---------------------------------------------------------
    Ret = []
    for pat, ber in zip(Pats, Bers) :
        Ret.append([pat, ber])
    return Ret
