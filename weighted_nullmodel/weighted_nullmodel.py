# -*- coding: utf-8 -*-
import networkx as nx
import copy
import random

def random_0k(G0, nswap=1, max_tries=100):   #加权无向网络的0阶零模型
	#从网络中随机选一条边和两个不相连的节点，断边重连，且新连边权重等于断开的那条边的权重  
    if nswap > max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 3:
        raise nx.NetworkXError("Graph has less than three nodes.")
    G = copy.deepcopy(G0)
    n = 0
    swapcount = 0
    edges = G.edges()
    nodes = G.nodes()
    while swapcount < nswap:
        u,v = random.choice(edges)      #随机选一条要断开的边
        x,y = random.sample(nodes,2)    #随机找两个节点
        if (x,y) not in edges and (y,x) not in edges: #若x,y不相连,断边重连
            G.add_edge(x,y,weight=G[u][v]['weight'])            
            G.remove_edge(u,v)
            edges.append((x,y)) #更新边列表
            edges.remove((u,v))            
            swapcount+=1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n += 1
    return G
    
def random_0kc(G0, nswap=1, max_tries=100): #保持连通性的0阶零模型
    """
    在random_0k()的基础上增加连通性判断，若置乱后的网络不保持连通性则撤销该置乱操作
    注：G0为连通网络
    """
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if not nx.is_connected(G0):
        raise nx.NetworkXError("Graph not connected")
    if len(G0) < 3:
        raise nx.NetworkXError("Graph has less than three nodes.")
    G = copy.deepcopy(G0)
    n=0
    swapcount=0
    edges = G.edges()
    nodes = G.nodes()
    while swapcount < nswap:
        u,v = random.choice(edges)      #随机选一条要断开的边        
        x,y = random.sample(nodes,2)    #随机找两个节点
        if (x,y) not in edges and (y,x) not in edges: #若x,y不相连，则断边重连             
            G.add_edge(x,y,weight=G[u][v]['weight']) 
            G.remove_edge(u,v)                 
            edges.append((x,y))
            edges.remove((u,v))
            swapcount+=1
            if not nx.is_connected(G):          
                G.add_edge(u,v,weight=G[x][y]['weight'])  
                G.remove_edge(x,y)           
                edges.remove((x,y))
                edges.append((u,v))
                swapcount -= 1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
    return G

def random_1k(G0, nswap=1, max_tries=100):  #权重置乱的1阶零模型
    """
    随机取两条边 u-v 和 x-y, 且节点u和x,v和y无连边, 则断边重连,w(u,x)=w(u,v)及w(v,y)=w(x,y)
    """
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    n=0
    swapcount=0
    edges = G.edges()
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(edges,2)
        if len(set([u,v,x,y])) < 4: #防止自环           
            continue
        if (x,u) not in edges and (u,x) not in edges and (y,v) not in edges and (v,y) not in edges:     
            G.add_edges_from([(u,x),(v,y)])
            G[u][x]['weight'] = G[u][v]['weight']  
            G[v][y]['weight'] = G[x][y]['weight'] 
            G.remove_edges_from([(u,v),(x,y)])
            edges.extend([(u,x),(v,y)])
            edges.remove((u,v))
            edges.remove((x,y))
            swapcount+=1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
    return G

def random_1kc(G0, nswap=1, max_tries=100):     #保持连通性下权重置乱的1阶零模型
    """
    在random_1k()的基础上增加连通性判断，若置乱后的网络不保持连通性则撤销该置乱操作
    注：G0为连通网络
    """
    if not nx.is_connected(G0):
       raise nx.NetworkXError("Graph not connected")
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    n=0
    swapcount=0
    edges = G.edges()
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(edges,2) 
        if len(set([u,v,x,y])) < 4: #防止自环           
            continue
        if (x,u) not in edges and (u,x) not in edges and (y,v) not in edges and (v,y) not in edges:     
            G.add_edges_from([(u,x),(v,y)])
            G[u][x]['weight'] = G[u][v]['weight']  
            G[v][y]['weight'] = G[x][y]['weight'] 
            G.remove_edges_from([(u,v),(x,y)])
            edges.extend([(u,x),(v,y)])
            edges.remove((u,v))
            edges.remove((x,y))
            swapcount+=1
            if not nx.is_connected(G):
                G.add_edges_from([(u,v),(x,y)])
                G[u][v]['weight'] = G[u][x]['weight']  
                G[x][y]['weight'] = G[v][y]['weight']
                G.remove_edges_from([(u,x),(v,y)])
                edges.remove((u,x))
                edges.remove((v,y))
                edges.extend([(u,v),(x,y)])
                swapcount -= 1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
    return G

def random_sw(G0, nswap=1, max_tries=100): #等权重置乱
    """
    任选两条权重相同的边u-v,x-y,若u-x,v-y不相连，则断边重连
    
    """
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    n=0
    swapcount=0
    edges = G.edges()
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(edges,2)
        if len(set([u,v,x,y])) < 4: #防止自环           
            continue
        if G[u][v]['weight']!=G[x][y]['weight']:
            continue
        if (x,u) not in edges and (u,x) not in edges and (y,v) not in edges and (v,y) not in edges:     
            G.add_edges_from([(u,x),(v,y)])
            G[u][x]['weight'] = G[u][v]['weight']  
            G[v][y]['weight'] = G[x][y]['weight'] 
            G.remove_edges_from([(u,v),(x,y)])
            edges.extend([(u,x),(v,y)])
            edges.remove((u,v))
            edges.remove((x,y))
            swapcount+=1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
    return G

def random_swc(G0, nswap=1, max_tries=100): #保持联通性的等权重置乱
    """
    增加联通性判断即可
    """
    if not nx.is_connected(G0):
       raise nx.NetworkXError("Graph not connected")
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    
    G = copy.deepcopy(G0)
    n=0
    swapcount=0
    edges = G.edges()
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(edges,2)
        if len(set([u,v,x,y])) < 4: #防止自环           
            continue
        if G[u][v]['weight']!=G[x][y]['weight']:
            continue
        if (x,u) not in edges and (u,x) not in edges and (y,v) not in edges and (v,y) not in edges:     
            G.add_edges_from([(u,x),(v,y)])
            G[u][x]['weight'] = G[u][v]['weight']  
            G[v][y]['weight'] = G[x][y]['weight'] 
            G.remove_edges_from([(u,v),(x,y)])
            edges.extend([(u,x),(v,y)])
            edges.remove((u,v))
            edges.remove((x,y))
            swapcount+=1
            if not nx.is_connected(G):
                G.add_edges_from([(u,v),(x,y)])
                G[u][v]['weight'] = G[u][x]['weight']  
                G[x][y]['weight'] = G[v][y]['weight']
                G.remove_edges_from([(u,x),(v,y)])
                edges.remove((v,y))
                edges.remove((u,x))
                edges.extend([(u,v),(x,y)])
                swapcount -= 1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
    return G

def random_w(G0, nswap=1, max_tries=100): #权重置乱
    """
    任取两条权重不相同的边，互换权重
    """  
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 3:
        raise nx.NetworkXError("Graph has less than three nodes.")
        
    G = copy.deepcopy(G0)
    n=0
    swapcount=0
    edges = G.edges()
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(edges,2)
        if G[u][v]['weight'] != G[x][y]['weight']:
            G[u][v]['weight'],G[x][y]['weight']=G[x][y]['weight'],G[u][v]['weight']
            swapcount+=1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
    return G
            

def rich_club_creat(G0, k, max_tries=100):
    """
    节点的强度 = 节点所有连边的权重值之和
    根据节点的强度将所有节点分成富节点和非富节点
    任选两条边(富节点和非富节点的连边)，若富节点间无连边，非富节点间无连边，则断边重连
    达到最大尝试次数或全部富节点间都有连边，循环结束
    强度大于k的节点为富节点
    """
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    edges = G.edges()
    nodes = G.nodes()
    rnodes = [e for e in nodes if G.degree(e,weight='weight')>=k]     #全部富节点
    len_redges = len([e for e in edges if e[0] in rnodes and e[1] in rnodes]) #网络中已有的富节点和富节点的连边数
    len_possible_redges = len(rnodes)*(len(rnodes)-1)/2        #全部富节点间都有连边的边数
    n = 0
    while len_redges < len_possible_redges:
        u,x = random.sample(rnodes,2)                       #任选两个富节点
        candidate_v = [e for e in list(G[u]) if G.degree(e,weight='weight')<k]
        candidate_y = [e for e in list(G[x]) if G.degree(e,weight='weight')<k]
        if candidate_v != [] and candidate_y != []:
            v = random.choice(candidate_v) #非富节点
            y = random.choice(candidate_y)          
            if len(set([u,v,x,y])) < 4: #防止自环           
                continue
            if (x not in G[u]) and (y not in G[v]):
                G.add_edges_from([(u,x),(v,y)])
                G[u][x]['weight'] = G[u][v]['weight']  
                G[v][y]['weight'] = G[x][y]['weight'] 
                G.remove_edges_from([(u,v),(x,y)])
                len_redges += 1
        if n >= max_tries:
            print ('Maximum number of attempts (%s) exceeded '%n)
            break
        n += 1
    return G

def rich_club_creatc(G0, k,max_tries=100):
    """
    保持连通性：断边重连后增加连通性判断，若不保持连通性则撤销该断边重连操作
    """
    if not nx.is_connected(G0):
       raise nx.NetworkXError("Graph not connected")
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    edges = G.edges()
    nodes = G.nodes()
    rnodes = [e for e in nodes if G.degree(e,weight='weight')>=k]     #全部富节点
    len_redges = len([e for e in edges if e[0] in rnodes and e[1] in rnodes]) #网络中已有的富节点和富节点的连边数
    len_possible_edges = len(rnodes)*(len(rnodes)-1)/2        #全部富节点间都有连边的边数
    n = 0
    while len_redges < len_possible_edges:
        u,x = random.sample(rnodes,2)                       #任选两个富节点
        candidate_v = [e for e in list(G[u]) if G.degree(e,weight='weight')<k]
        candidate_y = [e for e in list(G[x]) if G.degree(e,weight='weight')<k]
        if candidate_v != [] and candidate_y != []:
            v = random.choice(candidate_v) #非富节点
            y = random.choice(candidate_y)          
            if len(set([u,v,x,y])) < 4: #防止自环           
                continue
            if (x not in G[u]) and (y not in G[v]):
                G.add_edges_from([(u,x),(v,y)])
                G[u][x]['weight'] = G[u][v]['weight']  
                G[v][y]['weight'] = G[x][y]['weight'] 
                G.remove_edges_from([(u,v),(x,y)])
                len_redges += 1
                if not nx.is_connected(G):
                    G.add_edges_from([(u,v),(x,y)])
                    G[u][v]['weight'] = G[u][x]['weight']  
                    G[x][y]['weight'] = G[v][y]['weight']
                    G.remove_edges_from([(u,x),(v,y)])
                    len_redges -= 1
        if n >= max_tries:
            print ('Maximum number of attempts (%s) exceeded '%n)
            break
        n += 1
    return G


def rich_club_break(G0, k, max_tries=100):
    """
    富边：富节点和富节点的连边
    非富边：非富节点和非富节点的连边
    任选两条边(一条富边，一条非富边)，若富节点和非富节点间无连边，则断边重连
    达到最大尝试次数或无富边或无非富边，循环结束
    """    
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    edges = G.edges()
    nodes = G.nodes()
    rnodes = [e for e in nodes if G.degree(e,weight='weight')>=k]     #全部富节点
    redges = [e for e in edges if e[0] in rnodes and e[1] in rnodes] #网络中已有的富节点和富节点的连边
    pedges = [e for e in edges if e[0] not in rnodes and e[1] not in rnodes] #网络中已有的非富节点和非富节点的连边
#    len_redges = len(redges)
#    len_pedges = len(pedges)
    n = 0
    while redges and pedges:
        u,v = random.choice(redges)              #随机选一条富边
        x,y = random.choice(pedges)           #随机选一条非富边              
        if (x,u) not in edges and (u,x) not in edges and (v,y) not in edges and (y,v) not in edges:              
            G.add_edges_from([(u,x),(v,y)])
            G[u][x]['weight'] = G[u][v]['weight']  
            G[v][y]['weight'] = G[x][y]['weight'] 
            G.remove_edges_from([(u,v),(x,y)])
            edges.extend([(u,x),(v,y)])
            edges.remove((u,v))
            edges.remove((x,y))
            redges.remove((u,v))
            pedges.remove((x,y))
        if n >= max_tries:
            print ('Maximum number of attempts (%s) exceeded '%n)
            break
        n += 1
    return G
    
    
def rich_club_breakc(G0, k, max_tries=100):
    """
    保持连通性：断边重连后增加连通性判断，若不保持连通性则撤销该断边重连操作
    """
    if not nx.is_connected(G0):
       raise nx.NetworkXError("Graph not connected")
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    edges = G.edges()
    nodes = G.nodes()
    rnodes = [e for e in nodes if G.degree(e,weight='weight')>=k]     #全部富节点
    redges = [e for e in edges if e[0] in rnodes and e[1] in rnodes] #网络中已有的富节点和富节点的连边
    pedges = [e for e in edges if e[0] not in rnodes and e[1] not in rnodes] #网络中已有的非富节点和非富节点的连边
#    len_redges = len(redges)
#    len_pedges = len(pedges)
    n = 0
    while redges and pedges:
        u,v = random.choice(redges)              #随机选一条富边
        x,y = random.choice(pedges)           #随机选一条非富边              
        if (x,u) not in edges and (u,x) not in edges and (v,y) not in edges and (y,v) not in edges:              
            G.add_edges_from([(u,x),(v,y)])
            G[u][x]['weight'] = G[u][v]['weight']  
            G[v][y]['weight'] = G[x][y]['weight'] 
            G.remove_edges_from([(u,v),(x,y)])
            edges.extend([(u,x),(v,y)])
            edges.remove((u,v))
            edges.remove((x,y))
            redges.remove((u,v))
            pedges.remove((x,y))
            if not nx.is_connected(G):
                G.add_edges_from([(u,v),(x,y)])
                G[u][v]['weight'] = G[u][x]['weight']  
                G[x][y]['weight'] = G[v][y]['weight']
                G.remove_edges_from([(u,x),(v,y)])
                edges.remove((u,x));edges.remove((v,y))
                edges.extend([(u,v),(x,y)])
                redges.extend([(u,v),(x,y)])
        if n >= max_tries:
            print ('Maximum number of attempts (%s) exceeded '%n)
            break
        n += 1
    return G


#匹配特性
def assort_mixing(G0, nswap=1, max_tries=100):
    """
    让强度大的节点和强度大的节点相连
    """       
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    n=0
    swapcount=0
#    nodes = G.nodes()
    edges = G.edges()
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(edges,2) #任选两条边
        if len(set([u,v,x,y]))<4:
            continue
        a,b,c,d = zip(*sorted(G.degree([u,v,x,y],weight='weight').items(),key=lambda d:d[1],reverse=True))[0]
        if (a,b) not in edges and (b,a)not in edges and (c,d) not in edges and (d,c)not in edges:
            G.add_edges_from([(a,b),(c,d)])
            G[a][b]['weight'] = G[u][v]['weight']  
            G[c][d]['weight'] = G[x][y]['weight'] 
            G.remove_edges_from([(u,v),(x,y)])
            edges.extend([(a,b),(c,d)])
            edges.remove((u,v))
            edges.remove((x,y))
            swapcount += 1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n += 1       
    return G
    
def assort_mixingc(G0,nswap=1, max_tries=100):     
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    n=0
    swapcount=0
#    nodes = G.nodes()
    edges = G.edges()
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(edges,2) #任选两条边
        if len(set([u,v,x,y]))<4:
            continue
        a,b,c,d = zip(*sorted(G.degree([u,v,x,y],weight='weight').items(),key=lambda d:d[1],reverse=True))[0]
        if (a,b) not in edges and (b,a)not in edges and (c,d) not in edges and (d,c)not in edges:
            G.add_edges_from([(a,b),(c,d)])
            G[a][b]['weight'] = G[u][v]['weight']  
            G[c][d]['weight'] = G[x][y]['weight'] 
            G.remove_edges_from([(u,v),(x,y)])
            edges.extend([(a,b),(c,d)])
            edges.remove((u,v))
            edges.remove((x,y))
            swapcount += 1
            if not nx.is_connected(G):
                G.add_edges_from([(u,v),(x,y)])
                G[u][v]['weight'] = G[a][b]['weight']  
                G[x][y]['weight'] = G[c][d]['weight']
                G.remove_edges_from([(a,b),(c,d)])
                edges.remove((a,b))
                edges.remove((c,d))
                edges.extend([(u,v),(x,y)])
                swapcount -= 1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n += 1       
    return G


def disassort_mixing(G0, nswap=1, max_tries=100):     #异配
    """
    让强度大的节点和强度小的节点相连
    """       
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    n=0
    swapcount=0
#    nodes = G.nodes()
    edges = G.edges()
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(edges,2) #任选两条边
        if len(set([u,v,x,y]))<4:
            continue
        a,b,c,d = zip(*sorted(G.degree([u,v,x,y],weight='weight').items(),key=lambda d:d[1],reverse=True))[0]
        if (a,d) not in edges and (d,a) not in edges and (c,b) not in edges and (b,c)not in edges:
            G.add_edges_from([(a,d),(b,c)])
            G[a][d]['weight'] = G[u][v]['weight']  
            G[b][c]['weight'] = G[x][y]['weight'] 
            G.remove_edges_from([(u,v),(x,y)])
            edges.extend([(a,d),(b,c)])
            edges.remove((u,v))
            edges.remove((x,y))
            swapcount += 1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n += 1       
    return G
    
def disassort_mixingc(G0, nswap=1, max_tries=100):    
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    n=0
    swapcount=0
#    nodes = G.nodes()
    edges = G.edges()
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(edges,2) #任选两条边
        if len(set([u,v,x,y]))<4:
            continue
        a,b,c,d = zip(*sorted(G.degree([u,v,x,y],weight='weight').items(),key=lambda d:d[1],reverse=True))[0]
        if (a,d) not in edges and (d,a)not in edges and (b,c) not in edges and (c,b)not in edges:
            G.add_edges_from([(a,d),(b,c)])
            G[a][d]['weight'] = G[u][v]['weight']  
            G[b][c]['weight'] = G[x][y]['weight'] 
            G.remove_edges_from([(u,v),(x,y)])
            edges.extend([(a,d),(b,c)])
            edges.remove((u,v))
            edges.remove((x,y))
            swapcount += 1
            if not nx.is_connected(G):
                G.add_edges_from([(u,v),(x,y)])
                G[u][v]['weight'] = G[a][d]['weight']  
                G[x][y]['weight'] = G[b][c]['weight']
                G.remove_edges_from([(a,d),(b,c)])
                edges.remove((a,d))
                edges.remove((b,c))
                edges.extend([(u,v),(x,y)])
                swapcount -= 1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n += 1       
    return G    
        
def random_1kd(G0, nswap=1, max_tries=100): 
    """
    随机取两条边 u->v 和 x->y, 若u->y,x->v不存在, 断边重连
    """
    if not G0.is_directed():
        raise nx.NetworkXError("Graph not directed")
    if nswap>max_tries:
            raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    n = 0
    swapcount = 0
    edges = G.edges()
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(edges,2)
        if len(set([u,v,x,y]))<4:            
            continue
        if (x,v) not in edges and (u,y) not in edges:
            G.add_edges_from([(u,y),(x,v)])
            G[u][y]['weight']=G[u][v]['weight']
            G[x][v]['weight']=G[x][y]['weight']
            G.remove_edges_from([(u,v),(x,y)])
            edges.extend([(u,y),(x,v)])
            edges.remove((u,v))
            edges.remove((x,y))
            swapcount+=1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
    return G
    
def random_1kcd(G0, nswap=1, max_tries=100): #保持连通性
    """
    随机取两条边 u->v 和 x->y, 若u->y,x->v不存在, 断边重连
    """
    if not G0.is_directed():
        raise nx.NetworkXError("Graph not directed")
    if nswap>max_tries:
            raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    n = 0
    swapcount = 0
    edges = G.edges()
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(edges,2)
        if len(set([u,v,x,y]))<4:            
            continue
        if (x,v) not in edges and (u,y) not in edges:
            G.add_edges_from([(u,y),(x,v)])
            G[u][y]['weight']=G[u][v]['weight']
            G[x][v]['weight']=G[x][y]['weight']
            G.remove_edges_from([(u,v),(x,y)])
            G.remove_edge(x,y)
            edges.extend([(u,y),(x,v)])
            edges.remove((u,v))
            edges.remove((x,y))
            swapcount+=1
            if not nx.is_connected(G):          
                G.add_edges_from([(u,v),(x,y)])  
                G[u][v]['weight']=G[u][y]['weight']
                G[x][y]['weight']=G[x][v]['weight']
                G.remove_edges_from([(u,y),(x,v)])
                edges.extend([(u,v),(x,y)])
                edges.remove(u,y);edges.remove(x,v)
                swapcount -= 1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
    return G
    
def random_out_lw(G0, nswap=1, max_tries=100): #局部权重置乱(出)
    """
    任取同一节点的两条权重不相同的边，互换权重
    """ 
    if not G0.is_directed():
        raise nx.NetworkXError("Graph not directed")
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 3:
        raise nx.NetworkXError("Graph has less than three nodes.")
        
    G = copy.deepcopy(G0)
    n=0
    swapcount=0
    nodes = G.nodes()
    while swapcount < nswap:
        u = random.choice(nodes)
        candidate_edges = G.out_edges(u)
        if len(candidate_edges) < 2:
            continue
        (u,v),(u,x) = random.sample(candidate_edges,2)
        if G[u][v]['weight'] != G[u][x]['weight']:
            G[u][v]['weight'],G[u][x]['weight']=G[u][x]['weight'],G[u][v]['weight']
            swapcount+=1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
    return G
    
def random_in_lw(G0, nswap=1, max_tries=100): #局部权重置乱(入)
    """
    任取同一节点的两条权重不相同的边，互换权重
    """ 
    if not G0.is_directed():
        raise nx.NetworkXError("Graph not directed")
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 3:
        raise nx.NetworkXError("Graph has less than three nodes.")
        
    G = copy.deepcopy(G0)
    n=0
    swapcount=0
    nodes = G.nodes()
    while swapcount < nswap:
        x = random.choice(nodes)
        candidate_edges = G.in_edges(x)
        if len(candidate_edges) < 2:
            continue
        (u,x),(v,x) = random.sample(candidate_edges,2)
        if G[u][x]['weight'] != G[v][x]['weight']:
            G[u][x]['weight'],G[v][x]['weight']=G[v][x]['weight'],G[u][x]['weight']
            swapcount+=1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
    return G
