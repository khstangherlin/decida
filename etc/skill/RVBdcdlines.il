;###############################################################################
; NAME    : RVBdcdlines.il
; PURPOSE : create starter python decida script
; AUTHOR  : Richard Booth
; DATE    : Sat Jan 19 15:57:56 2013
; NOTES   : 
;###############################################################################
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
; PROC: RVBdcdFormProjCB
; PURPOSE: Project choice form call-back
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
procedure( RVBdcdFormProjCB()
    prog(()
        RVBproject=RVBdcdAppForm~>dcdProj~>value
    )
)
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
; PROC: RVBdcdFormTechCB
; PURPOSE: Technology choice form call-back
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
procedure( RVBdcdFormTechCB()
    prog(()
        RVBtechnology=RVBdcdAppForm~>dcdTech~>value
    )
)
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
; PROC: RVBdcdFormSimuCB
; PURPOSE: Simulator choice form call-back
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
procedure( RVBdcdFormSimuCB()
    prog(()
        RVBsimulator=RVBdcdAppForm~>dcdSimu~>value
    )
)
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
; PROC: RVBdcdFormViewCB
; PURPOSE: Netlist view choice form call-back
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
procedure( RVBdcdFormViewCB()
    prog(()
        RVBview=RVBdcdAppForm~>dcdView~>value
    )
)
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
; PROC: RVBdcdForm
; PURPOSE: main decida generation form
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
procedure( RVBdcdForm()
    prog(
        (fields promptWidth xmin xmax ypos  proj tech simu
            projprompt techprompt simuprompt viewprompt
            projects techs simulators views help_file
        )
        ;----------------------------------------------------------------------
        ; location specific
        ;----------------------------------------------------------------------
        projects   = list("bird", "trane")
        techs      = list("ptm_130nm" "ptm_45nm")
        simulators = list("Spectre" "HSpice")
        views      = list("schematic" "config")
        help_file  = simplifyFilename("~/.DeCiDa/skill/RVBdcd_help.txt")
        ;----------------------------------------------------------------------
        ; try to get RVBproject RVBtechnology RVBsimulator from PROJECT
        ; if the parameters are already set in .cdsinit, use those values
        ;----------------------------------------------------------------------
        proj = RVBgetenv("PROJECT")
        case( proj
            (("bird")
                tech="ptm_130nm"
                simu="Spectre"
            )
            (("trane")
                tech="ptm_45nm"
                simu="Spectre"
            )
            (t
                proj="trane"
                tech="ptm_45nm"
                simu="Spectre"
            )
        )
        if(!boundp('RVBproject)    || !RVBproject    || \
            !member(RVBproject    projects)   RVBproject    = proj)
        if(!boundp('RVBtechnology) || !RVBtechnology || \
            !member(RVBtechnology techs)      RVBtechnology = tech)
        if(!boundp('RVBsimulator)  || !RVBsimulator  || \
            !member(RVBsimulator  simulators) RVBsimulator  = simu)
        RVBview = "schematic"
        ;----------------------------------------------------------------------
        ; form prompts
        ;----------------------------------------------------------------------
        projprompt = "project:"
        techprompt = "technology:"
        simuprompt = "simulator:"
        viewprompt = "netlist view:"
        promptWidth = max(
            hiGetTextWidth( hiGetFont("label") projprompt)
            hiGetTextWidth( hiGetFont("label") techprompt)
            hiGetTextWidth( hiGetFont("label") simuprompt)
            hiGetTextWidth( hiGetFont("label") viewprompt)
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
                    ?name 'dcdProj
                    ?prompt projprompt
                    ?callback '("RVBdcdFormProjCB()" )
                    ?choices projects
                    ?defValue RVBproject
                )
                xmin:ypos*hicLineHeight xmax:(++ypos)*hicLineHeight promptWidth
            )
            list(
                hiCreateRadioField(
                    ?name 'dcdTech
                    ?prompt techprompt
                    ?callback '("RVBdcdFormTechCB()" )
                    ?choices techs
                    ?defValue RVBtechnology
                )
                xmin:ypos*hicLineHeight xmax:(++ypos)*hicLineHeight promptWidth
            )
            list(
                hiCreateRadioField(
                    ?name 'dcdSimu
                    ?prompt simuprompt
                    ?callback '("RVBdcdFormSimuCB()" )
                    ?choices simulators
                    ?defValue RVBsimulator
                )
                xmin:ypos*hicLineHeight xmax:(++ypos)*hicLineHeight promptWidth
            )
            list(
                hiCreateRadioField(
                    ?name 'dcdView
                    ?prompt viewprompt
                    ?callback '("RVBdcdFormViewCB()" )
                    ?choices views
                    ?defValue RVBview
                )
                xmin:ypos*hicLineHeight xmax:(++ypos)*hicLineHeight promptWidth
            )
        )
        ;----------------------------------------------------------------------
        ; create form
        ;----------------------------------------------------------------------
        cmd = strcat("view(\"" help_file "\")")
        hiCreateAppForm(
            ?name          'RVBdcdAppForm
            ?formTitle     "DeCiDa TestPack"
            ?fields        fields
            ?callback      '("RVBdcdlines()" "")
            ?buttonLayout  '(
               OKCancelApply
               (DecidaHelp cmd)
            )
        )
        hiDisplayForm('RVBdcdAppForm)
    )
)
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
; PROC: RVBdcdProjPars
; PURPOSE: find projmnt, scratch, cases, simulator, modelfile
;     from user, proj, tech, simu
; NOTES: 
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
procedure( RVBdcdProjPars(user proj tech simu)
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
        ;----------------------------------------------------------------------
        ; project scratch directory:
        ; first try to find from env(asimenv.startup projectDir)
        ;----------------------------------------------------------------------
        scratch = simplifyFilename(strcat(
            "~/.DeCiDa/projects/" proj "/scratch"
        ))
        ;----------------------------------------------------------------------
        ; case names:
        ;----------------------------------------------------------------------
        case( tech
            (("ptm_130nm")
                cases = "tt ss ff fs sf"
            )
            (("ptm_45nm")
                cases = "tt ss ff fs sf"
            )
            (t
                cases = "tt ss ff fs sf"
            )
        )
        ;----------------------------------------------------------------------
        ; simulator: name that goes into script
        ;----------------------------------------------------------------------
        case( simu
            ("Spectre" simulator = "spectre")
            ("HSpice"  simulator = "hspiceD")
            (t         simulator = "spectre")
        )
        ;----------------------------------------------------------------------
        ; modelfile: if different from the one that Tckt returns
        ;----------------------------------------------------------------------
        modelfile = ""
        return(list(projmnt scratch cases simulator modelfile))
    )
)
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
; PROC: RVBbusexpand
; PURPOSE: expand a possibly bussed name
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
procedure(RVBbusexpand(name)
    prog((names buf i bus1 bus2)
        names = nil
        if(rexMatchp("^\\(.+\\)<\\([0-9]+\\):\\([0-9]+\\)>$" name) then
            root=     rexSubstitute("\\1")
            bus1=atoi(rexSubstitute("\\2"))
            bus2=atoi(rexSubstitute("\\3"))
            if(bus2 < bus1 then
                i=bus2
                bus2=bus1
                bus1=i
            )
            for(i bus1 bus2
                sprintf(buf "%s<%d>" root i)
                names=append(names list(buf))
            )
        else
            if(rexMatchp("^\\(.+\\)<\\([0-9]+\\)>$" name) then
                root=     rexSubstitute("\\1")
                bus1=atoi(rexSubstitute("\\2"))
                sprintf(buf "%s<%d>" root bus1)
                names=append(names list(buf))
            else
                names=append(names list(name))
            )
        )
        return(names)
    )
)
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
; PROC: RVBdcdlines
; PURPOSE: get decida lines for current cellview
; NOTES: 
;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
procedure(RVBdcdlines()
    prog(
        (   proj tech simu
            cv nh ih buf i bus1 bus2 root val
            user home date projmnt scratch cases simulator modelfile
            e sig1 sig2 report fout outfileName
            monitorLines elementLines
            tr_testReg tr_testLines tr_controlLines
            age_testReg age_testLines abe_controlLines
            mosfets analogLibSrcs case0 casespy ckt buss nbits yparbuf
            net     nets     Nets
            fet     fets     Fets
            ipin    ipins    IPins
            vsrcsig vsrcsigs VsrcSigs
            isrcsig isrcsigs IsrcSigs
            vsrcbus vsrcbuss VsrcBuss
        )
        ;----------------------------------------------------------------------
        ; list of analogLib sources
        ;----------------------------------------------------------------------
        analogLibSrcs=parseString(
            strcat(
                " vexp vpulse vpwl vpwlf vsin"
                " iexp ipulse ipwl ipwlf isin"
            )
        )
        ;----------------------------------------------------------------------
        ; list of mosfet types
        ;----------------------------------------------------------------------
        mosfets=parseString(
            strcat(
                " nch_lvt nch_hvt pch_lvt pch_hvt"
                " nsfet psfet nufet pufet nefet pefet nlfet plfet"
                " ntfet ptfet ntsfet ptsfet nt33fet pt33fet nts33fet pts33fet"
                " nsmos psmos numos pumos nemos pemos nlmos plmos"
                " ntmos ptmos ntsmos ptsmos nt33mos pt33mos nts33mos pts33mos"
                " tntsmos tptsmos"
            )
        )
        ;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        ; global parameter information
        ;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        ;--------------------------------------------------------------------
        ; user, home, date
        ; home is where the script is written
        ;--------------------------------------------------------------------
        user = RVBgetenv("USER")
        home = RVBgetenv("HOME")
        date = getCurrentTime()
        if(!boundp('user) || !user then
            user = "whoami"
        )
        if(!boundp('home) || !home then
            home = strcat("/home/" user)
        )
        ;--------------------------------------------------------------------
        ; RVBdcdForm sets:
        ;     RVBproject, RVBtechnology, RVBsimulator, RVBview
        ; RVBdcdProjPars used to set:
        ;     projmnt, scratch, cases, simulator, modelfile
        ;--------------------------------------------------------------------
        pars = RVBdcdProjPars(user RVBproject RVBtechnology RVBsimulator)
        projmnt   = nth(0 pars)
        scratch   = nth(1 pars)
        cases     = nth(2 pars)
        simulator = nth(3 pars)
        modelfile = nth(4 pars)
        cases     = parseString(cases)
        case0     = nth(0 cases)
        casespy   = ""
        foreach( case cases
            if( strlen(casespy) > 0 then
                casespy = strcat(casespy ", ")
            )
            casespy = strcat(casespy "\"" case "\"")
        )
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
        Nets     = makeTable("nets")
        Fets     = makeTable("fets")
        IPins    = makeTable("ipins")
        IsrcSigs = makeTable("isrcsigs")
        VsrcSigs = makeTable("vsrcsigs")
        VsrcBuss = makeTable("vsrcbuss")
        ;---------------------------------------------------------------------
        ; accumulate nets
        ; don't save <*x>node
        ;---------------------------------------------------------------------
        foreach(nh cv~>nets
            names = parseString(nh->name ",")
            foreach(name names
                if(rexMatchp("^<" name) || name == "gnd!" then
                else
                    if(rexMatchp("^\\(.+\\)<\\(.+\\)>$" name) then
                        root=rexSubstitute("\\1")
                        buss=rexSubstitute("\\2")
                        Nets[name] = 1
                    else
                        Nets[name] = 1
                    )
                )
            )
        )
        ;---------------------------------------------------------------------
        ; accumulate mosfets
        ;---------------------------------------------------------------------
        foreach(ih cv~>instances
            name=ih~>name
            libr=ih~>libName
            cell=ih~>cellName
            if(member(cell mosfets) then
                foreach(name RVBbusexpand(name)
                    Fets[name]=1
                )
            )
        )
        ;---------------------------------------------------------------------
        ; accumulate input terminals, which will be hooked-up to a vsrc
        ;---------------------------------------------------------------------
        foreach(th cv~>terminals
            if(th~>direction == "input" then
                name=th~>name
                IPins[name]=1
                if(rexMatchp("^\\(.+\\)<\\([0-9]+\\):\\([0-9]+\\)>$" name) then
                    root=rexSubstitute("\\1")
                    bus1=atoi(rexSubstitute("\\2"))
                    bus2=atoi(rexSubstitute("\\3"))
                    if( bus2 < bus1 then
                        nbits = bus1 - bus2 + 1
                    else
                        nbits = bus2 - bus1 + 1
                    )
                    sprintf(val "%d'd0 v0=0.0 v1=$vdd" nbits)
                    VsrcBuss[strcat("v_" name)]="0.0"
                else
                    VsrcSigs[strcat("v_" name)]="0.0"
                )
            )
        )
        ;---------------------------------------------------------------------
        ; accumulate sources
        ;---------------------------------------------------------------------
        foreach(ih cv~>instances
            name=ih~>name
            libr=ih~>libName
            cell=ih~>cellName
            if(libr == "analogLib" then
                if(cell == "idc" then
                    foreach(name RVBbusexpand(name)
                        IsrcSigs[name]="netlist"
                    )
                else
                    if(cell == "vdc" then
                        if(rexMatchp("^\\(.+\\)<\\([0-9]+\\):\\([0-9]+\\)>$" name) then
                            root=rexSubstitute("\\1")
                            bus1=atoi(rexSubstitute("\\2"))
                            bus2=atoi(rexSubstitute("\\3"))
                            if( bus2 < bus1 then
                                nbits = bus1 - bus2 + 1
                            else
                                nbits = bus2 - bus1 + 1
                            )
                            sprintf(val "%d'd0 v0=0.0 v1=$vdd" nbits)
                            VsrcBuss[name]=val
                        else
                            val = "netlist"
                            if(name == "vdd" val = "$vdd")
                            if(name == "vss" val = "0")
                            VsrcSigs[name] = val
                        )
                    else
                        if(member(cell analogLibSrcs) then
                            VsrcSigs[name] = "netlist"
                        )
                    )
                )
            )
        )
        ;---------------------------------------------------------------------
        ; sort nets, fets, srcs
        ;---------------------------------------------------------------------
        nets     = setof(element Nets t)
        nets     = sort(nets    'alphalessp)
        ipins    = setof(element IPins t)
        ipins    = sort(ipins 'alphalessp)
        vsrcbuss = setof(element VsrcBuss t)
        vsrcbuss = sort(vsrcbuss 'alphalessp)
        vsrcsigs = setof(element VsrcSigs t)
        vsrcsigs = sort(vsrcsigs 'alphalessp)
        isrcsigs = setof(element IsrcSigs t)
        isrcsigs = sort(isrcsigs 'alphalessp)
        fets     = setof(element Fets t)
        fets     = sort(fets 'alphalessp)
        ;---------------------------------------------------------------------
        ; default signals for view/report
        ; might want to bus-expand
        ;---------------------------------------------------------------------
        if(nets && (length(nets) > 1) then
            sig1=nth(0 nets)
            sig2=nth(1 nets)
        else
            sig1="clk"
            sig2="data"
        )
        ;---------------------------------------------------------------------
        ; monitor lines
        ;---------------------------------------------------------------------
        e = "       "
        monitorLines = ""
        buf = e
        if(nets then
            foreach(net nets
                buf=strcat(buf " " net)
                if(strlen(buf) > 60 then
                    monitorLines=strcat(monitorLines buf "\n")
                    buf = e
                )
            )
        )
        if(vsrcsigs then
            foreach(vsrcsig vsrcsigs
                buf=strcat(buf " I(" vsrcsig ")")
                if(strlen(buf) > 60 then
                    monitorLines=strcat(monitorLines buf "\n")
                    buf = e
                )
            )
        )
        if(fets then
            foreach(fet fets
                buf=strcat(buf " ID(" fet ")")
                if(strlen(buf) > 60 then
                    monitorLines=strcat(monitorLines buf "\n")
                    buf = e
                )
            )
        )
        if(strlen(buf) > 7 then
            monitorLines=strcat(monitorLines buf "\n")
        )
        ;---------------------------------------------------------------------
        ; element lines
        ;---------------------------------------------------------------------
        e = "            "
        elementLines = ""
        if(vsrcsigs then
            foreach(vsrcsig vsrcsigs
                val = VsrcSigs[vsrcsig]
                elementLines=strcat(elementLines e vsrcsig " " val "\n")
            )
        )
        if(isrcsigs then
            foreach(isrcsig isrcsigs
                val = IsrcSigs[isrcsig]
                elementLines=strcat(elementLines e isrcsig " " val "\n")
            )
        )
        if(vsrcbuss then
            foreach(vsrcbus vsrcbuss
                val = VsrcBuss[vsrcbus]
                elementLines=strcat(elementLines e vsrcbus " " val "\n")
            )
        )
        ;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        ; get .designVariables and netlistFooter
        ;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        testbench=cv->cell->name
        ;---------------------------------------------------------------------
        ; testbench directory
        ;---------------------------------------------------------------------
        tbdir = strcat(scratch "/" testbench "/" simulator "/" RVBview)
        ;---------------------------------------------------------------------
        ; design variables and netlist footer
        ;---------------------------------------------------------------------
        netlist_desvar = strcat(tbdir "/netlist/.designVariables")
        netlist_footer = strcat(tbdir "/netlist/netlistFooter")
        ;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        ; modelfile lines
        ;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        modelfile_lines = "    modelfile = tckt.get_modelfile()\n"
        if(strlen(modelfile) > 0 then
            modelfile_lines = strcat(
                modelfile_lines "    modelfile = \"" modelfile "\"\n"
            )
        )
        ;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        ; build control block before putting into netlist
        ;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        tr_controlLines  = ""
        age_controlLines = ""
        case( simulator
            ("spectre" 
                e = "            "
                tr_controlLines = strcat(
                    e "//----------------------------------------\n"
                    e "// default options: \n"
                    e "//----------------------------------------\n"
                    e "simulatorOptions options \\\\\n"
                    e "    reltol=1e-3 vabstol=1e-6 iabstol=1e-12 \\\\\n"
                    e "    temp=$temp tnom=27 scalem=1.0 scale=1.0 \\\\\n"
                    e "    gmin=1e-12 rforce=1 pivrel=1e-3 \\\\\n"
                    e "    maxnotes=5 maxwarns=5 digits=5 cols=80 \n"
                    e "//----------------------------------------\n"
                    e "// other options: \n"
                    e "//----------------------------------------\n"
                    e "//  saveOptions options save=allpub\n"
                    e "//  saveOptions options save=all currents=all\n"
                    e "//  ic osc.icp_phb=0.0\n"
                    e "//  parameters cx=0.8p\n"
                )
                if(ipins then
                    tr_controlLines = strcat(tr_controlLines
                        e "//----------------------------------------\n"
                        e "// netlist pin lines\n"
                        e "//----------------------------------------\n"
                    )
                    foreach(name ipins
                        foreach(name RVBbusexpand(name)
                            tr_controlLines=strcat(tr_controlLines
                                e "v_" name
                                " (" name " 0) vsource type=dc dc=0.0 mag=1.0\n"
                            )
                        )
                    )
                )
                tr_controlLines = strcat(tr_controlLines
                    e "//----------------------------------------\n"
                    e "// models and analysis\n"
                    e "// NOTE: ocean requires -format psfbin\n"
                    e "//----------------------------------------\n"
                    e "include \"$modelfile\" section=$process\n"
                    e "    trAnal tran stop=$tstop\n"
                    e "//  dcOpAnal dc\n"
                    e "//  dcOpInfo info what=oppoint\n"
                    e "//  dcAnal   dc   param=temp start=-40 stop=125 step=10\n"
                    e "//  dcAnal   dc   dev=iload param=dc start=0 stop=1.0 step=0.1\n"
                    e "//  acAnal   ac   start=10 stop=10G dec=20\n"
                    e "//  stbAnal  stb  start=10 stop=10G probe=reg.vstb\n"
                    e "//  pssAnal    VOUT_P VOUT_N pss     fund=10.8G \\\\\n"
                    e "//      errpreset=conservative tstab=5n method=trap \\\\\n"
                    e "//      harms=10\n"
                    e "//  pnoiseAnal VOUT_P VOUT_N pnoise  start=1 stop=10G\n"
                    e "//  mcAnal montecarlo variations=mismatch \\\\\n"
                    e "//      seed=1221 numruns=3 savefamilyplots=yes\n"
                    e "//  {\n"
                    e "//      tran1 tran stop=$tstop\n"
                    e "//      export tz=oceanEval(\"cross(v(\\\\\\\"Z\\\\\\\") $vdd/2 1 'falling)\")\n"
                    e "//  }\n"
                )
                if(isFile(netlist_desvar) || isFile(netlist_footer) then
                    tr_controlLines = strcat(tr_controlLines
                        e "//----------------------------------------\n"
                        e "// variables and netlist footer:\n"
                        e "//----------------------------------------\n"
                    )
                    if(isFile(netlist_desvar) then
                        f=infile(netlist_desvar)
                        while( gets(line, f) 
                            tr_controlLines = strcat(tr_controlLines e line)
                        )
                        close(f)
                    )
                    if(isFile(netlist_footer) then
                        f=infile(netlist_footer)
                        while( gets(line, f) 
                            if(!rexMatchp("\\.END" upperCase(line)) then
                                tr_controlLines = strcat(tr_controlLines e line)
                            )
                        )
                        close(f)
                    )
                )
            )
            ("hspiceD"
                e = "            "
                tr_controlLines = strcat(
                    e ".options rawpts=150 nomod brief=1 probe csdf\n"
                    e ".options itl1=200 itl2=50\n"
                    e ".options conv=-1 accurate=1 gmin=0 dcpath=0\n"
                )
                if(ipins then
                    tr_controlLines = strcat(tr_controlLines
                        e "*-----------------------------------------\n"
                        e "*  netlist pin lines\n"
                        e "*-----------------------------------------\n"
                    )
                    foreach(name ipins
                        foreach(name RVBbusexpand(name)
                            tr_controlLines=strcat(tr_controlLines
                                e "v_" name " " name " 0 0.0\n"
                            )
                        )
                    )
                )
                tr_controlLines = strcat(tr_controlLines
                    e ".lib \"$modelfile\" $process\n"
                    e ".temp $temp\n"
                    e ".tran $tstep $tstop\n"
                )
                if(isFile(netlist_desvar) || isFile(netlist_footer) then
                    tr_controlLines = strcat(tr_controlLines
                        e "*-----------------------------------------\n"
                        e "*  variables and netlist footer:\n"
                        e "*-----------------------------------------\n"
                    )
                    if(isFile(netlist_desvar) then
                        f=infile(netlist_desvar)
                        while( gets(line, f) 
                            tr_controlLines = strcat(tr_controlLines e line)
                        )
                        close(f)
                    )
                    if(isFile(netlist_footer) then
                        f=infile(netlist_footer)
                        while( gets(line, f) 
                            if(!rexMatchp("\\.END" upperCase(line)) then
                                tr_controlLines = strcat(tr_controlLines e line)
                            )
                        )
                        close(f)
                    )
                )
            )
        )
        ;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        ; build tr test block before putting into template
        ;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        tr_testReg   = "    tr simulate dcop accum_view view report\n"
        tr_testLines = strcat(
            "#"  RVBseparator("=" 78) "\n"
            "# tr: transient analysis\n"
            "#"  RVBseparator("=" 78) "\n"
            "def tr(detail=\"simulate\") :\n"
            "    global tckt\n"
            "    test      = tckt.get_test()\n"
            modelfile_lines
            "    tckt[\"circuit\"]     = testcircuit\n"
            "    tckt[\"netlistfile\"] = \"netlist\"\n"
            "    #" RVBseparator("-" 72) "\n"
            "    # signals to monitor\n"
            "    #" RVBseparator("-" 72) "\n"
            "    tckt.monitor(\"\"\"\n"
            monitorLines
            "    \"\"\")\n"
            "    #" RVBseparator("-" 72) "\n"
            "    # loop through experiments\n"
            "    #" RVBseparator("-" 72) "\n"
            "    poststart = True\n"
            "    remote = \"\"\n"
            "    cases = [" casespy "]\n"
            "    #-----------------------------------------------------------\n"
            "    # additional resistor corner cases\n"
            "    #-----------------------------------------------------------\n"
            "    # cases.extend([\"cssa_rmax\", \"cssa_rmin\", \"cffa_rmax\", \"cffa_rmin\"])\n"
            "    #-----------------------------------------------------------\n"
            "    # change following True to False after debugging the script:\n"
            "    #-----------------------------------------------------------\n"
            "    if True :\n"
            "        cases = [\"" case0 "\"]\n"
            "        remote = \"\"\n"
            "    for case in cases :\n"
            "        tag     = \"%s\" % (case)\n"
            "        tckt[\"case\"] = case\n"
            "        ckey    = tckt.get_case_key()\n"
            "        process = tckt.get_process()\n"
            "        vdd     = tckt.get_vdd()\n"
            "        temp    = tckt.get_temp()\n"
            "        prefix  = \"%s.%s.%s\" % (test, tckt[\"circuit\"], tag)\n"
            "        print prefix\n"
            "        tckt[\"title\"]  = prefix\n"
            "        tckt[\"prefix\"] = prefix\n"
            "        tstop = 10e-9\n"
            "        tstep = 1e-11\n"
            "        tckt.elements(\"\"\"\n"
            elementLines
            "        \"\"\")\n"
            "        tckt.control(\"\"\"\n"
            tr_controlLines
            "        \"\"\")\n"
            "        if   detail == \"simulate\" :\n"
            "            if False and tckt.is_already_done() : continue\n"
            "            tckt.generate_inputfile()\n"
            "            if remote != \"\" : tckt[\"progress\"] = False\n"
            "            tckt.simulate(clean=False, remote=remote)\n"
            "        elif detail == \"dcop\" :\n"
            "            tckt.dcop()\n"
            "        elif detail == \"accum_view\" :\n"
            "            if poststart :\n"
            "                poststart = False\n"
            "                cmd = []\n"
            "            if False and tckt.no_data() : continue\n"
            "            datafile = tckt.get_datafile(\"tr\")\n"
            "            d = Data()\n"
            "            d.read(datafile)\n"
            "            avar = \"" sig1 "\"\n"
            "            d.set(\"%s_%s = %s\" % (avar, tag, avar))\n"
            "            plt = \"time %s_%s\" % (avar, tag)\n"
            "            cmd.extend([d, plt])\n"
            "        elif detail == \"view\" :\n"
            "            if poststart :\n"
            "                poststart = False\n"
            "                fn = FrameNotebook(tab_location=\"top\")\n"
            "            if False and tckt.no_data() : continue\n"
            "            datafile = tckt.get_datafile(\"tr\")\n"
            "            d = Data()\n"
            "            d.read(datafile)\n"
            "            plt = \"time " sig1 "\"\n"
            "            if True :\n"
            "                DataViewm(fn.new_page(prefix), data=d, command=[[plt]])\n"
            "                fn.lift_tab(prefix)\n"
            "            else :\n"
            "                XYplotm(fn.new_page(prefix), command=[d, plt])\n"
            "            fn.wait(\"continue\")\n"
            "        elif detail == \"report\" :\n"
            "            if poststart :\n"
            "                poststart = False\n"
            "                point = 0\n"
            "                rpt = Report(test + \".report\", verbose=True, csv=False)\n"
            "                header  = \"point case temp vdd\"\n"
            "                rpt.header(header)\n"
            "            datafile = tckt.get_datafile(\"tr\")\n"
            "            if not os.path.isfile(datafile) :\n"
            "                continue\n"
            "            d = Data()\n"
            "            d.read(datafile)\n"
            "            rpt.report(point, ckey, temp, vdd)\n"
            "            point += 1\n"
            "        else :\n"
            "            print  \"detail \" + detail + \" not supported\"\n"
            "    if detail == \"accum_view\" :\n"
            "        XYplotm(command=cmd)\n"
        )
        ;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        ; begin report
        ;%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        report = ""
        ckt=cv->cell->name
        if(rexMatchp("^test_\\(.+\\)$" ckt) then
            ckt=rexSubstitute("\\1")
        )
        if(rexMatchp("^tb_\\(.+\\)$" ckt) then
            ckt=rexSubstitute("\\1")
        )
        if(rexMatchp("^\\(.+\\)_tb$" ckt) then
            ckt=rexSubstitute("\\1")
        )
        _FILE      = strcat(ckt ".py")
        _DATE      = date
        _USER      = user
        _TESTBENCH = testbench
        _CIRCUIT   = ckt
        _PROJECT   = RVBproject
        _SCRATCH   = scratch
        _PROJMNT   = projmnt
        report=strcat(report
          "#! /usr/bin/env python\n"
          "#"  RVBseparator("#" 78) "\n"
          "# NAME:    " _FILE "\n"
          "# PURPOSE: sequence file for simulation\n"
          "# DATE:    " _DATE "\n"
          "# AUTHOR:  " _USER "\n"
          "# " RVBseparator("-" 77) "\n"
          "# NOTES:\n"
          "#   * example tckt.monitor() specifications:\n"
          "#     REF       : monitor voltage of node REF\n"
          "#     VCD<3:0>  : monitor voltage of nodes VCD_3, ... , VCD_0\n"
          "#     I(vsc)    : monitor current in voltage source vsc\n"
          "#     ID(mn1)   : monitor drain current in mosfet mn1\n"
          "#     IR(res)   : monitor current in resistor res\n"
          "#     IX(xa1.p) : monitor current in subcircuit xa1, node p\n"
          "#     PN(mn1-vds) : monitor mosfet mn1 vds\n"
          "#       (vgs, vbs, vdss, vsat_marg, Gm, Gds, ...)\n"
          "#     @gmc:     : following specs are for subcircuit gmc\n"
          "#     @gmc.q:   : following specs are for subcircuit gmc.q\n"
          "#     @:        : following specs are for top-level circuit\n"
          "#   * example tckt.element() definitions:\n"
          "#     vin sin 0.6 0.2 $freq\n"
          "#     vbg netlist\n"
          "#     vdd $vdd\n"
          "#     vb1 pwl 0,0 10u,$vdd\n"
          "#     vsd<3:0> 5'b0011 v0=0.0 v1=$vdd\n"
          "#     vdac_in<9:0> counter v0=0.0 v1=$vdd edge=$edge hold=$hold\n"
          "#     vac ac dc=0.5 mag=1 phase=180\n"
          "#     vclk clock v0=0.0 v1=$vdd edge=$edge freq=$freq\n"
          "#     vdat rand v0=0.0 v1=$vdd length=1024 edge=$edge data_rate=$data_rate\n"
          "#     vdat prbs size=7 v0=0.0 v1=$vdd edge=$edge data_rate=$data_rate\n"
          "#   * example Data commands:\n"
          "#     d.set(\"z = OUT*2\")\n"
          "#     d.a2d(\"z\", \"SD<3:0>\", slice=1.5)\n"
          "#     x = d.crossings(\"time\", \"OUT\", level=1.5, edge=\"rising\")\n"
          "#     period = x[3] - x[2]\n"
          "#     freq = d.measure_freq(\"time\", \"OUT\")\n"
          "#     iavg = d.time_average(\"time\", \"vdd:1\")\n"
          "#     d.filter(\"time > 10e-9\")\n"
          "#"  RVBseparator("#" 78) "\n"
          "import user, decida, sys, string, os, os.path, re, math\n"
          "from decida.Report        import Report\n"
          "from decida.Data          import Data\n"
          "from decida.Tckt          import Tckt\n"
          "from decida.XYplotm       import XYplotm\n"
          "from decida.DataViewm     import DataViewm\n"
          "from decida.FrameNotebook import FrameNotebook\n"
          "#"  RVBseparator("=" 78) "\n"
          "# test-circuit init\n"
          "#"  RVBseparator("=" 78) "\n"
          "user        = \"" _USER      "\"\n"
          "project     = \"" _PROJECT   "\"\n"
          "testbench   = \"" _TESTBENCH "\"\n"
          "testcircuit = \"" _CIRCUIT   "\"\n"
          "projmnt     = \"" _PROJMNT   "\"\n"
          "scratch     = \"" _SCRATCH   "\"\n"
          "simulator   = \"" simulator  "\"\n"
          "tbview      = \"" RVBview    "\"\n"
          "wsdir = \"%s/%s/ws/%s\" % (projmnt, project, user)\n"
          "tbdir = \"%s/%s/%s/%s\" % (scratch, testbench, simulator, tbview)\n"
          "tckt = Tckt(project=project, simulator=simulator, verbose=True)\n"
          "tckt[\"testdir\"]     = tbdir\n"
          "tckt[\"path\"]        = [\".\", tbdir + \"/netlist\"]\n"
          "tckt[\"temp_high\"]   = 125\n"
          "tckt[\"resultsdir\"]  = tbdir + \"/decida\"\n"
          "#tckt[\"progress\"]    = False\n"
          "#tckt[\"simulator_args\"] += \" +aps +mt=4 \"\n"
          "#tckt[\"simulator_args\"] += \" -format psfbin -raw %s/psf \" % (tckt[\"resultsdir\"]) \n"
          "#"  RVBseparator("@" 78) "\n"
          "# tests\n"
          "#"  RVBseparator("@" 78) "\n"
          tr_testLines
          "#"  RVBseparator("=" 78) "\n"
          "# run specified tests\n"
          "# all_tests format:  test details\n"
          "# command-line argument format: test:detail or test (if no details)\n"
          "#"  RVBseparator("=" 78) "\n"
          "all_tests = \"\"\"\n"
          tr_testReg
          "\"\"\"\n"
          "tests = tckt.test_select(all_tests, sys.argv[1:])\n"
          "for test in tests :\n"
          "    eval(test)\n"
          "exit()\n"
        )
        ;---------------------------------------------------------------------
        ; print to file in home directory
        ;---------------------------------------------------------------------
        outfileName=strcat(home "/" ckt ".py")
        fout=outfile(outfileName)
        fprintf(fout "%s" report)
        close(fout)
        system(strcat("/bin/chmod +x " outfileName))
        RVBwarning(strcat("DeCiDa testpack file = \"" outfileName "\""))
    )
)
