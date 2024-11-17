from ParticipantAbstract import ParticipantAbstract
from typing import List, Callable

class Group:
    def __init__(self, participant: ParticipantAbstract):
        self.name = participant.name
        self.id = participant.id
        self.people_in_group: List[ParticipantAbstract] = [participant]
        self.group_size: int = len(self.people_in_group)
        self.preferred_team_size: int = participant.preferred_team_size
        
        self.roles_fullfilled: List[str] = [participant.preferred_role]
        self.objective_abs: List[str] = participant.objective_abs # Abstracted objective
        print(self.objective_abs)
        self.interest_in_challenges: set[str] = participant.interest_in_challenges
        self.preferred_languages: List[str] = participant.preferred_languages
        self.interests: set[str] = participant.interests
        self.programming_skills: dict[str, int] = participant.programming_skills
        #self.expert_programs: set[str] = participant.expert_programs

    def get_people_in_group(self) -> List[ParticipantAbstract]:
        return self.people_in_group
    
    def get_roles_fullfilled(self) -> List[str]:
        return self.roles_fullfilled
    
    def get_objective_abs(self) -> set[str]:
        return self.objective_abs
    
    def get_interest_in_challenges(self) -> set[str]:
        return self.interest_in_challenges
    
    def get_preferred_languages(self) -> set[str]:
        return self.preferred_languages

    def merge_group(self, group: 'Group'):
        '''Merges both groups and actualizes the group's attributes'''
        self.people_in_group.extend(group.people_in_group) # Add people to the group
        self.roles_fullfilled.extend(group.roles_fullfilled) # Add roles to the group
        self.preferred_languages = list(set(self.preferred_languages).intersection(set(group.preferred_languages))) # Intersect languages
        
        self.name = f'{self.name}-{group.name}'
        self.programming_skills = self.update_programming_skills(group) # Update programming level
        self.objective_abs = self.objective_abs + group.objective_abs # Update objectives
        self.interest_in_challenges = self.update_interest_in_challenges(group)
        #self.expert_ptograms = self.update_expert_ptograms(group)


        return self


    def update_programming_skills(self, group: 'Group'):
        '''Updates the programming level of the group'''
        programming_skills = self.programming_skills.copy()
        for key, value in group.programming_skills.items():
            if key in self.programming_skills.keys():
                programming_skills[key] = max(self.programming_skills[key], value)
            else:
                programming_skills[key] = value
        return programming_skills
    

    def update_interest_in_challenges(self, group: 'Group'):
        '''Updates the interest in challenges of the group'''
        # Intersection for now
        # Can be changed in the future
        return list(set(self.interest_in_challenges).intersection(set(group.interest_in_challenges)))
    
    