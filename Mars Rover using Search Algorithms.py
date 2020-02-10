import heapq
# Read and process the input
with open('input.txt', 'r') as f:
    algorithm = str(f.readline().strip())
    matrix_size = f.readline().split()
    w = int(matrix_size[0])
    h = int(matrix_size[1])
    start_coordinates = f.readline().split()
    x_start, y_start = int(start_coordinates[0]), int(start_coordinates[1])
    threshold = int(f.readline())
    targets = int(f.readline())
    target_list = []
    for _ in range(targets):
        target_co = f.readline().split()
        x = int(target_co[0])
        y = int(target_co[1])
        temp_list = (x, y)
        target_list.append(temp_list)
    matrix = []
    for _ in range(h):
        matrix_co = f.readline().split()
        for e in range(0, len(matrix_co)):
            matrix_co[e] = int(matrix_co[e])
        matrix.append(matrix_co)
    print("matrix", matrix)


# Flipping the Target Coordinates to make search easier
for xyz in range(len(target_list)):
    target_list[xyz] = target_list[xyz][::-1]


# Path printing onto the file
def path_print(paths):
    path = ""
    x = len(paths)
    for p in range(x-1):
        if paths[p] == "FAIL":
            path = path + "FAIL" + "\n"
        else:
            temp = paths[p].strip()
            path = path + temp + "\n"
    if paths[x-1] == "FAIL":
        path = path + "FAIL"
    else:
        temp = paths[x-1].strip()
        path = path + temp
    with open("output.txt", 'w+') as of:
        of.write(path)
    exit(0)


ucs_paths = []


# Path in Uniform Cost Search
def ucs_findpath(path_list, t):
    ucs_path = path_list[2]
    for ucs_i in range(len(ucs_path)):
        ucs_path[ucs_i] = ucs_path[ucs_i][::-1]
    path_string = ""
    for x_ucs in ucs_path:
        path_string += str(x_ucs[0]) + "," + str(x_ucs[1]) + " "
    ucs_paths.append(path_string)
    if t == len(target_list):
        path_print(ucs_paths)
    return


# Children nodes in Uniform Cost Search
def ucs_children(ucs_cur, ucs_level):
    x_c = ucs_cur[1][0]
    y_c = ucs_cur[1][1]
    c = ucs_cur[0]
    # Search in all possible directions [N,S,E,W,NE,NW,SE.SW]
    ucs_row = [0, 1, 0, -1, -1, 1, 1, -1]
    ucs_col = [-1, 0, 1, 0, -1, -1, 1, 1]
    ucs_children_list = []
    for j in range(4):
        t1 = x_c+ucs_row[j]
        t2 = y_c+ucs_col[j]
        if t1 < 0 or t2 < 0:
            continue
        if t2 >= w or t1 >= h:
            continue
        if abs(matrix[x_c][y_c] - matrix[t1][t2]) <= threshold:
            cost = c + 10
            if (t1, t2) in ucs_level:
                if cost > ucs_level[(t1, t2)]:
                    continue
            ucs_children_list.append((cost, (t1, t2), ucs_cur[2]+[(t1, t2)]))
    for j in range(4, 8):
        t1 = x_c+ucs_row[j]
        t2 = y_c+ucs_col[j]
        if t1 < 0 or t2 < 0:
            continue
        if t2 >= w or t1 >= h:
            continue
        if abs(matrix[x_c][y_c] - matrix[t1][t2]) <= threshold:
            cost = c + 14
            if (t1, t2) in ucs_level:
                if cost > ucs_level[(t1, t2)]:
                    continue
            ucs_children_list.append((cost, (t1, t2), ucs_cur[2]+[(t1, t2)]))
    return ucs_children_list


# Function to calculate the path, using uniform cost search
def ucs():
    t = 0
    for target in target_list:
        t += 1
        ucs_level = {}
        flag = 1
        opened = []
        if (y_start, x_start) == target:
            path = str(x_start)+","+str(y_start) + " " + str(x_start)+","+str(y_start) + " "
            ucs_paths.append(path)
            if t == len(target_list):
                path_print(ucs_paths)
            continue
        # cost + node + path   (cost,(x,y), [Nodes visited till now])
        heapq.heappush(opened, (0, (y_start, x_start), [(y_start, x_start)]))
        while opened:
            current_node_cost = heapq.heappop(opened)
            current_node = current_node_cost[1]
            if current_node == target:
                ucs_findpath(current_node_cost, t)
                flag = 0
                break
            # Find all the children
            children = ucs_children(current_node_cost, ucs_level)
            while children:
                child = children.pop()
                ucs_level[child[1]] = child[0]
                temp_opened = [opened[k][1] for k in range(len(opened))]
                if child[1] not in temp_opened:
                    heapq.heappush(opened, child)
                elif child[1] in temp_opened:
                    for c in range(len(opened)):
                        if opened[c][1] == child[1]:
                            if opened[c][0] < child[0]:
                                break
                            else:
                                del opened[c]
                                heapq.heappush(opened, child)
                                break
            heapq.heapify(opened)
        if flag:
            ucs_paths.append("FAIL")
            if t == len(target_list):
                path_print(ucs_paths)
        else:
            continue


# BFS

bfs_paths = []


# Function to calculate the path using Breadth First Search
def bfs():
    t = 0
    for target in target_list:
        flag = 0
        print(target)
        t += 1
        start = (y_start, x_start)
        level = {start: 0}
        parent = {start: 0}
        i = 1
        # if Start element is Target
        if (y_start, x_start) == target:
            path = str(x_start)+","+str(y_start) + " " + str(x_start)+","+str(y_start) + " "
            bfs_paths.append(path)
            if t == len(target_list):
                path_print(bfs_paths)
            continue
        # BFS
        frontier = [start]
        while frontier:
            next_coords = []
            for co_ord in frontier:
                # Coordinates for N,S,E,W,NE,NW,SE,SW
                row = [-1, 0, 1, 1, 1, 0, -1, -1]
                col = [-1, -1, -1, 0, 1, 1, 1, 0]
                children_list = []
                for j in range(8):
                    t1 = co_ord[0]+row[j]
                    t2 = co_ord[1]+col[j]
                    if t1 < 0 or t2 < 0:
                        continue
                    if t2 >= w or t1 >= h:
                        continue
                    if (t1, t2) in level:
                        continue
                    if abs(matrix[co_ord[0]][co_ord[1]]-matrix[t1][t2]) <= threshold:
                        children_list.append((t1, t2))
                for v in children_list:
                    if v not in level:
                        if v == target:
                            print("Inside flag V",v)
                            flag = 1
                        level[v] = i
                        parent[v] = co_ord
                        print("V",v,"Parent of v",parent[v])
                        next_coords.append(v)
            frontier = next_coords
            i += 1
        # Tracing back to start ..
        if flag:
            reverse_path = list()
            # print("target", target)
            reverse_path.append(target)
            # print(reverse_path)
            p = parent[target]
            while p != (y_start, x_start):
                reverse_path.append(p)
                p = parent[p]
            reverse_path.append((y_start, x_start))
            # Coordinates will be normal, reverse it.
            bfs_path = reverse_path[::-1]
            for r in range(len(bfs_path)):
                bfs_path[r] = bfs_path[r][::-1]
            path_string = ""
            for bfs_s in bfs_path:
                path_string += str(bfs_s[0]) + "," + str(bfs_s[1]) + " "
            bfs_paths.append(path_string)
            if t == len(target_list):
                path_print(bfs_paths)
        else:
            bfs_paths.append("FAIL")
            if t == len(target_list):
                path_print(bfs_paths)


# A Star
a_start_paths = []


# Heuristics to calculate the distance
def my_heuristics(n1, n2):
    x1, x2 = n1[0], n2[0]
    y1, y2 = n1[1], n2[1]
    m_dist = (abs(x2-x1) + abs(y2-y1))*10
    cost = m_dist - (6 * min(abs(x2-x1), abs(y2-y1)))
    return cost


def astar_findpath(path_list, t):
    astar_path = path_list[2]
    for astar_i in range(len(astar_path)):
        astar_path[astar_i] = astar_path[astar_i][::-1]
    path_string = ""
    for a_s in astar_path:
        path_string += str(a_s[0]) + "," + str(a_s[1]) + " "
    a_start_paths.append(path_string)
    if len(target_list) == t:
        path_print(a_start_paths)
    return


# Finding
def astar_children(ucs_cur, tar, a_star_level):
    x_c = ucs_cur[1][0]
    y_c = ucs_cur[1][1]
    c = ucs_cur[3]
    ucs_row = [0, 1, 0, -1, -1, 1, 1, -1]
    ucs_col = [-1, 0, 1, 0, -1, -1, 1, 1]
    ucs_children_list = []
    for j in range(4):
        t1 = x_c+ucs_row[j]
        t2 = y_c+ucs_col[j]
        if t1 < 0 or t2 < 0:
            continue
        if t2 >= w or t1 >= h:
            continue
        if abs(matrix[x_c][y_c] - matrix[t1][t2]) <= threshold:
            elevation_diff = abs(matrix[x_c][y_c] - matrix[t1][t2])
            h_dist = my_heuristics((t1, t2), tar)
            overall_cost = c + elevation_diff + 10
            cost = 10 + elevation_diff + h_dist + c
            if (t1, t2) in a_star_level:
                if cost > a_star_level[(t1, t2)]:
                    continue
            ucs_children_list.append((cost, (t1, t2), ucs_cur[2]+[(t1, t2)], overall_cost))
    for j in range(4, 8):
        t1 = x_c+ucs_row[j]
        t2 = y_c+ucs_col[j]
        if t1 < 0 or t2 < 0:
            continue
        if t2 >= w or t1 >= h:
            continue
        if abs(matrix[x_c][y_c] - matrix[t1][t2]) <= threshold:
            elevation_diff = abs(matrix[x_c][y_c] - matrix[t1][t2])
            h_dist = my_heuristics((t1, t2), tar)
            overall_cost = c + 14 + elevation_diff
            cost = 14 + elevation_diff + h_dist + c
            if (t1, t2) in a_star_level:
                if cost > a_star_level[(t1, t2)]:
                    continue
            ucs_children_list.append((cost, (t1, t2), ucs_cur[2]+[(t1, t2)], overall_cost))
    return ucs_children_list


def a_star():
    t = 0
    for target in target_list:
        t += 1
        a_star_level = {}
        flag = 1
        opened = []
        if (y_start, x_start) == target:
            path = str(x_start)+","+str(y_start) + " " + str(x_start)+","+str(y_start) + " "
            a_start_paths.append(path)
            if t == len(target_list):
                path_print(a_start_paths)
            continue
    # cost_overall + node + Path + cost   (cost,(x,y),[path], cost)
        heapq.heappush(opened, (0, (y_start, x_start), [(y_start, x_start)], 0))
        while opened:
            current_node_cost = heapq.heappop(opened)
            current_node = current_node_cost[1]
            if current_node == target:
                astar_findpath(current_node_cost, t)
                flag = 0
                break
            children = astar_children(current_node_cost, target, a_star_level)
            while children:
                child = children.pop()
                a_star_level[child[1]] = child[0]
                # This is check if the node is already present
                temp_opened = [opened[k][1] for k in range(len(opened))]
                if child[1] not in temp_opened:
                    heapq.heappush(opened, child)
                elif child[1] in temp_opened:
                    for c in range(len(opened)):
                        if opened[c][1] == child[1]:
                            if opened[c][0] < child[0]:
                                break
                            else:
                                del opened[c]
                                heapq.heappush(opened, child)
                                break
            heapq.heapify(opened)
        if flag:
            a_start_paths.append("FAIL")
            if t == len(target_list):
                path_print(a_start_paths)
        else:
            continue


if algorithm == "BFS":
    bfs()
elif algorithm == "UCS":
    ucs()
elif algorithm == "A*":
    a_star()
