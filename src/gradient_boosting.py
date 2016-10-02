from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import mean_squared_error
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
print len(X)
print len(Y)
clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,max_depth=1, random_state=0)
print "1st step done"
clf=clf.fit(X[:750],Y[:750])
print "2nd step done"
pre=clf.predict(X[750:])
print "3rd step done"
print "to be predicted: ",len(pre)
for i in range(len(pre)):
    if pre[i]==Y[i+750]:
        count +=1
    else:
        print pre[i],Y[i+750]
        
print "predicted: ",count

