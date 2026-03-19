`timescale 1ns/1ps
module half_addertb;
    reg a;
    reg b;
    wire sum;
    wire carry;
    integer i;
    reg expected_sum;
    reg expected_carry;

    half_adder dut (.a(a), .b(b), .sum(sum), .carry(carry));

    initial begin
        for (i = 0; i < 4; i = i + 1) begin
            a = i[1];
            b = i[0];
            #1;
            expected_sum = a ^ b;
            expected_carry = a & b;
            if (sum !== expected_sum || carry !== expected_carry) begin
                $display("half_adder failed: a=%0b b=%0b expected_sum=%0b expected_carry=%0b got_sum=%0b got_carry=%0b", a, b, expected_sum, expected_carry, sum, carry);
                $finish;
            end
        end
        $display("half_adder passed!");
        $finish;
    end
endmodule
