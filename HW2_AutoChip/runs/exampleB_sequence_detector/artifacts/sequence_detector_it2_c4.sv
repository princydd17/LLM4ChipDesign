module sequence_detector(
  input  wire clk,
  input  wire rst_n,
  input  wire [2:0] data,
  output reg seq_found
);

  // State register
  enum logic [4:0] {
    IDLE,
    DETECT_001,
    DETECT_101,
    DETECT_110,
    DETECT_000,
    DETECT_110_1,
    DETECT_110_2,
    DETECT_011,
    DETECT_101_1,
    DONE
  } current_state, next_state;

  // Next-state logic
  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      current_state <= IDLE;
      seq_found <= 1'b0;
    end else begin
      case (current_state)
        IDLE: current_state <= (data == 3'b001) ? DETECT_001 : IDLE;
        DETECT_001: current_state <= (data == 3'b101) ? DETECT_101 : IDLE;
        DETECT_101: current_state <= (data == 3'b110) ? DETECT_110 : IDLE;
        DETECT_110: current_state <= (data == 3'b000) ? DETECT_000 : IDLE;
        DETECT_000: current_state <= (data == 3'b110) ? DETECT_110_1 : IDLE;
        DETECT_110_1: current_state <= (data == 3'b110) ? DETECT_110_2 : IDLE;
        DETECT_110_2: current_state <= (data == 3'b011) ? DETECT_011 : IDLE;
        DETECT_011: current_state <= (data == 3'b101) ? DETECT_101_1 : IDLE;
        DETECT_101_1: current_state <= DONE;
        DONE: current_state <= DONE;
        default: current_state <= IDLE;
      endcase
    end
  end

  // Output logic
  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      seq_found <= 1'b0;
    end else begin
      case (current_state)
        DONE: seq_found <= 1'b1;
        default: seq_found <= 1'b0;
      endcase
    end
  end

endmodule
