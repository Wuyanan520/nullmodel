# -*- coding: utf-8 -*-
import random
import networkx as nx
import copy
import datetime

def edges_swap_0k(G0, nswap=1, max_tries=100):   #时变网络的连边置乱算法
    """
    从网络中随机选一条边和两个不相连的节点，断边重连，且新连边时序等于断开的那条边的时序  
    """
    if nswap > max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 3:
        raise nx.NetworkXError("Graph has less than three nodes.")
    
    n = 0
    swapcount = 0
    G = copy.deepcopy(G0)
    nodes = G.nodes()
    
    while swapcount < nswap:
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n += 1
        x,u = random.sample(nodes,2)    #随机找两个节点
        candicate_y = [no for no in nodes if no not in list(G[x])]
        if list(G[u]) and candicate_y:
            v = random.choice(list(G[u])) #任选一条边u-v
            y = random.choice(candicate_y)  #任选一条不相连边x-y
        else:
            continue
        if len(set([u,v,x,y])) < 3: #防止自环           
            continue
        for i in range(G.number_of_edges(u,v)):
            G.add_edge(x,y,key=i,timestamp=G[u][v][i]['timestamp'])            
            G.remove_edge(u,v,key=i)       
            swapcount+=1
        
    return G
    
    
def edges_swap_1k(G0, nswap=1, max_tries=100):  #时变网络的连边置乱算法
    """
    随机取两条边 u-v 和 x-y, 且节点u和x,v和y无连边, 则断边重连且t(u,x)=t(u,v)及t(v,y)=t(x,y)
    """
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    
    n=0
    swapcount=0
    G = copy.deepcopy(G0)
    keys,degrees=zip(*G.degree().items()) 
    cdf=nx.utils.cumulative_distribution(degrees)
    
    while swapcount < nswap:
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue 
        u=keys[ui] 
        x=keys[xi]
        v=random.choice(list(G[u]))
        y=random.choice(list(G[x]))        
        if len(set([u,v,x,y])) < 4: #防止自环           
            continue
        if y not in G[u] and v not in G[x]: 
            for i in G[u][v].keys():
#                print G[u][v].keys(), i
                G.add_edge(u,y,key=i,timestamp=G[u][v][i]['timestamp'])
                G.remove_edge(u,v,key=i)
            for j in G[x][y].keys():
#                print G[x][y].keys(), j
                G.add_edge(x,v,key=j,timestamp=G[x][y][j]['timestamp']) 
                G.remove_edge(x,y,key=j)
#            G.remove_edges_from([(u,v),(x,y)])#仅移除一条边
            swapcount+=1        
    return G
    

def time_swap(G0, nswap=1, max_tries=100):  #时变网络的时间置乱算法
    """
    在保证单条边上不出现相同时间戳的前提下，分别从两条边上任选一个时间戳互换
    """
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 3:
        raise nx.NetworkXError("Graph has less than three nodes.")
    
    n=0
    swapcount=0
    G = copy.deepcopy(G0)
    keys,degrees=zip(*G.degree().items()) 
    cdf=nx.utils.cumulative_distribution(degrees)
    while swapcount < nswap:
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue 
        u=keys[ui] 
        x=keys[xi]
        v=random.choice(list(G[u]))
        y=random.choice(list(G[x]))
        if len(set([u,v,x,y])) < 3: #保证从两条边上选时间戳           
            continue
        key1 = random.choice(G[u][v].keys())
        key2 = random.choice(G[x][y].keys())
        stamp1 = G[u][v][key1]['timestamp']
        stamp2 = G[x][y][key2]['timestamp']
        if stamp1 == stamp2 or {'timestamp':stamp1} in G[x][y].values() or {'timestamp':stamp2} in G[u][v].values():
            continue
        else:
            G[u][v][key1]['timestamp'] = stamp2
            G[x][y][key2]['timestamp'] = stamp1
            swapcount+=1        
    return G
    
def time_random(G0, nswap=1, max_tries=100,mins=1000000,maxs=31556926):  #时变网络的时间随机化算法
    """
    在保证单条边上不出现相同时间戳的前提下，任选一个时间戳用在该网络时间范围内的新生时间戳代替
    """
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 3:
        raise nx.NetworkXError("Graph has less than three nodes.")
    
    n=0
    swapcount=0
    G = copy.deepcopy(G0)
    while swapcount < nswap:
#        print swapcount
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
        u,v = random.choice(G.edges())
        key1 = random.choice(G[u][v].keys())
        stamp1 = G[u][v][key1]['timestamp']
        stamp2 = random.randrange(mins,maxs)
        if stamp1 == stamp2 or {'timestamp':stamp2} in G[u][v].values():
            continue
        else:
            G[u][v][key1]['timestamp'] = stamp2
            swapcount+=1
        print n,swapcount
    return G
   
def timeweight_swap(G0, nswap=1, max_tries=100):  #时变网络的时权置乱算法
    """
    任选两条边，将其上的时间序列互换
    """
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 3:
        raise nx.NetworkXError("Graph has less than three nodes.")
    
    n=0
    swapcount=0
    G = copy.deepcopy(G0)
    keys,degrees=zip(*G.degree().items()) 
    cdf=nx.utils.cumulative_distribution(degrees)
    while swapcount < nswap:
        if swapcount%100 == 0:
            print swapcount
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue 
        u=keys[ui] 
        x=keys[xi]
        v=random.choice(list(G[u]))
        y=random.choice(list(G[x]))
        if len(set([u,v,x,y])) < 3: #保证从两条边上选          
            continue
        stamp1 = []
        stamp2 = []        
#        print G.number_of_edges(u,v),G.number_of_edges(x,y)
        for i in G[u][v].keys():
            stamp1.append(G[u][v][i]['timestamp'])
            G.remove_edge(u,v,key=i)
        for i in G[x][y].keys():
            stamp2.append(G[x][y][i]['timestamp'])
            G.remove_edge(x,y,key=i)
#        print G.number_of_edges(u,v),G.number_of_edges(x,y)
        for i in range(len(stamp2)):
            G.add_edge(u,v,key=i,timestamp=stamp2[i])
        for i in range(len(stamp1)):
            G.add_edge(x,y,key=i,timestamp=stamp1[i])
#        print G.number_of_edges(u,v),G.number_of_edges(x,y)
        swapcount+=1        
    return G
    
def sametimeweight_swap(G0, nswap=1, max_tries=100):  #时变网络的等时权置乱算法
    """
    任选两条权重相等的边，将其上的时间序列互换
    """
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 3:
        raise nx.NetworkXError("Graph has less than three nodes.")
    
    n=0
    swapcount=0
    G = copy.deepcopy(G0)
    keys,degrees=zip(*G.degree().items()) 
    cdf=nx.utils.cumulative_distribution(degrees)
    while swapcount < nswap:
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue 
        u=keys[ui] 
        x=keys[xi]
        v=random.choice(list(G[u]))
        y=random.choice(list(G[x]))
        if len(set([u,v,x,y])) < 3: #保证从两条边上选          
            continue
        if G.number_of_edges(u,v) == G.number_of_edges(x,y):#两条边权重相等
            stamp1 = []
            stamp2 = []        
#            print G.number_of_edges(u,v),G.number_of_edges(x,y)
            for i in G[u][v].keys():
                stamp1.append(G[u][v][i]['timestamp'])
                G.remove_edge(u,v,key=i)
            for i in G[x][y].keys():
                stamp2.append(G[x][y][i]['timestamp'])
                G.remove_edge(x,y,key=i)
#            print G.number_of_edges(u,v),G.number_of_edges(x,y)
            for i in range(len(stamp2)):
                G.add_edge(u,v,key=i,timestamp=stamp2[i])
            for i in range(len(stamp1)):
                G.add_edge(x,y,key=i,timestamp=stamp1[i])
#            print G.number_of_edges(u,v),G.number_of_edges(x,y)
            swapcount+=1        
    return G


#保持个体天、月、周模式的时间置乱算法
def time_SameMode_swap(G0, nswap=1, max_tries=100, mode='day'):  
    """
    在保证单条边上不出现相同时间戳的前提下，分别从两条边上任选一个时间戳（具有相同的天/月/周模式）互换
    """
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 3:
        raise nx.NetworkXError("Graph has less than three nodes.")
    
    n=0
    swapcount=0
    G = copy.deepcopy(G0)
    keys,degrees=zip(*G.degree().items()) 
    cdf=nx.utils.cumulative_distribution(degrees)
    while swapcount < nswap:
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue 
        u=keys[ui] 
        x=keys[xi]
        v=random.choice(list(G[u]))
        y=random.choice(list(G[x]))
        if len(set([u,v,x,y])) < 3: #保证从两条边上选时间戳           
            continue
        key1 = random.choice(G[u][v].keys())
        key2 = random.choice(G[x][y].keys())
        stamp1 = G[u][v][key1]['timestamp']
        stamp2 = G[x][y][key2]['timestamp']
        #Python下将时间戳转换到日期
        stamp1_date = datetime.datetime.utcfromtimestamp(stamp1)
        stamp2_date = datetime.datetime.utcfromtimestamp(stamp2)
        if mode == 'day': #保持个体天模式
            if stamp1_date.day != stamp2_date.day or {'timestamp':stamp1} in G[x][y].values() or {'timestamp':stamp2} in G[u][v].values():
                continue
        elif mode == 'week': #保持个体周模式
            if stamp1_date.weekday() != stamp2_date.weekday() or {'timestamp':stamp1} in G[x][y].values() or {'timestamp':stamp2} in G[u][v].values():
                continue
        elif mode == 'month': #保持个体月模式
            if stamp1_date.month != stamp2_date.month or {'timestamp':stamp1} in G[x][y].values() or {'timestamp':stamp2} in G[u][v].values():
                continue
        else:
            G[u][v][key1]['timestamp'] = stamp2
            G[x][y][key2]['timestamp'] = stamp1
        swapcount+=1        
    return G
    
def time_randomswap(G0, nswap=1, max_tries=100):  #时变网络的接触置乱算法
    """
    在保证单条边上不出现相同时间戳的前提下，将时间戳和连边随机组合
    """
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 3:
        raise nx.NetworkXError("Graph has less than three nodes.")
    
    n=0
    swapcount=0
    G = copy.deepcopy(G0)
    keys,degrees=zip(*G.degree().items()) 
    cdf=nx.utils.cumulative_distribution(degrees)
    while swapcount < nswap:
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
        #任选两条边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue 
        u=keys[ui] 
        x=keys[xi]
        v=random.choice(list(G[u]))
        y=random.choice(list(G[x]))
        if len(set([u,v,x,y])) < 3: #保证从两条边上选          
            continue
        #从u-v上任选一个时间戳
        key1 = random.choice(G[u][v].keys())
        stamp1 = G[u][v][key1]['timestamp']
        if {'timestamp':stamp1} in G[x][y].values() or G.number_of_edges(u,v) < 2:
            continue
        else:
            G.remove_edge(u,v,key=key1)
            G.add_edge(x,y,timestamp=stamp1)
            swapcount+=1        
    return G
    
#时间倒转后的网络
def time_reverse(fh):
    fh1 = fh.sort_values(by='timestamp')
    ts_list = list(fh1['timestamp'])
    ts_list.reverse()
    fh1['timestamp'] = ts_list
    return fh1
