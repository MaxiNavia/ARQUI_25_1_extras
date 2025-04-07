----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 27.09.2024 15:14:10
-- Design Name: 
-- Module Name: Control_unit - Behavioral
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

entity Control_unit is
    Port ( rom_data : in STD_LOGIC_VECTOR (19 downto 0);
           status : in STD_LOGIC_VECTOR (2 downto 0);
           enableA : out std_logic;
           enableB : out std_logic;
           selA : out std_logic_vector (1 downto 0);
           selB : out std_logic_vector (1 downto 0);
           loadPC : out std_logic;
           selALU : out std_logic_vector (2 downto 0);
           w : out std_logic;
           sel_Add : out STD_LOGIC_VECTOR (1 downto 0);
           inc_sp : out std_logic;
           dec_sp : out std_logic;
           sel_pc : out std_logic;
           sel_din : out std_logic);
end Control_unit;
-- ####################################################
-- ####     IMPORTANTE:   LEER ANTES DE SEGUIR     ####
-- #################################################### 

-- esta control unit NO ESTA COMPLETA faltan:

        -- algunas señales etapa 2
        
-- sin embargo esta todo conectado y hardcodeado 
-- cosa de llegar y reemplazar/rellenar lo que falte

-- ####################################################
-- ####         GRACIAS POR SU ATENCION <3         ####
-- #################################################### 

architecture Behavioral of Control_unit is

signal opcode : std_logic_vector (6 downto 0);
signal cntrl_unit : std_logic_vector (16 downto 0);
signal c : std_logic;
signal z : std_logic;
signal n : std_logic;

begin
opcode <= rom_data (6 downto 0);
--     enable a ## enable b ## sel a ## sel b ## sel alu ## -load pc- ## w ## sel add ## inc sp ## dec sp ## -sel pc- ## sel din ##
with opcode select 
cntrl_unit <= "10000100000" & "000000" when "0000001", -- MOV A, B 
              "01100000000" & "000000" when "0000010", -- MOV B, A 
              "10001000000" & "000000" when "0000011", -- MOV A, LIT 
              "01001000000" & "000000" when "0000100", -- MOV B, LIT 
              "10001100000" & "000000" when "0000101", -- MOV A, (DIR) 
              "01001100000" & "000000" when "0000110", -- MOV B, (DIR)
              "00100000001" & "000000" when "0000111", -- MOV (DIR), A
              "00000100001" & "000000" when "0001000", -- MOV (DIR), B
              "10001100000" & "100000" when "1000100", -- MOV A, (B)
              "01001100000" & "100000" when "1000101", -- MOV B, (B)
              "00100000001" & "100000" when "1000110", -- MOV (B), A
              "00001000001" & "100000" when "1000111", -- MOV (B), LIT
              
              "10100100000" & "000000" when "0001001", -- ADD A, B
              "01100100000" & "000000" when "0001010", -- ADD B, A
              "10101000000" & "000000" when "0001011", -- ADD A, LIT
              "01101000000" & "000000" when "0001100", -- ADD B, LIT 
              "10101100000" & "000000" when "0001101", -- ADD A, (DIR)
              "01101100000" & "000000" when "0001110", -- ADD B, (DIR) 
              "00100100001" & "000000" when "0001111", -- (DIR)
              "10101100000" & "100000" when "1001000", -- ADD A, (B) 
              "01101100000" & "100000" when "1001001", -- ADD B, (B)
              
              "10100100100" & "000000" when "0010000", -- SUB A, B
              "01100100100" & "000000" when "0010001", -- SUB B, A
              "10101000100" & "000000" when "0010010", -- SUB A, LIT 
              "01101000100" & "000000" when "0010011", -- SUB B, LIT 
              "10101100100" & "000000" when "0010100", -- SUB A, (DIR)
              "01101100100" & "000000" when "0010101", -- SUB B, (DIR) 
              "00100100101" & "000000" when "0010110", -- SUB (DIR)
              "10101100100" & "100000" when "1001010", -- SUB A,(B)
              "01101100100" & "100000" when "1001011", -- SUB B, (B)
              
              "10100101000" & "000000" when "0010111", -- AND A, B
              "01100101000" & "000000" when "0011000", -- AND B, A
              "10101001000" & "000000" when "0011001", -- AND A, LIT
              "01101001000" & "000000" when "0011010", -- AND B, LIT 
              "10101101000" & "000000" when "0011011", -- AND A, (DIR)
              "01101101000" & "000000" when "0011100", -- AND B, (DIR)
              "00100101001" & "000000" when "0011101", -- AND (DIR)
              "10101101000" & "100000" when "1001100", -- AND A, (B)
              "01101101000" & "100000" when "1001101", -- AND B, (B)
              
              "10100101100" & "000000" when "0011110", -- OR A, B
              "01100101100" & "000000" when "0011111", -- OR B, A
              "10101001100" & "000000" when "0100000", -- OR A, LIT 
              "01101001100" & "000000" when "0100001", -- OR B, LIT 
              "10101101100" & "000000" when "0100010", -- OR A, (DIR)
              "01101101100" & "000000" when "0100011", -- OR B, (DIR) 
              "00100101101" & "000000" when "0100100", -- OR (DIR)
              "10101101100" & "100000" when "1001110", -- OR A, (B)
              "01101101100" & "100000" when "1001111", -- OR B, (B)
              
              "10100110000" & "000000" when "0100101", -- XOR A, B
              "01100110000" & "000000" when "0100110", -- XOR B, A
              "10101010000" & "000000" when "0100111", -- XOR A, LIT
              "01101010000" & "000000" when "0101000", -- XOR B, LIT 
              "10101110000" & "000000" when "0101001", -- XOR A, (DIR)
              "01101110000" & "000000" when "0101010", -- XOR B, (DIR) 
              "00100110001" & "000000" when "0101011", -- XOR (DIR)
              "10101110000" & "100000" when "1010000", -- XOR A, (B)
              "01101110000" & "100000" when "1010001", -- XOR B, (B)
              
              "10100010100" & "000000" when "0101100", -- NOT A
              "01100010100" & "000000" when "0101101", -- NOT B, A
              "00100010101" & "000000" when "0101110", -- NOT (DIR), A
              "00100010101" & "100000" when "1010010", -- NOT (B), A
              
              "10100011100" & "000000" when "0101111", -- SHL A
              "01100011100" & "000000" when "0110000", -- SHL B, A
              "00100011101" & "000000" when "0110001", -- SHL (DIR), A
              "00100011101" & "100000" when "1010011", -- SHL (B), A
              
              "10100011000" & "000000" when "0110010", -- SHR 
              "01100011000" & "000000" when "0110011", -- SHR B, A 
              "00100011001" & "000000" when "0110100", -- SHR (DIR), A
              "00100011001" & "100000" when "1010100", -- SHR (B), A
              
              "10101000000" & "000000" when "0110101", -- INC A ***
              "01010100000" & "000000" when "0110110", -- INC B
              "00011100001" & "000000" when "0110111", -- INC (DIR)
              "00011100001" & "100000" when "1010101", -- INC (B)
              
              "10101000100" & "000000" when "0111000", -- DEC A ***
              
              "00100100100" & "000000" when "0111001", -- CMP A, B
              "00101000100" & "000000" when "0111010", -- CMP A, LIT
              "00101100100" & "000000" when "0111011", -- CMP A. (DIR)
              "00101100100" & "100000" when "1010110", -- CMP A, (B)
              
              "00100000001" & "010100" when "1010111", -- PUSH A
              "00000100001" & "010100" when "1011000", -- PUSH B
              "00001100000" & "001000" when "1011001", -- POP A 1
              "10001100000" & "010000" when "1011010", -- POP A 2
              "00001100000" & "001000" when "1011011", -- POP B
              "01001100000" & "010000" when "1011100", -- POP B 2
              "00000000011" & "010111" when "1011101", -- CALL
              "00000000000" & "001000" when "1011110", -- RET 1
              "00000000010" & "010000" when "1011111", -- RET 2
              "00000000000000000" when others; 

c <= status(2);
z <= status(1);
n <= status(0);

with opcode select
loadPC <= '1'               when "0111100", -- JMP
          z                 when "0111101", -- JEQ
          not(z)            when "0111110", -- JNE
          not(n) and not(z) when "0111111", -- JGT
          n                 when "1000001", -- JLT
          not(n)            when "1000000", -- JGE
          n or z            when "1000010", -- JLE
          c                 when "1000011", -- JCR
          '1'               when "1011101", -- CALL
          '1'               when "1011111", -- RET 2
          '0'               when others;
with opcode select 
sel_pc <= '1'               when "0111100", -- JMP
          z                 when "0111101", -- JEQ
          not(z)            when "0111110", -- JNE
          not(n) and not(z) when "0111111", -- JGT
          n                 when "1000001", -- JLT
          not(n)            when "1000000", -- JGE
          n or z            when "1000010", -- JLE
          c                 when "1000011", -- JCR
          '1'               when "1011101", -- CALL
          '0'               when others;

-- enable a >> 16
enableA <= cntrl_unit(16);
-- enable b >> 15
enableB <= cntrl_unit(15);
-- sel a >> 14 downto 13
selA <= cntrl_unit(14 downto 13);
-- sel b >> 12 downto 11
selB <= cntrl_unit(12 downto 11);
-- sel alu >> 10 downto 8
selALU <= cntrl_unit(10 downto 8);
-- w >> 6
w <= cntrl_unit(6);
-- sel add >> 5 downto 4 
sel_Add <= cntrl_unit(5 downto 4);
-- inc sp  >> 3
inc_sp <= cntrl_unit(3);
-- dec sp >> 2
dec_sp <= cntrl_unit(2);
-- sel din >> 0
sel_din <= cntrl_unit(0);

end Behavioral;
