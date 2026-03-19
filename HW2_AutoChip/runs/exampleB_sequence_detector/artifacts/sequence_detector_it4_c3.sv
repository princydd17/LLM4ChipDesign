module sequence_detector (
  input  wire clk,
  input  wire rst_n,
  input  wire [2:0] data,
  output reg seq_found
);

  localparam IDLE = 3'd0,
             SEQ_001 = 3'd1,
             SEQ_101 = 3'd2,
             SEQ_110 = 3'd3,
             SEQ_000 = 3'd4,
             SEQ_110_1 = 3'd5,
             SEQ_110_2 = 3'd6,
             SEQ_011 = 3'd7,
             SEQ_101_1 = 3'd8;

  reg [2:0] state;
  reg [2:0] next_state;

  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state <= IDLE;
    end else begin
      state <= next_state;
    end
  end

  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      seq_found <= 1'b0;
    end else begin
      case (state)
        IDLE: next_state = (data == 3'b001) ? SEQ_001 : IDLE;
        SEQ_001: next_state = (data == 3'b101) ? SEQ_101 : IDLE;
        SEQ_101: next_state = (data == 3'b110) ? SEQ_110 : IDLE;
        SEQ_110: next_state = (data == 3'b000) ? SEQ_000 : IDLE;
        SEQ_000: next_state = (data == 3'b110) ? SEQ_110_1 : IDLE;
        SEQ_110_1: next_state = (data == 3'b110) ? SEQ_110_2 : IDLE;
        SEQ_110_2: next_state = (data == 3'b011) ? SEQ_011 : IDLE;
        SEQ_011: next_state = (data == 3'b101) ? SEQ_101_1 : IDLE;
        SEQ_101_1: next_state = (data == 3'b101) ? (seq_found = 1'b1, IDLE) : IDLE;
      endcase
    end
  end

endmodule
