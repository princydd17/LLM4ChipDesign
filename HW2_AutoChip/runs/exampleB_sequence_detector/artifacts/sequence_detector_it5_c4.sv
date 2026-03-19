module sequence_detector (
  input  wire  clk,
  input  wire  rst_n,
  input  wire  [2:0] data,
  output reg   seq_found
);

reg [3:0] state;
reg [2:0] seq_count;

always @(posedge clk) begin
  if (!rst_n) begin
    state <= 4'd0;
    seq_count <= 3'd0;
    seq_found <= 1'b0;
  end else begin
    case (state)
      4'h0: begin
        if (data == 3'h1)
          state <= 4'h1;
        else
          state <= 4'h0;
      end
      4'h1: begin
        if (data == 3'h0)
          state <= 4'h2;
        else
          state <= 4'h0;
      end
      4'h2: begin
        if (data == 3'h1)
          state <= 4'h3;
        else
          state <= 4'h0;
      end
      4'h3: begin
        if (data == 3'h0)
          state <= 4'h4;
        else
          state <= 4'h0;
      end
      4'h4: begin
        if (data == 3'h1)
          state <= 4'h5;
        else if (data == 3'h1)
          state <= 4'h5;
        else
          state <= 4'h0;
      end
      4'h5: begin
        if (data == 3'h1)
          state <= 4'h6;
        else if (data == 3'h0)
          state <= 4'h7;
        else
          state <= 4'h0;
      end
      4'h6: begin
        if (data == 3'h1)
          state <= 4'h8;
        else
          state <= 4'h0;
      end
      4'h7: begin
        if (data == 3'h0)
          state <= 4'h8;
        else
          state <= 4'h0;
      end
      4'h8: begin
        if (data == 3'h1)
          state <= 4'h9;
        else if (data == 3'h1)
          state <= 4'h9;
        else
          state <= 4'h0;
      end
      4'h9: begin
        if (data == 3'h0)
          state <= 4'ha;
        else
          state <= 4'h0;
      end
      4'ha: begin
        if (data == 3'h1)
          state <= 4'hb;
        else if (data == 3'h1)
          state <= 4'hb;
        else
          state <= 4'h0;
      end
      4'hb: begin
        if (data == 3'h0)
          state <= 4'hc;
        else
          state <= 4'h0;
      end
      4'hc: begin
        if (data == 3'h1)
          state <= 4'hd;
        else
          state <= 4'h0;
      end
      4'hd: begin
        if (data == 3'h1)
          state <= 4'he;
        else if (data == 3'h0)
          state <= 4'hf;
        else
          state <= 4'h0;
      end
      4'he: begin
        if (data == 3'h0)
          state <= 4'hf;
        else
          state <= 4'h0;
      end
      4'hf: begin
        if (data == 3'h1)
          state <= 4'10;
        else if (data == 3'h1)
          state <= 4'10;
        else
          state <= 4'h0;
      end
      default: state <= 4'h0;
    endcase

    case (state)
      4'h5: seq_count <= 3'd1;
      4'h6: seq_count <= 3'd2;
      4'h7: seq_count <= 3'd3;
      4'h8: seq_count <= 3'd4;
      4'h9: seq_count <= 3'd5;
      4'ha: seq_count <= 3'd6;
      4'hb: seq_count <= 3'd7;
      4'hc: seq_count <= 3'd8;
      4'hd: seq_count <= 3'd9;
      4'he: seq_count <= 3'd10;
      4'hf: seq_count <= 3'd11;
      default: seq_count <= 3'd0;
    endcase

    if (seq_count == 11'd11)
      seq_found <= 1'b1;
    else
      seq_found <= 1'b0;
  end
end

endmodule
