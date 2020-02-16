import wpilib
from wpilib.interfaces import GenericHID

import rev
from rev.color import ColorMatch
#TODO: What else will we need for 2020?
#TODO: Create and import subsystems (shooter, climb, etc.)

#This year, all IDs are stored in the robotmap
import robotmap


#Subsystems
from subsystems.color_sensor import color_sensor
from subsystems.rev_brushed import rev_brushed

#Controller hands (sides)
LEFT_HAND = wpilib._wpilib.XboxController.Hand.kLeftHand
RIGHT_HAND = wpilib._wpilib.XboxController.Hand.kRightHand


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        #Controllers
        self.driver = wpilib.XboxController(0)
        self.operator = wpilib.XboxController(0)


        
        #Motors
        self.left_side = wpilib.SpeedControllerGroup(robotmap.LEFT_LEADER_ID, robotmap.LEFT_FOLLOWER_ID)
        self.right_side = wpilib.SpeedControllerGroup(robotmap.RIGHT_LEADER_ID, robotmap.RIGHT_FOLLOWER_ID)
        
        #Drivetrain
        self.drivetrain = wpilib.drive.DifferentialDrive(self.left_side, self.right_side)

        #TODO: Add subsystems and sensors as the code is written
        #TODO: SmartDashboard
        
        # Color Sensor
        self.colorSensor = color_sensor()
        self.colorSensorMotor = rev_brushed(robotmap.COLOR_SENSOR_MOTOR)
       
        self.stopColorMap = {"r":"g", "y":"r", "b":"y", "g":"b"}
        
        self.gameData = ""
        
        self.setupColorSensor()


    def setupColorSensor(self)
        self.colorMatch = ColorMatch()
        
        self.blue = wpilib._wpilib.Color(0.143, 0.427, 0.429)
        self.green = wpilib._wpilib.Color(0.197, 0.561, 0.240)
        self.red = wpilib._wpilib.Color(0.561, 0.232, 0.144)
        self.yellow = wpilib._wpilib.Color(0.361, 0.524, 0.133)

        self.colorMap = {"b":self.blue, "g":self.green, "r":self.red, "y":self.yellow}
        
        self.colorMatch.addColorMatch(self.blue) #Blue
            
        self.colorMatch.addColorMatch(self.green) #Green
        self.colorMatch.addColorMatch(self.red) #Red
        self.colorMatch.addColorMatch(self.yellow)

    def robotPeriodic(self):
        return
    
    def autonomousInit(self):
        self.gameData = ""

    def autonomousPeriodic(self):
        pass

    def teleopInit(self):
        self.gameData = ""
        self.goal = ""
        self.turnedAmount = 8

        self.searchForColor = False

        self.turnWheel = False
        self.startColor = None

        self.currentColor = None
        self.lastColor = None
        
        
        self.found = False
   
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
        print(self.colorSensor.getColorName(c))

    def checkGameData(self):
        gd = wpilib.DriverStation.getInstance().getGameSpecificMessage()
        if(gd != None and not self.searchForColor):
            self.gameData = gd


    def turnWheelInit(self):
        self.currentColor = None
        self.lastColor = None
        self.startColor = self.stopColorMap[self.colorSensor.getColorName(self.colorSensor.getColor())]
        #print(self.startColor)
        self.lastColor = self.startColor
        self.turnWheel = True
        #print("START!")
    
    def turnWheelCycle(self):
        #self.debugColorSensor()
        self.colorSensorMotor.set(0.3)
        self.currentColor = self.colorSensor.getColorName(self.colorSensor.getColor())
        
        if self.currentColor != self.lastColor:            
            if self.currentColor == self.startColor:
                self.turnedAmount -= 1           
            if self.turnedAmount == 0:
                self.colorSensorMotor.set(0)
                self.turnWheel = False

        self.lastColor = self.currentColor

    def searchColorInit(self):
        self.currentColor = None
        self.lastColor = None
        self.goal = self.stopColorMap[self.gameData]
        self.searchForColor = True
        self.found = False

    def searchColorCycle(self):
        if self.colorMap[self.goal] != self.colorMatch.matchClosestColor(self.colorSensor.getWPIColor(), 1.0):
            self.colorSensorMotor.set(0.25)
        else:
            if self.found == False:
                self.found = True
            else:    
                self.colorSensorMotor.set(0)
                self.searchForColor = False

    def teleopPeriodic(self):

        #Drive Train
        forward = self.driver.getY(RIGHT_HAND) #Right stick y-axis
        forward = deadzone(forward, robotmap.deadzone)
        
        rotation_value = self.driver.getX(LEFT_HAND)
	     
        self.drivetrain.arcadeDrive(forward, rotation_value)
        
    
        
        #Color Sensor Stuff
        self.checkGameData()

        if self.operator.getAButtonPressed():
            self.searchColorInit()

        if self.searchForColor:
            self.searchColorCycle()

        if self.operator.getXButtonPressed():
            self.turnWheelInit()

        if self.turnWheel:
            self.turnWheelCycle()
           
        
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