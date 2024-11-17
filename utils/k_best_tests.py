import numpy as np
from utils.matchesBasic import roles_match, interests_match, programming_skills_match
from utils.matchesCompulsory import get_compatible_groups, init_tables
from Group import Group
from typing import Dict, List
from math import inf
from utils.Table import Table


def maikelfunction(allgroups:  List[Group], k: int,matrix_bool: bool = False):
    '''Returns the number of common elements between two lists'''
    
    topk_dict = {}
    group_index, index_group = index_dict(allgroups)

    

    matrix = np.full((len(allgroups), len(allgroups)), -inf)

    challenges_table, objectives_table, languages_table = init_tables(allgroups)

    for group in allgroups:         
        compatible_groups = get_compatible_groups(group, challenges_table, objectives_table, languages_table)

        challenges_table, objectives_table, languages_table = init_tables(allgroups)
        matched_roles = roles_match(group=group, compatible_groups=compatible_groups)
        matched_interests = interests_match(group=group, compatible_groups=compatible_groups)
        matched_skills = programming_skills_match(group=group, compatible_groups=compatible_groups)
        

        r, i, s = 1,1,1 # Weights for the different matches
        for group2 in compatible_groups:
            matrix[group_index[group]][group_index[group2]] = r*matched_roles[group2] + i*matched_interests[group2] + s*matched_skills[group2] 
        
        topk_dict[group] = topk(matrix, group, k, group_index, index_group)
    
    max_antiguo = (-inf, None, None)
    for group in allgroups:
        for top in topk_dict[group]:
            (group, value) = top
            if value > max_antiguo[0]:
                max_antiguo = (value, group, group2)
    
    # Find best pairs => Blossom algorithm
    pairs , values = find_disjoint_pairs(matrix, index_group) 

    # return the best pairs of groups
    group = max_antiguo[1]
    group2 = max_antiguo[2]
    value = max_antiguo[0]
    if matrix_bool:
        return pairs, values, ["Role" "Programming_skills"],  ["Interests"], matrix
    return pairs, values, ["Role" "Programming_skills"],  ["Interests"]

def index_dict(allgroups):
    '''Returns a dictionary with the indexes of the groups'''
    groupindex_dict = {}
    indexgroup_dict = {}
    for i, group in enumerate(allgroups):
        groupindex_dict[group] = i
        indexgroup_dict[str(i)] = group
    return groupindex_dict, indexgroup_dict


def topk(matrix: np.array, group, k, group_index, index_group ):
    '''Returns the k best groups to merge with the given group'''
    topk = []
    for i in range(len(matrix[group_index[group]])):
        topk.append((index_group[str(i)], matrix[group_index[group]][i]))
    topk.sort(reverse=True, key=lambda x: x[1])
    return topk[:k]


import numpy as np
import networkx as nx

def find_disjoint_pairs(matrix: np.ndarray, index_group):
    """
    Finds the best combination of disjoint pairs to maximize the total value.

    Args:
        matrix (np.ndarray): A square matrix where matrix[i][j] is the value of pairing group i with group j.

    Returns:
        pairs (List[Tuple[int, int]]): List of optimal pairs (group indices).
        total_value (float): The total value of the optimal pairing.
    """
    n = len(matrix)
    G = nx.Graph()

    # Add edges for all possible pairs with their weights
    for i in range(n):
        for j in range(i + 1, n):  # Avoid duplicates (j > i)
            if matrix[i][j] != -np.inf:  # Skip invalid pairs
                G.add_edge(i, j, weight=matrix[i][j])

    # Find maximum weight matching
    matching = nx.max_weight_matching(G, maxcardinality=True)

    # Extract total value and pairs
    values = {}
    pairs = []
    for u, v in matching:
        values[index_group[str(u)],index_group[str(v)]] = matrix[u][v]
        pairs.append((index_group[str(u)], index_group[str(v)]))


    return pairs, values

