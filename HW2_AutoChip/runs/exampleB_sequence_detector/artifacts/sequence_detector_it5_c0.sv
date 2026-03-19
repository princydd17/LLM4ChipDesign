```verilog
module sequence_detector (
    input  wire clk,
    input  wire rst_n,
    input  wire [2:0] data,
    output reg seq_found
);

reg [3:0] state;
reg [2:0] seq_ptr;

always @(posedge clk) begin
    if (!rst_n) begin
        state <= 0;
        seq_ptr <= 0;
    end else begin
        case (state)
            0: begin
                if (data == 3'b001) begin
                    seq_ptr <= 0;
                    state <= 1;
                end else
                    state <= 0;
            end
            1: begin
                if (data == 3'b101) begin
                    seq_ptr <= 0;
                    state <= 2;
                end else if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 3;
                end else
                    state <= 0;
            end
            2: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 4;
                end else if (data == 3'b011) begin
                    seq_ptr <= 0;
                    state <= 5;
                end else
                    state <= 0;
            end
            3: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 6;
                end else
                    state <= 0;
            end
            4: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 7;
                end else
                    state <= 0;
            end
            5: begin
                if (data == 3'b101) begin
                    seq_ptr <= 0;
                    state <= 8;
                end else
                    state <= 0;
            end
            6: begin
                if (data == 3'b101) begin
                    seq_ptr <= 0;
                    state <= 9;
                end else
                    state <= 0;
            end
            7: begin
                if (data == 3'b000) begin
                    seq_ptr <= 0;
                    state <= 10;
                end else
                    state <= 0;
            end
            8: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 11;
                end else
                    state <= 0;
            end
            9: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 12;
                end else
                    state <= 0;
            end
            10: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 13;
                end else
                    state <= 0;
            end
            11: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 14;
                end else
                    state <= 0;
            end
            12: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 15;
                end else
                    state <= 0;
            end
            13: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 16;
                end else
                    state <= 0;
            end
            14: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 17;
                end else
                    state <= 0;
            end
            15: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 18;
                end else
                    state <= 0;
            end
            16: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 19;
                end else
                    state <= 0;
            end
            17: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 20;
                end else
                    state <= 0;
            end
            18: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 21;
                end else
                    state <= 0;
            end
            19: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 22;
                end else
                    state <= 0;
            end
            20: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 23;
                end else
                    state <= 0;
            end
            21: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 24;
                end else
                    state <= 0;
            end
            22: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 25;
                end else
                    state <= 0;
            end
            23: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 26;
                end else
                    state <= 0;
            end
            24: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 27;
                end else
                    state <= 0;
            end
            25: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 28;
                end else
                    state <= 0;
            end
            26: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 29;
                end else
                    state <= 0;
            end
            27: begin
                if (data == 3'b110) begin
                    seq_ptr <= 0;
                    state <= 30;
                end else
                    state <= 0;
            end
            28: begin
                if (data == 3'b110) begin
