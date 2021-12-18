from django.shortcuts import render,HttpResponse ,redirect
import numpy as np


def gethidden(data,x,y,hidden_data,a=[]):
    if data[x][y]!=0:
        if data[x][y]==10:
            hidden_data=np.ones(data.shape,dtype="int")
            return hidden_data
        else:
            hidden_data[x][y]=1
            return hidden_data
    else:
        hidden_data[x][y]=1   
        rangeX = range(0, data.shape[0])
        rangeY = range(0, data.shape[1]) 
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                (newX, newY) = (x+dx, y+dy) 
                if (newX in rangeX) and (newY in rangeY) and (x,y) != (newX,newY) and ((newX, newY) not in a):
                    a.append((newX, newY))
                    gethidden(data,newX,newY,hidden_data,a)
    return hidden_data  


def create_array(request,row,col):
    data=np.zeros((row,col),dtype="int")
    hidden_data=np.zeros((row,col),dtype="int")
    request.session["data"]=data.tolist()
    request.session["hidden_data"]=hidden_data.tolist()
    return data 


def adjcent_flag_count(matrix, position):
    count=0
    rangeX = range(0, matrix.shape[0])
    rangeY = range(0, matrix.shape[1]) 
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            (newX, newY) = (position[0]+dx, position[1]+dy)       
            if (newX in rangeX) and (newY in rangeY) and position != (newX,newY) :
                if matrix[newX,newY]==10:
                    count+=1
    return count



def generate_minespace(data):
    for i in range(0, data.shape[0]):
        for j in range(0, data.shape[1]):
            if data[i][j]!=10:
                data[i][j]=adjcent_flag_count(data,(i,j))



def home(request):
    if request.method=="POST":
        row = int(request.POST.get("row"))
        col = int(request.POST.get("col"))
        data=create_array(request,row,col)
        return render(request,"placebomb.html",{"row":range(row),"col":range(col)})
    else:
        return render(request,"home.html")




def placebomb_random(request):
    row = int(request.POST.get("row"))
    col = int(request.POST.get("col"))
    data=create_array(request,row,col)
    data=np.random.choice([0,0,0,0,10],(row,col))
    hidden_data=np.array(request.session["hidden_data"])
    print(data.size)
    generate_minespace(data)
    winning_matrix=np.where(data==10,0,data)
    request.session["winning_matrix"]=winning_matrix.tolist()
    request.session["data"]=data.tolist()
    display_data=np.multiply(data,hidden_data)
    return render(request,"gamepage.html",{"display_data":display_data,"hidden_data":hidden_data,"row":range(data.shape[0]),"col":range(data.shape[1])})
    


def placebomb(request):
    data=np.array(request.session["data"])
    hidden_data=np.array(request.session["hidden_data"])
    if request.method=="POST":
        for i in  list(request.POST.keys())[1:]:
            x,y= map(int,i.split(" "))
            data[x][y]=10
        generate_minespace(data)
        winning_matrix=np.where(data==10,0,data)
        request.session["winning_matrix"]=winning_matrix.tolist()
        request.session["data"]=data.tolist()
        display_data=np.multiply(data,hidden_data)
        return render(request,"gamepage.html",{"display_data":display_data,"hidden_data":hidden_data,"row":range(data.shape[0]),"col":range(data.shape[1])})


def playgame(request):
    data=np.array(request.session["data"])
    hidden_data=np.array(request.session["hidden_data"])
    winning_matrix=np.array(request.session["winning_matrix"])
    if request.method == "POST":
        try:
            i,j=map(int,request.POST.get("key").split("\xa0"))
        except:
            print("no key")
        else:
            hidden_data = gethidden(data,i,j,hidden_data,a=[])   
        request.session["hidden_data"]=hidden_data.tolist()
        display_data=np.multiply(data,hidden_data)
        if (display_data==winning_matrix).all():
            return render(request,"gamepage.html",{"display_data":display_data,"hidden_data":hidden_data,"row":range(data.shape[0]),"col":range(data.shape[1]),"message":"You Win!"})
        elif (display_data==data).all():
            return render(request,"gamepage.html",{"display_data":display_data,"hidden_data":hidden_data,"row":range(data.shape[0]),"col":range(data.shape[1]),"message":"Game Over!"})
        else:
            return render(request,"gamepage.html",{"display_data":display_data,"hidden_data":hidden_data,"row":range(data.shape[0]),"col":range(data.shape[1])})
    else:
        return redirect("/")




