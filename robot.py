import wpilib
from wpilib.interfaces import GenericHID
#TODO: What else will we need for 2020?
#TODO: Create and import subsystems (shooter, climb, etc.)

#This year, all IDs are stored in the robotmap
import robotmap

#Controller hands (sides)
LEFT_HAND = GenericHID.Hand.kLeft
RIGHT_HAND = GenericHID.Hand.kRight

class Robot(wpilib.TimedRobot):
    def robotInit(self):
        #Controllers
        self.driver = wpilib.XboxController(0)
        self.operator = wpilib.XboxController(1)

        #Motors
        self.left_side = wpilib.SpeedControllerGroup(robotmap.LEFT_LEADER_ID, robotmap.LEFT_FOLLOWER_ID)
        self.right_side = wpilib.SpeedControllerGroup(robotmap.RIGHT_LEADER_ID, robotmap.RIGHT_FOLLOWER_ID)

        #Drivetrain
        self.drivetrain = wpilib.drive.DifferentialDrive(self.left_side, self.right_side)

        #TODO: Add subsystems and sensors as the code is written
        #TODO: SmartDashboard

    def robotPeriodic(self):
        return
    
    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        #TODO: Add encoders, other sensors
        # print("Teleop begins!")
        pass

    def teleopPeriodic(self):
        forward = self.driver.getRawAxis(5) #Right stick y-axis
        forward = deadzone(forward, robotmap.deadzone)
        
        rotation_value = self.driver.getX(LEFT_HAND)
        #TODO: figure out for sure what drive type we're using
        self.drivetrain.arcadeDrive(forward, rotation_value)
        
def deadzone(val, deadzone):
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

if __name__ == "__main__":
	wpilib.run(Robot)