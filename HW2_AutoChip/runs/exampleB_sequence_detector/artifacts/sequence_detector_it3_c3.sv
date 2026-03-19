module sequence_detector(
    input  logic clk,
    input  logic rst_n,
    input  logic [2:0] data,
    output logic seq_found
);

    // States
    enum logic [3:0] {
        S0,
        S1,
        S2,
        S3,
        S4,
        S5,
        S6,
        S7,
        S8,
        S9,
        S10,
        S11,
        S12,
        S13,
        S14,
        S15,
        S16,
        S17,
        S18,
        S19,
        S20,
        S21,
        S22
    } state, next_state;

    // State register
    logic [3:0] state_reg;

    // Sequence
    logic [3:0] seq = 4'b0011; // 001, 101, 110, 000, 110, 110, 011, 101

    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state_reg <= S0;
        end else begin
            state_reg <= next_state;
        end
    end

    always_comb begin
        case (state_reg)
            S0: next_state = (data == 3'b001) ? S1 : S0;
            S1: next_state = (data == 3'b101) ? S2 : S0;
            S2: next_state = (data == 3'b110) ? S3 : S0;
            S3: next_state = (data == 3'b000) ? S4 : S0;
            S4: next_state = (data == 3'b110) ? S5 : S0;
            S5: next_state = (data == 3'b110) ? S6 : S0;
            S6: next_state = (data == 3'b011) ? S7 : S0;
            S7: next_state = (data == 3'b101) ? S8 : S0;
            S8: next_state = S9;
            S9: next_state = S10;
            S10: next_state = S11;
            S11: next_state = S12;
            S12: next_state = S13;
            S13: next_state = S14;
            S14: next_state = S15;
            S15: next_state = S16;
            S16: next_state = S17;
            S17: next_state = S18;
            S18: next_state = S19;
            S19: next_state = S20;
            S20: next_state = S21;
            S21: next_state = S22;
            S22: next_state = S0;
            default: next_state = S0;
        endcase

        seq_found = (state_reg == S22);
    end

endmodule
