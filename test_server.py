from networktables import NetworkTables as nt
import time

DISTANCE_KEY = "DISTANCE"
ANGLE_KEY = "ANGLE"
CAMERA_CONNECTED_KEY = "CAMERA_CONNECTED"
RECEVING_IMAGES_KEY = "RECEIVING_IMAGES"
CONTOURS_FOUND_KEY = "CONTOURS_FOUND"
TARGET_IN_FRAME_KEY = "TARGET_FOUND"

NT_VISON_TABLE_NAME = "VISION"

nt.initialize()
print("Initialized. Table name is", NT_VISON_TABLE_NAME)
    
target_info = nt.getTable(NT_VISON_TABLE_NAME)
while True:
    distance = target_info.getNumber(DISTANCE_KEY, -111)
    angle = target_info.getNumber(ANGLE_KEY, -111)
    contours_found = target_info.getNumber(CONTOURS_FOUND_KEY, -111)
    print ('d =', distance, '; a = ', angle, '; c=', contours_found)
    time.sleep(1)
    
