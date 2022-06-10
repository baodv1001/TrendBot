def add_new_user(userId):
    if get_user_num (userId) != 0:
        return
    
    try:
        f=open("../recommend_service/main_user.dat","r")
        text=f.readlines()
        size=len(text)
    finally:
        f.close()
    try:
        f=open("../recommend_service/main_user.dat","a+")
        text=f.readline()
        result=str(size+1)+" "+str(userId)+" \n"
        f.write(result)
    finally:
        f.close()
        
def get_user_num(userId):
    try:
        f=open("../recommend_service/main_user.dat","r")
        text=f.readlines()
        for t in text:
            a=t.split()
            if (a[1]==str(userId)):
                return(a[0])
        return 0
    finally:
        f.close()

def user_watched(userNum, itemNum):
    try:
        userWatchFilePath = "../recommend_service/user_watch/{0}.dat".format(userNum)
        
        f=open(userWatchFilePath,"a+")
        
        result=str(itemNum) + "\n"
        
        f.write(result)
    finally:
        f.close()

def is_watched(userNum, itemNum):
    try:
        userWatchFilePath = "../recommend_service/user_watch/{0}.dat".format(userNum)
        
        f=open(userWatchFilePath,"r")
        
        text=f.readlines()
        
        for t in text:
            if str(itemNum) == str(t):
                return True
        return False
    finally:
        return False
