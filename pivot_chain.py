#!/usr/bin/env python3

import heapq
from collections import defaultdict
import sys

def dijkstra(graph, start, end, n):
    """
    Find the shortest path from start to end using Dijkstra's algorithm.
    Returns the minimum cumulative risk.
    """
    # Initialize distances with infinity
    distances = {node: float('inf') for node in range(1, n + 1)}
    
    # Map host names to node numbers for easier processing
    host_to_num = {}
    num_to_host = {}
    
    # Build the node mapping
    node_counter = 1
    for src in graph:
        if src not in host_to_num:
            host_to_num[src] = node_counter
            num_to_host[node_counter] = src
            node_counter += 1
        for dst, _ in graph[src]:
            if dst not in host_to_num:
                host_to_num[dst] = node_counter
                num_to_host[node_counter] = dst
                node_counter += 1
    
    # Convert start and end to numbers
    start_num = host_to_num.get(start)
    end_num = host_to_num.get(end)
    
    if start_num is None or end_num is None:
        return -1  # Start or end node not found
    
    # Priority queue: (distance, node)
    pq = [(0, start)]
    distances = {node: float('inf') for node in host_to_num.keys()}
    distances[start] = 0
    visited = set()
    
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        
        # If we reached the destination
        if current_node == end:
            return current_dist
        
        # Skip if already visited
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        # Check all neighbors
        if current_node in graph:
            for neighbor, weight in graph[current_node]:
                if neighbor not in visited:
                    new_dist = current_dist + weight
                    
                    # If we found a shorter path
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        heapq.heappush(pq, (new_dist, neighbor))
    
    # If end is unreachable
    return distances.get(end, -1)

def solve():
    # Read N (hosts) and M (paths)
    n, m, start, end = input().split()
    n = int(n)
    m = int(m)
    
    # Build the graph
    graph = defaultdict(list)
    
    for _ in range(m):
        parts = input().split()
        src = parts[0]
        dst = parts[1]
        risk = int(parts[2])
        graph[src].append((dst, risk))
    
    # Find the minimum risk path
    min_risk = dijkstra(graph, start, end, n)
    
    # Output the result
    if min_risk == float('inf') or min_risk == -1:
        print(-1)  # No path exists
    else:
        print(min_risk)

if __name__ == "__main__":
    solve()