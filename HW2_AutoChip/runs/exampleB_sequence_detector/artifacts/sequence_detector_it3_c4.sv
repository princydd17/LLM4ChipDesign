module sequence_detector(
  input  wire  clk,
  input  wire  rst_n,
  input  wire  [2:0] data,
  output reg   seq_found
);

  // State register
  enum logic [3:0] {
    START,
    STATE_1,
    STATE_2,
    STATE_3,
    STATE_4,
    STATE_5,
    STATE_6,
    STATE_7
  } current_state, next_state;

  // Next-state logic
  always_comb begin
    case (current_state)
      START: next_state = data == 3'b001 ? STATE_1 : START;
      STATE_1: next_state = data == 3'b101 ? STATE_2 : START;
      STATE_2: next_state = data == 3'b110 ? STATE_3 : START;
      STATE_3: next_state = data == 3'b000 ? STATE_4 : START;
      STATE_4: next_state = data == 3'b110 ? STATE_5 : START;
      STATE_5: next_state = data == 3'b110 ? STATE_6 : START;
      STATE_6: next_state = data == 3'b011 ? STATE_7 : START;
      STATE_7: next_state = data == 3'b101 ? START : STATE_7;
      default: next_state = START;
    endcase
  end

  // State register update
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      current_state <= START;
    end else begin
      current_state <= next_state;
    end
  end

  // Output logic
  always_comb begin
    seq_found = (current_state == STATE_7 && data == 3'b101);
  end

endmodule
