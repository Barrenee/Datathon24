from participant import Participant
from typing import List

class Group:
    def __init__(self, participant:Participant):
        self.people_in_group: List[Participant] = [participant]
        self.preferred_team_size: int = participant.preferred_team_size
        
        self.roles_fullfilled: List[str] = participant.preferred_role
        self.objective: set[str] = participant.objective # Abstracted objective
        self.interest_in_challenges: set[str] = participant.interest_in_challenges
        self.preferred_languages: set[str] = participant.preferred_languages

    def add_group(self, group: Group):
        '''Merges both groups and actualizes the group's attributes'''
        self.people_in_group.extend(group.people_in_group)
        self.roles_fullfilled.extend(group.roles_fullfilled)          

