module sequence_detector(
  input  wire clk,
  input  wire rst_n,
  input  wire [2:0] data,
  output wire seq_found
);

  reg [3:0] state;
  reg [2:0] prev_data;
  reg [2:0] curr_data;
  reg seq_found_r;

  always @(posedge clk) begin
    if (!rst_n) begin
      state <= 0;
      prev_data <= 0;
      curr_data <= 0;
      seq_found_r <= 0;
    end else begin
      prev_data <= data;
      case (state)
        4'd0: begin
          if (data == 3'b001)
            state <= 4'd1;
        end
        4'd1: begin
          if (data == 3'b101)
            state <= 4'd2;
        end
        4'd2: begin
          if (data == 3'b110)
            state <= 4'd3;
        end
        4'd3: begin
          if (data == 3'b000)
            state <= 4'd4;
        end
        4'd4: begin
          if (data == 3'b110)
            state <= 4'd5;
        end
        4'd5: begin
          if (data == 3'b110)
            state <= 4'd6;
        end
        4'd6: begin
          if (data == 3'b011)
            state <= 4'd7;
        end
        4'd7: begin
          if (data == 3'b101)
            state <= 4'd8;
        end
        default: state <= 4'd0;
      endcase

      case (state)
        4'd0, 4'd1, 4'd2, 4'd3, 4'd4, 4'd5, 4'd6, 4'd7: curr_data <= prev_data;
        4'd8: begin
          if (data == 3'b110)
            seq_found_r <= 1;
          else
            seq_found_r <= 0;
        end
        default: curr_data <= 0;
      endcase
    end
  end

  assign seq_found = seq_found_r;

endmodule
