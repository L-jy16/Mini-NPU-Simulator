import json
# 필터 이름을 정규화하기 위한 함수 import
from judge import normalize_label

 # JSON 파일을 읽어서 데이터를 반환하는 함수
def load_json_data(filename):
    # 파일을 읽기 모드로 열기
    with open(filename, "r", encoding="utf-8") as file:
        # JSON 데이터를 파싱하여 파이썬 객체로 반환
        return json.load(file)

# 키 문자열에서 크기(size)를 추출하는 함수
def extract_size_from_key(key):
    # "_" 기준으로 문자열을 나눔
    parts = key.split("_")

    # 형식이 올바르지 않은 경우
    if len(parts) < 3 or parts[0] != "size":
        raise ValueError(f"잘못된 패턴 키 형식: {key}")

    try:
        # 두 번째 값을 정수로 변환하여 반환 (예: size_3_x → 3)
        return int(parts[1])
    # 숫자로 변환 실패 시
    except ValueError as exc:
        raise ValueError(f"크기 추출 실패: {key}") from exc

# 행렬의 크기가 올바른지 검사하는 함수
def validate_matrix_size(matrix, size):
    # 리스트가 아니거나 행 개수가 다르면 false 반환
    if not isinstance(matrix, list) or len(matrix) != size:
        return False

    # 각 행 검사
    for row in matrix:
        # 행이 리스트가 아니거나 열 개수가 다르면 false 반환
        if not isinstance(row, list) or len(row) != size:
            return False

    return True

# 특정 size에 해당하는 필터를 가져오는 함수
def get_filters_for_size(filters_data, size):
    # size에 맞는 키 생성 (예: size_3)
    size_key = f"size_{size}"

    # 해당 키가 존재하지 않으면
    if size_key not in filters_data:
        raise KeyError(f"{size_key} 필터가 존재하지 않습니다.")

    # 해당 size의 필터 데이터 가져오기
    raw_filters = filters_data[size_key]

    # 필터 구조가 딕셔너리가 아니면
    if not isinstance(raw_filters, dict):
        raise ValueError(f"{size_key} 필터 구조가 올바르지 않습니다.")

    # 정규화된 필터를 저장할 딕셔너리
    normalized = {}

    # 필터 이름과 행렬을 순회
    for key, matrix in raw_filters.items():
        # 필터 이름을 정규화
        label = normalize_label(key)
        # 정규화된 이름을 키로 저장
        normalized[label] = matrix

    # 필수 필터가 없는 경우
    if "Cross" not in normalized or "X" not in normalized:
        raise ValueError(f"{size_key} 필터에 Cross/X 필터가 모두 있어야 합니다.")

    # Cross와 X 필터를 반환
    return normalized["Cross"], normalized["X"]