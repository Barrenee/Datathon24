from Group import Group
from config.literals import ROLES, INTERESTS, PROGRAMMING_LANGUAGES
from typing import List, Dict

def roles_match(allgroups: List[Group]) -> Dict[str, List[Group]]:
    '''Matches groups based on their preferred roles'''

    # maximize the number of diferent roles fullfilled
    # for every pair of groups, we assign a 1-5 score based on how many roles they fullfill together
    # Ex: if group1 has roles A, B, C and group2 has roles B, C, D, the score would be 4

    pass



def interests_match(allgroups: List[Group]) -> Dict[str, List[Group]]:
    '''Matches groups based on their interests'''

    # maximize the intersection of interests
    