# pattern과 flt(필터)를 입력받아 MAC 연산을 수행하는 함수 정의
def mac_operation(pattern, flt):
    # 결과 값을 저장할 변수 초기화 (실수형)
    total = 0.0
    # pattern의 크기(행 또는 열 길이)를 구함 
    n = len(pattern)

    # pattern의 행을 순회
    for i in range(n):
        # pattern의 열을 순회
        for j in range(n):
            # 각 위치의 값을 곱해서 total에 누적
            total += pattern[i][j] * flt[i][j]

    return total