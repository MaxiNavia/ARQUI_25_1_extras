----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 15.11.2024 16:00:53
-- Design Name: 
-- Module Name: demux - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity demux is
    Port ( demux_in : in STD_LOGIC;
           ram_address : in STD_LOGIC_VECTOR (11 downto 0);
           demux_out_0 : out STD_LOGIC;
           demux_out_1 : out STD_LOGIC;
           demux_out_2 : out STD_LOGIC);
end demux;

architecture Behavioral of demux is

begin

with ram_address select
  demux_out_0 <= demux_in when "000000000010",
                 '0' when others;
with ram_address select
  demux_out_1 <= demux_in when "000000000000",
                 '0' when others;
with ram_address select
  demux_out_2 <= demux_in when "000000000111",
                 '0' when others;
end Behavioral;
