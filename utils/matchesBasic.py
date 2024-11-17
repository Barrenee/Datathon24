from Group import Group
from config.literals import ROLES, INTERESTS, PROGRAMMING_SKILLS
from typing import List, Dict



def roles_match_pair(group1: Group, group2: Group) -> float:

    roles1 = group1.roles_fullfilled
    roles2 = group2.roles_fullfilled
    repeated_role_values = set(roles1).intersection(set(roles2))



    if set(roles1).intersection(set(roles2)) == set():
        return 5 # We return 5 as it is the best option, and the values are normalized in order to go from 0-5

    else:
        repeated_role_num = 0
        for role in roles1:
            if role not in ["Don't care", "Don't know"]:
                if role in repeated_role_values:
                    repeated_role_num += 1

        for role in roles2:
            if role not in ["Don't care", "Don't know"]:
                if role in repeated_role_values:    
                    repeated_role_num += 1

        roles_match = (len(roles1) + len(roles2)) / repeated_role_num
        
        # Normalization of values.
        maximum = len(roles1) + len(roles2)
        minimum = 1
        roles_match -= 1
        roles_match = roles_match / (maximum-1)
        roles_match *= 5
        
        return roles_match
    


def roles_match(group: Group, compatible_groups: List[Group]) -> Dict[str, List[Group]]:
    '''Matches groups based on their preferred roles'''

    roles_values = {}
    for group2 in compatible_groups:
        roles_values[group2] = roles_match_pair(group, group2)
    return roles_values



def interest_match_pair(group1: Group, group2: Group) -> float:
    """
    :group1: Group: group whose value of interest match will be merged with group1
    :group2: Group: group which will be used to calculate the value of interest match for group1
    """
    interests1 = group1.interests
    interests2 = group2.interests 
    intersection_num = len(set(interests1).intersection(set(interests2)))
    union_num = len(set(interests1).union(set(interests2)))

    interests_match = intersection_num - (union_num - intersection_num)

    # Normalization of values.
    # The minimum values is -Max Union (len interest1 + len interst2)
    # The maximum is the biggest possible intersection
    # So we sum the minimum, divide by the maximum + minimum and then multiply by the max value we ant to achieve
    minimum = len(interests1) + len(interests2)
    maximum = min(len(interests1), len(interests2)) 
    interests_match += minimum
    interests_match = interests_match / (maximum + minimum)
    interests_match *= 5
    return interests_match


def interests_match(group: Group, compatible_groups: List[Group]) -> Dict[str, List[Group]]:
    '''Matches groups based on their interests'''
    interest_values = {}
    for group2 in compatible_groups:
        interest_values[group2] = interest_match_pair(group, group2)
    return interest_values

#def programming_skills(group: Group, compatible_groups: Dict[List[Group]]) -> Dict[str, List[Group]]:
    
    
    