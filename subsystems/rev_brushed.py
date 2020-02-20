import rev

class rev_brushed:
    def __init__(self,port):
        self.motor = rev.CANSparkMax(port, rev.MotorType.kBrushed)

    def set(self,speed):
        self.motor.set(speed)
