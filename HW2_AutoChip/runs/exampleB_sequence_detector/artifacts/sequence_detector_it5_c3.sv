module sequence_detector(
    input  wire clk,
    input  wire rst_n,
    input  wire [2:0] data,
    output wire seq_found
);

reg [2:0] seq_state;
reg [2:0] seq_next_state;
reg seq_found;

initial seq_state = 3'd0;

always @(posedge clk) begin
    if (!rst_n) begin
        seq_state <= 3'd0;
        seq_found <= 1'b0;
    end else begin
        seq_state <= seq_next_state;
        case (seq_state)
            3'd0: begin
                if (data == 3'd1) seq_next_state <= 3'd1;
                else seq_next_state <= 3'd0;
            end
            3'd1: begin
                if (data == 3'd0) seq_next_state <= 3'd2;
                else if (data == 3'd1) seq_next_state <= 3'd3;
                else seq_next_state <= 3'd1;
            end
            3'd2: begin
                if (data == 3'd1) seq_next_state <= 3'd4;
                else seq_next_state <= 3'd2;
            end
            3'd3: begin
                if (data == 3'd1) seq_next_state <= 3'd5;
                else seq_next_state <= 3'd3;
            end
            3'd4: begin
                if (data == 3'd1) seq_next_state <= 3'd6;
                else seq_next_state <= 3'd4;
            end
            3'd5: begin
                if (data == 3'd0) seq_next_state <= 3'd7;
                else if (data == 3'd1) seq_next_state <= 3'd8;
                else seq_next_state <= 3'd5;
            end
            3'd6: begin
                if (data == 3'd0) seq_next_state <= 3'd9;
                else if (data == 3'd1) seq_next_state <= 3'd10;
                else seq_next_state <= 3'd6;
            end
            3'd7: begin
                if (data == 3'd1) seq_next_state <= 3'd11;
                else seq_next_state <= 3'd7;
            end
            3'd8: begin
                if (data == 3'd0) seq_next_state <= 3'd12;
                else seq_next_state <= 3'd8;
            end
            3'd9: begin
                if (data == 3'd1) seq_next_state <= 3'd13;
                else seq_next_state <= 3'd9;
            end
            3'd10: begin
                if (data == 3'd0) seq_next_state <= 3'd14;
                else if (data == 3'd1) seq_next_state <= 3'd15;
                else seq_next_state <= 3'd10;
            end
            3'd11: begin
                if (data == 3'd0) seq_next_state <= 3'd0;
                else seq_next_state <= 3'd11;
            end
            3'd12: begin
                if (data == 3'd0) seq_next_state <= 3'd0;
                else seq_next_state <= 3'd12;
            end
            3'd13: begin
                if (data == 3'd0) seq_next_state <= 3'd0;
                else seq_next_state <= 3'd13;
            end
            3'd14: begin
                if (data == 3'd0) seq_next_state <= 3'd0;
                else seq_next_state <= 3'd14;
            end
            3'd15: begin
                if (data == 3'd0) seq_next_state <= 3'd0;
                else seq_next_state <= 3'd15;
            end
            default: seq_next_state <= seq_state;
        endcase
        if (seq_state == 3'd15) seq_found <= 1'b1;
        else seq_found <= 1'b0;
    end
end

assign seq_found = seq_found;

endmodule
