// Manual binary-to-BCD converter for HW2 Part I(b)
// 5-bit unsigned binary -> 2-digit BCD {tens, ones} in bcd_out[7:4], bcd_out[3:0]

// Port names chosen to match the ChipChat/AutoChip testbench:
//   input  [4:0] binary_input;
//   output [7:0] bcd_output;

module binary_to_bcd_converter(
    input  [4:0] binary_input,
    output reg [7:0] bcd_output
);
    integer i;
    reg [7:0] bcd;
    reg [4:0] bin;

    always @* begin
        // initialize
        bcd = 8'd0;
        bin = binary_input;

        // Double-dabble (shift-add-3) algorithm for 5-bit input
        for (i = 0; i < 5; i = i + 1) begin
            // if any BCD digit >= 5, add 3
            if (bcd[3:0] >= 5)
                bcd[3:0] = bcd[3:0] + 3;
            if (bcd[7:4] >= 5)
                bcd[7:4] = bcd[7:4] + 3;

            // shift left and bring in next binary bit
            {bcd, bin} = {bcd, bin} << 1;
        end

        bcd_output = bcd;
    end

endmodule

