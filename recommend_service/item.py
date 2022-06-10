def add_new_item(itemId):
    if get_item_num(itemId) != 0:
        return
    
    try:
        f=open("../recommend_service/main_item.dat","r")
        text=f.readlines()
        size=len(text)
    finally:
        f.close()
    try:
        f=open("../recommend_service/main_item.dat","a+")
        result=str(size+1)+" "+itemId+"\n"
        f.write(result)
    finally:
        f.close()

def get_item_num(itemId):
    try:
        f=open("../recommend_service/main_item.dat","r")
        text=f.readlines()
        for t in text:
            a=t.split()
            if (a[1]==itemId):
                return(a[0])
        return 0
    finally:
        f.close()