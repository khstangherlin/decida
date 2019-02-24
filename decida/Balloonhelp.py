################################################################################
# CLASS    : Ballonhelp
# PURPOSE  : tooltips
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:24:24 2013
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
from decida.ItclObjectx import ItclObjectx

class Balloonhelp(ItclObjectx, tk.Toplevel) :
    """
    **synopsis**:

        Tool-tips help class.

        *Balloonhelp* sets up tool-tips help pop-up windows.

    **configuration options**:

        **verbose** (bool, default=False)

            enable/disable verbose mode

        **active** (bool, default=True)

            enable/disable tool-tip display

        **delay** (int, default=150)

            number of milliseconds to delay before displaying tool-tip
            message after hovering over associated window.

        **background** (str, default="yellow")

            help label background

        **foreground** (str, default="black")

            help label foreground

        **font** (str, default="Lucida 10")

            help label font

        **place** (str, default="under")

            placement of help window with respect to target window.
            One of ("over", "under", "left", "right")

        **offset** (int, default="3")

            offset in x, y placement of help window with respect
            to target window

    **example**:

        >>> from decida.Balloonhelp import Balloonhelp
        >>> import tkinter as tk
        >>> tk= tk.Tk()
        >>> b= tk.Button(text="OK", command=tk.quit)
        >>> b.pack()
        >>> w=Balloonhelp(delay=100, background="#fcf87f")
        >>> w.help_message(b, "display\\n  tooltips")
        >>> tk.mainloop()

    **public methods**:

        * public methods from *ItclObjectx*

    """
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Balloonhelp main
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, **kwargs) :
        ItclObjectx.__init__(self)
        #----------------------------------------------------------------------
        # private variables:
        #----------------------------------------------------------------------
        self.__Component    = {}
        self.__pending      = None
        self.__Help_Message = {}
        #----------------------------------------------------------------------
        # configuration options:
        #----------------------------------------------------------------------
        self._add_options({
            "verbose"        : [False, None],
            "active"         : [True, None],
            "delay"          : [150, None],
            "background"     : ["yellow",    self._config_background_callback],
            "foreground"     : ["black",     self._config_foreground_callback],
            "font"           : ["Lucida 10", self._config_font_callback],
            "place"          : ["under",     self._config_place_callback],
            "offset"         : [3, None],
        })
        #----------------------------------------------------------------------
        # keyword arguments are all configuration options
        #----------------------------------------------------------------------
        for key, value in list(kwargs.items()) :
            self[key] = value
        #----------------------------------------------------------------------
        # build window:
        #----------------------------------------------------------------------
        tk.Toplevel.__init__(self, class_ = "Balloonhelp")
        info = tk.Label(self, justify="left", wraplength="3i")
        info.pack(side="left", fill="y")
        info["background"]  = self["background"]
        info["foreground"]  = self["foreground"]
        info["font"]        = self["font"]
        self.__Component["info"] = info
        self.wm_overrideredirect(True)
        self.wm_withdraw()
        self._config_place_callback()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Balloonhelp configuration option callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _config_background_callback
    # PURPOSE : background
    #==========================================================================
    def _config_background_callback(self) :
        if "info" in self.__Component :
            info  = self.__Component["info"]
            info["background"]  = self["background"]
    #==========================================================================
    # METHOD  : _config_foreground_callback
    # PURPOSE : foreground
    #==========================================================================
    def _config_foreground_callback(self) :
        if "info" in self.__Component :
            info  = self.__Component["info"]
            info["foreground"]  = self["foreground"]
    #==========================================================================
    # METHOD  : _config_font_callback
    # PURPOSE : font
    #==========================================================================
    def _config_font_callback(self) :
        if "info" in self.__Component :
            info  = self.__Component["info"]
            info["font"]  = self["font"]
    #==========================================================================
    # METHOD  : _config_place_callback
    # PURPOSE : place
    #==========================================================================
    def _config_place_callback(self) :
        place = self["place"]
        if not place in ("over", "under", "left", "right") :
            return False
        return True
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Balloonhelp scedule/cancel/show
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _schedule
    # PURPOSE : schedule balloonhelp show
    #==========================================================================
    def _schedule(self, win) :
        self._cancel()
        def cmd(self=self, win=win):
            self._show(win)
        self.__pending = self.after(self["delay"], cmd)
    #==========================================================================
    # METHOD  : _cancel
    # PURPOSE : cancel balloonhelp show
    #==========================================================================
    def _cancel(self) :
        if self.__pending :
            self.after_cancel(self.__pending)
            self.__pending = None
        self.wm_withdraw()
    #==========================================================================
    # METHOD  : _show
    # PURPOSE : balloonhelp show
    #==========================================================================
    def _show(self, win) :
        if self["active"] :
            info = self.__Component["info"]
            info["text"] = self.__Help_Message[win]
            offset = self["offset"]
            self.update_idletasks()
            x = win.winfo_rootx()
            y = win.winfo_rooty()
            wh = win.winfo_height()
            ww = win.winfo_width()
            sh = self.winfo_height()
            sw = self.winfo_width()
            if   self["place"] == "under" :
                x += offset
                y += offset + wh
            elif self["place"] == "over" :
                x += offset
                y -= offset + sh
            elif self["place"] == "left" :
                x -= offset + sw
                y += (wh - sh)//2
            elif self["place"] == "right" :
                x += offset + ww
                y += (wh - sh)//2
            self.wm_geometry("+%s+%s" % (x, y))
            self.wm_deiconify()
            self.lift()
        self.__pending = False
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Balloonhelp public methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : help_message
    # PURPOSE : bindings for balloon help
    #==========================================================================
    def help_message(self, win, message) :
        """ bind a help message to a window.

        **arguments**:

            **win** (tk window)

                window which is to be bound

            **message** (str)

                tool-tip help message to display

        """
        self.__Help_Message[win] = message
        def cmd_enter(event, self=self, win=win) :
            self._schedule(win)
        def cmd_leave(event, self=self) :
            self._cancel()
        win.bind("<Enter>", cmd_enter)
        win.bind("<Leave>", cmd_leave)
