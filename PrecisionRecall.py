# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 11:57:13 2016

@author: Yutthana
"""

import pandas as pd
from pandas import *
import random
import math
import matplotlib.pyplot as plt

f = open('UserToItemTable.csv') #from UserToItemTable.py
all_item = []
hide_item = []
y_true = []
#print df['Product_ID']
for item in f:
    item = item.replace('{', '').replace('}', '').replace('"', '').replace(' ', '')
    item = item.rstrip().split(',')
    all_item.append(item)
    y_true.append(item[1:])
    random_item = random.sample(item[1:], int(round((len(item)*0.6) - 0.5))) #hide 40% of data
#    print random_item
#    random_item.insert(0, item[0]) #insert reviewerid infront of list of itemid
    hide_item.append(random_item)
    
del y_true[0]
#print type(all_item[1][1:300])
#print len(all_item[1][1:])
#
#y_true = all_item[1][1:]
#
#sim = open('Movie_500_result.csv')

Precision_content = []
Recall_content = []
Precision_collab = []
Recall_collab = []

for it in range(2):
    for k in xrange(1,10):
        if (it == 0):
            sim = open('result_content500.csv') # content based
        if (it == 1):
            sim = open('Movie_500_result.csv') # collaborative
        
        sim_item = []
        sim_key = []
    #    k = 9 #number of k
        
        #read similar item from file and append in list
        sim_key = []
        sim_item = []
        
        for item in sim:
            item = item.rstrip().split(',')
            sim_key.append(item[0])
            sim_item.append(item[1:k+2])
        sim.close()
        
        #set up y pred 
        y_pred = []
        for i in xrange(1, len(hide_item)):
            recommend_item = []
            for j in hide_item[i]:
                if j in sim_key:
                    recommend_item = recommend_item + sim_item[sim_key.index(j)][1:]
            y_pred.append(recommend_item)
        
        
        total_recall = 0.0
        total_precision = 0.0
        max_recall = 0.0
        max_precision = 0.0
        ##calculate precision & recall
        for i in xrange(len(y_true)):
            if len(y_pred[i]) == 0:
                total_precision += 0.0
                total_recall += 0.0
            else:
                tp = len(list(set(y_true[i]) & set(y_pred[i])))
                precision = float(tp)/float(len(y_pred[i]))
                recall = float(tp)/float(len(y_true[i]))
                if (precision > max_precision):
                    max_precision = precision
                if (recall > max_recall):
                    max_recall = recall
                total_precision += precision
                total_recall += recall
                
                
        total_precision = (total_precision/len(y_true))
        total_recall = (total_recall/len(y_true))
        if (it == 0):
            Precision_content.append(total_precision)
            Recall_content.append(total_recall)
        if (it == 1):
            Precision_collab.append(total_precision)
            Recall_collab.append(total_recall)


#normalize data to be in range [0,1]
norm_precision_collab = [float(i)/max(Precision_collab) for i in Precision_collab]

norm_recall_collab = [float(i)/max(Recall_collab) for i in Recall_collab]

norm_precision_content = [float(i)/max(Precision_content) for i in Precision_content]
 
norm_recall_content = [float(i)/max(Recall_content) for i in Recall_content]

plt.figure(figsize=(10,10))
plt.plot(norm_recall_collab, norm_precision_collab, 'r-o', label = 'Collaborative Filltering')
plt.plot(norm_recall_content,norm_precision_content, 'b-o', label = 'Content-based')
plt.ylabel('Precision')
plt.xlabel('Recall')
#
#plt.axis([0.2,0.5,0.7,1.0])
plt.legend(loc='upper right')




