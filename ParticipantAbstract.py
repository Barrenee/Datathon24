from participant import Participant
from typing import Dict, List, Literal


class ParticipantAbstract(Participant):

    def __init__(self, participant: Participant, 
                 programming_level: Dict[str, Literal["Beginner", "Intermediate", "Advanced"]], 
                 processed_objective: Literal["Learn", "Fun", "Win", "Friends"], 
                 **kwargs):
        
        self.__dict__ = participant.__dict__.copy()
        self.programming_level = programming_level
        self.objective_abs = processed_objective