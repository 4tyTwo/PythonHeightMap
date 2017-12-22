import random as rnd
import numpy as np
from PIL import Image,ImageDraw

def diamond_displace(hmap,i,j,half_step,roughness):
    #углы ромба
    ul = hmap[i-half_step,j-half_step]
    ur = hmap[i-half_step,j+half_step]
    ll = hmap[i+half_step,j-half_step]
    lr = hmap[i+half_step,j+half_step]
    avg = (ul+ur+ll+lr)/4.0
    return (1-roughness)*avg + roughness*rnd.uniform(0,1)

def square_displace(hmap,x_size,y_size,i,j,half_step,roughness):
    total = 0.0
    divide_by = 4
    #Проверка существования клеток
    if i-half_step >=0:
        total += hmap[i-half_step,j]
    #elif hmap[abs(i-half_step)-1,y_size-j-1] != -1:
    #else:
     #   total += hmap[abs(i-half_step)-1,y_size-j-1]
    else:
        total+=0

    if i+half_step < x_size:
        total += hmap[i+half_step,j]
   # elif hmap[x_size - abs(i-half_step),y_size-j-1]:
    #    total += hmap[x_size - abs(i-half_step),y_size-j-1]
    else:
        total += 0

    if j-half_step >=0:
        total += hmap[i,j-half_step]
    #elif hmap[i,y_size+(j-half_step)]!= -1:
    #else:
     #   total += hmap[i,y_size+(j-half_step)]
    else:
        total += 0;

    if j+half_step < y_size:
        total += hmap[i,j+half_step]
    #elif hmap[i,(j+half_step)%y_size] != -1:
    #else:
     #   total += hmap[i,(j+half_step)%y_size]
    else:
        total += 0

    avg = total/divide_by

    return roughness*rnd.uniform(0,1)+(1-roughness)*avg

def diamond(hmap,x_size,y_size,step_size,roughness,step):
    half_step = int(step_size/2)
    quater_step = int(step_size/4)
    x_steps = range(quater_step,x_size,half_step)
    y_steps = range(quater_step,y_size-1,half_step)
    for i in x_steps:
        for j in y_steps:
            hmap[i,j] = diamond_displace(hmap,i,j,quater_step,roughness)


def square(hmap,x_size,y_size,step_size,roughness):
    half_step = int(step_size/2)
    quater_step = int(step_size/4)
    steps_x_vert = range(quater_step,x_size,half_step)
    steps_y_vert = range(0,y_size,half_step)
    steps_x_horiz = range(0,x_size,half_step)
    steps_y_horiz = range(int(half_step/2),y_size,half_step)
    for i in steps_x_horiz:
        for j in steps_y_horiz:
            hmap[i,j] = square_displace(hmap,x_size,y_size,i,j,quater_step,roughness)
    for i in steps_x_vert:
        for j in steps_y_vert:
            hmap[i,j] = square_displace(hmap,x_size,y_size,i,j,quater_step,roughness)


def diamond_square(x_size,y_size,roughness):
    #Высота меняется от 0 до 1
    hmap = np.zeros((x_size, y_size), dtype='float')
    #hmap = hmap-1.0
    #Задаем высоты угловых точек
    hmap[0,0] = rnd.uniform(0,1)
    hmap[0,y_size-1] = rnd.uniform(0,1)
    hmap[x_size-1,0] = rnd.uniform(0,1)
    hmap[x_size-1,y_size-1] = rnd.uniform(0,1)
    hmap[0,int((y_size-1)/2)] = rnd.uniform(0,1)
    hmap[x_size-1,int((y_size-1)/2)] = rnd.uniform(0,1)
    for i in range(14):
        if x_size == 2**i + 1:
            iterations = i
            break
    for i in range(iterations):
        curr_rough = roughness**i
        step_size = int((y_size-1)/(2**i))
        diamond(hmap,x_size,y_size,step_size,curr_rough,i)
        square(hmap,x_size,y_size,step_size,curr_rough)
    return hmap


print("Input size: ")
x_size,y_size =map(int,input().split())
print("Input rougness: ")
roughness = float(input())
hmap = diamond_square(x_size,y_size,roughness)
img = Image.new('RGB',(y_size,x_size),(255,255,255))
imgDrawer = ImageDraw.Draw(img)
hmap = hmap**2
avg = hmap.mean()
for _i in range(x_size):
    for _j in range(y_size):
        if hmap[_i,_j] >=avg*1.07:
            color = (0, int(255 - hmap[_i,_j]*255), 0)
        else:
            color = (0, 0, int(255 - hmap[_i,_j]*255))
        imgDrawer.point((_j, _i), color)
img.save("map.jpg")