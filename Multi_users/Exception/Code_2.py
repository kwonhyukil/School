import socket

try:
    print("10")

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    my_socket.connect(("127.0.0.1", 12345)) # 서버가 동작하지 않을 떄, 나의 네트워트가 문제가 있을 때때

    print((my_socket.recv(1024).decode('utf-8'))) # 연경이 비정상적으로 종료 되었을 때

except:
    print("소켓 예외 발생^^:;")
else:
    my_socket.sendall("OK".encode('utf-8'))

finally:
    my_socket.close()


print("종료")