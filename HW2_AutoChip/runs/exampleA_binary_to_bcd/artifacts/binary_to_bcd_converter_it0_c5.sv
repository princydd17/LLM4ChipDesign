module binary_to_bcd_converter(
    input  [4:0] bin_input,
    output [7:0] bcd_output
);

    reg [7:0] bcd;
    reg [4:0] working_bin;

    always_comb begin
        working_bin = bin_input;
        bcd = 8'b0;

        for (int i = 0; i < 5; i++) begin
            if (bcd[3:0] >= 5) begin
                bcd[3:0] = bcd[3:0] + 3;
            end
            if (bcd[7:4] >= 5) begin
                bcd[7:4] = bcd[7:4] + 3;
            end
            {bcd, working_bin} = {bcd[6:0], working_bin[4:0], working_bin[4]};
        end
        bcd_output = bcd;
    end

endmodule
