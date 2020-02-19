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
        #self.driver = wpilib.XboxController(0)
        self.operator = wpilib.XboxController(0)


        
        #Motors
        
        #self.left_side = wpilib.SpeedControllerGroup(robotmap.LEFT_LEADER_ID, robotmap.LEFT_FOLLOWER_ID)
        #self.right_side = wpilib.SpeedControllerGroup(robotmap.RIGHT_LEADER_ID, robotmap.RIGHT_FOLLOWER_ID)
        
        #Drivetrain
        #self.drivetrain = wpilib.drive.DifferentialDrive(self.left_side, self.right_side)

        #TODO: Add subsystems and sensors as the code is written
        #TODO: SmartDashboard
        
        # Color Sensor
        self.colorSensor = color_sensor()
        self.colorSensorMotor = rev_brushed(robotmap.COLOR_SENSOR_MOTOR)
       
        self.stopColorMap = {"R":"B", "Y":"G", "B":"R", "G":"Y"}
        
        self.gameData = ""
        
        self.setupColorSensor()


    def setupColorSensor(self):
        self.colorMatch = ColorMatch()
        
        self.blue = wpilib._wpilib.Color(0.143, 0.427, 0.429)
        self.green = wpilib._wpilib.Color(0.197, 0.561, 0.240)
        self.red = wpilib._wpilib.Color(0.561, 0.232, 0.144)
        self.yellow = wpilib._wpilib.Color(0.361, 0.524, 0.133)

        #self.blue = wpilib._wpilib.Color.kAqua
        #self.green = wpilib._wpilib.Color.kLime
        #self.red = wpilib._wpilib.Color.kRed
        #self.yellow = wpilib._wpilib.Color.kYellow

        self.colorMap = {"B":self.blue, "G":self.green, "R":self.red, "Y":self.yellow}
        
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
        self.turnedAmount = 0

        self.searchForColor = False

        self.turnWheel = False
        self.startColor = None

        self.currentColor = None
        self.lastColor = None
        
        
        self.found = False
   
        #TODO: Add encoders, other sensors
        # print("Teleop begins!")
        pass

    def debugColorSensor(self, color=None):
        if color is not None:
            color = self.colorSensor.getColor()
        red = color.red
        blue = color.blue
        green = color.green
        # TODO: Use better debugging tools
        print("Red: {} Green: {} Blue: {} ".format(red, green, blue))
        #print(self.colorSensor.getColorName(color))

    def checkGameData(self):
        gd = wpilib.DriverStation.getInstance().getGameSpecificMessage()
        if(gd != None and not self.searchForColor):
            self.gameData = gd


    def turnWheelInit(self):
        self.turnedAmount = 8
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
        self.colorSensor.colorSensor.setGain(rev.color._rev_color.ColorSensorV3.GainFactor.k18x)
        
        self.currentColor = None
        self.lastColor = None
        self.goal = self.stopColorMap[self.gameData]
        self.goal = self.stopColorMap[self.goal]
        #self.goal = self.gameData
        self.searchForColor = True
        self.found = False
        self.timer = 0
        self.timer2 = 2
        

    def searchColorCycle(self):

        if self.timer < 100:
            self.timer += 1
            self.colorSensorMotor.set(0.2)
            
        elif self.timer == 100:
            self.currentColor = self.colorMatch.matchClosestColor(self.colorSensor.getWPIColor(), 1)
           

            self.timer +=1
        else:

            self.lastColor = self.currentColor

            color = self.colorMatch.matchClosestColor(self.colorSensor.getWPIColor(), 0.95)
            
            self.currentColor = color


            if self.lastColor == self.yellow and self.currentColor == self.green:
                self.currentColor == self.yellow

            if self.colorMap[self.goal] != color:
                self.colorSensorMotor.set(0.2)
            else:
                
                if self.timer2 == 0:
                    print("STOP!!!!")    
                    self.colorSensorMotor.set(0)
                    self.searchForColor = False
                else:
                    self.timer2 -= 1

            
                
           
                

    def teleopPeriodic(self):

        #Drive Train
        #forward = self.driver.getY(RIGHT_HAND) #Right stick y-axis
        #forward = deadzone(forward, robotmap.deadzone)
        
        #rotation_value = self.driver.getX(LEFT_HAND)
	     
        #self.drivetrain.arcadeDrive(forward, rotation_value)
        
        #Spin 1(3/4, ect) before seaerching for color
        
        #Color Sensor Stuff
        self.checkGameData()

        #print(self.colorMatch.matchClosestColor(self.colorSensor.getWPIColor(), 0.95))

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