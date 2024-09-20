"""
WHAT IS HAPPENING:
-> for any length of "experiment"
  -> initialize node and edge dictionaries for each strategy
  -> on each day
    -> pick two people
    -> allow each strategy to pick a driver
    -> accumulate unfairness
  -> find the max and min unfairness values for each strategry over this length
-> plot the length vs. max/min unfairness for each strategy

STRATEGIES
1. Randomized deterministic local
  -> if two people have not carpooled together, determine the driver randomly
  -> this sets an "order" for this pair
  -> they strictly alternate going forward
2. Randomized local greedy
  -> if two people are locally out of balance, restore it
  -> else, pick the driver randomly
3. Randomized global greedy
  -> if one person has more debt than the other, they drive
  -> else, pick the driver randomly
4. Biased local greedy
  -> if two people are locally out of balance, restore it
  -> else, generate a biased coin to chose the driver
  -> coin 1
    -> say A has 10 less unfairness than B
    -> randomly pick r in (0,1)
    -> if r is anywhere but the top 2^(-11), A drives
"""

from random import choice, random
n = 50 # number of people
start = 200
end = 10000
step = 200

x_val = list(range(start,end+step,step))

min_rand_det = []
max_rand_det = []

min_local_greedy = []
max_local_greedy = []

min_global_greedy = []
max_global_greedy = []

min_local_biased = []
max_local_biased = []

"""
Goes through all people and calculates their unfairness
"""
def calc_unf2(edges,nodes):
  for i in range(1,n+1):
    total = 0
    for j in range(1,i):
      total -= edges[pow(j,2)*pow(i,3)][1]
    for j in range(i+1,n+1):
      total += edges[pow(i,2)*pow(j,3)][1]
    nodes[i] = total
    
def calc_unf(edges,nodes):
  for i in range(1,n+1):
    total = 0
    for j in range(1,i):
      total -= edges[pow(j,2)*pow(i,3)]
    for j in range(i+1,n+1):
      total += edges[pow(i,2)*pow(j,3)]
    nodes[i] = total

def plot_unfairness():
  import matplotlib.pyplot as plt
  plt.plot(x_val, max_rand_det, label="rand det max")
  plt.plot(x_val, min_rand_det, label="rand det min")
  plt.plot(x_val, max_local_greedy, label="local greedy max")
  plt.plot(x_val, min_local_greedy, label="local greedy min")
  plt.plot(x_val, max_global_greedy, label="global greedy max")
  plt.plot(x_val, min_global_greedy, label="global greedy min")
  plt.plot(x_val, max_local_biased, label="local biased max")
  plt.plot(x_val, min_local_biased, label="local biased min")
  plt.xlabel("number of days")
  plt.ylabel('unfairness')
  plt.title('Unfairness over time')
  plt.legend()
  plt.show()
  
"""
- Edge (a,b) is hashed to a^2*b^3 for a<b
- If this edge is positive, a has driven more
- Edge (b,a) is found with the negative of (a,b)
- The people are 1-indexed because of the hashing
"""
def init2(edges,nodes):
  for i in range(1,n+1): # initializing
    nodes[i] = 0
    for j in range(i+1,n+1):
      edges[pow(i,2)*pow(j,3)] = [".",0]
      
def day_rand_def(edges,nodes,a,b):
  if edges[pow(a,2)*pow(b,3)][0] == ".": # first time for this pair
    driver = choice(["a","b"])
    if driver == "a":
      edges[pow(a,2)*pow(b,3)] = ["a", 1]
      nodes[a] += 1
      nodes[b] -= 1
    else:
      edges[pow(a,2)*pow(b,3)] = ["b", -1]
      nodes[a] -= 1
      nodes[b] += 1
  else:
    if edges[pow(a,2)*pow(b,3)][0] == "a":
      edges[pow(a,2)*pow(b,3)][0] = "b"
      edges[pow(a,2)*pow(b,3)][1] -= 1
      nodes[a] -= 1
      nodes[b] += 1
    else:
      edges[pow(a,2)*pow(b,3)][0] = "a"
      edges[pow(a,2)*pow(b,3)][1] += 1
      nodes[a] += 1
      nodes[b] -= 1
      
  node_list = [nodes[i] for i in range(1,n+1)]
  max_rand_det[-1] = max(max_rand_det[-1], max(node_list))
  min_rand_det[-1] = min(min_rand_det[-1], min(node_list))
  
def init1(edges,nodes):
  for i in range(1,n+1): # initializing
    nodes[i] = 0
    for j in range(i+1,n+1):
      edges[pow(i,2)*pow(j,3)] = 0
      
def day_local_greedy(edges,nodes,a,b):
  if edges[pow(a,2)*pow(b,3)] > 0:
    driver = "b"
  elif edges[pow(a,2)*pow(b,3)] < 0:
    driver = "a"
  else:
    driver = choice(["a","b"])
  if driver == "a":
    edges[pow(a,2)*pow(b,3)] += 1
  else:
    edges[pow(a,2)*pow(b,3)] -+ 1
  calc_unf(edges,nodes)
  node_list = [nodes[i] for i in range(1,n+1)]
  max_local_greedy[-1] = max(max_local_greedy[-1], max(node_list))
  min_local_greedy[-1] = min(min_local_greedy[-1], min(node_list))
  
def day_global_greedy(nodes,a,b):
  if nodes[a] > nodes[b]:
    driver = "b"
  elif nodes[a] < nodes[b]:
    driver = "a"
  else:
    driver = choice(["a","b"])
  if driver == "a":
    nodes[a] += 1
    nodes[b] -= 1
  else:
    nodes[a] -= 1
    nodes[b] += 1
  node_list = [nodes[i] for i in range(1,n+1)]
  max_global_greedy[-1] = max(max_global_greedy[-1], max(node_list))
  min_global_greedy[-1] = min(min_global_greedy[-1], min(node_list))
    
def biased_coin1(nodes,a,b):
  if nodes[a] <= nodes[b]:
    diff = nodes[b] - nodes[a] + 1
    if random() <= 1 - pow(2,-1*diff):
      return "a"
    else:
      return "b"
  else:
    diff = nodes[a] - nodes[b] + 1
    if random() >= pow(2,-1*diff):
      return "b"
    else:
      return "a"
  
def day_local_biased(edges,nodes,a,b):
  if edges[pow(a,2)*pow(b,3)] > 0:
    driver = "b"
  elif edges[pow(a,2)*pow(b,3)] < 0:
    driver = "a"
  else:
    driver = biased_coin1(nodes,a,b)
  if driver == "a":
    edges[pow(a,2)*pow(b,3)] += 1
  else:
    edges[pow(a,2)*pow(b,3)] -+ 1
  calc_unf(edges,nodes)
  node_list = [nodes[i] for i in range(1,n+1)]
  max_local_biased[-1] = max(max_local_biased[-1], max(node_list))
  min_local_biased[-1] = min(min_local_biased[-1], min(node_list))

def main():
  for span in range(start,end+step,step):
    edges_rand_det = {}
    nodes_rand_det = {} # unfairness of each person
    init2(edges_rand_det,nodes_rand_det)
    max_rand_det.append(0)
    min_rand_det.append(0)
    
    edges_local_greedy = {}
    nodes_local_greedy = {}
    init1(edges_local_greedy, nodes_local_greedy)
    max_local_greedy.append(0)
    min_local_greedy.append(0)
    
    edges_global_greedy = {}
    nodes_global_greedy = {}
    init1(edges_global_greedy, nodes_global_greedy)
    max_global_greedy.append(0)
    min_global_greedy.append(0)
    
    edges_local_biased = {}
    nodes_local_biased = {}
    init1(edges_local_biased, nodes_local_biased)
    max_local_biased.append(0)
    min_local_biased.append(0)
    
    for d in range(span):
      a = choice(range(1,n+1))
      b = choice(list(range(1,a)) + list(range(a+1,n+1)))
      if a > b:
        a,b = b,a
      day_rand_def(edges_rand_det, nodes_rand_det, a, b)
      day_local_greedy(edges_local_greedy, nodes_local_greedy, a, b)
      day_global_greedy(nodes_global_greedy, a, b)
      day_local_biased(edges_local_biased, nodes_local_biased, a, b)

  print("max unfairness, random det:\n", max_rand_det)
  print("min unfairness, random det:\n", min_rand_det)
  
  print("max unfairness, local greedy:\n", max_local_greedy)
  print("min unfairness, local greedy:\n", min_local_greedy)
  
  print("max unfairness, global greedy:\n", max_global_greedy)
  print("min unfairness, global greedy:\n", min_global_greedy)
  
  print("max unfairness, local biased:\n", max_local_biased)
  print("min unfairness, local biased:\n", min_local_biased)

  #plot_unfairness()
    
main()
