from input_handler import read_matrix
from mac import mac_operation
from judge import judge_scores, normalize_label
from json_handler import load_json_data, extract_size_from_key, validate_matrix_size, get_filters_for_size
from performance import measure_mac_time


class MiniNPUSimulator:
    # 클래스가 생성될 때 자동으로 실행되는 초기화 함수
    def __init__(self):
         # 부동소수점 비교 시 사용할 아주 작은 기준값 (오차 허용 범위)
        self.epsilon = 1e-9
        # 사용할 데이터 파일 이름을 저장
        self.data_file = "data.json"

    # 프로그램의 메인 실행 루프를 담당하는 함수
    def run(self):
        # 사용자가 종료할 때까지 계속 반복
        while True:
            print("\n=== Mini NPU Simulator ===")
            print("[모드 선택]")
            print("1. 사용자 입력 (3x3)")
            print("2. data.json 분석")
            print("3. 종료")

            # 사용자 입력을 받고 공백 제거
            choice = input("선택: ").strip()
    
            if choice == "1":
                self.run_user_input_mode()
    
            elif choice == "2":
                self.run_json_mode()
    
            elif choice == "3":
                print("프로그램을 종료합니다.")
                break
            
            else:
                print("올바른 번호를 입력하세요.")

    # 사용자 입력을 받아 MAC 연산 및 판정을 수행하는 함수
    def run_user_input_mode(self):
        print("#---------------------------------------")
        print("# [1] 필터 입력")
        print("#---------------------------------------")
        # 3x3 크기의 필터 A, B 입력
        filter_a = read_matrix(3, "필터 A")
        filter_b = read_matrix(3, "필터 B")

        print("#---------------------------------------")
        print("# [2] 패턴 입력")
        print("#---------------------------------------")
        # 3x3 크기의 패턴 입력
        pattern = read_matrix(3, "패턴")

        # 패턴과 필터 A, B의 MAC 연산 결과
        score_a = mac_operation(pattern, filter_a)
        score_b = mac_operation(pattern, filter_b)
    
        # 점수 차이가 거의 없으면 "UNDECIDED" 출력 
        if abs(score_a - score_b) < self.epsilon:
            decision = "UNDECIDED"
        # A 점수가 더 크면 "A"를, B 점수가 더 크면 "B"를 판단
        elif score_a > score_b:
            decision = "A"
        else:
            decision = "B"

        # MAC 연산 평균 시간 측정
        avg_time = measure_mac_time(pattern, filter_a, repeat=10)

        print("#---------------------------------------")
        print("# [3] MAC 결과")
        print("#---------------------------------------")
        # A 점수 출력
        print(f"A 점수: {score_a}") 
        # B 점수 출력
        print(f"B 점수: {score_b}")
        # 평균 연산 시간 출력 (소수점 6자리)
        print(f"연산 시간(평균/10회): {avg_time:.6f} ms")
        # 최종 판정 결과 출력
        print(f"판정: {decision}")

    # data.json 파일을 읽어 패턴 분석과 성능 측정을 수행하는 함수
    def run_json_mode(self):  
        try:
            # JSON 파일에서 전체 데이터를 불러옴
            data = load_json_data(self.data_file)  
        # 파일이 없는 경우
        except FileNotFoundError:  
            # 오류 메시지 출력
            print(f"오류: {self.data_file} 파일을 찾을 수 없습니다.")  
            # 함수 종료
            return  
        # 그 외 다른 예외가 발생한 경우
        except Exception as err:  
            # 예외 내용 출력
            print(f"오류: {err}")  
            # 함수 종료
            return  
    
        # JSON에서 filters 데이터를 가져오고 없으면 빈 딕셔너리 사용
        filters_data = data.get("filters", {})  
        # JSON에서 patterns 데이터를 가져오고 없으면 빈 딕셔너리 사용
        patterns_data = data.get("patterns", {})  
    
        # 각 패턴의 판정 결과를 저장할 리스트
        results = []  
        # 성능 측정 결과를 저장할 리스트
        performance_rows = []  
        # 이미 성능 측정을 한 size를 저장하는 집합
        seen_sizes = set()  
    
        print("#---------------------------------------")
        print("# [1] 필터 로드")
        print("#---------------------------------------")
    
        # 사용할 필터 크기 목록을 순회
        for size in [5, 13, 25]:  
            try:
                # 해당 크기의 Cross, X 필터를 불러오는지 확인
                get_filters_for_size(filters_data, size)  
                print(f"✓ size_{size} 필터 로드 완료 (Cross, X)")  
            # 필터 로드 중 오류가 발생한 경우
            except Exception as err:  
                print(f"✗ size_{size} 필터 로드 실패: {err}")  
    
        print("#---------------------------------------")
        print("# [2] 패턴 분석 (라벨 정규화 적용)")
        print("#---------------------------------------")
    
        # 모든 패턴 데이터를 순회
        for key, item in patterns_data.items():  
            # 실패 시 저장할 기본 결과 구조
            fail_result = {  
                "id": key,
                "status": "FAIL",
                "reason": ""
            }
    
            try:
                # 패턴 키에서 행렬 크기 추출
                size = extract_size_from_key(key)  
                # 패턴 입력 행렬 가져오기
                pattern = item.get("input")  
                # 원본 expected 라벨 가져오기
                expected_raw = item.get("expected")  
                # expected 라벨을 표준 형식으로 정규화
                expected = normalize_label(expected_raw)  
    
                # 해당 크기의 Cross, X 필터 가져오기
                cross_filter, x_filter = get_filters_for_size(filters_data, size)  
    
                # 패턴 행렬 크기가 올바르지 않은 경우
                if not validate_matrix_size(pattern, size):  
                    # 실패 이유 저장
                    fail_result["reason"] = f"패턴 크기 불일치: expected {size}x{size}"  
                    # 결과 리스트에 추가
                    results.append(fail_result)  
                    # 패턴 구분선 출력
                    print(f"--- {key} ---")  
                    # 실패 메시지 출력
                    print(f"FAIL: {fail_result['reason']}")  
                    # 다음 패턴으로 이동
                    continue  
                
                # Cross 필터 크기가 올바르지 않은 경우
                if not validate_matrix_size(cross_filter, size):  
                    fail_result["reason"] = f"Cross 필터 크기 불일치: expected {size}x{size}"
                    results.append(fail_result)
                    print(f"--- {key} ---")
                    print(f"FAIL: {fail_result['reason']}")
                    continue
                
                # X 필터 크기가 올바르지 않은 경우
                if not validate_matrix_size(x_filter, size):  
                    fail_result["reason"] = f"X 필터 크기 불일치: expected {size}x{size}"
                    results.append(fail_result)
                    print(f"--- {key} ---")
                    print(f"FAIL: {fail_result['reason']}")
                    continue
                
                # expected 라벨을 정규화할 수 없는 경우
                if expected == "UNKNOWN":  
                    fail_result["reason"] = f"expected 라벨 정규화 실패: {expected_raw}"
                    results.append(fail_result)
                    print(f"--- {key} ---")
                    print(f"FAIL: {fail_result['reason']}")
                    continue
                
                # Cross 필터와 MAC 연산 수행
                score_cross = mac_operation(pattern, cross_filter)  
                # X 필터와 MAC 연산 수행
                score_x = mac_operation(pattern, x_filter)  
                # 두 점수를 비교하여 최종 판정
                decision = judge_scores(score_cross, score_x, self.epsilon)  
    
                # 판정이 expected와 같으면 PASS, 다르면 FAIL
                status = "PASS" if decision == expected else "FAIL"  
                # 기본 사유 설정
                reason = "정상 판정"  
    
                # FAIL인 경우 상세 사유 설정
                if status == "FAIL":  
                    # 점수가 같아 판정 불가인 경우
                    if decision == "UNDECIDED":  
                        reason = "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
                    # expected와 실제 판정이 다른 경우
                    else:  
                        reason = f"예상값 불일치: expected={expected}, actual={decision}"
    
                # 현재 패턴 구분선 출력
                print(f"--- {key} ---")  
                print(f"Cross 점수: {score_cross}")  
                print(f"X 점수: {score_x}")  
                print(f"판정: {decision} | expected: {expected} | {status}")  
    
                # 최종 결과 저장
                results.append({  
                    "id": key,
                    "status": status,
                    "reason": reason
                })
    
                # 아직 이 크기에 대한 성능 측정을 하지 않았다면
                if size not in seen_sizes:  
                    # 평균 연산 시간 측정
                    avg_ms = measure_mac_time(pattern, cross_filter, repeat=10)  
                    # 성능 결과 저장
                    performance_rows.append({  
                        "size": f"{size}x{size}",
                        "avg_ms": avg_ms,
                        "ops": size * size
                    })
                    # 측정 완료한 size로 등록
                    seen_sizes.add(size)  
    
            # 패턴 처리 중 예외가 발생한 경우
            except Exception as err:  
                # 예외 메시지를 실패 사유로 저장
                fail_result["reason"] = str(err)  
                # 결과 리스트에 추가
                results.append(fail_result)  
                print(f"--- {key} ---")
                print(f"FAIL: {fail_result['reason']}")  
    
        # 3x3 Cross 샘플 필터
        sample_3_cross = [  
            [0.0, 1.0, 0.0],
            [1.0, 1.0, 1.0],
            [0.0, 1.0, 0.0]
        ]
        # 3x3 샘플 패턴
        sample_3_pattern = [  
            [0.0, 1.0, 0.0],
            [1.0, 1.0, 1.0],
            [0.0, 1.0, 0.0]
        ]
    
        # 성능 표의 첫 번째 행에 3x3 샘플 결과 추가
        performance_rows.insert(0, {  
            "size": "3x3",
            # 3x3 평균 연산 시간 측정
            "avg_ms": measure_mac_time(sample_3_pattern, sample_3_cross, repeat=10),  
            # 3x3이므로 연산 횟수는 9
            "ops": 9  
        })
    
        # 성능 측정 결과 표 출력
        self.print_performance_table(performance_rows)  
        # 전체 PASS/FAIL 요약 출력
        self.print_summary(results)  
    
    def print_performance_table(self, rows):
        print("#---------------------------------------")
        print("# [3] 성능 분석 (평균/10회)")
        print("#---------------------------------------")
        print(f"{'크기':<10}{'평균 시간(ms)':<20}{'연산 횟수(N²)':<15}")
        print("-" * 45)

        for row in rows:
            print(f"{row['size']:<10}{row['avg_ms']:<20.6f}{row['ops']:<15}")

    def print_summary(self, results):
        total = len(results)
        passed = sum(1 for r in results if r["status"] == "PASS")
        failed = total - passed

        print("#---------------------------------------")
        print("# [4] 결과 요약")
        print("#---------------------------------------")
        print(f"총 테스트: {total}개")
        print(f"통과: {passed}개")
        print(f"실패: {failed}개")

        if failed > 0:
            print("실패 케이스:")
            for result in results:
                if result["status"] == "FAIL":
                    print(f"- {result['id']}: {result['reason']}")