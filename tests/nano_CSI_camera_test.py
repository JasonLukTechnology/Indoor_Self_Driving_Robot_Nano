import cv2
import time

# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen or the output size

# The following setting is optimize for low light environment 

def gstreamer_pipeline(
      capture_width=3264,
      capture_height=2464,
      display_width=848,
      display_height=480,
      framerate=11,
      flip_method=0,
      exposure_time= 357142840):
    exp_time_str = '"' + str(90000000) + ' ' + str(exposure_time) + '"'
    return ('nvarguscamerasrc '
            'sensor-id=0 '
            'wbmode=1 '  # 1
            # 'aelock=true '
            # 'awblock=true '
            'gainrange="2 16" '  # 4 16
            'ispdigitalgainrange="2 8" '  # 4 8
            'exposuretimerange=%s '
            'exposurecompensation=0.5 '
            'aeantibanding=0 '
            'tnr-mode=2 '  # 2
            'tnr-strength=1 '  # 1
            # 'ee-mode=2 '
            # 'ee-strength=1 '
            '! video/x-raw(memory:NVMM), '
            'width=%d, height=%d, '
            'format=NV12, '
            'framerate=%d/1 ! '
            'nvvidconv flip-method=%d ! '
            'video/x-raw,  width=(int)%d, height=(int)%d, format=(string)I420 !'
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink max-buffers=1 drop=true"
            % (exp_time_str, capture_width, capture_height, framerate, flip_method, display_width, display_height))


class nano_cam:
    def __init__(self):
        # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
        self.cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

    def show_camera(self, img_name):
        if self.cap.isOpened():
            ret_val, img = self.cap.read()
            print(ret_val)
            cv2.imwrite(img_name, img)
            # This also acts as

    def close_camera(self):
        if self.cap != None:
            self.cap.release()
            

if __name__ == "__main__":
     t1 = time.time() # start time in seconds
     c = nano_cam() # Initiate the camera
     time.sleep(0.2) # Wait for 2 secs
     c.show_camera("jasonluk_test.jpg") # capture image
     c.close_camera() # Close camera object
     print(time.time()-t1) # calculate time usage in seconds
