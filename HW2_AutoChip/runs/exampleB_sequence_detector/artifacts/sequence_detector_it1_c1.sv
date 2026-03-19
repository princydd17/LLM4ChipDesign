```verilog
module sequence_detector(
  input  logic clk,
  input  logic rst_n,
  input  logic [2:0] data,
  output logic seq_found
);

  logic [2:0] seq_reg;
  logic [2:0] seq_next;
  logic [6:0] state;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      seq_reg <= 3'b000;
      state <= 7'b0000000;
    end else begin
      seq_reg <= seq_next;
      state <= state + 1;
      if (state == 7'b1101110) seq_found <= 1'b1;
      else seq_found <= 1'b0;
    end
  end

  always_comb begin
    case (state)
      7'b0000000: seq_next = seq_reg;
      7'b0000001: seq_next = seq_reg;
      7'b0000010: seq_next = seq_reg;
      7'b0000011: seq_next = seq_reg;
      7'b0000100: seq_next = seq_reg;
      7'b0000101: seq_next = seq_reg;
      7'b0000110: seq_next = seq_reg;
      7'b0000111: seq_next = seq_reg;
      7'b0001000: seq_next = seq_reg;
      7'b0001001: seq_next = seq_reg;
      7'b0001010: seq_next = seq_reg;
      7'b0001011: seq_next = seq_reg;
      7'b0001100: seq_next = seq_reg;
      7'b0001101: seq_next = seq_reg;
      7'b0001110: seq_next = seq_reg;
      7'b0001111: seq_next = seq_reg;
      7'b0010000: seq_next = seq_reg;
      7'b0010001: seq_next = seq_reg;
      7'b0010010: seq_next = seq_reg;
      7'b0010011: seq_next = seq_reg;
      7'b0010100: seq_next = seq_reg;
      7'b0010101: seq_next = seq_reg;
      7'b0010110: seq_next = seq_reg;
      7'b0010111: seq_next = seq_reg;
      7'b0011000: seq_next = seq_reg;
      7'b0011001: seq_next = seq_reg;
      7'b0011010: seq_next = seq_reg;
      7'b0011011: seq_next = seq_reg;
      7'b0011100: seq_next = seq_reg;
      7'b0011101: seq_next = seq_reg;
      7'b0011110: seq_next = seq_reg;
      7'b0011111: seq_next = seq_reg;
      7'b0100000: seq_next = seq_reg;
      7'b0100001: seq_next = seq_reg;
      7'b0100010: seq_next = seq_reg;
      7'b0100011: seq_next = seq_reg;
      7'b0100100: seq_next = seq_reg;
      7'b0100101: seq_next = seq_reg;
      7'b0100110: seq_next = seq_reg;
      7'b0100111: seq_next = seq_reg;
      7'b0101000: seq_next = seq_reg;
      7'b0101001: seq_next = seq_reg;
      7'b0101010: seq_next = seq_reg;
      7'b0101011: seq_next = seq_reg;
      7'b0101100: seq_next = seq_reg;
      7'b0101101: seq_next = seq_reg;
      7'b0101110: seq_next = seq_reg;
      7'b0101111: seq_next = seq_reg;
      7'b0110000: seq_next = seq_reg;
      7'b0110001: seq_next = seq_reg;
      7'b0110010: seq_next = seq_reg;
      7'b0110011: seq_next = seq_reg;
      7'b0110100: seq_next = seq_reg;
      7'b0110101: seq_next = seq_reg;
      7'b0110110: seq_next = seq_reg;
      7'b0110111: seq_next = seq_reg;
      7'b0111000: seq_next = seq_reg;
      7'b0111001: seq_next = seq_reg;
      7'b0111010: seq_next = seq_reg;
      7'b0111011: seq_next = seq_reg;
      7'b0111100: seq_next = seq_reg;
      7'b0111101: seq_next = seq_reg;
      7'b0111110: seq_next = seq_reg;
      7'b0111111: seq_next = seq_reg;
      7'b1000000: seq_next = seq_reg;
      7'b1000001: seq_next = seq_reg;
      7'b1000010: seq_next = seq_reg;
      7'b1000011: seq_next = seq_reg;
      7'b1000100: seq_next = seq_reg;
      7'b1000101: seq_next = seq_reg;
      7'b1000110: seq_next = seq_reg;
      7'b1000111: seq_next = seq_reg;
      7'b1001000: seq_next = seq_reg;
      7'b1001001: seq_next = seq_reg;
      7'b1001010: seq_next = seq_reg;
      7'b1001011: seq_next = seq_reg;
      7'b1001100: seq_next = seq_reg;
      7'b1001101: seq_next = seq_reg;
      7'b1001110: seq_next = seq_reg;
      7'b1001111: seq_next = seq_reg;
      7'b1010000: seq_next = seq_reg;
      7'b1010001: seq_next = seq_reg;
      7'b1010010: seq_next = seq_reg;
      7'b1010011: seq_next = seq_reg;
      7'b1010100: seq_next = seq_reg;
      7'b1010101: seq_next = seq_reg;
      7'b1010110: seq_next = seq_reg;
      7'b101011
