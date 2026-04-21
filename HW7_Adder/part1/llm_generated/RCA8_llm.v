module FA(output sum, cout, input a, b, cin);
  wire ab_xor;
  wire t1, t2;

  xor (ab_xor, a, b);
  xor (sum, ab_xor, cin);

  and (t1, a, b);
  and (t2, cin, ab_xor);
  or  (cout, t1, t2);
endmodule

module RCA8(output [7:0] sum, output cout, input [7:0] a, b);
  wire [7:1] c;

  FA fa0(sum[0], c[1], a[0], b[0], 1'b0);
  FA fa[6:1](sum[6:1], c[7:2], a[6:1], b[6:1], c[6:1]);
  FA fa7(sum[7], cout, a[7], b[7], c[7]);
endmodule
