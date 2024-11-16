from Group import Group
from config.literals import LANGUAGES, OBJECTIVES
from typing import List, Dict


def find_possible_new_merge(group, all_groups:List[Group]) -> List[Group]:
    '''Returns the group that is the best fit to merge with the given group'''
    closest_groups = []
    for group2 in all_groups:
        if group2.preferred_languages.intersection(group.preferred_languages): # Check if they have a common language
            if group2.interest_in_challenges.intersection(group.interest_in_challenges): # Check if they have a common interest
                if group2.objective.intersect(group.objective): # Check if they have the same objective
                    if not(group2.roles_fullfilled.intersection(group.roles_fullfilled)): # Check if they have complementary roles
                        closest_groups.append(group2)
    return closest_groups


def languages_match(allgroups: List[Group]) -> Dict[str, List[Group]]:
    '''Matches groups based on their preferred languages'''

    result = {}
    for language in LANGUAGES:
        result[language] = []
        for group in allgroups:
            if language in group.preferred_languages:
                result[language].append(group)

    return result
    #for langauge in LANGUAGES:
        
    
def objectives_match(allgroups: List[Group]) -> Dict[str, List[Group]]:
    '''Matches groups based on their objectives'''

    result = {}
    for objective in OBJECTIVES:
        result[objective] = []
        for group in allgroups:
            if objective in group.objective_abs:
                result[objective].append(group)

    return result
    #for langauge in LANGUAGES:
#def match(group1, group2):