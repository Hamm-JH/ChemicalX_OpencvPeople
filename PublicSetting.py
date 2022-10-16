from enum import Enum

class PublicSetting(Enum):
    """ 세팅값 """
    serverUrl = 'http://192.168.10.11:3002/VISION'
    requestInterval = 0.3

    labelTarget = '0'   # 사람
    # labelTarget = '65'    # 디버깅 리모컨

    DetectingCount = 2  # 디텍팅 수량