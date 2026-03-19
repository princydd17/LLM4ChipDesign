module sequence_detector (
  input  wire  clk,
  input  wire  rst_n,
  input  wire  [2:0] data,
  output reg   seq_found
);

// Define states for the FSM
typedef enum {
  IDLE,
  STATE_001,
  STATE_101,
  STATE_110,
  STATE_000,
  STATE_1101,
  STATE_1102,
  STATE_011,
  STATE_1011
} state_t;

// State register and next-state logic
state_t state, next_state;

always @(posedge clk or negedge rst_n) begin
  if (!rst_n) begin
    state <= IDLE;
    seq_found <= 1'b0;
  end else begin
    state <= next_state;
  end
end

// Next-state logic
always @(*) begin
  case (state)
    IDLE: begin
      if (data == 3'b001) next_state = STATE_001;
      else if (data == 3'b101) next_state = STATE_101;
      else if (data == 3'b110) next_state = STATE_110;
      else if (data == 3'b000) next_state = STATE_000;
      else next_state = IDLE;
    end
    STATE_001: begin
      if (data == 3'b101) next_state = STATE_101;
      else if (data == 3'b110) next_state = STATE_1101;
      else next_state = IDLE;
    end
    STATE_101: begin
      if (data == 3'b110) next_state = STATE_1102;
      else if (data == 3'b000) next_state = STATE_000;
      else next_state = IDLE;
    end
    STATE_110: begin
      if (data == 3'b000) next_state = STATE_000;
      else if (data == 3'b110) next_state = STATE_1101;
      else next_state = IDLE;
    end
    STATE_000: begin
      if (data == 3'b110) next_state = STATE_1102;
      else next_state = IDLE;
    end
    STATE_1101: begin
      if (data == 3'b110) next_state = STATE_1102;
      else next_state = IDLE;
    end
    STATE_1102: begin
      if (data == 3'b011) next_state = STATE_011;
      else if (data == 3'b101) next_state = STATE_1011;
      else next_state = IDLE;
    end
    STATE_011: begin
      if (data == 3'b101) next_state = STATE_1011;
      else next_state = IDLE;
    end
    STATE_1011: begin
      seq_found <= 1'b1;
      next_state = IDLE;
    end
  endcase
end

endmodule
