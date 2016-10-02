from sklearn.ensemble import RandomForestClassifier
import numpy as np
import random
X=[]
Y=[]
X1=[]
Y1=[]
with open("2members.txt") as f:
    lines=f.readlines()
l=lines
random.shuffle(l)
for line in l:
    line=line.rstrip()
    lst=line.split(',')
    X.append([float(each) for each in lst[:len(lst)-1]])
    Y.append(lst[-1])
count =0
#print len(X)
#print len(Y)
clf = RandomForestClassifier(n_estimators=100)
print "1st step done"
clf=clf.fit(X[:749],Y[:749])
print "2nd step done"
pre=clf.predict(X[749:])
print "3rd step done"
print "to be predicted: ",len(pre)
for i in range(len(pre)):
    if pre[i]==Y[i+749]:
        count +=1
    else:
        print pre[i],Y[i+749]
        
print "predicted: ",count



