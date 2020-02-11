import rev

class rev_brushed(rev.CANSparkMax):
    def __init__(self,port):
        self.motor = rev.CANSparkMax(port, rev.MotorType.kBrushed)

    def set(self,speed):
        super().set(speed)
