module binary_to_bcd_converter(
  input  wire [4:0] binary_in,
  output reg [7:0] bcd_out
);

  reg [7:0] bcd_reg;
  reg [4:0] binary_work;

  initial begin
    bcd_reg = 8'b0;
    binary_work = binary_in;
  end

  always_comb begin
    // Repeat 5 times
    for (int i = 0; i < 5; i++) begin
      // If low BCD digit >= 5, add 3
      if (bcd_reg[3:0] >= 5) begin
        bcd_reg[3:0] = bcd_reg[3:0] + 3;
      end

      // If high BCD digit >= 5, add 3
      if (bcd_reg[7:4] >= 5) begin
        bcd_reg[7:4] = bcd_reg[7:4] + 3;
      end

      // Shift left by 1 bit
      {bcd_reg, binary_work} = {bcd_reg[6:0], bcd_reg[7], binary_work[4:0], 1'b0};
    end

    // After 5 iterations, bcd_reg holds the correct tens and ones digits
    bcd_out = bcd_reg;
  end
endmodule
