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
#LEFT_HAND = GenericHID.Hand.kLeft
#RIGHT_HAND = GenericHID.Hand.kRight

class Robot(wpilib.TimedRobot):
    def robotInit(self):
        #Controllers
        #self.driver = wpilib.XboxController(0)
        self.operator = wpilib.XboxController(0)


        """
        #Motors
        self.left_side = wpilib.SpeedControllerGroup(robotmap.LEFT_LEADER_ID, robotmap.LEFT_FOLLOWER_ID)
        self.right_side = wpilib.SpeedControllerGroup(robotmap.RIGHT_LEADER_ID, robotmap.RIGHT_FOLLOWER_ID)
        
        #Drivetrain
        self.drivetrain = wpilib.drive.DifferentialDrive(self.left_side, self.right_side)

        #TODO: Add subsystems and sensors as the code is written
        #TODO: SmartDashboard
        """
        # Color Sensor
        self.colorSensor = color_sensor()
        self.colorSensorMotor = rev_brushed(robotmap.COLOR_SENSOR_MOTOR)
       
        self.stopColorMap = {"r":"b", "y":"g", "b":"r", "g":"y"}
        self.gameData = ""
        
        
        
        


    def robotPeriodic(self):
        return
    
    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        self.turnedAmount = 8

        self.searchForColor = False

        self.turnWheel = False
        self.startColor = None

        self.currentColor = None
        self.lastColor = None

   
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

    def checkGameData(self):
        gd = str(wpilib.DriverStation.getInstance().getGameSpecificMessage())
        if(len(gd) > 0):
            self.gameData = gd

    def teleopPeriodic(self):
       
        
        
        #forward = self.driver.getRawAxis(5) #Right stick y-axis
        #forward = deadzone(forward, robotmap.deadzone)
        
        #rotation_value = self.driver.getX(LEFT_HAND)
        #TODO: figure out for sure what drive type we're using
        #self.drivetrain.arcadeDrive(forward, rotation_value)
        self.checkGameData()
            

        #TODO: Refactor this
        if self.searchForColor:
            if self.colorSensor.checkColor(self.gameData):
                self.colorSensorMotor.set(0.2)
            else:
                self.colorSensorMotor.set(0)
                self.searchForColor = False

        if self.operator.getXButton():
            self.startColor = self.stopColorMap[self.colorSensor.getColorName(self.colorSensor.getColor())]
            print(self.startColor)
            self.lastColor = self.startColor
            self.turnWheel = True
            print("START!")

        if self.operator.getAButton():
            self.searchForColor = True

        if self.turnWheel:
            self.debugColorSensor()
            self.colorSensorMotor.set(0.3)
            self.currentColor = self.colorSensor.getColorName(self.colorSensor.getColor())
            
            if self.currentColor != self.lastColor:
                if self.currentColor == self.startColor:
                    self.turnedAmount -= 1
                
                if self.turnedAmount == 0:
                    #if self.oneMoreTime:
                    self.colorSensorMotor.set(0)
                    self.turnWheel = False
                    #else:
                    #    self.oneMoreTime = True
                       
                    
                    

            print(self.turnedAmount)
            self.lastColor = self.currentColor
           
        
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