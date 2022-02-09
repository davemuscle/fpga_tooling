########################################################
# Quartus Build Source Files
# RTL
sv_list   = ../rtl/file.sv
v_list    = 
vhd_list  = 
top  = top
# TCL/QSF
tcl_list = pins.qsf
# Qsys
qsys_list =
# SDC
sdc_list = timing.sdc

########################################################
# Project Details
family  = "MAX 10"
device  = 10M50DAF484C6GES
prj     = my_project
prj_dir = prj
pathfix = ../

########################################################
# Build Recipes

.PHONY: build
build:
	mkdir -p $(prj_dir)
	echo "$$tcl_script" > $(prj_dir)/$@.tcl
	cd $(prj_dir) && \
	quartus_sh -t $@.tcl && \
	quartus_map $(prj) && \
	quartus_fit $(prj) && \
	quartus_asm $(prj) && \
	quartus_sta $(prj)
	$(MAKE) summary

.PHONY: summary
summary:
	@echo ""
	@echo "*** Build Summary ***"
	@grep "logic elements" $(prj_dir)/$(prj).fit.summary
	@grep "combinational functions" $(prj_dir)/$(prj).fit.summary
	@grep "logic registers" $(prj_dir)/$(prj).fit.summary
	@grep "memory bits" $(prj_dir)/$(prj).fit.summary
	@grep "Multiplier" $(prj_dir)/$(prj).fit.summary
	@grep "PLL" $(prj_dir)/$(prj).fit.summary
	@grep "Total pins" $(prj_dir)/$(prj).fit.summary
	@echo ""
	@echo "*** Build Complete ***"
	@echo "Instances Failing Timing: `grep -c "TNS.*:.*-" $(prj_dir)/$(prj).sta.summary`"
	@echo ""

.PHONY: prog
prog:
	quartus_pgm -m jtag -o "p;$(prj_dir)/$(prj).sof"

.PHONY: clean
clean:
	rm -rf $(prj_dir)

########################################################
# Project Setup Script

define tcl_script
project_new $(prj) -overwrite
set_global_assignment -name FAMILY $(family)
set_global_assignment -name DEVICE $(device)
set_global_assignment -name TOP_LEVEL_ENTITY $(top)
foreach i {$(addprefix $(pathfix),$(sv_list))}   {set_global_assignment -name SYSTEMVERILOG_FILE $$i}
foreach i {$(addprefix $(pathfix),$(v_list))}    {set_global_assignment -name VERILOG_FILE $$i}
foreach i {$(addprefix $(pathfix),$(vhd_list))}  {set_global_assignment -name VHDL_FILE $$i}
foreach i {$(addprefix $(pathfix),$(qsys_list))} {set_global_assignment -name QSYS_FILE $$i}
foreach i {$(addprefix $(pathfix),$(sdc_list))}  {set_global_assignment -name SDC_FILE $$i}
foreach i {$(addprefix $(pathfix),$(tcl_list))}  {set_global_assignment -name SOURCE_TCL_SCRIPT $$i}
endef
export tcl_script
