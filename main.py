import MultiCamera
import detect

import cv2
from realsense_depth import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    """ Main """
    # MultiCamera.Run()
    # MultiCamera.CamRun("camera1", 0)
    # MultiCamera.CamRun("camera2", 2)

    # 단일 카메라에서 디텍팅 먼저
    detect.run(source=0, save_txt=True)



    # while True:
    #     ret,
