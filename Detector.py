import math
import time

import requests

import cv2
import pyrealsense2
from realsense_depth import *

dc = DepthCamera()
XPPerD = 0.1359375  # 픽셀당 x 각도
YPPerD = 0.11875    # 픽셀당 y 각도

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

# region [3. 리얼벡터 구하기]

# region [3-1. 픽셀차에서 각도 구하기]

def distToDeg(xdist, ydist):
    """ 각도 구하기"""
    xdeg = xdist * XPPerD
    ydeg = ydist * YPPerD

    return (xdeg, ydeg)

# endregion

# region [3-2. 3-6. 각도로 평행거리 구하기]

def degToHDist(deg, cDepth):
    """ 각도로 거리구하기"""
    # print(deg)

    xhdist = math.tan(math.radians(deg[0])) * cDepth
    yhdist = math.tan(math.radians(deg[1])) * cDepth

    # print(xhdist, yhdist)
    return (xhdist, yhdist)

# endregion

# region [3-3. 평행 거리 구하기]

def horizontalDepth(hdist, cDepth):
    """ 포인트의 평행 뎁스 구하기"""
    t1 = hdist[0]
    t2 = hdist[1]
    t3 = float(cDepth)

    hDepth = math.sqrt(t1**2 + t2**2 + t3**2)

    return hDepth

# endregion

# region [3-4. 평행뎁스와 측정 뎁스간 비율 구하기]

def depthRatio(hdepth, depth):
    """ 수평거리 뎁스와 그냥 뎁스간 비교"""
    
    # 측정된 거리 / 수평 뎁스거리
    return depth / hdepth

# endregion

# region [3-5. 측정된 비율로 측정 뎁스의 중심 뎁스 구하기]

def getCenterDepth(dRatio, cDepth):
    """ 측정 거리의 중심 뎁스 계산"""

    return cDepth * dRatio

# endregion

# region [3-7. 중심점에서 뎁스간 사잇거리 계산]

def diffCenterDepth(rcDepth, cDepth):
    """ 중심점간 거리 구하기"""
    return rcDepth - cDepth

# endregion

# endregion

# region [4. 벡터간 거리 구하기]

def getFinalDists(p1, p2):
    """ 두 사람간 거리 계산"""
    p1c = float(p1[2])
    p2c = float(p2[2])
    p1p2 = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

    return p1c, p2c, p1p2

# endregion

# list :: list
# camIndex :: str
def OnDetect(image, list : list[str], camIndex : str):
    """ 디텍팅 결과 반환"""
    imgsz = (640, 480) # :: tuple
    cPx = (320, 240)

    print(f'cam index : {camIndex}')

    # print(f'list : {type(list)}, {list}')
    # print(f'cam index {type(camIndex)}, {camIndex}') # '0', '2'
    # print(f'img size : {type(imgsz)}, {imgsz}')   # (640, 480)

    # dc = DepthCamera()
    ret, depth_frame, color_frame = dc.get_frame()

    # 중심 뎁스 계산
    cDep = depth_frame[320, 240]
    # 중심 좌표
    cPoint = (320, 240, cDep)
    # print(f'center distance {cDep}')

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

        if label == '0':  # 사람
        # if label == '65':   # 리모컨 (데모용)
            # print(f'label {label}, values {lVal}')
            depth = depth_frame[int(lVal[0]), int(lVal[1])]
            center = (int(lVal[0]), int(lVal[1]))
            # print(f'center {center}, depth {depth}')
            people = [center[0], center[1], depth]

            peoples.append(people)

    if len(peoples) >= 2:
        realVector = []

        # 근처 두명 추려내기 (캠 기준)
        nears = GetNearTwo(peoples, cPx)
        # print(nears)

        cv2.line(image, (nears[0][0], nears[0][1]), (nears[1][0], nears[1][1]), (255, 0, 255))

        # 근처 두명 잡아두고 거리재기 시작
        # x축 fov 87
        # y축 fov 57
        for elem in nears:
            # 0 [400, 327, 347]
            # 1 [112, 384, 1355]
            # print(f'center depth {cDep}')
            # print(f'element {elem}')

            xdiff = elem[0] - cPoint[0] # x 픽셀차
            ydiff = elem[1] - cPoint[1] # y 픽셀차
            xdist = int(math.fabs(xdiff))
            ydist = int(math.fabs(ydiff))

            # print(xdiff, ydiff)
            # print(xdist, ydist)
            
            # 1. 픽셀차로 각도 구하기
            deg = distToDeg(xdist, ydist)
            # print(res)

            # 2. 구한 각도로 평행 거리 구하기
            hdist = degToHDist(deg, cDep)
            # print(f'h dist : {hdist}')

            # 3. 구한 거리로 평행 뎁스 구함
            hdepth = horizontalDepth(hdist, cDep)
            # print(f'h depth : {hdepth}')

            # 4. 측정된 거리 / 수평 뎁스거리 계산
            # 1보다 크면 카메라 기준점보다 멀리 있음
            # 1보다 작으면 카메라 기준점보다 가까이 있음
            depRatio = depthRatio(hdepth, elem[2])
            # print(f'depth ratio : {depRatio}')

            # 5. 측정된 비율로 측정 뎁스의 중심뎁스 계산
            calCenterDepth = getCenterDepth(depRatio, cDep)
            # print(f'cal center depth : {calCenterDepth}')

            # 6. 각도와 실측 중심 뎁스간 평행 거리 구하기
            rcdist = degToHDist(deg, calCenterDepth)
            # print(f'real center to point {rcdist}')

            # 7. 중심점에서 뎁스간 사잇거리 계산
            rcdDiff = diffCenterDepth(calCenterDepth, cDep)
            # print(f'center diff {rcdDiff}')

            # 8. 최종 중심점 대비 리얼벡터
            result = (rcdist[0], rcdist[1], rcdDiff)
            # print(f'result {result}')

            realVector.append(result)

        p1c, p2c, p1p2 = getFinalDists(realVector[0], realVector[1])

        data = {
            "camID" : camIndex,
            "result" : {
                "p1CDist" : math.fabs(p1c),
                "p2CDist" : math.fabs(p2c),
                "p1p2Dist" : p1p2
            }
        }

        # print(type(data))
        # print(type(camIndex))
        # print(type(p1c))
        # print(type(p2c))
        # print(type(p1p2))

        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        # params=
        res = requests.get(url='http://192.168.10.11:3002/VISION', json=data, headers=headers)

        time.sleep(0.3)

    # cv2.circle(image, (320, 240), 15, (255, 0, 255), -1)

