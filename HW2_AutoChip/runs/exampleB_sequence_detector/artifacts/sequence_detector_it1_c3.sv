module sequence_detector (
  input  logic clk,
  input  logic rst_n,
  input  logic [2:0] data,
  output logic seq_found
);

  // Define the states for the FSM
  enum logic [2:0] { S_INIT, S_001, S_101, S_110, S_000, S_110_1, S_110_2, S_011, S_101_1 } state, next_state;

  // Initialize the state register
  logic [2:0] state_reg;

  // Define the next-state logic
  always_comb begin
    case (state)
      S_INIT: next_state = data == 3'b001 ? S_001 : S_INIT;
      S_001: next_state = data == 3'b101 ? S_101 : S_INIT;
      S_101: next_state = data == 3'b110 ? S_110 : S_INIT;
      S_110: next_state = data == 3'b000 ? S_000 : S_INIT;
      S_000: next_state = data == 3'b110 ? S_110_1 : S_INIT;
      S_110_1: next_state = data == 3'b110 ? S_110_2 : S_INIT;
      S_110_2: next_state = data == 3'b011 ? S_011 : S_INIT;
      S_011: next_state = data == 3'b101 ? S_101 : S_INIT;
      S_101_1: next_state = S_INIT;
      default: next_state = S_INIT;
    endcase
  end

  // Define the state register
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state_reg <= S_INIT;
    end else begin
      state_reg <= next_state;
    end
  end

  // Define the output logic
  always_comb begin
    case (state_reg)
      S_INIT: seq_found = 1'b0;
      S_001: seq_found = 1'b0;
      S_101: seq_found = 1'b0;
      S_110: seq_found = 1'b0;
      S_000: seq_found = 1'b0;
      S_110_1: seq_found = 1'b0;
      S_110_2: seq_found = 1'b0;
      S_011: seq_found = 1'b0;
      S_101_1: seq_found = 1'b1;
      default: seq_found = 1'b0;
    endcase
  end

endmodule
