import socket
import sys

# set arguments
server_ip = sys.argv[1]
server_port = sys.argv[2]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# request ip
try:
    while True:
        # What IP are you looking for?
        ip = input()
        s.sendto(ip.encode(), (server_ip, eval(server_port)))
        data, addr = s.recvfrom(1024)
        print(str(data)[2:-1])
        data, addr = s.recvfrom(1024)
except KeyboardInterrupt:
    # do nothing
    print()
finally:
    # closing socket
    s.close()
