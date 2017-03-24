# -*- coding: utf-8 -*-
"""
Created on Wed Mar 01 11:52:09 2017
实证网络的某个模体数量/零模型的某个模体数量。
如果零模型的某个模体不存在，或者两者比例相差是很多倍>2，可以就取2
实际上就是讲你的几个txt文件里面的对应元素相除，分母为零或者得到的结果大于2的，你都让它等于2，然后在画图。
@author: 08119
"""
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os  
path = os.getcwd()
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
df = pd.read_csv(path+'/tnm1/'+files[0],sep=' ',header=None)
df_title,_ = os.path.splitext(files[0])
for f in files[1:]:
    title,_ = os.path.splitext(f)
#    title = df_title + '_' + title
    df1 = pd.read_csv(path+'/tnm1/'+f,sep=' ',header=None)
    z = df/df1
    z.to_csv(path+'/tnm2/'+title+'.csv')
    z[z>2] = 2
    z[z<0] = 0
    z.replace(np.inf,2,inplace=True)
    z.to_csv(path+'/tnm2/After_'+title+'.csv')
    

    sns.heatmap(z,cmap='RdYlBu_r',vmin=0, vmax=2, annot=True,linewidths=.5)
    
    plt.title(title)
    plt.savefig(path+'/tnm2/'+title+'.jpg')
    plt.show()