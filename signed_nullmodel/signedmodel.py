import networkx as nx
import copy
import random
"""
+ : weight=1
- : weight=2
"""

"""
1.1.正边置乱:[度序列相同]
任选两条边(u,v,1),(x,y,1)且(u,y),(x,v)不在G0的边列表中，断边重连
   
"""
def positive_edges_swap(G0, nswap=1, max_tries=100):  
    G = copy.deepcopy(G0)
    positive_edges = [(u,v) for u,v,edata in G.edges(data=True)if edata['weight']==1]
    n=0
    swapcount=0
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(positive_edges,2) #任取两条正边
        # 兼容有向无向
        if (u,y)not in G.edges() and (y,u)not in G.edges()and(x,v)not in G.edges()and(v,x)not in G.edges() and len([u,v,x,y])==4:
            G.add_weighted_edges_from([(u,y,1),(x,v,1)])
            positive_edges.extend([(u,y),(x,v)])
            G.remove_edge(u,v)
            G.remove_edge(x,y)
            positive_edges.remove((u,v))
            positive_edges.remove((x,y))    
            swapcount+=1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n + 'before desired swaps achieved (%s).'%nswap)
            print nx.NetworkXAlgorithmError(e)
            break
        n+=1
        print n
    return G

"""
1.2.负边置乱:[度序列相同]
   
"""
def negative_edges_swap(G0, nswap=1, max_tries=100):
    G = copy.deepcopy(G0)
    negative_edges = [(u,v) for u,v,edata in G.edges(data=True)if edata['weight']==2]
    
    n=0
    swapcount=0
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(negative_edges,2) #任取两条负边
        # 兼容有向无向
        if (u,y)not in G.edges() and (y,u)not in G.edges()and(x,v)not in G.edges()and(v,x)not in G.edges()and len([u,v,x,y])==4: 
            G.add_edge(u,y)
            G.add_edge(x,v)
            negative_edges.extend([(u,y),(x,v)])
            G[u][y]['weight'] = 2
            G[x][v]['weight'] = 2
            G.remove_edge(u,v)
            G.remove_edge(x,y)
            negative_edges.remove((u,v))
            negative_edges.remove((x,y))
            swapcount+=1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n + 'before desired swaps achieved (%s).'%nswap)
            print nx.NetworkXAlgorithmError(e)
            break
        n+=1
        print n
    return G


"""
2.符号置乱:
   
"""
def signs_swap(G0, nswap=1, max_tries=100):
    G = copy.deepcopy(G0)
    positive_edges = [(u,v) for u,v,edata in G.edges(data=True)if edata['weight']==1]
    negative_edges = [(u,v) for u,v,edata in G.edges(data=True)if edata['weight']==2]
    n=0
    swapcount=0
    while swapcount < nswap:
        (u,v) = random.choice(positive_edges) #任取一条正边，
        (x,y) = random.choice(negative_edges) #一条负边
        # 兼容有向无向
        if G[u][v]['weight'] == G[x][y]['weight']: print 'err'
        else:
            G[u][v]['weight'],G[x][y]['weight'] = G[x][y]['weight'],G[u][v]['weight']
            positive_edges.remove((u,v))
            positive_edges.append((x,y))
            negative_edges.remove((x,y))
            negative_edges.append((u,v))
            swapcount+=1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n + 'before desired swaps achieved (%s).'%nswap)
            print nx.NetworkXAlgorithmError(e)
            break
        n+=1
        print n
    return G

"""
3.完全置乱:
   
"""
def fully_swap(G0, nswap=1, max_tries=100):
    G = copy.deepcopy(G0)
    n=0
    swapcount=0
    while swapcount < nswap:
        (u,v),(x,y) = random.sample(G.edges(),2)
        if (u,y)not in G.edges() and (y,u)not in G.edges()and(x,v)not in G.edges()and(v,x)not in G.edges()and len([u,v,x,y])==4: # don't create parallel edges
            G.add_edge(u,y)
            G.add_edge(x,v)
            G[u][y]['weight'] = G[x][y]['weight']
            G[x][v]['weight'] = G[u][v]['weight']
            G.remove_edge(u,v)
            G.remove_edge(x,y)
            swapcount+=1
        if n >= max_tries:
            e=('Maximum number of swap attempts (%s) exceeded '%n + 'before desired swaps achieved (%s).'%nswap)
            print nx.NetworkXAlgorithmError(e)
            break
        n+=1
        print n
    return G
