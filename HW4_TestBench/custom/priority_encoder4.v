
module priority_encoder4 (
    input wire [3:0] d,
    output reg valid,
    output reg [1:0] enc
);
    always @* begin
        valid = |d;
        casez (d)
            4'b1???: enc = 2'b11;
            4'b01??: enc = 2'b10;
            4'b001?: enc = 2'b01;
            4'b0001: enc = 2'b00;
            default: enc = 2'b00;
        endcase
    end
endmodule
