# Overview

To generate a hypothetical flow for playbook scripts using network graph and DFS. 

# Steps

1. Filter to only get windows technics
2. loop through each APT to create a 2d matrix of (tactic x technic) list
3. Loop through the new apt matrix and permutate by P(n, 2) to form edge pairs(based on the image below) ![image-20210727092535588](image-20210727092535588.png)
4. Use a counter to count total number of same pairs in the permutation to calculate weightage. eg. [(A,B, 3), (A,C,10), (B,C, 2)...(source node, target node, weight)]
5. Form a graph using networkx
6. Pick a root node from tactic of either Credential Access or Exfiltration. Eg. T1030(Brute Force) of Exfiltration
7. Run DFS on the rootnode in the graph and loop through on each depth by finding the next largest weight until weight reaches 0

```
graph = {(A,B,4), (A,C,6), (B,C,2)}
rootnode = A
visted = []
result = []

1. if node not in visited
	1a. detect ttp
		1a.1 if detect ttp, add to result
    1b. add node to visited
    1c. get weight of all neighbours of node
    1d. get the next max weighted node
    1e. repeat (1) using the next max weighted node
2. else end

```



# Integration note

1. In frontend, user will pick from drop down list ["Credential Access", "Exfiltration"]
2. Server will get the tecnique ids in Eg. Exfiltration["Automatic Exfiltration(T1020)", "Data Transfer Limit(T1030)", "Exfiltration over Alternative(T1048)"...]
3. User selects "Automatic Exfiltration(T1020)" as the playbook for exfiltration
4. Display diagram of the playbook T1020
5. User can choose to edit, if not run the playbook
6. Server will loop through each id. If one of the ID is True, carry out DFS search. Otherwise, display detected TTP to user of the tactic.

# Reference

- [Finding Related ATT&CK Techniques](https://medium.com/mitre-attack/finding-related-att-ck-techniques-f1a4e8dfe2b6)
- [MITRE MATRIX](https://mitre-attack.github.io/attack-navigator//#layerURL=https%3A%2F%2Fattack.mitre.org%2Fgroups%2FG0018%2FG0018-enterprise-layer.json)
- Traversal Animation



![8 Difference Between DFS (Depth First Search) And BFS (Breadth First Search)  In Artificial Intelligence - Viva Differences](https://vivadifferences.com/wp-content/uploads/2019/10/DFS-VS-BFS.png)

![BFS_gif](https://github.com/Dannikk/dfs-bfs-animation-using-networkx/raw/main/output/bfs%20animation%20(...input.graph.txt).gif)

![DFS_gif](https://raw.githubusercontent.com/Dannikk/dfs-bfs-animation-using-networkx/main/output/dfs%20animation%20(...input.graph.txt).gif)

