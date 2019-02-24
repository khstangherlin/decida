procedure(RVBschMenu()
  hiCreatePulldownMenu(
    'RVBschMenu ; menu handle
    "-- RVB --"       ; menu title
    list(
      hiCreateMenuItem(
        ?name           'RVBdcd
        ?itemText       "Generate DeCiDa testpack"
        ?callback       "RVBdcdForm()"
      )
      hiCreateMenuItem(
        ?name           'RVBvlog
        ?itemText       "Generate verilog testbench"
        ?callback       "RVBvtbForm()"
      )
      hiCreateMenuItem(
        ?name           'TopCellsAndNets
        ?itemText       "List (top) cells and nets"
        ?callback       "RVBinfo(t)"
      )
      hiCreateMenuItem(
        ?name           'AllCellsAndNets
        ?itemText       "List (all) cells and nets"
        ?callback       "RVBinfo(nil)"
      )
      hiCreateMenuItem(
        ?name           'ListComponentsCell
        ?itemText       "List tree of (cell-by-cell) unique component cells"
        ?callback       "RVBcomp(?unique nil)"
      )
      hiCreateMenuItem(
        ?name           'ListComponentsGlob
        ?itemText       "List tree of (globally) unique component cells"
        ?callback       "RVBcomp(?unique t)"
      )
      hiCreateMenuItem(
        ?name           'RVBCopy
        ?itemText       "Copy Multiple"
        ?callback       "schHiCopy(t)"
      )
      hiCreateMenuItem(
        ?name           'InstanceProperties
        ?itemText       "Instance Properties"
        ?callback       "RVBinstProps()"
      )
      hiCreateMenuItem(
        ?name           'EnableSnapSpacing
        ?itemText       "Enable Snap Spacing"
        ?callback       "RVBenableSnapSpacing()"
      )
    )
  )
)

hiSetBindKey(
  "Schematics"     ; which viewtype to bind to
  "<Key>y"         ; bindKey
  "hiInsertBannerMenu(  
    hiGetCurrentWindow()
    RVBschMenu()
    12
  )"
)
