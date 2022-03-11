module dpram #(
    parameter int DEPTH = 16, //length of ram entries
    parameter int WIDTH = 32, //width of data 
    parameter int DEPTH_L2 = $clog2(DEPTH)
)(
    //port a
    input  bit                a_clk,
    input  bit                a_wr_valid,
    input  bit [DEPTH_L2-1:0] a_wr_addr,
    input  bit [WIDTH-1:0]    a_wr_data,
    input  bit                a_rd_valid,
    output bit                a_rd_ready,
    output bit [WIDTH-1:0]    a_rd_data,
    output bit [DEPTH_L2-1:0] a_rd_addr,

    //port b
    input  bit                b_clk,
    input  bit                b_wr_valid,
    input  bit [DEPTH_L2-1:0] b_wr_addr,
    input  bit [WIDTH-1:0]    b_wr_data,
    input  bit                b_rd_valid,
    output bit                b_rd_ready,
    output bit [WIDTH-1:0]    b_rd_data,
    output bit [DEPTH_L2-1:0] b_rd_addr
);
    //infer RAM
    bit [WIDTH-1:0] ram [(2**DEPTH_L2)-1:0];

    always_ff @(posedge a_clk) begin
        if(a_wr_valid) begin
            ram[a_wr_addr] <= a_wr_data;
        end
        a_rd_ready <= a_rd_valid;
        a_rd_data <= ram[a_rd_addr];
    end

    always_ff @(posedge b_clk) begin
        if(b_wr_valid) begin
            ram[b_wr_addr] <= b_wr_data;
        end
        b_rd_ready <= b_rd_valid;
        b_rd_data <= ram[b_rd_addr];
    end

endmodule
