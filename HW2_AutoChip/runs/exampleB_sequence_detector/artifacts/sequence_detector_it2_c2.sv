module sequence_detector(
    input  wire clk,
    input  wire rst_n,
    input  wire [2:0] data,
    output reg seq_found
);

    reg [2:0] state = 0;
    reg [2:0] next_state;
    reg [2:0] sequence = 7'b001_101_110_000_110_110_011_101;

    always @(posedge clk) begin
        if (!rst_n) begin
            state <= 0;
            seq_found <= 1'b0;
        end else begin
            state <= next_state;
            seq_found <= (state == sequence[7:5]) ? 1'b1 : 1'b0;
        end
    end

    always @(*) begin
        case (state)
            3'd0: next_state = sequence[0];
            3'd1: next_state = sequence[1];
            3'd2: next_state = sequence[2];
            3'd3: next_state = sequence[3];
            3'd4: next_state = sequence[4];
            3'd5: next_state = sequence[5];
            3'd6: next_state = sequence[6];
            default: next_state = state;
        endcase
    end

endmodule
