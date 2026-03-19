```verilog
module binary_to_bcd_converter (
    input  logic        clk,
    input  logic        rst_n,
    input  logic [4:0]  binary_input,
    output logic [7:0]  bcd_output
);

logic [3:0] bcd_ones, bcd_tens;

always_comb begin
    case (binary_input)
        5'b00000: bcd_output = 8'b00000000;
        5'b00001: bcd_output = 8'b00000010;
        5'b00010: bcd_output = 8'b00000100;
        5'b00011: bcd_output = 8'b00000110;
        5'b00100: bcd_output = 8'b00001000;
        5'b00101: bcd_output = 8'b00001010;
        5'b00110: bcd_output = 8'b00001100;
        5'b00111: bcd_output = 8'b00001110;
        5'b01000: bcd_output = 8'b00010000;
        5'b01001: bcd_output = 8'b00010010;
        5'b01010: bcd_output = 8'b00010100;
        5'b01011: bcd_output = 8'b00010110;
        5'b01100: bcd_output = 8'b00011000;
        5'b01101: bcd_output = 8'b00011010;
        5'b01110: bcd_output = 8'b00011100;
        5'b01111: bcd_output = 8'b00011110;
        5'b10000: bcd_output = 8'b00100000;
        5'b10001: bcd_output = 8'b00100010;
        5'b10010: bcd_output = 8'b00100100;
        5'b10011: bcd_output = 8'b00100110;
        5'b10100: bcd_output = 8'b00101000;
        5'b10101: bcd_output = 8'b00101010;
        5'b10110: bcd_output = 8'b00101100;
        5'b10111: bcd_output = 8'b00101110;
        5'b11000: bcd_output = 8'b00110000;
        5'b11001: bcd_output = 8'b00110010;
        5'b11010: bcd_output = 8'b00110100;
        5'b11011: bcd_output = 8'b00110110;
        5'b11100: bcd_output = 8'b00111000;
        5'b11101: bcd_output = 8'b00111010;
        5'b11110: bcd_output = 8'b00111100;
        5'b11111: bcd_output = 8'b00111110;
        default:  bcd_output = 8'b11111111;
    endcase
end

assign bcd_ones = bcd_output[3:0];
assign bcd_tens = bcd_output[7:4];

always_comb begin
    case (bcd_tens)
        4'b0000: begin
            case (bcd_ones)
                4'b0000: bcd_output = 8'b00000000;
                4'b0001: bcd_output = 8'b00000010;
                4'b0010: bcd_output = 8'b00000100;
                4'b0011: bcd_output = 8'b00000110;
                4'b0100: bcd_output = 8'b00001000;
                4'b0101: bcd_output = 8'b00001010;
                4'b0110: bcd_output = 8'b00001100;
                4'b0111: bcd_output = 8'b00001110;
                4'b1000: bcd_output = 8'b00010000;
                4'b1001: bcd_output = 8'b00010010;
                4'b1010: bcd_output = 8'b00010100;
                4'b1011: bcd_output = 8'b00010110;
                4'b1100: bcd_output = 8'b00011000;
                4'b1101: bcd_output = 8'b00011010;
                4'b1110: bcd_output = 8'b00011100;
                4'b1111: bcd_output = 8'b00011110;
                default:  bcd_output = 8'b11111111;
            endcase
        end
        4'b0001: begin
            case (bcd_ones)
                4'b0000: bcd_output = 8'b00000100;
                4'b0001: bcd_output = 8'b00000110;
                4'b0010: bcd_output = 8'b00001000;
                4'b0011: bcd_output = 8'b00001010;
                4'b0100: bcd_output = 8'b00001100;
                4'b0101: bcd_output = 8'b00001110;
                4'b0110: bcd_output = 8'b00010000;
                4'b0111: bcd_output = 8'b00010010;
                4'b1000: bcd_output = 8'b00010100;
                4'b1001: bcd_output = 8'b00010110;
                4'b1010: bcd_output = 8'b00011000;
                4'b1011: bcd_output = 8'b00011010;
                4'b1100: bcd_output = 8'b00011100;
                4'b1101: bcd_output = 8'b00011110;
                4'b1110: bcd_output = 8'b00100000;
                4'b1111: bcd_output = 8'b00100010;
                default:  bcd_output = 8'b11111111;
            endcase
        end
        4'b0010: begin
            case (bcd_ones)
                4'b0000: bcd_output = 8'b00001000
