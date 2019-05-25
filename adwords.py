#!/usr/bin/env python
# coding: utf-8

# In[59]:


import pandas as pd
import numpy as np
import math
import random
import sys

# Setting a seed to ensure replicability of results
random.seed(0)


# In[60]:

# Function that implements Greedy algorithm
def greedy(budgets, bids, queries):
    revenue = 0
    for q in queries:
        max_bid = 0
        max_bidder = None
        for bidder in bids[q].keys():
            bidder_budget = budgets[bidder]
            if(bidder_budget >= bids[q][bidder] and bids[q][bidder]>max_bid):
                max_bid = bids[q][bidder]
                max_bidder = bidder
            elif(bidder_budget >= bids[q][bidder] and bids[q][bidder]==max_bid and bidder < max_bidder):
                max_bidder = bidder  
                
        if(max_bidder):
            budgets[max_bidder] -= max_bid
            revenue=revenue+max_bid
    return revenue


# In[61]:


def frac_used(x):
    return 1-math.exp(x-1)

# Function that implements MSVV algorithm
def msvv(budgets,used, bids, queries):
    revenue = 0
    bidders['Used']=0
    for q in queries:
        max_scaled_budget = 0
        max_bidder = None
        for bidder in bids[q].keys():
            if((budgets[bidder]-used[bidder]) >= bids[q][bidder]):
                x = used[bidder]/budgets[bidder]
                if(bids[q][bidder]*frac_used(x)>max_scaled_budget):
                    max_scaled_budget = bids[q][bidder]*frac_used(x)
                    max_bidder = bidder
                elif(bids[q][bidder]*frac_used(x)==max_scaled_budget and bidder < max_bidder):
                    max_bidder = bidder
                
        if(max_bidder is not None):
            used[max_bidder] += bids[q][max_bidder]   
            revenue=revenue+bids[q][max_bidder]
    return revenue                              


# In[62]:

# Function that implements balance algorithm
def balance(budgets, bids, queries):
    revenue = 0
    for q in queries:
        max_budget = 0
        max_bidder = None
        for bidder in bids[q].keys():
            bidder_budget = budgets[bidder]
            if(bidder_budget >= bids[q][bidder] and bidder_budget > max_budget):
                max_budget = budgets[bidder]
                max_bidder = bidder
            elif(bidder_budget >= bids[q][bidder] and bidder_budget == max_budget and bidder < max_bidder):
                max_bidder = bidder 
                
        if(max_bidder):
            budgets[max_bidder] -= bids[q][max_bidder]
            revenue=revenue+bids[q][max_bidder]
    return revenue


# In[63]:


algo = 'greedy'
if len(sys.argv) > 1:
    algo = sys.argv[1]
queries = open('queries.txt').readlines()
queries = [q.strip() for q in queries]
bidders = pd.read_csv('bidder_dataset.csv')
bids = {}
budgets_main = {}
for bid in range(bidders.shape[0]):
    if(bidders.iloc[bid]['Advertiser'] not in budgets_main):
        budgets_main[bidders.iloc[bid]['Advertiser']] = bidders.iloc[bid]['Budget']
    if(bidders.iloc[bid]['Keyword'] not in bids):    
        bids[bidders.iloc[bid]['Keyword']] = {}
    bids[bidders.iloc[bid]['Keyword']][bidders.iloc[bid]['Advertiser']] = bidders.iloc[bid]['Bid Value']

optimal = 0
for advertiser in budgets_main.keys():
    optimal = optimal + budgets_main[advertiser]

sum_revenue = 0
for i in range(100):
    permuted = np.random.permutation(queries)
    budgets_copy = dict(budgets_main)
    if(algo=='greedy'):
        revenue = greedy(budgets_copy,bids,permuted)
        sum_revenue += revenue
    elif(algo=='msvv'):
        used = dict(budgets_copy)
        for bidder in used.keys():
            used[bidder] = 0
        sum_revenue = sum_revenue + msvv(budgets_copy, used, bids,permuted)
    elif(algo=='balance'):
        sum_revenue = sum_revenue + balance(budgets_copy,bids,permuted)
        
avg_revenue = sum_revenue/100
competitive_ratio = avg_revenue/optimal
print(round(avg_revenue,2))
print(round(competitive_ratio,2))


# In[ ]:




