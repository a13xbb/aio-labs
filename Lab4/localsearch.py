import random
import numpy as np

class Factory():
    def __init__(self, id, location):
        self.id = id
        self.location = location
        

def get_flow_value(cur_solution: list, dist: list, flow: list):
    value = 0
    for i in range(len(cur_solution) - 1):
        for j in range(i + 1, len(cur_solution)):
            value += dist[i][j] * flow[cur_solution[i]][cur_solution[j]]
    value *= 2
    return value


def swap_factories(solution: list, i: int, j: int):
    sol_copy = solution.copy()
    tmp = sol_copy[i]
    sol_copy[i] = sol_copy[j]
    sol_copy[j] = tmp
    return sol_copy
        
def local_search(n_factories: int, dist: list, flow: list, n_iterations=10):
    best_sol = [i for i in range(n_factories)]
    best_sol_value = get_flow_value(best_sol, dist, flow)
    for _ in range(n_iterations):
        dlb = [False for i in range(n_factories)]
        for i in range(n_factories):
            dlb_flag = True
            for j in range(n_factories):
                if not dlb[j] and i != j:
                    new_sol = swap_factories(best_sol, i, j)
                    delta = 0
                    for k in range(n_factories):
                        if k != i and k != j:
                            delta -= dist[i][k] * flow[best_sol[i]][best_sol[k]]
                            delta -= dist[j][k] * flow[best_sol[j]][best_sol[k]]
                            delta += dist[i][k] * flow[new_sol[i]][new_sol[k]]
                            delta += dist[j][k] * flow[new_sol[j]][new_sol[k]]
                    delta *= 2
                    if delta > 0:
                        dlb_flag = False
                        best_sol_value += delta
                        best_sol = new_sol
            if dlb_flag:
                dlb[i] = True
        print(best_sol, best_sol_value)
        
        
files_list = ['tai20a.txt', 'tai40a.txt', 'tai60a.txt', 'tai80a.txt', 'tai100a.txt']
 
for file in files_list:       
    with open(f'Lab4/benchmarks/{file}', 'r') as f:
        dist = []
        flow = []
        n_factories = int(f.readline())
        for i in range(n_factories):
            arr = f.readline().split()
            arr = list(map(int, arr))
            dist.append(arr)
        
        f.readline()
        for i in range(n_factories):
            arr = f.readline().split()
            arr = list(map(int, arr))
            flow.append(arr)
        
        local_search(n_factories, dist, flow)
