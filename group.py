from participant import Participant
from typing import List

class Group:
    def __init__(self, participant:Participant):
        self.people_in_group: List[Participant] = [participant]
        self.preferred_team_size: int = participant.preferred_team_size
        
        self.roles_fullfilled: List[str] = participant.preferred_role
        self.objective: str = participant.objective # Abstracted objective
        self.interest_in_challenges: set[str] = participant.interest_in_challenges
        self.preferred_languages: set[str] = participant.preferred_languages

    def add_group(self, group:Group):
        '''Merges both groups and actualizes the group's attributes'''
        self.people_in_group.extend(group.people_in_group)
        self.roles_fullfilled.extend(group.roles_fullfilled)          

def find_possible_new_merge(group, all_groups:List[Group]) -> List[Group]:
    '''Returns the group that is the best fit to merge with the given group'''
    closest_groups = []
    for group2 in all_groups:
        if group2.preferred_languages.intersection(group.preferred_languages): # Check if they have a common language
            if group2.interest_in_challenges.intersection(group.interest_in_challenges): # Check if they have a common interest
                if group2.objective == group.objective: # Check if they have the same objective
                    if not(group2.roles_fullfilled.intersection(group.roles_fullfilled)): # Check if they have complementary roles
                        closest_groups.append(group2)
    return closest_groups