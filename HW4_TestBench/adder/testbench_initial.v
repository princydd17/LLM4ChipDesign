module adder4bit_tb;
    // Instantiate the DUT using its exact module name
    adder4bit uut (
        .b(1'b0), // initial value
        .sum(4'b0000), // initial value
        .carry(1'b0) // initial value
    );

    // Test patterns
    parameter TB_SIZE = 16;
    reg [3:0] b [TB_SIZE-1:0];
    reg [3:0] a [TB_SIZE-1:0];
    wire [3:0] sum [TB_SIZE-1:0];
    wire carry [TB_SIZE-1:0];

    initial begin
        for (int i = 0; i < TB_SIZE; i++) begin
            // Set input b
            b[i] = i[3:0];
            // Set input a
            a[i] = i[3:0];

            // Apply input values
            uut.b <= b[i];
            uut.sum <= 4'b0000;
            uut.carry <= 1'b0;

            // Wait for 10 ns
            #10;

            // Check output sum
            assert(sum[i] === a[i] + b[i]) $display("Sum is correct for a=%h, b=%h", a[i], b[i]);
            else $display("Sum is incorrect for a=%h, b=%h", a[i], b[i]);

            // Check output carry
            if (a[i] + b[i] > 15) begin
                assert(carry[i] === 1'b1) $display("Carry is correct for a=%h, b=%h", a[i], b[i]);
            end else begin
                assert(carry[i] === 1'b0) $display("Carry is correct for a=%h, b=%h", a[i], b[i]);
            end

            // Wait for 10 ns
            #10;
        end
    end

endmodule