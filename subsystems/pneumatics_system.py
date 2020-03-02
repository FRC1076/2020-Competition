#PNEUMATICS SYSTEM FOR FIRST ROBOTICS 2020 COMPETITION
#The area below the main code contains the solenoids used for our 'bot
import wpilib


# RoboFoot 2: Now colorArm! ( code copied and edited from WAPUR 2020 )
class pneumatic_system:
    stateExtend = wpilib.DoubleSolenoid.Value.kForward
    stateRetract = wpilib.DoubleSolenoid.Value.kReverse
    def __init__(self, piston):
        self.piston = piston

    def retract(self):
        self.piston.set(pneumatic_system.stateRetract)
    
    def extend(self):
        self.piston.set(pneumatic_system.stateExtend)

    def get(self):
        self.piston.get()


        ''' SOLENOID LIST
            COLOR SENSOR WHEEL: 4, 5




        Define Code: self.piston = pneuamtic_system(wpilib.DoubleSolenoid(PNCANID, RFForward, RFReverse))
        '''