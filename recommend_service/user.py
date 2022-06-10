from recommend_service.item import get_item_num
import os


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
    

def user_vote(userID, rate):
    userNum=get_user_num(userID)
    
    flag = 0
    
    voteFile = "../recommend_service/vote.dat"
    userWatchFile = "../recommend_service/user_watch/{0}.dat".format(userNum)
    
    if not os.path.exists(userWatchFile):
        return
    
    fuW = open(userWatchFile,"r")
    
    userWatcheds = fuW.readlines()
    
    for itemNum in userWatcheds:
        try:
            f = open(voteFile,"r")
            
            text = f.readlines()
            
            for t in text:
                a = t.split()
                
                if (str(a[0]) == userNum and str(a[1]) == itemNum.rstrip() and str(a[0]) != '\n'):
                    
                    b = text.index("{0} {1} {2}\n".format(a[0], a[1], a[2]))
                    
                    text[b] = "{0} {1} {2}.\n".format(str(userNum), itemNum.rstrip(), str(rate))
                    
                    flag = 1
                    
                    break
        finally:
            f.close()
            
        if flag == 0:
            try:
                f=open(voteFile,"a+")
                
                result = "{0} {1} {2}.\n".format(str(userNum), itemNum.rstrip(), str(rate))
                
                f.write(result)
            finally:
                f.close()
        else:
            try:
                f=open(voteFile,"w")
                
                f.writelines(text)
            finally:
                f.close()