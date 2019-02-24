##############################################################################
# NAME    : simvision_core.tcl
# PURPOSE : setup body for displaying signals and running ncsim
# AUTHOR  : Richard Booth
# DATE    : Mon Apr 15 17:11:08 2013
# NOTES   :
#   * required variables:
#   o testbench specifics:
#     - $testbench: toplevel testbench
#     - $signals: list of signals to plot
#       o group specification: "<Group Name>"
#       o group specification with overlayed analog signals: "<Group Name>:-1:1"
#       o subcircuit specification: @subcircuit1.subcircuit2:
#       o group and signal specifications follow group or signal name:
#        (separated by colon: example VLF:^:0.0:1.2)
#         ~  : analogLinear trace
#         ^  : analogSampleAndHold trace
#         %d %h %b : radix specifications
#         number : limit specification (lower, upper)
#         #ffee33 or #red : color specification
#   o preferences:
#     - $colors:       overlay plot colors 
#                      default={red yellow green blue orange cyan magenta}
#     - $analogheight: height of analog signals 
#                      default=100
#     - $wgeometry:    waveform window geometry
#                      default="1204x800-0+0"
#     - $wunits:       waveform time units
#                      default="us"
#     - $database:     simvision database
#                      default="simulator"
##############################################################################
#-----------------------------------------------------------------------------
# default values
#-----------------------------------------------------------------------------
if {![info exists testbench]} {
  puts "\"testbench\" variable is not set"
}
if {![info exists signals]} {
  puts "\"signals\" variable is not set"
}
if {![info exists colors]} {
  set colors  {red yellow green blue orange cyan magenta}
}
if {![info exists analogheight]} {
  set analogheight 100
}
if {![info exists wunits]} {
  set wunits us
}
if {![info exists wgeometry]} {
  set wgeometry 1204x800-0+0
}
if {![info exists database]} {
  set database simulator
}
set scope ${database}::${testbench}
#-----------------------------------------------------------------------------
# place console and design browser
#-----------------------------------------------------------------------------
set console [window find -name Console]
if {$console != ""} {
    eval window geometry $console 700x250-0+531
}
set browser [window find -type browser]
if {$browser != ""} {
    eval window geometry $browser 700x500-0+0
}
#-----------------------------------------------------------------------------
# waveform viewer
#-----------------------------------------------------------------------------
if {[window find -match exact -name "Waveform 1"] == {}} {
  window new WaveWindow -name "Waveform 1"
}
window geometry "Waveform 1" $wgeometry
window target   "Waveform 1" on
waveform using  "Waveform 1"
waveform clearall
waveform sidebar visibility partial
waveform set -primarycursor "TimeA" -signalnames name -signalwidth 175 \
  -units $wunits -valuewidth 75

#ursor set -using "TimeA" -time 0
#ursor set -using "TimeA" -marching 1
cursor set -using "TimeA" -time 100
waveform baseline set -time 0
#-----------------------------------------------------------------------------
# add groups and signals
#-----------------------------------------------------------------------------
set subckt ""
set group  ""
set gradix ""
set sradix ""
foreach signal $signals {
  puts SIGNAL=$signal
  if       {[regexp {^@(.*):$} $signal match subckt]} {
    puts "SUBCKT=$subckt"
  } elseif {[regexp {^<(.*)>}  $signal match group ]} {
    puts "GROUP=$group"
    if {$group != ""} {
      set fields [split $signal :]
      set fields [lrange $fields 1 end]
      set ganalog 0
      set overlay 0
      set gcolor  ""
      set gradix  ""
      set gymin   ""
      set gymax   ""
      foreach field $fields {
        if {[regexp {^(%.)$} $field match radix]} {
          set gradix $radix
        } elseif {[regexp {^(#[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F])$} $field match color]} {
          set gcolor $color
        } elseif {[regexp {^#([a-zA-Z]+[0-9a-zA-Z]*)$} $field match color]} {
          set gcolor $color
        } elseif {[regexp {^([-0-9.e]*)$} $field match num]} {
          set ganalog 1
          if {$gymin == ""} {
            set gymin $num
          } else {
            set gymax $num
          }
        }
      }
      if {$ganalog} {
        set gradix  ""
        set overlay 1
        set gicolor 0
        set gstart  1
      }
      if {[group find -match exact -name $group] != ""} {group delete $group}
      group new -name $group -overlay $overlay
      set gid [waveform add -groups [list $group]]
    }
  } else {
    set fields [split $signal :]
    set signal [lindex $fields 0]
    set fields [lrange $fields 1 end]
    set sanalog 0
    set scolor  ""
    set sradix  ""
    set strace  ""
    set symin   ""
    set symax   ""
    foreach field $fields {
      if {[regexp {^(%.)$} $field match radix]} {
        set sradix $radix
      } elseif {[regexp {^(#[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F])$} $field match color]} {
        set scolor $color
      } elseif {[regexp {^#([a-zA-Z]+[0-9a-zA-Z]*)$} $field match color]} {
        set scolor $color
      } elseif {$field == "^"} {
        set sanalog 1
        set strace  analogSampleAndHold
      } elseif {$field == "~"} {
        set sanalog 1
        set strace  analogLinear
      } elseif {[regexp {^([-0-9.e]*)$} $field match num]} {
        set sanalog 1
        if {$symin == ""} {
          set symin $num
        } else {
          set symax $num
        }
      }
    }
    if {$sanalog} {
      set sradix ""
      if {$symin  == ""} {set symin 0}
      if {$symax  == ""} {set symax 0}
      if {$strace == ""} {set strace analogSampleAndHold}
    } else {
      if  {$sradix != ""} {
        set radix $sradix
      } elseif {$gradix != "" && $group != ""} {
        set radix $gradix
      } else {
        set radix %b
      }
    }
    if {$subckt != ""} {set signal $subckt.$signal}
    #-------------------------------------------------------------------------
    # takes too much time:
    #-------------------------------------------------------------------------
    #   if {[dbfind find -name $scope.$signal] == ""} {continue}
    #-------------------------------------------------------------------------
    # within top-level group
    #-------------------------------------------------------------------------
    if {$group == ""} {
      set id [waveform add -signals [list $scope.$signal]]
      if {$sanalog} {
        if {$symin < $symax}  {
          waveform axis range $id -min $symin -max $symax -scale linear
        }
        if {$strace != ""}  {
          waveform format $id -trace $strace
        }
        waveform format $id -height $analogheight
      } else {
        if {$radix != ""} {
          waveform format $id -radix $radix
        }
      }
      if {$scolor != ""} {
        waveform format $id -color $scolor
      }
    #-------------------------------------------------------------------------
    # within sub group
    #-------------------------------------------------------------------------
    } else {
      group insert $scope.$signal
      set id [lrange [waveform hierarchy contents $gid] end end]
      if {$overlay} {
        if {$scolor != ""} {
          set color $scolor
        } elseif {$gcolor != ""} {
          set color $gcolor
        } else {
          set color   [lindex $colors $gicolor]
          set gicolor [expr ($gicolor+1)%[llength $colors]]
        }
        waveform format $id -color $color
        if {$ganalog && $gstart} {
          waveform axis range $gid -min $gymin -max $gymax -scale linear
          if {$gymin < $gymax}  {
            waveform axis range $gid -min $gymin -max $gymax -scale linear
          }
          if {$strace != ""}  {
            waveform format $id -trace $strace
          }
          waveform format $id -height $analogheight
          set gstart 0
        }
      } else {
        if {$sanalog} {
          if {$symin < $symax}  {
            waveform axis range $id -min $symin -max $symax -scale linear
          }
          if {$strace != ""} {
            waveform format $id -trace $strace
          }
          waveform format $id -height $analogheight
        } else {
          if {$radix != ""} {
            waveform format $id -radix $radix
          }
        }
        if {$scolor != ""} {
          waveform format $id -color $scolor
        }
      }
    }
  }
}
