LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.MATH_REAL.ALL;
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;


ENTITY BufferT IS

  PORT (
    CLK								: IN  STD_LOGIC;
	 WD							   : IN  STD_LOGIC;
	 DATA_IN							: IN STD_LOGIC_VECTOR(31 DOWNTO 0);
	 DATA_OUT					   : OUT STD_LOGIC_VECTOR(31 DOWNTO 0)
	 );
	 
END BufferT;
 
ARCHITECTURE RMemory OF BufferT IS

TYPE RAM_TYPE IS ARRAY (0 to 0) OF STD_LOGIC_VECTOR (31 DOWNTO 0);
SIGNAL RAM : RAM_TYPE;
									 
BEGIN

	RamProc: process(CLK) IS
	BEGIN
		IF RISING_EDGE(CLK) THEN
			IF (WD='1') THEN
				RAM(0)<=DATA_IN;
			END IF;
		END IF;
	END PROCESS RamProc;

	DATA_OUT<=RAM(0);
				

END RMemory;