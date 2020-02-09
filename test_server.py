from networktables import NetworkTables as nt
import time

nt.initialize()
    
target_info = nt.getTable("targetInfo")
while True:
    distance = target_info.getNumber("distance", -1)
    angle = target_info.getNumber("angle", -1)
    print (distance, angle)
    time.sleep(1)
    
