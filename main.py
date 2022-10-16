import MultiCamera
import detect
import pyautogui as auto
# import uiautomation as auto
import keyboard

import cv2
from realsense_depth import *

def stopAllThread(thread :MultiCamera.camThread):
    """ 모든 스레드 멈추기"""


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    """ Main """
    # MultiCamera.Run()
    thread1 = MultiCamera.CamRun("camera1", 0)
    thread2 = MultiCamera.CamRun("camera2", 2)

    # 단일 카메라에서 디텍팅 먼저
    # detect.run(source=0, save_txt=True)
    # print(type(thread1))
    #
    # keyboard.add_hotkey('ctrl+num 9', lambda : print('hello'))

    # while True:
    #     ret,
