from config.literals import LANGUAGES
from utils.utils import *
from Group import Group
from participant import Participant, load_participants
from ParticipantAbstract import ParticipantAbstract
import json


data = json.load(open("data/datathon_participants.json", "r"))

MOD: utils has languages_match and objective_match


pabs1 = ParticipantAbstract(Participant(**data[0]), {"python":"Beginner"}, "Learn")
pabs2 = ParticipantAbstract(Participant(**data[1]), {"python":"Intermediate"}, "Friends")

g1 = Group(pabs1)
g2 = Group(pabs2)

all_groups = [g1, g2]
table_language = languages_match(all_groups)
table_objectives = objectives_match(all_groups)
print(table_objectives)