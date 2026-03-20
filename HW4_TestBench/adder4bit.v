
module adder4bit (
    input wire [3:0] a, b,
    output wire [3:0] sum,
    output wire carry
);
    wire [4:0] r = a + b;
    assign sum = r[3:0];
    assign carry = r[4];
endmodule
