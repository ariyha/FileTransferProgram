import socket 
from pathlib import Path
from merkle import merkle
import pickle
from cryptography.fernet import Fernet

def ftp_client_download(fname,host='127.0.0.1'):


    client_socket = socket.socket()

    client_socket.connect((host,2000))

    client_socket.send(fname.encode())

    rvd = client_socket.recv(2048)
    data=rvd

    while(True):
        rvd = client_socket.recv(2048)
        if not rvd:
            break
        data = data+rvd
    
    with open('C:/client_side/'+fname+'kye.bin','rb') as f:
        key = pickle.load(f)
        
    f2 = Fernet(key)

    data  = f2.decrypt(data)

    chunks=[]

    for i in range(0,len(data),128):
        chunks.append(str(data[i:i+128]))
    

    tree = merkle()
    k = tree.generatetree(chunks)
    print(k)

    with open('C:/client_side/'+fname+'.bin','rb') as f:
        k1 = pickle.load(f)    

    if k!=k1:
        return 'FILE_SEND_UNSUCCESFUL'


    dpath = str(Path.home()).replace('\\','/') +'/Downloads/'

    with open(dpath+fname,'wb') as f:
        f.write(data)

    client_socket.close()


def get_files(host='127.0.0.1'):
    client_socket = socket.socket()

    client_socket.connect((host,2000))

    client_socket.send('GET FILE DETAILS'.encode())

    data = client_socket.recv(8589934592).decode()

    return data.split('--')


def client_upload(fpath,host='localhost'):

    client_socket = socket.socket()


    client_socket.connect((host,2000))


    f = open(fpath,'rb')

    data = f.read()
 
    print(len(data))

    fname = fpath.split('\\')[-1]

    key = Fernet.generate_key()
    fernet = Fernet(key)

    chunks=[]

    for i in range(0,len(data),128):
        chunks.append(str(data[i:i+128]))


    tree = merkle()
    k = tree.generatetree(chunks)

    print(k)

    with open('C:/client_side/'+fname+'.bin','wb') as f:
        pickle.dump(k,f)
    
    with open('C:/client_side/'+fname+'kye.bin','wb') as f:
        pickle.dump(key,f)
    
    data = fernet.encrypt(data)

    val = 'UPLOAD FILE-'+fname
    
    while(True):

        client_socket.send(val.encode())

        msg = client_socket.recv(102400).decode()

        n=0

        if msg=='SEND_FILE':
            for i in range(0,len(data),2048):
                n+=1
                client_socket.send(data[i:i+2048])
            print(n)
            
            return
        else:
            continue


if __name__=='__main__':
    print(get_files())