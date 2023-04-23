import numpy as np
import math
import matplotlib.pyplot as plt
import random
import sys
NUMBER_OF_DATA=1000
XMAX=100
YMAX=100
data=[]
percent_of_original=0.3

def function(x):
    return 3.8*x+205

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def set_random_points():
    points=[]
    for i in range(0,int(NUMBER_OF_DATA*0.05)):
        x_point=random.randrange(0,int(function(NUMBER_OF_DATA)/10))
        y_point=random.randrange(0,int(function(NUMBER_OF_DATA)/10))
        points.append({"x": x_point, "y": y_point})

    for i in range(0,int(NUMBER_OF_DATA)):
        x_point=i/10
       # x_point=i/10
        y=int(function(i))
        delta=random.randrange(-100,100)
        y_point=int((y+delta)/10)
        points.append({"x": x_point, "y": y_point})
    np.random.shuffle(points)
    return points

def set_random_subset(data):


    subset=[]
    used_numbers=random.sample(range(0,len(data)),int(len(data)*percent_of_original))
    for i in range(0,len(used_numbers)):
        subset.append(data[used_numbers[i]])




    return subset
def fit_linear_regression(data,model):

    for point in data:
        e=(point['y'] -(model['slope']*point['x']+model['intercept']))
        model['slope']=model['slope']+0.00001*point['x']*e
        model['intercept'] = model['intercept'] + 0.00001 * e

    return {"slope":model['slope'],"intercept":model['intercept']}
def distance(point,tempModel,data):
    x1=point['x']
    y1=point['y']
    x2=x1
    y2=tempModel['slope']*x2+tempModel['intercept']
    return math.sqrt((y1 - y2) ** 2 + (x1 - x2) ** 2)
def error(data,newModel):
    sum=0

    for point in data:
        sum=sum+(point['y'] -(newModel['slope']*point['x']+newModel['intercept']))**2

    return sum/(len(data))

def RANSAC(data):
    threshold=10
    k=NUMBER_OF_DATA*percent_of_original/3
    bestError=999999
    val = random.sample(range(0, len(data)), 2)
    val.sort(reverse=False)
    bestFit = fit_linear_regression(data,{"slope":random.randrange(-10,10),"intercept":random.randrange(-10,10)})
    for i in range(0,30):
        tempInliers=set_random_subset(data)
        tempInliersAdd=[]
        val = random.sample(range(0, len(tempInliers)), 2)
        val.sort(reverse=False)
        tempModel=fit_linear_regression(tempInliers,bestFit)
        for point in data:
            if point not in tempInliers:
                if distance(point,tempModel,tempInliers)<threshold:
                    tempInliersAdd.append(point)
        if len(tempInliersAdd)>k:
            newInline=[]
            newInline=tempInliersAdd+tempInliers
            val=random.sample(range(0,len(newInline)),2)
            val.sort(reverse=False)
            newModel=fit_linear_regression(newInline,tempModel)
            newModelError=error(newInline,newModel)


            if newModelError<bestError:
                bestError=newModelError
                print("best error")
                print(bestError)
                print("best fit")
                print(newModel)
                bestFit=newModel

                ploting(data,bestFit)


    return bestFit
def ploting(data,values):
    for i in range(0, len(data)):
        plt.plot(data[i]['x'],data[i]['y'],'.',color='0')

    x_points = [10, 90]
    y_points = [values['slope'] * x_points[0] + values['intercept'],values['slope'] * x_points[1] + values['intercept']]
    plt.plot(x_points, y_points)
    print(values)
    plt.show()
def main():
    data = set_random_points()
    values = RANSAC(data)
    ploting(data,values)


if __name__=='__main__':

    main()
