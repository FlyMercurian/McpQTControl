import socket, json

def send_command(cmd):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8088))
    
    message = {
        "id": "test_001",
        "method": "execute", 
        "params": {"command": cmd}
    }
    
    sock.send((json.dumps(message) + '\n').encode())
    response = sock.recv(1024).decode()
    sock.close()
    return response

# 测试
print(send_command("login:admin:123456"))
#print(send_command("testbutton"))
# print(send_command("getstate"))