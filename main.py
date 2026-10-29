

import sys

from pathlib import Path

import subprocess



from PySide6.QtCore import QRegularExpression

from PySide6.QtGui import QRegularExpressionValidator

from PySide6.QtWidgets import (

    QApplication,

    QWidget,

    QLabel,

    QLineEdit,

    QPushButton,

    QVBoxLayout,

    QHBoxLayout,

    QGridLayout,

    QFrame,

)





class DigitalLock(QWidget):

    def __init__(self):

        super().__init__()



        self.setWindowTitle("Digital Lock System")

        self.setMinimumSize(480, 560)



        # System configuration
        self.correct_password = "1010"

        self.failed_attempts = 0

        self.max_attempts = 3

        self.access_granted = False

        self.locked = False

        self.attempt_history = []

        self.project_dir = Path(__file__).resolve().parent

        self.ghdl_path = r"C:\ghdl-mcode-6.0.0-mingw64\bin\ghdl.exe"



        # Main heading
        self.title = QLabel("Digital Lock")

        self.title.setObjectName("title")



        self.subtitle = QLabel(

            "PASSWORD-BASED SECURITY SIMULATOR"

        )

        self.subtitle.setObjectName("subtitle")



        # Password input
        self.password_label = QLabel(

            "ENTER FOUR-BIT PASSWORD"

        )

        self.password_label.setObjectName("fieldLabel")



        self.password_input = QLineEdit()

        self.password_input.setPlaceholderText("Enter 4-bit code")

        self.password_input.setMaxLength(4)

        self.password_input.setEchoMode(

            QLineEdit.EchoMode.Password

        )



        validator = QRegularExpressionValidator(

            QRegularExpression("[01]{0,4}"),

            self.password_input,

        )

        self.password_input.setValidator(validator)



        # Action buttons
        self.enter_button = QPushButton("Enter Password")

        self.enter_button.setObjectName("primaryButton")



        self.reset_button = QPushButton("Reset System")

        self.reset_button.setObjectName("secondaryButton")



        # Lock status panel
        self.lock_card = QFrame()

        self.lock_card.setObjectName("panel")



        self.lock_heading = QLabel("LOCK STATUS")

        self.lock_heading.setObjectName("panelHeading")



        self.lock_status = QLabel("READY")

        self.lock_status.setObjectName("ready")



        lock_layout = QVBoxLayout(self.lock_card)

        lock_layout.setContentsMargins(16, 16, 16, 16)

        lock_layout.setSpacing(10)

        lock_layout.addWidget(self.lock_heading)

        lock_layout.addWidget(self.lock_status)



        # Fan status panel
        self.fan_card = QFrame()

        self.fan_card.setObjectName("panel")



        self.fan_heading = QLabel("FAN OUTPUT")

        self.fan_heading.setObjectName("panelHeading")



        self.fan_status = QLabel("OFF")

        self.fan_status.setObjectName("fanOff")



        fan_layout = QVBoxLayout(self.fan_card)

        fan_layout.setContentsMargins(16, 16, 16, 16)

        fan_layout.setSpacing(10)

        fan_layout.addWidget(self.fan_heading)

        fan_layout.addWidget(self.fan_status)



        # Security information panel
        self.security_card = QFrame()

        self.security_card.setObjectName("panel")



        self.security_heading = QLabel("SECURITY MONITOR")

        self.security_heading.setObjectName("panelHeading")



        self.attempt_status = QLabel(

            "Failed attempts: 0 / 3"

        )



        self.remaining_status = QLabel(

            "Attempts remaining: 3"

        )



        security_layout = QVBoxLayout(self.security_card)

        security_layout.setContentsMargins(16, 16, 16, 16)

        security_layout.setSpacing(10)

        security_layout.addWidget(self.security_heading)

        security_layout.addWidget(self.attempt_status)

        security_layout.addWidget(self.remaining_status)



        # Feedback message
        self.message = QLabel(

            "System ready. Awaiting password."

        )

        self.message.setObjectName("message")

        self.message.setWordWrap(True)



        # Arrange status panels
        panels = QGridLayout()

        panels.addWidget(self.lock_card, 0, 0)

        panels.addWidget(self.fan_card, 0, 1)

        panels.addWidget(self.security_card, 1, 0, 1, 2)

        panels.setSpacing(12)



        # Arrange buttons
        buttons = QHBoxLayout()

        buttons.setSpacing(10)

        buttons.addWidget(self.enter_button)

        buttons.addWidget(self.reset_button)



        # Main layout
        layout = QVBoxLayout()

        layout.setContentsMargins(26, 26, 26, 26)

        layout.setSpacing(16)



        layout.addWidget(self.title)

        layout.addWidget(self.subtitle)

        layout.addSpacing(8)

        layout.addWidget(self.password_label)

        layout.addWidget(self.password_input)

        layout.addLayout(buttons)

        layout.addLayout(panels)

        layout.addWidget(self.message)

        layout.addStretch()



        self.setLayout(layout)



        # Connect controls
        self.enter_button.clicked.connect(self.check_password)

        self.reset_button.clicked.connect(self.reset_lock)

        self.password_input.returnPressed.connect(

            self.check_password

        )



        # Soft ivory, sage, and lavender styling
        self.setStyleSheet("""

            QWidget {

                background-color: #F7F5EF;

                color: #414A45;

                font-size: 13px;

                font-family: "Segoe UI";

            }



            QLabel#title {

                color: #496956;

                font-size: 32px;

                font-weight: bold;

            }



            QLabel#subtitle {

                color: #8A8D84;

                font-size: 10px;

                letter-spacing: 2px;

            }



            QLabel#fieldLabel {

                color: #596A5E;

                font-size: 11px;

                font-weight: bold;

                letter-spacing: 1px;

            }



            QLineEdit {

                background-color: #FFFDF8;

                border: 1px solid #D5DCCF;

                border-radius: 10px;

                padding: 13px;

                color: #414A45;

                font-size: 17px;

                selection-background-color: #DCE9DE;

            }



            QLineEdit:focus {

                border: 2px solid #9BB7A0;

            }



            QLineEdit:disabled {

                background-color: #ECEBE5;

                color: #92968F;

            }



            QPushButton {

                border-radius: 10px;

                padding: 12px 10px;

                font-weight: bold;

                min-height: 18px;

            }



            QPushButton#primaryButton {

                background-color: #789681;

                color: #FFFFFF;

                border: 1px solid #789681;

            }



            QPushButton#primaryButton:hover {

                background-color: #688773;

            }



            QPushButton#secondaryButton {

                background-color: #EAE5F0;

                color: #675B78;

                border: 1px solid #D8CFE4;

            }



            QPushButton#secondaryButton:hover {

                background-color: #DED6E9;

            }



            QPushButton:disabled {

                background-color: #E5E5DF;

                color: #A0A29A;

                border: 1px solid #E5E5DF;

            }



            QFrame#panel {

                background-color: #FFFDF8;

                border: 1px solid #E5E2D8;

                border-radius: 12px;

            }



            QLabel#panelHeading {

                background-color: transparent;

                color: #858A80;

                font-size: 10px;

                font-weight: bold;

                letter-spacing: 1px;

            }



            QLabel#ready {

                background-color: transparent;

                color: #66846D;

                font-size: 20px;

                font-weight: bold;

            }



            QLabel#granted {

                background-color: transparent;

                color: #4D815E;

                font-size: 19px;

                font-weight: bold;

            }



            QLabel#denied {

                background-color: transparent;

                color: #B56C6C;

                font-size: 19px;

                font-weight: bold;

            }



            QLabel#locked {

                background-color: transparent;

                color: #A84F58;

                font-size: 19px;

                font-weight: bold;

            }



            QLabel#fanOn {

                background-color: transparent;

                color: #4D815E;

                font-size: 20px;

                font-weight: bold;

            }



            QLabel#fanOff {

                background-color: transparent;

                color: #9B8B64;

                font-size: 20px;

                font-weight: bold;

            }



            QLabel#message {

                background-color: transparent;

                color: #777C73;

                padding: 6px 2px;

            }

        """)







    def run_vhdl(self):

        input_file = self.project_dir / "bridge_input.txt"

        output_file = self.project_dir / "bridge_output.txt"



        if output_file.exists():
            output_file.unlink()

        with input_file.open("w", encoding="utf-8") as file:

            for code in self.attempt_history:

                file.write(f"{code} 1\n")



        commands = [

            [self.ghdl_path, "-a", "--std=08", "DigitalLockFinal.vhd"],

            [self.ghdl_path, "-a", "--std=08", "lock_bridge_tb.vhd"],

            [self.ghdl_path, "-e", "--std=08", "lock_bridge_tb"],

            [self.ghdl_path, "-r", "--std=08", "lock_bridge_tb"],

        ]



        for command in commands:

            result = subprocess.run(

                command,

                cwd=self.project_dir,

                capture_output=True,

                text=True

            )



            if result.returncode != 0:

                details = result.stderr.strip() or result.stdout.strip()

                raise RuntimeError(details or "GHDL simulation failed.")



        if not output_file.exists():

            raise RuntimeError("The VHDL output file was not created.")



        lines = [

            line.split()

            for line in output_file.read_text(encoding="utf-8").splitlines()

            if line.strip()

        ]



        if len(lines) != len(self.attempt_history) + 1:

            raise RuntimeError(

                "Unexpected VHDL output. Check the testbench."

            )



        return lines[-1]



    def check_password(self):

        if self.locked:

            return



        entered = self.password_input.text()



        if len(entered) != 4 or any(bit not in "01" for bit in entered):

            self.message.setText("Please enter four binary digits (0 or 1).")

            return



        self.password_input.clear()

        self.attempt_history.append(entered)



        try:

            fan, lockout, attempt_bits, correct = self.run_vhdl()

        except Exception as error:

            self.attempt_history.pop()

            self.password_input.setText(entered)

            self.message.setText(f"VHDL simulation error: {error}")

            return



        self.failed_attempts = int(attempt_bits, 2)

        self.locked = lockout == "1"

        self.access_granted = fan == "1"



        if fan == "1":

            self.fan_status.setText("ON")

            self.fan_status.setObjectName("fanOn")

        else:

            self.fan_status.setText("OFF")

            self.fan_status.setObjectName("fanOff")



        if self.locked:

            self.lock_status.setText("SYSTEM LOCKED")

            self.lock_status.setObjectName("locked")

            self.message.setText(

                "Maximum failed attempts reached. "

                "Press RESET to unlock the system."

            )

            self.password_input.setDisabled(True)

            self.enter_button.setDisabled(True)



        elif correct == "1":

            self.lock_status.setText("ACCESS GRANTED")

            self.lock_status.setObjectName("granted")

            self.message.setText("Correct password. Access granted.")



        else:

            self.lock_status.setText("ACCESS DENIED")

            self.lock_status.setObjectName("denied")

            self.message.setText("Incorrect password.")



        self.update_security_panel()

        self.refresh_status_styles()





    def update_security_panel(self):

        remaining = max(

            0,

            self.max_attempts - self.failed_attempts

        )



        self.attempt_status.setText(

            f"Failed attempts: {self.failed_attempts} / "

            f"{self.max_attempts}"

        )



        self.remaining_status.setText(

            f"Attempts remaining: {remaining}"

        )



    def refresh_status_styles(self):

        for label in (

            self.lock_status,

            self.fan_status,

        ):

            label.style().unpolish(label)

            label.style().polish(label)

            label.update()





    def reset_lock(self):

        self.attempt_history.clear()



        try:

            fan, lockout, attempt_bits, correct = self.run_vhdl()

        except Exception as error:

            self.message.setText(f"VHDL simulation error during reset: {error}")

            return



        self.failed_attempts = int(attempt_bits, 2)

        self.access_granted = fan == "1"

        self.locked = lockout == "1"



        self.password_input.clear()

        self.password_input.setDisabled(False)

        self.enter_button.setDisabled(False)



        self.lock_status.setText("READY")

        self.lock_status.setObjectName("ready")

        self.fan_status.setText("OFF")

        self.fan_status.setObjectName("fanOff")

        self.message.setText("System reset. Awaiting password.")



        self.update_security_panel()

        self.refresh_status_styles()







if __name__ == "__main__":

    app = QApplication(sys.argv)



    window = DigitalLock()

    window.show()



    sys.exit(app.exec())
