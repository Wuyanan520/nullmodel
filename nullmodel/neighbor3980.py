# -*- coding: utf-8 -*-
import networkx as nx
import nullmodel as nm
import numpy as np
import math
import matplotlib.pyplot as plt

def z(G,list_G1,list_G2,f):#计算z值
    """
    输入参数：原始网络G，不保持连通性置乱网络list_G1,保持连通性置乱网络list_G2，对网络连通性无要求的指标函数名f
    返回：该指标的不保持连通性z值z1,保持连通性z值z2
    """
    G_l0 = f(G)
    list_G_l1 = []; list_G_l2 = []
    for G1 in list_G1:
        list_G_l1.append(f(G1))#指标值列表
    for G2 in list_G2:
        list_G_l2.append(f(G2))
    G_l1 = np.mean(list_G_l1) #求均值 
    G_l2 = np.mean(list_G_l2)
    var_z1 = np.var(list_G_l1) #求方差
    var_z2 = np.var(list_G_l2)
    if var_z1 == 0: #若方差为0，则z值取0
        z1 = 0
    else:
        z1 = (G_l0 - G_l1)/var_z1#z值
    if var_z2 == 0: 
        z2 = 0
    else:
        z2 = (G_l0 - G_l2)/var_z2#z值
    return z1, z2
    
def zc(G,list_G1,list_G2,f):#计算z值
    """
    输入参数：原始网络G，不保持连通性置乱网络list_G1,保持连通性置乱网络list_G2，要求网络连通的指标函数名f
    返回：该指标的不保持连通性z值z1,保持连通性z值z2
    """
    list_G_l0 = []; list_G_l1 = []; list_G_l2 = []
    for g in nx.connected_component_subgraphs(G):
        list_G_l0.append(f(g))
    for G1 in list_G1:
        for g1 in nx.connected_component_subgraphs(G1):
            list_G_l1.append(f(g1))#指标值列表
    for G2 in list_G2:
        for g2 in nx.connected_component_subgraphs(G2):
            list_G_l2.append(f(g2))
    #print list_G_l0, list_G_l1, list_G_l2
    G_l0 = np.mean(list_G_l0)
    G_l1 = np.mean(list_G_l1) #求均值 
    G_l2 = np.mean(list_G_l2)
    var_z1 = np.var(list_G_l1) #求方差
    var_z2 = np.var(list_G_l2)
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
      if valz == 0:
          spm=0
      else:
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
fh=open("3980_links.txt", 'rb') #4个连通子图
#fh=open("698_links.txt", 'rb') #4个连通子图
G=nx.read_edgelist(fh)
fh.close()
#print len(G.edges()),len(G.nodes())
list_G = list(nx.connected_component_subgraphs(G))#原始网络的连通子图
num = nx.number_connected_components(G)#连通组元数	

#置乱网络
list_G1 = []
list_G2 = []
nswap = 2 * len(G.edges())
maxtry = 100 * nswap
for i in range(0,1):
   G1 = nm.random_25k(G, nswap=nswap, max_tries=maxtry)#不同阶数的置乱只需改变调用的函数即可
   list_G1.append(G1)
   G2 = nx.Graph()
   for j in range(num):
       if len(list_G[j].nodes()) < 4: continue        
       g = nm.random_25kc(list_G[j], nswap=nswap, max_tries=maxtry)
       G2.add_edges_from(g.edges())
   list_G2.append(G2)
   i += 1

#画分布图的一些参数   
markers = ['o','s','x']
colors = ['r','b','g']
alphas = [1,0.5,1]
size = [30,60,80]
labels = ['yuanshi','bubaochiliantong','baochiliantong']


#==============================================================================
# #最大派系分布
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
# plt.xlabel('cliques')
# plt.ylabel('frequency')
# plt.show()
#==============================================================================


#富人俱乐部系数分布
l0 = nx.rich_club_coefficient(G,normalized=False)
l1 = nx.rich_club_coefficient(G1,normalized=False)
l2 = nx.rich_club_coefficient(G2,normalized=False)
j = 0
for l in [l0,l1,l2]:
    x = l.keys()
    y = l.values()
    plt.scatter(x,y,s=size[j],c=colors[j],label=labels[j],marker=markers[j],alpha=alphas[j])
    plt.plot(x,y,c=colors[j])
    j += 1
plt.legend(loc='upper left')
plt.xlabel('degree')
plt.ylabel('rich_club_coefficient')
plt.show()

#==============================================================================
# ##接近中心性分布
# l0 = map(lambda t:(t[1],t[0]), G.degree().items())  #(度,节点)组成的列表
# l1 = map(lambda t:(t[1],t[0]), G1.degree().items())
# l2 = map(lambda t:(t[1],t[0]), G2.degree().items())
# D0 = dict_degree_nodeslist(l0)
# D1 = dict_degree_nodeslist(l1)
# D2 = dict_degree_nodeslist(l2)
# list_D = [D0,D1,D2]
# j = 0
# bc = nx.closeness_centrality(G)
# for D in list_D:
#     bc1 = []
#     for i in range(len(D)):
#         t = D.values()[i]
#         bc1.extend([bc[e]for e in D.values()[i]])
#         D[D.keys()[i]] = np.mean(bc1)
#     x = D.keys()
#     y = D.values()
# #    print j,D
#     plt.scatter(x,y,s=size[j],c=colors[j],label=labels[j],marker=markers[j],alpha=alphas[j])
#     plt.plot(x,y,c=colors[j])
#     j += 1
# plt.legend(loc='lower right')
# plt.xlabel('degree')
# plt.ylabel('closeness_centrality')
# plt.show()
#==============================================================================

#==============================================================================
# ##介数分布
# l0 = map(lambda t:(t[1],t[0]), G.degree().items())  #(度,节点)组成的列表
# l1 = map(lambda t:(t[1],t[0]), G1.degree().items())
# l2 = map(lambda t:(t[1],t[0]), G2.degree().items())
# D0 = dict_degree_nodeslist(l0)
# D1 = dict_degree_nodeslist(l1)
# D2 = dict_degree_nodeslist(l2)
# list_D = [D0,D1,D2]
# j = 0
# bc = nx.betweenness_centrality(G)
# for D in list_D:
#     bc1 = []
#     for i in range(len(D)):
#         t = D.values()[i]
#         bc1.extend([bc[e]for e in D.values()[i]])
#         D[D.keys()[i]] = np.mean(bc1)
#     x = D.keys()
#     y = D.values()
# #    print j,D
#     plt.scatter(x,y,s=size[j],c=colors[j],label=labels[j],marker=markers[j],alpha=alphas[j])
#     plt.plot(x,y,c=colors[j])
#     j += 1
# plt.legend(loc='lower right')
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
# 
# for t in [l0,l1,l2]:
#     dt = {e:t.count(e)/float(len(t)) for e in set(t)}
#     x = dt.keys()
#     y = dt.values()
#     plt.scatter(x,y,s=size[j],c=colors[j],label=labels[j],marker=markers[j],alpha=alphas[j])
#     plt.plot(x,y,c=colors[j])
#     j += 1
# plt.legend(loc='upper right')
# plt.xlabel('degree')
# plt.ylabel('P')
# plt.show()
#==============================================================================

#==============================================================================
# #最短路径长度分布
# j = 0
# for g in [G,G1,G2]:
#     l0 = nx.all_pairs_shortest_path_length(g).values()
#     t = []
#     for i in range(len(l0)):
#         t.extend(l0[i].values())
#     dt = {e:t.count(e)/float(len(t)) for e in set(t)}
#     x = dt.keys()
#     y = dt.values()
#     plt.scatter(x,y,s=size[j],c=colors[j],label=labels[j],marker=markers[j],alpha=alphas[j])
#     plt.plot(x,y,c=colors[j])
#     j += 1
# plt.legend(loc='upper right')
# plt.xlabel('distance')
# plt.ylabel('P')
# plt.show()
#==============================================================================

#==============================================================================
# #聚类系数分布
# l0 = map(lambda t:(t[1],t[0]), G.degree().items())  #(度,节点)组成的列表
# l1 = map(lambda t:(t[1],t[0]), G1.degree().items())
# l2 = map(lambda t:(t[1],t[0]), G2.degree().items())
# list_degreenodes = [l0,l1,l2]
# j = 0
# for l in list_degreenodes:
#     D = dict_degree_nodeslist(l)
#     for i in range(len(D)):
#         D[D.keys()[i]] = nx.average_clustering(G, nodes=D.values()[i])
#     x = D.keys()
#     y = D.values()
# #    print j,D
#     plt.scatter(x,y,s=size[j],c=colors[j],label=labels[j],marker=markers[j],alpha=alphas[j])
#     plt.plot(x,y,c=colors[j])
#     j += 1
# plt.legend(loc='upper right')
# plt.xlabel('degree')
# plt.ylabel('samedegree_average_clustering')
# plt.show()
#==============================================================================


#==============================================================================
# #最临近节点的平均度分布
# l0 = map(lambda t:(t[1],t[0]), G.degree().items())  #(度,节点)组成的列表
# l1 = map(lambda t:(t[1],t[0]), G1.degree().items())
# l2 = map(lambda t:(t[1],t[0]), G2.degree().items())
# list_degreenodes = [l0,l1,l2]
# j = 0
# for l in list_degreenodes:
#     D = dict_degree_nodeslist(l)
# #    print D
#     for i in range(len(D)):
#         D[D.keys()[i]] = np.mean((nx.average_neighbor_degree(G, nodes=D.values()[i])).values())
#     x = D.keys()
#     y = D.values()
# #    print j,D
#     plt.scatter(x,y,s=size[j],c=colors[j],label=labels[j],marker=markers[j],alpha=alphas[j])
#     plt.plot(x,y,c=colors[j])
#     j += 1
# plt.legend(loc='upper right')
# plt.xlabel('degree')
# plt.ylabel('samedegree_average_neighbor_degree')
# plt.show()
#==============================================================================



#==============================================================================
# #微观性质
# def ave_degree(G):
#     d = G.degree().values()
#     return np.mean(d)
#     
# #平均聚类系数
# z1_average_clustering,z2_average_clustering = z(G,list_G1,list_G2,nx.average_clustering)
# 
# #匹配系数
# z1_assortativity_coefficient,z2_assortativity_coefficient = z(G,list_G1,list_G2,nx.degree_assortativity_coefficient)
# 
# #平均度
# z1_average_degree,z2_average_degree = z(G,list_G1,list_G2,ave_degree)
# 
# #print z1_average_clustering,z1_assortativity_coefficient,z1_average_degree
# sp1,sp2 = sp([z1_average_clustering,z1_assortativity_coefficient,z1_average_degree]),sp([z2_average_clustering,z2_assortativity_coefficient,z2_average_degree])
# plt.xticks((0,1,2),('average_clustering','assortativity_coefficient','average_degree'))
#==============================================================================


#==============================================================================
# #宏观性质
# #平均最短路径长度 (#graph must be connected)
# z1_path,z2_path = zc(G,list_G1,list_G2,nx.average_shortest_path_length)    
# #直径
# z1_diameter,z2_diameter = z(G,list_G1,list_G2,nx.diameter) 
# #连通组元数量
# z1_components,z2_components = z(G,list_G1,list_G2,nx.number_connected_components) 
# 
# sp1,sp2 = sp([z1_path,z1_diameter,z1_components]),sp([z2_path,z2_diameter,z2_components])
# plt.xticks((0,1,2),('average_shortest_path_length','diameter','number_connected_components'))
#==============================================================================

#plt.scatter(list(zip(*sp1)[0]),list(zip(*sp1)[1]),c='r',marker='o',label='blt')
#plt.scatter(list(zip(*sp2)[0]),list(zip(*sp2)[1]),c='b',marker='x',label='lt',s=60)
#plt.plot(list(zip(*sp1)[0]),list(zip(*sp1)[1]),c='r')
#plt.plot(list(zip(*sp2)[0]),list(zip(*sp2)[1]),c='b',ls=':',linewidth=5)
#plt.legend(loc='upper right')
#plt.xlabel('zhibiao')
#plt.ylabel('sp')
#plt.show()
#plt.show()         # test for git


