from drone_commands import *

# 각 드론의 명령을 해당 기능에 매핑합니다.
command_functions = {
    'TKOFF': take_off,      # 이륙
    'UPWAR': move_up,       # 드론 상승
    'DOWAR': move_down,     # 드론 하강
    'FOWAR': move_forward,  # 드론 전진
    'BACK_': move_backward, # 드론 후진
    'LEFT_': move_left,     # 드론 좌측으로 이동
    'RIGHT': move_right,    # 드론 우측으로 이동
    'TURNL': turn_left,     # 드론 좌측으로 회전
    'TURNR': turn_right,    # 드론 우측으로 회전
    'RHOME': return_home,   # 리턴 홈
    'FFLIP': flip_front,    # 앞으로 플립
    'BFLIP': flip_back,     # 뒤로 플립
    'LFLIP': flip_left,     # 왼쪽으로 플립
    'RFLIP': flip_right,    # 오른쪽으로 플립
    'LAND_': land,          # 착륙
    'QUIT_': quit_program,  # 연결 종료
}
