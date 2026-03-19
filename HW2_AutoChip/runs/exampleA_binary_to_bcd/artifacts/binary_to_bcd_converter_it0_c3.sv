module binary_to_bcd_converter (
    input  [4:0] binary_input,
    output [7:0] bcd_output
);
    // Calculate 10's place BCD
    assign bcd_output[7:4] = (binary_input[4] ? 3 : 0) + (binary_input[3] ? 2 : 0) + (binary_input[2] ? 1 : 0);
    
    // Calculate 1's place BCD
    assign bcd_output[3:0] = (binary_input[1] ? 8 : 0) + (binary_input[0] ? 1 : 0);
    
endmodule
