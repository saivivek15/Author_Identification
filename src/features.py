from mongo import load_from_mongo
import re,nltk
from collections import Counter
from nltk.corpus import words
from string import punctuation
from enchant.checker import SpellChecker
import collections
import itertools
alphabet="abcdefghijklmnopqrstuvwxyz"
exclude = set(punctuation)
func_wrds=[]
with open('Function Words/EnglishAuxiliaryVerbs.txt') as f:
    for i in f:
        j=i.split('\n')
        func_wrds.append(j[0])
with open('Function Words/EnglishConjunctions.txt') as f:
    for i in f:
        j=i.split('\n')
        func_wrds.append(j[0])
with open('Function Words/EnglishDeterminers.txt') as f:
    for i in f:
        j=i.split('\n')
        func_wrds.append(j[0])
with open('Function Words/EnglishPrepositions.txt') as f:
    for i in f:
        j=i.split('\n')
        func_wrds.append(j[0])
with open('Function Words/EnglishPronouns.txt') as f:
    for i in f:
        j=i.split('\n')
        func_wrds.append(j[0])
with open('Function Words/EnglishQuantifiers.txt') as f:
    for i in f:
        j=i.split('\n')
        func_wrds.append(j[0])
with open('Function Words/stopwords.txt') as f:
    for i in f:
        j=i.split('\n')
        func_wrds.append(j[0])
taglst=[]
with open('taglist.txt') as f:
    tags=f.readlines()
    for i in tags:
        a= re.split('\t?\s?',i)[0]
        taglst.append(a)
#print taglst
##taglst1=[]
##for i in taglst:
##    for j in taglst:
##        if i!=j:
##            d=(i,j)
##            if d not in taglst1:
##                taglst1.append(d)
##
##for (i,j) in taglst1:
##    if (j,i) in taglst1:
##        taglst1.remove((j,i))
##
taglst1=[]
with open('pos_tags.txt') as f:
    tags=f.readlines()
    for i in tags:
        a=re.split("\s",i)
        a=a[:2]
        taglst1.append(tuple(a))
        if tags.index(i)==50:
            break


func_wrds=set(func_wrds)

def ngrams(text):
    w1=[]
    wordlist= text.split()
    for w in wordlist:
        w2=re.split("[.]+",w)
        w1=w1 +w2
    for i in range(len(w1)):
        w1[i] = ''.join(ch for ch in w1[i] if ch not in exclude)
    w1[:]=[x for x in w1 if x!=""]
    #print w1
    output=[]
    bgs=nltk.bigrams(w1)
    tgs=nltk.trigrams(w1)
    return bgs,tgs

def letter_freq(text):
    return Counter(text.strip())

def blank_lines(text):
    line_list=text.split('\n')
    blanklines=line_list.count("")
    return blanklines

def punct(text):
    count = Counter(text)
    #print count
    punct_count = {k:v for k, v in count.iteritems() if k in punctuation}
    return punct_count

def word_freq(text):
    w1=[]
    wordlist= text.split()
    for w in wordlist:
        w2=re.split("[.]+",w)
        w1=w1 +w2
    for i in range(len(w1)):
        w1[i] = ''.join(ch for ch in w1[i] if ch not in exclude)
    wordfreq =[w1.count(p) for p in wordlist]
    return dict(zip(w1,wordfreq))

def funct_vocab(text):
    vocab=0
    funct =0
    w1=[]
    wordlist= text.split()
    for w in wordlist:
        w2=re.split("[.]+",w)
        w1=w1 +w2
    for i in range(len(w1)):
        w1[i] = ''.join(ch for ch in w1[i] if ch not in exclude)
        if w1[i] in func_wrds:
            #print w1[i]
            funct +=1
        else:
            if w1[i] !='':
                vocab +=1
    try:
        total=float(vocab+funct)
        vocab_rich=vocab/total
    except:
        vocab_rich=0.0
    return [funct,"%.2f" % vocab_rich]

def spelling_check(text):
    errors=0
    error_words=[]
    chkr=SpellChecker("en_US")
    chkr.set_text(text)
    for err in chkr:
        errors +=1
        error_words.append(err.word)
    return errors,error_words

def length(text):
    wordlist=[]
    wordlength=[]
    sentences=text.split('.')
    para=text.split('\n')
    #print para
    num_para=len(para)
    #print num_para
    num_sentences=len(sentences)
    #print num_sentences
    length=[]
    for i in sentences:
        words=i.split()
        wordlist=wordlist +words
        length_sentence=len(words)
        length.append(length_sentence)
    #print wordlist
    #print sum(length),len(wordlist)
    for i in wordlist:
        wordlength.append(len(i))
    #print sum(wordlength)
    try:
        avg_word_length=sum(wordlength)/float(len(wordlist))
    except:
        avg_word_length=0.0
    try:
        avg_para_length=num_sentences/float(num_para)
    except:
        avg_para_length=0.0
    try:
        avg_sent_length=sum(length)/float(num_sentences)
    except:
        avg_sent_length=0.0
    return ("%.2f" % avg_para_length),("%.2f" % avg_sent_length),("%.2f" % avg_word_length)
    
email_content = load_from_mongo('email_content','coll_ten')
for i in email_content:
    name = i['name']
    text = i['email']
    token = i['email_number']
    _id = i['_id']
##    fdist=nltk.FreqDist(ngrams(text)[0])
##    fdist1=nltk.FreqDist(ngrams(text)[1])
##    with open('test.txt','a') as f:
##        for k,v in fdist1.items():
##            for iter in k:
##                f.write(iter)
##                if iter!=k[-1]:
##                    f.write(",")
##            f.write('\n')
    let_f= sorted(letter_freq(text).iteritems())
    lf=[0]*26
    pf=[0]*len(punctuation)
    for ilf in range(26):
        for jlf in let_f:
            if alphabet[ilf]==jlf[0]:
                lf[ilf] +=jlf[1]
    for ip in range(len(punctuation)):
        for jp in let_f:
            if punctuation[ip]==jp[0]:
                pf[ip] +=jp[1]
    pos_dep=i['pos_dependecies']
    for i in range(len(pos_dep)):
        pos_dep[i]=tuple(pos_dep[i])
    count_tag=collections.Counter(pos_dep)
    tag=[0]*len(taglst1)
    count_tag=sorted(count_tag.iteritems())
    #print count_tag
    for rot in range(len(count_tag)):
        a,b=count_tag[rot][0]
        c=(b,a)
        if count_tag[rot][0] in taglst1:
            ind=taglst1.index(count_tag[rot][0])
            tag[ind]=count_tag[rot][1]
        elif c in taglst1:
            ind=taglst1.index(c)
            tag[ind]=count_tag[rot][1]
    with open('features.txt','a') as f:
        f.write(str(blank_lines(text)))
        f.write(',')
        f.write(str(funct_vocab(text)[0]))
        f.write(',')
        f.write(str(funct_vocab(text)[1]))
        f.write(',')
        f.write(str(spelling_check(text)[0]))
        f.write(',')
        f.write(str(length(text)[0]))
        f.write(',')
        f.write(str(length(text)[1]))
        f.write(',')
        f.write(str(length(text)[2]))
        f.write(',')
        for gamma in lf:
            f.write(str(gamma))
            f.write(',')
        for gamma in pf:
            f.write(str(gamma))
            f.write(',')
        for bing in tag:
            f.write(str(bing))
            f.write(',')
        f.write(name)
        f.write('\n')
    print text
##    print "Letter and Punctuation Frequency: ", let_f
##    print "Number of blank lines: ", blank_lines(text)
##    print "Vocabualry Richness: ", funct_vocab(text)[1]
##    print "Number of function words: ", funct_vocab(text)[0]
##    print "Idiosyncracies: " ,spelling_check(text)[0]
##    print "Average Paragraph length: ", length(text)[0]
##    print "Average Sentence length: ", length(text)[1]
##    print "Average Word length: ", length(text)[2]




