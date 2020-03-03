from networktables import NetworkTables as nt
import time

DISTANCE_KEY = "DISTANCE"
ANGLE_KEY = "ANGLE"
CAMERA_CONNECTED_KEY = "CAMERA_CONNECTED"
RECEVING_IMAGES_KEY = "RECEIVING_IMAGES"
CONTOURS_FOUND_KEY = "CONTOURS_FOUND"
TARGET_IN_FRAME_KEY = "TARGET_FOUND"
FIRE_KEY = "FIRE"
FIRE_AS_NUMBER_KEY = "FIRE_AS_NUMBER"

NT_ADDRESS = "10.10.76.2"
NT_ADDRESS = "127.0.0.1"
NT_VISON_TABLE_NAME = "VISION"
NT_HANDLE = None

SD_TABLE_NAME = "SmartDashboard"

SD_HANDLE = None

def init_network_tables():
    global NT_HANDLE, SD_HANDLE
    nt.initialize(server = NT_ADDRESS)
    print("nt is initialized. server is", NT_ADDRESS)    
    NT_HANDLE = nt.getTable(NT_VISON_TABLE_NAME)
    SD_HANDLE = nt.getTable(SD_TABLE_NAME)

def update_network_tables(key, value):
    global NT_HANDLE, SD_HANDLE

    print("updating", key, value, type(value))

    if NT_HANDLE is not None:
        NT_HANDLE.putNumber(key, value)

        print("wrote to nt:", key, value)
    else: 
        print("no network table handle")

# def update_smart_dashboard(key, value):


init_network_tables()
i = 0
fire = True
while True:
    update_network_tables(ANGLE_KEY, i * .01)
    update_network_tables(DISTANCE_KEY, i)
    update_network_tables(FIRE_AS_NUMBER_KEY, fire)
    NT_HANDLE.putBoolean(FIRE_KEY, fire)

    print('putting', i, fire)
    i += 1
    fire = not fire
    time.sleep(1)