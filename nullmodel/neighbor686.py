# -*- coding: utf-8 -*-
import networkx as nx
from nullmodel import *
import numpy as np
import math
import matplotlib.pyplot as plt

def z(G,list_G1,list_G2,f):#计算z值
    """
    输入参数：原始网络G，不保持连通性置乱网络list_G1,保持连通性置乱网络list_G2，指标函数名f
    返回：该指标的不保持连通性z值z1,保持连通性z值z2
    """
    G_l0 = f(G)
    print 'G=',G_l0
    list_G_l1 = []; list_G_l2 = []
    for G1 in list_G1:
        list_G_l1.append(f(G1))#指标值列表
    for G2 in list_G2:
        list_G_l2.append(f(G2))
    print 'list_G_l1:',list_G_l1
    print 'list_G_l2:',list_G_l2
    G_l1 = np.mean(list_G_l1) #求均值 
    G_l2 = np.mean(list_G_l2)
    print 'mean_G1=',G_l1
    print 'mean_G2=',G_l2
    var_z1 = np.var(list_G_l1) #求方差
    var_z2 = np.var(list_G_l2)
    print 'var_G1=',var_z1
    print 'var_G2=',var_z2
    if var_z1 == 0: #若方差为0，则z值取0
        z1 = 0
    else:
        z1 = (G_l0 - G_l1)/var_z1#z值
    if var_z2 == 0: 
        z2 = 0
    else:
        z2 = (G_l0 - G_l2)/var_z2#z值
    return z1, z2
    
def sp(tjl): #计算sp值
   """
    输入参数：统计量列表tjl eg:[tjl0,tjl1,...]
    返回：[（指标序号，sp值）,...]列表 eg:[(0,0.0),(1,0.23),(2,0.0),...]
   """
   list_spm = []
   length = len(tjl)
   for i in range(0,length): #遍历统计量，每个统计量得一个sp值
      valz = math.sqrt(sum([math.pow(e,2) for e in tjl]))
      spm = tjl[i]/valz
      list_spm.append([i,spm])
   return list_spm

def dict_degree_nodeslist(ndlist):
    D = {}      #{度：[节点1，节点2，..]}，其中节点1和节点2有相同的度
    for e in ndlist:
        if e[0] not in D:
            D[e[0]] = [e[1]]
        else:
            D[e[0]].append(e[1])
    return D

#原始网络
fh=open("686_links.txt", 'rb') #1656条边,168个节点
G=nx.read_edgelist(fh)
fh.close()
print len(G.edges()),len(G.nodes())


#置乱网络
list_G1 = []
list_G2 = []
nswap = 2 * len(G.edges())
maxtry = 100 * nswap
#G1 = random_1k(G, nswap=nswap, max_tries=maxtry)
#G2 = random_1kc(G, nswap=nswap, max_tries=maxtry)
#print len(G1.edges()),len(G1.nodes())
#print len(G2.edges()),len(G2.nodes())
for i in range(0,10):
   G1 = random_1k(G, nswap=nswap, max_tries=maxtry)
   G2 = random_1kc(G, nswap=nswap, max_tries=maxtry)
   list_G1.append(G1)
   list_G2.append(G2)

markers = ['o','s','x']
colors = ['r','b','g']
alphas = [1,0.5,1]
size = [30,60,80]
labels = ['yuanshi','bubaochiliantong','baochiliantong']
j = 0
#==============================================================================
# #最大派系分布
# """
# 1)cl = list(nx.find_cliques(G))-->cl=[[n1,n2,n3],[],...]
# 2)len_cl = [len(e) for e in cl] -->len_cl=[3,...]
# 3)draw
# """
# def get_counts(sequence):
#     from collections import defaultdict
#     counts = defaultdict(int)
#     for x in sequence:
#         counts[x] += 1
#     return counts
#     
# markers = ['o','s','x']
# colors = ['r','b','g']
# alphas = [1,0.5,1]
# size = [30,60,80]
# labels = ['yuanshi','bubaochiliantong','baochiliantong']
# j = 0
# cl0 = list(nx.find_cliques(G))
# cl1 = list(nx.find_cliques(G1))
# cl2 = list(nx.find_cliques(G2))
# for cl in [cl0,cl1,cl2]:
#     len_cl = [len(e)for e in cl]
#     dict_cl = {e:len_cl.count(e)/float(len(len_cl))for e in set(len_cl)}
#     x = dict_cl.keys()
#     y = dict_cl.values()
#     plt.scatter(x,y,s=size[j],c=colors[j],label=labels[j],marker=markers[j],alpha=alphas[j])
#     plt.plot(x,y,c=colors[j])
#     j += 1
# plt.legend(loc='upper right')
# plt.xlabel('len_cliques')
# plt.ylabel('frequence')
# plt.show()
#==============================================================================

#==============================================================================
# #富人俱乐部系数分布
# l0 = nx.rich_club_coefficient(G,normalized=False)
# l1 = nx.rich_club_coefficient(G1,normalized=False)
# l2 = nx.rich_club_coefficient(G2,normalized=False)
# j = 0
# markers = ['o','s','x']
# colors = ['r','b','g']
# alphas = [1,0.5,1]
# size = [30,60,80]
# labels = ['yuanshi','bubaochiliantong','baochiliantong']
# for l in [l0,l1,l2]:
#     x = l.keys()
#     y = l.values()
#     plt.scatter(x,y,s=size[j],c=colors[j],label=labels[j],marker=markers[j],alpha=alphas[j])
# #    plt.plot(x,y,c=colors[j])
#     j += 1
# plt.legend(loc='upper left')
# plt.xlabel('degree')
# plt.ylabel('rich_club_coefficient')
# plt.show()
#==============================================================================

#==============================================================================
# ##接近中心性分布#err
# l0 = map(lambda t:(t[1],t[0]), G.degree().items())  #(度,节点)组成的列表
# l1 = map(lambda t:(t[1],t[0]), G1.degree().items())
# l2 = map(lambda t:(t[1],t[0]), G2.degree().items())
# D0 = dict_degree_nodeslist(l0)
# D1 = dict_degree_nodeslist(l1)
# D2 = dict_degree_nodeslist(l2)
# list_D = [D0,D1,D2]
# markers = ['o','s','x']
# colors = ['r','b','g']
# alphas = [1,0.5,1]
# size = [30,60,80]
# labels = ['yuanshi','bubaochiliantong','baochiliantong']
# j = 0
# bc = nx.closeness_centrality(G)
#  for D in list_D:
#     bc1 = []
#     for i in range(len(D)):
#         t = D.values()[i]
#         bc1.extend([bc[e]for e in D.values()[i]])
#         D[D.keys()[i]] = numpy.mean(bc1)
#     x = D.keys()
#     y = D.values()
# #    print j,D
#     plt.scatter(x,y,s=size[j],c=colors[j],label=labels[j],marker=markers[j],alpha=alphas[j])
#     plt.plot(x,y,c=colors[j])
#     j += 1
# plt.legend(loc='upper right')
# plt.xlabel('degree')
# plt.ylabel('closeness_centrality')
# plt.show()
#==============================================================================

#==============================================================================
# ##介数分布#err
# l0 = map(lambda t:(t[1],t[0]), G.degree().items())  #(度,节点)组成的列表
# l1 = map(lambda t:(t[1],t[0]), G1.degree().items())
# l2 = map(lambda t:(t[1],t[0]), G2.degree().items())
# D0 = dict_degree_nodeslist(l0)
# D1 = dict_degree_nodeslist(l1)
# D2 = dict_degree_nodeslist(l2)
# list_D = [D0,D1,D2]
# markers = ['o','s','x']
# colors = ['r','b','g']
# alphas = [1,0.5,1]
# size = [30,60,80]
# labels = ['yuanshi','bubaochiliantong','baochiliantong']
# j = 0
# bc = nx.betweenness_centrality(G)
#
# for D in list_D:
#     bc1 = []
#     for i in range(len(D)):
#         t = D.values()[i]
#         bc1.extend([bc[e]for e in D.values()[i]])
#         D[D.keys()[i]] = numpy.mean(bc1)
#     x = D.keys()
#     y = D.values()
# #    print j,D
#     plt.scatter(x,y,s=size[j],c=colors[j],label=labels[j],marker=markers[j],alpha=alphas[j])
#     plt.plot(x,y,c=colors[j])
#     j += 1
# plt.legend(loc='upper right')
# plt.xlabel('degree')
# plt.ylabel('betweenness_centrality')
# plt.show()
#==============================================================================

#==============================================================================
# ##度分布
# l0 = G.degree().values()#度序列
# l1 = G1.degree().values()
# l2 = G2.degree().values()
# j = 0
# colors = ['r','b','g']
# labels = ['yuanshi','bubaochiliantong','baochiliantong']
# markers = ['o','s','x']
# alphas = [1,0.5,1]
# size = [30,60,80]
# for t in [l0,l1,l2]:
#     dt = {e:t.count(e)/float(len(t)) for e in set(t)}
#     x = dt.keys()
#     y = dt.values()
#     plt.scatter(x,y,s=size[j],c=colors[j],label=labels[j],marker=markers[j],alpha=alphas[j])
# #    plt.plot(x,y,c=colors[j])
#     j += 1
# plt.legend(loc='upper right')
# plt.xlabel('degree')
# plt.ylabel('P')
# plt.show()
#==============================================================================

#==============================================================================
# #最短路径长度分布
# j = 0
# colors = ['r','b','y']
# labels = ['yuanshi','bubaochiliantong','baochiliantong']
# markers = ['o','s','x']
# size = [20,30,40]
# for g in [G,G1,G2]:
#     l0 = nx.all_pairs_shortest_path_length(g).values()
#     t = []
#     for i in range(len(l0)):
#         t.extend(l0[i].values())
#     dt = {e:t.count(e)/float(len(t)) for e in set(t)}
#     x = dt.keys()
#     y = dt.values()
#     plt.scatter(x,y,s=size[j],c=colors[j],label=labels[j],marker=markers[j])
#     plt.plot(x,y,c=colors[j])
#     j += 1
# plt.legend(loc='upper right')
# plt.xlabel('distance')
# plt.ylabel('P')
# plt.show()
#==============================================================================

#聚类系数分布
for g in [G,G1,G2]:
    l = map(lambda t:(t[1],t[0]), g.degree().items())  #(度,节点)组成的列表
    D = dict_degree_nodeslist(l)
    for i in range(len(D)):
        D[D.keys()[i]] = nx.average_clustering(g, nodes=D.values()[i])#
    x = D.keys()
    y = D.values()
    print np.mean(y)
    plt.scatter(x,y,s=size[j],c=colors[j],label=labels[j],marker=markers[j])
    plt.plot(x,y,c=colors[j])
    j += 1
plt.legend(loc='upper right')
plt.xlabel('degree')
plt.ylabel('samedegree_average_clustering')
plt.show()


#==============================================================================
# #最临近节点的平均度分布#err
# l0 = map(lambda t:(t[1],t[0]), G.degree().items())  #(度,节点)组成的列表
# l1 = map(lambda t:(t[1],t[0]), G1.degree().items())
# l2 = map(lambda t:(t[1],t[0]), G2.degree().items())
# list_degreenodes = [l0,l1,l2]
# colors = ['r','b','g']
# labels = ['yuanshi','bubaochiliantong','baochiliantong']
# j = 0
# for l in list_degreenodes:
#     D = dict_degree_nodeslist(l)
# #    print D
#     for i in range(len(D)):
#         D[D.keys()[i]] = numpy.mean((nx.average_neighbor_degree(G, nodes=D.values()[i])).values())
#     x = D.keys()
#     y = D.values()
# #    print j,D
#     plt.scatter(x,y,c=colors[j],label=labels[j])
# #    plt.plot(x,y,c=colors[j])
#     j += 1
# plt.legend(loc='lower right')
# plt.xlabel('degree')
# plt.ylabel('samedegree_average_neighbor_degree')
# plt.show()
#==============================================================================

def ave_degree(G):
    d = G.degree().values()
    return np.mean(d)
    
#平均聚类系数
z1_average_clustering,z2_average_clustering = z(G,list_G1,list_G2,nx.average_clustering)

#匹配系数
z1_assortativity_coefficient,z2_assortativity_coefficient = z(G,list_G1,list_G2,nx.degree_assortativity_coefficient)

#平均度
z1_average_degree,z2_average_degree = z(G,list_G1,list_G2,ave_degree)

print z1_average_clustering,z1_assortativity_coefficient,z1_average_degree
sp1,sp2 = sp([z1_average_clustering,z1_assortativity_coefficient,z1_average_degree]),sp([z2_average_clustering,z2_assortativity_coefficient,z2_average_degree])
plt.xticks((0,1,2),('average_clustering','assortativity_coefficient','average_degree'))


#==============================================================================
# #平均最短路径长度
# z1_path,z2_path = z(G,list_G1,list_G2,nx.average_shortest_path_length)    
# #直径
# z1_diameter,z2_diameter = z(G,list_G1,list_G2,nx.diameter) 
# #连通组元数量
# z1_components,z2_components = z(G,list_G1,list_G2,nx.number_connected_components) 
# 
# sp1,sp2 = sp([z1_path,z1_diameter,z1_components]),sp([z2_path,z2_diameter,z2_components])
# #plt.xticks((0,1,2),('average_shortest_path_length','diameter','number_connected_components'))
#==============================================================================

plt.scatter(list(zip(*sp1)[0]),list(zip(*sp1)[1]),c='r',marker='o',label='blt')
plt.scatter(list(zip(*sp2)[0]),list(zip(*sp2)[1]),c='b',marker='x',label='lt',s=60)
plt.plot(list(zip(*sp1)[0]),list(zip(*sp1)[1]),c='r')
plt.plot(list(zip(*sp2)[0]),list(zip(*sp2)[1]),c='b',ls=':',linewidth=5)
plt.legend(loc='upper right')
plt.xlabel('zhibiao')
plt.ylabel('sp')
plt.show()



