from time import sleep
from e_drone.drone import Drone
from e_drone.protocol import FlightEvent

# 드론 초기화 전역 변수
drone = Drone()
DRONE_PORT = "COM4"  # 드론 포트 번호

def connect_drone():
    drone.open(DRONE_PORT)
    print(f"드론이 {DRONE_PORT} 포트에 연결되었습니다.")


def disconnect_drone():
    drone.close()
    print("드론 연결 종료")
    

def move(x=0, y=0, yaw=0, throttle=0, duration=2000, stop_duration=1000):
    drone.sendControlWhile(x, y, yaw, throttle, duration) # 이동 명령
    drone.sendControlWhile(0, 0, 0, 0, stop_duration)  # 이동 후 안정화 시간


def take_off():
    print("드론 이륙")
    drone.sendTakeOff()


def move_up():
    print("드론 상승")
    move(throttle=50)


def move_down():
    print("드론 하강")
    move(throttle=-50)


def move_forward():
    print("드론 전진")
    move(y=50)


def move_backward():
    print("드론 후진")
    move(y=-50)


def move_left():
    print("드론 좌측으로 이동")
    move(x=-50)


def move_right():
    print("드론 우측으로 이동")
    move(x=50)


def turn_left():
    print("드론 좌측으로 회전")
    move(yaw=30, duration=1500)


def turn_right():
    print("드론 우측으로 회전")
    move(yaw=-30, duration=1500)


def return_home():
    print("리턴 홈")
    drone.sendFlightEvent(FlightEvent.Return)


def flip_front():
    print("앞으로 플립")
    drone.sendFlightEvent(FlightEvent.FlipFront)


def flip_back():
    print("뒤로 플립")
    drone.sendFlightEvent(FlightEvent.FlipRear)


def flip_left():
    print("왼쪽으로 플립")
    drone.sendFlightEvent(FlightEvent.FlipLeft)


def flip_right():
    print("오른쪽으로 플립")
    drone.sendFlightEvent(FlightEvent.FlipRight)


def land():
    print("드론 착륙")
    drone.sendLanding()
    sleep(0.01)
    drone.sendLanding()
    sleep(0.01)

def quit_program():
    print(" 프로그램 종료")
    drone.sendLanding()
    sleep(0.01)
    drone.sendLanding()
    sleep(0.01)
