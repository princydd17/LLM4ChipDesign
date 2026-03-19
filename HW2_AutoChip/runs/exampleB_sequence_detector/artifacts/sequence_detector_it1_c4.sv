module sequence_detector(
    input  wire clk,
    input  wire rst_n,
    input  wire [2:0] data,
    output reg seq_found
);

// State register
reg [4:0] state;

// Next-state logic
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        state <= 5'b00000;
    end else begin
        case (state)
            5'b00000: state <= (data == 3'b001) ? 5'b00001 : 5'b00000;
            5'b00001: state <= (data == 3'b101) ? 5'b00010 : 5'b00001;
            5'b00010: state <= (data == 3'b110) ? 5'b00011 : 5'b00010;
            5'b00011: state <= (data == 3'b000) ? 5'b00100 : 5'b00011;
            5'b00100: state <= (data == 3'b110) ? 5'b00101 : 5'b00100;
            5'b00101: state <= (data == 3'b110) ? 5'b00110 : 5'b00101;
            5'b00110: state <= (data == 3'b011) ? 5'b00111 : 5'b00110;
            5'b00111: state <= (data == 3'b101) ? 5'b01000 : 5'b00111;
            default:  state <= 5'b00000;
        endcase
    end
end

// Output logic
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        seq_found <= 1'b0;
    end else begin
        case (state)
            5'b01000: seq_found <= 1'b1;
            default:  seq_found <= 1'b0;
        endcase
    end
end

endmodule
