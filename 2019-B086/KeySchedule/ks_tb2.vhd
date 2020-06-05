LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.NUMERIC_BIT.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;

entity ks_tb2 is
end ks_tb2;

architecture behavior of ks_tb2 is
  component Ks is
    PORT (
      const_ronda_addr : in std_logic_vector(1 downto 0);
      const_ronda_delta : in std_logic_vector(1 downto 0);
      sumador : in std_logic_vector(4 downto 0);
      buffer_t_rw : in std_logic;
      memoria_t_addr : in std_logic_vector(1 downto 0);
      memoria_t_rw : in std_logic;
      memoria_t_mux : in std_logic;
      kmem_in : in std_logic_vector(31 downto 0);
      CLK: in std_logic
      );
  end component;
  
  signal cra : std_logic_vector(1 downto 0);
  signal crd : std_logic_vector(1 downto 0);
  signal sum:  std_logic_vector(4 downto 0);
  signal btrw: std_logic;
  signal mta: std_logic_vector(1 downto 0);
  signal mtrw: std_logic;
  signal mtmux: std_logic;
  signal clkin:std_logic;
  signal kmi : std_logic_vector(31 downto 0);
begin
    uut: Ks port map (
      const_ronda_addr => cra,
      const_ronda_delta => crd,
      sumador => sum,
      buffer_t_rw => btrw,
      memoria_t_addr => mta,
      memoria_t_rw => mtrw,
      memoria_t_mux => mtmux,
      kmem_in => kmi,
      CLK => clkin
    );

    stim_proc: process
	 variable imod4 : std_logic_vector(1 downto 0) := "00";
	 variable iloop : std_logic_vector(4 downto 0) := "00000";
	 variable jloop : std_logic_vector(1 downto 0) := "00";
    begin

      wait for 10 ns;
      -- write t0
      cra <= "00";
      crd <= "00";
      sum <= "00000";
      btrw <= '0';
      mta <= "00";
      mtrw <= '1';
      mtmux <= '1';
      kmi <= "11001000010010010101000100101111";
      wait for 10 ns;
      -- write t1
      cra <= "00";
      crd <= "00";
      sum <= "00000";
      btrw <= '0';
      mta <= "01";
      mtrw <= '1';
      mtmux <= '1';
      kmi <= "01110101101010110101001001010010";
      wait for 10 ns;
      -- write t2
      cra <= "00";
      crd <= "00";
      sum <= "00000";
      btrw <= '0';
      mta <= "10";
      mtrw <= '1';
      mtmux <= '1';
      kmi <= "11110101010000100111101001000100";
      wait for 10 ns;
      -- write t3
      cra <= "00";
      crd <= "00";
      sum <= "00000";
      btrw <= '0';
      mta <= "11";
      mtrw <= '1';
      mtmux <= '1';
      kmi <= "01001000010011010111010100101111";
      wait for 10 ns;
	 
-- le spitball
		for i in 0 to 23 loop 
			imod4 := iloop(1 downto 0);
			for j in 0 to 3 loop	
				cra <= conv_std_logic_vector(j, 2); -- dirección de la memoria de constantes de ronda (j)
				crd <= imod4; --dirección de la memoria constantes delta (i)
				sum <= conv_std_logic_vector(i, 5); -- (i)
				btrw <= '1'; -- modo escritura en buffer T
				mta <= conv_std_logic_vector(j, 2); -- dirección de lectura de la memoria T (j)
				mtrw <= '0'; -- modo lectura en memoria T
				mtmux <= '1'; 
				kmi <= (OTHERS=>'0');
				wait for 10 ns;
				mtrw <= '1';
				mtmux <= '0';
				wait for 1 ns;
				jloop := jloop + "01";
			end loop;
			iloop := iloop + "00001";
		end loop;
		
		
		mtrw <= '0';

		
		
----------------------------------------------------------------------------------------------
		wait;
		
		
    end process;
end behavior;
