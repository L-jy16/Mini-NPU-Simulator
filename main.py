# simulator 파일에서 MiniNPUSimulator 클래스를 가져옴
from simulator import MiniNPUSimulator

def main():
    # MiniNPUSimulator 객체를 생성해서 simulator 변수에 저장
    simulator = MiniNPUSimulator()
    
    try:
        simulator.run()
    # ctrl+c와 ctrl+d를 누르면 프로그램 종료
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다\n")

if __name__ == "__main__":
    main()  