import numpy as np 
import cv2 


imageFrame = cv2.imread("32.jpg") 

color = ['red', 'purple', 'yellow']
lower_colors = [np.array([136, 87, 111]), np.array([94, 80, 2]), np.array([28, 50, 180])]
upper_colors = [np.array([180, 255, 255]), np.array([120, 255, 255]), np.array([35, 255, 255])]
colors_colors = ((0, 0, 150), (255, 80, 100), (0, 200, 180))


def detect(color, lower_color,upper_color, kernel, imageFrame,hsv_image,tmp):
    #define mask
    
    color_mask = cv2.inRange(hsv_image, lower_color, upper_color)
    
    color_mask = cv2.dilate(color_mask, kernel)
    res_color = cv2.bitwise_and(imageFrame, imageFrame, mask = color_mask)
    
    contours, hierarchy = cv2.findContours(color_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)     
    
    for pic, contour in enumerate(contours): 
        area = cv2.contourArea(contour) 
        if(area > 300): 
            x, y, w, h = cv2.boundingRect(contour) 
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), tmp , 2) 
            
            cv2.putText(imageFrame, f"{color}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, tmp)	 

kernel = np.ones((5, 5), "uint8")
hsv_image = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

for i in range(len(color)):
    print(colors_colors[i])
    detect(color[i], lower_colors[i], upper_colors[i], kernel, imageFrame, hsv_image,colors_colors[i] )
        
# Program Termination 
win = cv2.imshow("Multiple Color Detection", cv2.resize(imageFrame,(1820,1020))) 
cv2.moveWindow("Multiple Color Detection", 0, 0)

cv2.waitKey(0) 
cv2.destroyAllWindows() 