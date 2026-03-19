// Hand-written sequence detector RTL for HW2 Example B.
// Detects the 3-bit sequence on consecutive cycles:
//   001, 101, 110, 000, 110, 110, 011, 101
//
// The testbench expects:
// - synchronous active-low reset (reset_n)
// - output `sequence_found` is 1 for exactly one cycle when the final symbol matches
//   (i.e., when the 8 most-recent input symbols equal the sequence).

module sequence_detector (
    input        clk,
    input        reset_n,      // active-low, synchronous
    input  [2:0] data,
    output       sequence_found
);

    // Store last 8 symbols (8 * 3 bits = 24 bits).
    reg [23:0] history;
    wire [23:0] history_nxt = {history[20:0], data};

    // history_nxt layout (MSB..LSB):
    //   {sym1, sym2, sym3, sym4, sym5, sym6, sym7, sym8}
    localparam [23:0] PATTERN = {
        3'b001, 3'b101, 3'b110, 3'b000,
        3'b110, 3'b110, 3'b011, 3'b101
    };

    // Combinational pulse (aligned to the testbench's cycle counting):
    // asserted when the *next* history (including current `data`) matches.
    assign sequence_found = reset_n && (history_nxt == PATTERN);

    // Shift history each cycle.
    always @(posedge clk) begin
        if (!reset_n)
            history <= 24'd0;
        else
            history <= history_nxt;
    end

endmodule

