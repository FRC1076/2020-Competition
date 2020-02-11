import wpilib
from rev.color import ColorSensorV3
import rev


class color_sensor:
    def __init__(self):
        self.colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)
        self.color = self.colorSensor.getRawColor()
        self.gameData = ""

    def getColorName(self, color):
        """
        TODO: improve color accuracy

        """

        r = color.red
        if(r < 30):
            return "g"
        elif(r < 80):
            return "b"
        elif(r < 200):
            return "r"
        else:
            return "y"

    def checkGameData(self):
        gd = str(wpilib.DriverStation.getInstance().getGameSpecificMessage())
        if(len(gd) > 0):
            self.gameData = gd

    def getGameData(self):
        return self.gameData

    def getColor(self):
        return self.color

    def checkColor(self):
        self.color = self.colorSensor.getRawColor()

    def checkColor(self):
        return (self.getColorName(self.color) != self.gameData)

    
