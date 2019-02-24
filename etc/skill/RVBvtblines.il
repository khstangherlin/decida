;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
; PROC: RVBvtbFormProjCB
; PURPOSE: Project choice form call-back
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
procedure( RVBvtbFormProjCB()
    prog(()
        RVBproject=RVBvtbAppForm~>vtbProj~>value
    )
)
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
; PROC: RVBvtbFormTechCB
; PURPOSE: Technology choice form call-back
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
procedure( RVBvtbFormTechCB()
    prog(()
        RVBtechnology=RVBvtbAppForm~>vtbTech~>value
    )
)
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
; PROC: RVBvtbFormRealCB
; PURPOSE: wreals choice form call-back
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
procedure( RVBvtbFormRealCB()
    prog(()
        RVBwreals=parseString(RVBvtbAppForm~>vtbReal~>value)
    )
)
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
; PROC: RVBvtbForm
; PURPOSE: main verilog testbench generation form
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
procedure( RVBvtbForm()
    prog(
        (fields promptWidth xmin xmax ypos proj tech
            projprompt techprompt
            projects techs help_file
            realprompt
        )
        ;----------------------------------------------------------------------
        ; location specific
        ;----------------------------------------------------------------------
        projects   = list("bird", "trane")
        techs      = list("ptm_130nm" "ptm_45nm")
        help_file  = simplifyFilename("~/.DeCiDa/skill/RVBvtb_help.txt")
        ;----------------------------------------------------------------------
        ; try to get RVBproject RVBtechnology from PROJECT
        ; if the parameters are already set in .cdsinit, use those values
        ;----------------------------------------------------------------------
        proj = RVBgetenv("PROJECT")
        case( proj
            (("bird")
                tech="ptm_130nm"
            )
            (("trane")
                tech="ptm_45nm"
            )
            (t
                proj="trane"
                tech="ptm_45nm"
            )
        )
        if(!boundp('RVBproject)    || !RVBproject    || \
            !member(RVBproject    projects)   RVBproject    = proj)
        if(!boundp('RVBtechnology) || !RVBtechnology || \
            !member(RVBtechnology techs)      RVBtechnology = tech)
        RVBwreals = list()
        ;----------------------------------------------------------------------
        ; form prompts
        ;----------------------------------------------------------------------
        projprompt = "project:"
        techprompt = "technology:"
        realprompt = "wreals:"
        promptWidth = max(
            hiGetTextWidth( hiGetFont("label") projprompt)
            hiGetTextWidth( hiGetFont("label") techprompt)
            hiGetTextWidth( hiGetFont("label") realprompt)
        ) + 20
        ;----------------------------------------------------------------------
        ; form fields
        ;----------------------------------------------------------------------
        xmin = 10
        xmax = 10 + promptWidth + 100
        ypos = 0
        fields = list(
            list(
                hiCreateRadioField(
                    ?name 'vtbProj
                    ?prompt projprompt
                    ?callback '("RVBvtbFormProjCB()" )
                    ?choices projects
                    ?defValue RVBproject
                )
                xmin:ypos*hicLineHeight xmax:(++ypos)*hicLineHeight promptWidth
            )
            list(
                hiCreateRadioField(
                    ?name 'vtbTech
                    ?prompt techprompt
                    ?callback '("RVBvtbFormTechCB()" )
                    ?choices techs
                    ?defValue RVBtechnology
                )
                xmin:ypos*hicLineHeight xmax:(++ypos)*hicLineHeight promptWidth
            )
            list(
                hiCreateStringField(
                    ?name 'vtbReal
                    ?prompt realprompt
                    ?callback "RVBvtbFormRealCB()"
                    ?defValue ""
                )
                xmin:ypos*hicLineHeight xmax:(++ypos)*hicLineHeight promptWidth
            )
        )
        ;----------------------------------------------------------------------
        ; create form
        ;----------------------------------------------------------------------
        cmd = strcat("view(\"" help_file "\")")
        hiCreateAppForm(
            ?name          'RVBvtbAppForm
            ?formTitle     "Verilog TestBench"
            ?fields        fields
            ?callback      '("RVBvtblines()" "")
            ?buttonLayout  '(
                OKCancelApply
                (VTBHelp cmd)
            )
        )
        hiDisplayForm('RVBvtbAppForm)
    )
)
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
; PROC: RVBvtbProjPars
; PURPOSE: find projmnt
;     from user, proj, tech
; NOTES: 
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
procedure( RVBvtbProjPars(user proj tech)
    prog(()
        ;----------------------------------------------------------------------
        ; project mount:
        ;----------------------------------------------------------------------
        case( proj
            (("bird")
                projmnt = simplifyFilename("~/.DeCiDa/projects")
            )
            (("trane")
                projmnt = simplifyFilename("~/.DeCiDa/projects")
            )
            (t
                projmnt = simplifyFilename("~/.DeCiDa/projects")
            )
        )
        return(list(projmnt))
    )
)
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
; PROC: RVBvtblines
; PURPOSE: get verilog testbench lines for current cellview
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
procedure(RVBvtblines()
    prog(
        ( cv nh ih buf i sbus1 sbus2 bus1 bus2 root user home date
          val report fout outfileName
          circuit buss nbits yparbuf
          analogLibVsrcs analogLibIsrcs supply1_nets supply0_nets
          net     nets     Nets
          ipin    ipins    IPins
          vsrcsig vsrcsigs VsrcSigs
          isrcsig isrcsigs IsrcSigs
          vsrcbus vsrcbuss VsrcBuss
          isrcbus isrcbuss IsrcBuss
          reg_lines real_lines supply1_lines supply0_lines
          signal_lines plot_signal_lines
          vtbLines tclLines sv_Lines makLines
          vtbDir vtbFile tclFile sv_File genFile makFile tptDir cktFile
          _DATE _USER _TESTBENCH _CIRCUIT _TECH _PROJECT
          _PROJMNT _VTBFILE _TCLFILE _SV_FILE _MAKFILE
        )
        ;--------------------------------------------------------------------
        ; list of analogLib sources and nets identified as supply1/0
        ;--------------------------------------------------------------------
        analogLibVsrcs=parseString("vdc vexp vpulse vpwl vpwlf vsin")
        analogLibIsrcs=parseString("idc iexp ipulse ipwl ipwlf isin")
        supply1_nets = parseString("VDD VDD09 VDD33 VDD18")
        supply0_nets = parseString("VSS BP BN")
        ;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        ; global parameter information
        ;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        ;--------------------------------------------------------------------
        ; user, home, date
        ; home is where the script is written
        ;--------------------------------------------------------------------
        user=RVBgetenv("USER")
        home=RVBgetenv("HOME")
        date=getCurrentTime()
        if(!boundp('user) || !user then
            user = "whoami"
        )
        if(!boundp('home) || !home then
            home = simplifyFilename("~")
        )
        ;--------------------------------------------------------------------
        ; RVBvtbForm sets:
        ;     RVBproject, RVBtechnology, RVBwreals
        ; RVBvtbProjPars used to set:
        ;     projmnt
        ;--------------------------------------------------------------------
        pars = RVBvtbProjPars(user RVBproject RVBtechnology)
        projmnt = nth(0 pars)
        ;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        ; accumulate information from the test-bench schematic
        ;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        ;---------------------------------------------------------------------
        ; schematic window must be open
        ;---------------------------------------------------------------------
        cv=RVBgetCV()
        if(cv == nil then
            return("Schematic window not open")
        )
        ;---------------------------------------------------------------------
        ; accumulation tables
        ;---------------------------------------------------------------------
        Nets      = makeTable("nets")
        IsrcSigs  = makeTable("isrcsigs")
        IsrcBuss  = makeTable("isrcbuss")
        VsrcSigs  = makeTable("vsrcsigs")
        VsrcBuss  = makeTable("vsrcbuss")
        InstCell  = makeTable("instcell")
        InstPorts = makeTable("instports")
        ;---------------------------------------------------------------------
        ; accumulate nets
        ; don't save <*x>node
        ;---------------------------------------------------------------------
        foreach(nh cv~>nets
            name=nh~>name
            if(rexMatchp("^<" name) || name == "gnd!" then
            else
                Nets[name] = 1
            )
        )
        ;---------------------------------------------------------------------
        ; accumulate instance parameters
        ;---------------------------------------------------------------------
        foreach(ih cv~>instances
            name=ih~>name
            libr=ih~>libName
            cell=ih~>cellName
            ports = ih~>instTerms
            ;...................................................................
            ; current sources and voltage sources
            ;...................................................................
            if(libr == "analogLib" then
                if(member(cell analogLibIsrcs) then
                    foreach(port ports
                        port_name = port~>name
                        if( strcmp(port_name "MINUS") == 0 then
                            port_net  = port~>net~>name
                            if(rexMatchp("^\\(.+\\)<\\([0-9]+\\):\\([0-9]+\\)>$" port_net) then
                                root=rexSubstitute("\\1")
                                sbus1=rexSubstitute("\\2")
                                sbus2=rexSubstitute("\\3")
                                IsrcBuss[name] = list(root sbus1 sbus2)
                            else
                                IsrcSigs[name] = port_net
                            )
                        )
                    )
                )
                if(member(cell analogLibVsrcs) then
                    foreach(port ports
                        port_name = port~>name
                        if( strcmp(port_name "PLUS") == 0 then
                            port_net  = port~>net~>name
                            if(rexMatchp("^\\(.+\\)<\\([0-9]+\\):\\([0-9]+\\)>$" port_net) then
                                root=rexSubstitute("\\1")
                                sbus1=rexSubstitute("\\2")
                                sbus2=rexSubstitute("\\3")
                                VsrcBuss[name] = list(root sbus1 sbus2)
                            else
                                VsrcSigs[name] = port_net
                            )
                        )
                    )
                )
            ;...................................................................
            ; other libraries
            ;...................................................................
            else
                if(!member(libr list("US_8ths" "basic")) then
                    port_list = list()
                    foreach(port ports
                        port_name = port~>name
                        port_net  = port~>net~>name
                        port_dir  = port~>direction
                        port_bus1 = ""
                        port_bus2 = ""
                        if(rexMatchp("^\\(.+\\)<\\([0-9]+\\):\\([0-9]+\\)>$" port_name) then
                            port_name=rexSubstitute("\\1")
                            port_bus1=rexSubstitute("\\2")
                            port_bus2=rexSubstitute("\\3")
                        )
                        if(rexMatchp("^\\(.+\\)<\\([0-9]+\\):\\([0-9]+\\)>$" port_net) then
                            port_net=rexSubstitute("\\1")
                        )
                        port_list = append(port_list list(list(port_name port_net port_dir port_bus1 port_bus2)))
                    )
                    InstCell[name]  = cell
                    InstPorts[name] = port_list
                )
            )
        )
        ;---------------------------------------------------------------------
        ; sort nets, srcs
        ;---------------------------------------------------------------------
        nets     = setof(element Nets t)
        nets     = sort(nets     'alphalessp)
        ipins    = setof(element IPins t)
        ipins    = sort(ipins    'alphalessp)
        vsrcbuss = setof(element VsrcBuss t)
        vsrcbuss = sort(vsrcbuss 'alphalessp)
        vsrcsigs = setof(element VsrcSigs t)
        vsrcsigs = sort(vsrcsigs 'alphalessp)
        isrcbuss = setof(element IsrcBuss t)
        isrcbuss = sort(isrcbuss 'alphalessp)
        isrcsigs = setof(element IsrcSigs t)
        isrcsigs = sort(isrcsigs 'alphalessp)
        insts    = setof(element InstPorts t)
        insts    = sort(insts    'alphalessp)
        ;---------------------------------------------------------------------
        ; regs and reals
        ;---------------------------------------------------------------------
        reg_lines     = ""
        real_lines    = ""
        supply1_lines = ""
        supply0_lines = ""
        init_lines    = ""
        used_nets     = list()
        if(isrcsigs then
            foreach(isrcsig isrcsigs
                net = IsrcSigs[isrcsig]
                if((!member(net supply1_nets) && !member(net supply0_nets)) then
                    real_lines=strcat(real_lines "    wreal      " net ";\n")
                    used_nets = append(used_nets list(net))
                )
            )
        )
        if(isrcbuss then
            foreach(isrcbus isrcbuss
                root  = nth(0 IsrcBuss[isrcbus])
                sbus1 = nth(1 IsrcBuss[isrcbus])
                sbus2 = nth(2 IsrcBuss[isrcbus])
                net   = strcat(root "<" sbus1 ":" sbus2 ">")
                real_lines=strcat(real_lines "    // the following must be bit-blasted:\n")
                real_lines=strcat(real_lines "    wreal [" sbus1 ":" sbus2 "] " root ";\n")
                used_nets = append(used_nets list(net))
            )
        )
        if(vsrcsigs then
            foreach(vsrcsig vsrcsigs
                net = VsrcSigs[vsrcsig]
                if(member(net supply1_nets) then
                    supply1_lines=strcat(supply1_lines "    supply1   " net ";\n")
                    used_nets = append(used_nets list(net))
                else
                    if(member(net supply0_nets) then
                        supply0_lines=strcat(supply0_lines "    supply0   " net ";\n")
                        used_nets = append(used_nets list(net))
                    else
                        reg_lines=strcat(reg_lines "    reg       " net ";\n")
                        init_lines = strcat(init_lines "        " net " = 0;\n")
                        used_nets = append(used_nets list(net))
                    )
                )
            )
        )
        if(vsrcbuss then
            foreach(vsrcbus vsrcbuss
                root  = nth(0 VsrcBuss[vsrcbus])
                sbus1 = nth(1 VsrcBuss[vsrcbus])
                sbus2 = nth(2 VsrcBuss[vsrcbus])
                net   = strcat(root "<" sbus1 ":" sbus2 ">")
                reg_lines=strcat(reg_lines "    reg [" sbus1 ":" sbus2 "] " root ";\n")
                used_nets = append(used_nets list(net))
                bus1 = atoi(sbus1)
                bus2 = atoi(sbus2)
                nbits = abs(bus1 - bus2) + 1
                sprintf(val "%d'd0" nbits)
                init_lines = strcat(init_lines "        " root " = " val ";\n")
            )
        )
        ;---------------------------------------------------------------------
        ; dut instances
        ;---------------------------------------------------------------------
        inst_lines = ""
        foreach(inst insts
           inst_cell = InstCell[inst]
           port_list = list()
           foreach(item InstPorts[inst]
               port  = nth(0 item)
               net   = nth(1 item)
               dir   = nth(2 item)
               sbus1 = nth(3 item)
               sbus2 = nth(4 item)
               if(rexMatchp("^\\(<\\*[0-9]+>\\)\\(.+\\)$" net) then
                   mult= rexSubstitute("\\1")
                   net = rexSubstitute("\\2")
               )
               port_list = append(port_list
                   list(strcat("        ." port "(" net ")"))
               )
           )
           ;------------------------------------------------------------------
           ; a bus instance
           ;------------------------------------------------------------------
           if(rexMatchp("^\\(.+\\)<\\([0-9]+\\):\\([0-9]+\\)>$" inst) then
               root=rexSubstitute("\\1")
               sbus1=rexSubstitute("\\2")
               sbus2=rexSubstitute("\\3")
               bus1 = atoi(sbus1)
               bus2 = atoi(sbus2)
               if(bus2 < bus1 then
                   i = bus2
                   bus2 = bus1
                   bus1 = i
               )
               inst_lines = strcat(inst_lines
                   "    //" RVBseparator("~" 50) "\n"
                   "    // the following bus instances probably need port adjustments:\n" 
                   "    //" RVBseparator("~" 50) "\n"
               )
               if(nil then
                   for(i bus1 bus2
                       sprintf(buf "%s__%d" root i)
                       inst_lines = strcat(inst_lines
                           "    " inst_cell " " buf "(\n"
                           buildString(port_list ",\n") "\n"
                           "    );\n"
                       )
                   )
               else
                   inst_lines = strcat(inst_lines
                       "    " inst_cell " " root "[" bus2 ":" bus1 "] (\n"
                       buildString(port_list ",\n") "\n"
                       "    );\n"
                   )
               )
           ;------------------------------------------------------------------
           ; a non-bus instance
           ;------------------------------------------------------------------
           else
               inst_lines = strcat(inst_lines
                   "    " inst_cell " " inst "(\n"
                   buildString(port_list ",\n") "\n"
                   "    );\n"
               )
           )
        )
        ;---------------------------------------------------------------------
        ; signals
        ;---------------------------------------------------------------------
        signal_lines  = ""
        foreach(net nets
            if(member(net supply1_nets) || member(net supply0_nets) || member(net used_nets) then
            else
                if(rexMatchp("^\\(.+\\)<\\([0-9]+\\):\\([0-9]+\\)>$" net) then
                    root=rexSubstitute("\\1")
                    sbus1=rexSubstitute("\\2")
                    sbus2=rexSubstitute("\\3")
                    signal_lines = strcat(signal_lines "    wire [" sbus1 ":" sbus2 "] " root ";\n")
                else
                    if( member(net RVBwreals) then
                        signal_lines = strcat(signal_lines "    wreal " net ";\n")
                    else
                        signal_lines = strcat(signal_lines "    wire "  net ";\n")
                    )
                )
            )
        )
        plot_signal_lines  = ""
        foreach(net nets
            if(rexMatchp("^\\(.+\\)<\\([0-9]+\\):\\([0-9]+\\)>$" net) then
                net=rexSubstitute("\\1")
            )
            if( member(net RVBwreals) then
                plot_signal_lines = strcat(plot_signal_lines "    " net ":^" "\n")
            else
                plot_signal_lines = strcat(plot_signal_lines "    " net "\n")
            )
        )
        ;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        ; verilog testbench
        ;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        testbench = cv->cell->name
        circuit   = cv->cell->name
        if(rexMatchp("^test_\\(.+\\)$" circuit) then
            circuit = rexSubstitute("\\1")
        )
        if(rexMatchp("^tb_\\(.+\\)$" circuit) then
            circuit = rexSubstitute("\\1")
        )
        _DATE      = date
        _USER      = user
        _TESTBENCH = testbench
        _CIRCUIT   = circuit
        _TECH      = RVBtechnology
        _PROJECT   = RVBproject
        _PROJMNT   = projmnt
        _VTBFILE   = strcat(testbench ".v")
        _TCLFILE   = strcat(testbench ".ntcl")
        _SV_FILE   = strcat(testbench ".sv")
        _MAKFILE   = "Makefile"
        vtbLines = strcat(
            "//"  RVBseparator("#" 78) "\n"
            "// NAME:    " _VTBFILE "\n"
            "// PURPOSE: verilog testbench for " _CIRCUIT "\n"
            "// DATE:    " _DATE "\n"
            "// AUTHOR:  " _USER "\n"
            "//" RVBseparator("-" 77) "\n"
            "// NOTES:\n"
            "//   * define parameters:\n"
            "//     these can be defined in this file or by using the vlog compiler\n"
            "//     +define command-line-option (ex: +define+ANALOG +define+CASE=0)\n"
            "//     __WREAL__ : enable wreals in analog functional blocks\n"
            "//"  RVBseparator("#" 78) "\n"
            "`timescale 10ps / 100fs\n"
            "`define TIMESCALE 10e-12\n"
            "`define __WREAL__\n"
            "module " _TESTBENCH "();\n"
            "    //" RVBseparator("-" 72) "\n"
            "    // inputs: \n"
            "    //" RVBseparator("-" 72) "\n"
            reg_lines
            real_lines
            "    //" RVBseparator("-" 72) "\n"
            "    // signals: \n"
            "    //" RVBseparator("-" 72) "\n"
            signal_lines
            "    //" RVBseparator("-" 72) "\n"
            "    // supply: \n"
            "    //" RVBseparator("-" 72) "\n"
            supply1_lines
            supply0_lines
            "    //" RVBseparator("-" 72) "\n"
            "    // resources: \n"
            "    //" RVBseparator("-" 72) "\n"
            "    real rtime, fclk, pclk, dclk;\n"
            "    real pi = 3.1415926535;\n"
            "    integer i, j, k, ifile;\n"
            "    //" RVBseparator("-" 72) "\n"
            "    // DUT: \n"
            "    //" RVBseparator("-" 72) "\n"
            inst_lines
            "    //" RVBseparator("-" 72) "\n"
            "    // clock:\n"
            "    //" RVBseparator("-" 72) "\n"
            "    // always begin \n"
            "    //     #(dclk) CLK = ~CLK;\n"
            "    // end\n"
            "    //" RVBseparator("-" 72) "\n"
            "    // test-sequence: \n"
            "    //" RVBseparator("-" 72) "\n"
            "    initial begin\n"
            "        //" RVBseparator("-" 68) "\n"
            "        // default inputs: \n"
            "        //" RVBseparator("-" 68) "\n"
            init_lines
            "        //" RVBseparator("-" 68) "\n"
            "        // input overrides: \n"
            "        //" RVBseparator("-" 68) "\n"
            "        fclk = 100e6;\n"
            "        pclk = 1.0/fclk;\n"
            "        dclk = (0.5*pclk)/`TIMESCALE;\n"
            "        //" RVBseparator("-" 68) "\n"
            "        // test-sequence body: \n"
            "        //" RVBseparator("-" 68) "\n"
            "        // CLK  = 0;\n"
            "        // CDN  = 1; #10 CDN = 0; #10 CDN=1;\n"
            "        #1000000;\n"
            "        $stop;\n"
            "    end\n"
            "endmodule\n"
        )
        tclLines = strcat(
            RVBseparator("#" 78) "\n"
            "# NAME    : " _TCLFILE "\n"
            "# PURPOSE : tcl macro for ncsim simulation of " _CIRCUIT "\n"
            "# AUTHOR  : " _USER "\n"
            "# DATE    : " _DATE "\n"
            "# " RVBseparator("-" 77) "\n"
            "# NOTES :\n"
            RVBseparator("#" 78) "\n"
            "simvision -input " _SV_FILE "\n"
        )
        sv_Lines = strcat(
            RVBseparator("#" 78) "\n"
            "# NAME    : " _SV_FILE "\n"
            "# PURPOSE : simvision script for " _CIRCUIT "\n"
            "# AUTHOR  : " _USER "\n"
            "# DATE    : " _DATE "\n"
            "# " RVBseparator("-" 77) "\n"
            "# NOTES :\n"
            "#   * analog waveforms come up as continuous(*) if format -trace analogLinear\n"
            "#   * the dbfind search / dbfind find commands are time-consuming; can\n"
            "#     be eliminated if all of the named signals are present\n"
            RVBseparator("#" 78) "\n"
            "#" RVBseparator("-" 78) "\n"
            "# testbench specifics:\n"
            "#   * group specification: \"<Group Name>\"\n"
            "#   * group specification with overlayed analog signals: \"<Group Name>:-1:1\"\n"
            "#   * subcircuit specification: @subcircuit1.subcircuit2:\n"
            "#   * group and signal specifications follow group or signal name:\n"
            "#       ~  : analogLinear trace\n"
            "#       ^  : analogSampleAndHold trace\n"
            "#       %d %h %b : radix specifications\n"
            "#       number : limit specification (lower, upper)\n"
            "#       #ffee33 or #red : color specification\n"
            "#" RVBseparator("-" 78) "\n"
            "set testbench " _TESTBENCH "\n"
            "set signals {\n"
            "    " plot_signal_lines "\n"
            "}\n"
            "#" RVBseparator("-" 78) "\n"
            "# preferences\n"
            "#   * colors:       overlay plot colors\n"
            "#   * analogheight: height of analog signals\n"
            "#   * wgeometry:    waveform window geometry\n"
            "#   * wunits:       waveform time units\n"
            "#" RVBseparator("-" 78) "\n"
            "set colors  {red yellow green blue orange cyan magenta}\n"
            "set analogheight 100\n"
            "set wgeometry 1204x800+0+0\n"
            "set wunits ps\n"
            "preferences set marching-waveform {1}\n"
            "preferences set db-signal-show-live {1}\n"
            "#" RVBseparator("-" 78) "\n"
            "# (re)-start simulation\n"
            "#" RVBseparator("-" 78) "\n"
            "console submit -using simulator reset\n"
            "#" RVBseparator("-" 78) "\n"
            "# configure waveform window\n"
            "#" RVBseparator("-" 78) "\n"
            "source /auto/lwtools/local/lib/synthesis/simvision_core.tcl\n"
            "#" RVBseparator("-" 78) "\n"
            "# run simulation\n"
            "#" RVBseparator("-" 78) "\n"
            "console submit -using simulator run\n"
            "waveform xview zoom -outfull\n"
        )
        makLines = strcat(
            RVBseparator("#" 78) "\n"
            "# NAME    : " _MAKFILE "\n"
            "# PURPOSE : Makefile for synthesis project\n"
            "# AUTHOR  : " _USER "\n"
            "# DATE    : " _DATE "\n"
            "# " RVBseparator("-" 77) "\n"
            "# NOTES :\n"
            "#   project-specific definitions:\n"
            "#     PROJ : project name\n"
            "#     CELL : cell name\n"
            "#     DEFS : specific verilog compiler defines (ex. +define+OUTPUT)\n"
            "#   technology-specific definitions:\n"
            "#     TECH  : technology name\n"
            "#     VLLIB : standard-cell library\n"
            RVBseparator("#" 78) "\n"
            "RCAD  = /auto/lwtools/local/lib\n"
            "PROJ  = " _PROJECT "\n"
            "CELL  = " _CIRCUIT "\n"
            "DEFS  = +define+OUTPUT +define+UNIT_DELAY \\\n"
            " 	-y ncsim_" testbench "/lib_" testbench "\n"
            "#	-y _pandr\n"
            "#	+nctimescale+10ps/10fs\n"
            "#	+ncsdf_cmd_file+sdf.SLOW.cmd +sdf_verbose\n"
            "include $(RCAD)/synthesis/make.$(PROJ)\n"
            "include $(RCAD)/synthesis/make_body\n"
            "\n"
            "# alternative ncverilog definitions\n"
            "# NCS    = $(RVBBIN)/run_ncverilog        +nc64bit +access+w -ams\n"
            "# NCS    = /auto/edatools/bin/ncverilog   +nc64bit +access+w -ams\n"
        )
        genLines = strcat(
            "#!/auto/lwtools/local/bin/python\n"
            RVBseparator("#" 78) "\n"
            "# NAME    : generate_ncsim_lib.py"  "\n"
            "# PURPOSE : use ncsim to netlist, generate module library for testbench\n"
            "# AUTHOR  : " _USER "\n"
            "# DATE    : " _DATE "\n"
            "# " RVBseparator("-" 77) "\n"
            "# NOTES   :\n"
            "#     * from testbench schematic window:\n"
            "#       Launch -> Simulation -> NC-Verilog\n"
            "#         o  initialize run directory (1st icon)\n"
            "#               use default netlistdirectory/run-directory:\n"
            "#               testbench_run1\n"
            "#         o  netlist (2nd icon)\n"
            RVBseparator("#" 78) "\n"
            "import user, decida\n"
            "from decida.vtb import vtb\n"
            "\n"
            "user       = \"" _USER "\"\n"
            "project    = \"" _PROJECT "\"\n"
            "projmnt    = \"" _PROJMNT "\"\n"
            "testbench  = \"" _TESTBENCH "\"\n"
            "netlistdir = \"%s/%s/ws/%s/%s_run1\" % (projmnt, project, user, testbench)\n"
           "\n"
           "vtb(netlistdir, testbench, mod_dir=None)\n"
        )
        ;---------------------------------------------------------------------
        ; print to testbench directory in home directory
        ;---------------------------------------------------------------------
        vtbDir  = strcat(home "/" testbench)
        vtbFile = strcat(vtbDir "/" _VTBFILE)
        tclFile = strcat(vtbDir "/" _TCLFILE)
        sv_File = strcat(vtbDir "/" _SV_FILE)
        genFile = strcat(vtbDir "/generate_ncsim_lib.py")
        makFile = strcat(vtbDir "/" _MAKFILE)
        tptDir  = strcat(vtbDir "/module_templates")
        cktFile = strcat(vtbDir "/" _CIRCUIT ".v")
        if( !isDir(vtbDir) then
           createDir(vtbDir)
        else
           printf("warning: testbench directory already exists %L\n" vtbDir)
        )
        if( isDir(tptDir) then
           printf("removing and re-creating module template directory\n")
           sh(strcat("rm -rf " tptDir))
        )
        createDir(tptDir)
    
        fout=outfile(vtbFile)
        fprintf(fout "%s" vtbLines)
        close(fout)
    
        fout=outfile(tclFile)
        fprintf(fout "%s" tclLines)
        close(fout)
    
        fout=outfile(sv_File)
        fprintf(fout "%s" sv_Lines)
        close(fout)
    
        fout=outfile(makFile)
        fprintf(fout "%s" makLines)
        close(fout)
    
        fout=outfile(genFile)
        fprintf(fout "%s" genLines)
        close(fout)
        printf(strcat("chmod +x " genFile "\n"))
        sh(strcat("chmod +x " genFile))
        ;---------------------------------------------------------------------
        ; touch the dummy circuit module file
        ;---------------------------------------------------------------------
        sh(strcat("touch " cktFile))
        ;---------------------------------------------------------------------
        ; print module templates
        ;---------------------------------------------------------------------
        foreach(inst insts
           inst_cell = InstCell[inst]
           port_list = list()
           input_lines = ""
           output_lines = ""
           inout_lines = ""
           foreach(item InstPorts[inst]
               port  = nth(0 item)
               net   = nth(1 item)
               dir   = nth(2 item)
               sbus1 = nth(3 item)
               sbus2 = nth(4 item)
               port_list = append(port_list
                   list(strcat("    " port))
               )
               if(strcmp(sbus1, "") == 0 then
                   sbus = " "
               else
                   sbus = strcat("[" sbus1 ":" sbus2 "] ")
               )
               if(strcmp(dir, "input")  == 0 then
                   input_lines = strcat(input_lines "    input " sbus port ";\n")
               )
               if(strcmp(dir, "output")  == 0 then
                   output_lines = strcat(output_lines "    output " sbus port ";\n")
               )
               if(strcmp(dir, "inout")  == 0 then
                   inout_lines = strcat(inout_lines "    inout " sbus port ";\n")
               )
           )
           port_lines = strcat(buildString(port_list ",\n") "\n")
           _CELL = inst_cell
           _VCMFILE = strcat(inst_cell ".v")
           vcmLines = strcat(
               "//"  RVBseparator("#" 78) "\n"
               "// NAME:    " _VCMFILE "\n"
               "// PURPOSE: verilog module " _CELL "\n"
               "// DATE:    " _DATE "\n"
               "// AUTHOR:  " _USER "\n"
               "//" RVBseparator("-" 77) "\n"
               "//" RVBseparator("#" 78) "\n"
               "module " _CELL "(\n"
               port_lines
               ");\n"
               input_lines
               output_lines
               "\n"
               "    initial begin\n"
               "    end\n"
               "endmodule\n"
           )
           vcmFile = strcat(tptDir "/" _VCMFILE)
           fout=outfile(vcmFile)
           fprintf(fout "%s" vcmLines)
           close(fout)
        )
        ;---------------------------------------------------------------------
        ; display where files were written
        ;---------------------------------------------------------------------
        RVBwarning(strcat("Verilog Testbench dirctory = \"" vtbDir "\""))
    )
)
