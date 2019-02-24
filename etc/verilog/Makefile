##############################################################################
# NAME    : Makefile
# PURPOSE : Makefile for synthesis project
# AUTHOR  : Richard Booth
# DATE    : Mon Oct 16 09:47:36 EDT 2006
# ---------------------------------------------------------------------------
# NOTES :
#   project-specific definitions:
#     PROJ : project name
#     CELL : synthesize cell name
#     DEFS : specific verilog compiler defines (ex. +define+OUTPUT)
#   technology-specific definitions:
#     TECH  : technology name
#     VLLIB : standard-cell library
##############################################################################
RCAD  = ~/.DeCiDa/verilog
PROJ  = trane
CELL  = dr_dig
DEFS  = +define+OUTPUT +define+UNIT_DELAY
#	-y $(RCAD)/behavioral/verilog
#	-y _pandr
#	+nctimescale+10ps/10fs
#	+ncsdf_cmd_file+sdf.SLOW.cmd +sdf_verbose
include $(RCAD)/make/make.$(PROJ)
include $(RCAD)/make/make_body
