#!/usr/bin/env/python3
#coding=utf-8
import copy
#邻接矩阵
Adjacent_Matrix = []
#存储所有节点
Nodes = []
INF = 100000000
#所有的边
Edges = []
#加载数据，初始化邻接矩阵等
def load_data(path):
    global Nodes,Edges,Adjacent_Matrix

    file = open(path,'r+')
    next(file)
    for line in file:
        lines = line.strip().split()
        start = lines[0]
        end = lines[1]
        Edges.append([start,end,int(lines[2])])
        if not start in Nodes:
            Nodes.append(start)
        if not end in Nodes:
            Nodes.append(end)

    for node in Nodes:
        Adjacent_Matrix.append([INF for i in range(len(Nodes))])

    for edge in Edges:
        s_index = Nodes.index(edge[0])
        e_index = Nodes.index(edge[1])
        Adjacent_Matrix[s_index][e_index] = int(edge[2])
        Adjacent_Matrix[e_index][s_index] = int(edge[2])

#标准dijkstra算法
def dijkstra(v_start,v_end):
    global Adjacent_Matrix
    i_start = Nodes.index(v_start)

    Set = [0 for x in Nodes]
    Set[i_start] = 1

    dist = copy.deepcopy(Adjacent_Matrix[i_start])

    paths = []
    for v in Nodes:
        if Adjacent_Matrix[i_start][Nodes.index(v)] == INF:
            paths.append(-1)
        else:
            paths.append(i_start)


    for i in range(len(Nodes)-1):
        min = INF
        min_n = 0

        for j in range(len(Nodes)):
            if Set[j] == 0 and dist[j] < min:
                min_n = j
                min = dist[j]

        Set[min_n] = 1

        for j in range(len(Nodes)):
            if Set[j] == 0 and dist[min_n] + Adjacent_Matrix[min_n][j] < dist[j]:
                dist[j] = dist[min_n] + Adjacent_Matrix[min_n][j]
                paths[j] = min_n


    return dist,paths
#根据存储在paths里的双亲树获取路径
def get_path(paths,v_start,v_end):
    path = []
    i_start = Nodes.index(v_start)
    i_end = Nodes.index(v_end)
    index = i_end
    path.append(index)
    while True :
        value = paths[index]
        index = value
        path.append(index)
        if value == i_start:
            break

    final_path = []
    for v in path:
        final_path.append(Nodes[v])
    final_path.reverse()
    return final_path

#删除一条边
def remove(edge):
    global Adjacent_Matrix,Nodes
    s_index = Nodes.index(edge[0])
    e_index = Nodes.index(edge[1])
    Adjacent_Matrix[s_index][e_index] = INF
    #Adjacent_Matrix[e_index][s_index] = INF

#获取路径的长度
def get_length(path):
    i = 0
    sum = 0
    while i < len(path)-1:
        sum += Adjacent_Matrix[Nodes.index(path[i])][Nodes.index(path[i + 1])]
        i += 1

    return sum
#获取两个节点间的长度
def get_len_between(p1,p2):
    for e in Edges:
        temp = [e[0],e[1]]
        if [p1,p2] == temp or [p2,p1] == temp:
            return e[2]
    return INF
#标准的YEN算法
def YEN(start,end,K=1):
    global Adjacent_Matrix,Nodes,Edges

    A = []
    dist,paths = dijkstra(start,end)
    A.append(get_path(paths,start,end))
    B = []

    for k in range(1,K):
        for i in range(0,len(A[k-1]) - 1 ):
            spur_node = A[k-1][i]
            root_path = A[k-1][:i+1]
            removed_paths = []
            for p in A:
                if (i + 1 < len(p) and root_path == p[:i+1] and Adjacent_Matrix[Nodes.index(spur_node)][Nodes.index(p[i+1])] != INF and spur_node != p[i+1])  :
                    remove([spur_node,p[i+1]])
                    removed_paths.append([spur_node,p[i+1]])
                    removed_paths.append([ p[i + 1],spur_node])

            spur_dist, spur_paths = dijkstra(spur_node,end)

            if spur_paths[Nodes.index(end)] != -1:
                temp = get_path(spur_paths,spur_node,end)
                total_path = root_path[:-1] + temp
                if total_path not in B:
                    flag = 0
                    for n in root_path[:-1]:
                        if n in temp:
                            flag = 1
                            break
                    if flag == 0:
                        B.append(total_path)
            for e in removed_paths:
                Adjacent_Matrix[Nodes.index(e[0])][Nodes.index(e[1])] = get_len_between(e[0],e[1])


        if B == []:
            break
        else:
            B.sort(key=lambda p :get_length(p))
            A.append(B.pop(0))
    return A
#匹配两个路径重复的部分
def match(path1,shortest):
    matched_edges = []
    for i in range(len(path1)-1):
        if path1[i] in shortest and shortest[shortest.index(path1[i])+1] == path1[i+1]:
            matched_edges.append([path1[i],path1[i+1]])

    return matched_edges

#计算绕道率
def get_rate(path1,shortest_path):

    p1_len = path1[1]
    s_len = shortest_path[1]

    matched_edges = match(path1[0],shortest_path[0])

    sum_len = 0
    for e in matched_edges:
        sum_len += get_length(e)
    rate = (float(p1_len-sum_len)/(s_len-sum_len))

    return rate

def process():

    Paths = []
    load_data('Data.txt')
    yen = YEN('24','8',1000)
    for y in yen:
        Paths.append((y,get_length(y)))
        #print(y,end='')
        #print('lenght : '+ str(get_length(y)))
    #print('---------------------------------------')
    Res = []
    count = 1
    for p in Paths[1:]:
        rate = get_rate(p,Paths[0])
        if rate <= 1.3:
            temp = [len(p[0][1:])]
            temp.extend(p[0][1:])
            t = [count,temp]

            Res.append(t)
            count += 1
    for l in Res:
        print(l)

if "__main__" == __name__:

    process()