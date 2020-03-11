import wpilib
import rev
import robotmap as rm
class shooter:
    """
    Creates a shooter object, which uses a shooter motor and a loader
    motor to launch balls. The class also contains a setPIDCoefficients() function
    to calibrate the PID controller for aiming based on the robot map.
    """
    def __init__(self, port1, port2):
        self.driver = wpilib.XboxController(0)
        if rm.LOADER is not None:
            self.motor1 = rev.CANSparkMax(port1, rev.MotorType.kBrushed)
        if rm.SHOOTER is not None:
            self.motor2 = rev.CANSparkMax(port2, rev.MotorType.kBrushed)
        if rm.SHOOTER is not None:
            self.pidController2 = self.motor2.getPIDController()
        
        self.setPIDCoefficients()

    def setPIDCoefficients(self):
        """
        Sets the PID controller values to the values specified in the robotmap.
        """
        if rm.SHOOTER is not None:
            self.pidController2.setP(rm.PID_kP) 
            self.pidController2.setI(rm.PID_kI) 
            self.pidController2.setD(rm.PID_kD)
            #self.pidController2.setIz(rm.PID_kIz)
            self.pidController2.setFF(rm.PID_kFF)
            self.pidController2.setOutputRange(rm.PID_kMinOutput, rm.PID_kMaxOutput)

    def setShooterSpeed(self, loader_speed, shooter_RPM):
        """
        Sets the speed of the loader and shooter motors based on
        the speed/RPM specified in the robotmap.
        """
        if (shooter_RPM > rm.PID_kMaxRPM):
            shooter_RPM = rm.PID_kMaxRPM
        elif (shooter_RPM < 0):
            shooter_RPM = 0
        if (loader_speed > 1):
            loader_speed = 1
        elif (loader_speed < 0):
            loader_speed = 0
    
        if rm.LOADER is not None:
            self.motor1.set(-loader_speed)
        if rm.SHOOTER is not None:
            self.pidController2.setReference(shooter_RPM, rev.ControlType.kVelocity)

      #SCALE = 120 / 0.02
      #RPM = forward * SCALE
      #0.02 is 120 rpm (about)