`timescale 1ns/1ps
module mux2to1tb;
    reg in1;
    reg in2;
    reg select;
    wire out;
    integer i;
    reg expected;

    mux2to1 dut (.in1(in1), .in2(in2), .select(select), .out(out));

    initial begin
        for (i = 0; i < 8; i = i + 1) begin
            in1 = i[2];
            in2 = i[1];
            select = i[0];
            #1;
            expected = select ? in2 : in1;
            if (out !== expected) begin
                $display("mux2to1 failed: in1=%0b in2=%0b select=%0b expected=%0b got=%0b", in1, in2, select, expected, out);
                $finish;
            end
        end
        $display("mux2to1 passed!");
        $finish;
    end
endmodule
