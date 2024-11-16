from participant import Participant
from ParticipantAbstract import ParticipantAbstract


def abstract_tryhard(participant: ParticipantAbstract) -> None:
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