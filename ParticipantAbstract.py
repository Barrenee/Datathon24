from participant import Participant
from typing import Dict, List, Literal


class ParticipantAbstract(Participant):

    def __init__(self, participant: Participant):
                 #programming_level: Dict[str, Literal["Beginner", "Intermediate", "Advanced"]], 
                 #processed_objective: Literal["Learn", "Fun_Friends", "Win"], 
                 #**kwargs):
        
        self.__dict__ = participant.__dict__.copy()
        #self.programming_level = None
        self.objective_abs = None

    # def add_expertise(self):
    #     if 
        
    """def add_programming_level(self, programming_levels: Dict[str, Literal[""]]):
        self.programming_level = programming_levels"""

    def add_tryhard(self, tryhard: Literal["Extreme", "Medium", "Low", "None"]):
        self.tryhard = tryhard


    def add_objective_abs(self, objective_abs: Literal["Win", "Fun_Friends", "Learn"]):
        self.objective_abs = objective_abs
        
    