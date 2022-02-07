##############################################################
# Generic Sim Using Modelsim

sim_list = file1.sv file2.sv
sim_tb = tb
sim_params = CLK=500, FEATURE=true

.PHONY: modelsim
modelsim:
	vlog $(sim_list)
	vsim -c $(addprefix -g, $(sim_params)) -do "run -all" $(sim_tb)

.PHONY: gui
gui:
	gtkwave -og dump.vcd &

.PHONY: clean
clean:
	rm -rf work
	rm -rf *.vcd *.fst
	rm -rf transcript
##############################################################
