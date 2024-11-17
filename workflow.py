from config.literals import LANGUAGES
from utils.matchesCompulsory import languages_match, objectives_match, challenges_match, find_obligatory_compatibles, init_tables
from utils.abstraction import abstract_objective, abstract_expertise, abstract_tryhard, abstract_general, init_participant
from Group import Group
from participant import Participant, load_participants
from ParticipantAbstract import ParticipantAbstract
import json



data = json.load(open("data/datathon_participants.json", "r"))

g1 = init_participant(data[0])
g2 = init_participant(data[1])

all_groups = [g1, g2]

init_tables()

"""
table_language = languages_match(all_groups) # {language: [group1, group2, ...]}
table_objectives = objectives_match(all_groups) # {objective: [group1, group2, ...]}
table_challenges = challenges_match(all_groups) # {challenge: [group1, group2, ...]}
"""
obligatory_compatibles = find_obligatory_compatibles(all_groups, table_language, table_objectives, table_challenges)
# enter program -> assign to group / look for friends in group
# Texto juntado (obj intro technical future excitement fun fact) => LLM 
# OBJECTIVE_ABSTRACT => A partir de (obj intro technical future excitement fun fact) => "Win" "Fun" "Learn" "Friends"
# 

# ABSTRACCIÓN Tryhard: if win only => extreme
#                      if win +1 => medium
#                      if win +2 => low
#                      else      => none

# ABSTRACCIÓN Expertise: if year=> extreme


# MATCHES:

# -> BASIC MATCHES:

print(compatibles)
print(table_language)
print(table_objectives)