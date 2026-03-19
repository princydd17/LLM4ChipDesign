module binary_to_bcd_converter(
    input  [4:0] binary_input,
    output [7:0] bcd_output
);

    wire [4:0] tens_digit;
    wire [3:0] ones_digit;

    assign tens_digit = binary_input[4] ? {1'b1, binary_input[3:1]} : {1'b0, binary_input[4:1]};
    assign ones_digit = binary_input[4] ? {1'b0, binary_input[3:1]} : binary_input[4:1];
    assign bcd_output = {tens_digit, ones_digit};

endmodule
