module sequence_detector(
  input  logic clk,
  input  logic rst_n,
  input  logic [2:0] data,
  output logic seq_found
);

  logic [6:0] state;
  logic [6:0] next_state;
  logic found;

  always_comb begin
    case (state)
      7'd0: next_state = (data == 3'd1) ? 7'd1 : 7'd0;
      7'd1: next_state = (data == 3'd0) ? 7'd2 : 7'd1;
      7'd2: next_state = (data == 3'd1) ? 7'd3 : 7'd2;
      7'd3: next_state = (data == 3'd1) ? 7'd4 : 7'd3;
      7'd4: next_state = (data == 3'd0) ? 7'd5 : 7'd4;
      7'd5: next_state = (data == 3'd1) ? 7'd6 : 7'd5;
      7'd6: next_state = (data == 3'd1) ? 7'd7 : 7'd6;
      7'd7: next_state = (data == 3'd0) ? 7'd0 : 7'd7;
      default: next_state = 7'd0;
    endcase

    found = (state == 7'd7);
  end

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state <= 7'd0;
    end else begin
      state <= next_state;
    end
  end

  assign seq_found = found;

endmodule
