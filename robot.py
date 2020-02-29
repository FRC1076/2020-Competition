import wpilib
from wpilib.interfaces import GenericHID

import rev
from rev.color import ColorMatch

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
        self.colorPiston = pneumatic_system(wpilib.DoubleSolenoid(0, robotmap.COLOR_SENSOR_EXTEND,robotmap.COLOR_SENSOR_RETRACT))
        self.climberPiston = pneumatic_system(wpilib.DoubleSolenoid(0, robotmap.COLOR_SENSOR_EXTEND,robotmap.COLOR_SENSOR_RETRACT))
        
        self.climberWinchMotor = rev.CANSparkMax(robotmap.CLIMBER_WINCH_MOTOR, rev.MotorType.kBrushed)
        
        # Color Sensor
        self.colorSensor = color_sensor()
        self.colorSensorMotor = rev.CANSparkMax(robotmap.COLOR_SENSOR_MOTOR, rev.MotorType.kBrushed)
       
        self.stopColorMap = {"R":"B", "Y":"G", "B":"R", "G":"Y"}
        
        self.gameData = ""
        
        self.setupColorSensor()

        self.hasTurnedWheel = False

        #Shooter
    
        self.shooter = shooter(robotmap.SHOOTER)


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


    def autonomousPeriodic(self):
        #Go forward 10ft
        #Shoot?
        pass


    def teleopInit(self):
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

        #TODO: Add encoders, other sensors


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
        if self.operator.getAButtonPressed():
            if not self.colorArmIsExtended:
                self.colorPiston.extend()
                self.colorArmIsExtended = True
            else:
                self.colorPiston.retract()
                self.colorArmIsExtended = False


    def climberPistonUpdate(self):  
        if self.operator.getBumperPressed(LEFT_HAND) and self.driver.getBumperPressed(LEFT_HAND):
            if not self.colorArmIsExtended:
                self.climberPiston.extend()
                self.climberArmIsExtended = True

        elif self.operator.getTriggerAxis(LEFT_HAND) > 0.8 and self.driver.getTriggerAxis(LEFT_HAND) > 0.8:
            if self.colorArmIsExtended:
                self.climberPiston.retract()
                self.climberArmIsExtended = False

    def climbWinchUpdate(self):
        if self.operator.getBumperPressed(RIGHT_HAND) > 0.8 and self.driver.getBumperPressed(RIGHT_HAND) > 0.8 and self.climberArmIsExtended:
                self.climberWinchMotor.set(0.3)

        elif self.operator.getTriggerPressed(RIGHT_HAND) > 0.8 and self.driver.getTriggerPressed(RIGHT_HAND) > 0.8 and self.climberArmIsExtended:
            self.climberWinchMotor.set(-0.3)
        else:
            self.climberWinchMotor.set(0)


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

            
            
                
    def teleopPeriodic(self):
        forward = self.driver.getY(RIGHT_HAND) #Right stick y-axis
        forward = 0.75 * deadzone(forward, robotmap.deadzone)
        
        rotation_value = -0.7 * self.driver.getX(LEFT_HAND)
	     
        self.drivetrain.arcadeDrive(forward, rotation_value)

        self.checkGameData()

        if self.operator.getStartButtonPressed():
            if not self.hasTurnedWHeel():
                self.turnWheelInit()
            else:
                self.searchColorInit()
            
        if self.operator.getBackButton:
            self.colorSensorMotor.set(0.1)
        else:
            self.colorSensorMotor.set(0)

        if self.searchForColor:
            self.searchColorCycle()

        if self.turnWheel:
            self.turnWheelCycle()

        self.colorPistonUpdate()
        self.climberPistonUpdate()
        self.climbWinchUpdate()

        forward = self.stick.getRawAxis(5)
        if self.stick.getXButton():
            forward = -1
        if self.stick.getAButton() and self.stick.getStickButton(LEFT_HAND):
            forward = -0.5   
        self.shooter.setShooterSpeed(forward)


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