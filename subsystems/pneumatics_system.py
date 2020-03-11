#PNEUMATICS SYSTEM FOR FIRST ROBOTICS 2020 COMPETITION
#The area below the main code contains the solenoids used for our 'bot
import wpilib

# RoboFoot 2: Now colorArm! ( code copied and edited from WAPUR 2020 )
class pneumatic_system:
    """
    A basic class used to create and activate double solenoids, specifically pistons.
    """
    stateExtend = wpilib.DoubleSolenoid.Value.kForward
    stateRetract = wpilib.DoubleSolenoid.Value.kReverse
    def __init__(self, piston):
        self.piston = piston

    def retract(self):
        """
        Retracts the solenoid.
        """
        self.piston.set(pneumatic_system.stateRetract)
    
    def extend(self):
        """
        Extends the solenoid.
        """
        self.piston.set(pneumatic_system.stateExtend)

    def get(self):
        """
        Returns the current value of the solenoid.
        This can be either kForward (extended) or kReverse (retracted).
        """
        self.piston.get()