from navx import AHRS
import wpilib
import wpilib.controller
import math

kP = 0.05
kI = 0.02
kD = 0.00
kF = 0.00
kToleranceDegrees = 2.0
class Aimer:
    def __init__(self,gyro):
        self.gyro=gyro
        

        
        
        turnController = wpilib.controller.PIDController(
            kP, kI, kD
        )
        turnController.setTolerance(kToleranceDegrees)
        turnController.enableContinuousInput(-180.0, 180.0)
        self.turncontroller =turnController
        self.rotateToAngleRate = 0

    def reset(self):
        self.gyro.reset()

    def setaim(self,setpoint):
        self.setpoint=setpoint
        self.turncontroller.setSetpoint(self.gyro.getAngle()+self.setpoint)

    def getAngle(self):
        self.ag=abs(self.gyro.getAngle())%360
        
        return self.ag
    
    def getsetpoint(self):
        return self.setpoint

    def calculate(self, m):
        return self.turncontroller.calculate(m)

    def pidWrite(self, output):
        """This function is invoked periodically by the PID Controller,
        based upon navX MXP yaw angle input and PID Coefficients.
        """
        self.rotateToAngleRate = output
        