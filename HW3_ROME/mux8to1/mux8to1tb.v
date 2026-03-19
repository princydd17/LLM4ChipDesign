`timescale 1ns/1ps
module mux8to1tb;
    reg [2:0] sel;
    reg [7:0] in;
    wire out;
    integer i;
    integer j;
    reg expected;

    mux8to1 dut (.sel(sel), .in(in), .out(out));

    initial begin
        for (i = 0; i < 8; i = i + 1) begin
            for (j = 0; j < 256; j = j + 1) begin
                sel = i[2:0];
                in = j[7:0];
                #1;
                expected = in[sel];
                if (out !== expected) begin
                    $display("mux8to1 failed: sel=%0d in=%0b expected=%0b got=%0b", sel, in, expected, out);
                    $finish;
                end
            end
        end
        $display("mux8to1 passed!");
        $finish;
    end
endmodule
