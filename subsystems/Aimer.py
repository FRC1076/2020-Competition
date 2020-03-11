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
    """
    Creates an object which uses a gyroscope (in our case, a NavX) and a
    PID controller to turn the robot to a specified angle. Also contains
    several other functions to use with the PID controller.
    """
    def __init__(self,gyro):
        self.gyro = gyro
        turnController = wpilib.controller.PIDController(
            kP, kI, kD
        )
        turnController.setTolerance(kToleranceDegrees)
        turnController.enableContinuousInput(-180.0, 180.0)
        self.turncontroller = turnController
        self.rotateToAngleRate = 0

    def reset(self):
        """
        Resets the gyrocope to the default angle.
        """
        self.gyro.reset()

    def setaim(self, setpoint):
        """
        Sets the target angle for the robot to turn to based
        on the setpoint given to the function.
        """
        self.setpoint = setpoint
        self.turncontroller.setSetpoint(self.gyro.getAngle() + self.setpoint)

    def getAngle(self):
        """
        Returns the angle that the gyro is currently getting,
        scaled from 0 to 360.
        """
        self.ag = abs(self.gyro.getAngle()) % 360
        return self.ag
    
    def getsetpoint(self):
        """
        Returns the current setpoint that was provided in setaim().
        """
        return self.setpoint

    def calculate(self, m):
        """
        Returns the PID controller's next value, based on the supplied value 'm'.
        """
        return self.turncontroller.calculate(m)

    def pidWrite(self, output):
        """
        This function is invoked periodically by the PID Controller,
        based upon navX MXP yaw angle input and PID Coefficients.
        """
        self.rotateToAngleRate = output
        