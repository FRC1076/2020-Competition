import wpilib
import rev

class shooter:
    def __init__(self, port1, port2):
        print("Shooter init")
        self.stick = wpilib.XboxController(0)
        self.motor1 = rev.CANSparkMax(port1, rev.MotorType.kBrushed)
        self.motor2 = rev.CANSparkMax(port2, rev.MotorType.kBrushed)

    def setShooterSpeed(self, forward):
      
      self.motor1.set(forward)
      self.motor2.set(forward)

      SCALE = 120 / 0.02
      RPM = forward * SCALE
      #print("Set shooter speed ", forward, "RPM = ", RPM) 

      #0.02 is 120 rpm (about)
