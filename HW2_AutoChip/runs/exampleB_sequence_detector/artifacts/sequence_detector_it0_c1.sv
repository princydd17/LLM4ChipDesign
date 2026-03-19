module sequence_detector(
  input  logic clk,
  input  logic rst_n,
  input  logic [2:0] data,
  output logic seq_found
);

  // State register
  logic [6:0] state;

  // State machine next-state logic
  always_comb begin
    case (state)
      7'd0: // Initial state
        if (data == 3'b001) state = 7'd1;
        else state = 7'd0;
      7'd1: // State 1
        if (data == 3'b101) state = 7'd2;
        else state = 7'd0;
      7'd2: // State 2
        if (data == 3'b110) state = 7'd3;
        else state = 7'd0;
      7'd3: // State 3
        if (data == 3'b000) state = 7'd4;
        else state = 7'd0;
      7'd4: // State 4
        if (data == 3'b110) state = 7'd5;
        else state = 7'd0;
      7'd5: // State 5
        if (data == 3'b110) state = 7'd6;
        else state = 7'd0;
      7'd6: // State 6
        if (data == 3'b011) state = 7'd7;
        else state = 7'd0;
      7'd7: // State 7
        if (data == 3'b101) state = 7'd8;
        else state = 7'd0;
      7'd8: // Final state
        if (data == 3'b000) state = 7'd0;
        else state = 7'd0;
      default: state = 7'd0;
    endcase
  end

  // Output logic
  always_comb begin
    seq_found = 1'b0;
    case (state)
      7'd8: seq_found = 1'b1;
      default: seq_found = 1'b0;
    endcase
  end

  // Reset logic
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) state <= 7'd0;
    else state <= state;
  end

endmodule
