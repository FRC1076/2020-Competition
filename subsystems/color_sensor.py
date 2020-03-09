import wpilib
from rev.color import ColorSensorV3
import rev
import robotmap

class color_sensor:
    def __init__(self):
        self.colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)
        self.color = self.colorSensor.getRawColor()

        self.colorSensorMotor = rev.CANSparkMax(robotmap.COLOR_SENSOR_MOTOR, rev.MotorType.kBrushed)

        self.stopColorMap = {"R":"B", "Y":"G", "B":"R", "G":"Y"}
        self.gameData = ""
        self.setupColors()

        self.hasTurnedWheel = False
        self.turnedInit = False
        self.colorFindInit = False



    def colorWheelCycle():
        if not self.hasTurnedWheel:
            self.turnWheelInit()
        else:
            self.searchColorInit()
            
        

    def setupColors(self):
        self.colorMatch = ColorMatch()
        
        self.blue = wpilib._wpilib.Color(0.143, 0.427, 0.429)
        self.green = wpilib._wpilib.Color(0.197, 0.561, 0.240)
        self.red = wpilib._wpilib.Color(0.561, 0.232, 0.144)
        self.yellow = wpilib._wpilib.Color(0.361, 0.524, 0.133)

        self.colorMap = {"B":self.blue, "G":self.green, "R":self.red, "Y":self.yellow}
        
        self.colorMatch.addColorMatch(self.blue)
        self.colorMatch.addColorMatch(self.green)
        self.colorMatch.addColorMatch(self.red)
        self.colorMatch.addColorMatch(self.yellow)


    def debug(self, color=None):
        if color is not None:
            color = self.colorSensor.getColor()
        red = color.red
        blue = color.blue
        green = color.green
        print("Red: {} Green: {} Blue: {} ".format(red, green, blue))


    def checkGameData(self):
        gd = wpilib.DriverStation.getInstance().getGameSpecificMessage()
        if(gd != None and not self.searchForColor):
            self.gameData = gd


    def getColorName(self, color):
        r = color.red
        g = color.green
        b = color.blue

        if(r > g and r > b):
            return "R"
        elif(g > r and r > b):
            return "Y"
        elif(g > b and g > r):
            return "G"
        elif(b > r and g > r):
            return "B"
        else:
            return "w"

    def turnWheelInit(self):
        if not self.turnedInit:
            self.turnedAmount = 8
            self.currentColor = None
            self.lastColor = None
            self.startColor = self.stopColorMap[self.colorSensor.getColorName(self.colorSensor.getColor())]
            self.lastColor = self.startColor
            self.turnWheel = True
            self.turnedInit = True
        else:
            self.turnWheelCycle()

    
    def turnWheelCycle(self):
        self.colorSensorMotor.set(0.3)
        self.currentColor = self.colorSensor.getColorName(self.colorSensor.getColor())
        
        if self.currentColor != self.lastColor:            
            if self.currentColor == self.startColor:
                self.turnedAmount -= 1           
            if self.turnedAmount == 0:
                self.colorSensorMotor.set(0)
                self.turnWheel = False
                self.hasTurnedWheel = True

        self.lastColor = self.currentColor

    
    def searchColorInit(self):
        if not self.colorFindInit:
            self.colorSensor.colorSensor.setGain(rev.color._rev_color.ColorSensorV3.GainFactor.k18x)
            self.currentColor = None
            self.lastColor = None
            self.goal = self.stopColorMap[self.gameData]
            self.goal = self.stopColorMap[self.goal]
            self.searchForColor = True
            self.found = False
            self.timer = 0
            self.timer2 = 2
            self.colorFindInit = True
        else:
            self.searchColorCycle()
        
    
    def manual_turn(self, speed):
        self.colorSensorMotor.set(speed)


    def stop_turn(self):
        if not self.searchForColor and not self.turnWheel:
            self.colorSensorMotor.set(0)
            return True
        else:
            return False


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
                    self.colorSensorMotor.set(0)
                    self.searchForColor = False
                else:
                    self.timer2 -= 1

    def getWPIColor(self):
        return self.colorSensor.getColor()

    def getColor(self):
        self.color = self.colorSensor.getRawColor()
        return self.color


    

