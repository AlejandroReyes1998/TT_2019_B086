LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL; 
USE IEEE.NUMERIC_STD.ALL;

ENTITY NModulus IS
	
	PORT (
		N : in std_logic_vector(4 downto 0) ;
		operando : in std_logic_vector(31 downto 0);
		resultado : out std_logic_vector(31 downto 0)
	);
 
END NModulus;

ARCHITECTURE NMArchitecture OF NModulus IS


BEGIN

	resultado <= std_logic_vector(to_unsigned(to_integer(unsigned(operando)) mod to_integer(unsigned(N)), 32));
	
END NMArchitecture;