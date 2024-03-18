# 32.jpg

import cv2 
import numpy as np 
import os

# Load image 
#image = cv2.imread("js_l/32.jpg") # 200 0.3 0.9 0.6
image = cv2.imread("186.jpg") 
# Set our filtering parameters 
# Initialize parameter setting using cv2.SimpleBlobDetector 
params = cv2.SimpleBlobDetector_Params() 

# Set Area filtering parameters 
params.filterByArea = True
params.minArea = 200

# Set Circularity filtering parameters 
params.filterByCircularity = True
params.minCircularity = 0.3 # 0.9

# Set Convexity filtering parameters 
params.filterByConvexity = True
params.minConvexity = 0.9 # 0.2
	
# Set inertia filtering parameters 
params.filterByInertia = True
params.minInertiaRatio = 0.6 # 0.01

# Create a detector with the parameters 
detector = cv2.SimpleBlobDetector_create(params) 
	
# Detect blobs 
keypoints = detector.detect(image) 

# Draw blobs on our image as red circles 
blank = np.zeros((1, 1)) 
blobs = cv2.drawKeypoints(image, keypoints, blank, (0, 255, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) 

number_of_blobs = len(keypoints) 
text = "Number of Circular Blobs: " + str(len(keypoints)) 
cv2.putText(blobs, text, (20, 550), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2) 

# Show blobs 
cv2.imshow("Filtering Circular Blobs Only", cv2.resize(blobs,(1920,1080))) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 
