;##############################################################################
; NAME: RVBcomp.il
; PURPOSE: shows tree of unique component cells
; DATE:    Wed Mar 24 10:25:24 EDT 2010
; AUTHOR:  rvb
; ----------------------------------------------------------------------------
; ARGUMENTS (keyword):
;   unique
;     if t, only list globally unique cells
;     (useful for list of unique cells to extract from a netlist)
;   ignore
;     string containing list of libraries to ignore
; EXAMPLE-CALL:
;   RVBcomp(?unique t ?ignore "cs200a_devices poly_hs_tw") 
;
;##############################################################################
;============================================================================
; RVBcomp
;============================================================================
procedure(RVBcomp(@key (unique nil) (ignore ""))
  prog((cv buf fout items lib cell bBox)
    ;-------------------------------------------------------------------------
    ; schematic window must be open
    ;-------------------------------------------------------------------------
    cv=RVBgetCV()
    if(cv == nil then
      return("Schematic window not open")
    )
    ;-------------------------------------------------------------------------
    ; initialize globals
    ;-------------------------------------------------------------------------
    RVBcomp_list=nil        ;# list of depth, component
    RVBcomp_depth=0         ;# current hierarchy depth
    RVBcomp_unique=unique   ;# if t, print only unique list of cells
    RVBcomp_unique_list=nil ;# list of globally unique cells
    ignore = strcat("basic sheets " ignore)
    RVBcomp_ignore=list=parseString(ignore) ;# list of libraries to ignore
    RVBcompGo(cv)
    ;-------------------------------------------------------------------------
    ; show results
    ;-------------------------------------------------------------------------
    fout=outfile("info.txt")
    fprintf(fout "# %s\n" RVBseparator("=" 72))
    fprintf(fout "# %s\n" "components of current schematic")
    fprintf(fout "#\n")
    if(RVBcomp_unique then
      fprintf(fout "# %s\n" "only globally unique component cells are shown")
    else
      fprintf(fout "# %s\n" "unique components for each cell are shown")
    )
    fprintf(fout "# ignored libraries: %s\n" ignore)
    fprintf(fout "#\n")
    fprintf(fout "# example command-line procedure call:\n")
    fprintf(fout "#    RVBcomp(?unique t ?ignore \"cs200a_devices poly_hs\")\n")
    fprintf(fout "#\n")
    fprintf(fout "# cell:                                            library:\n")
    fprintf(fout "# %s\n" RVBseparator("=" 72))
    foreach(line RVBcomp_list
      buf=RVBseparator("    " nth(0 line))
      items = parseString(nth(1 line) ":")
      lib = nth(0 items)
      cell= nth(1 items)
      fprintf(fout "%-50s %s\n" strcat(buf cell) lib)
    )
    close(fout)
    bBox='((0 0) (540 800))          ; set view box size
    view("info.txt" bBox)            ; view the file
  )
)
;============================================================================
; RVBcompGo
;============================================================================
procedure(RVBcompGo(cv)
  prog(
    (ih lib cel nam buf item _cell_unique_list cv_next)
    _cell_unique_list = nil
    foreach(ih cv~>instances
      lib = ih~>libName
      cel = ih~>cellName
      nam = ih~>name
      buf = strcat(lib ":" cel)
      if(
        !member(lib RVBcomp_ignore) &&
        !member(buf _cell_unique_list) && 
       (!member(buf RVBcomp_unique_list) || !RVBcomp_unique)
      then
        _cell_unique_list   = append(_cell_unique_list   list(buf))
        RVBcomp_unique_list = append(RVBcomp_unique_list list(buf))
        item = list(RVBcomp_depth buf)
        RVBcomp_list = append(RVBcomp_list list(item))
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
            RVBcomp_depth = RVBcomp_depth + 1
            RVBcompGo(cv_next)
            RVBcomp_depth = RVBcomp_depth - 1
          )
        )
      )
    )
  )
)
