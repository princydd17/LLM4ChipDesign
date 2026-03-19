module sequence_detector(
  input  wire logic clk,
  input  wire logic rst_n,
  input  wire logic [2:0] data,
  output wire logic seq_found
);

  // State register
  logic [4:0] state;

  // Next-state logic
  logic [4:0] next_state;

  // Sequence definition
  logic [7:0] seq = 8'b00110111000011011011;

  // FSM state definitions
  parameter IDLE   = 5'd0;
  parameter DETECT = 5'd1;
  parameter FOUND  = 5'd2;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state <= IDLE;
    end else begin
      state <= next_state;
    end
  end

  always_comb begin
    // Default next-state
    next_state = state;

    // Sequence detection logic
    case (state)
      IDLE: begin
        if (data == 3'b001) begin
          next_state = DETECT;
        end
      end
      DETECT: begin
        if (data == 3'b101) begin
          next_state = FOUND;
        end else if (data == 3'b110) begin
          next_state = DETECT;
        end
      end
      FOUND: begin
        if (data == 3'b110) begin
          next_state = FOUND;
        end else if (data == 3'b011) begin
          next_state = DETECT;
        end else if (data == 3'b101) begin
          next_state = DETECT;
        end else begin
          next_state = IDLE;
        end
      end
      default: next_state = IDLE;
    endcase
  end

  assign seq_found = (state == FOUND) ? 1'b1 : 1'b0;

endmodule
