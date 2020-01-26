# read and process an image
# hi
import cv2 #USE OPENCV 3.1 FOR FINDCONTOURS TO WORK
import numpy as np

displayImages =  True

def removeNoise(hsv_img, kernelSize, lower_color_range, upper_color_range):
    # Kernal to use for removing noise
    kernel = np.ones(kernelSize, np.uint8)
    # Convert image to binary
    mask = cv2.inRange(hsv_img, lower_color_range, upper_color_range)
    # Show the binary (masked) image
    # if(displayImages):
    #     cv2.imshow("img", mask)
    # Close the gaps (due to noise) in the masked image
    close_gaps = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # Remove noisy parts of the masked image
    no_noise = cv2.morphologyEx(close_gaps, cv2.MORPH_OPEN, kernel)
    # Undo the erosion to the actual target done during noise removal
    dilate = cv2.dilate(no_noise, np.ones((5,10), np.uint8), iterations=5)
    return dilate

def findObjectContours(dilate, objName):
    # Find boundary of object
    dilcopy = dilate.copy()
    _, contours, _ = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(len(returns))
    con = contours[0]
    x, y, w, h = cv2.boundingRect(con)
    obj_center = (int(x+(w/2)), int(y+(h/2))) 
    img_center = (dilate.shape[1]/2, dilate.shape[0]/2)
    xydist = (obj_center[0]-img_center[0], obj_center[1] -img_center[1])
    print(str(xydist) + "x,y distances")
    #moments = cv2.moments(con)
    #print(moments)
    print(str(len(contours)) + " -contour length")
    #print(contours)
    contoured_image = cv2.drawContours(dilcopy, contours, -1, (100,0,0), 2)
    contoured_image = cv2.rectangle(contoured_image, (x,y), (x+w, y+h), (100, 0, 0), 2)
    contoured_image = cv2.circle(contoured_image, obj_center, 3, (100, 0, 0), 2)
    cv2.imshow("contours", contoured_image)
    cv2.waitKey(0) #Waits long enough for image to load

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
    cv2.imshow("frame", frame)
    cv2.waitKey(0)
    return frame
if __name__ == "__main__":
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
    img_hsv_lower = np.array([49, 70, 87]) #NOTE: opencv hsv is 0-179, 0-255, 0-255
    img_hsv_upper = np.array([180, 255, 225])
    img_dilate = removeNoise(bgr_img, (3,3), img_hsv_lower, img_hsv_upper)
    cv2.imshow("dilated image", img_dilate)
    cv2.waitKey(0)
    #print (hex_dilate.shape)
    #hex_img = np.array([])
    findObjectContours(img_dilate, "retroreflective")
    while True:

        continue

    # # # Display the BGR image with found objects bounded by rectangles
    # # if(displayImages):
    # #     cv2.imshow("Objects found!", bgr_img)
