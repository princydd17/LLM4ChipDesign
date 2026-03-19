module binary_to_bcd_converter (
    input  [4:0] binary_input,
    output [7:0] bcd_output
);
    // The BCD output is a 4-bit number for the 10's place and a 4-bit number for the 1's place
    // We'll use the binary input to calculate the 10's and 1's place digits
    wire [3:0] tens_digit;
    wire [3:0] ones_digit;

    // To convert binary to BCD, we need to split the binary input into two parts:
    // the 10's place and the 1's place. We'll use bitwise operations to achieve this.
    assign tens_digit = binary_input[4] ? 8'd3 : 8'd0;
    assign tens_digit = tens_digit + (binary_input[3] ? 8'd2 : 8'd0);
    assign tens_digit = tens_digit + (binary_input[2] ? 8'd1 : 8'd0);

    assign ones_digit = binary_input[1] ? 8'd3 : 8'd0;
    assign ones_digit = ones_digit + (binary_input[0] ? 8'd2 : 8'd0);

    // Now, we'll combine the 10's and 1's place digits to form the BCD output
    assign bcd_output[7:4] = tens_digit;
    assign bcd_output[3:0] = ones_digit;
endmodule
