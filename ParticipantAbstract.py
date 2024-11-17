from participant import Participant
from typing import Dict, List, Literal
from utils.utils import preprocess_prog_skills


class ParticipantAbstract():

    def __init__(self, participant: Participant):
                 #programming_level: Dict[str, Literal["Beginner", "Intermediate", "Advanced"]], 
                 #processed_objective: Literal["Learn", "Fun_Friends", "Win"], 
                 #**kwargs):
        #self.programming_level = None
        self.name = participant.name
        self.id = participant.id
        self.email = participant.email
        self.age = participant.age
        self.year_of_study = participant.year_of_study
        self.shirt_size = participant.shirt_size
        self.university = participant.university
        self.dietary_restrictions = participant.dietary_restrictions

        self.programming_skills = participant.programming_skills
        self.experience_level = participant.experience_level
        self.hackathons_done = participant.hackathons_done

        self.interests = participant.interests
        self.preferred_role = participant.preferred_role
        self.objective = participant.objective
        self.interest_in_challenges = participant.interest_in_challenges
        self.preferred_languages = participant.preferred_languages
        self.friend_registration = participant.friend_registration
        self.preferred_team_size = participant.preferred_team_size
        self.availability = participant.availability

        self.introduction = participant.introduction
        self.technical_project = participant.technical_project
        self.future_excitement = participant.future_excitement
        self.fun_fact = participant.fun_fact

        
        
        self.objective_abs = None
        if self.preferred_languages == []:
            self.preferred_languages = ["Catalan"]
        self.programming_skills = preprocess_prog_skills(self.programming_skills)


    #     if 
        
    """def add_programming_level(self, programming_levels: Dict[str, Literal[""]]):
        self.programming_level = programming_levels"""

    def add_tryhard(self, tryhard: Literal["Extreme", "Medium", "Low", "None"]):
        self.tryhard = tryhard


    def add_objective_abs(self, objective_abs: Literal["Win", "Fun_Friends", "Learn"]):
        self.objective_abs = objective_abs
        
    