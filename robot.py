import wpilib
from wpilib.interfaces import GenericHID
#TODO: What else will we need for 2020?
#TODO: Create and import subsystems (shooter, climb, etc.)

#This year, all IDs are stored in the robotmap
import robotmap
from subsystems.color_sensor import color_sensor
from subsystems.rev_brushed import rev_brushed
import rev

#Controller hands (sides)
LEFT_HAND = wpilib._wpilib.XboxController.Hand.kLeftHand
RIGHT_HAND = wpilib._wpilib.XboxController.Hand.kRightHand


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        #Controllers
        self.driver = wpilib.XboxController(0)
        self.operator = wpilib.XboxController(1)

        #Motors
        self.left_motor_1 = rev.CANSparkMax(robotmap.LEFT_LEADER_ID, rev.MotorType.kBrushed)
        self.left_motor_2 = rev.CANSparkMax(robotmap.LEFT_FOLLOWER_ID, rev.MotorType.kBrushed)
        self.right_motor_1 = rev.CANSparkMax(robotmap.RIGHT_LEADER_ID, rev.MotorType.kBrushed)
        self.right_motor_2 = rev.CANSparkMax(robotmap.RIGHT_FOLLOWER_ID, rev.MotorType.kBrushed)
        
        self.left_side = wpilib.SpeedControllerGroup(self.left_motor_1, self.left_motor_2)
        self.right_side = wpilib.SpeedControllerGroup(self.right_motor_1, self.right_motor_2)
        
        #Drivetrain
        self.drivetrain = wpilib.drive.DifferentialDrive(self.left_side, self.right_side)

        #TODO: Add subsystems and sensors as the code is written
        #TODO: SmartDashboard

        # Color Sensor
        #self.colorSensor = color_sensor()
        #self.colorSensorMotor = rev_brushed()
        #self.searchForColor = False
        #self.turnWheel = False


        
        


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

    def debugColorSensor(self):
        c = self.colorSensor.getColor()
        red = c.red
        blue = c.blue
        green = c.green
        # TODO: Use better debugging tools
        print("Red: {} Green: {} Blue: {} ".format(red, green, blue))

    def teleopPeriodic(self):
        
        forward = self.driver.getY(RIGHT_HAND) #Right stick y-axis
        forward = deadzone(forward, robotmap.deadzone)
        
        rotation_value = self.driver.getX(LEFT_HAND)
	     
        self.drivetrain.arcadeDrive(forward, rotation_value)

        #TODO: Refactor this
        #if self.searchForColor:
        #    if self.colorSensor.checkColor():
        #        self.colorSensorMotor.set(0.2)
        #    else:
        #        self.colorSensorMotor.set(0)
        
	

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
