`timescale 1ns/1ps
module full_addertb;
    reg a;
    reg b;
    reg cin;
    wire sum;
    wire cout;
    integer i;
    reg [1:0] expected;

    full_adder dut (.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));

    initial begin
        for (i = 0; i < 8; i = i + 1) begin
            a = i[2];
            b = i[1];
            cin = i[0];
            #1;
            expected = a + b + cin;
            if (sum !== expected[0] || cout !== expected[1]) begin
                $display("full_adder failed: a=%0b b=%0b cin=%0b expected_sum=%0b expected_cout=%0b got_sum=%0b got_cout=%0b", a, b, cin, expected[0], expected[1], sum, cout);
                $finish;
            end
        end
        $display("full_adder passed!");
        $finish;
    end
endmodule
