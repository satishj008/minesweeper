from django.shortcuts import render,HttpResponse ,redirect
import numpy as np

hidden_data=np.empty((1,1))

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


def create_array(row,col):
    global data
    global hidden_data
    data=np.zeros((row,col),dtype="int")
    hidden_data=np.zeros((row,col),dtype="int")
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

def generate_minespace():
    for i in range(0, data.shape[0]):
        for j in range(0, data.shape[1]):
            if data[i][j]!=10:
                data[i][j]=adjcent_flag_count(data,(i,j))



def home(request):
    if request.method=="POST":
        row = int(request.POST.get("row"))
        col = int(request.POST.get("col"))
        array=create_array(row,col)
        return render(request,"placebomb.html",{"row":range(row),"col":range(col)})
        return render(request,"placebomb.html",{"array":array})
        return render(request,"showmine.html",{"array":array})
    else:
        return render(request,"home.html")


def placebomb(request):
    global data
    if request.method=="POST":
        for i in  list(request.POST.keys())[1:]:
            print(i)
            x,y= map(int,i.split(" "))
            data[x][y]=10
        generate_minespace()
        print(data)
        print(hidden_data)
        display_data=np.multiply(data,hidden_data)
        # print(display_data)
        return render(request,"gamepage.html",{"display_data":display_data,"hidden_data":hidden_data,"row":range(data.shape[0]),"col":range(data.shape[1])})


def playgame(request):
    global data
    global hidden_data
    if request.method == "POST":
        print(request.POST.get("key"))
        i,j=map(int,request.POST.get("key").split("\xa0"))
        print(i,j)
        hidden_data = gethidden(data,i,j,hidden_data,a=[])
        print(hidden_data)
        display_data=np.multiply(data,hidden_data)

        return render(request,"gamepage.html",{"display_data":display_data,"hidden_data":hidden_data,"row":range(data.shape[0]),"col":range(data.shape[1])})
    else:
        return redirect("/")




