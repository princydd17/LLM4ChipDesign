module top (a,b,c);
input a, b;
output c;


//assign c = ~ a|b;
//assign c = !a | !b;
//assign c = !( !a ^ !b);
assign c_inter = a ^ b;
assign c = !c_inter;
//assign c = ~|{a,b};
wire c_inter;
endmodule
