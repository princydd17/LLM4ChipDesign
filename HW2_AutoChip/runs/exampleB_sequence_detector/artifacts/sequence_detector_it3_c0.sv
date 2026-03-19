module sequence_detector(
    input  wire        clk,
    input  wire        rst_n,
    input  wire [2:0]  data,
    output wire        seq_found
);

reg [2:0] current_seq;
reg [2:0] next_seq;
reg [7:0] state;
reg seq_found;

always @(posedge clk)
begin
    if (!rst_n)
        state <= 0;
    else
    begin
        case (state)
            0: next_seq = 3'b001;
            1: next_seq = 3'b101;
            2: next_seq = 3'b110;
            3: next_seq = 3'b000;
            4: next_seq = 3'b110;
            5: next_seq = 3'b110;
            6: next_seq = 3'b011;
            7: next_seq = 3'b101;
            default: next_seq = 3'b000;
        endcase

        current_seq <= next_seq;

        case (current_seq)
            3'b001: state <= 1;
            3'b101: state <= 2;
            3'b110: state <= 3;
            3'b000: state <= 4;
            3'b110: state <= 5;
            3'b110: state <= 6;
            3'b011: state <= 7;
            3'b101: state <= 8;
            default: state <= 0;
        endcase

        if (state == 8 && current_seq == 3'b101)
            seq_found <= 1;
        else
            seq_found <= 0;
    end
end

endmodule
