module sequence_detector(
    input  wire clk,
    input  wire rst_n,
    input  wire [2:0] data,
    output reg  seq_found
);

    reg [2:0] state_reg;
    reg [2:0] next_state_reg;

    parameter IDLE = 3'd0;
    parameter DETECT_001 = 3'd1;
    parameter DETECT_101 = 3'd2;
    parameter DETECT_110 = 3'd3;
    parameter DETECT_000 = 3'd4;
    parameter DETECT_110_1 = 3'd5;
    parameter DETECT_110_2 = 3'd6;
    parameter DETECT_011 = 3'd7;
    parameter DETECT_101_1 = 3'd8;
    parameter FINAL_STATE = 3'd9;

    always @(posedge clk) begin
        if (!rst_n) begin
            state_reg <= IDLE;
            next_state_reg <= IDLE;
            seq_found <= 1'b0;
        end else begin
            case (state_reg)
                IDLE: begin
                    if (data == 3'd0) next_state_reg <= DETECT_000;
                    else next_state_reg <= IDLE;
                end
                DETECT_000: begin
                    if (data == 3'd0) next_state_reg <= DETECT_000;
                    else if (data == 3'd1) next_state_reg <= DETECT_001;
                    else next_state_reg <= IDLE;
                end
                DETECT_001: begin
                    if (data == 3'd1) next_state_reg <= DETECT_101;
                    else next_state_reg <= IDLE;
                end
                DETECT_101: begin
                    if (data == 3'd0) next_state_reg <= DETECT_110;
                    else if (data == 3'd1) next_state_reg <= DETECT_101;
                    else next_state_reg <= IDLE;
                end
                DETECT_110: begin
                    if (data == 3'd1) next_state_reg <= DETECT_110_1;
                    else if (data == 3'd0) next_state_reg <= DETECT_110;
                    else next_state_reg <= IDLE;
                end
                DETECT_110_1: begin
                    if (data == 3'd1) next_state_reg <= DETECT_110_2;
                    else next_state_reg <= IDLE;
                end
                DETECT_110_2: begin
                    if (data == 3'd0) next_state_reg <= DETECT_011;
                    else if (data == 3'd1) next_state_reg <= DETECT_110;
                    else next_state_reg <= IDLE;
                end
                DETECT_011: begin
                    if (data == 3'd0) next_state_reg <= DETECT_101;
                    else if (data == 3'd1) next_state_reg <= DETECT_101_1;
                    else next_state_reg <= IDLE;
                end
                DETECT_101_1: begin
                    if (data == 3'd1) next_state_reg <= FINAL_STATE;
                    else next_state_reg <= IDLE;
                end
                FINAL_STATE: begin
                    seq_found <= 1'b1;
                    next_state_reg <= IDLE;
                end
                default: next_state_reg <= IDLE;
            endcase
            state_reg <= next_state_reg;
        end
    end

endmodule
