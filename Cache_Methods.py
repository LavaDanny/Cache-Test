import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
import scipy as sp
import scipy.stats as st
import csv as csv
import random

#Loads the CSV file
def load_file(filename):
    names = []
    try:
        f = open(filename)
        reader = csv.reader(f)
        for row in reader:
            names.append(row[0])
        f.close()
    except:
       print ('Error: Could Not Load File')
    return np.array(names)

#Creates a zipf distribution using the stats discrete module
def zipf(s, N):
    n = range(1,N+1)
    p = []
    z = 0.
    for i in n:
        temp = (1./i)**s
        p.append(temp)
        z = z+temp
    for i in range(np.size(p)): p[i]=p[i]/z
    return st.rv_discrete(name = 'Zipf', values=(n,p))

#When a hit occurs, puts the hit item at the top of the list
def cache_hit(cache,item,rv):
    for i in range(rv,np.size(cache)-1):
        cache[i] = cache[i+1]
    cache[np.size(cache)-1] = item
    return cache

#When a hit occurs, puts the hit item at the top of the list
def cache_hit3(cache,item,rv, number_of_hits):
    
    i = 0
    while i < 2:
        if cache[i] == item:
            number_of_hits[i] = number_of_hits[i] + 1
        i = i + 1

    return cache
    
#When a miss occurs, replaces the least recently used item
def cache_miss(cache, item, maxSize):
    if(np.size(cache) < maxSize):
        cache.append(item)
    else:
        for i in range(np.size(cache)-1):
            cache[i]=cache[i+1]
            cache[np.size(cache)-1] = item
    return cache

#random replacement
def cache_miss2(cache, item, maxSize):

    if(np.size(cache) < maxSize):
        cache.append(item)
    else:
        randint = random.randint(0,1)
        cache[randint] = item
    return cache

#remove least frequently used
def cache_miss3(cache, item, maxSize, number_of_hits):
    if(np.size(cache) < maxSize):
        cache.append(item)
    else:
        #for i in range(np.size(cache)-1):
        #    cache[i]=cache[i+1]
        #    cache[np.size(cache)-1] = item

        if number_of_hits[0] > number_of_hits[1]:
            number_of_hits[1] = 0
            cache[1] = item
        else:
            number_of_hits[0] = 0
            cache[0] = item

    return cache
    
def look_for_cache(cache,item):
    y = -1
    for i in range(np.size(cache)):
        if (cache[i] == item):
            y = i
            break
    return y

#Runs the main code for the simulation
filename = 'testdata.csv'
names = load_file(filename) #This is treated as your memory
rv_zipf = zipf(1,np.size(names))
print("number of contents:", np.size(names))
k = 2 #Size of the Cache
r = 10**4 #Number of retrievals

hits = 0. #Keeps track of the number of hits in the cache
hits2 = 0
hits3 = 0

hit_av_lru = [] #Keeps track of the hit average
hit_av_rr = []
hit_av_lfu = []

cache = [] #Array to represent the cache
cache2 = []
cache3 = ['','']

number_of_hits = [0,0] # array to track hits in lfu

for i in range(r):
    rv = rv_zipf.rvs()-1 #Random variate from the zipf distribution
    item = names[rv] #Item to be retrieved
    index = look_for_cache(cache, item)
    #print (rv)
    #print ("retrieve:",i, item)
    if (index >=0):
        cache = cache_hit(cache, item, index)
        hits = hits+1
    else:
        cache = cache_miss(cache, item, k)
    hit_av_lru.append(hits*1.0/(i+1))
    #print ("hits:",hits)

for i in range(r):
    rv = rv_zipf.rvs()-1 #Random variate from the zipf distribution
    item = names[rv] #Item to be retrieved
    index = look_for_cache(cache2, item)
    if (index >= 0):
        #cache = cache_hit(cache,item,index)
        hits2 = hits2 + 1
    else:
        cache2 = cache_miss2(cache2,item,k)
    hit_av_rr.append(hits2*1.0/(i+1))  

for i in range(r):
    rv = rv_zipf.rvs()-1 #Random variate from the zipf distribution
    item = names[rv] #Item to be retrieved
    index = look_for_cache(cache3, item)
    if (index >= 0):
        #cache = cache_hit(cache,item,index)
        cache3 = cache_hit3(cache3,item,index, number_of_hits)
        hits3 = hits3 + 1
    else:
        cache3 = cache_miss3(cache3,item,k, number_of_hits)
    hit_av_lfu.append(hits3*1.0/(i+1))  



print ("cache size:",np.size(cache))
print ("cache:",cache)
plt.subplot(3,1,1)
plt.title('Moving Hit Percentage LRU')
plt.xlabel('Number of Items Retrieved')
plt.ylabel('Hit Percentage')
plt.plot(hit_av_lru)
print ('Hit Percentage:', hit_av_lru[np.size(hit_av_lru)-1])

print ("cache2 size:",np.size(cache2))
print ("cache2:",cache2)
plt.subplot(3,1,2)
plt.title('Moving Hit Percentage RR')
plt.xlabel('Number of Items Retrieved')
plt.ylabel('Hit Percentage')

plt.plot(hit_av_rr)
print ('Hit Percentage 2:', hit_av_rr[np.size(hit_av_rr)-1])

print ("cache3 size:",np.size(cache3))
print ("cache3:",cache3)
plt.subplot(3,1,3)
plt.title('Moving Hit Percentage LFU')
plt.xlabel('Number of Items Retrieved')
plt.ylabel('Hit Percentage')
plt.plot(hit_av_lfu)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=1)
print ('Hit Percentage 3:', hit_av_lfu[np.size(hit_av_lfu)-1])
plt.show()