module mux2to1(input wire in1, input wire in2, input wire select, output wire out);
    assign out = select ? in2 : in1;
endmodule
module mux4to1(input [1:0] sel, input [3:0] in, output wire out);
    wire m1_out, m2_out;
    
    mux2to1 m1(.in1(in[0]), .in2(in[1]), .select(sel[0]), .out(m1_out));
    mux2to1 m2(.in1(in[2]), .in2(in[3]), .select(sel[0]), .out(m2_out));
    mux2to1 m3(.in1(m1_out), .in2(m2_out), .select(sel[1]), .out(out));
endmodule
module mux8to1(input [2:0] sel, input [7:0] in, output wire out);
    wire m1_out, m2_out;
    
    mux4to1 m1(.sel(sel[1:0]), .in(in[3:0]), .out(m1_out));
    mux4to1 m2(.sel(sel[1:0]), .in(in[7:4]), .out(m2_out));
    mux2to1 m3(.in1(m1_out), .in2(m2_out), .select(sel[2]), .out(out));
endmodule
