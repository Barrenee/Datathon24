from Group import Group
from config.literals import ROLES, INTERESTS, PROGRAMMING_SKILLS
from config.value_tables import PROGRAMMING_SKILLS_VALUES
from typing import List, Dict



def roles_match_pair(group1: Group, group2: Group) -> float:

    roles1 = group1.roles_fullfilled
    roles2 = group2.roles_fullfilled
    repeated_role_values = set(roles1).intersection(set(roles2))


    intersection = set(roles1).intersection(set(roles2)) 

    intersection-= {"Don't care", "Don't know"}
    
    if intersection == set():
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

def interest_match_pair2(group1: Group, group2: Group) -> float:
    """
    Calculate a normalized interest match score between two groups.

    :param group1: Group: The first group.
    :param group2: Group: The second group.
    :return: A float representing the normalized interest match score.
    """
    interests1 = set(group1.interests)
    interests2 = set(group2.interests)
    
    # Compute intersection and union sizes
    intersection_num = len(interests1 & interests2)
    union_num = len(interests1 | interests2)
    
    # Interest match calculation
    interests_match = 2*intersection_num - union_num
    
    # Normalization
    len1, len2 = len(interests1), len(interests2)
    minimum = len1 + len2
    maximum = min(len1, len2)
    interests_match += minimum
    normalized_match = interests_match / (maximum + minimum)
    
    # Scale to range [0, 5]
    return normalized_match * 5


def interests_match(group: Group, compatible_groups: List[Group]) -> Dict[str, List[Group]]:
    '''Matches groups based on their interests'''
    interest_values = {}
    for group2 in compatible_groups:
        interest_values[group2] = interest_match_pair2(group, group2)
    return interest_values

def programming_skills_match_pair(group1: Group, group2: Group) -> float:
    levels1 = group1.programming_skills
    levels2 = group2.programming_skills
    
    skills1 = group1.programming_skills.keys()
    skills2 = group2.programming_skills.keys()

    skills_union = list(set(skills1).union(set(skills2)))

    total_skills1 = 0
    total_skills2 = 0
    total_skills_union = 0

    for skill in skills1:
        total_skills1 += levels1[skill] * PROGRAMMING_SKILLS_VALUES[skill]
    for skill in skills2:
        total_skills2 += levels2[skill] * PROGRAMMING_SKILLS_VALUES[skill]
    
    for skill in skills_union:
        total_skills_union += max(levels1.get(skill, 0), levels2.get(skill, 0)) * PROGRAMMING_SKILLS_VALUES[skill]

    skill_win = total_skills_union - (total_skills1 + total_skills2 - total_skills_union)
    
    return skill_win


def programming_skills_match(group: Group, compatible_groups: List[Group]) -> Dict[str, List[Group]]:
    '''Matches groups based on their programming skills'''
    programming_skills_values = {}
    for group2 in compatible_groups:
        programming_skills_values[group2] = programming_skills_match_pair(group, group2)
    return programming_skills_values