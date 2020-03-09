import wpilib
import wpilib.drive
#import robotmap
#from helper import GetSet
import rev

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
from subsystems.drivetrain import Drivetrain



import unittest


class TestDrivetrain(unittest.TestCase):
    def test_forward(self):
        left_motor = rev.CANSparkMax(99, rev.MotorType.kBrushed)
        right_motor = rev.CANSparkMax(100, rev.MotorType.kBrushed)
        drivetrain = Drivetrain(left_motor, right_motor, None)
        drivetrain.arcade_drive(0.5, 0)
        assert left_motor.get() > 0
        assert right_motor.get() < 0
        drivetrain.arcade_drive(-0.5, 0)
        assert left_motor.get() < 0
        assert right_motor.get() > 0


    def test_rotate(self):
        left_motor = rev.CANSparkMax(99, rev.MotorType.kBrushed)
        right_motor = rev.CANSparkMax(100, rev.MotorType.kBrushed)
        drivetrain = Drivetrain(left_motor, right_motor, None)
        drivetrain.arcade_drive(0, 0.42)
        assert left_motor.get() > 0
        assert right_motor.get() > 0
        drivetrain.arcade_drive(0, -0.42)
        assert left_motor.get() < 0
        assert right_motor.get() < 0


    

if __name__ == '__main__':
    print(os.path.dirname(os.path.abspath(__file__)))
    unittest.main()


