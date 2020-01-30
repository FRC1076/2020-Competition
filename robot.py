import wpilib
from wpilib.interfaces import GenericHID

#This year, all IDs are stored in the robotmap
from robotmap import robot

LEFT_HAND = GenericHID.Hand.kLeft
RIGHT_HAND = GenericHID.Hand.kRight

class Robot(wpilib.TimedRobot):
    def robotInit(self):
        #DRIVETRAIN
        self.driver = wpilib.XboxController(0)
        self.operator = wpilib.XboxController(1)

        self.left_side = wpilib.SpeedControllerGroup(robot["LEFT_LEADER_ID"], robot["LEFT_FOLLOWER_ID"])
        self.right_side = wpilib.SpeedControllerGroup(robot["RIGHT_LEADER_ID"], robot["RIGHT_FOLLOWER_ID"])

        self.drivetrain = wpilib.drive.DifferentialDrive(self.left_side, self.right_side)

    def robotPeriodic(self):
        return
    
    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        #self.encoder = wpilib.Encoder(0,1)
        #setup wheel diameter
        print("Teleop begins!")

    def teleopPeriodic(self):
        forward = self.driver.getRawAxis(5)
        rotation_value = self.driver.getX(LEFT_HAND)
        #TODO: figure out for sure what drive type we're using
        self.drivetrain.arcadeDrive(forward, rotation_value)
        
        #print(self.encoder.get())

if __name__ == "__main__":
	wpilib.run(Robot)
    
