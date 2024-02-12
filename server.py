import socket
import os
import threading
def start_ftp_server(conn,address,host='localhost'):
    
    fpath = conn.recv(8589934592).decode()


    if fpath=='GET FILE DETAILS':
        
        path = r'D:/3RD SEMESTER/DATA STRUCTURES AND ALGORITHM/PROJECT/SERVER'
        data = os.listdir(path)
        data='--'.join(data)

        conn.send(data.encode())
        conn.close()
        return

    if fpath.startswith('UPLOAD FILE-'):

        path = r'D:/3RD SEMESTER/DATA STRUCTURES AND ALGORITHM/PROJECT/SERVER/'
        
        conn.send('SEND_FILE'.encode())

        rvd = conn.recv(2048)

        print(rvd)
        
        data=rvd

        while(True):
            rvd = conn.recv(2048)
            if not rvd:
                break
            data = data+rvd

        print(len(data))

        fname = fpath.split('UPLOAD FILE-')[-1]

        print(path+fname)

        f = open(path+fname,'wb')
        f.write(data)

        f.close()  

        return
    
    fd = 'D:/3RD SEMESTER/DATA STRUCTURES AND ALGORITHM/PROJECT/SERVER/'+fpath

    with open(fd,'rb') as f:
        data = f.read()

    for i in range(0,len(data),2048):
        conn.send(data[i:i+2048])

    conn.close()

def start():
    host='192.168.11.152'

    server_socket = socket.socket()
    print(host)


    server_socket.bind((host,2000))
    print('Server Ready')

    server_socket.listen(10)
    conn,addr = server_socket.accept()
    t1 = threading.Thread(target=start_ftp_server,args=(conn,addr))
    t1.start()


if __name__ == "__main__":
    while True:
        start()
