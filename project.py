from os import stat
import math
import random

import operator as op
from functools import reduce
from re import S
import timeit

###Coordinate System
class Cell:
    def __init__(self, state,sector,type,root,value):
            self.state = state
            self.sector=sector
            self.type=type
            self.root=root
            self.value=value
            self.neighbours=[]
            self.level=None
            self.signal=[]
            self.children=[]

#basic tiling definition       
nullcell=Cell(None,None,None,None,None)
centralCell=Cell(0,0,0,0,0)
centralCell.level=0

##Populating a sector
def constructnewlevel(inlist,p,q):
    # print("created a level")

    lastcurrlevel=inlist[-1].level
    for i in range(len(inlist)):
        if (inlist[i].level==lastcurrlevel):
            self=inlist[i]
            break

    if((q%2==0)or(q==3)):
        h=q/2
        value=inlist[-1].value
        while(self.level==lastcurrlevel):
            #Type s0
            if(self.type==0):
                #type 3 nodes
                value=value+1
                for i in range((p-3)*(h-1)):
                    self.children.append(Cell(0,self.sector,0,self,value))
                    value=value+1
                #type 2 node
                self.children.append(Cell(0,self.sector,1,self,value))

                for nodes in self.children:
                        nodes.level=self.level+1
                        inlist.insert(nodes.value,nodes)

                self=inlist[self.value+1]

            if (self.type==1):
                #type 3 nodes
                value=value+1
                r=(p-2)*(h-1)
                for i in range(r-2):
                    self.children.append(Cell(0,self.sector,0,self,value))
                    value=value+1
                
                #type 2 nodes
                self.children.append(Cell(0,self.sector,1,self,value))

                for nodes in self.children:
                        nodes.level=self.level+1
                        inlist.insert(nodes.value,nodes)

                self=inlist[self.value+1]

    elif(q%2!=0):

        h=q//2
        value=inlist[-1].value
        while(self.level==lastcurrlevel):
            #types0
            if(self.type==0):
                #s0-children
                value=value+1
                for i in range((p-3)*(h-1)):
                    self.children.append(Cell(0,self.sector,0,self,value))
                    value=value+1 

                #s1-child
                self.children.append(Cell(0,self.sector,2,self,value))
                value=value+1

                #s2-child
                self.children.append(Cell(0,self.sector,1,self,value))

                for nodes in self.children:
                    nodes.level=self.level+1
                    inlist.insert(nodes.value,nodes)

                self=inlist[self.value+1]

            elif(self.type==2):

                # print("here too")
                #s0-children
                value=value+1
                for i in range((p-3)*(h-1)):
                    self.children.append(Cell(0,self.sector,0,self,value))
                    value=value+1
                    
                #s2-child
                self.children.append(Cell(0,self.sector,1,self,value))

                for nodes in self.children:
                    nodes.level=self.level+1
                    inlist.insert(nodes.value,nodes)

                self=inlist[self.value+1]

            elif(self.type==1):
                #s0-children
                value=value+1
                r=(p-2)*(h-1)
                for i in range(r-2):
                    self.children.append(Cell(0,self.sector,0,self,value))
                    value=value+1
                
                #s2-child
                self.children.append(Cell(0,self.sector,1,self,value))

                for nodes in self.children:
                    nodes.level=self.level+1
                    # print(nodes.value,"hey")
                    inlist.insert(nodes.value,nodes)
 
                self=inlist[self.value+1]

    return inlist            

# Neighbours list creation
def neighbourupdate(list,p,q):
    for  i in range(len(list)):
        for obj in list[i]:
            #starting node
            if(obj.value==1):
                for nodes in obj.children:
                    obj.neighbours.append(nodes)
                obj.neighbours.append(centralCell)
                k=(p-(len(obj.children)+1))
                if(i==(p-1)):
                    addval=1
                    for b in range(k):
                        obj.neighbours.append(list[0][addval])
                        addval=addval+1
                else:
                    addval=1
                    for b in range(k):
                        obj.neighbours.append(list[i+1][addval])
                        addval=addval+1
                    #print("Neighbours filled for "+ str(obj.value) +"one if loop in sector" + str(i) )

                #left branch
            elif(obj.value==obj.root.children[0].value):
                for nodes in obj.children:
                    obj.neighbours.append(nodes)
                obj.neighbours.append(centralCell)
                k=(p-len(obj.children)+1)
                if(i==0):
                    addval=obj.root.value
                    for r in range(q//2):
                        obj.neighbours.append(list[p-1][addval])
                        addval=addval-1
                    addval=obj.root.value
                    for r in range(q-(q//2)):
                        obj.neighbours.append(list[p-1][addval])
                        addval=addval+1
                else:
                    addval=obj.root.value
                    for r in range(q//2):
                        obj.neighbours.append(list[i-1][addval])
                        addval=addval-1
                    addval=obj.root.value
                    for r in range(q-(q//2)):
                        obj.neighbours.append(list[i-1][addval])
                        addval=addval+1
                k=k-q
                if(k>0):
                    if(i==0):
                        addval=obj.children[-1].value
                        for r in range(q//2):
                            obj.neighbours.append(list[p-1][addval])
                            addval=addval+1
                    else:
                        addval=obj.children[-1].value
                        for r in range(q//2):
                            obj.neighbours.append(list[i-1][addval])
                            addval=addval-1
                    obj=obj.children[0]   
                else: 
                    #print("Neighbours partially filled for "+str(obj.value)+"left branch loop")
                    break
                        
                #right branch
            elif(obj.value==4):
                while(obj.value<len(list[i])):
                    obj.neighbours.append(list[i][obj.root.value])
                    obj.neighbours.append(list[i][obj.value-1])
                    if(i==6):
                        if((obj.value)+1<len(list[i])-1):
                          obj.neighbours.append(list[0][obj.value+1])
                        obj.neighbours.append(list[0][obj.root.value+1])
                    else:
                        if((obj.value)+1<len(list[i])-1):
                          obj.neighbours.append(list[i+1][obj.value+1])
                        obj.neighbours.append(list[i+1][obj.root.value+1])
                    if(obj.right is not None):  
                        obj.neighbours.append(list[i][(obj.left.value)])
                        obj.neighbours.append(list[i][(obj.right.value)])
                        obj.neighbours.append(list[i][(obj.middle.value)])
                        #print("Neighbours filled for "+ str(obj.value)+ "by right branch loop")
                        obj=obj.right
                    else:
                        #print("Neighbours partially filled for "+str(obj.value)+"by right branch loop")
                        break          
#                 #2-nodes
            elif((obj.type==2) and (len(obj.neighbours)==0)):                
                obj.neighbours.append(list[i][(obj.root.value)])
                obj.neighbours.append(list[i][(obj.root.value)-1])
                obj.neighbours.append(list[i][(obj.value)-1])
                if(obj.right is not None):
                    obj.neighbours.append(list[i][(obj.left.value)])
                    obj.neighbours.append(list[i][(obj.right.value)])
                    if(int(obj.right.value)+1<len(list[i])):
                        obj.neighbours.append(list[i][(obj.right.value+1)])
                obj.neighbours.append(list[i][(obj.value)+1])
                #print("Neighbours filled for "+ str(obj.value)+ "mid 2 loop")                   
#                 #3-nodes
            elif((obj.type==3) and (len(obj.neighbours)==0)):               
                obj.neighbours.append(list[i][obj.root.value])
                obj.neighbours.append(list[i][obj.value-1])
                obj.neighbours.append(list[i][obj.value+1])
                if(obj.right is not None):
                    obj.neighbours.append(list[i][(obj.left.value)])
                    obj.neighbours.append(list[i][(obj.right.value)])
                    obj.neighbours.append(list[i][(obj.middle.value)])
                    if(int(obj.right.value)+1<len(list[i])):
                        obj.neighbours.append(list[i][(obj.right.value)+1])
                #print("Neighbours filled for "+ str(obj.value) + "mid 3 loop") 
#      #central cell update
    return list   

#Defining p,q values
p=5
q=5

list=[]
for i in range(p):
    listin=[nullcell]
    start=Cell(0,i,0,None,1)
    start.level=1
    listin.append(start)
    for j in range(10):
      listin=constructnewlevel(listin,p,q)
    list.append(listin)

# list=neighbourupdate(list,p,q)

#Game of Life
statematrix=[]
list[0][1].state=1
list[0][5].state=1
list[0][7].state=1
list[0][8].state=1
list[0][9].state=1
for i in range(len(list)):
    statematrix.append([])
    for j in range(1,len(list[i])):
        statematrix[i].append(list[i][j].state)
# print("At Time = 0")
# print(statematrix[0])
prevstatematrix=statematrix
for i in range(len(statematrix)):
    for j in range(len(statematrix[i])):
        ncount=0
        for obj in list[i][j+1].neighbours:
            if(prevstatematrix[obj.sector][obj.value-1]==1):
                ncount=ncount+1
        if(prevstatematrix[i][j]==0):
            if(ncount==3):
                statematrix[i][j]=1
        elif(prevstatematrix[i][j]==1):
            if(ncount<2):
                statematrix[i][j]=0
            elif(ncount==2 or ncount==3):
                statematrix[i][j]=1
            elif(ncount>3):
                statematrix[i][j]=0
for i in range(len(list)):
    for j in range(1,len(list[i])):
        list[i][j].state=statematrix[i][j-1]

def changestate(i,j,tostate):
    statematrix[i][j-1]=tostate
    list[i][j].state=tostate
    return None

# print("At Time = 1")
# print(statematrix[0])

print("The neighbourhood has been set appropriately")
print("_______________________________")

# #Marking algorithm
#States Key:
# State 0: Dead cells
# State 1: Marking of n in SE/The n-level binary tress of SW quarter/Mark of s-statements/Mark of the 3 variables for each statement if positive/Active s OR value of 0
# State 2: Mark of the 3 variables for each statement if negative/ Active s OR value of 1

#Clear-out
for i in range(len(list)):
  for obj in list[i]:
    obj.state=0


#Getting the statement from user
inputstart = [[1,2,3],[-1,2,4],[1,-2,3]]
s=len(inputstart)
n=4
time=0


# for i in range(p):
#     for j in range(s+n):
#             list[i]=constructnewlevel(list[i],p,q)
print("This 3-SAT problem has " +str(n)+ " variables and is set in a {" + str(p) +"," +str(q)+"} tessellation.")
#Representation of n in the south-eastern quarter
r=list[p-1][1]
for i in range(n):
    r.state=1
    r=r.children[0]    


#Developing n-level in the SW-quarter treee from the n-rep in the SE quarter
def genNlevels(n):
    activenodes=[1]
    while (list[0][activenodes[0]].level<n):
        activenodes.append(list[0][activenodes[0]].children[0].value)
        activenodes.append(list[0][activenodes[0]].children[1].value)
        activenodes.remove(list[0][activenodes[0]].value)
    return activenodes

#Note: The value of r is now the last node pointing at value of n
# r=r.root
#If there is a number, the central cell takes a proceed state
list[p-1][0].state=list[p-1][1].state

#It starts from r until 1. If it is not at 1, it generates for levels until there, and then if it is at 1, it activates for 1 as well.
#
k=0
while(list[p-1][0].state==1):
    if(r.value!=1):
        r.state=0
        time=time+1
        leafnodes=genNlevels(k+1)
        for nodes in (leafnodes):
            list[0][nodes].state=1
        k=k+1
        r=r.root
    elif(r.value==1):
        time=time+1
        list[0][1].state=2
        leafnodes=genNlevels(i+1)
        for nodes in (leafnodes):
            list[0][nodes].state=1
        list[p-1][0].state=0
        break
def sendsignal(i):
    list[0][i].children[0].signal=list[0][i].signal
    list[0][i].children[1].signal=list[0][i].signal
    list[0][i].signal=[]
    return None
 
# #Marking s statements start
start=list[0][1].children[-1]
s=len(inputstart)
absinputstart=[]

# for j in range (32):
#     print(list[0][j].value,list[0][j].type,len(list[0][j].children))



for i in range(s):
    time=time+1
    r=[]
    for num in inputstart[i]:
        r.append(abs(num))
    absinputstart.append(r)


time=time+(q//2)
for i in range(s):
    start.state=1
    loc=start
    while((loc.level-start.level)<=abs(inputstart[i][-1])):
        if(((loc.level-start.level) in absinputstart[i]) and ((loc.level-start.level) in inputstart[i])):
            loc.state=1
        elif(((loc.level-start.level) in absinputstart[i]) and (-(loc.level-start.level) in inputstart[i])):
            loc.state=2
        loc=loc.children[0]
    start=start.children[-1]


#Check


# #Solving
start=list[0][1].children[-1]
for i in range(s):
    time=time+1
    loc=start.children[0]

    while((loc.level-start.level)<=n):
        if(loc.state==1 or loc.state==2):
            k=loc.level-start.level
            currLevel=1
            while(currLevel<=(n+1)):
                nodesatn=genNlevels(currLevel)
                if(currLevel<(n)):
                    if(len(nodesatn)==pow(2,k-1)):
                        for i in nodesatn:
                            if(loc.state==1):
                                list[0][i].children[0].signal.append(0)
                                list[0][i].children[1].signal.append(1)
                                list[0][i].signal=[]
                            elif(loc.state==2):
                                list[0][i].children[0].signal.append(1)
                                list[0][i].children[1].signal.append(0)
                                list[0][i].signal=[]
                    else:
                        for i in nodesatn:
                           sendsignal(i)
                elif(currLevel==(n)):
                    if(k!=n):
                        for i in nodesatn:
                            list[0][i].children[0].signal.extend(list[0][i].signal)
                            list[0][i].children[1].signal.extend(list[0][i].signal)
                            list[0][i].signal=[]
                    elif(k==n):
                        for i in nodesatn:
                            if(loc.state==1):
                                    list[0][i].children[0].signal.append(0)
                                    list[0][i].children[1].signal.append(1)
                                    list[0][i].signal=[]
                            elif(loc.state==2):
                                list[0][i].children[0].signal.append(1)
                                list[0][i].children[1].signal.append(0)
                                list[0][i].signal=[]
                elif(currLevel==n+1):
                    # for o in nodesatn:
                        # print(list[0][o].signal)
                    break
                currLevel=currLevel+1
                time=time+1
        loc=loc.children[0]
    
    for obj in genNlevels(n+1):
        list[0][obj].state=1
    
    for node in nodesatn:
        # print(nodesatn)
        k=list[0][node].signal[0]
        for l in range(len(list[0][node].signal)):
            k=k or list[0][node].signal[l]
        if(list[0][node].state==1):
            if(k==0):
                list[0][node].state=1
            elif(k==1):
                list[0][node].state=2
        elif(list[0][node].state==1 or list[0][node].state==2):
            # print("Enter C")
            if(list[0][node].state==1):
                r=0
            elif(list[0][node].state==2):
                r=1
            if((k and r)==0):
                list[0][node].state=1
            elif((k and r)==1):
                list[0][node].state=2
        list[0][node].signal=[]

    start=start.children[-1]



currLevel=currLevel-1

while(currLevel>=1):
    time=time+1
    nodesgroup=genNlevels(currLevel)
    for node in nodesgroup:
        l=list[0][node].children[0].state
        r=list[0][node].children[1].state
        # print(l)
        if(l==1):
            l=0
        elif(l==2):
            l=1
        if(r==1):
            r=0
        elif(r==2):
            r=1
        val=l or r
        if(val==1):
            list[0][node].state=1
        elif(val==0):
            list[0][node].state=2
    currLevel=currLevel-1

list[0][0].state=list[0][1].state
time=time+1

if(list[0][0].state==1):
    print("There exists a solution for this 3-SAT")
elif(list[0][0].state==2):
    print("There exists no solution for this 3-SAT")

print("Time taken by the CA to solve is " + str(time))


