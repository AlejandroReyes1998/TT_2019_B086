LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL; 
USE IEEE.NUMERIC_STD.ALL;


ENTITY ModulusAddition IS
 
	PORT (
		OpA, OpB : IN STD_LOGIC_VECTOR(31 DOWNTO 0);
		Result: OUT STD_LOGIC_VECTOR(31 DOWNTO 0)
	);
 
END ModulusAddition;

ARCHITECTURE MAArchitecture OF ModulusAddition IS


BEGIN
	
	Result<= std_logic_vector(unsigned(OpA) + unsigned(OpB));
	
END MAArchitecture;