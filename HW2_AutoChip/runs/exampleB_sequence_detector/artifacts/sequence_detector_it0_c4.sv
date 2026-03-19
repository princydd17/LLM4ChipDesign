module sequence_detector(
    input  wire clk,
    input  wire rst_n,
    input  wire [2:0] data,
    output wire seq_found
);

reg [2:0] state;
reg [2:0] next_state;
reg seq_found;

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        state <= 3'b000;
        seq_found <= 1'b0;
    end else begin
        state <= next_state;
        seq_found <= (state == 3'b110 && data == 3'b110) ? 1'b1 : 1'b0;
    end
end

always @(*)
begin
    case (state)
        3'b000: next_state = (data == 3'b001) ? 3'b001 : 3'b000;
        3'b001: next_state = (data == 3'b101) ? 3'b101 : 3'b000;
        3'b101: next_state = (data == 3'b110) ? 3'b110 : 3'b000;
        3'b110: next_state = (data == 3'b000) ? 3'b000 : 3'b000;
        default: next_state = 3'b000;
    endcase
end

endmodule
