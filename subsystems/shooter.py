import wpilib
import rev
import robotmap as rm
class shooter:
    def __init__(self, port1, port2):
        print("Shooter init")
        self.driver = wpilib.XboxController(0)
        if rm.LOADER is not None:
            self.motor1 = rev.CANSparkMax(port1, rev.MotorType.kBrushed)
        if rm.SHOOTER is not None:
            self.motor2 = rev.CANSparkMax(port2, rev.MotorType.kBrushed)
        
        if rm.LOADER is not None:
            self.pidController1 = self.motor1.getPIDController()
        if rm.SHOOTER is not None:
            self.pidController2 = self.motor2.getPIDController()
        self.setPIDCoefficients()

    def setPIDCoefficients(self):
        if rm.LOADER is not None:
            self.pidController1.setP(rm.PID_kP)
            self.pidController1.setI(rm.PID_kI)
            self.pidController1.setD(rm.PID_kD)
            #self.pidController1.setIz(rm.PID_kIz)
            self.pidController1.setFF(rm.PID_kFF)
            self.pidController1.setOutputRange(rm.PID_kMinOutput, rm.PID_kMaxOutput)

        if rm.SHOOTER is not None:
            self.pidController2.setP(rm.PID_kP)
            self.pidController2.setI(rm.PID_kI)
            self.pidController2.setD(rm.PID_kD)
            #self.pidController2.setIz(rm.PID_kIz)
            self.pidController2.setFF(rm.PID_kFF)
            self.pidController2.setOutputRange(rm.PID_kMinOutput, rm.PID_kMaxOutput)

    def setShooterSpeed(self, loader_RPM, shooter_RPM):
      
      #self.motor1.set(forward)
      #self.motor2.set(forward)

        print("RPM Before = ", loader_RPM, shooter_RPM)

        if (shooter_RPM > rm.PID_kMaxRPM):
            shooter_RPM = rm.PID_kMaxRPM
        elif (shooter_RPM < 0):
            shooter_RPM = 0
        if (loader_RPM > rm.PID_kMaxRPM):
            loader_RPM = rm.PID_kMaxRPM
        elif (loader_RPM < 0):
            loader_RPM = 0

  
        print("RPM After = ", loader_RPM, shooter_RPM)

        
    
        if rm.LOADER is not None:
            self.pidController1.setReference(loader_RPM, rev.ControlType.kVelocity)
        if rm.SHOOTER is not None:
            self.pidController2.setReference(shooter_RPM, rev.ControlType.kVelocity)

      #SCALE = 120 / 0.02
      #RPM = forward * SCALE
      #print("Set shooter speed ", forward, "RPM = ", RPM) 

      #0.02 is 120 rpm (about)
