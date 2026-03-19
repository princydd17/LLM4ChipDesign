module sequence_detector(
  input  wire clk,
  input  wire rst_n,
  input  wire [2:0] data,
  output reg seq_found
);

reg [2:0] state;
reg [2:0] next_state;
reg [7:0] sequence;

initial begin
  sequence = 8'h00; // 000
end

always @(posedge clk) begin
  if (!rst_n) begin
    state <= 3'b000;
    next_state <= 3'b000;
    seq_found <= 1'b0;
  end else begin
    state <= next_state;
    next_state <= 3'b000;

    case (state)
      3'b000: begin
        if (data == 3'b001) next_state <= 3'b001;
      end
      3'b001: begin
        if (data == 3'b101) next_state <= 3'b010;
      end
      3'b010: begin
        if (data == 3'b110) next_state <= 3'b011;
      end
      3'b011: begin
        if (data == 3'b000) next_state <= 3'b100;
      end
      3'b100: begin
        if (data == 3'b110) next_state <= 3'b101;
      end
      3'b101: begin
        if (data == 3'b110) next_state <= 3'b110;
      end
      3'b110: begin
        if (data == 3'b011) next_state <= 3'b111;
      end
      3'b111: begin
        if (data == 3'b101) next_state <= 3'b000;
        seq_found <= 1'b1;
      end
      default: next_state <= 3'b000;
    endcase
  end
end

endmodule
