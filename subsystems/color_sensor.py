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
            return "r"
        elif(g > r and g > b):
            return "y"
        elif(g > b and g > r):
            return "g"
        elif(b > r and g > r):
            return "b"
        else:
            raise NotImplementedError

        
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

    
