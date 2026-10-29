----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    08:47:32 10/28/2026 
-- Design Name: 
-- Module Name:    DigitalLockFinal - Behavioral 
-- Project Name: 
-- Target Devices: 
-- Tool versions: 
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
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity DigitalLockFinal is
    Port ( clk : in  STD_LOGIC;
           reset : in  STD_LOGIC;
           enter : in  STD_LOGIC;
           resistor_input : in  STD_LOGIC_VECTOR(3 downto 0);
           fan : out  STD_LOGIC;
           lockout : out  STD_LOGIC;
           attempt_count : out  STD_LOGIC_VECTOR(1 downto 0);
           correct : out  STD_LOGIC);
end DigitalLockFinal;

architecture Behavioral of DigitalLockFinal is
		 -- Four-bit stored resistor code
    constant STORED_RESISTOR_CODE :
        STD_LOGIC_VECTOR(3 downto 0) := "1010";

    signal attempts : UNSIGNED(1 downto 0) := "00";
    signal locked   : STD_LOGIC := '0';
    signal unlocked : STD_LOGIC := '0';
begin
	 process(clk, reset)
    begin
        if reset = '1' then
            attempts <= "00";
            locked   <= '0';
            unlocked <= '0';

        elsif rising_edge(clk) then

            if enter = '1' and locked = '0' then

                if resistor_input = STORED_RESISTOR_CODE then
                    unlocked <= '1';
				     else
                    unlocked <= '0';

                    -- Lock on the third incorrect attempt
                    if attempts = to_unsigned(2, 2) then
                        attempts <= "11";
                        locked   <= '1';
                    else
                        attempts <= attempts + 1;
                    end if;

                end if;

            end if;

        end if;
    end process;
	 -- Fan operates when access is granted
    fan <= unlocked and not locked;

    -- Lockout status
    lockout <= locked;

    -- Password correctness indication
    correct <= '1' when
        (resistor_input = STORED_RESISTOR_CODE and
         enter = '1' and locked = '0')
        else '0';

    -- Display failed-attempt count
    attempt_count <= STD_LOGIC_VECTOR(attempts);
	 
	 
end Behavioral;

