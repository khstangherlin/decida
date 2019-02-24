################################################################################
# CLASS    : CanvasIdentify
# PURPOSE  : report at a particular canvas location
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

class CanvasIdentify(ItclObjectx, tk.Toplevel) :
    """
    **synopsis**:

        Canvas identify class.

        *CanvasIdentify* sets up a pop-up window to report location, curve
        identity, or other information at a canvas position.

    **configuration options**:

        **verbose** (bool, default=False)

            enable/disable verbose mode

        **active** (bool, default=True)

            enable/disable identify display

        **delay** (int, default=150)

            number of milliseconds to delay before displaying identification
            message after hovering over associated window.

        **background** (str, default="yellow")

            help label background

        **foreground** (str, default="black")

            help label foreground

        **font** (str, default="Lucida 10")

            help label font

        **place** (str, default="NE")

            placement of help window with respect to target window.
            One of ("over", "under", "left", "right", "N", "S", "E", "W", "NE", "SE", "NW", "SW")

        **offset** (int, default="10")

            offset in x, y placement of help window with respect
            to target window

    **public methods**:

        * public methods from *ItclObjectx*

    """
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # CanvasIdentify main
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, canvas, **kwargs) :
        ItclObjectx.__init__(self)
        #----------------------------------------------------------------------
        # private variables:
        #----------------------------------------------------------------------
        self.__Canvas       = canvas
        self.__Component    = {}
        self.__pending      = None
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
            "place"          : ["NE",        self._config_place_callback],
            "offset"         : [10, None],
        })
        #----------------------------------------------------------------------
        # keyword arguments are all configuration options
        #----------------------------------------------------------------------
        for key, value in list(kwargs.items()) :
            self[key] = value
        #----------------------------------------------------------------------
        # build window:
        #----------------------------------------------------------------------
        tk.Toplevel.__init__(self, class_ = "CanvasIdentify")
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
    # CanvasIdentify configuration option callback methods
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
        if not place in ("over", "under", "left", "right", "N", "S", "E", "W", "NE", "SE", "NW", "SW") :
            return False
        return True
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # CanvasIdentify schedule/cancel/show
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _schedule
    # PURPOSE : schedule CanvasIdentify show
    #==========================================================================
    def _schedule(self, u, v, message) :
        self._cancel()
        def cmd(self=self):
            self._show(u, v, message)
        self.__pending = self.after(self["delay"], cmd)
    #==========================================================================
    # METHOD  : _cancel
    # PURPOSE : cancel CanvasIdentify show
    #==========================================================================
    def _cancel(self) :
        if self.__pending :
            self.after_cancel(self.__pending)
            self.__pending = None
        self.wm_withdraw()
    #==========================================================================
    # METHOD  : _show
    # PURPOSE : CanvasIdentify show
    # u, v come in as canvas coordinates
    #==========================================================================
    def _show(self, u, v, message) :
        canv = self.__Canvas
        if self["active"] :
            info = self.__Component["info"]
            info["text"] = message
            offset = self["offset"]
            self.update_idletasks()
            cx = canv.winfo_rootx()
            cy = canv.winfo_rooty()
            sh = self.winfo_height()
            sw = self.winfo_width()
            x = cx + u
            y = cy + v
            if   self["place"] in ("under", "S") :
                x -= sw//2
                y += offset
            elif self["place"] in ("over",  "N") :
                x -= sw//2
                y -= (offset + sh)
            elif self["place"] in ("left",  "W") :
                x -= (offset + sw)
                y -= sh//2
            elif self["place"] in ("right", "E") :
                x += offset
                y -= sh//2
            elif self["place"] in ("SE") :
                x += offset
                y += offset
            elif self["place"] in ("NE") :
                x += offset
                y -= (offset + sh)
            elif self["place"] in ("SW") :
                x -= (offset + sw)
                y += offset
            elif self["place"] in ("NW") :
                x -= (offset + sw)
                y -= (offset + sh)

            self.wm_geometry("+%s+%s" % (x, y))
            self.wm_deiconify()
            self.lift()
        self.__pending = False
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # CanvasIdentify public methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : message_show
    # PURPOSE : bindings for CanvasIdentify
    #==========================================================================
    def message_show(self, u, v, text) :
        """ bind a message to a coordinate.

        **arguments**:

            **u** (canvas coordinate)

                canvas horizontal coordinate

            **v** (canvas coordinate)

                canvas vertical coordinate

            **text** (str)

                text to display

        """
        self._schedule(u, v, text)
        def cmd_leave(event, self=self) :
            self._cancel()
        self.bind("<Leave>", cmd_leave)
    #==========================================================================
    # METHOD  : message_hide
    # PURPOSE : bindings for CanvasIdentify
    #==========================================================================
    def message_hide(self) :
        """ hide the canvas identify window.
        """
        self._cancel()
