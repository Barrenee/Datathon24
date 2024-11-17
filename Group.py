from ParticipantAbstract import ParticipantAbstract
from typing import List, Callable

class Group:
    def __init__(self, participant: ParticipantAbstract):
        self.people_in_group: List[ParticipantAbstract] = [participant]
        self.preferred_team_size: int = participant.preferred_team_size
        
        self.roles_fullfilled: List[str] = participant.preferred_role
        self.objective_abs: set[str] = participant.objective_abs # Abstracted objective
        self.interest_in_challenges: set[str] = participant.interest_in_challenges
        self.preferred_languages: set[str] = participant.preferred_languages

        #self.programming_level: dict[str, List[str]] = participant.programming_level
        #self.expert_ptograms: set[str] = participant.expert_programs

    def merge_group(self, group: 'Group'):
        '''Merges both groups and actualizes the group's attributes'''
        self.people_in_group.extend(group.people_in_group) # Add people to the group
        self.roles_fullfilled.extend(group.roles_fullfilled) # Add roles to the group
        self.preferred_languages = self.preferred_languages.intersection(group.preferred_languages) # Intersect languages
        
        self.programming_level = self.update_programming_level(group) # Update programming level
        self.objective_abs = self.update_objectives(group) # Update objectives
        self.interest_in_challenges = self.update_interest_in_challenges(group)
        self.expert_ptograms = self.update_expert_ptograms(group)
    
    def update_programming_level(self, group: 'Group'):
        '''Updates the programming level of the group'''
        for key, value in group.programming_level.items():
            if key in self.programming_level:
                if self.programming_level[key] != value:
                    self.programming_level[key].append(value)
            else:
                self.programming_level[key] = value

    def update_objectives(self, group: 'Group'):
        '''Updates the objectives of the group'''
        # Intersection for now
        # Can be changed in the future
        self.objective_abs = self.objective_abs.intersection(group.objective_abs)
    
    def update_interest_in_challenges(self, group: 'Group'):
        '''Updates the interest in challenges of the group'''
        # Intersection for now
        # Can be changed in the future
        self.interest_in_challenges = self.interest_in_challenges.intersection(group.interest_in_challenges)
    
    def update_expert_ptograms(self, group: 'Group'):
        '''Updates the expert programs of the group'''
        # Union for now
        # Can be changed in the future
        self.expert_ptograms = self.expert_ptograms.union(group.expert_ptograms)