----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 13.09.2024 15:47:52
-- Design Name: 
-- Module Name: Adder16 - Behavioral
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

entity Adder16 is
    Port ( a : in STD_LOGIC_VECTOR (15 downto 0);
           b : in STD_LOGIC_VECTOR (15 downto 0);
           s : out STD_LOGIC_VECTOR (15 downto 0);
           Cin : in STD_LOGIC;
           Cout : out STD_LOGIC);
end Adder16;

architecture Behavioral of Adder16 is

component Adder8 is
    Port ( a8  : in  std_logic_vector (7 downto 0);
           b8  : in  std_logic_vector (7 downto 0);
           ci : in  std_logic;
           s8  : out std_logic_vector (7 downto 0);
           co : out std_logic);
end component;

signal c :  std_logic; 

begin

inst_adder1: Adder8 port map(
        a8      => a(7 downto 0),
        b8      => b(7 downto 0),
        ci     => cin,
        s8      => s(7 downto 0),
        co     => c
);

inst_adder2: Adder8 port map(
        a8      => a(15 downto 8),
        b8      => b(15 downto 8),
        ci     => c,
        s8      => s(15 downto 8),
        co     => Cout
);

end Behavioral;
