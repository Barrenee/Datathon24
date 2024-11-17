from config.literals import LANGUAGES
from utils.matchesCompulsory import find_obligatory_compatibles, init_tables, get_compatible_groups
from utils.abstraction import abstract_objective, abstract_expertise, abstract_tryhard, abstract_general, init_participant
from utils.matchesBasic import  roles_match, interests_match, programming_skills_match
from Group import Group
from participant import Participant, load_participants
from ParticipantAbstract import ParticipantAbstract
import json
from utils.k_best import maikelfunction



data = json.load(open("data/datathon_participants.json", "r"))


all_groups = []
for person in data[0:3]:
    all_groups.append(init_participant(Participant(**person)))

maikelfunction(all_groups, 2)