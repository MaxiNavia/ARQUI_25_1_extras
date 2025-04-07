----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 15.11.2024 15:27:36
-- Design Name: 
-- Module Name: mux8 - Behavioral
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

entity mux8 is
    Port ( mux_in_0 : in STD_LOGIC_VECTOR (15 downto 0);
           mux_in_1 : in STD_LOGIC_VECTOR (15 downto 0);
           mux_in_2 : in STD_LOGIC_VECTOR (15 downto 0);
           mux_in_3 : in STD_LOGIC_VECTOR (15 downto 0);
           mux_in_4 : in STD_LOGIC_VECTOR (15 downto 0);
           mux_in_5 : in STD_LOGIC_VECTOR (15 downto 0);
           ram_address : in STD_LOGIC_VECTOR (11 downto 0);
           mux_in_out : out STD_LOGIC_VECTOR (15 downto 0));
end mux8;

architecture Behavioral of mux8 is

begin

with ram_address select
mux_in_out <= mux_in_0 when "000000000100",
              mux_in_1 when "000000000101",
              mux_in_2 when "000000000110",
              mux_in_3 when "000000000001",
              mux_in_4 when "000000000011",
              mux_in_5 when others;
              

end Behavioral;
