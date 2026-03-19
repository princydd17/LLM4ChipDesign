module sequence_detector(
  input  logic clk,
  input  logic rst_n,
  input  logic [2:0] data,
  output logic seq_found
);

logic [2:0] state_reg;
logic [2:0] next_state;
logic [7:0] seq_index;
logic seq_found_reg;

always_ff @(posedge clk or negedge rst_n) begin
  if (!rst_n) begin
    state_reg <= 3'b000;
    seq_index <= 8'b00000000;
  end else begin
    state_reg <= next_state;
    seq_index <= seq_index + 1;
  end
end

always_comb begin
  case (state_reg)
    3'b000: begin
      if (seq_index == 8'b00000000) next_state = 3'b001;
      else if (seq_index == 8'b00000001) next_state = 3'b101;
      else if (seq_index == 8'b00000010) next_state = 3'b110;
      else if (seq_index == 8'b00000011) next_state = 3'b000;
      else if (seq_index == 8'b00000100) next_state = 3'b110;
      else if (seq_index == 8'b00000101) next_state = 3'b110;
      else if (seq_index == 8'b00000110) next_state = 3'b011;
      else if (seq_index == 8'b00000111) next_state = 3'b101;
      else next_state = 3'b000;
    end
    3'b001: begin
      if (seq_index == 8'b00000001) next_state = 3'b101;
      else if (seq_index == 8'b00000010) next_state = 3'b110;
      else if (seq_index == 8'b00000011) next_state = 3'b000;
      else if (seq_index == 8'b00000100) next_state = 3'b110;
      else if (seq_index == 8'b00000101) next_state = 3'b110;
      else if (seq_index == 8'b00000110) next_state = 3'b011;
      else if (seq_index == 8'b00000111) next_state = 3'b101;
      else next_state = 3'b000;
    end
    3'b101: begin
      if (seq_index == 8'b00000010) next_state = 3'b110;
      else if (seq_index == 8'b00000011) next_state = 3'b000;
      else if (seq_index == 8'b00000100) next_state = 3'b110;
      else if (seq_index == 8'b00000101) next_state = 3'b110;
      else if (seq_index == 8'b00000110) next_state = 3'b011;
      else if (seq_index == 8'b00000111) next_state = 3'b101;
      else next_state = 3'b000;
    end
    3'b110: begin
      if (seq_index == 8'b00000011) next_state = 3'b000;
      else if (seq_index == 8'b00000100) next_state = 3'b110;
      else if (seq_index == 8'b00000101) next_state = 3'b110;
      else if (seq_index == 8'b00000110) next_state = 3'b011;
      else if (seq_index == 8'b00000111) next_state = 3'b101;
      else next_state = 3'b000;
    end
    3'b000: begin
      if (seq_index == 8'b00000111) next_state = 3'b000;
      else next_state = 3'b000;
    end
    3'b011: begin
      if (seq_index == 8'b00000111) next_state = 3'b101;
      else next_state = 3'b000;
    end
    default: next_state = 3'b000;
  endcase

  case (state_reg)
    3'b000: seq_found_reg = (seq_index == 8'b00000111) ? 1'b1 : 1'b0;
    3'b001: seq_found_reg = (seq_index == 8'b00000010) ? 1'b1 : 1'b0;
    3'b101: seq_found_reg = (seq_index == 8'b00000011) ? 1'b1 : 1'b0;
    3'b110: seq_found_reg = (seq_index == 8'b00000011) ? 1'b1 : 1'b0;
    3'b011: seq_found_reg = (seq_index == 8'b00000111) ? 1'b1 : 1'b0;
    default: seq_found_reg = 1'b0;
  endcase
end

assign seq_found = seq_found_reg;
