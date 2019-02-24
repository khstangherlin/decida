################################################################################
# CLASS    : StatusDialog
# PURPOSE  : generic status dialog
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:24:40 2013
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
import sys
import os
import tkinter as tk
import tkinter.filedialog
from decida.DialogBase import DialogBase
from decida.ItclObjectx import ItclObjectx

class StatusDialog(ItclObjectx, DialogBase):
    """
    **synopsis**:

        Generic message dialog for status information.

        *StatusDialog* is a generic dialog for displaying status information.

    **constructor arguments**:

        **parent** (tk handle, default=None)

            handle of frame or other widget to pack plot in.
            if this is not specified, top-level is created.

        **title** (str, default="")

            title to be placed on dialog window

        **bitmap** (str, default="")

            bitmap to be displayed on dialog window

        **command** (function, default=None)

            command to update status

    **configuration options**:

        **verbose** (bool, default=False)

            enable verbose mode

        **update_time_ms** (int, default=1000)

            time interval to check status, in milliseconds

    **public methods**:

        * public methods from *ItclObjectx*

        * public methods from *DialogBase*

    """
    #==========================================================================
    # METHOD : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, parent=None, title="", bitmap="info", command=None,
        **kwargs
    ):
        ItclObjectx.__init__(self)
        DialogBase.__init__(self, parent=parent, title=title, bitmap=bitmap)
        #----------------------------------------------------------------------
        # private variables:
        #----------------------------------------------------------------------
        self.__status_file = "status.txt"
        self.__command = command
        self.__iter = 0
        self.__after_id = None
        #----------------------------------------------------------------------
        # configuration options:
        #----------------------------------------------------------------------
        self._add_options({
            "verbose"          : [False, None],
            "update_time_ms"   : [1000, self._config_update_time_ms_callback],
        })
        #----------------------------------------------------------------------
        # keyword arguments are all configuration options
        #----------------------------------------------------------------------
        for key, value in list(kwargs.items()) :
            self[key] = value
        #----------------------------------------------------------------------
        # run command to update status message
        #----------------------------------------------------------------------
        if self.__command :
            self.__message = self.__command()
            while self.__message is None :
                self.__message = self.__command()
        #----------------------------------------------------------------------
        # start logging status
        #----------------------------------------------------------------------
        self._gui()
        msg = self._Component["message"]
        msg.update()
        self.__status_update()
        self.go()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # StatusDialog configuration option callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _config_update_time_ms_callback
    # PURPOSE : configure text height
    #==========================================================================
    def _config_update_time_ms_callback(self) :
        if self["update_time_ms"] <= 0 :
            return False
        return True
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # StatusDialog gui, update
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD : __status_update
    # PURPOSE : update status display
    #==========================================================================
    def __status_update(self):
        if self.__command :
            self.__iter += 1
            self.__message = self.__command()
            msg = self._Component["message"]
            msg["text"] = self.__message
            msg.update()
            self.__after_id = msg.after(self["update_time_ms"], self.__status_update)
    #==========================================================================
    # METHOD : _gui_middle
    # PURPOSE : gui middle section
    #==========================================================================
    def _gui_middle(self):
        top     = self._Component["top"]
        f_table = self._Component["table"]
        bf      = self._Component["but_frame"]
        message = self.__message
        #----------------------------------------------------------------------
        # middle entries
        #----------------------------------------------------------------------
        f_message = tk.Frame(f_table, relief="flat", bd=3)
        f_message.pack(side="top", expand=True, fill="both")
        m_message = tk.Label(f_message, relief="groove", bd=3, bg="GhostWhite",
            font="Courier 12 normal", text=message, anchor="w", justify="left",
            padx=20, pady=20)
        m_message.pack(side="top", expand=True, fill="both")
        m_message.bind("<MouseWheel>", self._mouse_wheel)
        m_message.bind("<Button-4>",   self._mouse_wheel)
        m_message.bind("<Button-5>",   self._mouse_wheel)
        m_message.bind("<Prior>",      self._page_key)
        m_message.bind("<Next>",       self._page_key)
        m_message.bind("<Home>",       self._page_key)
        m_message.bind("<End>",        self._page_key)
        self._Component["message"] = m_message
        #----------------------------------------------------------------------
        # write button
        #----------------------------------------------------------------------
        bf_write = tk.Frame(bf, bd=2, relief="sunken")
        bf_write.pack(side="left", expand=True, padx=3, pady=2)
        bf_write_button = tk.Button(bf_write, text="write ...",
            command=self.__write)
        bf_write_button.pack(anchor="c", expand=True, padx=3, pady=2)
        self._Component["write"] = bf_write_button
        #----------------------------------------------------------------------
        # ok button
        #----------------------------------------------------------------------
        bf_ok = tk.Frame(bf, bd=2, relief="sunken")
        bf_ok.pack(side="left", expand=True, padx=3, pady=2)
        bf_ok_button = tk.Button(bf_ok, text="ok",
            command=self.__ok)
        bf_ok_button.pack(anchor="c", expand=True, padx=3, pady=2)
        self._Component["ok"] = bf_ok_button
        #----------------------------------------------------------------------
        # key bindings
        #----------------------------------------------------------------------
        def ok_cmd(event, self=self) :
            self.__ok()
        top.bind("<Control-Key-s>",      ok_cmd)
        top.bind("<Return>",             ok_cmd)
        top.protocol('WM_DELETE_WINDOW', self.__ok)
    #==========================================================================
    # METHOD: __ok
    # PURPOSE: ok button call-back
    #==========================================================================
    def __ok(self):
        top = self._Component["top"]
        if self.__after_id:
            top.after_cancel(self.__after_id)
        top.quit()
    #==========================================================================
    # METHOD: __write
    # PURPOSE: write button call-back
    #==========================================================================
    def __write(self):
        top = self._Component["top"]
        initialfile = self.__status_file
        if sys.platform == "darwin" :
            filename = tkinter.filedialog.asksaveasfilename(
                parent = top,
                title = "Status file name to save?",
                initialfile=initialfile,
                initialdir = os.getcwd(),
                defaultextension = ".txt",
            )
        else:
            filename = tkinter.filedialog.asksaveasfilename(
                parent = top,
                title = "Status file name to save?",
                initialfile=initialfile,
                initialdir = os.getcwd(),
                defaultextension = ".txt",
                filetypes = (
                    ("Text format files", "*.txt"),
                    ("all files", "*")
                )
            )
        if not filename :
            return
        self.__status_file = filename
        f = open(filename, "w")
        f.write(self.__message)
        f.close()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # StatusDialog public methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD: go
    # PURPOSE: display dialog
    #==========================================================================
    def go(self):
        """ post dialog and wait for user response."""
        top = self._Component["top"]
        top.mainloop()
        root = tk._default_root
        root.update()
