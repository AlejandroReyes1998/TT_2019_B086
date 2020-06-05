LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.NUMERIC_BIT.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE work.KSPackage.ALL;

ENTITY Ks IS
 
	PORT (
          const_ronda_addr : in std_logic_vector(1 downto 0);
          const_ronda_delta : in std_logic_vector(1 downto 0);
          sumador : in std_logic_vector(4 downto 0);
          buffer_t_rw : in std_logic;
          memoria_t_addr : in std_logic_vector(1 downto 0);
          memoria_t_rw : in std_logic;
          memoria_t_mux : in std_logic;
          kmem_in: in std_logic_vector(31 downto 0);
          CLK: in std_logic
	);
 
END Ks;

ARCHITECTURE KsArchitecture OF Ks IS

--SIGNAL MYBus : STD_LOGIC_VECTOR(33 DOWNTO 0);
SIGNAL Sum	 : STD_LOGIC_VECTOR(5 DOWNTO 0);
SIGNAL RolResult1,RolResult2: STD_LOGIC_VECTOR(31 DOWNTO 0) ;
SIGNAL MAResult: STD_LOGIC_VECTOR(31 DOWNTO 0);
SIGNAL DCoutput: STD_LOGIC_VECTOR(31 DOWNTO 0);
SIGNAL RCoutput: STD_LOGIC_VECTOR(3 DOWNTO 0);
SIGNAL Muxoutput: STD_LOGIC_VECTOR(31 DOWNTO 0);
SIGNAL BToutput: STD_LOGIC_VECTOR(31 DOWNTO 0);
SIGNAL TMoutput: STD_LOGIC_VECTOR(31 DOWNTO 0);


BEGIN
	
C0 : Adder
PORT MAP(
    A =>"000"&const_ronda_addr,
    B =>sumador,
    Cin =>'0',
    Cout => Sum(5),
    Sum => Sum(4 DOWNTO 0)
    );

	 C5 : RolComponent
		PORT MAP(
			N => Sum(4 DOWNTO 0),
			OP => DCoutput,
			RESULT =>RolResult2
	);
	 
	C1 : RolComponent
		PORT MAP(
			N => '0'&RCoutput,
			OP => MAResult,
			RESULT =>RolResult1
	);
	
	C2 : ModulusAddition
		PORT MAP(
			OpA => RolResult2,
			OpB => BToutput,
			Result => MAResult
	);
	
	C3: DeltaConstants
        PORT MAP(
			Addr => '0'&const_ronda_delta,
			Data => DCoutput
	);	
	
	C4: RoundConstants
	PORT MAP(
			Addr => const_ronda_addr,
			Data => RCoutput
	);

	
			
	C7 : Mux2to1
		PORT MAP(
			A=> kmem_in,
			B=> RolResult1,
			S=> memoria_t_mux,
			C=> Muxoutput
		);
		
	MyBufferT : BufferT
		PORT MAP(
			CLK => CLK,
			WD => buffer_t_rw,
			DATA_IN => TMoutput,
			DATA_OUT => BToutput
		);
		
	TMemory : RAMMemory
		PORT MAP(
			CLK => CLK,
			ADDR => memoria_t_addr,
			WD => memoria_t_rw,
			DATA_IN =>Muxoutput,
			DATA_OUT =>TMoutput
		);
        
		
END KsArchitecture;
