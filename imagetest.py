
import cv2 #USE OPENCV 3.1 FOR FINDCONTOURS TO WORK
import numpy as np
import math
from networktables import NetworkTables as nt

__DEBUG__ = True
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
    if (aspect_ratio <= expected_aspect_ratio*.8
        or aspect_ratio >= expected_aspect_ratio*1.2):
        return -1, math.pi

    if __DEBUG__:
        contoured_image = cv2.drawContours(img, [contour], -1, (100,0,0), 2)
        contoured_image = cv2.rectangle(contoured_image, (x,y), (x+w, y+h), (100, 0, 0), 2)
        contoured_image = cv2.circle(contoured_image, (center_x, center_y), 3, (100, 0, 0), 2)
        
    if __DEBUG__:
        try:
            cv2.imshow("contours", contoured_image)
            cv2.waitKey(1) #Waits long enough for image to load
        except:
            print("monitor not connected")
    
    return w, h, center_x, center_y
    

def find_distance_and_angle(img, w, h, center_x, center_y):
    
    img_center = (img.shape[1]/2, img.shape[0]/2)
    xydist = (center_x - img_center[0], center_y - img_center[1])
    
    camera_fov_degrees = 56 # on the low fov setting
    camera_fov = camera_fov_degrees/360 * 2 * math.pi # convert to radians
    angle_to_obj = (xydist[0] / img.shape[1]) * camera_fov
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

    # # Only proceed if contours were found
    # if(contours != None):
    #     if(len(contours) > 1):
    #         sorted(contours, key=lambda contour: getApproximateArea(contour), reverse=True)
    #         contour_boundaries = []
    #         if True: # (len(contours) < 4):
    #             contour_boundaries = [getContourBoundary(contours[0]), getContourBoundary(contours[1])]
    #         else:
    #             interesting_contours = contours[:4]
    #             sorted(interesting_contours, key=lambda contour: abs(getCenterPoint(getContourBoundary(contour))[0] - frame_width/2))
    #             contour_boundaries = [getContourBoundary(interesting_contours[0]), getContourBoundary(interesting_contours[1])]
    #             # TODO: Add code to threshold area of contours
    #             # print("Interesting contours type:", type(interesting_contours))
    #         if sendPackets:
    #             prepareForRoboRIO(contour_boundaries, objName)
    #         else:
    #             sendData(False, 0, 0, "")
    #         for contour_boundary in contour_boundaries[:-1]:
    #             displayObject(contour_boundary, objName)
    #         return displayObject(contour_boundaries[-1], objName)
def capture_images(device):
    webcam = cv2.VideoCapture(device)
    
    _, frame = webcam.read()

    cv2.imwrite("test_images/frame1.jpg", img=frame)
    
    try:
        cv2.imshow("frame", frame)
        cv2.waitKey(1)
    except:
        print("failed to show frame")
    return frame

#def send():




if __name__ == "__main__":
    while True:
        print("Imagetest main is running")
        capture_images(0)
        bgr_img = cv2.imread("test_images/frame1.jpg")
        # cv2.imshow("Hello", bgr_img)
        # cv2.waitKey(5000) # keeps the window open for 5 seconds--long enough to load the image
        # Convert the frame to HSV
        hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
        #cv2.imshow("Win1", bgr_img)
        #img_hsv_lower = np.array([70, 170, 30])
        #img_hsv_upper = np.array([90, 200, 50])
        #color = whiteboard_color = np.array([110,91,80])
        #color = green_color = np.array([34, 177, 76])
        #color = retro_green = np.array([])
        #bound = 40
        #img_hsv_lower = np.array(color - bound)
        #img_hsv_upper = np.array(color + bound)
        img_hsv_lower = np.array([5, 24, 5]) #NOTE: opencv hsv is 0-179, 0-255, 0-255
        img_hsv_upper = np.array([180, 255, 225])
        binary_image = process_image(bgr_img, (5,5), img_hsv_lower, img_hsv_upper)
        try:
            cv2.imshow("dilated image", img_dilate)
            cv2.waitKey(1)
        except:
             print("no monitor")
        #print (hex_dilate.shape)
        #hex_img = np.array([])
        #dist, angle = findObjectContours(img_dilate)

        target_contour = find_object(binary_image)
        if (target_contour is None):
            continue

        width, height, center_x, center_y = find_bounding_box(binary_image, target_contour)

        distance, angle = find_distance_and_angle(binary_image, width, height, center_x, center_y)
        
        
        

    # # # Display the BGR image with found objects bounded by rectangles
    # # if(displayImages):
    # #     cv2.imshow("Objects found!", bgr_img)
