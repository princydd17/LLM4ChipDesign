`timescale 1ns/1ps
module adder4tb;
    reg [3:0] a;
    reg [3:0] b;
    reg cin;
    wire [3:0] sum;
    wire cout;
    integer i;
    integer j;
    integer k;
    reg [4:0] expected;

    adder4 dut (.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));

    initial begin
        for (i = 0; i < 16; i = i + 1) begin
            for (j = 0; j < 16; j = j + 1) begin
                for (k = 0; k < 2; k = k + 1) begin
                    a = i[3:0];
                    b = j[3:0];
                    cin = k[0];
                    #1;
                    expected = a + b + cin;
                    if (sum !== expected[3:0] || cout !== expected[4]) begin
                        $display("adder4 failed: a=%0h b=%0h cin=%0b expected_sum=%0h expected_cout=%0b got_sum=%0h got_cout=%0b", a, b, cin, expected[3:0], expected[4], sum, cout);
                        $finish;
                    end
                end
            end
        end
        $display("adder4 passed!");
        $finish;
    end
endmodule
