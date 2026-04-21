# Timing constraints for ABC (Part 3). Tune period / delays per your project.
create_clock -name clk -period 2.0
set_input_delay 0.2 -clock clk [all_inputs]
set_output_delay 0.2 -clock clk [all_outputs]
