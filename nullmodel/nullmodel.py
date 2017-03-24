import networkx as nx
import random
import copy


def ER_model(G0):
    n=len(G0.nodes())
    m=len(G0.edges())
    p=2.0*m/(n*n)
    G = nx.random_graphs.erdos_renyi_graph(n, p, directed=False)
    return G

def config_model(G0):
    degree_seq = list(G0.degree().values()) 
    G = nx.configuration_model(degree_seq) 
    return G

def random_0k(G0, nswap=1, max_tries=100):    #基于随机断边重连的0阶零模型
    G = copy.deepcopy(G0)      
    if nswap>max_tries:
            raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G) < 3:
        raise nx.NetworkXError("Graph has less than three nodes.")
    n = 0
    swapcount = 0
    while swapcount < nswap:
        u,v = random.choice(G.edges())      #随机选网络中的一条要断开的边
        x,y = random.sample(G.nodes(),2)    #随机找两个不相连的节点
        if (x,y) not in G.edges() and (y,x) not in G.edges():
            G.remove_edge(u,v)              #断旧边
            G.add_edge(x,y)                 #连新边
            swapcount+=1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n += 1
    return G
    
def random_0kc(G0, nswap=1, max_tries=100): #保持连通性的情况下基于随机断边重连的0阶零模型
    """
    在random_0k()的基础上增加连通性判断，若置乱后的网络不保持连通性则撤销该置乱操作
    注：G0为连通网络
    """
    G = copy.deepcopy(G0)
    if nswap>max_tries:
            raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if not nx.is_connected(G):
        raise nx.NetworkXError("Graph not connected")
    if len(G) < 3:
        raise nx.NetworkXError("Graph has less than three nodes.")
    n=0
    swapcount=0
    while swapcount < nswap:
        swapped = []
        u,v = random.choice(G.edges())      #随机选网络中的一条要断开的边        
        x,y = random.sample(G.nodes(),2)    #随机找两个不相连的节点
        if (x,y) not in G.edges() and (y,x) not in G.edges():
            G.remove_edge(u,v)              #断旧边
            G.add_edge(x,y)                 #连新边
            swapped.append((u, v, x, y))
            swapcount+=1
        if not nx.is_connected(G):  
            while swapped:
                (u, v, x, y) = swapped.pop()
                G.remove_edge(x,y)          #撤销连新边操作
                G.add_edge(u,v)             #撤销断边操作
                swapcount -= 1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
    return G

def random_1k(G0, nswap=1, max_tries=100):  #随机断边重连的1阶零模型
    """
    随机取两条边 u-v 和 x-y, 且节点u和x,v和y无连边, 则断边重连
    """
    if nswap>max_tries:
            raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    n=0
    swapcount=0
    keys,degrees=zip(*G.degree().items()) 
    cdf=nx.utils.cumulative_distribution(degrees)  
    while swapcount < nswap:
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue
        u=keys[ui] 
        x=keys[xi]
        v=random.choice(list(G[u]))
        y=random.choice(list(G[x]))
        if len(set([u,v,x,y]))<4:
            continue
        if v==y:
            continue 
        if (y not in G.neighbors(u)) and (v not in G.neighbors(x)) and ((u,v) in G.edges()) and ((x,y) in G.edges()):  
            G.add_edge(u,y)                           #断旧边
            G.add_edge(v,x)
            G.remove_edge(u,v)                        #连新边
            G.remove_edge(x,y)
            swapcount+=1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
    return G

def random_1kc(G0, nswap=1, max_tries=100):     #保持连通性下随机断边重连的1阶零模型
    """
    在random_1k()的基础上增加连通性判断，若置乱后的网络不保持连通性则撤销该置乱操作
    注：G0为连通网络
    """
    if not nx.is_connected(G0):
       raise nx.NetworkXError("Graph not connected")
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    n=0
    swapcount=0
    keys,degrees=zip(*G.degree().items()) 
    cdf=nx.utils.cumulative_distribution(degrees)  
    while swapcount < nswap:
        swapped=[]
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        if ui==xi:
            continue 
        u=keys[ui] 
        x=keys[xi]
        v=random.choice(list(G[u]))
        y=random.choice(list(G[x]))
        if v==y:
            continue
        if len(set([u,v,x,y]))<4:
            continue
        if (y not in G.neighbors(u)) and (v not in G.neighbors(x)) and ((u,v) in G.edges()) and ((x,y) in G.edges()):
            G.add_edge(u,y)         
            G.add_edge(v,x)
            G.remove_edge(u,v)      
            G.remove_edge(x,y)
            swapped.append((u,v,x,y))
            swapcount+=1
        if not nx.is_connected(G):      
            while swapped:
                (u, v, x, y) = swapped.pop()
                G.add_edge(u,v)         #撤销断边操作
                G.add_edge(x,y)
                G.remove_edge(u,x)      #撤销连新边操作
                G.remove_edge(v,y)
                swapcount -= 1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
    return G

def random_2k(G0, nswap=1, max_tries=100):
    """
    2阶置乱是在1阶置乱的基础上，增加约束条件：
    要求断开的边u-v和新连的边u-y中v,y度相同
    """
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    n=0
    swapcount=0
    while swapcount < nswap:
        (u,x)=random.sample(G.nodes(),2)     #随机找两个不相连的点
        v=random.choice(list(G[u]))
        y=random.choice(list(G[x]))
        if len(set([u,v,x,y]))<4:
            continue
        if G.degree(v)!=G.degree(y) or v==y:
            continue                        #若节点v,y度不相同，重新选择
        if (y not in G.neighbors(u)) and (v not in G.neighbors(x)) and ((u,v) in G.edges()) and ((x,y) in G.edges()):
            G.add_edge(u,y)
            G.add_edge(x,v)
            G.remove_edge(u,v)
            G.remove_edge(x,y)
            swapcount+=1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
    return G

def random_2kc(G0, nswap=1, max_tries=100):
    """
    在random_2k()的基础上增加连通性判断，若置乱后的网络不保持连通性则撤销该置乱操作
    注：G0为连通网络
    """
    G = copy.deepcopy(G0)
    if not nx.is_connected(G):
       raise nx.NetworkXError("Graph not connected")
    if len(G) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    n=0
    swapcount=0
    while swapcount < nswap:
        swapped = []
        (u,x)=random.sample(G.nodes(),2)    #随机找两个不相连的点
        v=random.choice(list(G[u]))
        y=random.choice(list(G[x]))
        if G.degree(v)!=G.degree(y) or v==y:
            continue                        #若节点v,y度不相同，重新选择
        if len(set([u,v,x,y]))<4:
            continue
        if (y not in G.neighbors(u)) and (v not in G.neighbors(x)) and ((u,v) in G.edges()) and ((x,y) in G.edges()):
            G.add_edge(u,y)
            G.add_edge(x,v)
            G.remove_edge(u,v)
            G.remove_edge(x,y)
            swapped.append((u,v,x,y))
            swapcount+=1
        if not nx.is_connected(G):
            while swapped:
                (u, v, x, y) = swapped.pop()
                G.add_edge(u,v)
                G.add_edge(x,y)
                G.remove_edge(u,y)
                G.remove_edge(x,v)
                swapcount -= 1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
    return G

def random_25k(G0, nswap=1, max_tries=100):
    """
    在2阶基础上增加度度相关的聚类系数的判断，若置乱前后值不同，则撤销此次置乱
    """
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    l = map(lambda t:(t[1],t[0]), G0.degree().items())  #(度,节点)组成的列表
    D = dict_degree_nodeslist(l)
    n=0
    swapcount=0
    while swapcount < nswap:
        (u,x)=random.sample(G.nodes(),2)    #随机找两个不相连的点
        v=random.choice(list(G[u]))
        y=random.choice(list(G[x]))
        
        if G.degree(v)!=G.degree(y) or v==y:
            continue    # 若节点v,y度不相同，重新选择
        if (y not in G.neighbors(u)) and (v not in G.neighbors(x)) and ((u,v) in G.edges()) and ((x,y) in G.edges()):
            G.add_edge(u,y)
            G.add_edge(x,v)
            G.remove_edge(u,v)
            G.remove_edge(x,y)
            swapcount+=1
        for i in range(len(D)):
            avcG0 = nx.average_clustering(G0, nodes=D.values()[i], weight=None, count_zeros=True)
            avcG = nx.average_clustering(G, nodes=D.values()[i], weight=None, count_zeros=True)
            i += 1
            if avcG0 != avcG:   #若置乱前后度相关的聚类系数不同，则撤销此次置乱操作
                G.add_edge(u,v)
                G.add_edge(x,y)
                G.remove_edge(u,y)
                G.remove_edge(x,v)
                swapcount -= 1
                break
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
    return G

def random_25kc(G0, nswap=1, max_tries=100):
    """
    只判断四个节点及邻居节点度相关的聚类系数
    """
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    n=0
    swapcount=0
    while swapcount < nswap:
        (u,x)=random.sample(G.nodes(),2)    
        v=random.choice(list(G[u]))
        y=random.choice(list(G[x]))
        if G.degree(v)!=G.degree(y) or v==y or len([u,v,x,y])<4:
            continue                    # 若节点v,y度不相同，重新选择
        n+=1
        if (y not in G.neighbors(u)) and (v not in G.neighbors(x)) and ((u,v)in G.edges()) and ((x,y) in G.edges()): 
            G.add_edge(u,y)
            G.add_edge(x,v)
            G.remove_edge(u,v)
            G.remove_edge(x,y)
            swapcount+=1
            if not nx.is_connected(G):
                G.add_edge(u,v)
                G.add_edge(x,y)
                G.remove_edge(u,y)
                G.remove_edge(x,v)
                swapcount -= 1
                continue
            l = map(lambda t:(t[1],t[0]), G0.degree([u,v,x,y]+list(G[u])+list(G[v])+list(G[x])+list(G[y])).items())  #(度,节点)组成的列表
            D = dict_degree_nodeslist(l)
            for i in range(len(D)):
                avcG0 = nx.average_clustering(G0, nodes=D.values()[i], weight=None, count_zeros=True)
                avcG = nx.average_clustering(G, nodes=D.values()[i], weight=None, count_zeros=True)
                i += 1
                if avcG0 != avcG:   #若置乱前后度相关的聚类系数不同，则撤销此次置乱操作
                    G.add_edge(u,v)
                    G.add_edge(x,y)
                    G.remove_edge(u,y)
                    G.remove_edge(x,v)
                    swapcount -= 1
                    break    
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
    return G


def rich_club_creat(G0, k,max_tries=100):
    """
    任选两条边(富节点和非富节点的连边)，若富节点间无连边，非富节点间无连边，则断边重连
    达到最大尝试次数或全部富节点间都有连边，循环结束
    """
    if len(G0) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    G = copy.deepcopy(G0)
    hubs = [e for e in G.nodes() if G.degree()[e]>=k]     #全部富节点
    hubs_edges = [e for e in G.edges() if G.degree()[e[0]]>=k and G.degree()[e[1]]>= k] #网络中已有的富节点和富节点的连边
    len_possible_edges = len(hubs)*(len(hubs)-1)/2        #全部富节点间都有连边的边数
    n = 0
    while len(hubs_edges) < len_possible_edges:
        u,y = random.sample(hubs,2)                       #任选两个富节点
        v = random.choice(list(G[u])) 
        x = random.choice(list(G[y]))
        if len(set([u,v,x,y]))<4:
            continue
        if G.degree()[v] > k or G.degree()[x] > k:
            continue   #另一端节点为非富节点               
        if (x,v) not in G.edges() and (v,x) not in G.edges() and (u,y) not in G.edges() and (y,u) not in G.edges():              
            G.add_edge(u,y)
            G.add_edge(x,v)
            G.remove_edge(u,v)
            G.remove_edge(x,y)
            hubs_edges.append((u,y)) #更新已存在富节点和富节点连边
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
    hubs = [e for e in G.nodes() if G.degree()[e]>=k]    #全部富节点
    hubs_edges = [e for e in G.edges() if G.degree()[e[0]]>=k and G.degree()[e[1]]>= k] #网络中已有的富节点和富节点的连边
    len_possible_edges = len(hubs)*(len(hubs)-1)/2       #全部富节点间都有连边的边数
    n = 0
    while len(hubs_edges) < len_possible_edges:
        u,y = random.sample(hubs,2)                      #任选两个富节点
        v = random.choice(list(G[u]))
        x = random.choice(list(G[y]))
        if len(set([u,v,x,y]))<4:
            continue
        if G.degree()[v] > k or G.degree()[x] > k:       #另一端节点为非富节点
            continue                  
        if ((x,v) not in G.edges()) and ((v,x) not in G.edges()) and ((u,y) not in G.edges()) and ((y,u) not in G.edges()):
            G.add_edge(u,y)
            G.add_edge(x,v)
            G.remove_edge(u,v)
            G.remove_edge(x,y)
            hubs_edges.append((u,y))                     #更新已存在富节点和富节点连边
        if not nx.is_connected(G):                       #不保持连通性，撤销
            G.add_edge(u,v)
            G.add_edge(x,y)
            G.remove_edge(u,y)
            G.remove_edge(x,v)
            hubs_edges.remove((u,y))
        if n >= max_tries:                               #若达最大尝试次数，退出循环
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
    hubedges = []                                    #富边
    nothubedges = []                                 #非富边
    hubs = [e for e in G.nodes() if G.degree()[e]>k] #全部富节点
    for e in G.edges():
        if e[0] in hubs and e[1] in hubs:
            hubedges.append(e)
        elif e[0] not in hubs and e[1] not in hubs:
            nothubedges.append(e)
            
    n = 0
    while hubedges and nothubedges:
        u,v = random.choice(hubedges)               #随机选一条富边
        x,y = random.choice(nothubedges)            #随机选一条非富边
        if len(set([u,v,x,y]))<4:
            continue
        if ((x,v) not in G.edges()) and ((v,x) not in G.edges()) and ((u,y) not in G.edges()) and ((y,u) not in G.edges()):              
            G.add_edge(u,y)
            G.add_edge(x,v)
            G.remove_edge(u,v)
            G.remove_edge(x,y)
            hubedges.remove((u,v))
            nothubedges.remove((x,y))
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
    hubedges = []                                    #富边
    nothubedges = []                                 #非富边
    hubs = [e for e in G.nodes() if G.degree()[e]>k] #全部富节点
    for e in G.edges():
        if e[0] in hubs and e[1] in hubs:
            hubedges.append(e)
        elif e[0] not in hubs and e[1] not in hubs:
            nothubedges.append(e)
    n = 0
    while hubedges and nothubedges:
        u,v = random.choice(hubedges)              #随机选一条富边
        x,y = random.choice(nothubedges)           #随机选一条非富边
        if len(set([u,v,x,y]))<4:
            continue
        if ((x,v) not in G.edges()) and ((v,x) not in G.edges()) and ((u,y) not in G.edges()) and ((y,u) not in G.edges()):              
            G.add_edge(u,y)
            G.add_edge(x,v)
            G.remove_edge(u,v)
            G.remove_edge(x,y)
            hubedges.remove((u,v))
            nothubedges.remove((x,y))
        if not nx.is_connected(G):                #不保持连通性，撤销
            G.add_edge(u,v)
            G.add_edge(x,y)
            G.remove_edge(u,y)
            G.remove_edge(x,v)
            hubedges.append((u,v))
            nothubedges.append((x,y))
        if n >= max_tries:
            print ('Maximum number of attempts (%s) exceeded '%n)
            break
        n += 1
    return G



def assort_mixing(G0, nswap=1, max_tries=100):       #同配
    G = copy.deepcopy(G0)
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    n=0
    swapcount=0
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(G.edges(),2)    #任选两条边        
        n += 1
        if len(set([u,v,x,y]))<4:
            continue
        sortednodes = zip(*sorted(G.degree([u,v,x,y]).items(),key=lambda d:d[1],reverse=True))[0]
        if ((sortednodes[0],sortednodes[1]) in G.edges() or (sortednodes[1],sortednodes[0]) in G.edges()
            or (sortednodes[2],sortednodes[3]) in G.edges() or (sortednodes[3],sortednodes[2]) in G.edges()):
            continue                                #若新连边已存在，则重选
        G.add_edge(sortednodes[0],sortednodes[1])   #连新边 
        G.add_edge(sortednodes[2],sortednodes[3])
        G.remove_edge(x,y)                          #断旧边
        G.remove_edge(u,v)
        swapcount+=1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print(e)
            break
    return G
    
def assort_mixingc(G0,nswap=1, max_tries=100):     #异配
    G = copy.deepcopy(G0)
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if not nx.is_connected(G):
       raise nx.NetworkXError("Graph not connected")
    if len(G) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    n=0
    swapcount=0
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(G.edges(),2)    #任选两条边        
        n += 1
        if len(set([u,v,x,y]))<4:
            continue
        sortednodes = zip(*sorted(G.degree([u,v,x,y]).items(),key=lambda d:d[1],reverse=True))[0]
        if ((sortednodes[0],sortednodes[3]) in G.edges() or (sortednodes[3],sortednodes[0])in G.edges()
            or (sortednodes[2],sortednodes[1]) in G.edges() or (sortednodes[1],sortednodes[2])in G.edges()):
            continue                                #若新连边已存在，则重选
        G.add_edge(sortednodes[0],sortednodes[3])   #连新边 
        G.add_edge(sortednodes[1],sortednodes[2])
        G.remove_edge(x,y)                          #断旧边
        G.remove_edge(u,v)
        swapcount+=1
        if not nx.is_connected(G):  
            G.remove_edge(sortednodes[0],sortednodes[3]) 
            G.remove_edge(sortednodes[1],sortednodes[2])
            G.add_edge(x,y) 
            G.add_edge(u,v)
            swapcount -= 1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print(e)
            break
    return G


def disassort_mixing(G0, nswap=1, max_tries=100):     #异配
    G = copy.deepcopy(G0)
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if len(G) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    n=0
    swapcount=0
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(G.edges(),2)    #任选两条边        
        n += 1
        if len(set([u,v,x,y]))<4:
            continue
        sortednodes = zip(*sorted(G.degree([u,v,x,y]).items(),key=lambda d:d[1],reverse=True))[0]
        if ((sortednodes[0],sortednodes[3])in G.edges() or (sortednodes[3],sortednodes[0])in G.edges()
            or (sortednodes[2],sortednodes[1])in G.edges() or (sortednodes[1],sortednodes[2])in G.edges()):
            continue                                #若新连边已存在，则重选
        G.add_edge(sortednodes[0],sortednodes[3])   #连新边 
        G.add_edge(sortednodes[1],sortednodes[2])
        G.remove_edge(x,y)                          #断旧边
        G.remove_edge(u,v)
        swapcount+=1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print(e)
            break
    return G
    
def disassort_mixingc(G0, nswap=1, max_tries=100):    #同配
    G = copy.deepcopy(G0)
    if nswap>max_tries:
        raise nx.NetworkXError("Number of swaps > number of tries allowed.")
    if not nx.is_connected(G):
       raise nx.NetworkXError("Graph not connected")
    if len(G) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    n=0
    swapcount=0
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(G.edges(),2)    #任选两条边        
        n += 1
        if len(set([u,v,x,y]))<4:
            continue
        sortednodes = zip(*sorted(G.degree([u,v,x,y]).items(),key=lambda d:d[1],reverse=True))[0]
        if ((sortednodes[0],sortednodes[1]) in G.edges() or (sortednodes[1],sortednodes[0])in G.edges()
            or (sortednodes[2],sortednodes[3]) in G.edges() or (sortednodes[3],sortednodes[2])in G.edges()):
            continue                                #若新连边已存在，则重选
        G.add_edge(sortednodes[0],sortednodes[1])   #连新边 
        G.add_edge(sortednodes[2],sortednodes[3])
        G.remove_edge(x,y)                          #断旧边
        G.remove_edge(u,v)
        swapcount+=1
        if not nx.is_connected(G):  
            G.remove_edge(sortednodes[0],sortednodes[1]) 
            G.remove_edge(sortednodes[2],sortednodes[3])
            G.add_edge(x,y) 
            G.add_edge(u,v)
            swapcount -= 1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print(e)
            break
    return G
    
def random_1kd(G0, nswap=1, max_tries=100):  #有向网络基于随机断边重连的1阶零模型
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
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(G.edges(),2)
        if len(set([u,v,x,y]))<4:            
            continue
        if (x,v) not in G.edges() and (u,y) not in G.edges():  #断边重连
            G.add_edge(u,y)
            G.add_edge(x,v)
            G.remove_edge(u,v)
            G.remove_edge(x,y)
            swapcount+=1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n +
            'before desired swaps achieved (%s).'%nswap)
            print e
            break
        n+=1
    return G
    
    


def dict_degree_nodeslist(ndlist):
    D = {}      #{度：[节点1，节点2，..]}，其中节点1和节点2有相同的度
    for e in ndlist:
        if e[0] not in D:
            D[e[0]] = [e[1]]
        else:
            D[e[0]].append(e[1])
    return D