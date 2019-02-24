################################################################################
# CLASS    : TextWindow
# PURPOSE  : text window for interactive session
# AUTHOR   : Richard Booth
# DATE     : Sat Nov  9 11:26:11 2013
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
##############################################################################
from __future__ import print_function
from builtins import zip
from builtins import str
from builtins import range
import sys
import os
import os.path
import re
import subprocess
import functools
import tkinter as tk
import tkinter.filedialog
import tkinter.colorchooser
import decida
from decida.ItclObjectx      import ItclObjectx
from decida.SelectionDialog  import SelectionDialog
from decida.GetEntryDialog   import GetEntryDialog
from decida.FrameNotebook    import FrameNotebook

class TextWindow(ItclObjectx, tk.Frame) :
    """
    **synopsis**:

        Text window graphical user-interface.

        *TextWindow* is a graphical user-interface wrapper around the tk
        *Text* widget.  On menus, it provides several ways to reformat the
        displayed text, such as lining up rows, (true) wrapping text, piping
        the text through sort, awk, or some other command.  *TextWindow* also
        has text searching and text highlighting.  And there are many other
        tools.

        The DeCiDa application *twin* simply instantiates one *TextWindow*
        object.

    **constructor arguments**:

        **parent** (tk handle, default=None)

            handle of frame or other widget to pack text-window in.
            If this is not specified, top-level is created.

        **\*\*kwargs** (dict)

            configuration-options or option

    **options**:

        **file** (str)

            name of file to read into text-window

    **results**:

        * Sets up text window with menu at top.

        * Configures binding for sending commands to program when user types
           return.

    **configuration options**:

        **verbose** (bool, default=False)

            enable verbose mode

        **text_height** (int, default=24)

            Height of TextWindow window in chars

        **text_width** (int, default=80)

            Width of TextWindow window in chars

        **text_background** (str, default="GhostWhite")

            Background of TextWindow window

        **text_foreground** (str, default="blue")

            Foreground of TextWindow window

        **progcmd** (str, default="")

            Prefix of command to send user-input to program.
            **The progcmd capability is not yet implemented.**

        **prompt** (str, default=">")

            Prompt to place in text window.
            **The progcmd capability is not yet implemented.**

        **wait** (bool, default=False)

            wait in main-loop until window is destroyed

        **destroy** (bool, default=False)

            destroy main window

    **example**:

        >>> twin = TextWindow(wait=False)
        >>> twin.enter("abc")
        >>> twin.wait()

    **public methods**:

        * public methods from *ItclObjectx*

    """
    @staticmethod
    def linecol(linespec) :
        """ convert a linespec into line and column

        **arguments**:

            **linespec** (str)

                Tk line-specification string in the format line.col

        **results**:

            * returns the line, col where line and col are integers

        """
        sline, scol = linespec.split(".")
        line = int(sline)
        col  = int(scol)
        return line, col
    @staticmethod
    def is_commented(s, comment_char="#") :
        """ return true if line begins with a comment character.

        **arguments**:

            **s** (str)

                A line of text

            **comment_char** (str, default="#")

                The specified comment character

        **results**:

            *  If the specified comment character is the first character
               in s, return True, else False.

        """
        s = s.strip()
        return True if len(s) < 1 or s[0] == comment_char else False
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # TextWindow main
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __init__
    # PURPOSE : constructor
    #==========================================================================
    def __init__(self, parent=None, **kwargs) :
        ItclObjectx.__init__(self)
        #----------------------------------------------------------------------
        # private variables:
        #----------------------------------------------------------------------
        self.__parent     = parent
        self.__Component  = {}
        self.__highlighted_lines   = {}
        self.__highlight_color     = "yellow"
        self.__comment_char        = "#"
        self.__truewrap_linelength = 80
        self.__savefile   = ""
        self.__wrapMode   = None
        #----------------------------------------------------------------------
        # configuration options:
        #----------------------------------------------------------------------
        if sys.platform == "darwin" :
            text_width  = 80
            text_height = 24
        else :
            text_width  = 80
            text_height = 24
        self._add_options({
            "verbose"        : [False, None],
            "text_width"     : [text_width,   self._config_text_width_callback],
            "text_height"    : [text_height,  self._config_text_height_callback],
            "text_background": ["GhostWhite", self._config_text_bg_callback],
            "text_foreground": ["black",      self._config_text_fg_callback],
            "progcmd"        : ["",           self._config_progcmd_callback],
            "prompt"         : [">",          None],
            "wait"           : [False,        None],
            "destroy"        : [True,         None],
        })
        #----------------------------------------------------------------------
        # keyword arguments are *not* all configuration options
        # file: command-line option to open file:
        #----------------------------------------------------------------------
        self.__openfile = None
        for key, value in list(kwargs.items()) :
            if key == "file" :
                self.__openfile = value
            else :
                self[key] = value
        #----------------------------------------------------------------------
        # build gui:
        #----------------------------------------------------------------------
        self.__gui()
    #==========================================================================
    # METHOD  : __del__
    # PURPOSE : destructor
    #==========================================================================
    def __del__(self) :
        if self.__toplevel :
            self.__toplevel.destroy()
        else :
            self.destroy()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # TextWindow configuration option callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : _config_text_height_callback
    # PURPOSE : configure text height
    #==========================================================================
    def _config_text_height_callback(self) :
        if not self.__Component :
            return
        height = self["text_height"]
        text = self.__Component["text"]
        text["height"] = height
    #==========================================================================
    # METHOD  : _config_text_width_callback
    # PURPOSE : configure text width
    #==========================================================================
    def _config_text_width_callback(self) :
        if not self.__Component :
            return
        width = self["text_width"]
        text = self.__Component["text"]
        text["width"]  = width
    #==========================================================================
    # METHOD  : _config_text_bg_callback
    # PURPOSE : configure text background
    #==========================================================================
    def _config_text_bg_callback(self) :
        if not self.__Component :
            return
        background = self["text_background"]
        text = self.__Component["text"]
        text["background"]  = background
    #==========================================================================
    # METHOD  : _config_text_fg_callback
    # PURPOSE : configure text foreground
    #==========================================================================
    def _config_text_fg_callback(self) :
        if not self.__Component :
            return
        foreground = self["text_foreground"]
        text = self.__Component["text"]
        text["foreground"]  = foreground
    #==========================================================================
    # METHOD  : _config_progcmd_callback
    # PURPOSE : configure progcmd
    #==========================================================================
    def _config_progcmd_callback(self) :
        if not self.__Component :
            return
        progcmd = self["progcmd"]
        if progcmd == "" :
            # bind TextProg <Return> ""
            pass
        else :
            # text = self.__Component["text"]
            # bind TextProg <Return> self.progcmd_return
            # bindtags text "Text TextProg text top all"
            # text.insert(endtext, self["prompt"])
            # text.mark_set(begtext, endtext)
            # text.mark_set(insert, endtext)
            pass
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # TextWindow GUI
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD  : __gui
    # PURPOSE : build graphical user interface
    #==========================================================================
    def __gui(self) :
        #----------------------------------------------------------------------
        # top-level:
        #----------------------------------------------------------------------
        if self.__parent is None :
            if not tk._default_root :
                root = tk.Tk()
                root.wm_state("withdrawn")
                tk._default_root = root
            self.__toplevel = tk.Toplevel()
            tk.Frame.__init__(self, self.__toplevel, class_ = "TextWindow")
            self.__toplevel.protocol('WM_DELETE_WINDOW', self.__quit_cmd)
            if not self.was_configured("wait") :
                self["wait"] = True
        else :
            self.__toplevel = None
            tk.Frame.__init__(self, self.__parent,   class_ = "TextWindow")
            if not self.was_configured("wait") :
                self["wait"] = False
        self.pack(side="top", fill="both", expand=True)
        #----------------------------------------------------------------------
        # option database:
        #----------------------------------------------------------------------
        if sys.platform == "darwin" :
            self.option_add("*TextWindow*Text.font", "Courier 20 bold")
            self.option_add("*TextWindow*Entry.font", "Courier 20 bold")
            self.option_add("*TextWindow.printCommand", "lpr")
        else :
            self.option_add("*TextWindow*Text.font", "Courier 12 bold")
            self.option_add("*TextWindow*Entry.font", "Courier 12 bold")
            self.option_add("*TextWindow.printCommand", "lpr")
        #----------------------------------------------------------------------
        # main layout
        #----------------------------------------------------------------------
        self.__Component["wbut"] = None
        mbar = tk.Frame(self, relief="raised", bd="3")
        mbar.pack(side="top", fill="x")
        self.__Component["mbar"]  = mbar
        #----------------------------------------------------------------------
        # text-window
        #----------------------------------------------------------------------
        text  = tk.Text(self, wrap="none", undo=True)
        sybar = tk.Scrollbar(self, orient="vertical")
        sxbar = tk.Scrollbar(self, orient="horizontal")
        text["yscrollcommand"] = sybar.set
        text["xscrollcommand"] = sxbar.set
        sybar["command"]       = text.yview
        sxbar["command"]       = text.xview
        text["height"]         = self["text_height"]
        text["width"]          = self["text_width"]
        text["background"]     = self["text_background"]
        text["foreground"]     = self["text_foreground"]
        sybar.pack(side="right", fill="y")
        sxbar.pack(side="bottom", fill="x")
        text.pack(side="top", fill="both", expand=True)
        self.__Component["text"] = text
        #----------------------------------------------------------------------
        # menu-bar
        #----------------------------------------------------------------------
        def cfind(event, self=self):
            self.__clear_find()
        def efind(event, self=self):
            self.__entry_find()
        findframe  = tk.Frame(mbar, relief="raised", bd="3")
        findframe.pack(side="right", fill="x")
        findbutton = tk.Button(findframe, bd="3", text="find", width="10")
        findbutton.pack(side="right")
        findentry  = tk.Entry(findframe, relief="sunken", bd="3")
        findentry.pack(fill="x")
        findentry["width"]=40
        findbutton["command"] = self.__entry_find
        findentry.bind("<Key>",    cfind)
        findentry.bind("<Return>", efind)
        self.__Component["findentry"]  = findentry
        self.__Component["findbutton"] = findbutton
        #----------------------------------------------------------------------
        # File, Edit menu buttons
        # highlight, undo, redo buttons
        #----------------------------------------------------------------------
        filemb = tk.Menubutton(mbar, text="File")
        filemb.pack(side="left", padx=10, pady=10)
        editmb = tk.Menubutton(mbar, text="Edit")
        editmb.pack(side="left", padx=10, pady=10)
        highlight_button = tk.Button(mbar, text="Highlight")
        highlight_button["command"] = self.highlight_lines
        highlight_button.pack(side="left", padx=10, pady=10)
        undo_button = tk.Button(mbar, bd=3, text="undo")
        undo_button["command"] = self.undo
        undo_button.pack(side="left", padx=10, pady=10)
        redo_button = tk.Button(mbar, bd=3, text="redo")
        redo_button["command"] = self.redo
        redo_button.pack(side="left", padx=10, pady=10)
        filemenu = tk.Menu(filemb)
        editmenu = tk.Menu(editmb)
        filemb["menu"] = filemenu
        editmb["menu"] = editmenu
        #----------------------------------------------------------------------
        # File, Edit menu commands
        #----------------------------------------------------------------------
        self.__wrapMode = tk.IntVar()
        self.__wrapMode.set(0)
        def delhigh(self=self):
            self.delete_lines(highlightedflag=True)
        def delunhigh(self=self):
            self.delete_lines(highlightedflag=False)
        def shr(self=self) :
            self.shift_highlighted_lines(shift_left=False)
        def shl(self=self) :
            self.shift_highlighted_lines(shift_left=True)
        filemenu.add_command(label="read",         command=self.fileread)
        filemenu.add_command(label="save",         command=self.filesave)
        filemenu.add_command(label="save as ...",  command=self.filesaveas)
        filemenu.add_command(label="print",        command=self.tbprint)
        filemenu.add_command(label="help",         command=self.help)
        filemenu.add_command(label="quit",         command=self.__quit_cmd)
        editmenu.add_command(label="clear",        command=self.clear)
        editmenu.add_checkbutton(label= "wrap", variable=self.__wrapMode,
            command=self.wrap)
        editmenu.add_command(label="line-up",      command=self.lineup)
        editmenu.add_command(label="line-up (csv)",command=self.lineupcsv)
        editmenu.add_command(label="split-up",     command=self.splitup)
        editmenu.add_command(label="true-wrap",    command=self.truewrap)
        editmenu.add_command(label="trim lines",   command=self.trimlines)
        editmenu.add_command(label="indent highlighted lines",
            command=shr)
        editmenu.add_command(label="unindent highlighted lines",
            command=shl)
        editmenu.add_command(label="delete highlighted lines",
            command=delhigh)
        editmenu.add_command(label="delete non-highlighted lines",
            command=delunhigh)
        editmenu.add_command(label="pipe through ...",
            command=self.pipethrough)
        editmenu.add_command(label="awk  ...",
            command=self.pipethrough_awk)
        editmenu.add_command(label="sort ...",
            command=self.pipethrough_sort)
        editmenu.add_command(label="join spice continued lines",
            command=self.join_spice)
        editmenu.add_command(label="join spectre continued lines",
            command=self.join_spectre)
        editmenu.add_command(label="change highlight color",
            command=self.choose_color)
        editmenu.add_command(label="change comment character",
            command=self.choose_comment_char)

        text = self.__Component["text"]
        # program interface
        #text.tag_configure("prog", foreground="blue")
        #text.tag_configure("user", foreground="red")
        text.mark_set("endtext", 1.0)
        text.mark_set("begtext", "endtext")
        text.mark_set("insert", "endtext")
        text.mark_gravity("begtext", "left")
        text.mark_gravity("endtext", "right")
        #----------------------------------------------------------------------
        # clipboard
        #----------------------------------------------------------------------
        def cb_cut(event=None, self=self):
            try:
                text = self.__Component["text"]
                self.clipboard_clear()
                t = text.get("sel.first", "sel.last")
                text.delete("sel.first", "sel.last")
                self.clipboard_append(t)
            except:
                pass
        def cb_copy(event=None, self=self):
            try:
                text = self.__Component["text"]
                self.clipboard_clear()
                t = text.get("sel.first", "sel.last")
                self.clipboard_append(t)
            except:
                pass
        def cb_paste(event=None, self=self):
            try:
                text = self.__Component["text"]
                t = self.clipboard_get()
                text.insert("insert", t)
            except:
                pass
        def cb_post(event=None, self=self):
            try:
                menu = self.__Component["edit_popup_menu"]
                menu.post(event.x_root, event.y_root)
            except:
                pass
        def cb_unpost(event=None, self=self):
            try:
                menu = self.__Component["edit_popup_menu"]
                menu.unpost()
            except:
                pass
        edit_popup_menu = tk.Menu(text, tearoff=False)
        edit_popup_menu.add_command(label="Copy  ^c", command=cb_copy)
        edit_popup_menu.add_command(label="Cut   ^x", command=cb_cut)
        edit_popup_menu.add_command(label="Paste ^v", command=cb_paste)
        edit_popup_menu.add_separator()
        edit_popup_menu.add_command(label="Cancel",   command=cb_unpost)
        edit_popup_menu.bind("<Leave>", cb_unpost)
        self.__Component["edit_popup_menu"] = edit_popup_menu
        text.bind("<Control-x>", cb_cut)
        text.bind("<Control-c>", cb_copy)
        text.bind("<Control-v>", cb_paste)
        text.bind("<ButtonPress-3>", cb_post)
        #----------------------------------------------------------------------
        # update / mainloop
        #----------------------------------------------------------------------
        text.focus()
        self.update()
        if self.__toplevel:
            self.__toplevel.wm_title("twin")
        if self.__openfile :
            self.fileread(self.__openfile)
        if self["wait"] :
            self.wait()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # TextWindow user commands
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD : wait
    # PURPOSE : wait in main-loop until main window is destroyed
    #==========================================================================
    def wait(self, text=None) :
        """ wait in main-loop until main window is destroyed.

        **arguments**:

            **text** (str, default=None)

                If text is specified, a button is displayed with the text
                in the button.  Clicking the button releases the application
                from the main event-loop.

        **results**:

            * If no text is displayed, then the application waits for the
              TextWindow instance to somehow be destroyed.  If text was
              specified, then the application waits until the button is
              clicked.

        """
        if self.__toplevel :
            self.__toplevel.deiconify()
        if text :
            mbar = self.__Component["mbar"]
            wbut = tk.Button(mbar, text=text, background="gold")
            wbut.pack(side="left")
            wbut["command"] = wbut.destroy
            self.__Component["wbut"] = wbut
            wbut.wait_window()
            if not self.winfo_exists() :
                exit()
        else :
            self.wait_window()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # TextWindow GUI file-menu callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD : fileread
    # PURPOSE : read file (also user method)
    #==========================================================================
    def fileread(self, filename=None) :
        """ read file.

        **arguments**:

            **filename** (str, default=None)

                Name of a file to read and display/edit.
                If *filename* is not specified, then a file dialog is used to
                find a file to read in.

        **results**:

            * Once a file name is found, and it is a valid file, then it
              is read in and displayed in the *Text* window.

        """
        if filename is None :
            if sys.platform == "darwin" :
                filename = tkinter.filedialog.askopenfilename(
                    parent = tk.Frame(self),
                    title = "file name to read?",
                    initialdir = os.getcwd(),
                )
            else :
                filename = tkinter.filedialog.askopenfilename(
                    parent = tk.Frame(self),
                    title = "file name to read?",
                    initialdir = os.getcwd(),
                    filetypes = (
                        ("all files", "*"),
                        ("text files", "*.txt"),
                    )
                )
            if not filename:
                return
        elif not os.path.isfile(filename):
            print("file " + filename + " doesn't exist")
            return
        self.__savefile = filename
        f = open(filename, "r")
        self.clear()
        lines = f.read()
        lines = lines.strip("\n")
        self.enter(lines)
        f.close()
    #==========================================================================
    # METHOD : filesaveas
    # PURPOSE : save file using filesave dialog (also user method)
    #==========================================================================
    def filesaveas(self) :
        """ save file using filesave dialog.

        **arguments**:

            **file** (str, default=None)

                Name of a file to save the *Text* contents to.
                If *file* is not specified, then a file dialog is used to
                find a file name to create or over-write.

        **results**:

            * Once a file name is found, and it is a valid file, then it
              is written or over-written with the contents of the *Text*
              window.

        """
        if sys.platform == "darwin" :
            savefile = tkinter.filedialog.asksaveasfilename(
                parent = tk.Frame(self),
                title = "file name to save?",
                initialfile = self.__savefile,
                initialdir = os.getcwd(),
            )
        else:
            savefile = tkinter.filedialog.asksaveasfilename(
                parent = tk.Frame(self),
                title = "file name to save?",
                initialfile = self.__savefile,
                initialdir = os.getcwd(),
                filetypes = (
                    ("all files", "*"),
                    ("text files", "*.txt"),
                )
            )
        if not savefile :
            return
        self.__savefile = savefile
        self.filesave()
    #==========================================================================
    # METHOD : filesave
    # PURPOSE : save file using current file name (also user method)
    #==========================================================================
    def filesave(self) :
        """ save file using current file name.

        **results**:

            * Save the contents of the *Text* window to the current
              file name, which is established when a file is read-in,
              or a file is specified to write to.

        """
        print("writing " + self.__savefile)
        f=open(self.__savefile, "w")
        lines=self.getall()
        lines=lines.encode("ascii", "replace").decode("ascii")
        f.write(lines)
        f.close()
    #==========================================================================
    # METHOD : tbprint
    # PURPOSE : print (also user method)
    #==========================================================================
    def tbprint(self) :
        """ print.

            **results**:

                * print *Text* window contents, using the current print command.
        """
        try :
            #rintCommand = "lpr"
            printCommand = self.option_get("printCommand", "Command")
        except :
            print("print command not defined")
            return
        filename = "textwindow.txt"
        f = open(filename, "w")
        lines=self.getall()
        lines=lines.encode("ascii", "replace").decode("ascii")
        f.write(lines)
        f.close()
        cmd = printCommand + " " + filename
        subprocess.Popen(cmd.split())
    #==========================================================================
    # METHOD : __quit_cmd
    # PURPOSE : destroy window
    #==========================================================================
    def __quit_cmd(self) :
        self.quit()
        wbut = self.__Component["wbut"]
        if wbut :
            wbut.destroy()
        if self["destroy"] :
            self.__del__()
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # TextWindow GUI edit-menu callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD : clear
    # PURPOSE : delete all text (also user command)
    #==========================================================================
    def clear(self) :
        """ delete all text.

        **results**:

            * The *Text* window is cleared of all text.

        """
        text = self.__Component["text"]
        text.delete(1.0, "end")
        text.mark_set("begtext", "endtext")
        text.mark_set("insert", "endtext")
    #==========================================================================
    # METHOD : enter
    # PURPOSE : enter text (also user command)
    #==========================================================================
    def enter(self, input_text) :
        """ enter text.

        **arguments**:

            **input_text** (str, default=None)

                Lines of text to enter into the *Text* window.

        **results**:

            * The input lines are entered into the *Text* window.

        """
        text = self.__Component["text"]
        text.insert("endtext", input_text, "prog")
        text.mark_set("begtext", "endtext")
        text.mark_set("insert", "endtext")
        self.update()
    #==========================================================================
    # METHOD : get
    # PURPOSE : return text from begtext to endtext marks (also user command)
    #==========================================================================
    def get(self) :
        """ return text from begtext to endtext marks.

        **results**:

            * Return text between begtext and endtext marks, including
              newlines.  The begtext and endtext marks are
              established by (text) highlighting a region of the *Text*
              window contents.

        """
        text = self.__Component["text"]
        input_text = text.get("begtext", "endtext")
        text.mark_set("begtext", "endtext")
        text.mark_set("insert",  "endtext")
        return(input_text)
    #==========================================================================
    # METHOD : getall
    # PURPOSE : return all text (also user command)
    #==========================================================================
    def getall(self) :
        """ return all text.

        **results**:

            * Return all of the *Text* window contents, including newlines.

        """
        text = self.__Component["text"]
        return(text.get(1.0, "end"))
    #==========================================================================
    # METHOD : getlinelist
    # PURPOSE : return lines of text as a list (also user command)
    #==========================================================================
    def getlinelist(self) :
        """ return lines of text as a list.

        **results**:

            * Return all of the *Text* window contents, split into a list
              by newlines.

        """
        lines = self.getall()
        lines = lines.split("\n")
        lines.pop(-1)
        return(lines)
    #==========================================================================
    # METHOD : choose_color
    # PURPOSE : set highlight color using color dialog (also user command)
    #==========================================================================
    def choose_color(self) :
        """ set highlight color using color dialog.

        **results**:

            * Display Tk color dialog (depends on the system)

            * Set the color which is to be used to highlight lines of
              the *Text* window.

        """
        color=self.__highlight_color
        cx, cy = tkinter.colorchooser.askcolor(
            parent=tk.Frame(self), title="color", color=color
        )
        if cy is not None :
            print("color = ", cy)
            self.__highlight_color = str(cy)
    #==========================================================================
    # METHOD : choose_comment_char
    # PURPOSE : set comment character (for lineup command)
    #==========================================================================
    def choose_comment_char(self) :
        """ set comment character.

        **results**:

            * Display dialog to choose a comment character.

            * Type in the comment character, which is used by some of the
              Edit tools.

        """
        ge = GetEntryDialog(title="comment character", message="comment character", initialvalue=self.__comment_char)
        c = ge.go()
        if c is not None :
            self.__comment_char = c
    #==========================================================================
    # METHOD : wrap
    # PURPOSE : wrap text (also user command)
    #==========================================================================
    def wrap(self) :
        """ wrap text.

        **results**:

            * The *Text* window wrap display is toggled.  The actual contents
              of the *Text* window are not changed.

        """
        text = self.__Component["text"]
        if self.__wrapMode.get() == 0 :
            text["wrap"] = "none"
        else :
            text["wrap"] = "char"
    #==========================================================================
    # METHOD : trimlines
    # PURPOSE : trim lines of text (also user command)
    #==========================================================================
    def trimlines(self) :
        """ trim lines of text.

        """
        olines = []
        for line in self.getlinelist() :
            line = line.strip()
            olines.append(line)
        self.clear()
        self.enter("\n".join(olines))
    #==========================================================================
    # METHOD : lineup
    # PURPOSE : line up all un-commented lines (also user command)
    #==========================================================================
    def lineup(self) :
        """ line up all un-commented lines.

        """
        lines = self.getlinelist()
        Col = {}
        for line in lines :
            if TextWindow.is_commented(line, self.__comment_char) :
                continue
            for i, word in enumerate(line.split()) :
                x = len(word)
                if not i in Col or x > Col[i] :
                    Col[i] = x
        olines = []
        for line in lines :
            if TextWindow.is_commented(line, self.__comment_char) :
                olines.append(line)
                continue
            oline = []
            for i, word in enumerate(line.split()) :
                n = Col[i] - len(word)
                pad = " " * n
                oline.append(word + pad)
            olines.append(" ".join(oline))
        self.clear()
        self.enter("\n".join(olines))
    #==========================================================================
    # METHOD : lineupcsv
    # PURPOSE : line up all un-commented lines (also user command) for csv
    #==========================================================================
    def lineupcsv(self) :
        """ line up all un-commented lines.

        """
        lines = self.getlinelist()
        nlines = []
        for line in lines :
            line=re.sub(" ",  "@_SPC_@", line)
            line=re.sub("\t", "@_TAB_@", line)
            line=re.sub(",,", ",_,", line)
            line=re.sub(",", " ", line)
            nlines.append(line)
        Col = {}
        for line in nlines :
            if TextWindow.is_commented(line, self.__comment_char) :
                continue
            for i, word in enumerate(line.split()) :
                word=re.sub("@_SPC_@", " ",  word)
                word=re.sub("@_TAB_@", "\t", word)
                x = len(word)
                if not i in Col or x > Col[i] :
                    Col[i] = x
        olines = []
        for line in nlines :
            if TextWindow.is_commented(line, self.__comment_char) :
                olines.append(line)
                continue
            oline = []
            for i, word in enumerate(line.split()) :
                word=re.sub("@_SPC_@", " ",  word)
                word=re.sub("@_TAB_@", "\t", word)
                n = Col[i] - len(word)
                pad = " " * n
                oline.append(word + pad)
            olines.append(" ".join(oline))
        self.clear()
        self.enter("\n".join(olines))
    #==========================================================================
    # METHOD : pipethrough
    # PURPOSE : pipe text lines through command (also user command)
    #==========================================================================
    def pipethrough(self) :
        """ pipe text lines through command.

        """
        ge = GetEntryDialog(title="pipethrough", message="pipe through command", initialvalue="sort -n -k 1")
        cmd = ge.go()
        if not cmd :
            return
        #----------------------------------------------------------------------
        # tokenize command for subprocess
        #----------------------------------------------------------------------
        apos = False
        toks = []
        tok  = ""
        for c in cmd :
            if c == "'" :
                apos = not apos
                if apos :
                    tok = ""
                else :
                    toks.append(tok)
                    tok = ""
            elif apos :
                tok +=c
            elif c == " " or c == "\t" :
                if tok :
                    toks.append(tok)
                    tok = ""
            else :
                tok += c
        if tok :
            toks.append(tok)

        tmp = "tmp_file.txt"
        f = open(tmp, "w")
        lines=self.getall()
        lines=lines.encode("ascii", "replace").decode("ascii")
        f.write(lines)
        f.close()
        try :
            p1 = subprocess.Popen(["cat", tmp], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(toks, stdin=p1.stdout, stdout=subprocess.PIPE)
            newtext = p2.communicate()[0]
        except subprocess.CalledProcessError as err:
            newtext = ""
            print(err)
        if os.path.isfile(tmp) :
            os.remove(tmp)
        self.clear()
        self.enter(newtext)
    #==========================================================================
    # METHOD : pipethrough_awk
    # PURPOSE : pipe text lines through command (also user command)
    #==========================================================================
    def pipethrough_awk(self) :
        """ pipe text lines through command.

        """
        ge = GetEntryDialog(title="awk", message="awk command", initialvalue="")
        cmd = ge.go()
        if not cmd :
            return
        toks = []
        toks.append("awk")
        toks.append(cmd)
        tmp = "tmp_file.txt"
        f = open(tmp, "w")
        lines=self.getall()
        lines=lines.encode("ascii", "replace").decode("ascii")
        f.write(lines)
        f.close()
        try :
            p1 = subprocess.Popen(["cat", tmp], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(toks, stdin=p1.stdout, stdout=subprocess.PIPE)
            newtext = p2.communicate()[0]
        except subprocess.CalledProcessError as err:
            newtext = ""
            print(err)
        if os.path.isfile(tmp) :
            os.remove(tmp)
        self.clear()
        self.enter(newtext)
    #==========================================================================
    # METHOD : __spice_sort
    # PURPOSE : sort fields with spice scale factors
    #==========================================================================
    def __spice_sort(self, line1, line2, ipos1, ipos2) :
        x1 = line1.split()
        x2 = line2.split()
        i1 = ipos1-1
        i2 = ipos2+1
        for y1,y2 in zip(x1[i1:i2],x2[i1:i2]) :
            u1 = float(decida.spice_value(y1))
            u2 = float(decida.spice_value(y2))
            if   u1 > u2 :
                return 1
            elif u1 < u2 :
                return -1
        return 0
    #==========================================================================
    # METHOD : pipethrough_sort
    # PURPOSE : pipe text lines through command (also user command)
    #==========================================================================
    def pipethrough_sort(self) :
        """ pipe text lines through command.

        """
        guititle = "sort parameters"
        guispecs = [
            ["check", "sort parameters", [
                 ["num", "numeric sort",  True],
                 ["rev", "reverse sort",  False],
                 ["spice", "use spice scale factors",  False],
            ]],
            ["entry", "sort positions",  [
                 ["pos1", "beginning position", "1"],
                 ["pos2", "ending position", ""],
            ]],
        ]
        sd = SelectionDialog(self, title=guititle, guispecs=guispecs)
        V=sd.go()
        if not V["ACCEPT"] :
            return
        pos1  = V["pos1"].strip()
        pos2  = V["pos2"].strip()
        num   = V["num"]
        rev   = V["rev"]
        spice = V["spice"]
        if not pos1 :
            pos1 = "1"
        if not pos2 :
            pos2 = pos1
        if spice :
            ipos1 = int(pos1)
            ipos2 = int(pos2)
            lines = self.getlinelist()
            def ssort(line1, line2, self=self, ipos1=ipos1, ipos2=ipos2) :
                return self.__spice_sort(line1, line2, ipos1, ipos2)
            lines.sort(key=functools.cmp_to_key(ssort))
            if rev:
                lines.reverse()
            self.clear()
            self.enter("\n".join(lines) + "\n")
            return
        toks = []
        toks.append("sort")
        if num :
            toks.append("-n")
        if rev :
            toks.append("-r")
        toks.append("-k")
        toks.append("%s,%s" % (pos1, pos2))

        tmp = "tmp_file.txt"
        f = open(tmp, "w")
        lines=self.getall()
        lines=lines.encode("ascii", "replace").decode("ascii")
        f.write(lines)
        f.close()
        try :
            p1 = subprocess.Popen(["cat", tmp], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(toks, stdin=p1.stdout, stdout=subprocess.PIPE)
            newtext = p2.communicate()[0]
        except subprocess.CalledProcessError as err:
            newtext = ""
            print(err)
        if os.path.isfile(tmp) :
            os.remove(tmp)
        self.clear()
        self.enter(newtext)
    #==========================================================================
    # METHOD : join_spice
    # PURPOSE : join spice netlist continued lines
    #==========================================================================
    def join_spice(self) :
        """ join spice netlist continued lines.

        """
        lines = self.getall()
        lines = re.sub("\r", " ", lines)
        #lines = re.sub("\n *\\+", " ", lines)
        newlines = []
        cline = []
        for line in lines.split("\n") :
            if re.search("^\s*\\*", line) :
                continue
            if re.search("^\s*$",   line) :
                continue
            m = re.search("^\s*\\+(.*)$", line)
            if m :
                cline.append(m.group(1))
            else :
                if cline :
                    newlines.append(" ".join(cline))
                cline = []
                cline.append(line)
        if cline :
            newlines.append(" ".join(cline))
        lines = "\n".join(newlines)
        self.clear()
        self.enter(lines)
    #==========================================================================
    # METHOD : join_spectre
    # PURPOSE : join spectre netlist continued lines
    #==========================================================================
    def join_spectre(self) :
        """ join spectre netlist continued lines.
        """
        xlines = []
        xline = ""
        lines = self.getall()
        lines = lines.split("\n")
        for line in lines :
            line = re.sub("\r", "", line)
            line = re.sub("\n", "", line)
            line = re.sub("\t", " ", line)
            line = line.strip()
            if not line :
                if xline :
                    xline = re.sub("[\t ]+", " ", xline)
                    xlines.append(xline)
                xline = ""
            elif line[-1] == "\\" :
                xline += line[0:-1]
            else :
                xline += line
                xline = re.sub("[\t ]+", " ", xline)
                xlines.append(xline)
                xline = ""
        if xline :
            xline = re.sub("[\t ]+", " ", xline)
            xlines.append(xline)
        self.clear()
        self.enter("\n".join(xlines))
    #==========================================================================
    # METHOD : splitup
    # PURPOSE : split up text lines (also user command)
    #==========================================================================
    def splitup(self) :
        """ split up text lines.

        """
        text = self.__Component["text"]
        #--------------------------------------------------------------------
        # get place to split: position of insert cursor
        #--------------------------------------------------------------------
        line, col = text.index("insert").split(".")
        firstline = int(line)
        place     = int(col)
        if place < 1 :
            print("insert cursor must be to the right of text length for split")
            print("It cannot be at left-most position in the line!")
            return
        #--------------------------------------------------------------------
        # eventually: split-up only highlighted lines!
        #--------------------------------------------------------------------
        lines = self.getlinelist()
        nlines = len(lines)
        Line = {}
        for iline, line in enumerate(lines) :
            nline = iline + 1
            n = min(place, len(line))
            if nline < firstline :
                Line[nline] = [line]
            else :
                Line[nline] = [line[0:n], line[n:]]
        olines = []
        for part in [0, 1] :
            for nline in range(1, nlines+1) :
                if part <= len(Line[nline]) - 1 :
                    olines.append(Line[nline][part])
            olines.append("_" * 72)
        self.clear()
        self.enter("\n".join(olines))
    #==========================================================================
    # METHOD : truewrap
    # PURPOSE : wrap text lines by modifying text (also user command)
    #==========================================================================
    def truewrap(self) :
        """ wrap text lines by modifying text.

        **results**:

            * The contents of the *Text* display are modified such that
              each line of text is limited to 80 characters or less.

        """
        #-------------------------------------------------------------------
        # eventually: truewrap only highlighted lines!
        #-------------------------------------------------------------------
        lines = self.getlinelist()
        linelength = self.__truewrap_linelength
        olines = []
        for line in lines :
            n = len(line)
            if n == 0 or n <= linelength :
                olines.append(line)
            else :
                while n > linelength :
                    found = False
                    i = 0
                    for i in range(linelength - 1, -1 , -1) :
                        if line[i] in [" ", "\t"] :
                            found = True
                            break
                    if  found :
                        olines.append(line[0:i])
                        line = line[i+1:]
                    else :
                        olines.append(line[0:linelength])
                        line = line[linelength:]
                    n = len(line)
                if n > 0 :
                    olines.append(line)
        self.clear()
        self.enter("\n".join(olines))
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # TextWindow GUI highlight callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD : highlight_clear
    # PURPOSE : clear all highlighting (also user command)
    #==========================================================================
    def highlight_clear(self, lineno=None) :
        """ clear highlighting.

        **arguments**:

            **lineno** (int, default=None)

               line number to clear highlighting.

        **results**:

            * Clear highlighting from specified line (lineno).

        """
        text = self.__Component["text"]
        if lineno in self.__highlighted_lines :
            tag = "highlight_" + str(lineno)
            tags = text.tag_names()
            if tag in tags :
                text.tag_delete(tag)
            self.__highlighted_lines.pop(lineno)
    #==========================================================================
    # METHOD : highlight_line
    # PURPOSE : highlight a line of text (also user command)
    #==========================================================================
    def highlight_line(self, lineno) :
        """ highlight a line of text.

        **arguments**:

            **lineno** (int, default=None)

                line number to highlight.

        **results**:

            * Highlight specified line.

        """
        text = self.__Component["text"]
        color = self.__highlight_color
        tag = "highlight_" + str(lineno)
        if not lineno in self.__highlighted_lines :
            self.__highlighted_lines[lineno] = 1
            ef  = str(lineno) + ".0"
            el  = str(lineno) + ".end"
            text.tag_add(tag, ef, el)
        text.tag_configure(tag, background=color)
    #==========================================================================
    # METHOD : highlight_lines
    # PURPOSE : highlight lines of text (also user command)
    #==========================================================================
    def highlight_lines(self) :
        """ highlight lines of text.

        **results**:

            * Highlight lines where text is selected, or insert cursor
              is placed.

        """
        text = self.__Component["text"]
        ranges = text.tag_ranges("sel")
        if len(ranges) == 2 :
            if True or sys.platform == "darwin" :
                sline1 = ranges[0].string
                sline2 = ranges[1].string
            else :
                sline1 = ranges[0]
                sline2 = ranges[1]
            line1, col1 = TextWindow.linecol(sline1)
            line2, col2 = TextWindow.linecol(sline2)
            for lineno in range(line1, line2+1) :
                if lineno in self.__highlighted_lines :
                    self.highlight_clear(lineno)
                else :
                    self.highlight_line(lineno)
        else :
            insert_place = text.index("insert")
            lineno, col = TextWindow.linecol(insert_place)
            if lineno in self.__highlighted_lines :
                self.highlight_clear(lineno)
            else :
                self.highlight_line(lineno)
    #==========================================================================
    # METHOD : gethighlightedlinelist
    # PURPOSE : get highlighted lines of text as list (also user command)
    #==========================================================================
    def gethighlightedlinelist(self) :
        """ get highlighted lines of text as a list.

        **results**:

            * Return list of lines of text which are highlighted.

        """
        text = self.__Component["text"]
        lines = []
        highlightedlines = list(self.__highlighted_lines.keys())
        highlightedlines.sort()
        for lineno in highlightedlines :
            ef = str(lineno) + ".0"
            el = str(lineno) + ".end"
            line = text.get(ef, ef, el)
            lines.append(line)
        print("gethighlightedlinelist", str(lines))
        return(lines)
    #==========================================================================
    # METHOD : delete_lines
    # PURPOSE : delete lines of text (also user command)
    #==========================================================================
    def delete_lines(self, highlightedflag=False) :
        """ delete lines of text.

        **arguments**:

            **highlightedflag** (bool, default=False)

               If True, delete highlighted lines, else delete unhighlighted
               lines.

        **results**:

            * *Text* window lines are deleted: if highlightedflag is True,
              delete only highlighted lines, otherwise delete unhighlighted
              lines.

        """
        olines = []
        lines = self.getlinelist()
        for lineno, line in enumerate(lines) :
            if lineno+1 in self.__highlighted_lines :
                is_highlighted = 1
            else :
                is_highlighted = 0
            if highlightedflag ^ is_highlighted :
                olines.append(line)
        self.clear()
        self.enter("\n".join(olines))
    #==========================================================================
    # METHOD : shift_highlighted_lines
    # PURPOSE : shift highlighted lines right or left
    #==========================================================================
    def shift_highlighted_lines(self, shift_left=False) :
        """ shift highlighted lines right or left.

        **arguments**:

            **shift_left** (bool, default=False)

                If True, shift left, otherwise shift right.

        **results**:

            * Highlighted text is shifted right or left by 4 characters.
              For left-shift, only lines that have 4 spaces to spare at the
              beginning of the line are shifted.

        """
        olines = []
        lines = self.getlinelist()
        for lineno, line in enumerate(lines) :
            if lineno+1 in self.__highlighted_lines :
                if shift_left :
                    line = re.sub("^    ", "", line)
                else :
                    line = "    " + line
            olines.append(line)
        self.clear()
        self.enter("\n".join(olines))
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # TextWindow GUI undo/redo callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD : undo
    # PURPOSE : undo last change (also user command)
    #==========================================================================
    def undo(self) :
        """ undo last change.

        **results**:

            * Last *Text* window editing change is undone.

        """
        text = self.__Component["text"]
        try :
            text.edit_undo()
        except tk.TclError as err :
            print(err)
    #==========================================================================
    # METHOD : redo
    # PURPOSE : redo last change (also user command)
    #==========================================================================
    def redo(self) :
        """ redo last change.

        **results**:

            * Last *Text* window editing change which was undone is redone.

        """
        text = self.__Component["text"]
        try :
            text.edit_redo()
        except tk.TclError as err :
            print(err)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # TextWindow GUI find callback methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD : __entry_find
    # PURPOSE : find entrybox text
    #==========================================================================
    def __entry_find(self) :
        findentry  = self.__Component["findentry"]
        findbutton = self.__Component["findbutton"]
        texttofind = findentry.get()
        self.find(texttofind)
        findbutton.configure(text="find next")
    #==========================================================================
    # METHOD : __clear_find
    # PURPOSE : clear entrybox text
    #==========================================================================
    def __clear_find(self) :
        text       = self.__Component["text"]
        findbutton = self.__Component["findbutton"]
        text.mark_set("mfind", 1.0)
        marks = text.mark_names()
        if "found" in marks :
            text.tag_delete("found")
        findbutton.configure(text="find")
    #==========================================================================
    # METHOD : find
    # PURPOSE : find texttofind (also user command)
    #==========================================================================
    def find(self, texttofind) :
        """ find text.

        **arguments**:

            **texttofine** (str)

                 Text to locate in the *Text* window.

        **results**:

            * If text is found, the *Text* window view is shifted to the
              line where the found text resides and the text is highlighted
              in red foreground.

        """
        text = self.__Component["text"]
        marks = text.mark_names()
        tags  = text.tag_names()
        if not "mfind" in marks :
            text.mark_set("mfind", 1.0)
        find_this = text.search(texttofind, "mfind")
        if find_this != "" :
            n = len(texttofind)
            ef = str(find_this) + " + " + str(n) + " chars"
            if "found" in tags :
                text.tag_delete("found")
            text.tag_add("found", find_this, ef)
            text.tag_configure("found", foreground = "red")
            text.see(find_this)
            text.mark_set("mfind", ef)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # TextWindow program interface methods
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #==========================================================================
    # METHOD : procmd_return
    # PURPOSE : gather user input, send to program, enter program response
    #==========================================================================
    def __progcmd_return(self) :
        """ gather user input, send to program, enter program response.

            ** not implemented **
        """
        #set userinput  [$_text get begtext endtext]
        #set progoutput [eval $progcmd $userinput]
        #$_text insert endtext "$progoutput" prog
        #$_text insert endtext "\n$prompt"
        #$_text mark set begtext endtext
        #$_text mark set insert  endtext
        #$_text see endtext
        pass
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # TextWindow GUI help button callback method
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #--------------------------------------------------------------------------
    # METHOD  : help
    # PURPOSE : help callback (also user command)
    #--------------------------------------------------------------------------
    def help(self) :
        """ help callback.

        **results**:

            * Help FrameNotebook is displayed.

        """
        #--------------------------------------------------------------------
        # locate help directory
        #--------------------------------------------------------------------
        ok = False
        for d in sys.path :
            dirname = "%s/decida/twin_help/" % (d)
            if os.path.isdir(dirname) :
                ok = True
                break
        if not ok :
            self.warning("can't locate help information")
            return
        #--------------------------------------------------------------------
        # get list of files to display (TableOfContents is in hyperhelp format)
        #--------------------------------------------------------------------
        fok = False
        files = []
        Label = {}
        f = open("%s/%s" % (dirname, "TableOfContents"))
        for line in f :
            if   re.match("^ *%% *hyperhelp_link_frame +{", line):
                fok = True
            elif re.match("^ *} *%%", line):
                fok = False
            elif fok :
                line = re.sub("[{}\"]", "", line)
                line = line.strip()
                line = line.split()
                filename = line[-1]
                files.append(filename)
                Label[file] = " ".join(line[:-1])
        f.close()
        #--------------------------------------------------------------------
        # display files
        #--------------------------------------------------------------------
        hfn = FrameNotebook(tab_location="right", wait_to_display=True, destroy=False)
        for filename in files:
            label = Label[filename]
            dfile = "%s/%s" % (dirname, filename)
            TextWindow(hfn.new_page(label), file=dfile)
        hfn.lift_tab(Label[files[0]])
        hfn.wait("dismiss")
        hfn.__del__()
        del hfn
