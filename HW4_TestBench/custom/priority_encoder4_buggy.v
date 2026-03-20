
module priority_encoder4 (
    input wire [3:0] d,
    output reg valid,
    output reg [1:0] enc
);
    always @* begin
        valid = |d;
        casez (d)
            4'b???1: enc = 2'b11;   // BUG: d[0] treated as highest
            4'b??10: enc = 2'b10;
            4'b?100: enc = 2'b01;
            4'b1000: enc = 2'b00;   // BUG: d[3] treated as lowest
            default: enc = 2'b00;
        endcase
    end
endmodule
