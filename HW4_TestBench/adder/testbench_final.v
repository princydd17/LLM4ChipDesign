module adder4bit_tb;
    reg [3:0] a,b; wire [3:0] sum; wire carry;
    adder4bit uut (.a(a),.b(b),.sum(sum),.carry(carry));
    integer passed_tests,failed_tests;
    initial begin
        passed_tests=0; failed_tests=0;
        a=4'b0000;b=4'b0000;#10; if(sum===4'b0000&&carry===0) passed_tests=passed_tests+1; else failed_tests=failed_tests+1;
        a=4'b1111;b=4'b0000;#10; if(sum===4'b1111&&carry===0) passed_tests=passed_tests+1; else failed_tests=failed_tests+1;
        a=4'b0000;b=4'b1111;#10; if(sum===4'b1111&&carry===0) passed_tests=passed_tests+1; else failed_tests=failed_tests+1;
        a=4'b1111;b=4'b1111;#10; if(sum===4'b1110&&carry===1) passed_tests=passed_tests+1; else failed_tests=failed_tests+1;
        a=4'b0010;b=4'b0011;#10; if(sum===4'b0101&&carry===0) passed_tests=passed_tests+1; else failed_tests=failed_tests+1;
        a=4'b0111;b=4'b0111;#10; if(sum===4'b1110&&carry===0) passed_tests=passed_tests+1; else failed_tests=failed_tests+1;
        a=4'b1000;b=4'b0111;#10; if(sum===4'b1111&&carry===0) passed_tests=passed_tests+1; else failed_tests=failed_tests+1;
        a=4'b1000;b=4'b1000;#10; if(sum===4'b0000&&carry===1) passed_tests=passed_tests+1; else failed_tests=failed_tests+1;
        a=4'b0101;b=4'b1010;#10; if(sum===4'b1111&&carry===0) passed_tests=passed_tests+1; else failed_tests=failed_tests+1;
        a=4'b1100;b=4'b0011;#10; if(sum===4'b1111&&carry===0) passed_tests=passed_tests+1; else failed_tests=failed_tests+1;
        $display("Summary: %0d passed, %0d failed", passed_tests, failed_tests); $finish;
    end
endmodule