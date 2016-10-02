from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn import svm
from sklearn.ensemble import GradientBoostingClassifier
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
#clf1 = LogisticRegression(random_state=1)
#clf2 = RandomForestClassifier(random_state=1)
clf1 = RandomForestClassifier(n_estimators=100)
clf3 = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,max_depth=1, random_state=0)
clf2 = svm.SVC(kernel='rbf',probability=True)
print "1st step done"
eclf = VotingClassifier(estimators=[('rf',clf1),('SVC', clf2), ('Gradient', clf3)], voting='soft')
for clf, label in zip([clf1,clf2, clf3, eclf], ['RF','SVM', 'Gradient', 'Ensemble']):
    scores = cross_validation.cross_val_score(clf, X[:750], Y[:750], cv=5, scoring='accuracy')
    print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))

#clf=clf.fit(X[:600],Y[:600])
print "2nd step done"
