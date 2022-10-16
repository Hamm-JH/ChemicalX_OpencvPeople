import cv2
import pyrealsense2


def Parse(line: str, imgsz: tuple):
    """ 라인 문자열 파싱"""

    splits = line.split()
    label = splits[0]
    lVal = [float(splits[1]), float(splits[2]), float(splits[3]), float(splits[4])]
    lVal = [lVal[0] * imgsz[0], lVal[1] * imgsz[1], lVal[2] * imgsz[0], lVal[3] * imgsz[1]]
    return label, lVal

# list :: list
# camIndex :: str
def OnDetect(image, list : list[str], camIndex : str):
    """ 디텍팅 결과 반환"""
    imgsz = (640, 480) # :: tuple

    # print(f'list : {type(list)}, {list}')
    # print(f'cam index {type(camIndex)}, {camIndex}') # '0', '2'
    # print(f'img size : {type(imgsz)}, {imgsz}')   # (640, 480)



    # 보간해보기
    for line in list:
        # print(line)
        # print(splits)

        # splits = line.split()
        # label = splits[0]
        # lVal = [float(splits[1]), float(splits[2]), float(splits[3]), float(splits[4])]

        label, lVal = Parse(line, imgsz)

        # print(f'label {label}, values {lVal}')

        # if label == '0':
        if label == '65':
            print(f'label {label}, values {lVal}')

    cv2.circle(image, (320, 240), 15, (255, 0, 255), -1)

