`timescale 1ns/1ps
module adder8tb;
    reg [7:0] a;
    reg [7:0] b;
    reg cin;
    wire [7:0] sum;
    wire cout;
    integer i;
    reg [8:0] expected;

    adder8 dut (.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));

    initial begin
        for (i = 0; i < 200; i = i + 1) begin
            a = (i * 17 + 8'h3C) & 8'hFF;
            b = (i * 29 + 8'h52) & 8'hFF;
            cin = i[0];
            #1;
            expected = a + b + cin;
            if (sum !== expected[7:0] || cout !== expected[8]) begin
                $display("adder8 failed: a=%0h b=%0h cin=%0b expected_sum=%0h expected_cout=%0b got_sum=%0h got_cout=%0b", a, b, cin, expected[7:0], expected[8], sum, cout);
                $finish;
            end
        end
        $display("adder8 passed!");
        $finish;
    end
endmodule
