module sequence_detector (
  input  logic clk,
  input  logic rst_n,
  input  logic [2:0] data,
  output logic seq_found
);

  logic [6:0] state_reg, next_state;
  logic [2:0] data_reg;
  logic seq_match;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state_reg <= 7'b0000000;
      data_reg <= 3'b000;
    end else begin
      state_reg <= next_state;
      data_reg <= data;
    end
  end

  always_comb begin
    case (state_reg)
      7'b0000000: begin
        seq_match = 1'b0;
        next_state = 7'b0000001;
      end
      7'b0000001: begin
        seq_match = (data_reg == 3'b001);
        next_state = (data_reg == 3'b001) ? 7'b0000010 : 7'b0000002;
      end
      7'b0000010: begin
        seq_match = (data_reg == 3'b101);
        next_state = (data_reg == 3'b101) ? 7'b0000011 : 7'b0000010;
      end
      7'b0000011: begin
        seq_match = (data_reg == 3'b110);
        next_state = (data_reg == 3'b110) ? 7'b0000100 : 7'b0000010;
      end
      7'b0000100: begin
        seq_match = (data_reg == 3'b000);
        next_state = (data_reg == 3'b000) ? 7'b0000101 : 7'b0000010;
      end
      7'b0000101: begin
        seq_match = (data_reg == 3'b110);
        next_state = (data_reg == 3'b110) ? 7'b0000110 : 7'b0000101;
      end
      7'b0000110: begin
        seq_match = (data_reg == 3'b110);
        next_state = (data_reg == 3'b110) ? 7'b0000111 : 7'b0000101;
      end
      7'b0000111: begin
        seq_match = (data_reg == 3'b011);
        next_state = (data_reg == 3'b011) ? 7'b0001000 : 7'b0000111;
      end
      7'b0001000: begin
        seq_match = (data_reg == 3'b101);
        next_state = (data_reg == 3'b101) ? 7'b0001001 : 7'b0000111;
      end
      7'b0001001: begin
        seq_match = (data_reg == 3'b110);
        next_state = (data_reg == 3'b110) ? 7'b0001010 : 7'b0001001;
      end
      default: begin
        seq_match = 1'b0;
        next_state = 7'b0000000;
      end
    endcase
  end

  assign seq_found = seq_match & (state_reg == 7'b0001010);

endmodule
