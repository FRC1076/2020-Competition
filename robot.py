
# General PYFRC Imports
import wpilib
import wpilib.drive
from wpilib.interfaces import GenericHID
import rev
from rev.color import ColorMatch
from navx import AHRS
from networktables import NetworkTables
import threading

# All ports are stored in robot map
import robotmap

# Subsystems
from subsystems.pneumatics_system import pneumatic_system
from subsystems.color_sensor import color_sensor
from subsystems.shooter import shooter
from subsystems.Aimer import Aimer
from subsystems.drivetrain import Drivetrain
from subsystems.climber import Climber

#Controller hands (sides)
LEFT_HAND = wpilib._wpilib.XboxController.Hand.kLeftHand
RIGHT_HAND = wpilib._wpilib.XboxController.Hand.kRightHand


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        # Controllers 
        self.driver = wpilib.XboxController(0)
        self.operator = wpilib.XboxController(1)

        # Motors
        self.left_motor_1 = rev.CANSparkMax(robotmap.LEFT_LEADER_ID, rev.MotorType.kBrushed)
        self.left_motor_2 = rev.CANSparkMax(robotmap.LEFT_FOLLOWER_ID, rev.MotorType.kBrushed)
        self.right_motor_1 = rev.CANSparkMax(robotmap.RIGHT_LEADER_ID, rev.MotorType.kBrushed)
        self.right_motor_2 = rev.CANSparkMax(robotmap.RIGHT_FOLLOWER_ID, rev.MotorType.kBrushed)

        self.left_motor_1.setClosedLoopRampRate(1.0)
        self.left_motor_2.setClosedLoopRampRate(1.0)
        self.right_motor_1.setClosedLoopRampRate(1.0)
        self.right_motor_2.setClosedLoopRampRate(1.0)
        
        # Group motors
        self.left_side = wpilib.SpeedControllerGroup(self.left_motor_1, self.left_motor_2)
        self.right_side = wpilib.SpeedControllerGroup(self.right_motor_1, self.right_motor_2)
        
        #Pneumatics
        self.colorPiston = pneumatic_system(wpilib.DoubleSolenoid(0, robotmap.COLOR_SENSOR_EXTEND, robotmap.COLOR_SENSOR_RETRACT))
       
        self.gearshiftPiston = pneumatic_system(wpilib.DoubleSolenoid(0, robotmap.DRIVE_SHIFT_EXTEND, robotmap.DRIVE_SHIFT_RETRACT))
    
        #Climber
        self.climber = Climber()

        #Drivetrain
        self.drivetrain = Drivetrain(self.left_side, self.right_side, self.gearshiftPiston)

        # Color Sensor
        self.colorSensor = color_sensor()

        #Shooter
        self.shooter = shooter(robotmap.LOADER, robotmap.SHOOTER)

        # Gyro
        self.ahrs = AHRS.create_spi()
        self.Aimer = Aimer(self.ahrs)
        
        #network tables
        self.sd = NetworkTables.getTable('VISION')
        
        
    def robotPeriodic(self):
        return
    

    def autonomousInit(self):
        self.gameData = ""
        self.autonTimer = wpilib.Timer()
        self.shooterTimer = wpilib.Timer()

        self.autonTimer.start()

        self.Aimer.reset()

        self.turned180 = False
        self.setTarget = False

        #Reset aimer
        self.Aimer.setaim(self.Aimer.getAngle())

    def autonomousPeriodic(self):
        
        lspeed = 0

        if self.autonTimer.get() < 0.5:
            self.drivetrain.arcadeDrive(-0.75, 0)
        else:
            amt = self.Aimer.calculate(self.Aimer.getAngle())
            print("Turn speed: {} Angle Difference: {}".format(amt, self.sd.getNumber("ANGLE", 0)))
            self.drivetrain.arcadeDrive(0, amt)

            if(abs(amt) < 1):
                if not self.turned180:
                    self.turned180 = True
                    self.Aimer.setaim(self.Aimer.getAngle() + self.sd.getNumber("ANGLE", 0))
                else:
                    #self.Aimer.setAim(self.)
                    self.shooterTimer.start()
                

        if self.shooterTimer.get() > 2:
            lspeed = robotmap.LOADER_SPEED
        
        
        self.shooter.setShooterSpeed(lspeed, robotmap.SHOOTER_RPM)


    def teleopInit(self):
        NetworkTables.initialize()
        self.sd = NetworkTables.getTable('VISION')
        
        self.goal = ""
        self.turnedAmount = 0

        self.searchForColor = False

        self.turnWheel = False
        self.startColor = None

        self.currentColor = None
        self.lastColor = None
        
        self.found = False

        #Pneumatics piston state recorder
        self.colorArmIsExtended = False
        self.climberArmIsExtended = False
        
        self.gearshiftPosition = "Low"
        self.gearshiftPiston.extend()

        #TODO: Add encoders, other sensors
        self.hasTurnedWheel = False


    


    def colorPistonUpdate(self):
        
        

    def visionShooterUpdate(self):
        """
        If whammy is pressed, do the following steps:
        aim at target
        run convayer to bring in 1 ball
        calculate speed?
        shoot
        """
        loaderSpeed = 0
        shooterRPM  = 0

        self.Aimer.reset()
        
        self.Aimer.setaim(self.sd.getNumber("ANGLE", 0))
        
        turnAmount = self.Aimer.calculate(self.Aimer.getAngle())
        print("The driver is turning: {}, to the angle of {}".format(turnAmount, self.sd.getNumber("ANGLE", 0 )))
        self.drivetrain.arcadeDrive(0, turnAmount)


        if abs(turnAmount) < 0.2:
            loaderSpeed = robotmap.LOADER_SPEED
            shooterRPM = robotmap.SHOOTER_RPM
            
        self.shooter.setShooterSpeed(loaderSpeed, shooterRPM)
        

    def isOperatorEndGame(self):
        return self.operator.getRawAxis(2) > 0.5

    def teleopPeriodic(self):

        forward = 0.8 * self.drivetrain.deadzone(self.driver.getY(RIGHT_HAND))
        rotation_value = -0.8 * self.driver.getX(LEFT_HAND)
        
        self.drivetrain.arcadeDrive(forward, rotation_value)

        self.colorSensor.checkGameData()

        if self.operator.getStartButtonPressed():
            self.colorSensor.colorWheelCycle()
            
        if self.operator.getBackButton():
            self.colorSensor.manual_turn(robotmap.COLOR_WHEEL_TURN_SPEED)
        else:
            self.colorSensor.stop()

        if self.driver.getBumperPressed(RIGHT_HAND):
            self.drivetrain.shift()


        if self.isOperatorEndGame():
            if self.driver.getBumperPressed(LEFT_HAND):
                self.climber.extendPiston()
            elif self.driver.getTriggerAxis(LEFT_HAND) > 0.8:
                self.climber.retractPiston()

            if self.driver.getTriggerAxis(RIGHT_HAND) > 0.8:
                self.climber.setMotor(robotmap.CLIMBER_MOTOR_UP_SPEED)
            else:
                self.climber.setMotor(0)


        if self.operator.getPOV() == 180:
            self.colorPiston.extend()
        elif self.operator.getPOV() == 0:
            self.colorPiston.retract()

        if self.operator.getRawAxis(4) > 0.8:
            self.visionShooterUpdate()
        
        
        loaderSpeed = 0
        shooterRPM = 0

        if self.operator.getAButton():
            shooterRPM = robotmap.SHOOTER_RPM 
        else:
            shooterRPM = 0
        
        if self.operator.getAButton() and self.operator.getBButton():
            loaderSpeed = robotmap.LOADER_SPEED 
        else:
            loaderSpeed = 0

        
        self.shooter.setShooterSpeed(loaderSpeed, shooterRPM)


if __name__ == "__main__":
	wpilib.run(Robot)