module binary_to_bcd_converter(
  input  wire [4:0] binary_input,
  output reg [7:0] bcd_output
);

  always @(binary_input)
    begin
      case (binary_input)
        5'b00000: bcd_output = 8'b00000000; // 0
        5'b00001: bcd_output = 8'b00000001; // 1
        5'b00010: bcd_output = 8'b00000010; // 2
        5'b00011: bcd_output = 8'b00000011; // 3
        5'b00100: bcd_output = 8'b00000100; // 4
        5'b00101: bcd_output = 8'b00000101; // 5
        5'b00110: bcd_output = 8'b00000110; // 6
        5'b00111: bcd_output = 8'b00000111; // 7
        5'b01000: bcd_output = 8'b00001000; // 8
        5'b01001: bcd_output = 8'b00001001; // 9
        default:  bcd_output = 8'b11111111; // invalid input
      endcase
    end
endmodule
