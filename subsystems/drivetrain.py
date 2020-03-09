import wpilib
import wpilib.drive
import robotmap

class Drivetrain:
    """
    Handles basic movement and shifting
    """
    def __init__(self, left, right, gear_shifter):
        self.drive = wpilib.drive.DifferentialDrive(left, right)
        self.gear_shift = gear_shifter
        self.gearPos = -1

    def arcade_drive(self, forward, rotate):
        self.drive.arcadeDrive(forward, rotate)

    def shift(self):
        if self.gearPos == "Low":
            self.gear_shift.retract()
            self.gearPos = "High"
        else:
            self.gear_shift.extend()
            self.gearPos = "Low"

    def deadzone(self, val, deadzone=robotmap.deadzone):
            """
            Given the deadzone value x, the deadzone both eliminates all
            values between -x and x, and scales the remaining values from
            -1 to 1, to (-1 + x) to (1 - x)
            """
            if abs(val) < deadzone:
                return 0
            elif val < (0):
                x = ((abs(val) - deadzone)/(1-deadzone))
                return (-x)
            else:
                x = ((val - deadzone)/(1-deadzone))
                return (x)
