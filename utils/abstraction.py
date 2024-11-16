from participant import Participant
from ParticipantAbstract import ParticipantAbstract
from api_handler import extract_properties
from config.value_tables import YEAR_EXPERTISE_GAIN
from config.literals import OBJECTIVES
from config.api_key import API_KEY


def abstract_tryhard(participant: ParticipantAbstract) -> ParticipantAbstract:
    '''Abstracts the tryhardness of the participant'''
    
    objectives_abs = participant.objective_abs
    if "Win" in objectives_abs:
        win = True
    else:
        win = False

    if win:
        len_objectives = len(objectives_abs)
        if len_objectives == 1: # There is only win in the objectives
            tryhard_value = "Extreme"
        elif len_objectives == 2: # There is win and another objective
            tryhard_value = "Medium"
        elif len_objectives == 3: # There is win and two other objectives
            tryhard_value = "Low"
    else:
        tryhard_value = "None"

    participant.tryhard = tryhard_value
    return participant

def abstract_expertise(participant: ParticipantAbstract) -> ParticipantAbstract:
    '''Abstracts the expertise of the participant'''
    
    year = participant.year_of_study
    exp_level = participant.experience_level
    # Poc = 0, mig = 1, high = 2
    # 1o => +0
    # 2o => +1
    # 3o => +2
    # 4o => +3
    # M => +4
    # D => +6
    expertise = exp_level + YEAR_EXPERTISE_GAIN[year]
  
    
    participant.expertise = expertise
    return participant
    

    

    
    
    
    
    
    
def abstract_objective(participant: ParticipantAbstract) -> ParticipantAbstract:
    extract_properties(api_key= API_KEY,
                       user_text= participant.objective, 
                       properties= "objective",
                       cardinality = ['single']
    )