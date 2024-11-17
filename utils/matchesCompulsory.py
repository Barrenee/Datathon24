from Group import Group
from config.literals import LANGUAGES, OBJECTIVES, CHALLENGES
from typing import List, Dict
from utils.Table import Table


def get_compatible_groups(group: Group, challenges_table: Table, objectives_table: Table, languages_table: Table) -> List[List[Group]]:
    language_union = languages_table.get_union(group)
    objectives_union = objectives_table.get_union(group)
    challenges_union = challenges_table.get_union(group)

    compatible_groups = challenges_union.union(language_union.intersection(objectives_union))
    compatible_groups = (compatible_groups)
    compatible_groups.remove(group)
    return compatible_groups
    

def build_matrix(allgroups: List[Group], challenges_table: Table, objectives_table: Table, languages_table: Table):
    matrix = {}
    for group in allgroups:
        matrix[group] = get_compatible_groups(group, challenges_table, objectives_table, languages_table)
    return matrix


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


def init_tables(allgroups):
    challenges_table = Table(CHALLENGES, Group.get_interest_in_challenges)
    objectives_table = Table(OBJECTIVES, Group.get_objective_abs)
    languages_table = Table(LANGUAGES, Group.get_preferred_languages)
    
    challenges_table.initialize(allgroups)
    objectives_table.initialize(allgroups)
    languages_table.initialize(allgroups)

    return challenges_table, objectives_table, languages_table


def find_obligatory_compatibles(all_groups:List[Group], table_language:Dict[str, List[Group]], table_objectives:Dict[str, List[Group]], table_challenges:Dict[str, List[Group]]) -> Dict[Group, List[Group]]:
    '''Finds the groups that are compatible with each other'''
    compatibles = {}
    for group in all_groups:
        compatibles[group] = set()
        language_set = set()
        objective_set = set()
        challenge_set = set()

        for language in group.preferred_languages:
            language_set = set(table_language[language]).union(language_set)
        
        for objective in group.objective_abs:
            objective_set = set(table_objectives[objective]).union(objective_set)

        for challenge in group.interest_in_challenges:
            challenge_set = set(table_challenges[challenge]).union(challenge_set)

        compatibles[group] = language_set.intersection(objective_set) # Get the groups that have the same language and objective preferences
        compatibles[group] = compatibles[group].intersection(challenge_set)
        compatibles[group].remove(group)
    return compatibles