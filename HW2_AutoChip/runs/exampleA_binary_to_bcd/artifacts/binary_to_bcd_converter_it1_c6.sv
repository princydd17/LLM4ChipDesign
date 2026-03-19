module binary_to_bcd_converter (
    input  [4:0] binary_input,
    output [7:0] bcd_output
);

    always_comb begin
        case (binary_input)
            5'b00000: bcd_output = 8'b00000000;
            5'b00001: bcd_output = 8'b00000001;
            5'b00010: bcd_output = 8'b00000010;
            5'b00011: bcd_output = 8'b00000011;
            5'b00100: bcd_output = 8'b00000100;
            5'b00101: bcd_output = 8'b00000101;
            5'b00110: bcd_output = 8'b00000110;
            5'b00111: bcd_output = 8'b00000111;
            5'b01000: bcd_output = 8'b00001000;
            5'b01001: bcd_output = 8'b00001001;
            5'b01010: bcd_output = 8'b00001010;
            5'b01011: bcd_output = 8'b00001011;
            5'b01100: bcd_output = 8'b00001100;
            5'b01101: bcd_output = 8'b00001101;
            5'b01110: bcd_output = 8'b00001110;
            5'b01111: bcd_output = 8'b00001111;
            5'b10000: bcd_output = 8'b00010000;
            5'b10001: bcd_output = 8'b00010001;
            5'b10010: bcd_output = 8'b00010010;
            5'b10011: bcd_output = 8'b00010011;
            5'b10100: bcd_output = 8'b00010100;
            5'b10101: bcd_output = 8'b00010101;
            5'b10110: bcd_output = 8'b00010110;
            5'b10111: bcd_output = 8'b00010111;
            5'b11000: bcd_output = 8'b00011000;
            5'b11001: bcd_output = 8'b00011001;
            5'b11010: bcd_output = 8'b00011010;
            5'b11011: bcd_output = 8'b00011011;
            5'b11100: bcd_output = 8'b00011100;
            5'b11101: bcd_output = 8'b00011101;
            5'b11110: bcd_output = 8'b00011110;
            5'b11111: bcd_output = 8'b00011111;
            default:  bcd_output = 8'b00000000;
        endcase
    end

endmodule
