`timescale 1ns/1ps

module RCA8_tb;
  reg  [7:0] a, b;
  wire [7:0] sum;
  wire       cout;

  integer i, j;
  integer pass_count;
  integer fail_count;
  reg [7:0] exp_sum;
  reg       exp_cout;
  reg [7:1] exp_c;

  RCA8 dut(
    .sum(sum),
    .cout(cout),
    .a(a),
    .b(b)
  );

  task automatic calc_expected(
    input  [7:0] ta,
    input  [7:0] tb,
    output [7:0] tsum,
    output       tcout,
    output [7:1] tc
  );
    integer k;
    reg carry_in;
    reg [8:0] full_sum;
    begin
      carry_in = 1'b0;
      for (k = 0; k < 8; k = k + 1) begin
        tc[k+1] = (ta[k] & tb[k]) | ((ta[k] ^ tb[k]) & carry_in);
        carry_in = tc[k+1];
      end
      full_sum = ta + tb;
      tsum  = full_sum[7:0];
      tcout = full_sum[8];
    end
  endtask

  initial begin
    pass_count = 0;
    fail_count = 0;
    a = 8'h00;
    b = 8'h00;
    #1;

    for (i = 0; i < 256; i = i + 1) begin
      for (j = 0; j < 256; j = j + 1) begin
        a = i[7:0];
        b = j[7:0];
        #1;
        calc_expected(a, b, exp_sum, exp_cout, exp_c);

        if ((sum !== exp_sum) || (cout !== exp_cout) || (dut.c !== exp_c)) begin
          fail_count = fail_count + 1;
          $display("FAIL RCA8 a=%h b=%h | sum=%h exp_sum=%h cout=%b exp_cout=%b | c=%b exp_c=%b",
                   a, b, sum, exp_sum, cout, exp_cout, dut.c, exp_c);
        end else begin
          pass_count = pass_count + 1;
        end
      end
    end

    $display("RCA8_tb complete: PASS=%0d FAIL=%0d", pass_count, fail_count);
    if (fail_count == 0) begin
      $display("RCA8_tb FINAL STATUS: PASS");
    end else begin
      $display("RCA8_tb FINAL STATUS: FAIL");
    end
    $finish;
  end
endmodule
