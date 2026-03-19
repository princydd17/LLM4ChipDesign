module sequence_detector(
  input  logic clk,
  input  logic rst_n,
  input  logic [2:0] data,
  output logic seq_found
);

  // States of the FSM
  enum logic [3:0] {IDLE, DETECT_001, DETECT_101, DETECT_110, DETECT_000, DETECT_110_1, DETECT_110_2, DETECT_011, DETECT_101_1} state, next_state;

  // State register
  logic [3:0] current_state;

  // Sequence register
  logic [2:0] seq_reg [9:0];

  // Reset state
  assign current_state = (rst_n) ? IDLE : 4'b0000;

  // Next-state logic
  always_comb begin
    case (current_state)
      IDLE: next_state = (data == 3'b001) ? DETECT_001 : IDLE;
      DETECT_001: next_state = (data == 3'b101) ? DETECT_101 : IDLE;
      DETECT_101: next_state = (data == 3'b110) ? DETECT_110 : IDLE;
      DETECT_110: next_state = (data == 3'b000) ? DETECT_000 : IDLE;
      DETECT_000: next_state = (data == 3'b110) ? DETECT_110_1 : IDLE;
      DETECT_110_1: next_state = (data == 3'b110) ? DETECT_110_2 : IDLE;
      DETECT_110_2: next_state = (data == 3'b011) ? DETECT_011 : IDLE;
      DETECT_011: next_state = (data == 3'b101) ? DETECT_101_1 : IDLE;
      DETECT_101_1: next_state = IDLE;
      default: next_state = IDLE;
    endcase
  end

  // State register
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) current_state <= IDLE;
    else current_state <= next_state;
  end

  // Sequence register
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      for (int i = 0; i < 10; i++) seq_reg[i] <= 3'b000;
    end else begin
      seq_reg[0] <= data;
      for (int i = 1; i < 10; i++) seq_reg[i] <= seq_reg[i-1];
    end
  end

  // seq_found output
  assign seq_found = (current_state == DETECT_101_1) ? 1'b1 : 1'b0;

endmodule
