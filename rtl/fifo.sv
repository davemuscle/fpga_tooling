module fifo #(
    parameter string FMODE = "SYNC", // "SYNC" or "ASYNC"
    parameter int    DEPTH = 8,      // length of fifo entries
    parameter int    WIDTH = 4       // data width
)(
    //clock/reset
    input bit wr_clk,
    input bit rd_clk, 
    input bit rst,

    //read/write
    input  bit             wr_valid,
    input  bit [WIDTH-1:0] wr_data,
    input  bit             rd_valid,
    output bit [WIDTH-1:0] rd_data,
    output bit             rd_ready,

    //full/empty status
    output bit full,
    output bit empty,

    //overflow/underflow
    output bit overflow, 
    output bit underflow
);

    parameter int DEPTH_L2 = $clog2(DEPTH);    

    bit [DEPTH_L2:0] wr_ptr, wr_ptr_gry, wr_ptr_gry_d0, wr_ptr_gry_d1, wr_ptr_rd = 0;
    bit [DEPTH_L2:0] rd_ptr, rd_ptr_gry, rd_ptr_gry_d0, rd_ptr_gry_d1, rd_ptr_wr = 0;

    bit wr_rst_d0, wr_rst_d1 = 0;
    bit rd_rst_d0, rd_rst_d1 = 0;

    //write domain
    always_ff @(posedge wr_clk) begin

        //synchronize reset
        wr_rst_d0 <= rst;
        wr_rst_d1 <= wr_rst_d0;
    
        //increment write pointer
        if(wr_valid & !full) begin
            wr_ptr <= wr_ptr + 1;
        end 
   
        if(FMODE == "ASYNC") begin 
            //encode write pointer
            wr_ptr_gry[DEPTH_L2]     <= wr_ptr[DEPTH_L2];
            wr_ptr_gry[DEPTH_L2-1:0] <= wr_ptr[DEPTH_L2:1] ^ wr_ptr[DEPTH_L2-1:0];
    
            //sync read pointer
            rd_ptr_gry_d0 <= rd_ptr_gry;
            rd_ptr_gry_d1 <= rd_ptr_gry_d0;
            
            //decode sync'd read pointer
            rd_ptr_wr[DEPTH_L2]     <= rd_ptr_gry_d1[DEPTH_L2];
            rd_ptr_wr[DEPTH_L2-1:0] <= rd_ptr_wr[DEPTH_L2:1] ^ rd_ptr_gry_d1[DEPTH_L2-1:0];
        end

        //full/overflow bits
        full <= (wr_ptr[DEPTH_L2-1:0] == rd_ptr_wr[DEPTH_L2-1:0]) ? (wr_ptr[DEPTH_L2] ^ rd_ptr_wr[DEPTH_L2]) : 0; 
        overflow <= (wr_valid & full & !wr_rst_d1) ? 1 : 0;

        //reset
        if(wr_rst_d1) begin
            wr_ptr        <= 0;
            if(FMODE == "ASYNC") begin
                wr_ptr_gry    <= 0;
                rd_ptr_gry_d0 <= 0;
                rd_ptr_gry_d1 <= 0;
                rd_ptr_wr     <= 0;
            end
        end
    end

    //read domain
    always_ff @(posedge rd_clk) begin

        //synchronize reset
        rd_rst_d0 <= rst;
        rd_rst_d1 <= rd_rst_d0;

        //increment read pointer
        if(rd_valid & !empty) begin
            rd_ptr <= rd_ptr + 1;
        end 

        if(FMODE == "ASYNC") begin
            //encode read pointer
            rd_ptr_gry[DEPTH_L2]     <= rd_ptr[DEPTH_L2];
            rd_ptr_gry[DEPTH_L2-1:0] <= rd_ptr[DEPTH_L2:1] ^ rd_ptr[DEPTH_L2-1:0];

            //sync write pointer
            wr_ptr_gry_d0 <= wr_ptr_gry;
            wr_ptr_gry_d1 <= wr_ptr_gry_d0;

            //decode sync'd read pointer
            wr_ptr_rd[DEPTH_L2]     <= wr_ptr_gry_d1[DEPTH_L2];
            wr_ptr_rd[DEPTH_L2-1:0] <= wr_ptr_rd[DEPTH_L2:1] ^ wr_ptr_gry_d1[DEPTH_L2-1:0];
        end

        //empty/underflow bit
        empty <= (rd_ptr == wr_ptr_rd) ? 1 : 0;
        underflow <= (rd_valid & empty & !rd_rst_d1) ? 1 : 0;

        //reset
        if(rd_rst_d1) begin
            rd_ptr        <= 0;
            wr_ptr_rd     <= 0;
            if(FMODE == "ASYNC") begin
                wr_ptr_rd     <= 0;
                rd_ptr_gry    <= 0;
                wr_ptr_gry_d0 <= 0;
                wr_ptr_gry_d1 <= 0;
            end
        end
    end
    
    //synchronous mode only, skip gray counters and dfs on pointers
    always_comb begin
        wr_ptr_rd = rd_ptr;
        rd_ptr_wr = wr_ptr;
    end

    //double check mode string parameters
    initial begin
        if(FMODE != "SYNC" && FMODE != "ASYNC") begin
            $error("Generic FIFO module FMODE param must be either SYNC or ASYNC");
        end
    end
    
    //infer RAM
    bit [WIDTH-1:0] ram [DEPTH-1:0];

    always_ff @(posedge wr_clk) begin
        if(wr_valid) begin
            ram[wr_ptr] <= wr_data;
        end
    end

    always_ff @(posedge rd_clk) begin
        rd_data <= ram[rd_ptr];
        rd_ready <= rd_valid;
    end

endmodule
