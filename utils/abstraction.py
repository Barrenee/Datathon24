from participant import Participant
from ParticipantAbstract import ParticipantAbstract
from api_handler import extract_properties
from config.value_tables import YEAR_EXPERTISE_GAIN, EXPERIENCE_LEVEL_VALUE
from config.literals import OBJECTIVES
from config.api_key import API_KEY
import pickle as pkl
import os
from Group import Group


def init_participant(data_participant: ParticipantAbstract) -> Group:
    '''
    Initializes a participant, abstracts it and returns a group with it
    param: data_participant: string or json file ? the one that is in the datafile with particpants
    '''
    participant = data_participant
    participant_abstracted = abstract_general(participant)
    group = Group(participant_abstracted)
    return group

def abstract_general(participant: ParticipantAbstract) -> ParticipantAbstract:
    """
    Applies every abstraction rule in the corresponding order
    """
    participant = abstract_objective(participant)
    participant = abstract_expertise(participant)
    participant = abstract_tryhard(participant)
    return participant
    


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
    expertise = EXPERIENCE_LEVEL_VALUE[exp_level] + YEAR_EXPERTISE_GAIN[year]
  
    
    participant.expertise = expertise
    return participant

    
def abstract_objective(participant: ParticipantAbstract) -> ParticipantAbstract:
    if os.path.exists(f"./cache_participants/{participant.id}.pkl"):
        with open(f"./cache_participants/{participant.id}.pkl", "rb") as output_file:
            participant_cache = pkl.load(output_file)
            
            if participant_cache.objective_abs != []:
                participant.objective_abs = participant_cache.objective_abs
                return participant
    else:
        objective_abs_result = extract_properties(api_key= API_KEY,
                       user_text= participant.objective, 
                       properties= ["objective"],
                       cardinality = ['single'],
                       values_restriction=[OBJECTIVES]
                        )
        if not isinstance(objective_abs_result, list):
            participant.add_objective_abs(list(objective_abs_result))
        participant.add_objective_abs(objective_abs_result)

        with open(f"./cache_participants/{participant.id}.pkl", "wb") as output_file:
            pkl.dump(participant, output_file)
        return participant
