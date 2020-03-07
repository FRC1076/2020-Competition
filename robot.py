import wpilib
from wpilib.interfaces import GenericHID

import rev
from rev.color import ColorMatch
from wpilib import SmartDashboard

#TODO: What else will we need for 2020?
#TODO: Create and import subsystems (shooter, climb, etc.)

#This year, all IDs are stored in the robotmap
import robotmap

#Subsystems
from subsystems.pneumatics_system import pneumatic_system
from subsystems.color_sensor import color_sensor
from subsystems.shooter import shooter
import rev
import wpilib.drive
from subsystems.Aimer import Aimer
from navx import AHRS
import threading
from networktables import NetworkTables

#Controller hands (sides)
LEFT_HAND = wpilib._wpilib.XboxController.Hand.kLeftHand
RIGHT_HAND = wpilib._wpilib.XboxController.Hand.kRightHand


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        #Controllers
        self.driver = wpilib.XboxController(0)
        self.operator = wpilib.XboxController(1)

        #Motors
        self.left_motor_1 = rev.CANSparkMax(robotmap.LEFT_LEADER_ID, rev.MotorType.kBrushed)
        self.left_motor_2 = rev.CANSparkMax(robotmap.LEFT_FOLLOWER_ID, rev.MotorType.kBrushed)
        self.right_motor_1 = rev.CANSparkMax(robotmap.RIGHT_LEADER_ID, rev.MotorType.kBrushed)
        self.right_motor_2 = rev.CANSparkMax(robotmap.RIGHT_FOLLOWER_ID, rev.MotorType.kBrushed)

        self.left_motor_1.setClosedLoopRampRate(1.0)
        self.left_motor_2.setClosedLoopRampRate(1.0)
        self.right_motor_1.setClosedLoopRampRate(1.0)
        self.right_motor_2.setClosedLoopRampRate(1.0)
        
        self.left_side = wpilib.SpeedControllerGroup(self.left_motor_1, self.left_motor_2)
        self.right_side = wpilib.SpeedControllerGroup(self.right_motor_1, self.right_motor_2)
        
        #Drivetrain
        self.drivetrain = wpilib.drive.DifferentialDrive(self.left_side, self.right_side)

        #TODO: Add subsystems and sensors as the code is written
        #TODO: SmartDashboard
        
        #Pneumatics
        self.colorPiston = pneumatic_system(wpilib.DoubleSolenoid(0, robotmap.COLOR_SENSOR_EXTEND, robotmap.COLOR_SENSOR_RETRACT))
        self.climberPiston = pneumatic_system(wpilib.DoubleSolenoid(0, robotmap.CLIMBER_EXTEND, robotmap.CLIMBER_RETRACT))
        self.gearshiftPiston = pneumatic_system(wpilib.DoubleSolenoid(0, robotmap.DRIVE_SHIFT_EXTEND, robotmap.DRIVE_SHIFT_RETRACT))
        
        self.climberWinchMotor1 = rev.CANSparkMax(robotmap.CLIMBER_WINCH_MOTOR1, rev.MotorType.kBrushed)
        self.climberWinchMotor2 = rev.CANSparkMax(robotmap.CLIMBER_WINCH_MOTOR2, rev.MotorType.kBrushed)

        # Color Sensor
        self.colorSensor = color_sensor()
        self.colorSensorMotor = rev.CANSparkMax(robotmap.COLOR_SENSOR_MOTOR, rev.MotorType.kBrushed)
       
        self.stopColorMap = {"R":"B", "Y":"G", "B":"R", "G":"Y"}
        
        self.gameData = ""
        
        self.setupColorSensor()

        
        

        #Shooter
    
        self.shooter = shooter(robotmap.LOADER, robotmap.SHOOTER)

        # Gyro
        self.ahrs = AHRS.create_spi()
        self.Aimer = Aimer(self.ahrs)
        
        #network tables
        NetworkTables.init()
        self.sd = NetworkTables.getTable('VISION')

        SmartDashboard.init()

        self.lookForTargetTurn = [90, -180, 90]
        self.lookForTargetIncrement = 0

        #self.shuffleboardAutonDelayGetter = NetworkTables.get


        
        


    def setupColorSensor(self):
        self.colorMatch = ColorMatch()
        
        self.blue = wpilib._wpilib.Color(0.143, 0.427, 0.429)
        self.green = wpilib._wpilib.Color(0.197, 0.561, 0.240)
        self.red = wpilib._wpilib.Color(0.561, 0.232, 0.144)
        self.yellow = wpilib._wpilib.Color(0.361, 0.524, 0.133)

        self.colorMap = {"B":self.blue, "G":self.green, "R":self.red, "Y":self.yellow}
        
        self.colorMatch.addColorMatch(self.blue)
        self.colorMatch.addColorMatch(self.green)
        self.colorMatch.addColorMatch(self.red)
        self.colorMatch.addColorMatch(self.yellow)


    def robotPeriodic(self):
        return
    

    def autonomousInit(self):
        self.gameData = ""
        self.autonTimer = wpilib.Timer()
        self.shooterTimer = wpilib.Timer()
        self.shooterTimer2 = wpilib.Timer()

        self.autonTimer.start()

        self.Aimer.reset()


        #self.Aimer.setaim(self.Aimer.getAngle())
        self.turned180 = False

        self.setTarget = False

        #
        #self.Aimer.setaim(self.Aimer.getAngle())

        self.autonDelay = SmartDashboard.getNumber("Auton Delay", 0)
        self.target_locked = False
        self.set_point_set = False
        self.motor_spun_up = False

    """
    def rotateToPoint(self):
        val = (self.Aimer.getAngle()-self.Aimer.getsetpoint())
        #print(val)
        if val > 6 or val < -6:
           self.drivetrain.arcadeDrive(0, 0.7)
        elrcadeDrive(0,0)
            return True

    """

    def lookUntilTargetFound(self):
        if self.sd.getNumber("CONTOURS_FOUND", 0) > 0:
            return True
        else:
            #if self.hasTurned90:
            #    self.Aimer.setaim(self.Aimer.getAngle() - 180)
            #else:
            #    self.Aimer.setaim(self.Aimer.getAngle() + 90)
            self.Aimer.setaim(self.Aimer.getAngle() + self.lookForTargetTurn[self.lookForTargetIncrement])


        amt = self.Aimer.calculate(self.Aimer.getAngle())
        self.drivetrain.arcadeDrive(0, amt)

        if abs(amt) < 0.1:
            if self.lookForTargetIncrement < 2:
                self.lookForTargetIncrement += 1
            else:
                self.lookForTargetIncrement = 0

        return False
        


    
    def visionShooterUpdate(self):
        angle = self.Aimer.getAngle()
        rotate_speed = self.Aimer.calculate(angle)
        self.drivetrain.arcadeDrive(0, rotate_speed)

        if self.Aimer.atSetpoint():
            self.target_locked = True
            self.shooterTimer.start()

    def autonomousPeriodic(self):
        

        if self.autonTimer.get() > self.autonDelay:
            if self.autonTimer.get() < 0.4 + self.autonDelay:
                self.drivetrain.arcadeDrive(-0.75, 0)
            elif not self.set_point_set:
                self.Aimer.setaim(self.sd.getNumber('ANGLE'))    #make default value 0
                self.set_point_set = True
            elif not self.target_locked:
                self.visionShooterUpdate()
            elif self.shooterTimer.get() < 1:
                self.shooter.setShooterSpeed(0, robotmap.shooter_RPM)
            elif self.shooterTimer < 8:
                self.shooter.setShooterSpeed(robotmap.LOADER_SPEED, robotmap.shooter_RPM)




    def teleopInit(self):
        NetworkTables.initialize()
        self.sd = NetworkTables.getTable('VISION')
       # self.sd = NetworkTables.getTable('VISION')
        self.gameData = ""
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

        self.autonDelay = SmartDashboard.getNumber("Auton Delay", 0)


    def debugColorSensor(self, color=None):
        if color is not None:
            color = self.colorSensor.getColor()
        red = color.red
        blue = color.blue
        green = color.green
        # TODO: Use better debugging tools
        print("Red: {} Green: {} Blue: {} ".format(red, green, blue))


    def checkGameData(self):
        gd = wpilib.DriverStation.getInstance().getGameSpecificMessage()
        if(gd != None and not self.searchForColor):
            self.gameData = gd


    def colorPistonUpdate(self):
        if self.operator.getPOV() == 180:
            self.colorPiston.extend()
            #self.colorArmIsExtended = True
        elif self.operator.getPOV() == 0:
            self.colorPiston.retract()
            #self.colorArmIsExtended = False


    def climberPistonUpdate(self):  
        if self.operator.getRawAxis(2) > 0.5 and self.driver.getBumperPressed(LEFT_HAND):
            if not self.climberArmIsExtended:
                print("extend")
                self.climberPiston.extend()
                self.climberArmIsExtended = True
        elif self.operator.getRawAxis(2) > 0.5 and self.driver.getTriggerAxis(LEFT_HAND) > 0.8:
            if self.climberArmIsExtended:
                self.climberPiston.retract()
                self.climberArmIsExtended = False

    def climbWinchUpdate(self):
        if self.operator.getRawAxis(2) > 0.5 and self.driver.getTriggerAxis(RIGHT_HAND) > 0.8 :

            self.climberWinchMotor1.set(0.75)
            self.climberWinchMotor2.set(0.75)

        elif self.operator.getRawAxis(2) > 0.5 and self.driver.getTriggerAxis(RIGHT_HAND) > 0.8:
            self.climberWinchMotor1.set(-0.3)
            self.climberWinchMotor2.set(-0.3)
        
        else:
            self.climberWinchMotor1.set(0)
            self.climberWinchMotor2.set(0)


    def turnWheelInit(self):
        self.turnedAmount = 8
        self.currentColor = None
        self.lastColor = None
        self.startColor = self.stopColorMap[self.colorSensor.getColorName(self.colorSensor.getColor())]
        self.lastColor = self.startColor
        self.turnWheel = True

    
    def turnWheelCycle(self):
        #self.debugColorSensor()
        self.colorSensorMotor.set(0.3)
        self.currentColor = self.colorSensor.getColorName(self.colorSensor.getColor())
        
        if self.currentColor != self.lastColor:            
            if self.currentColor == self.startColor:
                self.turnedAmount -= 1           
            if self.turnedAmount == 0:
                self.colorSensorMotor.set(0)
                self.turnWheel = False
                self.hasTurnedWheel = True

        self.lastColor = self.currentColor

    
    def searchColorInit(self):
        self.colorSensor.colorSensor.setGain(rev.color._rev_color.ColorSensorV3.GainFactor.k18x)
        self.currentColor = None
        self.lastColor = None
        self.goal = self.stopColorMap[self.gameData]
        self.goal = self.stopColorMap[self.goal]
        #self.goal = self.gameData
        self.searchForColor = True
        self.found = False
        self.timer = 0
        self.timer2 = 2
        

    def searchColorCycle(self):
        if self.timer < 100:
            self.timer += 1
            self.colorSensorMotor.set(0.2)
            
        elif self.timer == 100:
            self.currentColor = self.colorMatch.matchClosestColor(self.colorSensor.getWPIColor(), 1)
            self.timer +=1

        else:

            self.lastColor = self.currentColor

            color = self.colorMatch.matchClosestColor(self.colorSensor.getWPIColor(), 0.95)
            
            self.currentColor = color

            if self.lastColor == self.yellow and self.currentColor == self.green:
                self.currentColor == self.yellow

            if self.colorMap[self.goal] != color:
                self.colorSensorMotor.set(0.2)

            else:

                if self.timer2 == 0:
                    print("STOP!!!!")    
                    self.colorSensorMotor.set(0)
                    self.searchForColor = False
                else:
                    self.timer2 -= 1

    def shiftGears(self):
        if self.driver.getBumperPressed(RIGHT_HAND):
            if self.gearshiftPosition == "Low":
                self.gearshiftPiston.retract()
                self.gearshiftPosition = "High"
                #print("Shifted to high gear")
            else:
                self.gearshiftPiston.extend()
                self.gearshiftPosition = "Low"
                #print("Shifted to low gear")

    """
        
        If whammy is pressed, do the following steps:
        aim at target
        run convayer to bring in 1 ball
        calculate speed?
        shoot
        
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
    """

    def teleopPeriodic(self):
        print(SmartDashboard.getNumber("Auton Delay", 0))

        forward = self.driver.getY(RIGHT_HAND) 
        #Right stick y-axis
        forward = 0.90 * deadzone(forward, robotmap.deadzone)
        rotation_value = -0.8 * self.driver.getX(LEFT_HAND)
        
        #if rotation_value > 0 or forward > 0:
        self.drivetrain.arcadeDrive(forward, rotation_value)

        self.checkGameData()

        if self.operator.getStartButtonPressed():
            if not self.hasTurnedWheel:
                self.turnWheelInit()
            else:
                self.searchColorInit()
            
        if self.operator.getBackButton():
            self.colorSensorMotor.set(0.2)
        elif not self.searchForColor and not self.turnWheel:
            self.colorSensorMotor.set(0)

        if self.searchForColor:
            self.searchColorCycle()

        if self.turnWheel:
            self.turnWheelCycle()

        self.colorPistonUpdate()
        self.climberPistonUpdate()
        self.climbWinchUpdate()
        self.shiftGears()

        #if self.operator.getRawAxis(4) > 0.8:
        #    self.visionShooterUpdate()
        
        if self.operator.getYButton():
            self.Aimer.setaim(self.sd.getNumber("ANGLE", 0))
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



def deadzone(val, deadzone): 
    """
    Given the deadzone value x, the deadzone both eliminates all
    values between -x and x, and scales the remaining values from
    -1 to 1, to (-1 + x) to (1 - x)
    """
    if abs(val) < deadzone:
        return 0
    elif val < (0):
        x = ((abs(val) - deadzone)/(1-deadzone))
        return (-x)
    else:
        x = ((val - deadzone)/(1-deadzone))
        return (x)


if __name__ == "__main__":
	wpilib.run(Robot)