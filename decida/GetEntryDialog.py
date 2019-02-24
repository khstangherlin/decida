################################################################################
# CLASS    : GetEntryDialog
# PURPOSE  : generic entry input dialog
# AUTHOR   : Richard Booth
# DATE     : Thu Dec 27 14:08:19 EST 2018
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
import tkinter as tk
from decida.DialogBase import DialogBase

class GetEntryDialog(DialogBase):
    """
    **synopsis**:

        *GetEntryDialog* is a dialog for returning an entry box contents.

    **constructor arguments**:

        **parent** (tk handle, default=None)

            handle of frame or other widget to pack plot in.
            if this is not specified, top-level is created.

        **message** (str, default="")

            message to display

        **title** (str, default="")

            title to be placed on dialog window

        **bitmap** (str, default="")

            bitmap to be displayed on dialog window

        **initialvalue** (str, default="")

            initial value to display in entrybox

    **public methods**:

        * public methods from *DialogBase* (dialog base class)

    """
    #==========================================================================
    # METHOD : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, parent=None, message="", title="", bitmap="question",
        initialvalue=""
    ):
        DialogBase.__init__(self, parent=parent, title=title, bitmap=bitmap)
        self.__message = message
        self.__initialvalue = initialvalue
        self._gui()
    #==========================================================================
    # METHOD : _gui_middle
    # PURPOSE : gui middle section
    #==========================================================================
    def _gui_middle(self):
        top     = self._Component["top"]
        f_table = self._Component["table"]
        bf      = self._Component["but_frame"]
        #---------------------------------------------------------------------
        # middle entries
        #---------------------------------------------------------------------
        f_message = tk.Frame(f_table, relief="flat", bd=3)
        f_message.pack(side="top", expand=True, fill="both")
        f_entry   = tk.Frame(f_table, relief="flat", bd=3)
        f_entry.pack(side="top", expand=True, fill="both")
        m_message = tk.Label(f_message, relief="groove", bd=3,
            bg="GhostWhite", font="Courier 12 normal",
            text=self.__message, anchor="w", justify="left",
            padx=20, pady=20
        )
        m_message.pack(side="top", expand=True, fill="both")
        e_entry = tk.Entry(f_entry, relief="groove", bd=3, bg="GhostWhite")
        e_entry.pack(side="top", expand=True, fill="both")
        e_entry.insert(0, self.__initialvalue)
        self._Component["entry"] = e_entry
        #---------------------------------------------------------------------
        # accept and cancel buttons
        #---------------------------------------------------------------------
        bf_cancel = tk.Frame(bf, bd=2, relief="sunken")
        bf_cancel.pack(side="left", expand=True, padx=3, pady=2)
        bf_cancel_button = tk.Button(bf_cancel, text="cancel",
            command=self.__cancel)
        bf_cancel_button.pack(anchor="c", expand=True, padx=3, pady=2)
        bf_accept = tk.Frame(bf, bd=2, relief="sunken")
        bf_accept.pack(side="left", expand=True, padx=3, pady=2)
        bf_accept_button = tk.Button(bf_accept, text="accept",
            command=self.__accept)
        bf_accept_button.pack(anchor="c", expand=True, padx=3, pady=2)
        self._Component["cancel"] = bf_cancel_button
        self._Component["accept"] = bf_accept_button
        #---------------------------------------------------------------------
        # key bindings
        #---------------------------------------------------------------------
        def cancel_cmd(event, self=self) :
            self.__cancel()
        def accept_cmd(event, self=self) :
            self.__accept()
        top.bind("<Control-Key-q>",      cancel_cmd)
        top.bind("<Control-Key-s>",      accept_cmd)
        top.bind("<Return>",             accept_cmd)
        top.protocol('WM_DELETE_WINDOW', self.__cancel)
    #==========================================================================
    # METHOD: __cancel
    # PURPOSE: cancel button call-back
    #==========================================================================
    def __cancel(self):
        self._return_results = None
        top = self._Component["top"]
        top.quit()
    #==========================================================================
    # METHOD: __accept
    # PURPOSE: accept button call-back
    #==========================================================================
    def __accept(self):
        self._return_results = self._Component["entry"].get().strip()
        top = self._Component["top"]
        top.quit()
