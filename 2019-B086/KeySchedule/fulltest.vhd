LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.NUMERIC_BIT.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
USE work.KSPackage.ALL;
entity ks_tb is
end ks_tb;

architecture behavior of ks_tb is
  component Ks is
    PORT (
          const_ronda_addr : in std_logic_vector(1 downto 0);
          const_ronda_delta : in std_logic_vector(1 downto 0);
          sumador : in std_logic_vector(3 downto 0);
          buffer_t_addr : in std_logic_vector(1 downto 0);
          buffer_t_rw : in std_logic;
          memoria_t_addr : in std_logic_vector(1 downto 0);
          memoria_t_rw : in std_logic;
          memoria_t_mux : in std_logic;
          kmem_in : in std_logic_vector(32 downto 0);
          CLK: in std_logic
          );
    end component;
    signal cra : std_logic_vector(1 downto 0);
    signal crd : std_logic_vector(1 downto 0);
    signal sum:  std_logic_vector(3 downto 0);
    signal bta: std_logic_vector(1 downto 0);
    signal btrw: std_logic;
    signal mta: std_logic_vector(1 downto 0);
    signal mtrw: std_logic;
    signal mtmux: std_logic;
  signal clkin:std_logic;
  signal kmi : std_logic_vector(32 downto 0);
begin
    uut: Ks port map (
      const_ronda_addr => cra,
      const_ronda_delta => crd,
      sumador => sum,
      buffer_t_addr => bta,
      buffer_t_rw => btrw,
      memoria_t_addr => mta,
      memoria_t_rw => mtrw,
      memoria_t_mux => mtmux,
      kmem_in => kmi,
      CLK => clkin
    );

    stim_proc: process
    begin
      clkin <= '0';
      wait for 10 ns;
      -- write t0
      cra <= "00";
      crd <= "00";
      sum <= "0000";
      bta <=  "00";
      btrw <= '0';
      mta <= "00";
      mtrw <= '1';
      mtmux <= '1';
      kmi <= "01010101101010101010010100010010";
      clkin <= '1';
      wait for 10 ns;
      clkin <= '0';
      wait for 10 ns;
      -- write t1
      cra <= "00";
      crd <= "00";
      sum <= "0000";
      bta <=  "00";
      btrw <= '0';
      mta <= "01";
      mtrw <= '1';
      mtmux <= '1';
      kmi <= "01001000010010010101000100101111";
      clkin <= '1';
      wait for 10 ns;
      clkin <= '0';
      wait for 10 ns;
      -- write t2
      cra <= "00";
      crd <= "00";
      sum <= "0000";
      bta <=  "00";
      btrw <= '0';
      mta <= "10";
      mtrw <= '1';
      mtmux <= '1';
      kmi <= "01010101101010110101001001010010";
      clkin <= '1';
      wait for 10 ns;
      clkin <= '0';
      wait for 10 ns;
      -- write t3
      cra <= "00";
      crd <= "00";
      sum <= "0000";
      bta <=  "00";
      btrw <= '0';
      mta <= "11";
      mtrw <= '1';
      mtmux <= '1';
      kmi <= "11110101010000100111101001000000";
      clkin <= '1';
      wait for 10 ns;
      clkin <= '0';
      wait for 10 ns;
      --keyschedule
      wait;
    end process;
end;
