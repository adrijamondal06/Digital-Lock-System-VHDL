--------------------------------------------------------------------------------
-- Company: 
-- Engineer:
--
-- Create Date:   08:54:07 10/28/2026
-- Design Name:   
-- Module Name:   /home/ise/DigitalLockFinal/DigitalLockFinal_tb.vhd
-- Project Name:  DigitalLockFinal
-- Target Device:  
-- Tool versions:  
-- Description:   
-- 
-- VHDL Test Bench Created by ISE for module: DigitalLockFinal
-- 
-- Dependencies:
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
--
-- Notes: 
-- This testbench has been automatically generated using types std_logic and
-- std_logic_vector for the ports of the unit under test.  Xilinx recommends
-- that these types always be used for the top-level I/O of a design in order
-- to guarantee that the testbench will bind correctly to the post-implementation 
-- simulation model.
--------------------------------------------------------------------------------
LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
 
-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--USE ieee.numeric_std.ALL;
 
ENTITY DigitalLockFinal_tb IS
END DigitalLockFinal_tb;
 
ARCHITECTURE behavior OF DigitalLockFinal_tb IS 
 
    -- Component Declaration for the Unit Under Test (UUT)
 
    COMPONENT DigitalLockFinal
    PORT(
         clk : IN  std_logic;
         reset : IN  std_logic;
         enter : IN  std_logic;
         resistor_input : IN  std_logic_vector(3 downto 0);
         fan : OUT  std_logic;
         lockout : OUT  std_logic;
         attempt_count : OUT  std_logic_vector(1 downto 0);
         correct : OUT  std_logic
        );
    END COMPONENT;
    

   --Inputs
   signal clk : std_logic := '0';
   signal reset : std_logic := '0';
   signal enter : std_logic := '0';
   signal resistor_input : std_logic_vector(3 downto 0) := (others => '0');

 	--Outputs
   signal fan : std_logic;
   signal lockout : std_logic;
   signal attempt_count : std_logic_vector(1 downto 0);
   signal correct : std_logic;

 
 
BEGIN
 
	-- Instantiate the Unit Under Test (UUT)
   uut: DigitalLockFinal PORT MAP (
          clk => clk,
          reset => reset,
          enter => enter,
          resistor_input => resistor_input,
          fan => fan,
          lockout => lockout,
          attempt_count => attempt_count,
          correct => correct
        );

   -- Clock process definitions
   clk_process :process
   begin
	  while true loop
		clk <= '0';
		wait for 10 ns;
		clk <= '1';
		wait for 10 ns;
	  end loop;
   end process;
 

   -- Stimulus process
   stim_proc: process
   begin		
      -- TEST 0: Initial reset
        reset <= '1';
        enter <= '0';
        resistor_input <= "0000";
        wait for 40 ns;

        reset <= '0';
        wait for 20 ns;

        -- TEST 1: Correct resistor code (1010)
        resistor_input <= "1010";
        enter <= '1';
        wait for 20 ns;

        enter <= '0';
        wait for 20 ns;

        -- Reset before testing incorrect attempts
        reset <= '1';
        wait for 20 ns;

        reset <= '0';
        wait for 20 ns;
		  
		  -- TEST 2: First incorrect attempt
        resistor_input <= "1111";
        enter <= '1';
        wait for 20 ns;

        enter <= '0';
        wait for 20 ns;

        -- TEST 3: Second incorrect attempt
        resistor_input <= "0000";
        enter <= '1';
        wait for 20 ns;

        enter <= '0';
        wait for 20 ns;

        -- TEST 4: Third incorrect attempt
        resistor_input <= "1100";
        enter <= '1';
        wait for 20 ns;

        enter <= '0';
        wait for 20 ns;
		  
		  -- TEST 5: Correct code while locked
        resistor_input <= "1010";
        enter <= '1';
        wait for 20 ns;

        enter <= '0';
        wait for 20 ns;

        -- TEST 6: Reset after lockout
        reset <= '1';
        wait for 20 ns;

        reset <= '0';
        enter <= '0';
        wait for 20 ns;


      -- insert stimulus here 

      wait;
   end process;

END;
