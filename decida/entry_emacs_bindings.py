################################################################################
# FUNCTION : entry_emacs_bindings
# PURPOSE  : provide ^n ^p ^k ^y emacs bindings to a set of entry windows
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:28:05 2013
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
from builtins import zip
from builtins import str

yank = ""
def entry_emacs_bindings(entry_list) :
    """
    **synopsis**:

        Provide ^n ^p ^k ^y emacs bindings to a set of entry windows.

    **arguments**:

        **entry_list** (list of handles)

            list of tk entry handles

    **results**:

        * ^n and ^p focus on next or previous entry windows, respectively

        * ^k kills entry to end of line and saves the string

        * ^y enters a killed string into the current entry box

    """
    if not entry_list :
        return
    prev = entry_list[:-1]
    prev.insert(0, entry_list[-1])
    nexc = entry_list[1:]
    nexc.append(entry_list[0])

    for entry, prev, nexc in zip(entry_list, prev, nexc) :
        def cmdp(event, entry=entry, prev=prev) :
            prev.focus()
        def cmdn(event, entry=entry, nexc=nexc) :
            nexc.focus()
        def cmdk(event, entry=entry) :
            global yank
            c = entry.index("insert")
            e = entry.index("end")
            yank = str(entry.get())[c:e+1]
            entry.delete("insert", "end")
        def cmdy(event, entry=entry) :
            global yank
            entry.insert("insert", yank)
        entry.bind("<Control-Key-p>", cmdp)
        entry.bind("<Control-Key-n>", cmdn)
        entry.bind("<Control-Key-k>", cmdk)
        entry.bind("<Control-Key-y>", cmdy)
