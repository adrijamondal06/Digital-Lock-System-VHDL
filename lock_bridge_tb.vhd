
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;
use STD.TEXTIO.ALL;
use IEEE.STD_LOGIC_TEXTIO.ALL;

entity lock_bridge_tb is
end lock_bridge_tb;

architecture simulation of lock_bridge_tb is

    signal clk            : STD_LOGIC := '0';
    signal reset          : STD_LOGIC := '0';
    signal enter          : STD_LOGIC := '0';
    signal resistor_input : STD_LOGIC_VECTOR(3 downto 0) := "0000";

    signal fan            : STD_LOGIC;
    signal lockout        : STD_LOGIC;
    signal attempt_count  : STD_LOGIC_VECTOR(1 downto 0);
    signal correct        : STD_LOGIC;

begin

    clk <= not clk after 10 ns;

    DUT: entity work.DigitalLockFinal
        port map (
            clk            => clk,
            reset          => reset,
            enter          => enter,
            resistor_input => resistor_input,
            fan            => fan,
            lockout        => lockout,
            attempt_count  => attempt_count,
            correct        => correct
        );

    stimulus: process
        file input_file : TEXT open READ_MODE
                          is "bridge_input.txt";
        file output_file : TEXT open WRITE_MODE
                          is "bridge_output.txt";

        variable in_line     : LINE;
        variable out_line    : LINE;
        variable code_text   : STRING(1 to 4);
        variable enter_value : INTEGER;
        variable code_value  : STD_LOGIC_VECTOR(3 downto 0);

    begin
        -- Reset the digital lock.
        reset <= '1';
        enter <= '0';

        wait for 40 ns;
        wait until falling_edge(clk);
        reset <= '0';

        -- Write the initial reset-state output.
        wait for 1 ns;

        WRITE(out_line, fan);
        WRITE(out_line, STRING'(" "));
        WRITE(out_line, lockout);
        WRITE(out_line, STRING'(" "));
        WRITE(out_line, attempt_count);
        WRITE(out_line, STRING'(" "));
        WRITE(out_line, correct);
        WRITELINE(output_file, out_line);

        -- Replay every password attempt supplied by Python.
        while not ENDFILE(input_file) loop

            READLINE(input_file, in_line);
            READ(in_line, code_text);
            READ(in_line, enter_value);

            for i in 1 to 4 loop
                if code_text(i) = '1' then
                    code_value(4-i) := '1';
                else
                    code_value(4-i) := '0';
                end if;
            end loop;

            resistor_input <= code_value;

            if enter_value = 1 then
                enter <= '1';
            else
                enter <= '0';
            end if;

            wait until rising_edge(clk);
            wait for 1 ns;

            WRITE(out_line, fan);
            WRITE(out_line, STRING'(" "));
            WRITE(out_line, lockout);
            WRITE(out_line, STRING'(" "));
            WRITE(out_line, attempt_count);
            WRITE(out_line, STRING'(" "));
            WRITE(out_line, correct);

            WRITELINE(output_file, out_line);

        end loop;

        enter <= '0';

        wait for 1 ns;
        STD.ENV.STOP;
        wait;

    end process;

end simulation;
