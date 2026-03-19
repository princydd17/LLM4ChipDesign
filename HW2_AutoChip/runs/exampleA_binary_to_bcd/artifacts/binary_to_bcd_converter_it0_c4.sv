module binary_to_bcd_converter(
  input  [4:0] binary,
  output [7:0] bcd
);

  reg [7:0] bcd_reg;
  reg [4:0] working_binary;

  initial begin
    bcd_reg = 8'b0;
    working_binary = binary;
  end

  always @(*) begin
    // Repeat 5 times
    for (int i = 0; i < 5; i++) begin
      // Check if low BCD digit >= 5
      if (bcd_reg[3:0] >= 5'b1000) begin
        // Add 3 to low BCD digit
        bcd_reg[3:0] = (bcd_reg[3:0] + 3'b011) & 5'b1111;
      end

      // Check if high BCD digit >= 5
      if (bcd_reg[7:4] >= 5'b1000) begin
        // Add 3 to high BCD digit
        bcd_reg[7:4] = (bcd_reg[7:4] + 3'b011) & 5'b1111;
      end

      // Shift left by 1 bit
      bcd_reg = {bcd_reg[6:0], 1'b0};
      working_binary = {working_binary[4:0], 1'b0};
    end

    // Assign BCD output
    bcd = bcd_reg;
  end

endmodule
