import math

import cv2
import pyrealsense2
from realsense_depth import *

dc = DepthCamera()

# region [1. parse]

def Parse(line: str, imgsz: tuple):
    """ 라인 문자열 파싱"""

    splits = line.split()
    label = splits[0]
    lVal = [float(splits[1]), float(splits[2]), float(splits[3]), float(splits[4])]
    lVal = [lVal[0] * imgsz[0], lVal[1] * imgsz[1], lVal[2] * imgsz[0], lVal[3] * imgsz[1]]
    return label, lVal

#endregion

# region [2. get near two]

def nearSort(nearResult):
    return nearResult[0]

def GetNearTwo(peoples: list, center):
    """ 근저 두명 데려오기"""

    # print(len(peoples))
    # print(type(peoples))  # 아래것들 가지고 있음
    # print(type(peoples[0])) # [320, 240, 1200]

    nearResult = []

    for pp in peoples:
        # print(pp)

        ctop = (pp[0]-center[0], pp[1]-center[1])
        distance = math.sqrt(ctop[0]*ctop[0] + ctop[1]*ctop[1])
        res = (distance, pp)
        # print(distance)

        nearResult.append(res)

    # 정렬
    nearResult.sort(key=nearSort)

    # print(peoples)
    # print(nearResult)
    # print()

    result = []
    result.append(nearResult[0][1])
    result.append(nearResult[1][1])

    return result
    # 거리별 정렬이 완료되었으니, 가장 가까운 대상을 기준으로 C기준 거리 추정을 수행한다.

#endregion


# list :: list
# camIndex :: str
def OnDetect(image, list : list[str], camIndex : str):
    """ 디텍팅 결과 반환"""
    imgsz = (640, 480) # :: tuple
    cPx = (320, 240)

    # print(f'list : {type(list)}, {list}')
    # print(f'cam index {type(camIndex)}, {camIndex}') # '0', '2'
    # print(f'img size : {type(imgsz)}, {imgsz}')   # (640, 480)

    # dc = DepthCamera()
    ret, depth_frame, color_frame = dc.get_frame()

    cDep = depth_frame[320, 240]
    print(f'distance {cDep}')

    peoples = []

    # 보간해보기
    for line in list:
        # print(line)
        # print(splits)

        # splits = line.split()
        # label = splits[0]
        # lVal = [float(splits[1]), float(splits[2]), float(splits[3]), float(splits[4])]

        label, lVal = Parse(line, imgsz)

        # print(f'label {label}, values {lVal}')

        # if label == '0':  # 사람
        if label == '65':   # 리모컨 (데모용)
            # print(f'label {label}, values {lVal}')
            depth = depth_frame[int(lVal[0]), int(lVal[1])]
            center = (int(lVal[0]), int(lVal[1]))
            # print(f'center {center}, depth {depth}')
            people = [center[0], center[1], depth]

            peoples.append(people)



    if len(peoples) >= 2:
        nears = GetNearTwo(peoples, cPx)

        print(nears)
        # if len(peoples) > 2:
        #     peoples = GetNearTwo(peoples)

        # 근처 두명 잡아두고 거리재기 시작


    cv2.circle(image, (320, 240), 15, (255, 0, 255), -1)

