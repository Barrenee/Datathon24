from config.literals import LANGUAGES
from utils.matchesCompulsory import find_obligatory_compatibles, init_tables, get_compatible_groups
from utils.abstraction import abstract_objective, abstract_expertise, abstract_tryhard, abstract_general, init_participant
from utils.matchesBasic import  roles_match, interests_match
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

g1.interests = ['Enterprise',"Health", 'Blockchain']

matched_roles = roles_match(group=g1, compatible_groups=compatible_groups)
matched_interests = interests_match(group=g1, compatible_groups=compatible_groups)
print(g1.preferred_team_size, g2.preferred_team_size)
print(g1.roles_fullfilled, g2.roles_fullfilled)
print(g1.interests, g2.interests)
print(matched_roles)
print(matched_interests)