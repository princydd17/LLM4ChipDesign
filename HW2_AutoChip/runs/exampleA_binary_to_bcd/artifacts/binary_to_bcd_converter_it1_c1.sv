module binary_to_bcd_converter(
    input  logic        clk,
    input  logic        rst,
    input  logic [4:0]  binary_input,
    output logic [7:0]  bcd_output
);

    logic [3:0]  tens_digit;
    logic [3:0]  ones_digit;

    always_comb begin
        case (binary_input)
            5'b00000: tens_digit = 4'b0000, ones_digit = 4'b0000;
            5'b00001: tens_digit = 4'b0000, ones_digit = 4'b0001;
            5'b00010: tens_digit = 4'b0000, ones_digit = 4'b0010;
            5'b00011: tens_digit = 4'b0000, ones_digit = 4'b0011;
            5'b00100: tens_digit = 4'b0000, ones_digit = 4'b0100;
            5'b00101: tens_digit = 4'b0000, ones_digit = 4'b0101;
            5'b00110: tens_digit = 4'b0000, ones_digit = 4'b0110;
            5'b00111: tens_digit = 4'b0000, ones_digit = 4'b0111;
            5'b01000: tens_digit = 4'b0000, ones_digit = 4'b1000;
            5'b01001: tens_digit = 4'b0000, ones_digit = 4'b1001;
            5'b01010: tens_digit = 4'b0000, ones_digit = 4'b1010;
            5'b01011: tens_digit = 4'b0000, ones_digit = 4'b1011;
            5'b01100: tens_digit = 4'b0000, ones_digit = 4'b1100;
            5'b01101: tens_digit = 4'b0000, ones_digit = 4'b1101;
            5'b01110: tens_digit = 4'b0000, ones_digit = 4'b1110;
            5'b01111: tens_digit = 4'b0000, ones_digit = 4'b1111;
            5'b10000: tens_digit = 4'b0010, ones_digit = 4'b0000;
            5'b10001: tens_digit = 4'b0010, ones_digit = 4'b0001;
            5'b10010: tens_digit = 4'b0010, ones_digit = 4'b0010;
            5'b10011: tens_digit = 4'b0010, ones_digit = 4'b0011;
            5'b10100: tens_digit = 4'b0010, ones_digit = 4'b0100;
            5'b10101: tens_digit = 4'b0010, ones_digit = 4'b0101;
            5'b10110: tens_digit = 4'b0010, ones_digit = 4'b0110;
            5'b10111: tens_digit = 4'b0010, ones_digit = 4'b0111;
            5'b11000: tens_digit = 4'b0010, ones_digit = 4'b1000;
            5'b11001: tens_digit = 4'b0010, ones_digit = 4'b1001;
            5'b11010: tens_digit = 4'b0010, ones_digit = 4'b1010;
            5'b11011: tens_digit = 4'b0010, ones_digit = 4'b1011;
            5'b11100: tens_digit = 4'b0010, ones_digit = 4'b1100;
            5'b11101: tens_digit = 4'b0010, ones_digit = 4'b1101;
            5'b11110: tens_digit = 4'b0010, ones_digit = 4'b1110;
            5'b11111: tens_digit = 4'b0010, ones_digit = 4'b1111;
            default:  tens_digit = 4'b0000, ones_digit = 4'b0000;
        endcase

        bcd_output = {tens_digit, ones_digit};
    end

endmodule
