import os,re,subprocess,sys,os.path
import pymongo
from subprocess import STDOUT,PIPE
from mongo import load_from_mongo
import collections
import json
client=pymongo.MongoClient('localhost',27017)
db1=client['email_content']
coll2=db1['coll_charm']


def compile_java(java_file):
    subprocess.check_call(['javac', java_file])

def execute_java(java_file, stdin):
    java_class,ext = os.path.splitext(java_file)
    cmd = ['java', java_class]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate(stdin)
    return ('This was "' + stdout + '"')

distinct=[]
counter=0
persons=os.listdir("..\enron_mail\maildir")
#print persons
count=0
for person in persons:
    categories=os.listdir("..\enron_mail\maildir\\%s" %person)
    if '_sent_mail' in categories:
        mail_folder=os.listdir("..\enron_mail\maildir\\%s\\_sent_mail" %person)
        for each in mail_folder:
            pat= "..\enron_mail\maildir\\%s\\_sent_mail\\%s" %(person,each)
            with open(pat,'r') as f:
                try:
                    g={}
                    data=f.read()
                    ind=data.index('X-FileName: ')
                    data1=data[ind:]
                    t=re.sub("^X-FileName: .+\n","",data1)
                    g['name']=person
                    g['email_number']=each
                    g['email']=t
                    t=t.replace("\n","")
                    t=t.replace("\t","")
                    with open('input.txt','w') as f:
                        f.write(t)
                    with open('sample-input.txt','w') as f:
                        f.write(t)
                    tag_path = os.path.abspath('tag.bat')
                    vars=subprocess.check_output([tag_path,'&&','set'],shell=True)
                    with open('tagged.txt') as f:
                        text=f.readlines()
                        #print text
                        #print "#####"
                        g1={}
                        g2=[]
                        for i in text:
                            lst=re.split(" ",i)
                            #print lst
                            for j in lst:
                                c,d=re.split("_",j)
                                c=c.encode('ascii')
                                d=d.replace('\n','')
                                d=d.encode('ascii')
                                
                                g1[c]=d
                                g2.append([c,d])
                    g['tagged_text']=g2
                    
                    compile_java('ParserDemo.java')
                    a=execute_java('ParserDemo.java',t)
                    #print a
                    links=re.split("done \[\d+\.\d+ sec+\]\.",a)[1]
                    links=links.rstrip("\" ")
                    links=links.rstrip("\n")
                    links=links[1:-1]
                    links=re.split("\), ",links)
                    h=[]
                    for entry in links:
                        a,b=re.split(", ",entry)
                        index1=a.index('(')
                        index2=a.index('-')
                        a=a[index1+1:index2]
                        index3=b.index('-')
                        b=b[:index3]
                        h.append([a,b])
                    g['word_dependency']=h
                    for i in range(len(h)):
                        for k in g1.keys():
                            if h[i][0] == k:
                                h[i][0]=g1[k]
                            if h[i][1] == k:
                                h[i][1]=g1[k]
                    for i in range(len(h)):
                        if h[i] not in distinct:
                            distinct.append(h[i]) 
                        h[i]=tuple(h[i])
                        count+=1
                    #print collections.Counter(h)
                    g['pos_dependecies']=h      
                    
                    try:
                        print "*****"
                        coll2.insert(g)
                    except:
                        print "unexpected error",sys.exc_info()[0]
                except:
                    print person,each,sys.exc_info()[0]
                    print "####"

            counter +=1
            print counter

print count                   
print len(distinct)

    
