################################################################################
# CLASS    : DialogBase
# PURPOSE  : dialog base class
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
from builtins import object
import tkinter as tk
class DialogBase(object):
    """
    **synopsis**:

        *DialogBase* is a base class for dialog windows.

        *MessageDialog* and *SelectionDialog* inherit *DialogBase*.

    **constructor arguments**:

        **parent** (tk handle, default=None)

            handle of frame or other widget to pack dialog in.
            if this is not specified, top-level is created.

        **title** (str, default="")

            title to be placed on dialog window

    **protected methods**:

        * _gui: build grapical user-interface. derived classes supply
                _gui_middle method to build middle frame

        * _mouse_wheel: mouse-wheel event callback

        * _page_key: page up/dn key event callback

    **public methods**:

    """
    #=========================================================================
    # METHOD : __init__
    # PURPOSE : constructor
    #=========================================================================
    def __init__(self, parent=None, title="", bitmap=""):
        self._parent = parent
        self._title  = title
        self._bitmap = bitmap
        self._debug  = False
        self._Component = {}
        self._return_results = None
    #=========================================================================
    # METHOD: go
    # PURPOSE: display dialog
    #=========================================================================
    def go(self):
        """ post dialog and wait for user response."""
        top = self._Component["top"]
        top.wait_visibility()
        top.grab_set()
        top.mainloop()
        top.grab_release()
        top.destroy()
        root = tk._default_root
        root.update()
        return self._return_results
    #=========================================================================
    # METHOD: _gui_middle
    # PURPOSE: derived classes over-ride this method
    #=========================================================================
    def _gui_middle(self):
        top     = self._Component["top"]
        f_table = self._Component["table"]
        bf      = self._Component["but_frame"]
    #=========================================================================
    # METHOD : _gui
    # PURPOSE : build gui
    #=========================================================================
    def _gui(self):
        #---------------------------------------------------------------------
        # toplevel
        #---------------------------------------------------------------------
        if self._parent is None:
            if not tk._default_root :
                root = tk.Tk()
                root.wm_state("withdrawn")
                tk._default_root = root
            top = tk.Toplevel()
        else :
            top = tk.Toplevel()
        self._Component["top"] = top
        #---------------------------------------------------------------------
        # basic frames
        #---------------------------------------------------------------------
        tf = tk.Frame(top, bd=3, relief="groove")
        tf.pack(side="top", fill="x", expand=False)
        bf = tk.Frame(top, bd=3, relief="flat", bg="cadet blue")
        bf.pack(side="top", fill="x", expand=False)
        mf = tk.Frame(top, bd=3, relief="flat")
        mf.pack(side="top", fill="both", expand=True)
        self._Component["top_frame"] = tf
        self._Component["mid_frame"] = mf
        self._Component["but_frame"] = bf
        #---------------------------------------------------------------------
        # title
        #---------------------------------------------------------------------
        tf_l = tk.Label(tf)
        if self._bitmap != "" :
            tf_l["bitmap"] = self._bitmap
        tf_l.pack(side="left", fill="both", expand=True)
        tf_m = tk.Label(tf, justify="left", text=self._title)
        tf_m.pack(side="right", fill="both", expand=True)
        #---------------------------------------------------------------------
        # canvas/scrollbar
        #---------------------------------------------------------------------
        yscr = tk.Scrollbar(mf)
        yscr.pack(side="right", expand=True, fill="y")
        canv = tk.Canvas(mf)
        canv.pack(side="top", expand=True, fill="both")
        f_table = tk.Frame(canv, relief="flat", bd=3)
        f_table.pack(side="top", expand=True, fill="both")
        yscr.set(0, 0)
        yscr["command"] = canv.yview
        canv["yscrollcommand"] = yscr.set
        self._Component["yscr"] = yscr
        self._Component["canv"] = canv
        self._Component["table"] = f_table
        #---------------------------------------------------------------------
        # middle, buttons, bindings
        #---------------------------------------------------------------------
        self._gui_middle()
        #---------------------------------------------------------------------
        # init
        #---------------------------------------------------------------------
        top.after_idle(self.__place_table)
        self.__set_transient()
    #=========================================================================
    # METHOD: __place_table :
    # PURPOSE: place table on scrollable canvas when ready
    #=========================================================================
    def __place_table(self) :
        top   = self._Component["top"]
        mf    = self._Component["mid_frame"]
        yscr  = self._Component["yscr"]
        canv  = self._Component["canv"]
        table = self._Component["table"]
        top.update_idletasks()
        canv.create_window(0, 0, anchor="nw", window=table)
        width  = table.winfo_reqwidth()
        height = table.winfo_reqheight()
        height = min(height, top.winfo_pixels("8i"))
        canv["height"] = height
        canv["width"]  = width
        canv["scrollregion"] = canv.bbox("all")
        canv["yscrollincrement"] = "0.1i"
        def cmd(event, self=self) :
            top  = self._Component["top"]
            yscr = self._Component["yscr"]
            top.update_idletasks()
            units = yscr.get()
            fill  = units[1] - units[0]
            yscr["width"] = "0.15i" if fill < 1  else 0
        # note: there are multiple configure events
        top.bind("<Configure>", cmd)
    #=========================================================================
    # METHOD: __set_transient
    # PURPOSE: placement of toplevel wrt parent
    #=========================================================================
    def __set_transient(self, relx=0.1, rely=0.1):
        parent = self._parent
        widget = self._Component["top"]
        widget.withdraw() # Remain invisible while we figure out the geometry
        if parent is not None :
            widget.transient(tk.Frame(parent))
        widget.update_idletasks() # Actualize geometry information
        w_width  = widget.winfo_reqwidth()
        w_height = widget.winfo_reqheight()
        s_width  = widget.winfo_screenwidth()
        s_height = widget.winfo_screenheight()
        if parent is not None and parent.winfo_ismapped():
            m_width  = parent.winfo_width()
            m_height = parent.winfo_height()
            m_x      = parent.winfo_rootx()
            m_y      = parent.winfo_rooty()
        else :
            m_width  = s_width
            m_height = s_height
            m_x      = 0
            m_y      = 0
        x = m_x + m_width * relx
        y = m_y + m_height* rely
        # note: multiple monitors, but s_width = screen width of one monitor
        #x = min(x, s_width-w_width)
        x = max(x, 0)
        y = min(y, s_height-w_height)
        y = max(y, 0)
        widget.geometry("+%d+%d" % (x, y))
        widget.resizable(width=False, height=True)
        widget.deiconify() # Become visible at the desired location
    #-------------------------------------------------------------------------
    # METHOD: _mouse_wheel
    # PURPOSE: mouse wheel events
    #-------------------------------------------------------------------------
    def _mouse_wheel(self, event) :
        canv = self._Component["canv"]
        yscr = self._Component["yscr"]
        if yscr["width"] != "0" :
            if   (event.num == 4 or event.delta > 0) :
                canv.yview_scroll(-1, "units")
            elif (event.num == 5 or event.delta < 0) :
                canv.yview_scroll( 1, "units")
    #-------------------------------------------------------------------------
    # METHOD: _page_key
    # PURPOSE: canvas paging
    #-------------------------------------------------------------------------
    def _page_key(self, event) :
        canv = self._Component["canv"]
        yscr = self._Component["yscr"]
        if yscr["width"] != "0" :
            if   (event.keysym == "Prior") :
                canv.yview_scroll(-1, "pages")
            elif (event.keysym == "Next") :
                canv.yview_scroll( 1, "pages")
            elif (event.keysym == "Home") :
                canv.yview_moveto(0)
            elif (event.keysym == "End") :
                canv.yview_moveto(1)
