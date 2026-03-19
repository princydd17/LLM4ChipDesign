`timescale 1ns/1ps
module mux4to1tb;
    reg [1:0] sel;
    reg [3:0] in;
    wire out;
    integer i;
    integer j;
    reg expected;

    mux4to1 dut (.sel(sel), .in(in), .out(out));

    initial begin
        for (i = 0; i < 4; i = i + 1) begin
            for (j = 0; j < 16; j = j + 1) begin
                sel = i[1:0];
                in = j[3:0];
                #1;
                expected = in[sel];
                if (out !== expected) begin
                    $display("mux4to1 failed: sel=%0d in=%0b expected=%0b got=%0b", sel, in, expected, out);
                    $finish;
                end
            end
        end
        $display("mux4to1 passed!");
        $finish;
    end
endmodule
