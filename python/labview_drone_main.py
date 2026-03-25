from drone_commands import drone, connect_drone, disconnect_drone
from command_mapping import command_functions
from time import sleep
import socket
import threading as thr
import keyboard as kb

# 스레드 제어용 ​​전역 변수
stop_threads = False

def recv_exact(conn, size):
    data = b""

    while len(data) < size:
        packet = conn.recv(size - len(data))
        if not packet:
            raise ConnectionError("클라이언트 연결이 종료됨")
        data += packet

    return data

# 비상착륙 스레드 함수
def emergency_landing():
    global stop_threads

    while not stop_threads:
        try:
             if kb.is_pressed('space'):
                print("[비상] 스페이스 입력 감지")
                drone.sendLanding()
                sleep(1)
                drone.sendLanding()
                print("[비상] 비상착륙 완료")
                stop_threads = True
                break
        except Exception as e:
            print(f"[비상착륙 스레드 에러] {e}")

        sleep(0.1)  # CPU 과부하 방지 위해 짧은 대기

def main():
    global stop_threads

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 8087))
    server.listen(5)

    print("[서버] localhost:8087 에서 대기 중")
    connect_drone()

    e_thr = thr.Thread(name="emergency", target=emergency_landing, daemon=True)
    e_thr.start()

    try:
        while not stop_threads:
            conn = None
            addr = None

            try:
                conn, addr = server.accept()
                print(f"[연결] 클라이언트 접속: {addr}")

                cmnd = recv_exact(conn, 5).decode().strip()
                print(f"[수신] 명령어: {cmnd}")

                if cmnd in command_functions:
                    command_functions[cmnd]()
                    conn.sendall(cmnd.encode())
                    print(f"[응답] {cmnd} 전송 완료")

                    if cmnd == 'QUIT_':
                        print("[서버] 종료 명령 수신")
                        stop_threads = True
                        break
                else:
                    print(f"[경고] 알 수 없는 명령어: {cmnd}")
                    conn.sendall(b'ERROR')
                    print("[응답] ERROR 전송 완료")

            except ConnectionError:
                print("[연결] 클라이언트가 명령 처리 후 연결을 종료했습니다.")
            except Exception as e:
                print(f"[명령 처리 오류] {e}")
            finally:
                if conn is not None:
                    try:
                        conn.close()
                        if addr is not None:
                            print(f"[연결] 클라이언트 연결 종료: {addr}")
                    except Exception:
                        pass

    except Exception as e:
        print(f"[서버 오류] {e}")

    finally:
        stop_threads = True
        disconnect_drone()
        server.close()
        print("[서버] 종료 완료")    

if __name__ == "__main__":
    main()