module sequence_detector(
    input  wire clk,
    input  wire rst_n,
    input  wire [2:0] data,
    output reg seq_found
);

reg [2:0] state;
reg [2:0] seq [0:7];

initial begin
    seq[0] = 3'b001;
    seq[1] = 3'b101;
    seq[2] = 3'b110;
    seq[3] = 3'b000;
    seq[4] = 3'b110;
    seq[5] = 3'b110;
    seq[6] = 3'b011;
    seq[7] = 3'b101;
end

always @(posedge clk) begin
    if (!rst_n) begin
        state <= 3'b000;
        seq_found <= 1'b0;
    end else begin
        case (state)
            3'b000: if (data == seq[0]) state <= seq[0];
                      else state <= 3'b000;
            3'b001: if (data == seq[1]) state <= seq[1];
                      else state <= 3'b000;
            3'b010: if (data == seq[2]) state <= seq[2];
                      else state <= 3'b000;
            3'b011: if (data == seq[3]) state <= seq[3];
                      else state <= 3'b000;
            3'b100: if (data == seq[4]) state <= seq[4];
                      else state <= 3'b000;
            3'b101: if (data == seq[5]) state <= seq[5];
                      else state <= 3'b000;
            3'b110: if (data == seq[6]) state <= seq[6];
                      else if (data == seq[7]) seq_found <= 1'b1;
                      else state <= 3'b000;
        endcase
    end
end

endmodule
