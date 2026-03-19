module binary_to_bcd_converter (
    input  [4:0] binary_input,
    output [7:0] bcd_output
);
    // Calculate the 10's place
    wire [3:0] tens_place;
    assign tens_place[3] = (binary_input[4] == 1'b1) ? 1'b1 : 1'b0;
    assign tens_place[2] = (binary_input[4] == 1'b1 && binary_input[3] == 1'b1) ? 1'b1 : 1'b0;
    assign tens_place[1] = (binary_input[4] == 1'b1 && binary_input[3] == 1'b1 && binary_input[2] == 1'b1) ? 1'b1 : 1'b0;
    assign tens_place[0] = (binary_input[4] == 1'b1 && binary_input[3] == 1'b1 && binary_input[2] == 1'b1 && binary_input[1] == 1'b1) ? 1'b1 : 1'b0;

    // Calculate the 1's place
    wire [3:0] ones_place;
    assign ones_place[3] = (binary_input[4] == 1'b1 && binary_input[3] == 1'b1 && binary_input[2] == 1'b1 && binary_input[1] == 1'b1 && binary_input[0] == 1'b1) ? 1'b1 : 1'b0;
    assign ones_place[2] = (binary_input[4] == 1'b1 && binary_input[3] == 1'b1 && binary_input[2] == 1'b1 && binary_input[1] == 1'b1) ? 1'b1 : 1'b0;
    assign ones_place[1] = (binary_input[4] == 1'b1 && binary_input[3] == 1'b1 && binary_input[2] == 1'b1) ? 1'b1 : 1'b0;
    assign ones_place[0] = (binary_input[4] == 1'b1 && binary_input[3] == 1'b1) ? 1'b1 : 1'b0;

    // Assign outputs
    assign bcd_output[7:4] = tens_place;
    assign bcd_output[3:0] = ones_place;
endmodule
