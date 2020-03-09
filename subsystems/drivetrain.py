import wpilib
import wpilib.drive

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

    def shift():
        if self.gearshiftPosition == "Low":
            self.gear_shift.retract()
            self.gearPos = "High"
        else:
            self.gear_shift.extend()
            self.gearPos = "Low"
