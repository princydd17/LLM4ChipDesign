module sequence_detector (
    input  wire         clk,
    input  wire         rst_n,
    input  wire  [2:0]  data,
    output reg          seq_found
);

    localparam IDLE       = 3'b000;
    localparam DETECT_001 = 3'b001;
    localparam DETECT_101 = 3'b010;
    localparam DETECT_110 = 3'b011;
    localparam DETECT_000 = 3'b100;
    localparam DETECT_1102 = 3'b101;
    localparam DETECT_1103 = 3'b110;
    localparam DETECT_011 = 3'b111;
    localparam DETECT_1012 = 3'b112;

    reg  [2:0]  state;
    reg  [2:0]  next_state;

    always @(posedge clk, negedge rst_n) begin
        if (!rst_n) begin
            state <= IDLE;
            seq_found <= 1'b0;
        end else begin
            state <= next_state;
            seq_found <= 1'b0;
        end
    end

    always @(state or data) begin
        case (state)
            IDLE: begin
                if (data == 3'b001)
                    next_state = DETECT_001;
                else if (data == 3'b101)
                    next_state = DETECT_101;
                else if (data == 3'b110)
                    next_state = DETECT_110;
                else if (data == 3'b000)
                    next_state = DETECT_000;
                else
                    next_state = IDLE;
            end
            DETECT_001: begin
                if (data == 3'b101)
                    next_state = DETECT_101;
                else
                    next_state = IDLE;
            end
            DETECT_101: begin
                if (data == 3'b110)
                    next_state = DETECT_110;
                else
                    next_state = IDLE;
            end
            DETECT_110: begin
                if (data == 3'b000)
                    next_state = DETECT_000;
                else if (data == 3'b110)
                    next_state = DETECT_1102;
                else
                    next_state = IDLE;
            end
            DETECT_000: begin
                if (data == 3'b110)
                    next_state = DETECT_1103;
                else
                    next_state = IDLE;
            end
            DETECT_1102: begin
                if (data == 3'b011)
                    next_state = DETECT_011;
                else
                    next_state = IDLE;
            end
            DETECT_1103: begin
                if (data == 3'b110)
                    next_state = DETECT_110;
                else
                    next_state = IDLE;
            end
            DETECT_011: begin
                if (data == 3'b101)
                    next_state = DETECT_1012;
                else
                    next_state = IDLE;
            end
            DETECT_1012: begin
                if (data == 3'b110)
                    seq_found <= 1'b1;
                else
                    next_state = IDLE;
            end
            default: next_state = IDLE;
        endcase
    end

endmodule
