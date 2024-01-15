#!/usr/bin/env python3

import rospy
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import tensorflow as tf
import time
import os


class Callbacks:
    def __init__(self):
        self.image = None
        self.bridge = CvBridge()
        self.folder_path = os.getenv("FOLDER_PATH")
        self.erfnet_interpreter = tf.lite.Interpreter(model_path=os.getenv("MODEL_PATH"))
        self.erfnet_interpreter.allocate_tensors()
        self.erfnet_input_details = self.erfnet_interpreter.get_input_details()
        self.erfnet_output_details = self.erfnet_interpreter.get_output_details()
        self.num = 1
        self.rate = rospy.Rate(0.5)

        rospy.Subscriber("/cv_camera/image_raw", Image, self.image_callback)
        rospy.Subscriber("/speeding", String, self.speeding)
        self.speed_publisher = rospy.Publisher('/Twist', Twist, queue_size=10)


    def image_callback(self, data):
        self.image = self.bridge.imgmsg_to_cv2(data, desired_encoding='passthrough')
        self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)

    def process(self):
        if self.image is not None:
            img_str = f'image_{self.num}.png'
            cv2.imwrite(self.folder_path + img_str, self.image)
            self.make_prediction()
            self.num += 1

    def make_prediction(self):
        time_load_start = time.perf_counter()

        n_img = np.array(self.image, dtype='float32')
        n_img = np.expand_dims(n_img, axis=0)
        print(n_img.shape)

        time_start = time.perf_counter()
        self.erfnet_interpreter.set_tensor(self.erfnet_input_details[0]['index'], n_img)
        self.erfnet_interpreter.invoke()
        erfnet_preds = self.erfnet_interpreter.get_tensor(self.erfnet_output_details[0]['index'])
        time_end_pred = time.perf_counter() - time_start

        erfnet_preds_save = (erfnet_preds > 0.8).astype(np.uint8)
        erfnet_preds_save = erfnet_preds_save * 255
        erfnet_preds_end = np.squeeze(erfnet_preds_save)
        print(erfnet_preds_end.shape)
        img_str = f'image_{self.num}_1.png'
        cv2.imwrite(self.folder_path + img_str, erfnet_preds_end)
        time_load_end = time.perf_counter() - time_load_start
        print(f"Load time: {time_load_end}")
        print(f"Prediction time: {time_end_pred}")



if __name__ == '__main__':
    rospy.init_node('image_save_node')
    callbacks = Callbacks()
    try:
        rate = rospy.Rate(0.5)  # 0.2 hz
        while not rospy.is_shutdown():
            callbacks.process()
            rate.sleep()
    except rospy.ROSInterruptException:
        pass
