import socket
def send_data(x, y, z, ip, port):
    datagram = f"[X:{x};Y:{y};Z:{z};A:0;ID:1;ATTR:0]"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    sock.sendto(datagram.encode(), (ip, port))
        
