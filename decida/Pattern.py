################################################################################
# CLASS    : Pattern
# PURPOSE  : generate a bit-sequence pattern
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:23:03 2013
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
import math
import random
from decida.ItclObjectx import ItclObjectx

class Pattern(ItclObjectx) :
    """
    **synopsis**:

        Pattern generator.

        *Pattern* generates one of various bit-sequences and outputs the
        sequence as either a string of 1's and 0's, a piece-wise linear set of
        time, voltage pairs, or a set of time, binary pairs.

        The *Tckt* class uses *Pattern* to generate piece-wise linear voltage
        specifications for procedural simulation scripts.

    **constructor arguments**:

        **\*\*kwargs** (dict)

              keyword=value specifications:
              configuration-options

    **configuration options**:

        **v0** (float, default=0.0)

              low value of the signal.

        **v1** (float, default=1.0)

              high value of the signal.

        **delay** (float, default=0.0)

              delay before first bit.

        **edge** (float, default=50ps)

              rise and fall times in s.

        **period** (float, default=1ns)

              bit period in s.

        **pre** (str, default="")

              specify preamble to bit-pattern (bit-sequence)

        **post** (str, default="")

              specify suffix to bit-pattern (bit-sequence)

        **start_at_first_bit** (bool, default=False)

              Normally a pwl sequence starts at the common-mode.
              If start_at_first_bit=True, start at first bit value.

        **format** (str, default="pwl")

              Format of return list:

                "binary": return pattern only

                "time-binary": return list of time binary pairs

                "pwl": return piecewise linear waveform

    **example** (from test_Pattern): ::

        from decida.Pattern import Pattern

        p = Pattern(delay=4e-9, start_at_first_bit=True, edge=0.1e-9)
        pwl = p.prbs(length=50)
        print("t v")
        for t,v in zip(pwl[0::2], pwl[1::2]) :
            print(t, v)

    **public methods**:

        * public methods from *ItclObjectx*

    """
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Pattern main
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, **kwargs) :
        ItclObjectx.__init__(self)
        #----------------------------------------------------------------------
        # private variables:
        # from www.xilinx.com/support/documentation/application_notes/xapp052.pdf"
        #----------------------------------------------------------------------
        self.__poly = (
            [],            [],    [0],           [1],           [2],           [2],           [4],           [5],
            [5,4,3],       [4],   [6],           [8],           [5,3,0],       [3,2,0],       [4,2,0],       [13],
            [14,12,3],     [13],  [10],          [5,1,0],       [16],          [18],          [20],          [17],
            [22,21,16],    [21],  [5,1,0],       [4,1,0],       [24],          [26],          [5,3,0],       [27],
            [21,1,0],      [19],  [26,1,0],      [32],          [24],          [4,3,2,1,0],   [5,4,0],       [34],
            [37,20,18],    [37],  [40,19,18],    [41,37,36],    [42,17,16],    [43,41,40],    [44,25,24],    [41],
            [46,20,19],    [39],  [48,23,22],    [49,35,34],    [48],          [51,37,36],    [52,17,16],    [30],
            [54,34,33],    [49],  [38],          [57,37,36],    [58],          [59,45,44],    [60,5,4],      [61],
            [62,60,59],    [46],  [64,56,55],    [65,57,56],    [58],          [66,41,39],    [68,54,53],    [64],
            [65,24,18],    [47],  [72,58,57],    [73,64,63],    [74,40,39],    [75,46,45],    [76,58,57],    [69],
            [78,42,41],    [76],  [78,46,43],    [81,37,36],    [70],          [83,57,56],    [84,73,72],    [73],
            [86,16,15],    [50],  [88,71,70],    [89,7,6],      [90,79,78],    [90],          [72],          [83],
            [93,48,46],    [90],  [86],          [96,53,51],    [62],          [99,94,93],    [100,35,34],   [93],
            [102,93,92],   [88],  [90],          [104,43,41],   [76],          [107,102,101], [108,97,96],   [100],
            [109,68,66],   [103], [112,32,31],   [113,100,99],  [114,45,44],   [114,98,96],   [84],          [110],
            [112,8,1],     [102], [120,62,61],   [120],         [86],          [123,17,16],   [124,89,88],   [125],
            [125,100,98],  [123], [126],         [129,83,82],   [102],         [131,81,80],   [76],          [123],
            [134,10,9],    [115], [136,130,129], [135,133,130], [110],         [139,109,108], [120],         [141,122,121],
            [142,74,73],   [92],  [144,86,85],   [145,109,108], [120],         [147,39,38],   [96],          [147],
            [150,86,85],   [151], [151,26,24],   [153,123,122], [154,40,39],   [155,130,129], [156,131,130], [127],
            [158,141,140], [142], [160,74,73],   [161,103,102], [162,150,149], [163,134,133], [164,127,126], [160],
            [165,152,150],
        )
        #----------------------------------------------------------------------
        # configuration options:
        #----------------------------------------------------------------------
        self._add_options({
            "v0"          : [0.0,    None],
            "v1"          : [1.0,    None],
            "delay"       : [0.0,    None],
            "edge"        : [50e-12, None],
            "period"      : [1e-9,   None],
            "pre"         : ["",     None],
            "post"        : ["",     None],
            "start_at_first_bit" : [False,  None],
            "format"      : ["pwl",  None],
        })
        #----------------------------------------------------------------------
        # keyword arguments are all configuration options
        #----------------------------------------------------------------------
        for key, value in list(kwargs.items()) :
            self[key] = value
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Pattern configuration option callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Pattern user commands
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : pattern
    # PURPOSE : specify bit pattern directly
    #==========================================================================
    def pattern(self, pattern) :
        """ specify and generate a bit pattern directly.

        **arguments**:

            **pattern** (str)

                a string of "1"'s and "0"'s

        **results**:

            * The *Pattern* pattern is set to the bit pattern.

            * Returns pattern in format specified by the *format*
              configuration option.

        """
        return self.format(pattern)
    #==========================================================================
    # METHOD : clock
    # PURPOSE : generate clock bit-sequence
    # ARGUMENTS :
    #   % length
    #       number of bits to generate
    #   % startbit (optional)
    #       first bit in the sequence; default=0
    #   % bits_level (optional)
    #       number of bits in each clock level
    #==========================================================================
    def clock(self, length, startbit=0, bits_level=1) :
        """ generate clock pattern (0, 1, 0, 1, 0, ...).

        **arguments**:

            **length** (int)

                The number of bits in the sequence

            **startbit** (int, default=0)

                The starting bit of the bit sequence

            **bits_level** (int, default=1)

                Number of bits in each clock level.

        **results**:

            * The *Pattern* pattern is set to a clock pattern, with
              the start bit set to the specified value.

            * Returns pattern in format specified by the *format*
              configuration option.

        """
        if bits_level < 1:
            bits_level = 1
        pattern = []
        bit = startbit
        while len(pattern) < length :
            bit = 1-bit
            for j in range(0, bits_level) :
                pattern.append(str(bit))
        pattern=pattern[0:length]
        return self.format("".join(pattern))
    #==========================================================================
    # METHOD : long_short
    # PURPOSE : generate long 1/0 followed by clock
    #==========================================================================
    def long_short(self, longs, shorts, startbit=0, length=0) :
        """ generate a bit pattern with several repeated bits, followed by
            a phase where each bit is inverted.

        **arguments**:

            **longs** (int)

                number of bits in the long phase, where each bit
                is repeated.

            **shorts** (int)

                number of bits in the short phase, where each bit
                is inverted.

            **startbit** (int, default=0)

                The starting bit of the bit sequence

            **length** (int, default=0)

                The number of bits in the sequence.
                If not specified, or less than 1, set to long+short

        **results**:

            * The *Pattern* pattern is set to the bit pattern.

            * Returns pattern in format specified by the *format*
              configuration option.

        """
        if length < 1:
            length = longs+shorts
        pattern = []
        bit = startbit
        while len(pattern) < length :
            for j in range(0, longs) :
                pattern.append(str(bit))
            for j in range(0, shorts) :
                bit = 1 - bit
                pattern.append(str(bit))
        pattern = pattern[0:length]
        return self.format("".join(pattern))
    #==========================================================================
    # METHOD : rand
    # PURPOSE : generate random bit-sequence
    # ARGUMENTS :
    #   % length
    #       number of bits to generate
    #   % seed
    #       random seed (default = None)
    #==========================================================================
    def rand(self, length, seed=None) :
        """ generate a random bit sequence.

        **arguments**:

            **length** (int)

                the length of the bit sequence.

            **seed** (str, default=None)

                random seed to initialize random number generator.

        **results**:

            * The *Pattern* pattern is set to a random bit pattern.

            * Returns pattern in format specified by the *format*
              configuration option.

        """
        if seed :
            random.seed(seed)
        pattern = []
        for i in range(0, length) :
            bit = 1 if random.random() > 0.5 else 0
            pattern.append(str(bit))
        return self.format("".join(pattern))
    #==========================================================================
    # METHOD : prbs
    # ARGUMENTS :
    #==========================================================================
    def prbs(self, size=7, length=0) :
        """ generate a pseudo-random bit pattern.

        **arguments**:

            **size** (int, default=7)

                The PRBS specification: size=7 generates a pseudo-random
                bit-sequence of length 2^7-1.

            **length** (int, default=0)

                The length of the bit-sequence.  If length=0, generates
                a sequence of 2^size - 1.

        **results**:

            * The *Pattern* pattern is set to the PRBS bit pattern.

            * Returns pattern in format specified by the *format*
              configuration option.

        """
        if size < 2 or size > 168:
            self.error("size must be between 2 and 168")
            return None
        taps = [int(x) for x in self.__poly[size]]
        if length < 1 :
            length = int(math.pow(2, size)) - 1
        register = [0] * size
        pattern  = []
        for i in range(0, length) :
            acc = register[-1] ^ 1
            pattern.append(str(acc))
            for tap in taps :
                acc = register[tap] ^ acc
            register.pop(-1)
            register.insert(0, acc)
        return self.format("".join(pattern))
    #==========================================================================
    # METHOD : format
    # ARGUMENTS :
    #   % pattern
    #       generated bit sequence
    #==========================================================================
    def format(self, pattern) :
        """ format the bit-sequence.

        **arguments**:

            **pattern** (string)

                a string of "1"'s and "0"'s

        **results**:

            * Returns *Pattern* pattern in format specified by the *format*
              configuration option.

              format is one of:

                * "binary": string sequence of "1"'s and "0"'s

                * "time-binary": pairs of time, and integer value 1 or 0.

                * "pwl": pairs of time, value to account for signal
                  edge, period, and voltage low and high values.

        """
        pat = self["pre"] + pattern + self["post"]
        if   self["format"] == "binary" :
            return pat
        elif self["format"] == "time-binary" :
            time = 0.0
            olist = []
            for sbit in pat :
                olist.extend((time, int(sbit)))
                time += self["period"]
            return olist
        elif self["format"] == "pwl" :
            start = True
            time  = 0.0
            olist = []
            vcm   = (self["v1"] + self["v0"]) * 0.5
            for sbit in pat :
                vbit = self["v1"] if sbit == "1" else self["v0"]
                vbit_1 = vbit
                if start :
                    start = False
                    if self["start_at_first_bit"] :
                        if self["delay"] > 0.0:
                            olist.extend((time, vbit))
                            time += self["delay"]
                        olist.extend((time, vbit))
                    else :
                        if self["delay"] > 0.0:
                            olist.extend((time, vcm))
                            time += self["delay"]
                        olist.extend((time, vcm))
                        time += self["edge"]*0.5
                        olist.extend((time, vbit))
                else :
                    time += self["period"] - self["edge"]
                    olist.extend((time, vbit_1))
                    time += self["edge"]
                    olist.extend((time, vbit))
                vbit_1 = vbit
            return olist
        return None
