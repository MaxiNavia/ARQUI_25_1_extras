library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity ALU is
    Port ( a        : in  std_logic_vector (15 downto 0);   -- Primer operando.
           b        : in  std_logic_vector (15 downto 0);   -- Segundo operando.
           sop      : in  std_logic_vector (2 downto 0);   -- Selector de la operación.
           c        : out std_logic;                       -- Señal de 'carry'.
           z        : out std_logic;                       -- Señal de 'zero'.
           n        : out std_logic;                       -- Señal de 'nagative'.
           result   : out std_logic_vector (15 downto 0));  -- Resultado de la operación.
end ALU;

architecture Behavioral of ALU is

signal alu_result   : std_logic_vector(15 downto 0);
signal adder_result   : std_logic_vector(15 downto 0);
signal cout_adder : std_logic;
signal b_signal   : std_logic_vector(15 downto 0);
signal cin_adder : std_logic;


signal shl_result : std_logic_vector(15 downto 0);
signal and_result : std_logic_vector(15 downto 0);
signal or_result : std_logic_vector(15 downto 0);
signal xor_result : std_logic_vector(15 downto 0);
signal shr_result : std_logic_vector(15 downto 0);
signal not_result : std_logic_vector(15 downto 0);

signal z1 : std_logic;


component Adder16 is
    Port ( a : in STD_LOGIC_VECTOR (15 downto 0);
           b : in STD_LOGIC_VECTOR (15 downto 0);
           s : out STD_LOGIC_VECTOR (15 downto 0);
           Cin : in STD_LOGIC;
           Cout : out STD_LOGIC);
end component;

begin

-- Sumador/Restaror

with sop select
    b_signal <= not b     when "001", -- sub
                b when others; -- other operation
                  
with sop select
    cin_adder <= '1' when "001", -- sub
                 '0' when others;   
                 
and_result <= a and b;

or_result <= a or b;
    
xor_result <= a xor b;
    
not_result <= not a;
                 
shl_result <= a(14 downto 0) & '0';

shr_result <= '0' & a(15 downto 1);
             
-- Resultado de la Operación
               
with sop select
    alu_result <= adder_result     when "000", -- add
                  adder_result     when "001", -- sub
                  and_result    when "010", -- and
                  or_result     when "011", -- or
                  xor_result     when "100", -- xor
                  not_result     when "101", -- not 
                  shr_result     when "110", -- shr
                  shl_result     when "111"; -- shl
                  
result  <= alu_result;

inst_sum: Adder16 port map(
        a      => a,
        b      => b_signal,
        Cin     => cin_adder,
        s      => adder_result,
        Cout     => cout_adder
);


-- Flags c z n
with sop select
    c <= '0' when "010",
         '0' when "011",
         '0' when "100",
         '0' when "101",
         cout_adder when "000",
         cout_adder when "001",
         a(0) when "110",
         a(15) when "111";

with sop select
    n <= not cout_adder when "001",
         '0' when others;
         
with sop select
    z <= not (adder_result(0) or adder_result(1) or adder_result(2) or adder_result(3) or adder_result(4) or adder_result(5) or adder_result(6) or adder_result(7) or adder_result(8) or adder_result(9) or adder_result(10) or adder_result(11) or adder_result(12) or adder_result(13) or adder_result(14) or adder_result(15)) when "000",
         not (adder_result(0) or adder_result(1) or adder_result(2) or adder_result(3) or adder_result(4) or adder_result(5) or adder_result(6) or adder_result(7) or adder_result(8) or adder_result(9) or adder_result(10) or adder_result(11) or adder_result(12) or adder_result(13) or adder_result(14) or adder_result(15)) when "001",
         not (and_result(0) or and_result(1) or and_result(2) or and_result(3) or and_result(4) or and_result(5) or and_result(6) or and_result(7) or and_result(8) or and_result(9) or and_result(10) or and_result(11) or and_result(12) or and_result(13) or and_result(14) or and_result(15)) when "010",
         not (or_result(0) or or_result(1) or or_result(2) or or_result(3) or or_result(4) or or_result(5) or or_result(6) or or_result(7) or or_result(8) or or_result(9) or or_result(10) or or_result(11) or or_result(12) or or_result(13) or or_result(14) or or_result(15)) when "011",
         not (xor_result(0) or xor_result(1) or xor_result(2) or xor_result(3) or xor_result(4) or xor_result(5) or xor_result(6) or xor_result(7)or xor_result(8) or xor_result(9) or xor_result(10) or xor_result(11) or xor_result(12) or xor_result(13) or xor_result(14) or xor_result(15)) when "100",
         not (not_result(0) or not_result(1) or not_result(2) or not_result(3) or not_result(4) or not_result(5) or not_result(6) or not_result(7 )or not_result(8) or not_result(9) or not_result(10) or not_result(11) or not_result(12) or not_result(13) or not_result(14) or not_result(15)) when "101",
         not (shr_result(0) or shr_result(1) or shr_result(2) or shr_result(3) or shr_result(4) or shr_result(5) or shr_result(6) or shr_result(7)or shr_result(8) or shr_result(9) or shr_result(10) or shr_result(11) or shr_result(12) or shr_result(13) or shr_result(14) or shr_result(15)) when "110",
         not (shl_result(0) or shl_result(1) or shl_result(2) or shl_result(3) or shl_result(4) or shl_result(5) or shl_result(6) or shl_result(7) or shl_result(8) or shl_result(9) or shl_result(10) or shl_result(11) or shl_result(12) or shl_result(13) or shl_result(14) or shl_result(15)) when "111";
end Behavioral;