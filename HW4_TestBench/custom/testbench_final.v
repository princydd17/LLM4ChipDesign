module priority_encoder4_tb;
    reg [3:0] d;
    wire valid;
    wire [1:0] enc;

    priority_encoder4 uut (.d(d), .valid(valid), .enc(enc));

    integer passed_tests, failed_tests;
    integer i;

    function [0:0] exp_valid(input [3:0] x);
        begin
            exp_valid = (x != 4'b0000);
        end
    endfunction

    function [1:0] exp_enc(input [3:0] x);
        begin
            if (x[3])       exp_enc = 2'b11;
            else if (x[2])  exp_enc = 2'b10;
            else if (x[1])  exp_enc = 2'b01;
            else             exp_enc = 2'b00;
        end
    endfunction

    initial begin
        passed_tests = 0;
        failed_tests = 0;

        for (i = 0; i < 20; i = i + 1) begin
            case (i)
                0:  d = 4'b0000;
                1:  d = 4'b0001;
                2:  d = 4'b0010;
                3:  d = 4'b0011;
                4:  d = 4'b0100;
                5:  d = 4'b0101;
                6:  d = 4'b0110;
                7:  d = 4'b0111;
                8:  d = 4'b1000;
                9:  d = 4'b1001;
                10: d = 4'b1010;
                11: d = 4'b1011;
                12: d = 4'b1100;
                13: d = 4'b1101;
                14: d = 4'b1110;
                15: d = 4'b1111;
                16: d = 4'b1010; // random
                17: d = 4'b0100; // random
                18: d = 4'b1100; // random
                19: d = 4'b0001; // random
            endcase

            #10;

            if (valid === exp_valid(d) && enc === exp_enc(d)) begin
                passed_tests = passed_tests + 1;
            end else begin
                failed_tests = failed_tests + 1;
                $display("Fail i=%0d d=%b valid=%b enc=%b", i, d, valid, enc);
            end
        end

        $display("Summary: %0d passed, %0d failed", passed_tests, failed_tests);
        $finish;
    end
endmodule