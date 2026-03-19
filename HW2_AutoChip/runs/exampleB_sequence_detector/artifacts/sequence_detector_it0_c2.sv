module sequence_detector(
  input  wire         clk,
  input  wire         rst_n,
  input  wire [2:0]   data,
  output reg          seq_found
);

// Define states for the FSM
localparam [3:0] IDLE = 4'd0;
localparam [3:0] STATE_1 = 4'd1;
localparam [3:0] STATE_2 = 4'd2;
localparam [3:0] STATE_3 = 4'd3;
localparam [3:0] STATE_4 = 4'd4;
localparam [3:0] STATE_5 = 4'd5;
localparam [3:0] STATE_6 = 4'd6;
localparam [3:0] STATE_7 = 4'd7;

// State register and next-state logic
reg [3:0] state;

always @(posedge clk) begin
  if (!rst_n) begin
    state <= IDLE;
    seq_found <= 1'b0;
  end else begin
    case (state)
      IDLE: begin
        if (data == 3'd1)
          state <= STATE_1;
      end
      STATE_1: begin
        if (data == 3'd0)
          state <= STATE_2;
      end
      STATE_2: begin
        if (data == 3'd1)
          state <= STATE_3;
      end
      STATE_3: begin
        if (data == 3'd1)
          state <= STATE_4;
      end
      STATE_4: begin
        if (data == 3'd0)
          state <= STATE_5;
      end
      STATE_5: begin
        if (data == 3'd1)
          state <= STATE_6;
      end
      STATE_6: begin
        if (data == 3'd1)
          state <= STATE_7;
      end
      STATE_7: begin
        if (data == 3'd0)
          state <= IDLE;
        else if (data == 3'd1)
          state <= STATE_2;
        else if (data == 3'd0)
          state <= STATE_3;
        else if (data == 3'd1)
          state <= STATE_4;
        else if (data == 3'd1)
          state <= STATE_5;
        else if (data == 3'd0)
          state <= STATE_6;
        else if (data == 3'd1)
          state <= STATE_7;
        else if (data == 3'd0)
          state <= STATE_3;
        else if (data == 3'd1)
          state <= STATE_4;
        else if (data == 3'd1)
          state <= STATE_5;
        else if (data == 3'd1)
          state <= STATE_6;
        else if (data == 3'd0)
          state <= STATE_7;
        else
          state <= IDLE;
        seq_found <= data == 3'd1 ? 1'b1 : 1'b0;
        seq_found <= seq_found & (state == STATE_7);
        seq_found <= seq_found | (state == STATE_2) | (state == STATE_3) | (state == STATE_4) | (state == STATE_5) | (state == STATE_6);
      end
      default: state <= IDLE;
    endcase
  end
end

endmodule
