import os,sys
import pymongo

client=pymongo.MongoClient('localhost',27017)
db=client['urls']
coll=db['coll']


for root, dirs, files in os.walk(os.path.join("enron_mail\maildir")):
    for name in files:
        #print name
        my_files={}
        my_name = root.split("\\")[7]
        if my_name not in my_files:
            my_files[my_name] = []
        my_files[my_name].append(os.path.join(root, name))
        try:
            coll.insert(my_files)
        except:
            print "unexpected error",sys.exc_info()[0]
