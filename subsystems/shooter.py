import wpilib
import rev

class shooter:
    def __init__(self, port):
        print("Shooter init")
        self.stick = wpilib.XboxController(0)
        self.motor = rev.CANSparkMax(port, rev.MotorType.kBrushed)
        
    def setShooterSpeed(self):
      
      forward = self.stick.getRawAxis(5)
      if self.stick.getAButton():
         forward = -1
      if self.stick.getBButton():
         forward = -0.75
      if self.stick.getXButton():
         forward = -0.5
      if self.stick.getYButton():
         forward = -0.02
      self.motor.set(forward)

      SCALE = 120 / 0.02
      RPM = forward * SCALE
      print("Set shooter speed ", forward, "RPM = ", RPM) 

      #0.02 is 120 rpm (about)