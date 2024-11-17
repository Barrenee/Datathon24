from config.literals import LANGUAGES
from utils.matchesCompulsory import find_obligatory_compatibles, init_tables, get_compatible_groups
from utils.abstraction import abstract_objective, abstract_expertise, abstract_tryhard, abstract_general, init_participant
from Group import Group
from participant import Participant, load_participants
from ParticipantAbstract import ParticipantAbstract
import json



data = json.load(open("data/datathon_participants.json", "r"))

g1 = init_participant(data[0])
g2 = init_participant(data[1])

all_groups = [g1, g2]

challenges_table, objectives_table, languages_table = init_tables(all_groups)

compatible_groups = get_compatible_groups(g1, challenges_table, objectives_table, languages_table)


print(compatible_groups)