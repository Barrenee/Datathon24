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

        self.programming_level: dict = participant.programming_level

    def add_group(self, group: Group):
        '''Merges both groups and actualizes the group's attributes'''
        self.people_in_group.extend(group.people_in_group) # Add people to the group
        self.roles_fullfilled.extend(group.roles_fullfilled) # Add roles to the group
        self.preferred_languages = self.preferred_languages.intersection(group.preferred_languages) # Intersect languages
        # TODO: Objectives
        # TODO: Interest in challenges

    
    def update_programming_level(self, group: Group, way_of_update: function = lambda x, y: (x + y)/2):
        for key, value in self.programming_level.items():
            self.programming_level[key] = way_of_update(group.programming_level[key], value) 

    def update_objectives(self, group: Group):
        self.objective = self.objective.intersection(group.objective)