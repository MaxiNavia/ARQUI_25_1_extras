library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.std_logic_unsigned.all;
use IEEE.numeric_std.all;


entity CPU is
    Port (
           clock : in STD_LOGIC;
           clear : in STD_LOGIC;
           ram_address : out STD_LOGIC_VECTOR (11 downto 0);
           ram_datain : out STD_LOGIC_VECTOR (15 downto 0);
           ram_dataout : in STD_LOGIC_VECTOR (15 downto 0);
           ram_write : out STD_LOGIC;
           rom_address : out STD_LOGIC_VECTOR (11 downto 0);
           rom_dataout : in STD_LOGIC_VECTOR (35 downto 0));
           --dis : out STD_LOGIC_VECTOR (15 downto 0));
end CPU;

architecture Behavioral of CPU is
--##############################
--## REGISTROS 
--##############################

-- REG A
signal reg_a_out : std_logic_vector (15 downto 0);

-- REG B
signal reg_b_out : std_logic_vector (15 downto 0);

-- PROGRAM COUNTER 
signal out_pc : std_logic_vector (15 downto 0);

-- STATUS
signal status_in : std_logic_vector (15 downto 0);
signal status_out : std_logic_vector (15 downto 0);
-- FLAGS 
signal flag_c : std_logic;
signal flag_z : std_logic;
signal flag_n : std_logic;

-- STACK POINTER
signal SP_out : STD_LOGIC_VECTOR (15 downto 0);

--##############################
--## MULTIPLEXORES
--##############################

-- MUX A
signal muxA : std_logic_vector (15 downto 0);

-- MUX B
signal muxB : std_logic_vector (15 downto 0);

--MUX S
signal MUX_S : STD_LOGIC_VECTOR (11 downto 0);
signal MUX_S_16b : STD_LOGIC_VECTOR (15 downto 0);
signal MUX_S_IN_0 : STD_LOGIC_VECTOR (15 downto 0);
signal MUX_S_IN_1 : STD_LOGIC_VECTOR (15 downto 0);
signal MUX_S_IN_2 : STD_LOGIC_VECTOR (15 downto 0);

-- MUX PC 
signal MUX_PC : STD_LOGIC_VECTOR (15 downto 0);
signal MUX_PC_IN_0 : STD_LOGIC_VECTOR (15 downto 0);
signal MUX_PC_IN_1 : STD_LOGIC_VECTOR (15 downto 0);

-- MUX DATA IN 
signal MUX_Datain : std_logic_vector (15 downto 0);

--##############################
--## OPERADORES 
--##############################

-- ALU

signal alu_result : std_logic_vector (15 downto 0);

--ADDER DATA IN 
signal Adder_out : std_logic_vector (15 downto 0);
signal Adder_Cout : STD_LOGIC;



--##############################
--## CONTROL UNIT
--##############################

--inc dec sp
signal incSP : std_logic;
signal decSP : std_logic;
--enabler a 
signal enA : std_logic;
--enabler b
signal enB : std_logic;
--load pc
signal lpc : std_logic;
--sel alu
signal sAlu : std_logic_vector (2 downto 0);
--sel datain
signal selDIn : std_logic;
signal selDIn_2b : STD_LOGIC_VECTOR (1 downto 0);
--sel pc
signal selPC : std_logic;
signal selPC_2b : STD_LOGIC_VECTOR (1 downto 0);
--sel mux s 
signal selAdd : std_logic_vector (1 downto 0);
--mux b
signal sB : std_logic_vector (1 downto 0);
--mux a
signal sA : std_logic_vector (1 downto 0);
-- write
signal write : STD_LOGIC;


component Reg -- No Tocar
    Port (
        clock       : in    std_logic;
        clear       : in    std_logic;
        load        : in    std_logic;
        up          : in    std_logic;
        down        : in    std_logic;
        datain      : in    std_logic_vector (15 downto 0);
        dataout     : out   std_logic_vector (15 downto 0)
          );
    end component;
    
component ALU -- No Tocar
    Port ( 
        a           : in    std_logic_vector (15 downto 0);
        b           : in    std_logic_vector (15 downto 0);
        sop         : in    std_logic_vector (2 downto 0);
        c           : out   std_logic;
        z           : out   std_logic;
        n           : out   std_logic;
        result      : out   std_logic_vector (15 downto 0)
          );
    end component;
    
component Control_unit is
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
end component;

component inst_MUX is
    Port ( MUX_in_0 : in STD_LOGIC_VECTOR (15 downto 0);
           MUX_in_1 : in STD_LOGIC_VECTOR (15 downto 0);
           MUX_in_2 : in STD_LOGIC_VECTOR (15 downto 0);
           MUX_in_3 : in STD_LOGIC_VECTOR (15 downto 0);
           MUX_sel : in STD_LOGIC_VECTOR (1 downto 0);
           MUX_out : out STD_LOGIC_VECTOR (15 downto 0));
end component;

component Adder16 is
    Port ( a : in STD_LOGIC_VECTOR (15 downto 0);
           b : in STD_LOGIC_VECTOR (15 downto 0);
           s : out STD_LOGIC_VECTOR (15 downto 0);
           Cin : in STD_LOGIC;
           Cout : out STD_LOGIC);
end component;

begin

    -- declaracion de instancias
-- REG A   
inst_REG_A: Reg port map( -- Repárame!
    clock       => clock,
    clear       => clear,
    load        => enA,
    up          => '0',
    down        => '0',
    datain      => alu_result,
    dataout     => reg_a_out
    );
    
-- REG B
inst_REG_B: Reg port map( -- Repárame!
    clock       => clock,
    clear       => clear,
    load        => enB,
    up          => '0',
    down        => '0',
    datain      => alu_result,
    dataout     => reg_b_out
    );
    
-- ALU
 inst_ALU: ALU port map(
    a           => muxA,
    b           => muxB,
    sop         => sAlu,
    c           => flag_c,
    z           => flag_z,
    n           => flag_n,
    result      => alu_result
    );
    
-- PROGRAM COUNTER 
inst_PC : Reg port map( -- Repárame!
    clock       => clock,
    clear       => clear,
    load        => lpc,
    up          => '1',
    down        => '0',
    datain      => MUX_PC,
    dataout     => out_pc
    );
    
-- STATUS
status_in <= "0000000000000" & flag_c & flag_z & flag_n;
inst_status :  Reg port map( -- Repárame!
    clock       => clock,
    clear       => clear,
    load        => '1',
    up          => '0',
    down        => '0',
    datain      => status_in,
    dataout     => status_out
    );

-- STACK POINTER
inst_SP :  Reg port map( -- Repárame!
    clock       => clock,
    clear       => '0',
    load        => clear,
    up          => incSP,
    down        => decSP,
    datain      => "0000111111111111",
    dataout     => SP_out
    );

-- CNTRL UNIT 
 inst_control_unit: control_unit port map(
           rom_data => rom_dataout (35 downto 16),
           status => status_out (2 downto 0),
           enableA => enA,
           enableB => enB,
           selA => sA,
           selB => sB,
           loadPC => lpc,
           selALU => sAlu,
           w => write, 
           sel_Add => selAdd,
           inc_sp => incSP,
           dec_sp => decSP,
           sel_pc => selPC,
           sel_din => selDIn 
           
       );
       
 -- ADDER DATA IN 
 inst_Adder : Adder16 port map (
           a => "0000000000000001",
           b => out_pc,
           s => Adder_out,
           Cin => '0',
           Cout => Adder_Cout
            );
       
 --muxes
 -- MUX A
inst_MUX_A: inst_MUX port map (
           MUX_in_0 => "0000000000000000",
           MUX_in_1 => "0000000000000001",
           MUX_in_2 => reg_a_out,
           MUX_in_3 => "0000000000000000",
           MUX_sel => sA,
           MUX_out => muxA
            );
            
-- MUX B
inst_MUX_B: inst_MUX port map (
           MUX_in_0 => "0000000000000000",
           MUX_in_1 => reg_b_out,
           MUX_in_2 => rom_dataout(15 downto 0),
           MUX_in_3 => ram_dataout,
           MUX_sel => sB,
           MUX_out => muxB
            );
            
-- MUX DATA IN
selDIn_2b <= '0'& selDIn;
inst_MUX_Datain: inst_MUX port map (
           MUX_in_0 => alu_result,
           MUX_in_1 => Adder_out,
           MUX_in_2 => "0000000000000000",
           MUX_in_3 => "0000000000000000",
           MUX_sel => selDIn_2b,
           MUX_out => MUX_Datain
            );

-- MUX S chek
MUX_S_IN_0<= "0000" & rom_dataout (11 downto 0);
MUX_S_IN_2 <= "0000" & reg_b_out (11 downto 0);

inst_MUX_S: inst_MUX port map (
           MUX_in_0 => MUX_S_IN_0,
           MUX_in_1 => SP_out,
           MUX_in_2 => MUX_S_IN_2,
           MUX_in_3 => "0000000000000000",
           MUX_sel => selAdd,
           MUX_out => MUX_S_16b
            );
MUX_S <= MUX_S_16b (11 downto 0);

-- MUX PC chek
MUX_PC_IN_0 <= ram_dataout;
MUX_PC_IN_1 <= "0000" & rom_dataout (11 downto 0); --LIT 
selPC_2b <= '0' & selPC;
inst_MUX_PC: inst_MUX port map (
           MUX_in_0 => MUX_PC_IN_0,
           MUX_in_1 => MUX_PC_IN_1,
           MUX_in_2 => "0000000000000000",
           MUX_in_3 => "0000000000000000",
           MUX_sel => selPC_2b,
           MUX_out => MUX_PC
            );

-- SALIDASSS
ram_write <= write;
rom_address <= out_pc (11 downto 0);
ram_address <= MUX_S;
ram_datain <= MUX_Datain;
--dis <=  reg_a_out (7 downto 0) & reg_b_out (7 downto 0);
end Behavioral;

