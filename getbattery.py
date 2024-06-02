import socket

def get_battery_status(socket_path="/tmp/pisugar-server.sock"):
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(socket_path)
        client.sendall(b"get battery\n")
        response = client.recv(1024)
        client.close()
        return response.decode('utf-8')
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    status = get_battery_status()
    print(status)
