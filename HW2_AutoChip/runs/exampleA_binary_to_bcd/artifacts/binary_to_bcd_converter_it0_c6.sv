module binary_to_bcd_converter (
  input  wire [4:0]  bin_in,
  output reg [7:0]  bcd_out
);

  reg [7:0]  bcd_reg;
  reg [4:0]  bin_work;

  initial begin
    bcd_reg = 8'b0;
    bin_work = bin_in;
  end

  always @(*) begin
    for (int i = 0; i < 5; i++) begin
      if ((bcd_reg[3:0] >= 5'b01000) && (bcd_reg[3:0] < 5'b10000)) begin
        bcd_reg[3:0] = bcd_reg[3:0] + 5'b00011;
      end
      if ((bcd_reg[7:4] >= 5'b01000) && (bcd_reg[7:4] < 5'b10000)) begin
        bcd_reg[7:4] = bcd_reg[7:4] + 5'b00011;
      end
      {bcd_reg, bin_work} = {bcd_reg[7:0], bin_work} << 1;
    end
  end

  assign bcd_out = bcd_reg;

endmodule
