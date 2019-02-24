;############################################################################
;# translations
;############################################################################
;============================================================================
; RVBgetenv
; return environment parameter
;============================================================================
procedure(RVBgetenv(var)
  let(()
    getShellEnvVar(var)
  )
)
;============================================================================
; RVBecho
;============================================================================
procedure(RVBecho(messageString)
  prog(()
    printf("%s\n" messageString)
  )
)
;============================================================================
; RVBisNumString
; returns t if string can be successfully converted to an integer or real
; annoyingly atof("3.3v") returns 3.3 
;============================================================================
procedure(RVBisNumString(valString)
  prog((rval sval)
    rval=atof(valString)
    if(rval == nil return(nil))
   ;sval=sprintf(sval "%f" rval)
    return(t)
  )
)
;============================================================================
; RVBlset
; set list items to values 
; has problems 3.3v is interpreted as a number (3.3)
;============================================================================
procedure(RVBlset(varString valString)
  prog((var vars val vals sym num opn)
    vars=parseString(varString)
    vals=parseString(valString)
    foreach(var vars
      val=car(vals)
      vals=cdr(vals)
      if(RVBisNumString(val) then
        RVBecho(strcat("number " var " " val))
        evalstring(strcat(var "=" val))
      else
        RVBecho(strcat("string " var " " val))
        evalstring(strcat(var "=\"" val "\""))
      )
    )
    t
  )
)
;============================================================================
; RVBsetenv
; set environment parameter
;============================================================================
procedure(RVBsetenv(var val)
  let(()
    setShellEnvVar(strcat(var "=" val))
  )
)
;============================================================================
; RVBlunique
; return new list with unique elements
;============================================================================
procedure(RVBlunique(input_list)
  let((new_list)
    newlist = nil
    foreach(item input_list
      if(!member(item newlist) then
        newlist = append(newlist list(item))
      )
    )
    newlist
  )
)
;============================================================================
; RVBseparator
; return separator string, composed of nchars characters
;============================================================================
procedure(RVBseparator(char @optional (nchars 78))
  let((s)
    s=""
    for(i 1 nchars
      s=strcat(s char)
    )
    s
  )
)
;============================================================================
; RVBjoin
; join strings in a list together, separated with char
; originally:
; let((s i)
;   s=""
;   i=0
;   foreach(item list
;     if((i==1) then
;       s=strcat(s char)
;     )
;     s=strcat(s item)
;     i=1
;   )
;   s
; )
;============================================================================
procedure(RVBjoin(list @optional (char " "))
  buildString(list char)
)
;============================================================================
; RVBsplit
; split string using char, return list
;============================================================================
procedure(RVBsplit(string @optional (char " "))
  parseString(string char)
)
;=============================================================================
; RVBfileView
;   View a file
;=============================================================================
procedure(RVBfileView(file)
  view(file)
)
;============================================================================
; RVBmessageBox
;============================================================================
procedure(RVBmessageBox(@rest lines)
  let( (message)
    message = ""
    foreach( line lines
      message = strcat(message line "\n")
    )
    hiDisplayAppDBox(
      ?name 'messageBox
      ?dboxBanner ""
      ?dboxText   message
      ?dialogType hicQuestionDialog
      ?dialogStyle 'modal
      ?buttonLayout 'Close
      ?defaultButton  1
    )
  )
)
;============================================================================
; RVBwarning
;   display warning dialog box
;============================================================================
procedure(RVBwarning(@rest lines)
  let( (message)
    message = ""
    foreach( line lines
      message = strcat(message line "\n")
    )
    hiDisplayAppDBox(
      ?name 'Warning
      ?dboxBanner "warning"
      ?dboxText message
      ?dialogType hicWarningDialog
      ?dialogStyle 'modal
      ?buttonLayout 'Close
    )
  )
)
;============================================================================
; RVBerror
;   display error dialog box
;============================================================================
procedure(RVBerror(@rest lines)
  let( (message)
    message = ""
    foreach( line lines
      message = strcat(message line "\n")
    )
    hiDisplayAppDBox(
      ?name 'Error
      ?dboxBanner "error"
      ?dboxText message
      ?dialogType hicErrorDialog
      ?dialogStyle 'modal
      ?buttonLayout 'Close
    )
  )
)
;=============================================================================
; RVBtextWindow
; display text in a window
;=============================================================================
procedure(RVBtextWindow(text)
  textBox = hiCreateMLTextField(
    ?name        'textBox
    ?value       text
    ?hasVerticalScrollbar t
  )
  theForm = hiCreateAppForm(
    ?name         'textWindow
    ?formTitle    "Text Window"
    ?fields       list(textBox)
  )
  theForm->buttonLayout=list('OKCancelApply)
  hiDisplayForm(theForm)    
)
;############################################################################
;#
;############################################################################
;=============================================================================
; RVBgetCV
; get cell view handle of current window
;=============================================================================
procedure(RVBgetCV()
  let((win view)
    win=hiGetCurrentWindow()
    if(win != nil then
      view=geGetWindowCellView(win)
    else
      view=nil
    )
    view
  )
)
;=============================================================================
; RVBinstProps()
; print out all instance properties in a cell view
;=============================================================================
procedure(RVBinstProps()
  prog((cv ih fout name bBox ni)
    ;-------------------------------------------------------------------------
    ; schematic window must be open
    ;-------------------------------------------------------------------------
    cv=RVBgetCV()
    if(cv == nil then
      return("Schematic window not open")
    )
    ;-------------------------------------------------------------------------
    ; instance info
    ;-------------------------------------------------------------------------
    fout=outfile("info.txt")
    ni=0
    foreach(ih cv~>instances
      name=strcat(ih~>libName ":" ih~>cellName "::" ih~>name)
      fprintf(fout strcat(RVBseparator("=" 55) "\n"))
      fprintf(fout "%-4d:   %L\n" ni name)
      fprintf(fout strcat(RVBseparator("=" 55) "\n"))
      foreach(x ih~>?
        fprintf(fout "  %-15s = %L\n" x evalstring(strcat("ih~>" x)))
      )
      foreach(x ih~>prop
        fprintf(fout "    %-15s = %L\n" x~>name x~>value)
      )
      ni=ni+1
    )
    close(fout)
    bBox='((0 0) (540 800))          ; set view box size
    view("info.txt" bBox)            ; view the file
  )
)
;============================================================================
; RVBinstNames
; list instance names in current cell view
;============================================================================
procedure(RVBinstNames()
  prog((mosfets scale ih libr cell name names Info report
    ignoreLibrs ignoreLibrsString)
    mosfets=parseString(
      strcat(
        " lvtnfet_b lvtpfet_b"
        " nch_25od33 nch_lvt nch_hvt"
        " nch_25od33_dnw nch_lvt_dnw nch_hvt_dnw"
        " pch_25od33 pch_lvt pch_hvt"
        " nch_12 nch_12_dnw pch_12"
        " nsfet psfet nufet pufet nefet pefet nlfet plfet"
        " ntfet ptfet ntsfet ptsfet nt33fet pt33fet nts33fet pts33fet"
        " tnlfet tplfet tnefet tpefet tnsfet tpsfet"
        " tntsfet tptsfet tntfet tptfet"
        " nsmos psmos numos pumos nemos pemos nlmos plmos"
        " ntmos ptmos ntsmos ptsmos nt33mos pt33mos nts33mos pts33mos"
        " tnsmos tpsmos tnumos tpumos tnemos tpemos tnlmos tplmos"
        " tntsmos tptsmos tntmos tptmos"
      )
    )
    ;-------------------------------------------------------------------------
    ; schematic window must be open
    ;-------------------------------------------------------------------------
    cv=RVBgetCV()
    if(cv == nil then
      return("Schematic window not open")
    )
    ;-------------------------------------------------------------------------
    ; accumulate instance info, then sort by names
    ;-------------------------------------------------------------------------
    ignoreLibrsString = "basic com analogLib"
    ignoreLibrsString = "basic US_8ths"
    ignoreLibrs=parseString(ignoreLibrsString)
    Info=makeTable("info")
    foreach(ih cv~>instances
      name=ih~>name
      libr=ih~>libName
      cell=ih~>cellName
      name=strcat(libr ":" cell "::" name)
      if(! member(libr ignoreLibrs) then
        Info[name]=name
        if(member(cell mosfets) then
          scale="1"
          if(ih->m scale=ih~>m)
          Info[name]=sprintf(nil "%-40s %5s x %5s/%s"
            Info[name] scale ih~>w ih~>l)
        )
      )
    )
    names=setof(element Info t)  ; array names Info
    names=sort(names 'alphalessp)
    ;-------------------------------------------------------------------------
    ; report header
    ;-------------------------------------------------------------------------
    report=strcat(RVBseparator("@" 55) "\n")
    report=strcat(report "Top-level Instances\n")
    report=strcat(report "Ignoring these libraries: " ignoreLibrsString "\n")
    report=strcat(report RVBseparator("@" 55) "\n")
    ;-------------------------------------------------------------------------
    ; instance name table
    ;-------------------------------------------------------------------------
    foreach(name names
      report=strcat(report Info[name] "\n")
    )
    return(report)
  )
)
;============================================================================
; RVBnetNames
; list net names in current cell view
;============================================================================
procedure(RVBnetNames()
  prog((
      cv nh name names lab Info Moni buf report th terminals
    )
    ;-------------------------------------------------------------------------
    ; schematic window must be open
    ;-------------------------------------------------------------------------
    cv=RVBgetCV()
    if(cv == nil then
      return("Schematic window not open")
    )
    ;-------------------------------------------------------------------------
    ; accumulate net info, then sort by names
    ;-------------------------------------------------------------------------
    terminals=cv~>terminals~>name
    Info=makeTable("info")
    foreach(nh cv~>nets
      name=nh~>name
      sprintf(buf "%-10s :" name)
      if(member(name terminals) then
        foreach(th cv~>terminals
          if(th~>name == name then
            sprintf(buf "%s [%s pin]" buf th~>direction)
          )
        )
      )
      foreach(lab nh~>figs~>theLabel
        if(lab then
          sprintf(buf "%s %s" buf lab)
        )
      )
      Info[name]=buf
    )
    names=setof(element Info t)  ; array names Info
    names=sort(names 'alphalessp)
    ;-------------------------------------------------------------------------
    ; report header
    ;-------------------------------------------------------------------------
    report=strcat(RVBseparator("@" 55) "\n")
    report=strcat(report "Top-level Nets\n")
    report=strcat(report RVBseparator("@" 55) "\n")
    report=strcat(report "Net Name:   Labels:\n")
    report=strcat(report RVBseparator("-" 55) "\n")
    ;-------------------------------------------------------------------------
    ; net names / labels:
    ;-------------------------------------------------------------------------
    foreach(name names
      report=strcat(report Info[name] "\n")
    )
    return(report)
  )
)
;============================================================================
; RVBpinNames
; list pin names in current cell view
;============================================================================
procedure(RVBpinNames()
  prog((
      cv nh name inputs outputs bidirs Inputs Outputs Bidirs report th
    )
    ;-------------------------------------------------------------------------
    ; schematic window must be open
    ;-------------------------------------------------------------------------
    cv=RVBgetCV()
    if(cv == nil then
      return("Schematic window not open")
    )
    ;-------------------------------------------------------------------------
    ; accumulate info, then sort by names
    ;-------------------------------------------------------------------------
    Inputs  = makeTable("inputs")
    Outputs = makeTable("outputs")
    Bidirs  = makeTable("bidirs")
    foreach(th cv~>terminals
      name = th~>name
      dir  = th->direction
      case(dir
        ("input"
          Inputs[name]  = 1
        )
        ("output"
          Outputs[name] = 1
        )
        ("inputOutput"
          Bidirs[name] = 1
        )
      )
    )
    inputs  = setof(element Inputs t)
    outputs = setof(element Outputs t)
    bidirs  = setof(element Bidirs t)
    inputs  = sort(inputs 'alphalessp)
    outputs = sort(outputs 'alphalessp)
    bidirs  = sort(bidirs 'alphalessp)
    ;-------------------------------------------------------------------------
    ; report header
    ;-------------------------------------------------------------------------
    report=strcat(RVBseparator("@" 55) "\n")
    report=strcat(report "I/O\n")
    report=strcat(report RVBseparator("@" 55) "\n")
    report=strcat(report "Pin:  I/O:\n")
    report=strcat(report RVBseparator("-" 55) "\n")
    ;-------------------------------------------------------------------------
    ; pin name / direction:
    ;-------------------------------------------------------------------------
    foreach(name inputs
      report=strcat(report name "\t" "Input" "\n")
    )
    foreach(name outputs
      report=strcat(report name "\t" "Output" "\n")
    )
    foreach(name bidirs
      report=strcat(report name "\t" "IOput" "\n")
    )
    return(report)
  )
)
;============================================================================
; RVBcellCount
; count of cells in current cell view
; if ftop: list toplevel only
;============================================================================
procedure(RVBcellCount(ftop)
  prog((cv Count name names buf report)
    ;-------------------------------------------------------------------------
    ; schematic window must be open
    ;-------------------------------------------------------------------------
    cv=RVBgetCV()
    if(cv == nil then
      return("Schematic window not open")
    )
    ;-------------------------------------------------------------------------
    ; count cells
    ;-------------------------------------------------------------------------
    Count=makeTable("count")
    RVBcellCountGo(cv Count ftop 1)
    names=setof(element Count t)  ; array names Count
    names=sort(names 'alphalessp)
    ;-------------------------------------------------------------------------
    ; report header
    ;-------------------------------------------------------------------------
    report=strcat(RVBseparator("@" 55) "\n")
    if(ftop then
      report=strcat(report "Top-level Cells\n")
    else
      report=strcat(report "All Cells\n")
    )
    report=strcat(report RVBseparator("@" 55) "\n")
    report=strcat(report "Cell Name:                     Number:\n")
    report=strcat(report RVBseparator("-" 55) "\n")
    ;-------------------------------------------------------------------------
    ; add cell count information
    ;-------------------------------------------------------------------------
    foreach(name names
      sprintf(buf "%-30s %d\n" name Count[name])
      report=strcat(report buf)
    )
    return(report)
  )
)
;============================================================================
; RVBcellCountGo
; NumInst = number of instances of this instance (bussed name)
;============================================================================
procedure(RVBcellCountGo(cv Count ftop NumInst)
  prog(
    (ih lib cel nam num n1 n2 buf cv_next)
    foreach(ih cv~>instances
      lib = ih~>libName
      cel = ih~>cellName
      nam = ih~>name
      num = 1
      ; bussed names:
      if(rexMatchp("<\\([0-9]+\\):\\([0-9]+\\)>$" nam) then
        n1=evalstring(rexSubstitute("\\1"))
        n2=evalstring(rexSubstitute("\\2"))
        num=abs(n2-n1)+1
      )
      num=NumInst*num
      buf = strcat(lib ":" cel)
      if(!exists(key Count strcmp(key buf) == 0) then
        Count[buf]=0
      )
      Count[buf]=Count[buf]+num
      if(!ftop then
        if(ih~>master then
          if(
            ih~>master~>cellViewType == "schematicSymbol" &&
            member("schematic" ih~>master~>cell~>views~>name)
          then
            cv_next = dbOpenCellViewByType(
              ih~>master~>libName
              ih~>master~>cellName
              '("schematic" "cmos.sch")
            )
            RVBcellCountGo(cv_next Count ftop num)
          )
        )
      )
    )
  )
)
;============================================================================
; RVBinfo
; report cells and nets in current cellview
; ftop=t:   print nets and (top) cells
; ftop=nil: print nets and (all) cells
;============================================================================
procedure(RVBinfo(ftop)
  fout=outfile("info.txt")
  fprintf(fout "%s" strcat(
    RVBnetNames()
    RVBcellCount(ftop)
    RVBinstNames()
    RVBpinNames()
  ))
  close(fout)
  bBox='((0 0) (540 800))          ; set view box size
  view("info.txt" bBox)            ; view the file
)
;============================================================================
; RVBcellLibChange
;============================================================================
procedure(RVBcellLibChange(lib1 lib2)
  prog((cv ih lib cel new_master cdfid callback)
    cv=RVBgetCV()
    if(cv == nil then
      return("Cell view window not open")
    )
    foreach(ih cv~>instances
      lib = ih~>libName
      cel = ih~>cellName
      if(lib == lib1 then
        printf("  %L:%L -> %L:%L\n" lib1 cel lib2 cel)
        if(cel == "rntb_3t" then
          cel = "rntub_3t"
        )
        new_master=dbOpenCellViewByType(ddGetObj(lib2) cel "symbol")
        if( new_master then
          ih~>master = new_master
        )
        ;----------------------------------------------------------------------
        ; vddOption callback:
        ;----------------------------------------------------------------------
        cdfid = cdfGetInstCDF(ih)
        if( cdfid != nil then
          callback=cdfid->vddOption->callback
          if( callback != nil then
            ; They use this global in the call back routines
            cdfgData = cdfid
            printf("  %L %L %L\n" ih~>name ih~>cellName callback)
            evalstring(callback)
          )
        )
      )
    )
    schCheck(cv)
    dbCheck(cv)   
    dbSave(cv)   
  )
)
;============================================================================
; RVBplot
;============================================================================
procedure(RVBplot(@key (top nil) (color t) (printcmd nil) (papersize "A"))
  prog(
    ( hlvl plotter res plotsize plotdir
      pwd cds_xlibrs libid libr libp libq locdir
      name view cell bbox psfile
      cellspecs cellspec pagespecs pagespec pages page cpage
    )
    ;-------------------------------------------------------------------------
    ; map input parameters
    ;-------------------------------------------------------------------------
    if(top then
      hlvl = 0
    else
      hlvl = nil
    )
    if(color then
      plotter  = "color_lp"
    else
      plotter  = "lp_def"
    )
    res = 300 ; "lp_def" or "color_lp"
    case(papersize
      ("A" xy = list(2400.0 3150.0 75.0 75.0))
      ("B" xy = list(3150.0 4950.0 75.0 75.0))
    )
    plotsize = list((nth(0 xy) / res ) (nth(1 xy) / res))
    plotdir="plots"
    ;-------------------------------------------------------------------------
    ; find all cds.lib entries which are not in this directory
    ;-------------------------------------------------------------------------
    ddUpdateLibList()
    pwd = simplifyFilename(getWorkingDir())
    cds_xlibrs = nil
    foreach( libid ddGetLibList()
      libr=libid~>name
      libp=libid~>readPath
      libq=libid~>writePath
      locdir = strcat(pwd "/" libr)
      if( libp != locdir || libq != locdir then
        cds_xlibrs = append(cds_xlibrs list(libr))
      )
    )
;print every schematic everywhere, black and white:
;cds_xlibrs=nil
;plotter="lp_def"
    ;-------------------------------------------------------------------------
    ; get specification list of all cell pages to print
    ; LuGetHier is in "plot.il"
    ;-------------------------------------------------------------------------
    cellspecs=LuGetHier(
      ?viewlst list("schematic")
      ?ignore cds_xlibrs
      ?hlvl hlvl
    )
    ;-------------------------------------------------------------------------
    ; if plot subdirectory is not available, create it
    ;-------------------------------------------------------------------------
    if( !isDir(plotdir) then
      system(strcat("/bin/mkdir " plotdir))
    else
      system(strcat("/bin/rm " plotdir "/" "*.ps"))
    )
    ;-------------------------------------------------------------------------
    ; print each page of each cell
    ;-------------------------------------------------------------------------
    foreach(cellspec cellspecs
      name=parseString(nth(0 cellspec) "/")
      view=nth(2 name)
      cell=nth(1 name)
      libr=nth(0 name)
      pagespecs=nth(1 cellspec)
      pages=nil
      foreach(pagespec pagespecs
        page  = nth(0 pagespec)
        pages = append(pages list(atoi(page)))
      )
      pages=sort(pages 'lessp)
      foreach(page pages
        sprintf(cpage "%d" page)
        bbox=nth(1 assoc(cpage pagespecs))
        if(length(pages) > 1 then
          psfile=sprintf(nil "%s/%s.%s.ps" plotdir cell cpage)
        else
          psfile=sprintf(nil "%s/%s.ps"    plotdir cell)
        )
        schPlotOptions = list(nil
          'hierarchy       nil
          'hierleveldown   0
          'area            "select"
          'bBox            bbox
          'multisheet      nil
          'view            view
          'cell            cell
          'library         libr
          'plot            "cellview"
          'noteText        ""
          'grid            nil
          'indexsheet      t
          'notes           nil
          'header          nil
          'plotToFile      t
          'mailto          ""
          'papersize       papersize
          'plotter         plotter
          'display         "display"
          'outputfile      psfile
          'time            "now"
          'tmpdir          "/tmp"
          'copy            1
          'plotsize        plotsize
          'unit            "inches"            
          'center          nil
          'mail            nil
          'orientation     "automatic"
          'offset          '(0.0 0.0)
        )
        if(nil then
          println(cdr(schPlotOptions))
        )
        schPlot()
      )
    )
    if(printcmd then
      system(strcat(printcmd " " plotdir "/" "*.ps"))
    )
    return(t)
  )
)
;=============================================================================
; NAME    : RVBfinger
; PURPOSE : convert MOSFET fingers to multiplier, and vice versa
; AUTHOR  : Richard Booth
; DATE    : Thu Dec 20 11:01:03 EST 2001
; ---------------------------------------------------------------------------
; NOTES :
;   * if  fingered, convert m to fingers
;   * if !fingered, convert nf to m
;=============================================================================
procedure(RVBfinger(@optional (fingered nil))
  prog(
    (cv mosfets lib cel cdfid s w0 n0 m0 s0 t0 f0 w1 n1 m1 s1 t1 f1 callback)
    mosfets=parseString("nmos nmos_4t pmos pmos_4t")
    ;-------------------------------------------------------------------------
    ; schematic window must be open
    ;-------------------------------------------------------------------------
    cv=RVBgetCV()
    if(cv == nil then
      return("Schematic window not open")
    )
    ;-------------------------------------------------------------------------
    ; go through mosfet instances and fix properties
    ;-------------------------------------------------------------------------
    foreach(ih cv~>instances
      lib = ih~>libName
      cel = ih~>cellName
      if( member(cel mosfets) then
        RVBfingerFix(ih fingered)
        cdfid = cdfGetInstCDF(ih)
        callback=cdfid->vddOption->callback
        if( callback != nil then
          cdfgData = cdfid
          evalstring(callback)
        )
      )
    )
    schCheck(cv)
    dbCheck(cv)   
    dbSave(cv)   
    return()
  )
)
;=============================================================================
; NAME    : RVBfingerLibs
; PURPOSE : convert all cells in library list
;             MOSFET fingers to multiplier, and vice versa
; AUTHOR  : Richard Booth
; DATE    : Thu Dec 20 11:01:03 EST 2001
; ---------------------------------------------------------------------------
; NOTES :
;   * libs is a string of library names
;   * if  fingered, convert m to fingers
;   * if !fingered, convert nf to m
;=============================================================================
procedure(RVBfingerLibs(libs @optional (fingered nil))
  prog(
    (cv mosfets cell libId lib cel cdfid callback)
    mosfets=parseString("nmos nmos_4t pmos pmos_4t")

    foreach(library parseString(libs)
      libId = ddGetObj(library)
      foreach(cell libId~>cells
        if(cv=dbOpenCellViewByType(libId cell~>name "schematic" nil "a") then
          foreach(ih cv~>instances
            lib = ih~>libName
            cel = ih~>cellName
            if( member(cel mosfets) then
              RVBfingerFix(ih fingered)
              cdfid = cdfGetInstCDF(ih)
              callback=cdfid->vddOption->callback
              if( callback != nil then
                cdfgData = cdfid
                evalstring(callback)
              )
            )
          )
          schCheck(cv)
          dbCheck(cv)   
          dbSave(cv)   
        )
      )
    )
    return()
  )
)
;=============================================================================
; NAME    : RVBfingerFix
; PURPOSE : convert MOSFET finger to multiplier, and vice versa
; AUTHOR  : Richard Booth
; DATE    : Thu Dec 20 11:01:03 EST 2001
; ---------------------------------------------------------------------------
; NOTES :
;   * ih is the instance handler, must be a mosfet
;   * if  fingered, convert m to fingers
;   * if !fingered, convert nf to m
;   * returns t if a conversion was done
;=============================================================================
procedure(RVBfingerFix(ih fingered)
  prog(
    (cdfid s w0 n0 m0 s0 t0 f0 w1 n1 m1 s1 t1 f1)
    ;-------------------------------------------------------------------------
    ; get original properties
    ;-------------------------------------------------------------------------
    w0 = ih~>W
    m0 = ih~>m
    n0 = ih~>numFingers
    s0 = ih~>modelStyle
    t0 = ih~>threshold
    f0 = ih~>asymRatioSpec
    ; printf("%s::%s w=%L nf=%L m=%L style=%L threshold=%L fingers=%L\n"
    ;   ih~>cellName ih~>name w0 m0 n0 s0 t0 f0)
    ;-------------------------------------------------------------------------
    ; string to number conversion
    ;-------------------------------------------------------------------------
    if(w0 then
      w0=atof(w0)
    else
      w0=1.0
    )
    if(m0 then
      m0=atoi(m0)
    else
      m0=1
    )
    if(n0 then
      n0=atoi(n0)
    else
      n0=1
    )
    if(!w0 return(nil))
    if(!m0 return(nil))
    if(!n0 return(nil))
    ;-------------------------------------------------------------------------
    ; conversion
    ;-------------------------------------------------------------------------
    if(fingered then
      w1 = m0 * w0
      n1 = m0 * n0
      m1 = 1
      s1 = "Post_Layout"
      t1 = w0
    else
      w1 = w0 / n0
      m1 = m0 * n0
      n1 = 1
      s1 = "Pre_Layout"
      t1 = 9999.0
    )
    ;-------------------------------------------------------------------------
    ; create list of finger widths
    ;-------------------------------------------------------------------------
    f1 = ""
    for(i 1 n1
      sprintf(f1 "%g " w1)
    )
    ;-------------------------------------------------------------------------
    ; modify properties
    ;-------------------------------------------------------------------------
    if(w1 != w0 || n1 != n0 || m1 != m0 || s1 != s0 then
      printf("%s::%s " ih~>cellName ih~>name)
      printf("    w=%L nf=%L m=%L style=%L"   w0 n0 m0 s0)
      printf(" -> w=%L nf=%L m=%L style=%L\n" w1 n1 m1 s1)
      dbReplaceProp(ih "modelStyle"     "string" s1)
      dbReplaceProp(ih "asymRatioSpec"  "string" f1)
      sprintf(s "%g" t1)
      dbReplaceProp(ih "threshold"      "string" s)
      sprintf(s "%g" w1)
      dbReplaceProp(ih "W"              "string" s)
      sprintf(s "%d" n1)
      dbReplaceProp(ih "numFingers"     "string" s)
      sprintf(s "%d" m1)
      dbReplaceProp(ih "m"              "string" s)
      return(t)
    )
    return(nil)
  )
)
;=============================================================================
; RVBenableSnapSpacing()
; Enable the snap spacing stuff 
; Has to be done manually after everything is loaded.
;=============================================================================
procedure(RVBenableSnapSpacing()
  prog(()
    hiiSetCurrentForm('schDisplayOptionsForm)
    hiSetFieldEditable( schDisplayOptionsForm->snapSpacing t )
    hiSetFieldEditable( schDisplayOptionsForm->gridMultiple t )
    hiSetFieldEditable( schDisplayOptionsForm->gridSpacing t )
    hiFormDone(schDisplayOptionsForm)
  )
)
