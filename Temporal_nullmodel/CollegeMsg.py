# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 10:10:04 2017

@author: 08119
"""
import networkx as nx
import pandas as pd
from tnm import *
import os
path = os.getcwd()

filename = 'CollegeMsg.txt'
fh = pd.read_csv(filename,names=['node1', 'node2', 'timestamp'],header=None,delim_whitespace=True)
#fh.head()
#构建网络
G=nx.from_pandas_dataframe(fh,'node1','node2',edge_attr='timestamp', create_using=nx.MultiGraph())

nswap = 2 * len(G.edges())
maxtry = 100 * nswap

G0 = edges_swap_0k(G, nswap=nswap, max_tries=maxtry)
nx.write_edgelist(G0, path+'/edges_swap_0k.txt',data=['timestamp'])

G0 = edges_swap_1k(G, nswap=nswap, max_tries=maxtry)
nx.write_edgelist(G0, path+'/edges_swap_1k.txt',data=['timestamp'])

G0 = time_swap(G, nswap=nswap, max_tries=maxtry)
nx.write_edgelist(G0, path+'/time_swap.txt',data=['timestamp'])


G0 = time_random(G, nswap=nswap, max_tries=maxtry,mins=fh.timestamp.min(),maxs=fh.timestamp.max())
nx.write_edgelist(G0, path+'/time_random.txt',data=['timestamp'])


G0 = timeweight_swap(G, nswap=nswap, max_tries=maxtry)
nx.write_edgelist(G0, path+'/timeweight_swap.txt',data=['timestamp'])

G0 = sametimeweight_swap(G, nswap=nswap, max_tries=maxtry)
nx.write_edgelist(G0, path+'/sametimeweight_swap.txt',data=['timestamp'])

#youwenti
G0 = time_randomswap(G, nswap=nswap, max_tries=maxtry)
nx.write_edgelist(G0, path+'/time_randomswap.txt',data=['timestamp'])

# 画图
import seaborn as sns
import os  
# 获取文件夹内所有文件名  
def file_name(file_dir):   
    L=[]   
    for root, dirs, files in os.walk(file_dir):
        for file in files: 
#            print os.path.splitext(file)[1]
            if os.path.splitext(file)[1] == '.txt': 
                L.append(file) 
    return L

files = file_name(path+'/tnm1') 
for f in files:
    draw = pd.read_csv(path+'/tnm1/'+f,sep=' ',header=None)
    sns.heatmap(draw)
    title,_ = os.path.splitext(f)
    plt.title(title)
    plt.savefig(path+'/tnm1/'+title+'.jpg')
    plt.show()