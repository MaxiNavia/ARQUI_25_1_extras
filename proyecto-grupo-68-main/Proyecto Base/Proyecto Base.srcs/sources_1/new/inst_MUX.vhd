----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 25.10.2024 15:01:03
-- Design Name: 
-- Module Name: inst_MUX - Behavioral
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

entity inst_MUX is
    Port ( MUX_in_0 : in STD_LOGIC_VECTOR (15 downto 0);
           MUX_in_1 : in STD_LOGIC_VECTOR (15 downto 0);
           MUX_in_2 : in STD_LOGIC_VECTOR (15 downto 0);
           MUX_in_3 : in STD_LOGIC_VECTOR (15 downto 0);
           MUX_sel : in STD_LOGIC_VECTOR (1 downto 0);
           MUX_out : out STD_LOGIC_VECTOR (15 downto 0));
end inst_MUX;

architecture Behavioral of inst_MUX is
begin
with MUX_sel select 
MUX_out <= MUX_in_0 when "00",
           MUX_in_1 when "01",
           MUX_in_2 when "10",
           MUX_in_3 when "11";
end Behavioral;
