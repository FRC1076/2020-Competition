import wpilib
import robotmap

class Climber:

    def __init__(self):
        self.piston = pneumatic_system(wpilib.DoubleSolenoid(0, robotmap.CLIMBER_EXTEND, robotmap.CLIMBER_RETRACT))
        self.winchMotor1 = rev.CANSparkMax(robotmap.CLIMBER_WINCH_MOTOR1, rev.MotorType.kBrushed)
        self.winchMotor2 = rev.CANSparkMax(robotmap.CLIMBER_WINCH_MOTOR2, rev.MotorType.kBrushed)

        self.whinch = wpilib.SpeedControllerGroup(self.winchMotor1, self.winchMotor2)

        self.climberArmExtended = False


    def extendPiston(self):
        self.piston.extend()

    def retractPiston(self):
        self.pistion.retract()

    def setMotor(self, speed):
        self.whinch.set(speed)
        