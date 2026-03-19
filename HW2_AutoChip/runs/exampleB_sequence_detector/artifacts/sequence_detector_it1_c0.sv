module sequence_detector(
  input  wire  clk,
  input  wire  rst_n,
  input  wire  [2:0] data,
  output reg   seq_found
);

reg [3:0] state;
reg [2:0] sequence [7:0] = {8{3'b000}};
reg [2:0] current_data;

always @(posedge clk) begin
  if (!rst_n) begin
    state <= 4'd0;
    seq_found <= 1'b0;
  end else begin
    case (state)
      4'd0: begin
        current_data <= data;
        state <= 4'd1;
      end
      4'd1: begin
        if (current_data == sequence[0]) begin
          state <= 4'd2;
        end else begin
          state <= 4'd0;
          current_data <= data;
        end
      end
      4'd2: begin
        if (current_data == sequence[1]) begin
          state <= 4'd3;
        end else begin
          state <= 4'd0;
          current_data <= data;
        end
      end
      4'd3: begin
        if (current_data == sequence[2]) begin
          state <= 4'd4;
        end else begin
          state <= 4'd0;
          current_data <= data;
        end
      end
      4'd4: begin
        if (current_data == sequence[3]) begin
          state <= 4'd5;
        end else begin
          state <= 4'd0;
          current_data <= data;
        end
      end
      4'd5: begin
        if (current_data == sequence[4]) begin
          state <= 4'd6;
        end else begin
          state <= 4'd0;
          current_data <= data;
        end
      end
      4'd6: begin
        if (current_data == sequence[5]) begin
          state <= 4'd7;
        end else begin
          state <= 4'd0;
          current_data <= data;
        end
      end
      4'd7: begin
        if (current_data == sequence[6]) begin
          state <= 4'd8;
        end else begin
          state <= 4'd0;
          current_data <= data;
        end
      end
      4'd8: begin
        if (current_data == sequence[7]) begin
          seq_found <= 1'b1;
          state <= 4'd0;
        end else begin
          state <= 4'd0;
          current_data <= data;
        end
      end
      default: state <= 4'd0;
    endcase
  end
end

endmodule
