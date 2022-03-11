module spram #(
    parameter int DEPTH = 16, //length of ram entries
    parameter int WIDTH = 32, //width of data 
    parameter int DEPTH_L2 = $clog2(DEPTH)
)(
    input  bit                clk,
    input  bit                wr_valid,
    input  bit [DEPTH_L2-1:0] wr_addr,
    input  bit [WIDTH-1:0]    wr_data,
    input  bit                rd_valid,
    output bit                rd_ready,
    output bit [WIDTH-1:0]    rd_data,
    output bit [DEPTH_L2-1:0] rd_addr
);
    //infer RAM
    bit [WIDTH-1:0] ram [(2**DEPTH_L2)-1:0];

    always_ff @(posedge clk) begin
        if(wr_valid) begin
            ram[wr_addr] <= wr_data;
        end
        rd_ready <= rd_valid;
        rd_data <= ram[rd_addr];
    end

endmodule
