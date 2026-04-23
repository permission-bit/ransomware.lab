import socket

def find(ip: str, port: int = 22, timeout: float = 2.0):

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            
            status = s.connect_ex((ip, port))

            if status == 0:
                return "open"
            
            else:
                return "closed"
    except Exception as e:
        return e
    
print(find("127.0.0.1", 22))