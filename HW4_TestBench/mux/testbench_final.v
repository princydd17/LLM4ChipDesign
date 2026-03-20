module mux2to1_tb;
    reg a, b, sel; wire y;
    mux2to1 uut (.a(a), .b(b), .sel(sel), .y(y));
    integer passed_tests, failed_tests;
    initial begin
        passed_tests = 0; failed_tests = 0;
        a=0;b=0;sel=0;#10; if(y===0) begin passed_tests=passed_tests+1; end else failed_tests=failed_tests+1;
        a=0;b=0;sel=1;#10; if(y===0) begin passed_tests=passed_tests+1; end else failed_tests=failed_tests+1;
        a=0;b=1;sel=0;#10; if(y===0) begin passed_tests=passed_tests+1; end else failed_tests=failed_tests+1;
        a=0;b=1;sel=1;#10; if(y===1) begin passed_tests=passed_tests+1; end else failed_tests=failed_tests+1;
        a=1;b=0;sel=0;#10; if(y===1) begin passed_tests=passed_tests+1; end else failed_tests=failed_tests+1;
        a=1;b=0;sel=1;#10; if(y===0) begin passed_tests=passed_tests+1; end else failed_tests=failed_tests+1;
        a=1;b=1;sel=0;#10; if(y===1) begin passed_tests=passed_tests+1; end else failed_tests=failed_tests+1;
        a=1;b=1;sel=1;#10; if(y===1) begin passed_tests=passed_tests+1; end else failed_tests=failed_tests+1;
        $display("Summary: %0d passed, %0d failed", passed_tests, failed_tests); $finish;
    end
endmodule