# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 12:01:20 2016

@author: Yutthana
"""

import gzip
import csv
  
#read file from json.gz to csv and delete unused key       
def parsecsvNorm(path):
    f = open("Movie_1M.csv", 'wb') #save file name
#    unusedMeta = ['title', 'imUrl', 'related', 'salesRank', 'brand', 'categories', 'description'] #for meta file
#    unusedKey = ['helpful', 'reviewerName', 'summary', 'unixReviewTime', 'reviewTime'] #for content based
    unusedKey = ['helpful', 'reviewerName', 'summary', 'unixReviewTime', 'reviewText', 'reviewTime'] #for collab 
    g = gzip.open(path, 'r') 
    count = 1
    for l in g:
        data = eval(l)
        #delete unusedkey
        for key in unusedKey:
            if key in data:
                del data[key]        
        #set header
        if count == 1:
            w = csv.DictWriter(f, data.keys())
            w.writeheader()
            
        #chunk size (approx. 15% of data)
        count += 1
        if count == 1000000:
            break
        #write data
        w.writerow(data)
        
    f.close()
    return 0     
    
parsecsvNorm("reviews_Movies_and_TV.json.gz")


