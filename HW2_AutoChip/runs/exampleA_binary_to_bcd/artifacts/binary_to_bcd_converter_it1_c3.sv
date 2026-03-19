module binary_to_bcd_converter(
    input  [4:0] binary_input,
    output [7:0] bcd_output
);

    assign bcd_output = {binary_input[4], binary_input[3], binary_input[2], binary_input[1], binary_input[0], 0, 0, 0};

endmodule
