# 한 줄의 입력을 받아서 숫자 리스트로 변환하는 함수
def parse_row(row_text, size):
    # 양쪽 공백 제거 후 공백 기준으로 나눔
    parts = row_text.strip().split()

    # 입력된 값의 개수가 기대한 size와 다르면
    if len(parts) != size:
        # 예외(에러)를 발생시킴
        raise ValueError(f"입력 형식 오류: 각 줄에 {size}개의 숫자를 공백으로 구분해 입력하세요.")

    try:
        # 각 값을 float으로 변환하여 리스트로 반환
        return [float(x) for x in parts]
    except ValueError as exc:
        # 사용자에게 안내 메시지 출력
        raise ValueError("입력 형식 오류: 숫자만 입력하세요.") from exc

# 행렬 전체를 입력받는 함수
def read_matrix(size, name):
    # 올바른 입력이 들어올 때까지 반복
    while True:
        # 사용자에게 입력 형식 안내
        print(f"{name} ({size}줄 입력, 공백 구분)")
        # 행렬 데이터를 저장할 리스트 초기화
        matrix = []
        # 입력이 올바른지 확인하는 변수
        valid = True

        # size만큼 행을 입력받음
        for _ in range(size):
            # 사용자 입력을 받고 공백 제거
            row_text = input().strip()

            try:
                # 한 줄을 숫자 리스트로 변환
                row = parse_row(row_text, size)
                # 변환된 행을 matrix에 추가
                matrix.append(row)
            # 입력 오류가 발생한 경우
            except ValueError as err:
                # 에러 메시지 출력
                print(err)
                # 입력이 유효하지 않음을 표시
                valid = False
                # 반복 중단 (다시 처음부터 입력받기 위해)
                break
        
        # 모든 입력이 정상이고 행 개수도 맞으면
        if valid and len(matrix) == size:
            # 완성된 행렬 반환
            return matrix

        # 잘못된 입력 시 다시 입력 요청
        print("처음부터 다시 입력해주세요.")