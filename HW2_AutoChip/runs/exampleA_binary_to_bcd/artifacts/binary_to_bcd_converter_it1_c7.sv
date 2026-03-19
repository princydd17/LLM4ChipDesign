module binary_to_bcd_converter (
  input  logic [4:0] binary_input,
  output logic [7:0] bcd_output
);

  assign bcd_output = binary_input[4] ? {1'b1, 1'b0, binary_input[4:1], 3'b000} : {binary_input[4:0], 4'b0000};

endmodule
