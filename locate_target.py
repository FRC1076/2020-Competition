import cv2 #USE OPENCV 3.1 FOR FINDCONTOURS TO WORK
import numpy as np
import math
from networktables import NetworkTables as nt
import datetime
import os

__DEBUG__ = False
__DEBUG_REMOTE_PI__ = True

remote_pi_image_location = "/home/pi/test_images/frame1.jpg"
fisheye_pi_image_location = "/home/pi/dev/cvon3/2020-Competition/test_images/frame1.jpg"
image_location = remote_pi_image_location

DISTANCE_KEY = "DISTANCE"
ANGLE_KEY = "ANGLE"
CAMERA_CONNECTED_KEY = "CAMERA_CONNECTED"
RECEVING_IMAGES_KEY = "RECEIVING_IMAGES"
CONTOURS_FOUND_KEY = "CONTOURS_FOUND"
TARGET_IN_FRAME_KEY = "TARGET_FOUND"

NT_ADDRESS = "10.10.76.2"
NT_VISON_TABLE_NAME = "VISION"
NT_HANDLE = None


#use red camera fov if using the ps eye

def process_image(hsv_img, kernelSize, lower_color_range, upper_color_range):
    # Kernal to use for removing noise
    kernel = np.ones(kernelSize, np.uint8)

    # Convert image to binary
    mask = cv2.inRange(hsv_img, lower_color_range, upper_color_range)
    
    #remove noisy parts of the image
    close_gaps = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    no_noise = cv2.morphologyEx(close_gaps, cv2.MORPH_OPEN, kernel)

    return no_noise


def find_object(img):
    # Find boundary of object
    _, contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    update_network_tables(CONTOURS_FOUND_KEY, len(contours))

    #runs if no contours are found
    if len(contours) == 0:
        return None
    
    #finds largest contour, and uses this as our object
    largest_contour = contours[0]
    for con in contours:
        if cv2.contourArea(con) > cv2.contourArea(largest_contour):
            largest_contour = con
    return largest_contour

def find_bounding_box(img, contour):
    
    #generates bounding rectangle
    x, y, w, h = cv2.boundingRect(contour)

    #locates the midpoint of the top side of the bounding rectangle
    #and uses this as the object center
    # NOTE: this is specific to the 2020 competition target, where our
    # object is the bottom half of the whole target (a hexagon)
    center_x = int(x+(w/2))
    center_y = int(y)

    # reject all weird aspect ratios (too tall or flat)
    aspect_ratio = h/w
    expected_aspect_ratio = 17.5/39
    # if (aspect_ratio <= expected_aspect_ratio*.8
    #     or aspect_ratio >= expected_aspect_ratio*1.2):
    #     return -1, -1, -1, -1

    if __DEBUG__:
        contoured_image = cv2.drawContours(img, [contour], -1, (100,0,0), 2) #not using original image
        contoured_image = cv2.rectangle(contoured_image, (x,y), (x+w, y+h), (100, 0, 0), 2)
        contoured_image = cv2.circle(contoured_image, (center_x, center_y), 3, (100, 0, 0), 2)
        
    if __DEBUG__:
        try:
            cv2.imshow("contours", contoured_image)
            cv2.waitKey(0) #Waits long enough for image to load
        except:
            print("monitor not connected")
    
    return w, h, center_x, center_y
    

def find_distance_and_angle(img, w, h, center_x, center_y):
    
    img_center = (img.shape[1]/2, img.shape[0]/2)
    xydist = (center_x - img_center[0], center_y - img_center[1])
    
    camera_fov_degrees = 56 # on the low fov setting
    camera_fov = camera_fov_degrees/360 * 2 * math.pi # convert to radians
    angle_to_obj = (xydist[0] / img.shape[1]) * camera_fov
    angle_to_obj = (180/math.pi)*angle_to_obj
    obj_angle = (w / img.shape[1]) * camera_fov # degrees of fov taken up by the object
    obj_width = 38 # inches - original measurement, probably actually 39"
    distance = ((math.sin((math.pi - obj_angle) / 2) /
                math.sin(obj_angle / 2)) * (obj_width / 2))

    ## empirical measurement were used to come up with these corrections
    distance = distance - .25 * (117 - distance) + 27 # To account for measured error
    
    if __DEBUG__:
        print(str(distance) + "distance to target")
        print(str(angle_to_obj)+ "Angle to object")

    return distance, angle_to_obj

def capture_images(device):
    webcam = cv2.VideoCapture(device)
    
    _, frame = webcam.read()

    if __DEBUG_REMOTE_PI__:
        print("Read image", frame.shape)
    
    
#    if __DEBUG__: 
#       try:
#            cv2.imshow("frame", frame)
#            cv2.waitKey(1)
#        except:
#            print("failed to show frame")

    cv2.imwrite(image_location, frame)
    
    return frame

def init_network_tables():
    global NT_HANDLE
    nt.initialize(server = NT_ADDRESS)
    print("nt is initialized. server is", NT_ADDRESS)    
    NT_HANDLE = nt.getTable(NT_VISON_TABLE_NAME)

def update_network_tables(key, value):
    global NT_HANDLE

    print("updating", key, value, type(value))

    if NT_HANDLE is not None:
        NT_HANDLE.putNumber(key, value)
        print("wrote to nt:", key, value)
    else: 
        print("no network table handle")

def update_distance_angle(distance, angle):
    if __DEBUG_REMOTE_PI__:
        print("updating network tables", distance, angle)

    update_network_tables(DISTANCE_KEY, distance)
    update_network_tables(ANGLE_KEY, angle)
    

def camera_params(): #Only works on linux
    set_camera_params = "v4l2-ctl -d /dev/video0 --set-ctrl=white_balance_automatic=0,exposure=1,contrast=30,gain_automatic=0,auto_exposure=1"
#   while == os.system(set_camera_params):
#
#       continue
    os.system(set_camera_params)

def start():

    init_network_tables()
    camera_params()

    while True:
        before = datetime.datetime.now().timestamp()
        print("Imagetest main is running")
        frame = capture_images(0)
        
        bgr_img = cv2.imread(image_location)
        # print(bgr_img)
        # Convert the frame to HSV
        hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
        
        img_hsv_lower = np.array([50,50,50])
        img_hsv_upper = np.array([180,255,255])
        

        binary_image = process_image(hsv_img, (5,5), img_hsv_lower, img_hsv_upper)

#        if __DEBUG__:
#            try:
#                cv2.imshow("processed image", binary_image)
#                cv2.waitKey(1)
#            except:
#                print("failed to display proccessed image")

        target_contour = find_object(binary_image)

        if __DEBUG_REMOTE_PI__:
            if target_contour is not None:
                print("Found a contour", target_contour.shape)
                # print(target_contour)
            else:
                print("No contours!")
        
        if (target_contour is None):
            continue

        width, height, center_x, center_y = find_bounding_box(binary_image, target_contour)


        if __DEBUG_REMOTE_PI__:
            print("Bounding box is", width, height)


        if width == -1:
            continue
        
        distance, angle = find_distance_and_angle(binary_image, width, height, center_x, center_y)

        update_distance_angle(distance, angle)
        after = datetime.datetime.now().timestamp()
        
        delay = after - before
        print("processing complete in", delay, "microsec")


if __name__ == "__main__":
    
    start()

    # # # Display the BGR image with found objects bounded by rectangles
    # # if(displayImages):
    # #     cv2.imshow("Objects found!", bgr_img)
