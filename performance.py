# 시간 측정을 위한 모듈 import
import time
from mac import mac_operation

# MAC 연산의 평균 실행 시간을 측정하는 함수
def measure_mac_time(pattern, flt, repeat=10):
    # 정밀한 시간 측정을 위해 시작 시간 기록
    start = time.perf_counter()

    # repeat 횟수만큼 반복 실행
    for _ in range(repeat):
        # MAC 연산 실행
        mac_operation(pattern, flt)

    # 종료 시간 기록
    end = time.perf_counter()
    # 평균 실행 시간을 밀리초(ms) 단위로 계산
    avg_ms = ((end - start) / repeat) * 1000
    # 평균 실행 시간 반환
    return avg_ms