module RCA8(output [7:0] sum, output cout, input [7:0] a, input [7:0] b);

  wire [7:0] p, g;
  wire [8:1] c;

  // Propagate and Generate signals are calculated in parallel. Level 1.
  assign p = a ^ b;
  assign g = a & b;

  // Carry lookahead logic. All carries are computed in parallel from p, g, and c0.
  // This structure allows synthesis tools to create a fast tree.
  // Input carry c[0] is hardwired to 0.
  assign c[1] = g[0];
  assign c[2] = g[1] | (p[1] & g[0]);
  assign c[3] = g[2] | (p[2] & (g[1] | (p[1] & g[0])));
  assign c[4] = g[3] | (p[3] & (g[2] | (p[2] & (g[1] | (p[1] & g[0])))));
  assign c[5] = g[4] | (p[4] & c[4]);
  assign c[6] = g[5] | (p[5] & c[5]);
  assign c[7] = g[6] | (p[6] & c[6]);
  assign c[8] = g[7] | (p[7] & c[7]);

  // Final sum is computed in parallel. sum[i] = p[i] ^ c[i].
  assign sum = p ^ {c[7:1], 1'b0};
  
  // Final carry out is the last carry bit calculated.
  assign cout = c[8];

endmodule