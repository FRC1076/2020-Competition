import wpilib
from rev.color import ColorSensorV3
import rev


class color_sensor:
    def __init__(self):
        self.colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)
        self.color = self.colorSensor.getRawColor()
        

    def getColorName(self, color):
        """
        TODO: improve color accuracy

        """

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

        
        """
        if(r < 30):
            return "g"
        elif(r < 80):
            return "b"
        else:
            if(g < 100):
                return "r"
            else:
                return "y"
        """
        
        

    

    def getWPIColor(self):
        return self.colorSensor.getColor()

    def getColor(self):
        self.color = self.colorSensor.getRawColor()
        return self.color
        

    #def checkColor(self, goal):
    #    return (self.getColorName(self.getColor()) != goal)

    
