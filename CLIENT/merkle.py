import hashlib

class merkle:

    def hashfunc(self,val):
        return hashlib.sha256(val.encode()).hexdigest()

    def generatetree(self,chunks):
        if len(chunks)==0:
            return None
        
        if len(chunks)%2!=0:
            chunks.append(chunks[-1])

        hashed = [self.hashfunc(x) for x in chunks]

        tree=[]
        tree.append(hashed)

        while(len(hashed))>1:
            if len(hashed)%2!=0:
                hashed.append(hashed[-1])
            
            new_hashed = [self.hashfunc(hashed[i]+hashed[i+1]) for i in range(0,len(hashed),2)]
            hashed=new_hashed
            tree.append(hashed)
        
        return hashed
    
if __name__=='__main__':
    print('DATA_DONE'.encode())
            



