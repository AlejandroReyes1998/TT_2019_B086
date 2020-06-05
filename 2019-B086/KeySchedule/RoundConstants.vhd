LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.MATH_REAL.ALL;
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;


ENTITY RoundConstants IS

  PORT (
	 ADDR : IN  STD_LOGIC_VECTOR(1 DOWNTO 0);
	 DATA	: OUT STD_LOGIC_VECTOR(3 DOWNTO 0)
	 );
	 
END RoundConstants;
 
ARCHITECTURE RCArchitecture OF RoundConstants IS

TYPE ROM_MEMORY IS ARRAY (0 to 3) OF STD_LOGIC_VECTOR (3 downto 0);

SIGNAL ROM : ROM_MEMORY := ("0001",
									 "0011",
									 "0110",
									 "1011");
									 
BEGIN

	DATA <= ROM(CONV_INTEGER(ADDR));

END RCARCHITECTURE;
