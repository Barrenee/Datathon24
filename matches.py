from config.literals import LANGUAGES
from utils.utils import languages_match, objectives_match
from Group import Group
from participant import Participant, load_participants
from ParticipantAbstract import ParticipantAbstract
import json



data = json.load(open("data/datathon_participants.json", "r"))

pabs1 = ParticipantAbstract(Participant(**data[0]), {"python":"Beginner"}, set(["Learn"]))
pabs2 = ParticipantAbstract(Participant(**data[1]), {"python":"Intermediate"}, set(["Fun_Friends", "Learn"]))

g1 = Group(pabs1)
g2 = Group(pabs2)

all_groups = [g1, g2]
table_language = languages_match(all_groups)
table_objectives = objectives_match(all_groups)

compatibles = {}
for group in all_groups:
    compatibles[group] = set()
    language_set = set()
    objective_set = set()
    for language in group.preferred_languages:
        language_set = set(table_language[language]).union(language_set)
    
    for objective in group.objective_abs:
        objective_set = set(table_objectives[objective]).union(objective_set)

    compatibles[group] = language_set.intersection(objective_set)
    compatibles[group].remove(group)

# entee program -> assign to group / look for friends in group
# Texto juntado (obj intro technical future excitement fun fact) => LLM 
# OBJECTIVE_ABSTRACT => A partir de (obj intro technical future excitement fun fact) => "Win" "Fun" "Learn" "Friends"
# 

# ABSTRACCIÓN Tryhard: if win only => extreme
#                      if win +1 => medium
#                      if win +2 => low
#                      else      => none

# ABSTRACCIÓN Expertise: if year=> extreme


# MATCHES:

# -> 






print(compatibles)
print(table_language)
print(table_objectives)