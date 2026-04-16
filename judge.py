# 입력된 라벨을 표준화(정규화)하는 함수
def normalize_label(label):
    # 문자열로 변환 후 공백 제거하고 소문자로 변환
    text = str(label).strip().lower()

    # "+", "cross" 형태는 "Cross"로 통일 
    if text in ["+", "cross"]:
        return "Cross"
    # "x" 형태는 "X"로 통일 
    if text == "x":
        return "X"

    # 그 외 값은 알 수 없는 라벨로 처리
    return "UNKNOWN"

# 두 점수를 비교해서 결과를 판단하는 함수
def judge_scores(score_cross, score_x, epsilon=1e-9):
    # 두 값의 차이가 매우 작으면 (거의 같으면) "UNDECIDED" vkseks
    if abs(score_cross - score_x) < epsilon:
        return "UNDECIDED"
     # Cross 점수가 더 크면 "Cross"로, 아니면 "X"로 판단
    if score_cross > score_x:
        return "Cross"
    return "X"