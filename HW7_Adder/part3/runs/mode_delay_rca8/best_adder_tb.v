`timescale 1ns/1ps

module best_adder_tb;
  reg  [7:0] a, b;
  wire [7:0] sum;
  wire       cout;

  integer i, j;
  integer pass_count;
  integer fail_count;
  reg [8:0] expected;

  RCA8 dut (
    .a(a),
    .b(b),
    .sum(sum),
    .cout(cout)
  );

  initial begin
    pass_count = 0;
    fail_count = 0;

    for (i = 0; i < 256; i = i + 1) begin
      for (j = 0; j < 256; j = j + 1) begin
        a = i[7:0];
        b = j[7:0];
        #1;

        expected = a + b;
        if ({cout, sum} !== expected) begin
          fail_count = fail_count + 1;
          $display("FAIL a=%h b=%h | got=%h expected=%h", a, b, {cout, sum}, expected);
        end else begin
          pass_count = pass_count + 1;
        end
      end
    end

    $display("BEST ADDER: PASS=%0d FAIL=%0d", pass_count, fail_count);
    if (fail_count == 0)
      $display("FINAL STATUS: PASS");
    else
      $display("FINAL STATUS: FAIL");
    $finish;
  end
endmodule
