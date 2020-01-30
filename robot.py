import wpilib
from wpilib.interfaces import GenericHID

#This year, all IDs are stored in the robotmap
import robotmap

LEFT_HAND = GenericHID.Hand.kLeft
RIGHT_HAND = GenericHID.Hand.kRight

class Robot(wpilib.TimedRobot):
    def robotInit(self):
        #DRIVETRAIN
        self.driver = wpilib.XboxController(0)
        self.operator = wpilib.XboxController(1)

        self.left_side = createTalonAndFollower(robotmap.robot["LEFT_MASTER_ID"], robotmap.robot["LEFT_FOLLOWER_ID"])
        self.right_side = createTalonAndFollower(robotmap.robot["RIGHT_MASTER_ID"], robotmap.robot["RIGHT_FOLLOWER_ID"])

        self.drivetrain = wpilib.drive.DifferentialDrive(self.left_side, self.right_side)

    def robotPeriodic(self):
        return
    
    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        self.encoder = wpilib.Encoder(0,1)
        # setup wheel diameter
        print("Teleop begins!")

    def teleopPeriodic(self):
        forward = self.driver.getRawAxis(5)
        rotation_value = self.driver.getX(LEFT_HAND)
        self.drivetrain.arcadeDrive(forward, rotation_value)
        
        #print(self.encoder.get())

def createTalonAndFollower(MASTER, follower):
    '''
    First ID must be MASTER, Second ID must be follower talon
    This assumes that the left and right sides are the same, two talons.
    '''
    master_talon = wpilib.Talon(MASTER)
    follower_talon = wpilib.Talon(follower)
    follower_talon.follow(master_talon)
    return master_talon

if __name__ == "__main__":
	wpilib.run(Robot)
    