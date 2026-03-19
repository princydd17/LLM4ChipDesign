module sequence_detector(
  input  wire  clk,
  input  wire  rst_n,
  input  wire  [2:0] data,
  output wire  seq_found
);

  // Define the states
  enum logic [2:0] {
    S0, S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, S12
  } state, next_state;

  // Reset state to S0
  initial state = S0;

  // Next-state logic
  always @(*) begin
    case (state)
      S0: next_state = (data == 3'b001) ? S1 : S0;
      S1: next_state = (data == 3'b101) ? S2 : S0;
      S2: next_state = (data == 3'b110) ? S3 : S0;
      S3: next_state = (data == 3'b000) ? S4 : S0;
      S4: next_state = (data == 3'b110) ? S5 : S0;
      S5: next_state = (data == 3'b110) ? S6 : S0;
      S6: next_state = (data == 3'b011) ? S7 : S0;
      S7: next_state = (data == 3'b101) ? S8 : S0;
      S8: next_state = S9;  // seq_found is asserted here
      S9: next_state = S10; // seq_found remains high for 1 cycle
      S10: next_state = S0;
      S11: next_state = S0; // unreachable state
      S12: next_state = S0; // unreachable state
      default: next_state = S0;
    endcase
  end

  // State register
  always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
      state <= S0;
    else
      state <= next_state;
  end

  // Output logic
  assign seq_found = (state == S9);

endmodule
