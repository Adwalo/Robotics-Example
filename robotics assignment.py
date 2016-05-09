#dependencies
import rospy
import cv2
import numpy
from random import uniform
from geometry_msgs.msg import Twist 
from cv2 import namedWindow, imshow
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class Fear():


    def __init__(self):
        
        #Initializing camera windows and bridge
        namedWindow("colorblue", 1)
        namedWindow("colorgreen", 1)
        namedWindow("colorred", 1)
        cv2.startWindowThread()
        self.bridge = CvBridge()
        
        #Subcribing to camera node to get data REMOVE TURTLEBOT_2 WHEN USING REAL ROBOT
        self.image_sub = rospy.Subscriber("/turtlebot_2/camera/rgb/image_raw", Image, self.callback)
                                          
        #Publishing to Twist node for movement REMOVE TURTLEBOT_2 WHEN USING REAL ROBOT
        self.pub = rospy.Publisher("/turtlebot_2/cmd_vel", Twist) 
        
    def callback(self, data):
        
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError, e:
            print e
        
        #Converting image to HSV
        hsv_img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        
        #Range of blue scale
        hsv_blue = cv2.inRange(hsv_img,
                                 numpy.array((110, 100, 100)),
                                 numpy.array((130, 255, 255))) 
        #Range of green scale                        
        hsv_green = cv2.inRange(hsv_img,
                                 numpy.array((50, 100, 100)),
                                 numpy.array((70, 255, 255))) 
        #Range of red scale                         
        hsv_red = cv2.inRange(hsv_img,
                                 numpy.array((0, 100, 100)),
                                 numpy.array((10, 255, 255))) 
                                 
        #Pixel threshold for the amount of colour in the image
        numofblue=sum(hsv_blue[:])
        numofgreen=sum(hsv_green[:])
        numofred=sum(hsv_red[:])
        
        #Random variables for red threshold movement
        randz = uniform(-2,2)
        randx = uniform(-2,2)
        

        #If number of coloured pixels in the image arrays are less than the threshold spin on the spot.
        if (numofblue < 999999 and numofgreen < 999999 and numofred < 999999):          
            r = rospy.Rate(10);
            twist_msg = Twist()
            twist_msg.angular.z = 0.3
            twist_msg.linear.x = 0.0
            self.pub.publish(twist_msg)
            r.sleep()

        #If number of blue pixels in the image (hsv_blue) array are more than the threshhold freeze until threat passes.
        if numofblue > 1000000:
            r = rospy.Rate(10);
            twist_msg = Twist()
            twist_msg.angular.z = 0.0
            twist_msg.linear.x = 0.0
            self.pub.publish(twist_msg)
            r.sleep()
            imshow("colorblue", hsv_blue)
            print numofblue
        #If number of green pixels in the image (hsv_green) are more than the threshold, back away until away from the threat.   
        if numofgreen > 1000000:          
            r = rospy.Rate(10);
            twist_msg = Twist()
            twist_msg.angular.z = 0.0
            twist_msg.linear.x = -0.3
            self.pub.publish(twist_msg)
            r.sleep()
            imshow("colorgreen", hsv_green)
            print numofgreen
        #If number of red pixels in the image (hsv_red) are more than the threshold, randomly flail until threat is gone.    
        if numofred > 1000000:          
            r = rospy.Rate(10);
            twist_msg = Twist()
            twist_msg.angular.z = randz
            twist_msg.linear.x = randx
            self.pub.publish(twist_msg)
            r.sleep()
            imshow("colorred", hsv_red)
            print numofred
            
if __name__ == '__main__':
    rospy.init_node("Fear")
    cv = Fear()
    rospy.spin()
